"""Seed MARPLATA products (idempotent: re-runnable, updates if exists).

Estructura:
- Cada producto tiene un cover (imagen principal)
- Cada producto puede tener N imágenes adicionales para VariantImage
- Las imágenes se buscan en static/img/products/

Convenciones de nombres:
  - Cover:    {slug}.jpg       (ej: aura-beige-top.jpg)
  - Variante: {slug}_v{n}.jpg  (ej: aura-beige-top_v2.jpg)
  - Detalle:  {slug}_d{n}.jpg  (ej: aura-beige-top_d1.jpg)
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, r'C:\Users\Sebastian16\Desktop\MARPLATA')
django.setup()

from decimal import Decimal
from django.core.files import File
from apps.catalog.models import Collection, Product, ProductVariant, VariantImage

BASE = r'C:\Users\Sebastian16\Desktop\MARPLATA\static\img\products'
HERO = r'C:\Users\Sebastian16\Desktop\MARPLATA\static\img\hero\hero-home.jpg'

SIZES = ['S', 'M', 'L']

MATERIALS = '80% nylon reciclado, 20% elastano — secado rápido, protección UV UPF 50+'

PRODUCTS = [
    {
        'name': 'Aura Beige Top',
        'slug': 'aura-beige-top',
        'color': 'Beige',
        'color_slug': 'beige',
        'pieza': 'top',
        'price': Decimal('110000.00'),
        'stock_per_size': {'XS': 3, 'S': 3, 'M': 3, 'L': 3},
        'cover': os.path.join(BASE, 'aura-beige.jpg'),
        'extra_images': [],
        'description': (
            'Top de bikini con copas triangulares suaves y detalle de lazada frontal. '
            'Corte limpio que se adapta a tu silueta. '
            'Combina con la Tanga Aura Beige para el set completo a $189.000.'
        ),
        'story': 'Aura nace de la calma del mar al amanecer.',
    },
    {
        'name': 'Aura Beige Tanga',
        'slug': 'aura-beige-tanga',
        'color': 'Beige',
        'color_slug': 'beige',
        'pieza': 'tanga',
        'price': Decimal('79000.00'),
        'stock_per_size': {'XS': 3, 'S': 3, 'M': 3, 'L': 3},
        'cover': os.path.join(BASE, 'aura-beige.jpg'),
        'extra_images': [],
        'description': (
            'Tanga de bikini con laterales de amarre regulables y tiro medio. '
            'Combina con el Top Aura Beige para el set completo a $189.000.'
        ),
        'story': 'Una pieza esencial que se adapta a tu verano.',
    },
    {
        'name': 'Aura Verde Olivo Top',
        'slug': 'aura-verde-olivo-top',
        'color': 'Verde Olivo',
        'color_slug': 'verde-olivo',
        'pieza': 'top',
        'price': Decimal('110000.00'),
        'stock_per_size': {'XS': 3, 'S': 3, 'M': 3, 'L': 3},
        'cover': os.path.join(BASE, 'aura-verde-olivo.jpg'),
        'extra_images': [],
        'description': (
            'Top de bikini con copas triangulares y lazada frontal en verde olivo. '
            'Combina con la Tanga Aura Verde Olivo para el set completo a $189.000.'
        ),
        'story': 'El verde olivo que conecta con la naturaleza y el mar.',
    },
    {
        'name': 'Aura Verde Olivo Tanga',
        'slug': 'aura-verde-olivo-tanga',
        'color': 'Verde Olivo',
        'color_slug': 'verde-olivo',
        'pieza': 'tanga',
        'price': Decimal('79000.00'),
        'stock_per_size': {'XS': 3, 'S': 3, 'M': 3, 'L': 3},
        'cover': os.path.join(BASE, 'aura-verde-olivo.jpg'),
        'extra_images': [],
        'description': (
            'Tanga de bikini verde olivo con laterales de amarre regulables. '
            'Combina con el Top Aura Verde Olivo para el set completo a $189.000.'
        ),
        'story': 'Diseñada para acompañarte en cada ola.',
    },
    {
        'name': 'Brisa Mocca Top',
        'slug': 'brisa-mocca-top',
        'color': 'Mocca',
        'color_slug': 'mocca',
        'pieza': 'top',
        'price': Decimal('110000.00'),
        'stock_per_size': {'XS': 4, 'S': 4, 'M': 4, 'L': 3},
        'cover': os.path.join(BASE, 'brisa-mocca.jpg'),
        'extra_images': [],
        'description': (
            'Top de bikini minimalista con escote limpio y sujeción suave en tono mocca. '
            'Inspirado en el silencio de las mañanas en la costa. '
            'Combina con la Tanga Brisa Mocca para el set completo a $189.000.'
        ),
        'story': 'Brisa nace del silencio de las mañanas frente al mar.',
    },
    {
        'name': 'Brisa Mocca Tanga',
        'slug': 'brisa-mocca-tanga',
        'color': 'Mocca',
        'color_slug': 'mocca',
        'pieza': 'tanga',
        'price': Decimal('79000.00'),
        'stock_per_size': {'XS': 4, 'S': 4, 'M': 4, 'L': 3},
        'cover': os.path.join(BASE, 'brisa-mocca.jpg'),
        'extra_images': [],
        'description': (
            'Tanga de bikini en tono mocca con corte clásico y laterales finos. '
            'Combina con el Top Brisa Mocca para un set completo a $189.000.'
        ),
        'story': 'Una pieza que se mueve con vos y con el viento.',
    },
    {
        'name': 'Salida de Playa',
        'slug': 'salida-de-playa',
        'color': 'Unico',
        'color_slug': 'unico',
        'pieza': 'unica',
        'price': Decimal('189000.00'),
        'stock_per_size': {'XS': 5, 'S': 5, 'M': 5, 'L': 5},
        'cover': None,
        'extra_images': [],
        'description': (
            'Próximamente nuevas opciones de ropa de playa. '
            'Mantente atenta a nuestros lanzamientos.'
        ),
        'story': 'La playa se vive con estilo y comodidad.',
    },
]


def slugify_sku(text):
    out = []
    for ch in text.upper():
        if ch.isalnum():
            out.append(ch)
        elif ch in ' -_':
            out.append('-')
    return ''.join(out).strip('-')


def attach_image_to_variant(image_path, variant, is_primary=False, order=0, alt_text=''):
    if not os.path.exists(image_path):
        return None
    if VariantImage.objects.filter(variant=variant, image__endswith=os.path.basename(image_path)).exists():
        return None
    with open(image_path, 'rb') as f:
        vi = VariantImage.objects.create(
            variant=variant,
            image=File(f, name=os.path.basename(image_path)),
            alt_text=alt_text,
            is_primary=is_primary,
            order=order,
        )
    return vi


def main():
    print('=== Seeding products ===')

    collection, _ = Collection.objects.get_or_create(
        slug='esencia',
        defaults={'name': 'ESENCIA', 'is_active': True, 'description': 'Colección ESENCIA — el alma de MARPLATA.'}
    )
    print(f'  Collection: {collection.name} (slug={collection.slug})')

    for spec in PRODUCTS:
        product, created = Product.objects.get_or_create(
            slug=spec['slug'],
            defaults={
                'name': spec['name'],
                'description': spec['description'],
                'story': spec['story'],
                'materials': MATERIALS,
                'base_price': spec['price'],
                'collection': collection,
                'is_active': True,
            }
        )

        if not created:
            updated = False
            for field in ('name', 'description', 'story', 'materials', 'base_price'):
                new_val = spec[field] if field != 'base_price' else spec['price']
                if getattr(product, field) != new_val:
                    setattr(product, field, new_val)
                    updated = True
            if product.collection_id != collection.id:
                product.collection = collection
                updated = True
            if updated:
                product.save()
                print(f'  ~ Updated: {product.name}')

        if created:
            print(f'  + Created: {product.name}')

        if spec['cover'] and os.path.exists(spec['cover']):
            if not product.cover_image or not product.cover_image.name.endswith(os.path.basename(spec['cover'])):
                with open(spec['cover'], 'rb') as f:
                    product.cover_image.save(os.path.basename(spec['cover']), File(f), save=True)
                print(f'    cover_image: {os.path.basename(spec["cover"])}')

        first_variant = None
        for size in SIZES:
            sku = f"{slugify_sku(product.slug)}-{size}"
            variant, v_created = ProductVariant.objects.get_or_create(
                product=product,
                color_slug=spec['color_slug'],
                size=size,
                defaults={
                    'color': spec['color'],
                    'sku': sku,
                    'stock': spec['stock_per_size'][size],
                    'low_stock_threshold': 3,
                    'is_active': True,
                }
            )
            if v_created:
                print(f'    + variant: {size} (stock={variant.stock})')
            if first_variant is None:
                first_variant = variant

        if first_variant:
            images_to_attach = []
            if spec['cover'] and os.path.exists(spec['cover']):
                images_to_attach.append((spec['cover'], True, 0, product.name))
            for i, img_path in enumerate(spec.get('extra_images', []), start=1):
                if os.path.exists(img_path):
                    images_to_attach.append((img_path, False, i, f"{product.name} - vista {i}"))

            for img_path, is_primary, order, alt in images_to_attach:
                vi = attach_image_to_variant(img_path, first_variant, is_primary, order, alt)
                if vi:
                    suffix = ' (primary)' if is_primary else ''
                    print(f'    + image: {os.path.basename(img_path)}{suffix}')

    print('=== Done ===')


if __name__ == '__main__':
    main()
