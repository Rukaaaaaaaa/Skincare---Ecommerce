from django.db import models

# Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


# Sản phẩm
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('best_seller', 'Best Seller'),
        ('new', 'New Product'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    label = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return f"{self.name} ({self.get_label_display()})"


# Bài viết blog
class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.author}"


# Ưu đãi đặc biệt
class SpecialOffer(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    highlight = models.TextField()
    image = models.ImageField(upload_to='offers/')

    def __str__(self):
        return self.title

# Người đăng ký nhận bản tin
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
