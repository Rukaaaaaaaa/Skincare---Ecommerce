from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from .models import CartItem, Order, OrderItem
from products.models import Product
from django.db.models import Sum


@require_POST
@login_required
def add_to_cart_ajax(request):
    data = json.loads(request.body)
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found"}, status=404)

    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    item.quantity += quantity
    item.save()

    total = CartItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))["total"] or 0
    return JsonResponse({"success": True, "cart_count": total})

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.GET.get('qty', 1))

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity += quantity
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_items = CartItem.objects.filter(user=request.user).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        return JsonResponse({'success': True, 'cart_count': total_items})

    next_url = request.GET.get('next') or reverse('cart')
    return redirect(next_url)




@login_required
@require_POST
def update_cart_quantity(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))

    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity = quantity
    item.save()

    return redirect('cart')


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


@login_required
def checkout_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    if not cart_items.exists():
        messages.warning(request, "Giỏ hàng của bạn đang trống.")
        return redirect('cart')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
@require_POST
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Giỏ hàng trống!")
        return redirect('cart')

    try:
        # Lấy dữ liệu từ form
        full_name = request.POST.get('fullname', '').strip()
        phone = request.POST.get('phone', '').strip()
        province = request.POST.get('province', '').strip()
        district = request.POST.get('district', '').strip()
        ward = request.POST.get('ward', '').strip()
        address_detail = request.POST.get('detail_address', '').strip()
        payment_method = request.POST.get('payment_method')
        shipping_fee = int(request.POST.get('shipping_fee', 0))
        discount = int(request.POST.get('discount', 0))
        total = int(request.POST.get('total', 0))

        # Kiểm tra bắt buộc
        if not (full_name and phone and province and district and ward and address_detail and payment_method):
            messages.error(request, "Vui lòng điền đầy đủ thông tin giao hàng.")
            return redirect('checkout')

        # Kiểm tra số điện thoại hợp lệ
        import re
        if not re.match(r"^0\d{9}$", phone):
            messages.error(request, "Số điện thoại không hợp lệ. Vui lòng nhập đúng định dạng 10 số.")
            return redirect('checkout')

        # Tạo đơn hàng
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            province=province,
            district=district,
            ward=ward,
            address_detail=address_detail,
            shipping_fee=shipping_fee,
            discount=discount,
            total=total,
            payment_method=payment_method
        )

        # Thêm sản phẩm vào đơn hàng
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Xóa giỏ hàng
        cart_items.delete()

        # Gửi email xác nhận
        send_mail(
            subject="Xác nhận đơn hàng BEAUTYA",
            message=f"Cảm ơn {full_name}, bạn đã đặt hàng thành công.\nMã đơn hàng: #{order.id}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True
        )

        messages.success(request, "Đặt hàng thành công! Vui lòng kiểm tra email để xác nhận.")
        return redirect('cart')

    except Exception as e:
        messages.error(request, f"Đã xảy ra lỗi: {str(e)}")
        return redirect('checkout')