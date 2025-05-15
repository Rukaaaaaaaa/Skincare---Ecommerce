from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'category', 'author')
    list_filter = ('category', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
