import urllib.parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.cart.views import get_cart_items, save_cart, clear_coupon
from apps.catalog.models import ProductVariant, Promotion, CouponRedemption
from apps.core.models import SiteConfig
from .models import WhatsAppOrder, WhatsAppOrderItem


PAYMENT_METHOD_CHOICES = [
    ('transferencia', 'Transferencia bancaria'),
    ('nequi', 'Nequi / Daviplata'),
    ('mercadopago', 'Mercado Pago'),
    ('wompi', 'Wompi (tarjeta)'),
    ('otro', 'Otro (acordar por WhatsApp)'),
]


def checkout_form(request):
    """Render the checkout form. Login is optional - guests can checkout."""
    cart_data = get_cart_items(request)

    if not cart_data['items']:
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('cart:cart_detail')

    return render(request, 'orders/checkout.html', {
        'cart_data': cart_data,
        'payment_methods': PAYMENT_METHOD_CHOICES,
        'page_title': 'Finalizar compra',
    })


def checkout_whatsapp(request):
    cart_data = get_cart_items(request)

    if not cart_data['items']:
        return redirect('cart:cart_detail')

    user = request.user if request.user.is_authenticated else None

    shipping_address = (request.POST.get('shipping_address') or '').strip()
    shipping_city = (request.POST.get('shipping_city') or '').strip()
    shipping_department = (request.POST.get('shipping_department') or '').strip()
    shipping_notes = (request.POST.get('shipping_notes') or '').strip()
    customer_phone = (request.POST.get('customer_phone') or (user.phone if user else '')).strip()
    customer_name = (request.POST.get('customer_name') or (
        f"{user.first_name} {user.last_name}".strip() if user and (user.first_name or user.last_name)
        else (user.email if user else '')
    )).strip()
    customer_email = (request.POST.get('customer_email') or (user.email if user else '')).strip()
    payment_method = (request.POST.get('payment_method') or 'transferencia').strip()

    if not (shipping_address and shipping_city and shipping_department and customer_phone and customer_name and customer_email):
        messages.error(request, 'Completá todos los datos de envío para continuar.')
        return redirect('orders:checkout_form')

    try:
        with transaction.atomic():
            variant_ids = [item['variant_id'] for item in cart_data['items']]
            variants = {
                str(v.id): v
                for v in ProductVariant.objects.select_for_update().filter(id__in=variant_ids)
            }

            for item in cart_data['items']:
                variant = variants.get(item['variant_id'])
                if not variant:
                    raise ValueError(f"Variant {item['variant_id']} no longer exists")
                if variant.stock < item['quantity']:
                    size_label = f"Top {item.get('top_size', item.get('size'))} / Tanga {item.get('bottom_size', item.get('size'))}"
                    raise ValueError(
                        f"Stock insuficiente para {item['product_name']} ({item['color']} / {size_label}). "
                        f"Stock disponible: {variant.stock}"
                    )

            order = WhatsAppOrder.objects.create(
                user=user,
                customer_email=customer_email,
                customer_name=customer_name,
                customer_phone=customer_phone,
                status='pending',
                coupon_code=cart_data['coupon']['code'] if cart_data.get('coupon') else '',
                discount_amount=cart_data.get('discount', 0),
                shipping_address=shipping_address,
                shipping_city=shipping_city,
                shipping_department=shipping_department,
                shipping_notes=shipping_notes,
                payment_method=payment_method,
            )

            for item in cart_data['items']:
                variant = variants[item['variant_id']]
                size_label = f"Top {item.get('top_size', item.get('size'))} / Tanga {item.get('bottom_size', item.get('size'))}"
                WhatsAppOrderItem.objects.create(
                    order=order,
                    variant=variant,
                    product_name_snapshot=item['product_name'],
                    variant_snapshot=f"{item['color']} / {size_label}",
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                )
                variant.stock = F('stock') - item['quantity']
                variant.save(update_fields=['stock'])

            coupon = None
            if cart_data.get('coupon'):
                try:
                    coupon = Promotion.objects.get(code__iexact=cart_data['coupon']['code'])
                    coupon.usage_count = F('usage_count') + 1
                    coupon.save(update_fields=['usage_count'])
                    CouponRedemption.objects.create(
                        promotion=coupon,
                        user=user,
                        order=order,
                        code_used=coupon.code,
                        discount_applied=cart_data['discount'],
                    )
                except Promotion.DoesNotExist:
                    coupon = None

            lines = [
                "¡Hola! Quiero realizar un pedido en MARPLATA.",
                "",
                f"*Orden:* {order.order_number}",
                f"*Cliente:* {order.customer_name}",
                f"*Correo:* {order.customer_email}",
                f"*Teléfono:* {order.customer_phone}",
                "",
                "*Productos:*",
            ]

            for item in order.items.all():
                lines.append(
                    f"- {item.quantity} x {item.product_name_snapshot} ({item.variant_snapshot}) — ${item.subtotal:,.0f}"
                )

            order_subtotal = sum(float(item.subtotal) for item in order.items.all())

            lines.append("")
            lines.append(f"*Subtotal:* ${order_subtotal:,.0f}")

            if cart_data.get('discount', 0) > 0:
                lines.append(
                    f"*Descuento ({order.coupon_code}):* -${cart_data['discount']:,.0f}"
                )

            lines.append(f"*Total:* ${order.total_amount:,.0f}")
            lines.append("")
            lines.append("*Datos de envío:*")
            lines.append(f"{order.shipping_address}")
            lines.append(f"{order.shipping_city} · {order.shipping_department}")
            if order.shipping_notes:
                lines.append(f"Ref: {order.shipping_notes}")
            lines.append("")
            lines.append(f"*Pago:* {dict(PAYMENT_METHOD_CHOICES).get(order.payment_method, order.payment_method)}")
            lines.append("")
            lines.append("Por favor confirmame disponibilidad y medios de pago. ¡Gracias!")

            message = '\n'.join(lines)
            encoded_message = urllib.parse.quote(message)

            phone = SiteConfig.load().whatsapp_number or getattr(settings, 'MARPLATA_WHATSAPP_NUMBER', '')
            phone = ''.join(c for c in phone if c.isdigit())

            whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

            save_cart(request, {})
            clear_coupon(request)

            from apps.core.emails import send_order_confirmation, send_new_order_admin_notification
            order.refresh_from_db()
            send_order_confirmation(order)
            send_new_order_admin_notification(order)

            return redirect(whatsapp_url)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('cart:cart_detail')


def order_success(request, order_number):
    """Show order success page (fallback if WhatsApp redirect fails)."""
    if request.user.is_authenticated:
        order = WhatsAppOrder.objects.filter(
            order_number=order_number, user=request.user
        ).first()
    else:
        order = WhatsAppOrder.objects.filter(order_number=order_number).first()
    if not order:
        messages.error(request, 'Pedido no encontrado.')
        return redirect('home')

    return render(request, 'orders/order_success.html', {
        'order': order,
        'page_title': 'Pedido realizado',
    })


def order_tracking(request, order_number):
    """Public order tracking page (auth: must be the owner or admin)."""
    order = WhatsAppOrder.objects.filter(order_number=order_number).first()
    if not order:
        from django.http import Http404
        raise Http404('Pedido no encontrado')

    if request.user.is_authenticated and request.user.is_staff:
        pass
    elif request.user.is_authenticated and order.user_id == request.user.id:
        pass
    else:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('No tienes permiso para ver este pedido.')

    items = order.items.all().select_related('variant__product')
    return render(request, 'orders/order_tracking.html', {
        'order': order,
        'items': items,
        'page_title': f'Pedido #{order.order_number}',
    })


def tracking_lookup(request):
    """Form to look up an order by order_number + email (no login required)."""
    order = None
    error = None
    if request.method == 'POST':
        order_number = (request.POST.get('order_number') or '').strip()
        email = (request.POST.get('email') or '').strip().lower()
        if not (order_number and email):
            error = 'Ingresá el número de pedido y el correo.'
        else:
            order = WhatsAppOrder.objects.filter(
                order_number=order_number, customer_email__iexact=email
            ).first()
            if not order:
                error = 'No encontramos un pedido con esos datos. Verificá el número y el correo.'
    return render(request, 'orders/tracking_lookup.html', {
        'order': order,
        'error': error,
        'page_title': 'Rastrear mi pedido',
    })


def build_whatsapp_message(order):
    """Helper to rebuild WhatsApp message for an existing order."""
    lines = [
        f"¡Hola! Quiero realizar un pedido en MARPLATA.",
        f"",
        f"*Orden:* {order.order_number}",
        f"*Cliente:* {order.customer_name}",
        f"*Correo:* {order.customer_email}",
        f"*Teléfono:* {order.customer_phone or 'Por confirmar'}",
        f"",
        f"*Productos:*",
    ]

    total = 0
    for item in order.items.all():
        lines.append(
            f"- {item.quantity} x {item.product_name_snapshot} ({item.variant_snapshot}) — ${item.subtotal:,.0f}"
        )
        total += float(item.subtotal)

    lines.extend([
        f"",
        f"*Total:* ${total:,.0f}",
        f"",
        f"Por favor confirmame disponibilidad y medios de pago. ¡Gracias!",
    ])

    return '\n'.join(lines)
