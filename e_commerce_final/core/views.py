from django.shortcuts import render
from products.models import Product, Category, Slide
from blog.models import BlogPost

def home(request):

    slides = Slide.objects.all().order_by('order')
    categories = Category.objects.all()
    best_sellers = Product.objects.filter(is_best_seller=True)
    new_products = Product.objects.filter(is_new=True).order_by('-created_at')[:6]
    special_offer = Product.objects.filter(is_special_offer=True).first()
    blog_posts = BlogPost.objects.all().order_by('-created_at')[:3]

    context = {
        'slides': slides,
        'categories': categories,
        'best_sellers': best_sellers,
        'new_products': new_products,
        'special_offer': special_offer,
        'blog_posts': blog_posts,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contactus.html')
