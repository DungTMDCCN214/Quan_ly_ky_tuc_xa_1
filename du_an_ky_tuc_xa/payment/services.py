# payment/services.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_payment_reminder(payment, request=None):
    """Gửi email nhắc nhở thanh toán"""
    student = payment.contract.student
    context = {
        'student_name': student.full_name or student.user.get_full_name(),
        'payment_id': payment.id,
        'amount': payment.amount,
        'due_date': payment.due_date,
        'notes': payment.notes or "Tiền thuê phòng ký túc xá",
    }
    
    # Tạo payment URL
    if request:
        context['payment_url'] = request.build_absolute_uri(f'/payments/{payment.id}/')
    else:
        context['payment_url'] = f'http://localhost:8000/payments/{payment.id}/'
    
    # Render template
    html_content = render_to_string('payment/email/payment_reminder.html', context)
    text_content = strip_tags(html_content)
    
    # Tạo email
    subject = f"🔔 Thông báo thanh toán hóa đơn #{payment.id}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [student.user.email]
    
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e:
        print(f"Lỗi gửi email: {e}")
        return False