from django.contrib import admin
from .models import Product, Category  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'original_price', 'rating',
        'review_count', 'sold_count', 'label', 'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('rating', 'label', 'category')
    list_editable = ('price', 'original_price', 'sold_count', 'label', 'category')
    filter_horizontal = ('related_products','recommendations')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'description', 'detail', 'image', 'label', 'category')  
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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
