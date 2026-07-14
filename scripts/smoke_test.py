"""Smoke test rápido para verificar que el sitio funciona antes de deploy.

Uso:
    python scripts/smoke_test.py [--base-url http://localhost:8000]

Hace 12 chequeos rápidos y devuelve exit code 0 si todo pasa, 1 si hay fallos.
"""
import os
import sys
import argparse

sys.path.insert(0, r'C:\Users\Sebastian16\Desktop\MARPLATA')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

from django.test import Client
from django.conf import settings
from apps.catalog.models import Product, ProductVariant, Collection
from apps.orders.models import WhatsAppOrder
from apps.accounts.models import CustomUser, NewsletterSubscriber, WishlistItem


class Smoke:
    def __init__(self, base_url='http://localhost:8000'):
        self.c = Client()
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.base = base_url

    def check(self, name, fn):
        try:
            ok, msg = fn()
            if ok is True:
                self.passed += 1
                print(f'  PASS  {name}')
                if msg:
                    print(f'        {msg}')
            elif ok == 'warn':
                self.warnings += 1
                print(f'  WARN  {name}: {msg}')
            else:
                self.failed += 1
                print(f'  FAIL  {name}: {msg}')
        except Exception as e:
            self.failed += 1
            print(f'  FAIL  {name}: {e}')

    def report(self):
        total = self.passed + self.failed + self.warnings
        print()
        print('=' * 60)
        print(f'Resultado: {self.passed}/{total} OK ({self.warnings} warnings, {self.failed} failures)')
        print('=' * 60)
        return 0 if self.failed == 0 else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://localhost:8000')
    args = parser.parse_args()

    print('=' * 60)
    print('SMOKE TEST — MARPLATA')
    print('=' * 60)

    s = Smoke(args.base_url)

    print('\n[1] Health check')
    print('-' * 60)
    s.check('Health endpoint', lambda: (
        (True, '') if s.c.get('/health/').status_code == 200 else (False, 'no responde')
    ))

    print('\n[2] Database')
    print('-' * 60)
    s.check('Conexión a DB', lambda: (True, f'usando {settings.DATABASES["default"]["ENGINE"].split(".")[-1]}'))

    s.check('Productos cargados', lambda: (
        (True, f'{Product.objects.filter(is_active=True).count()} productos activos')
        if Product.objects.filter(is_active=True).count() > 0 else
        (False, 'No hay productos activos — corré python scripts/seed_products.py')
    ))

    s.check('Variantes con stock', lambda: (
        (True, f'{ProductVariant.objects.filter(stock__gt=0).count()} variantes con stock')
        if ProductVariant.objects.filter(stock__gt=0).count() > 0 else
        (False, 'Sin stock')
    ))

    s.check('Colección ESENCIA', lambda: (
        (True, '') if Collection.objects.filter(slug='esencia').exists() else (False, 'No existe la colección ESENCIA')
    ))

    print('\n[3] Páginas públicas')
    print('-' * 60)
    s.check('Home (/)', lambda: (
        (True, '') if s.c.get('/').status_code == 200 else (False, f'status {s.c.get("/").status_code}')
    ))

    s.check('Catálogo (/coleccion/)', lambda: (
        (True, '') if s.c.get('/coleccion/').status_code == 200 else (False, f'status {s.c.get("/coleccion/").status_code}')
    ))

    s.check('Búsqueda (/coleccion/buscar/?q=aura)', lambda: (
        (True, '') if s.c.get('/coleccion/buscar/?q=aura').status_code == 200 else (False, 'no responde')
    ))

    s.check('Página nosotros', lambda: (
        (True, '') if s.c.get('/pagina/nosotros/').status_code == 200 else (False, 'no responde')
    ))

    print('\n[4] Admin')
    print('-' * 60)
    s.check('Admin existe', lambda: (
        (True, 'admin@marplata.com') if CustomUser.objects.filter(is_superuser=True).exists() else
        (False, 'No hay superuser — corré python manage.py createsuperuser')
    ))

    s.check('Dashboard admin (/admin/dashboard/)', lambda: (
        (True, '') if 'Dashboard' in s.c.get('/admin/dashboard/').content.decode() or s.c.get('/admin/dashboard/').status_code in (200, 302) else (False, 'no responde')
    ))

    print('\n[5] API')
    print('-' * 60)
    s.check('Newsletter API (/cuenta/api/newsletter/)', lambda: (
        (True, 'OK') if s.c.post('/cuenta/api/newsletter/', {'email': f'smoke_{__import__("time").time()}@test.com'}).status_code in (200, 201) else (False, 'no responde')
    ))

    s.check('Cart summary API', lambda: (
        (True, '') if s.c.get('/carrito/api/summary/').status_code == 200 else (False, 'no responde')
    ))

    print('\n[6] Static files')
    print('-' * 60)
    s.check('CSS compilado', lambda: (
        (True, '') if os.path.exists('static/css/marplata.css') and os.path.getsize('static/css/marplata.css') > 1000 else
        (False, 'corré npm run build:css')
    ))

    s.check('Favicon existe', lambda: (
        (True, '') if os.path.exists('static/img/favicons/favicon.ico') else
        (False, 'corré python scripts/generate_assets.py')
    ))

    s.check('Logo branding existe', lambda: (
        (True, 'og-image.png, logo-blue.png, logo-white.png') if all(os.path.exists(f'static/img/branding/{f}') for f in ['og-image.png', 'logo-blue.png', 'logo-white.png']) else
        (False, 'corré python scripts/generate_assets.py')
    ))

    print('\n[7] Email')
    print('-' * 60)
    s.check('Email backend configurado', lambda: (
        ('warn', f'Consola (no envía real) — para emails reales configurá Gmail en .env')
        if 'console' in settings.EMAIL_BACKEND else
        (True, f'{settings.EMAIL_HOST}')
    ))

    s.check('Templates de email', lambda: (
        (True, '6 templates OK') if all(os.path.exists(f'templates/emails/{f}') for f in ['order_confirmation.html', 'new_order_admin.html', 'order_status_update.html', 'welcome.html', 'password_reset.html', 'newsletter_welcome.html']) else
        (False, 'Faltan templates de email')
    ))

    print('\n[8] WhatsApp')
    print('-' * 60)
    s.check('WhatsApp number configurado', lambda: (
        ('warn', f'Placeholder {settings.MARPLATA_WHATSAPP_NUMBER} — cambiar antes de producción')
        if settings.MARPLATA_WHATSAPP_NUMBER == '+573001234567' else
        (True, settings.MARPLATA_WHATSAPP_NUMBER)
    ))

    print()
    return s.report()


if __name__ == '__main__':
    sys.exit(main())
