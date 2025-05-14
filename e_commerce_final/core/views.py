from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Category
from .models import Blog, SpecialOffer, NewsletterSubscriber, VirtualAnalysis, AnalysisResult
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Trang chủ
def home(request):
    context = {
        'hero_slides': Product.objects.filter(label='models')[:3],
        'categories': Category.objects.all(),
        'best_sellers': Product.objects.filter(label='best_seller')[:8],
        'new_products': Product.objects.filter(label='new')[:6],
        'special_offer': SpecialOffer.objects.first(),
        'latest_posts': Blog.objects.order_by('-date')[:3],
        'analysis': VirtualAnalysis.objects.filter(is_active=True).first()
    }
    return render(request, 'homepage.html', context)


# Trang Giới thiệu
def about(request):
    return render(request, 'about.html')


# Trang Liên hệ
def contact(request):
    return render(request, 'contactus.html')

from django.core.paginator import Paginator

def blog_list(request):
    blog_list = Blog.objects.order_by('-date')
    paginator = Paginator(blog_list, 6)  # mỗi trang 6 bài
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'blog.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    related_posts = Blog.objects.filter(category=blog.category).exclude(id=blog.id)[:3]
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'related_posts': related_posts
    })
def user_logout(request):
    logout(request)
    return redirect('home') 


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                subscriber.subscribed_at = timezone.now()
                consent = request.POST.get('consent') == 'on'
                subscriber.consent = consent
                subscriber.save()
                messages.success(request, "Đăng ký thành công! ❤️")
            else:
                messages.info(request, "Email đã tồn tại! 💌")
        else:
            messages.error(request, "Vui lòng nhập email hợp lệ.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # quay về trang gốc
    else:
        return redirect('home')



# Tìm kiếm sản phẩm
def search_view(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'query': query, 'results': results})


# Hiển thị sản phẩm theo danh mục
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'category_products.html', {'category': category, 'products': products})


# Lấy API key từ biến môi trường

@csrf_exempt
def virtual_quiz_ajax(request):
    if request.method == 'POST':
        try:
            # Parse dữ liệu từ JSON nếu dùng JS fetch (frontend)
            data = json.loads(request.body)

            answers = {
                "skin_type": data.get("answers")[0],
                "concern": data.get("answers")[1],
                "cleanse_frequency": data.get("answers")[2],
                "sunscreen": data.get("answers")[3],
                "fragrance_free": data.get("answers")[4],
                "active_ingredients": data.get("answers")[5],
                "routine_level": data.get("answers")[6],
            }

            if any(value is None or value.strip() == '' for value in answers.values()):
                return JsonResponse({'error': 'Vui lòng trả lời đầy đủ 7 câu hỏi.'}, status=400)

            # --- Gửi Prompt đến OpenAI ---
            prompt = (
                f"Tôi có làn da {answers['skin_type']}, vấn đề chính là {answers['concern']}. "
                f"Tôi rửa mặt {answers['cleanse_frequency']} mỗi ngày, dùng kem chống nắng: {answers['sunscreen']}. "
                f"Tôi thích sản phẩm không mùi: {answers['fragrance_free']}, đang dùng: {answers['active_ingredients']}. "
                f"Routine hiện tại: {answers['routine_level']}. "
                f"Hãy đề xuất routine skincare phù hợp và các thành phần nên tìm trong sản phẩm (bằng tiếng Việt)."
            )

            response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia tư vấn chăm sóc da."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500)

            recommendation_text = response.choices[0].message.content

            # --- Trích xuất từ khóa đơn giản ---
            keywords_raw = ["Niacinamide", "Hyaluronic", "Retinol", "Vitamin C", "Ceramide", "Salicylic", "fragrance-free", "SPF", "green tea", "acne"]
            keywords = [kw for kw in keywords_raw if kw.lower() in recommendation_text.lower()]

            # --- Tìm sản phẩm theo từ khóa ---
            recommended_products = Product.objects.none()
            for kw in keywords:
                recommended_products |= Product.objects.filter(description__icontains=kw)

            # --- Lưu kết quả vào DB ---
            result = AnalysisResult.objects.create(
                user_input=answers,
                ai_recommendation=recommendation_text,
                keywords=keywords
            )
            result.recommended_products.set(recommended_products.distinct()[:10])

            # --- Chuẩn bị dữ liệu JSON trả về ---
            recommended_data = [
                {
                    'id': p.id,
                    'name': p.name,
                    'image': p.image.url if p.image else '',
                    'price': p.price,
                } for p in recommended_products.distinct()[:5]
            ]

            return JsonResponse({
                'recommendation': recommendation_text,
                'products': recommended_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
