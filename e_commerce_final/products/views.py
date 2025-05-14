from django.shortcuts import render, get_object_or_404
from .models import Product, Category



def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_ids = request.GET.getlist('category')
    if category_ids:
        products = products.filter(category__id__in=category_ids)

    in_stock = request.GET.get('in_stock') == '1'
    if in_stock:
        products = products.filter(sold_count__lt=100)

    price_range = request.GET.get('price')
    if price_range == '1':
        products = products.filter(price__lt=50000)
    elif price_range == '2':
        products = products.filter(price__gte=50000, price__lte=100000)
    elif price_range == '3':
        products = products.filter(price__gt=100000)

    return render(request, 'product.html', {
        'products': products,
        'categories': categories,
        'selected_price': price_range,
        'selected_categories': category_ids,
        'in_stock': in_stock,
    })

    
def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()  # Để hiển thị danh sách danh mục bên sidebar nếu cần
    return render(request, 'product.html', {
        'products': products,
        'selected_category': category,
        'categories': categories,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    vouchers = product.vouchers.split(',') if product.vouchers else []

    return render(request, 'proDetail.html', {
        'product': product,
        'vouchers': vouchers,
        })
