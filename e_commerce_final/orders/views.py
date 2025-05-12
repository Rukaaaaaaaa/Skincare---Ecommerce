from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CartItem, Order, OrderItem
from products.models import Product
from django.contrib import messages


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def update_cart_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.quantity = quantity
        item.save()
        return JsonResponse({'success': True, 'subtotal': item.subtotal()})
    return JsonResponse({'success': False})


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


@login_required
@require_POST
def checkout_view(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "Giỏ hàng trống!")
            return redirect('cart')

        full_name = request.POST['fullname']
        phone = request.POST['phone']
        province = request.POST['province']
        district = request.POST['district']
        ward = request.POST['ward']
        address_detail = request.POST['detail-address']
        payment_method = request.POST['payment-method']
        shipping_fee = int(request.POST.get('shipping_fee', 0))
        discount = int(request.POST.get('discount', 0))

        total = sum(item.subtotal() for item in cart_items) + shipping_fee - discount

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            province=province,
            district=district,
            ward=ward,
            address_detail=address_detail,
            payment_method=payment_method,
            shipping_fee=shipping_fee,
            discount=discount,
            total=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()
        messages.success(request, "Đặt hàng thành công!")
        return redirect('home')

    except Exception as e:
        messages.error(request, f"Đã xảy ra lỗi: {str(e)}")
        return redirect('checkout')
