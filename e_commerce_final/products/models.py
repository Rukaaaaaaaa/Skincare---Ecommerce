from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class Product(models.Model):
    LABEL_CHOICES = [
        ('best_seller', 'Best Seller'),
        ('new', 'New Arrival'),
        ('other', 'Other'),
        ('models', 'Models'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    detail = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

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

    label = models.CharField(
        max_length=20,
        choices=LABEL_CHOICES,
        default='other',
        help_text="Gắn nhãn để hiển thị ở mục đặc biệt (Best Seller, New Arrival)"
    )

    def __str__(self):
        return self.name
