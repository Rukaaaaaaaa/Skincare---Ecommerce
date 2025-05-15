from django.db import models
from django.conf import settings
from products.models import Product

# ==============================
# 1. Giỏ hàng (CartItem)
# ==============================
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi hàng'),
        ('done', 'Hoàn tất'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    province = models.CharField(max_length=255, default='')
    district = models.CharField(max_length=255, default='')
    ward = models.CharField(max_length=255, default='')
    address_detail = models.CharField(max_length=255, default='')


    shipping_fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField()

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.get_status_display()})"

    def full_address(self):
        return f"{self.address_detail}, {self.ward}, {self.district}, {self.province}"

    def item_count(self):
        return sum(item.quantity for item in self.items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()  # Giá tại thời điểm đặt hàng

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name if self.product else '[Đã xóa]'} x {self.quantity}"