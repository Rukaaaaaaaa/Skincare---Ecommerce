from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công. Vui lòng đăng nhập.")
            return redirect('login')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'dangky.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # có thể là email
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # chỉnh đúng tên url của trang chủ
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    return render(request, 'Login.html')
