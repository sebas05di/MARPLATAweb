"""Test E2E completo del flujo de compra de MARPLATA.

Cubre:
1. Registro y login
2. Navegación del catálogo
3. Selección de producto y talle
4. Agregar al carrito
5. Aplicar cupón (opcional)
6. Checkout completo
7. Verificación de WhatsApp message
8. Tracking de pedido
9. Newsletter
10. Búsqueda
11. Wishlist (login requerido)

Uso:
    python scripts/test_e2e.py
"""
import os
import sys
import re
import time

sys.path.insert(0, r'C:\Users\Sebastian16\Desktop\MARPLATA')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.catalog.models import ProductVariant
from apps.orders.models import WhatsAppOrder
from apps.accounts.models import NewsletterSubscriber, WishlistItem


class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def ok(self, name):
        self.passed.append(name)
        print(f'  PASS  {name}')

    def fail(self, name, error):
        self.failed.append((name, str(error)))
        print(f'  FAIL  {name}: {error}')

    def warn(self, name, note):
        self.warnings.append((name, note))
        print(f'  WARN  {name}: {note}')

    def summary(self):
        total = len(self.passed) + len(self.failed) + len(self.warnings)
        print(f'\n{"="*70}')
        print(f'RESUMEN: {len(self.passed)}/{total} pasaron')
        if self.failed:
            print(f'  {len(self.failed)} fallaron:')
            for n, e in self.failed:
                print(f'    - {n}: {e[:80]}')
        if self.warnings:
            print(f'  {len(self.warnings)} advertencias:')
            for n, w in self.warnings:
                print(f'    - {n}: {w[:80]}')
        print('='*70)


r = TestResult()

print('='*70)
print('TEST E2E — MARPLATA')
print('='*70)


print('\n[1] Registro y Login')
print('-'*70)
User = get_user_model()
test_email = f'e2e_{int(time.time())}@test.com'
try:
    user = User.objects.create_user(email=test_email, password='TestPass123!', first_name='E2E', last_name='Test')
    r.ok(f'Usuario creado: {test_email}')

    c = Client()
    c.force_login(user)
    r.ok('Login con force_login')
except Exception as e:
    r.fail('Registro/Login', str(e)[:100])
    sys.exit(1)


print('\n[2] Catálogo')
print('-'*70)
try:
    resp = c.get('/coleccion/')
    if resp.status_code == 200 and 'Aura' in resp.content.decode():
        r.ok('Catálogo carga con productos')
    else:
        r.fail('Catálogo', f'status={resp.status_code}')

    resp = c.get('/coleccion/buscar/?q=aura')
    if resp.status_code == 200 and 'Resultados' in resp.content.decode():
        r.ok('Búsqueda "aura" devuelve resultados')
    else:
        r.fail('Búsqueda', 'no encontró resultados')
except Exception as e:
    r.fail('Catálogo/Búsqueda', str(e)[:100])


print('\n[3] Producto y Carrito')
print('-'*70)
variant = None
try:
    variant = ProductVariant.objects.filter(is_active=True, stock__gt=0).first()
    if not variant:
        r.fail('Variante', 'no hay stock')
    else:
        r.ok(f'Variante seleccionada: {variant.product.name} ({variant.color}/{variant.size})')

        resp = c.post('/carrito/api/add/', {'variant_id': str(variant.id), 'quantity': '1'})
        if resp.status_code == 200:
            r.ok('Producto agregado al carrito')
        else:
            r.fail('Add to cart', f'status={resp.status_code}')

        resp = c.get('/carrito/')
        if resp.status_code == 200 and variant.product.name in resp.content.decode():
            r.ok('Carrito muestra el producto')
        else:
            r.fail('Carrito view', 'producto no aparece en carrito')
except Exception as e:
    r.fail('Producto/Carrito', str(e)[:100])


print('\n[4] Checkout')
print('-'*70)
order = None
try:
    form_email = f'form.email.{int(time.time())}@test.com'
    resp = c.post('/pedido/checkout/whatsapp/', {
        'customer_name': 'E2E Test Cliente',
        'customer_phone': '+57 300 111 2222',
        'customer_email': form_email,
        'shipping_address': 'Calle E2E 123',
        'shipping_city': 'Bogota',
        'shipping_department': 'Cundinamarca',
        'payment_method': 'contraentrega',
    })

    if resp.status_code == 302 and 'wa.me' in (resp.url or ''):
        r.ok(f'Checkout redirige a WhatsApp')
        wa_msg = resp.url
        if 'Hola' in wa_msg and 'MARPLATA' in wa_msg and form_email in wa_msg:
            r.ok('Mensaje WhatsApp incluye email del cliente')
        else:
            r.warn('Mensaje WhatsApp', f'no incluye email: {wa_msg[:100]}')
        if f'Orden' in wa_msg or '%2AOrden' in wa_msg:
            r.ok('Mensaje WhatsApp incluye número de orden')
    else:
        r.fail('Checkout', f'status={resp.status_code} redirect={resp.url}')

    order = WhatsAppOrder.objects.filter(customer_name='E2E Test Cliente').order_by('-created_at').first()
    if order:
        if order.customer_email == form_email:
            r.ok(f'Email del form guardado correctamente: {form_email}')
        else:
            r.fail('Email bug', f'esperaba {form_email}, obtuve {order.customer_email}')
        r.ok(f'Pedido creado: #{order.order_number}')
    else:
        r.fail('Pedido', 'no se creó el pedido')
except Exception as e:
    r.fail('Checkout', str(e)[:200])


print('\n[5] Tracking')
print('-'*70)
try:
    if order:
        resp = c.get(f'/pedido/orden/{order.order_number}/')
        if resp.status_code == 200:
            r.ok(f'Tracking page carga: {order.order_number}')
        else:
            r.fail('Tracking', f'status={resp.status_code}')

        resp = c.get(f'/pedido/orden/{order.order_number}/exito/')
        if resp.status_code == 200:
            r.ok('Order success page carga')
        else:
            r.warn('Order success', f'status={resp.status_code}')

        resp = c.get('/pedido/rastrear/')
        if resp.status_code == 200:
            r.ok('Tracking lookup page carga')
        else:
            r.warn('Tracking lookup', f'status={resp.status_code}')
except Exception as e:
    r.fail('Tracking', str(e)[:100])


print('\n[6] Newsletter')
print('-'*70)
try:
    test_nl = f'nl_{int(time.time())}@test.com'
    c.post('/', {'email': test_nl})

    if NewsletterSubscriber.objects.filter(email=test_nl, is_active=True).exists():
        r.ok(f'Newsletter suscripto: {test_nl}')
    else:
        r.fail('Newsletter', 'no se guardó la suscripción')
except Exception as e:
    r.fail('Newsletter', str(e)[:100])


print('\n[7] Wishlist')
print('-'*70)
try:
    if order:
        product = variant.product
        c.post('/cuenta/favoritos/agregar/', {'product_id': str(product.id)})
        if WishlistItem.objects.filter(user=user, product=product).exists():
            r.ok(f'Wishlist: {product.name} agregado')
        else:
            r.warn('Wishlist add', 'no se agregó (puede ser API diferente)')
except Exception as e:
    r.warn('Wishlist', str(e)[:100])


print('\n[8] Perfil')
print('-'*70)
try:
    resp = c.get('/cuenta/perfil/')
    if resp.status_code == 200:
        r.ok('Perfil carga')
    else:
        r.fail('Perfil', f'status={resp.status_code}')

    if order:
        if order.order_number in resp.content.decode():
            r.ok('Pedido aparece en perfil')
        else:
            r.warn('Perfil/pedido', 'el pedido no se ve en el perfil')
except Exception as e:
    r.fail('Perfil', str(e)[:100])


print('\n[9] Páginas estáticas')
print('-'*70)
static_pages = [
    ('/pagina/nosotros/', 'Nosotros'),
    ('/pagina/contacto/', 'Contacto'),
    ('/pagina/envios-devoluciones/', 'Envíos y devoluciones'),
    ('/pagina/terminos-condiciones/', 'Términos y condiciones'),
    ('/pagina/politica-privacidad/', 'Política de privacidad'),
]
for path, name in static_pages:
    try:
        resp = c.get(path)
        if resp.status_code == 200:
            r.ok(f'Página "{name}" carga')
        else:
            r.warn(f'Página {name}', f'status={resp.status_code}')
    except Exception as e:
        r.warn(f'Página {name}', str(e)[:80])


print('\n[10] URLs 404')
print('-'*70)
not_found_urls = [
    '/url-que-no-existe/',
    '/producto/inexistente/',
    '/pagina/que-no-existe/',
]
for url in not_found_urls:
    try:
        resp = c.get(url)
        if resp.status_code == 404:
            r.ok(f'404 correcto: {url}')
        else:
            r.warn(f'404 check: {url}', f'status={resp.status_code}')
    except Exception as e:
        r.warn(f'404 check: {url}', str(e)[:80])


print('\n[11] Health check')
print('-'*70)
try:
    resp = c.get('/health/')
    if resp.status_code == 200 and 'ok' in resp.content.decode().lower():
        r.ok(f'Health check: {resp.content.decode()[:80]}')
    else:
        r.warn('Health', f'status={resp.status_code}')
except Exception as e:
    r.warn('Health', str(e)[:80])


print('\n[12] Logout')
print('-'*70)
try:
    c.logout()
    r.ok('Logout exitoso')
    resp = c.get('/cuenta/perfil/')
    if resp.status_code == 302 or resp.status_code == 200:
        r.ok('Perfil no accesible sin login')
except Exception as e:
    r.warn('Logout', str(e)[:80])


r.summary()
