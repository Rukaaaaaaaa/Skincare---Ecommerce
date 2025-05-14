from django.db import models
from products.models import Product  # Để kết nối sản phẩm với kết quả AI
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)  # Thêm trích đoạn
    image = models.ImageField(upload_to='blogs/')
    category = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)  # Gán mặc định là ngày hiện tại

    def __str__(self):
        return f"{self.title} - {self.author}"

    def save(self, *args, **kwargs):
        # Tự động tạo excerpt nếu chưa có
        if not self.excerpt:
            self.excerpt = Truncator(self.content).chars(150, truncate='...')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date'] 

from django.db import models

class SpecialOffer(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    highlight = models.TextField()
    image = models.ImageField(upload_to='offers/')
    is_active = models.BooleanField(default=False, help_text="Đánh dấu ưu đãi đang hiển thị trên trang chủ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Special Offer"
        verbose_name_plural = "Special Offers"



# Phân tích chăm sóc da ảo (hiển thị trên trang chủ)
class VirtualAnalysis(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='analysis/')
    qr_code = models.ImageField(upload_to='analysis_qr/')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Kết quả phân tích AI từ khảo sát
class AnalysisResult(models.Model):
    user_input = models.JSONField(help_text="Danh sách câu trả lời từ người dùng (7 câu)")
    ai_recommendation = models.TextField(help_text="Phân tích tổng hợp từ AI")
    keywords = models.JSONField(help_text="Các từ khóa liên quan đến sản phẩm gợi ý")
    recommended_products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='analysis_results',
        help_text="Các sản phẩm được AI gợi ý dựa trên từ khóa"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Result #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Người đăng ký nhận bản tin
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
