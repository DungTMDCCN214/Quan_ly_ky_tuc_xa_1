
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dormitory.models import Student
from .models import CustomUser

def student_register(request):
    """Đăng ký tài khoản sinh viên"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        full_name = request.POST.get('full_name', '')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
            return render(request, 'accounts/student_register.html')
        
        # Tạo user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            user_type='student'
        )
        
        # Tạo student profile
        Student.objects.create(
            user=user,
            full_name=full_name
        )
        
        login(request, user)
        messages.success(request, "Đăng ký tài khoản thành công!")
        return redirect('student_dashboard')
    
    return render(request, 'accounts/student_register.html')

def student_login(request):
    """Đăng nhập cho sinh viên"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.user_type == 'student':
                login(request, user)
                messages.success(request, f"Chào mừng {username}!")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    form = AuthenticationForm()
    return render(request, 'accounts/student_login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from dormitory.models import Student, Contract, Room

def student_dashboard(request):
    """Dashboard cho sinh viên"""
    
    # Kiểm tra xác thực
    if not request.user.is_authenticated:
        messages.error(request, "Bạn cần đăng nhập để truy cập!")
        return redirect('login')
    
    # Kiểm tra user type
    if request.user.user_type != 'student':
        messages.error(request, "Bạn không có quyền truy cập!")
        return redirect('home')
    
    try:
        student = Student.objects.get(user=request.user)
        current_contract = Contract.objects.filter(student=student, status='active').first()
        available_rooms = Room.objects.filter(status='available')
        
        # Thêm context data
        context = {
            'student': student,
            'current_contract': current_contract,
            'available_rooms': available_rooms,
        }
        
        return render(request, 'student_dashboard.html', context)
        
    except Student.DoesNotExist:
        messages.error(request, "Thông tin sinh viên không tồn tại!")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {str(e)}")
        return redirect('home')

@login_required
def student_complete_profile(request):
    """Hoàn thiện hồ sơ sinh viên"""
    if request.user.user_type != 'student':
        return redirect('home')
    
    if request.method == 'POST':
        student_id = request.POST['student_id']
        university = request.POST['university']
        faculty = request.POST['faculty']
        course = request.POST['course']
        date_of_birth = request.POST.get('date_of_birth')
        
        student = Student.objects.get(user=request.user)
        student.student_id = student_id
        student.university = university
        student.faculty = faculty
        student.course = course
        if date_of_birth:
            student.date_of_birth = date_of_birth
        student.save()
        
        messages.success(request, "Cập nhật hồ sơ thành công!")
        return redirect('student_dashboard')
    
    return render(request, 'accounts/student_complete_profile.html')