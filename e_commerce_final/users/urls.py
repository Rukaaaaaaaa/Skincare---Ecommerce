from django.urls import path
from .views import register_view, login_view
from . import views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('profile/', views.profile_view, name='profile')
]
