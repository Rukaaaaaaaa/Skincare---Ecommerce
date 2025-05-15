from django.urls import path
from . import views
from .views import add_to_cart_ajax

urlpatterns = [
    # Giỏ hàng
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # Thanh toán
    path('checkout/', views.checkout_page, name='checkout'),
    path('checkout/submit/', views.checkout_view, name='checkout_submit'),

    # Ajax
    path('cart/ajax/add/', add_to_cart_ajax, name='add_to_cart_ajax'),

]
