from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import CustomUser, NewsletterSubscriber, WishlistItem


def _subscribe_to_newsletter(email, first_name='', user=None, source=''):
    """Subscribe an email to the newsletter if not already subscribed."""
    email = (email or '').strip().lower()
    if not email:
        return
    sub, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name or '',
            'user': user,
            'is_active': True,
            'source': source or '',
        },
    )
    if not created and not sub.is_active:
        sub.is_active = True
        sub.unsubscribed_at = None
        sub.save()


def login_view(request):
    """Custom login view using email as username."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'accounts/login.html', {'next': next_url})


def register_view(request):
    """Custom registration view."""
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        subscribe_newsletter = request.POST.get('newsletter') == 'on'

        errors = []
        if not email:
            errors.append('El correo electrónico es obligatorio.')
        if not first_name or not last_name:
            errors.append('El nombre y apellido son obligatorios.')
        if not password:
            errors.append('La contraseña es obligatoria.')
        elif password != password_confirm:
            errors.append('Las contraseñas no coinciden.')
        if CustomUser.objects.filter(email=email).exists():
            errors.append('Ya existe una cuenta con este correo.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/register.html', {
                'next': next_url,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'subscribe_newsletter': subscribe_newsletter,
            })

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        if subscribe_newsletter:
            _subscribe_to_newsletter(
                email=email,
                first_name=first_name,
                user=user,
                source='registro',
            )
        auth_login(request, user)
        messages.success(request, '¡Tu cuenta ha sido creada exitosamente!')

        from apps.core.emails import send_welcome_email
        try:
            send_welcome_email(user)
        except Exception:
            pass

        return redirect(next_url)

    return render(request, 'accounts/register.html', {'next': next_url})


def logout_view(request):
    auth_logout(request)
    return redirect('home')


def register_api(request):
    """AJAX registration endpoint used by footer form."""
    from django.http import JsonResponse

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    if request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Ya has iniciado sesión'})

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

    email = data.get('email', '').strip().lower()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '')
    subscribe_newsletter = data.get('newsletter', True)

    errors = []
    if not email:
        errors.append('El correo electrónico es obligatorio.')
    if not first_name or not last_name:
        errors.append('El nombre y apellido son obligatorios.')
    if not password:
        errors.append('La contraseña es obligatoria.')
    if CustomUser.objects.filter(email=email).exists():
        errors.append('Ya existe una cuenta con este correo.')

    if errors:
        return JsonResponse({'success': False, 'errors': errors})

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )
    if subscribe_newsletter:
        _subscribe_to_newsletter(
            email=email,
            first_name=first_name,
            user=user,
            source='footer',
        )
    auth_login(request, user)
    return JsonResponse({'success': True, 'message': 'Cuenta creada exitosamente'})


@require_POST
def newsletter_subscribe(request):
    """AJAX endpoint for newsletter-only subscription (no account creation)."""
    from django.http import JsonResponse
    email = (request.POST.get('email') or '').strip().lower()
    first_name = (request.POST.get('first_name') or '').strip()
    source = (request.POST.get('source') or 'inline')[:50]

    if not email:
        return JsonResponse({'success': False, 'error': 'Ingresa tu correo.'}, status=400)

    sub, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'user': request.user if request.user.is_authenticated else None,
            'is_active': True,
            'source': source,
        },
    )
    if not created and not sub.is_active:
        sub.is_active = True
        sub.unsubscribed_at = None
        sub.save()
    if created:
        from apps.core.emails import send_newsletter_welcome
        try:
            send_newsletter_welcome(email)
        except Exception:
            pass
        return JsonResponse({'success': True, 'message': '¡Gracias por suscribirte!'})
    return JsonResponse({'success': True, 'message': 'Ya estabas suscrito.'})

@login_required
def profile_view(request):
    from apps.orders.models import WhatsAppOrder

    orders = WhatsAppOrder.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        subscribe_newsletter = request.POST.get('newsletter') == 'on'

        if first_name and last_name:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone = phone
            request.user.save()
            if subscribe_newsletter:
                _subscribe_to_newsletter(
                    email=request.user.email,
                    first_name=first_name,
                    user=request.user,
                    source='perfil',
                )
            messages.success(request, 'Perfil actualizado correctamente.')
        else:
            messages.error(request, 'El nombre y apellido son obligatorios.')

    is_subscribed = NewsletterSubscriber.objects.filter(
        email=request.user.email, is_active=True
    ).exists()

    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'is_subscribed': is_subscribed,
        'page_title': 'Mi perfil',
    })


@login_required
def wishlist_view(request):
    items = request.user.wishlist_items.select_related('product', 'product__collection').prefetch_related('product__variants', 'product__variants__images').order_by('-added_at')
    return render(request, 'accounts/wishlist.html', {
        'items': items,
        'page_title': 'Mis favoritos',
    })


@require_POST
@login_required
def wishlist_toggle(request):
    """AJAX endpoint to add/remove a product from the user's wishlist."""
    from django.http import JsonResponse
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Falta el producto.'}, status=400)
    from apps.catalog.models import Product
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado.'}, status=404)
    item = WishlistItem.objects.filter(user=request.user, product=product).first()
    if item:
        item.delete()
        return JsonResponse({'success': True, 'action': 'removed', 'in_wishlist': False})
    WishlistItem.objects.create(user=request.user, product=product)
    return JsonResponse({'success': True, 'action': 'added', 'in_wishlist': True})
