from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_by_category, name='product_by_category'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
