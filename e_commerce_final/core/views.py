from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Category, Product, Blog, SpecialOffer, NewsletterSubscriber

# Trang chủ
def home(request):
    context = {
        # Hero slider: dùng 3 sản phẩm mới nhất
        'hero_slides': Product.objects.filter(label='new')[:3],

        # Danh mục sản phẩm
        'categories': Category.objects.all(),

        # Best sellers: lấy sản phẩm được gắn nhãn best_seller
        'best_sellers': Product.objects.filter(label='best_seller')[:8],

        # New In: sản phẩm được gắn nhãn new
        'new_products': Product.objects.filter(label='new')[:6],

        # Ưu đãi đặc biệt
        'special_offer': SpecialOffer.objects.first(),

        # Blog mới nhất
        'blog_posts': Blog.objects.order_by('-date')[:3],
    }
    return render(request, 'homepage.html', context)

# Danh sách blog
def blog_list(request):
    blogs = Blog.objects.order_by('-date')
    return render(request, 'blog.html', {'blogs': blogs})

# Chi tiết blog
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

# Trang Giới thiệu
def about(request):
    return render(request, 'about.html')

# Trang Liên hệ
def contact(request):
    return render(request, 'contactus.html')

# Đăng ký nhận bản tin (newsletter)
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                subscriber.subscribed_at = timezone.now()
                subscriber.save()
                return JsonResponse({'status': 'success', 'message': 'Đăng ký thành công!'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Email đã tồn tại!'})
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ.'})
