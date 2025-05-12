from django.contrib import admin
from .models import CartItem, Order, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'payment_method', 'total', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('full_name', 'phone')
    inlines = [OrderItemInline]
