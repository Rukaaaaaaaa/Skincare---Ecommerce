from django.contrib import admin
from products.models import Product, Category
from .models import (
    Blog,
    SpecialOffer,
    NewsletterSubscriber,
    VirtualAnalysis,
    AnalysisResult
)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'author', 'content')
    ordering = ('-date',)
    date_hierarchy = 'date'



@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle', 'description', 'highlight')
    list_editable = ('is_active',)
    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


@admin.register(VirtualAnalysis)
class VirtualAnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'qr_code', 'is_active')
        }),
    )


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'ai_recommendation_summary')
    search_fields = ('ai_recommendation',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('recommended_products',)
    
    fieldsets = (
        ("AI Analysis Result", {
            'fields': (
                'user_input',
                'ai_recommendation',
                'keywords',
                'recommended_products',
                'created_at',
            )
        }),
    )

    def ai_recommendation_summary(self, obj):
        return obj.ai_recommendation[:60] + "..." if obj.ai_recommendation else "-"
    ai_recommendation_summary.short_description = "AI Recommendation"
    ai_recommendation_summary.admin_order_field = 'ai_recommendation'
