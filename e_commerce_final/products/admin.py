from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'rating', 'review_count', 'sold_count')
    search_fields = ('name', 'description')
    list_filter = ('rating',)

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'description', 'detail', 'image')
        }),
        ('Giá & Số lượng', {
            'fields': ('price', 'original_price', 'sold_count')
        }),
        ('Đánh giá & Mã giảm giá', {
            'fields': ('rating', 'review_count', 'vouchers', 'combo', 'shipping')
        }),
        ('Thông tin sản phẩm', {
            'fields': ('features', 'ingredients', 'how_to_use', 'reviews')
        }),
        ('FAQ', {
            'fields': ('faqs',),
            'description': "Nhập dưới dạng JSON: [{'question': 'Câu hỏi?', 'answer': 'Trả lời.'}]"
            
        }),
        ('Sản phẩm liên quan', {
            'fields': ('recommendations', 'related_products')
        }),
    )
