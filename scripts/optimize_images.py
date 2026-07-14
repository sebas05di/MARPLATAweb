"""Optimize and copy product images to static/img/."""
import os
from PIL import Image, ImageOps

BASE = r'C:\Users\Sebastian16\Desktop\MARPLATA'
SRC = r'C:\Users\Sebastian16\Desktop\Contenido visual MP'

DEST_HERO = os.path.join(BASE, 'static', 'img', 'hero')
DEST_PRODUCTS = os.path.join(BASE, 'static', 'img', 'products')

os.makedirs(DEST_HERO, exist_ok=True)
os.makedirs(DEST_PRODUCTS, exist_ok=True)


def process_image(src_path, dest_path, max_width=1920, quality=85):
    """Open image, fix EXIF orientation, resize, and save."""
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(dest_path, 'JPEG', quality=quality, optimize=True)
    size_kb = os.path.getsize(dest_path) / 1024
    print(f'  OK {os.path.basename(src_path)} -> {os.path.basename(dest_path)} ({img.size[0]}x{img.size[1]}, {size_kb:.1f}KB)')


print('=== Optimizing images ===')

process_image(
    os.path.join(SRC, 'SALO2.jpg'),
    os.path.join(DEST_HERO, 'hero-home.jpg'),
    max_width=1920,
    quality=85,
)

process_image(
    os.path.join(SRC, 'SALOprincipal.jpg'),
    os.path.join(DEST_PRODUCTS, 'brisa-mocca.jpg'),
    max_width=1920,
    quality=85,
)

process_image(
    os.path.join(SRC, 'AURA - BEIGE.jpeg'),
    os.path.join(DEST_PRODUCTS, 'aura-beige.jpg'),
    max_width=1920,
    quality=90,
)

process_image(
    os.path.join(SRC, 'AURA - VERDE OLIVO.jpeg'),
    os.path.join(DEST_PRODUCTS, 'aura-verde-olivo.jpg'),
    max_width=1920,
    quality=90,
)

print('=== Done ===')
