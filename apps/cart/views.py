from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from apps.catalog.models import ProductVariant, Promotion


def get_cart(request):
    """Return cart dict from session."""
    cart = request.session.get('cart', {})
    return cart


def save_cart(request, cart):
    """Save cart dict to session."""
    request.session['cart'] = cart
    request.session.modified = True


def get_cart_items(request):
    """Return list of cart items with variant data."""
    cart = get_cart(request)
    items = []
    subtotal = 0
    total_items = 0

    for variant_id, item_data in cart.items():
        try:
            variant = ProductVariant.objects.select_related('product').get(
                id=variant_id, is_active=True
            )
            quantity = item_data.get('quantity', 1)
            unit_price = variant.final_price
            item_subtotal = unit_price * quantity
            subtotal += item_subtotal
            total_items += quantity

            primary_image = None
            if variant.images.exists():
                primary_image = variant.images.first().image.url

            items.append({
                'variant_id': str(variant.id),
                'product_name': variant.product.name,
                'product_slug': variant.product.slug,
                'color': variant.color,
                'size': variant.size,
                'quantity': quantity,
                'unit_price': float(unit_price),
                'subtotal': float(item_subtotal),
                'stock': variant.stock,
                'image_url': primary_image,
            })
        except ProductVariant.DoesNotExist:
            continue

    coupon = get_active_coupon(request)
    discount = 0
    coupon_data = None
    if coupon and subtotal > 0:
        valid, _ = coupon.is_valid(subtotal)
        if valid:
            discount = coupon.calculate_discount(subtotal)
            coupon_data = {
                'code': coupon.code,
                'name': coupon.name,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
            }
        else:
            clear_coupon(request)

    total = max(0, subtotal - discount)

    return {
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'total_items': total_items,
        'coupon': coupon_data,
    }


def get_active_coupon(request):
    """Return active Promotion coupon from session, or None."""
    code = request.session.get('coupon_code')
    if not code:
        return None
    try:
        return Promotion.objects.get(code__iexact=code)
    except Promotion.DoesNotExist:
        return None


def clear_coupon(request):
    request.session.pop('coupon_code', None)
    request.session.modified = True


@require_POST
def cart_add(request):
    """Add a variant to the cart."""
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    if not variant_id:
        return JsonResponse({'error': 'variant_id is required'}, status=400)

    try:
        variant = ProductVariant.objects.get(id=variant_id, is_active=True)
    except ProductVariant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)

    if variant.stock <= 0:
        return JsonResponse({'error': 'Out of stock'}, status=400)

    if quantity > variant.stock:
        return JsonResponse({'error': 'Not enough stock'}, status=400)

    if quantity < 1:
        return JsonResponse({'error': 'Invalid quantity'}, status=400)

    cart = get_cart(request)
    variant_id_str = str(variant_id)

    if variant_id_str in cart:
        new_quantity = cart[variant_id_str]['quantity'] + quantity
        if new_quantity > variant.stock:
            return JsonResponse({'error': 'Not enough stock'}, status=400)
        cart[variant_id_str]['quantity'] = new_quantity
    else:
        cart[variant_id_str] = {'quantity': quantity}

    save_cart(request, cart)
    cart_data = get_cart_items(request)

    return JsonResponse({
        'success': True,
        'message': f'{variant.product.name} ({variant.color} / {variant.size}) added to cart',
        'total_items': cart_data['total_items'],
        'subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total': cart_data['total'],
        'coupon': cart_data['coupon'],
    })


@require_POST
def cart_remove(request):
    """Remove a variant from the cart."""
    variant_id = request.POST.get('variant_id')

    if not variant_id:
        return JsonResponse({'error': 'variant_id is required'}, status=400)

    cart = get_cart(request)
    variant_id_str = str(variant_id)

    if variant_id_str in cart:
        del cart[variant_id_str]
        save_cart(request, cart)

    cart_data = get_cart_items(request)

    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart',
        'total_items': cart_data['total_items'],
        'subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total': cart_data['total'],
        'coupon': cart_data['coupon'],
    })


@require_POST
def cart_update(request):
    """Update quantity of a variant in the cart."""
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    if not variant_id:
        return JsonResponse({'error': 'variant_id is required'}, status=400)

    cart = get_cart(request)
    variant_id_str = str(variant_id)

    if variant_id_str not in cart:
        return JsonResponse({'error': 'Item not in cart'}, status=404)

    if quantity <= 0:
        del cart[variant_id_str]
        save_cart(request, cart)
        cart_data = get_cart_items(request)
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'total_items': cart_data['total_items'],
            'subtotal': cart_data['subtotal'],
            'discount': cart_data['discount'],
            'total': cart_data['total'],
            'coupon': cart_data['coupon'],
        })

    try:
        variant = ProductVariant.objects.get(id=variant_id, is_active=True)
        if quantity > variant.stock:
            return JsonResponse({'error': 'Not enough stock'}, status=400)
    except ProductVariant.DoesNotExist:
        del cart[variant_id_str]
        save_cart(request, cart)
        cart_data = get_cart_items(request)
        return JsonResponse({
            'success': True,
            'message': 'Variant no longer available, removed from cart',
            'total_items': cart_data['total_items'],
            'subtotal': cart_data['subtotal'],
            'discount': cart_data['discount'],
            'total': cart_data['total'],
            'coupon': cart_data['coupon'],
        })

    cart[variant_id_str]['quantity'] = quantity
    save_cart(request, cart)
    cart_data = get_cart_items(request)

    item = next((i for i in cart_data['items'] if i['variant_id'] == variant_id_str), None)

    return JsonResponse({
        'success': True,
        'message': 'Cart updated',
        'subtotal': item['subtotal'] if item else 0,
        'total_items': cart_data['total_items'],
        'cart_subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total': cart_data['total'],
        'coupon': cart_data['coupon'],
    })


@require_GET
def cart_summary(request):
    """Return cart summary as JSON (for navbar counter)."""
    cart_data = get_cart_items(request)
    return JsonResponse(cart_data)


def cart_detail(request):
    """Display cart page."""
    cart_data = get_cart_items(request)

    return render(request, 'cart/cart_detail.html', {
        'items': cart_data['items'],
        'subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total': cart_data['total'],
        'coupon': cart_data['coupon'],
        'total_items': cart_data['total_items'],
        'page_title': 'Carrito de compras',
    })


@require_POST
def coupon_apply(request):
    """Apply a coupon code to the cart."""
    code = (request.POST.get('code') or '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'Ingresa un código.'}, status=400)

    try:
        promotion = Promotion.objects.get(code__iexact=code)
    except Promotion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Código no válido.'}, status=404)

    cart_data = get_cart_items(request)
    valid, error = promotion.is_valid(cart_data['subtotal'])
    if not valid:
        return JsonResponse({'success': False, 'error': error}, status=400)

    request.session['coupon_code'] = promotion.code
    request.session.modified = True

    cart_data = get_cart_items(request)
    return JsonResponse({
        'success': True,
        'message': f'¡Cupón "{promotion.code}" aplicado!',
        'discount': cart_data['discount'],
        'total': cart_data['total'],
        'subtotal': cart_data['subtotal'],
        'coupon': cart_data['coupon'],
    })


@require_POST
def coupon_remove(request):
    """Remove the active coupon."""
    clear_coupon(request)
    cart_data = get_cart_items(request)
    return JsonResponse({
        'success': True,
        'message': 'Cupón eliminado.',
        'discount': 0,
        'total': cart_data['total'],
        'subtotal': cart_data['subtotal'],
        'coupon': None,
    })
