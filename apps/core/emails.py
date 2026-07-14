"""MARPLATA transactional email utilities.

Centralized functions for sending branded emails to customers and admins.
All emails use a shared HTML template with MARPLATA styling.
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import SiteConfig


def _get_base_context():
    site = SiteConfig.load()
    return {
        'site': site,
        'site_name': site.site_name or 'MARPLATA',
        'primary_color': '#6B8BC8',
        'site_tagline': site.site_tagline or 'Diseña tu estilo, resalta tu esencia',
        'contact_email': site.contact_email or '',
        'contact_phone': site.contact_phone or '',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }


def _send_email(subject, to_email, template_name, context, fail_silently=True):
    """Render an HTML email from a template and send it."""
    ctx = {**_get_base_context(), **context}
    html_content = render_to_string(template_name, ctx)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email] if isinstance(to_email, str) else list(to_email),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=fail_silently)
    return msg


def send_order_confirmation(order):
    """Email sent to the customer right after a new order is created."""
    if not order.customer_email:
        return None
    subject = f"¡Pedido #{order.order_number} recibido! | MARPLATA"
    return _send_email(
        subject,
        order.customer_email,
        'emails/order_confirmation.html',
        {'order': order, 'items': order.items.all().select_related('variant__product')},
    )


def send_new_order_admin_notification(order):
    """Email sent to admin/site owner when a new order arrives."""
    site = SiteConfig.load()
    admin_email = site.contact_email or settings.DEFAULT_FROM_EMAIL
    if not admin_email:
        return None
    subject = f"Nuevo pedido #{order.order_number} — {order.customer_name}"
    return _send_email(
        subject,
        admin_email,
        'emails/new_order_admin.html',
        {'order': order, 'items': order.items.all().select_related('variant__product')},
    )


def send_order_status_update(order, old_status=None):
    """Email sent when an admin changes the order status."""
    if not order.customer_email:
        return None
    status_labels = {
        'pending': 'Recibido',
        'contacted': 'Contactado',
        'confirmed': 'Confirmado',
        'dispatched': 'Despachado',
        'delivered': 'Entregado',
        'cancelled': 'Cancelado',
    }
    subject = f"Tu pedido #{order.order_number} está {status_labels.get(order.status, order.status)} | MARPLATA"
    return _send_email(
        subject,
        order.customer_email,
        'emails/order_status_update.html',
        {
            'order': order,
            'items': order.items.all().select_related('variant__product'),
            'old_status': old_status,
            'new_status_label': status_labels.get(order.status, order.status),
        },
    )


def send_welcome_email(user):
    """Email sent right after a new user registers."""
    if not user.email:
        return None
    subject = "¡Bienvenida a MARPLATA!"
    return _send_email(
        subject,
        user.email,
        'emails/welcome.html',
        {'user': user},
    )


def send_newsletter_welcome(email):
    """Confirmation email when someone subscribes to the newsletter."""
    subject = "¡Suscripción confirmada a MARPLATA!"
    return _send_email(
        subject,
        email,
        'emails/newsletter_welcome.html',
        {'subscriber_email': email},
    )


def send_password_reset_email(user, reset_url):
    """Branded password reset email."""
    if not user.email:
        return None
    subject = "Restablecé tu contraseña | MARPLATA"
    return _send_email(
        subject,
        user.email,
        'emails/password_reset.html',
        {'user': user, 'reset_url': reset_url},
    )
