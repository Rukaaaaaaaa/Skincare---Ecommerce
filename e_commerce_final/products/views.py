from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Dữ liệu liên quan giả định đã được liên kết trong model
    recommendations = product.recommendations.all() if hasattr(product, 'recommendations') else []
    related_products = product.related_products.all() if hasattr(product, 'related_products') else []

    # FAQ dạng danh sách dict nếu dùng JSONField
    faqs = product.faqs if hasattr(product, 'faqs') else []

    context = {
        'product': product,
        'product': {
            'name': product.name,
            'description': product.description,
            'detail': product.detail,
            'price': product.price,
            'original_price': product.original_price,
            'image': product.image,
            'rating': product.rating,
            'review_count': product.review_count,
            'sold_count': product.sold_count,
            'vouchers': product.vouchers,
            'combo': product.combo,
            'shipping': product.shipping,
            'features': product.features,
            'ingredients': product.ingredients,
            'how_to_use': product.how_to_use,
            'reviews': product.reviews,
            'faqs': faqs,
            'recommendations': recommendations,
            'related_products': related_products,
        }
    }

    return render(request, 'proDetail.html', context)
