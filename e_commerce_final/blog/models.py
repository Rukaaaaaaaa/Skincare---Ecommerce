from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    slug = models.SlugField(unique=True, max_length=255)
    excerpt = models.TextField(verbose_name="Tóm tắt ngắn", blank=True)
    content = models.TextField(verbose_name="Nội dung chi tiết")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Ảnh đại diện")
    category = models.CharField(max_length=100, verbose_name="Chuyên mục", default="Chăm Sóc Da")
    author = models.CharField(max_length=100, verbose_name="Tác giả", default="Admin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lúc")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"

    def __str__(self):
        return self.title
