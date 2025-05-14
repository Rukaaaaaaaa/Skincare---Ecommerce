from django.urls import path
from . import views
from django.contrib.auth import logout


urlpatterns = [
    # Trang chính
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Blog
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),

    # Newsletter
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # Tìm kiếm sản phẩm
    path('search/', views.search_view, name='search'),

    # Phân tích da ảo (AI quiz)
    path('virtual-analysis/quiz/ajax/', views.virtual_quiz_ajax, name='virtual_quiz_ajax'),

    # (Nếu dùng hiển thị chi tiết sản phẩm theo danh mục)
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('logout/', views.user_logout, name='logout'),
]
