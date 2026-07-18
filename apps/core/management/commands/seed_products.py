import os
import re
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Collection, Product, ProductVariant, VariantImage


BASE_DIR = Path(settings.BASE_DIR)
SOURCE_DIR = BASE_DIR / 'static' / 'img' / 'products'
MEDIA_DIR = BASE_DIR / 'media' / 'products' / 'variants'

# Map filename prefix -> product metadata
PRODUCTS = {
    'aura-beige': {
        'name': 'Aura Beige',
        'color': 'Beige',
        'top_price': Decimal('70000'),
        'bottom_price': Decimal('60000'),
        'description': 'Vestido de baño Aura en tono beige, con diseño versátil que se adapta a diferentes siluetas.',
        'story': 'La colección Aura nace para acompañar a la mujer en cada momento junto al mar.',
        'materials': '80% poliamida, 20% elastano.',
    },
    'aura-verde-olivo': {
        'name': 'Aura Verde Olivo',
        'color': 'Verde Olivo',
        'top_price': Decimal('70000'),
        'bottom_price': Decimal('60000'),
        'description': 'Vestido de baño Aura en verde olivo, elegante y atemporal.',
        'story': 'Pieza pensada para resaltar la esencia natural de cada mujer.',
        'materials': '80% poliamida, 20% elastano.',
    },
    'brisa': {
        'name': 'Brisa Mocca',
        'color': 'Mocca',
        'top_price': Decimal('80000'),
        'bottom_price': Decimal('80000'),
        'description': 'Vestido de baño Brisa en tono mocca, sofisticado y cómodo.',
        'story': 'Brisa combina elegancia y frescura para días de playa inolvidables.',
        'materials': '80% poliamida, 20% elastano.',
    },
}

OLD_SLUGS_TO_DELETE = [
    'aura-beige-top',
    'aura-beige-tanga',
    'aura-verde-olivo-top',
    'aura-verde-olivo-tanga',
    'brisa-mocca-top',
    'brisa-mocca-tanga',
    'salida-de-playa',
]


class Command(BaseCommand):
    help = 'Crea/actualiza productos unificados (top + tanga) desde static/img/products/'

    def handle(self, *args, **options):
        if not SOURCE_DIR.exists():
            self.stderr.write(f'No existe {SOURCE_DIR}')
            return

        MEDIA_DIR.mkdir(parents=True, exist_ok=True)

        collection, _ = Collection.objects.get_or_create(
            slug='esencia',
            defaults={'name': 'ESENCIA', 'description': 'Colección principal de vestidos de baño MARPLATA.'},
        )

        # Group source files by prefix
        groups = {}
        for f in sorted(SOURCE_DIR.iterdir()):
            if not f.is_file() or not f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                continue
            m = re.match(r'^([a-z]+(?:-[a-z]+)*)_\d+', f.name.lower())
            if not m:
                continue
            prefix = m.group(1)
            groups.setdefault(prefix, []).append(f)

        with transaction.atomic():
            # Delete old separate products (top/tanga) and legacy items
            deleted = Product.objects.filter(slug__in=OLD_SLUGS_TO_DELETE).delete()
            self.stdout.write(f'Productos viejos eliminados: {deleted[0]}')

            for prefix, meta in PRODUCTS.items():
                files = sorted(groups.get(prefix, []))
                if not files:
                    self.stdout.write(self.style.WARNING(f'Sin fotos para {prefix}'))
                    continue

                slug = slugify(meta['name'])
                base_price = meta['top_price'] + meta['bottom_price']

                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': meta['name'],
                        'collection': collection,
                        'description': meta['description'],
                        'story': meta['story'],
                        'materials': meta['materials'],
                        'top_price': meta['top_price'],
                        'bottom_price': meta['bottom_price'],
                        'base_price': base_price,
                        'is_active': True,
                    },
                )

                # Remove existing variants for this product to avoid conflicts
                ProductVariant.objects.filter(product=product).delete()

                color = meta['color']
                color_slug = slugify(color)

                # Create one base variant per color to hold images
                base_variant = None
                for top_size in ['S', 'M', 'L']:
                    for bottom_size in ['S', 'M', 'L']:
                        variant = ProductVariant.objects.create(
                            product=product,
                            color=color,
                            color_slug=color_slug,
                            top_size=top_size,
                            bottom_size=bottom_size,
                            sku=f'{slug}-{color_slug}-{top_size}-{bottom_size}'.upper(),
                            stock=5,
                            low_stock_threshold=3,
                            is_active=True,
                        )
                        if top_size == 'S' and bottom_size == 'S':
                            base_variant = variant

                # Assign images to base variant
                if base_variant:
                    VariantImage.objects.filter(variant=base_variant).delete()
                    for i, src in enumerate(files):
                        dst_name = f'{slug}_{color_slug}_{src.name}'
                        with open(src, 'rb') as img_file:
                            VariantImage.objects.create(
                                variant=base_variant,
                                image=File(img_file, name=dst_name),
                                alt_text=f'{meta["name"]} {color}',
                                is_primary=(i == 0),
                                order=i,
                            )

                action = 'creado' if created else 'actualizado'
                self.stdout.write(self.style.SUCCESS(
                    f'{action}: {product.name} — {len(files)} foto(s) — {base_price} COP'
                ))

        self.stdout.write(self.style.SUCCESS('Seed de productos finalizado.'))
