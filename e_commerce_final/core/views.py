from django.shortcuts import render
from .models import Category, Product, Blog, SpecialOffer

def homepage(request):
    categories = Category.objects.all()
    best_sellers = Product.objects.filter(label='best_seller')
    new_products = Product.objects.filter(label='new')
    blogs = Blog.objects.all().order_by('-date')[:3]  # Lấy 3 blog mới nhất
    special_offer = SpecialOffer.objects.first()  # Lấy ưu đãi đặc biệt đầu tiên

    context = {
        'categories': categories,
        'best_sellers': best_sellers,
        'new_products': new_products,
        'blogs': blogs,
        'special_offer': special_offer,
    }

    return render(request, 'homepage.html', context)
