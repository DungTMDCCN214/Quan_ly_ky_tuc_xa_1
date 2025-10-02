# payment/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from dormitory.models import Contract
from .forms import PaymentForm

@login_required
def payment_list(request):
    """Danh sách thanh toán"""
    if request.user.user_type == 'student':
        student = request.user.student
        contracts = Contract.objects.filter(student=student)
        payments = Payment.objects.filter(contract__in=contracts).select_related('contract__student', 'contract__room')
    else:
        payments = Payment.objects.all().select_related('contract__student', 'contract__room')
    
    # Thống kê
    total_pending = payments.filter(status='pending').count()
    total_paid = payments.filter(status='paid').count()
    total_amount = sum(p.amount for p in payments.filter(status='paid'))
    
    context = {
        'payments': payments,
        'stats': {
            'total_pending': total_pending,
            'total_paid': total_paid,
            'total_amount': total_amount,
        }
    }
    return render(request, 'payment/payment_list.html', context)

@login_required
def payment_create(request):
    """Tạo hóa đơn thanh toán (chỉ quản lý)"""
    if request.user.user_type == 'student':
        messages.error(request, "Bạn không có quyền tạo hóa đơn!")
        return redirect('payment_list')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"Đã tạo hóa đơn #{payment.id} thành công!")
            return redirect('payment_list')
    else:
        form = PaymentForm()
    
    return render(request, 'payment/payment_form.html', {'form': form})

@login_required
def payment_detail(request, pk):
    """Chi tiết thanh toán"""
    payment = get_object_or_404(Payment, pk=pk)
    
    # Kiểm tra quyền xem
    if request.user.user_type == 'student' and payment.contract.student.user != request.user:
        messages.error(request, "Bạn không có quyền xem hóa đơn này!")
        return redirect('payment_list')
    
    return render(request, 'payment/payment_detail.html', {'payment': payment})

@login_required 
def payment_update(request, pk):
    """Cập nhật trạng thái thanh toán (chỉ quản lý)"""
    if request.user.user_type == 'student':
        messages.error(request, "Bạn không có quyền cập nhật thanh toán!")
        return redirect('payment_list')
    
    payment = get_object_or_404(Payment, pk=pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật hóa đơn #{payment.id}!")
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    
    return render(request, 'payment/payment_form.html', {'form': form})

# payment/views.py - THÊM FUNCTION
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .services import send_payment_reminder

def send_reminder(request, pk):
    """Gửi email nhắc nhở cho hóa đơn cụ thể"""
    if request.user.user_type == 'student':
        messages.error(request, "Bạn không có quyền gửi email!")
        return redirect('payment_list')
    
    payment = get_object_or_404(Payment, pk=pk)
    
    if send_payment_reminder(payment, request):
        messages.success(request, f'✅ Đã gửi email nhắc nhở cho HĐ #{payment.id}!')
    else:
        messages.error(request, '❌ Gửi email thất bại!')
    
    return redirect('admin:payment_payment_changelist')