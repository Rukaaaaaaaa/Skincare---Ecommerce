from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    detail = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    
    rating = models.FloatField(default=5.0)
    review_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    
    vouchers = models.CharField(max_length=255, blank=True, help_text="Cách nhau bởi dấu phẩy, ví dụ: GIAM10K,FREESHIP")
    combo = models.CharField(max_length=255, blank=True)
    shipping = models.CharField(max_length=255, blank=True)

    features = models.TextField(blank=True, help_text="Mỗi dòng là một tính năng nổi bật")
    ingredients = models.TextField(blank=True)
    how_to_use = models.TextField(blank=True)
    reviews = models.TextField(blank=True)

    faqs = models.JSONField(default=list, blank=True, help_text="Danh sách câu hỏi & trả lời. VD: [{'question': 'Q?', 'answer': 'A.'}]")

    recommendations = models.ManyToManyField('self', symmetrical=False, related_name='recommended_by', blank=True)
    related_products = models.ManyToManyField('self', symmetrical=False, related_name='related_to', blank=True)

    def __str__(self):
        return self.name
