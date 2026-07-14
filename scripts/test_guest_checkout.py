"""Test E2E completo del checkout como invitado via Playwright."""
import os
import sys
import time
import subprocess
import json

sys.path.insert(0, r'C:\Users\Sebastian16\Desktop\MARPLATA')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

from django.test import Client
from apps.catalog.models import ProductVariant
from apps.orders.models import WhatsAppOrder

# Usar Django test client que mantiene sesion
c = Client()
variant = ProductVariant.objects.filter(is_active=True, stock__gt=0).first()
print(f'Variante: {variant.product.name} ({variant.color}/{variant.size}) stock={variant.stock}')

# Step 1: Add to cart
resp = c.post('/carrito/api/add/', {'variant_id': str(variant.id), 'quantity': '1'})
print(f'1. Add to cart: {resp.status_code}')

# Step 2: GET checkout
resp = c.get('/pedido/checkout/')
print(f'2. GET /pedido/checkout/: {resp.status_code} (esperado 200)')

if resp.status_code == 200:
    content = resp.content.decode('utf-8', errors='ignore')
    checks = {
        'Banner "¿Querés crear una cuenta?"': '¿Querés crear una cuenta?' in content,
        'Link "Iniciar sesion"': 'Iniciar sesión' in content,
        'Link "Crear cuenta"': 'Crear cuenta' in content,
        'Btn "FINALIZAR COMO INVITADO"': 'FINALIZAR COMO INVITADO' in content,
        'Frase "Es opcional"': 'opcional' in content,
    }
    for name, ok in checks.items():
        print(f'   {"OK " if ok else "FALTA"} {name}')

# Step 3: Submit checkout as guest
form_email = f'guest_{int(time.time())}@test.com'
resp = c.post('/pedido/checkout/whatsapp/', {
    'customer_name': 'Cliente Invitado',
    'customer_phone': '+57 300 999 1111',
    'customer_email': form_email,
    'shipping_address': 'Calle Invitado 100',
    'shipping_city': 'Bogota',
    'shipping_department': 'Cundinamarca',
    'payment_method': 'contraentrega',
})
print(f'3. POST checkout: {resp.status_code}')
if hasattr(resp, 'url') and resp.url:
    is_wa = 'wa.me' in resp.url
    print(f'   Redirect a WhatsApp: {is_wa}')

# Step 4: Verify order created
last = WhatsAppOrder.objects.filter(customer_email=form_email).order_by('-created_at').first()
if last:
    print(f'4. Pedido creado: #{last.order_number}')
    print(f'   user_id: {last.user_id} (None = invitado)')
    print(f'   email: {last.customer_email}')
else:
    print('4. ERROR: pedido no creado')
