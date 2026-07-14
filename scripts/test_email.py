"""Script de prueba para verificar el envío de emails transaccionales.

Uso:
    python scripts/test_email.py tu-email@gmail.com

Envía un email de prueba de cada template a la dirección especificada.
Útil para verificar que Gmail/SMTP está configurado correctamente.
"""
import os
import sys
import django

# Forzar UTF-8 en Windows para soportar emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from apps.catalog.models import Product, ProductVariant
from apps.orders.models import WhatsAppOrder, WhatsAppOrderItem


def print_config():
    print("=" * 60)
    print("Configuración de Email Actual")
    print("=" * 60)
    print(f"Backend:   {settings.EMAIL_BACKEND}")
    print(f"Host:      {settings.EMAIL_HOST}")
    print(f"Port:      {settings.EMAIL_PORT}")
    print(f"TLS:       {settings.EMAIL_USE_TLS}")
    print(f"User:      {settings.EMAIL_HOST_USER or '(vacío)'}")
    print(f"From:      {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 60)

    if 'console' in settings.EMAIL_BACKEND:
        print("\n⚠️  Estás usando el backend de CONSOLA.")
        print("   Los emails NO se envían realmente, se imprimen en pantalla.")
        print("   Para enviar emails reales, configurá EMAIL_HOST_USER en .env")
        print("   y cambiá EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
    elif not settings.EMAIL_HOST_USER:
        print("\n❌ EMAIL_HOST_USER está vacío. No se pueden enviar emails.")
        return False

    return True


def send_test_emails(to_email):
    """Envía un email de prueba de cada template."""
    from apps.core.emails import (
        send_welcome_email,
        send_password_reset_email,
        send_newsletter_welcome,
        send_order_confirmation,
        send_new_order_admin_notification,
        send_order_status_update,
    )

    User = get_user_model()
    user, _ = User.objects.get_or_create(
        email=to_email,
        defaults={'username': to_email.split('@')[0], 'first_name': 'Test'},
    )

    order = None
    if WhatsAppOrder.objects.exists():
        order = WhatsAppOrder.objects.first()
    else:
        print("\n⚠️  No hay pedidos en la DB. Los emails de pedido usarán un pedido mock.")

    results = []

    print(f"\n📧 Enviando emails de prueba a: {to_email}\n")

    # 1. Welcome
    try:
        msg = send_welcome_email(user)
        results.append(('welcome', bool(msg)))
        print(f"  {'✅' if msg else '❌'} send_welcome_email")
    except Exception as e:
        results.append(('welcome', False))
        print(f"  ❌ send_welcome_email: {e}")

    # 2. Password reset
    try:
        msg = send_password_reset_email(user, 'http://localhost:8000/reset/test-token/')
        results.append(('password_reset', bool(msg)))
        print(f"  {'✅' if msg else '❌'} send_password_reset_email")
    except Exception as e:
        results.append(('password_reset', False))
        print(f"  ❌ send_password_reset_email: {e}")

    # 3. Newsletter
    try:
        msg = send_newsletter_welcome(to_email)
        results.append(('newsletter', bool(msg)))
        print(f"  {'✅' if msg else '❌'} send_newsletter_welcome")
    except Exception as e:
        results.append(('newsletter', False))
        print(f"  ❌ send_newsletter_welcome: {e}")

    # 4-6. Order emails (si hay pedido)
    if order:
        try:
            msg = send_order_confirmation(order)
            results.append(('order_confirmation', bool(msg)))
            print(f"  {'✅' if msg else '❌'} send_order_confirmation")
        except Exception as e:
            results.append(('order_confirmation', False))
            print(f"  ❌ send_order_confirmation: {e}")

        try:
            msg = send_new_order_admin_notification(order)
            results.append(('new_order_admin', bool(msg)))
            print(f"  {'✅' if msg else '❌'} send_new_order_admin_notification")
        except Exception as e:
            results.append(('new_order_admin', False))
            print(f"  ❌ send_new_order_admin_notification: {e}")

        try:
            old = order.status
            order.status = 'dispatched'
            msg = send_order_status_update(order, old_status=old)
            order.status = old
            results.append(('order_status', bool(msg)))
            print(f"  {'✅' if msg else '❌'} send_order_status_update")
        except Exception as e:
            results.append(('order_status', False))
            print(f"  ❌ send_order_status_update: {e}")

    print("\n" + "=" * 60)
    success = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"Resultado: {success}/{total} emails enviados correctamente")
    print("=" * 60)

    return success == total


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_email.py tu-email@gmail.com")
        sys.exit(1)

    to_email = sys.argv[1]
    print_config()
    ok = send_test_emails(to_email)
    sys.exit(0 if ok else 1)
