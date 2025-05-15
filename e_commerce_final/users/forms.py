from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # nếu em dùng model mở rộng

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'full_name', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'phone': 'Số điện thoại',
            'full_name': 'Họ và tên',
            }