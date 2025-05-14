from django.contrib import admin
from .models import CartItem, Order, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')
    extra = 0

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'phone', 'total',
        'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)

    fieldsets = (
        ("Thông tin khách hàng", {
            'fields': ('full_name', 'phone', 'address_detail')
        }),
        ("Tóm tắt đơn hàng", {
            'fields': ('shipping_fee', 'discount', 'total', 'status')
        }),
        ("Thời gian", {
            'fields': ('created_at', 'updated_at')
        }),
    )
