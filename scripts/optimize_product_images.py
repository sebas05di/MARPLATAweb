"""Optimiza imágenes de productos: redimensiona y genera versiones WebP.

Uso:
    python scripts/optimize_product_images.py [--max-width 1920] [--quality 85]

Toma las imágenes de static/img/products/ y genera:
  - Versión JPG optimizada (full)
  - Versión WebP (50% más liviano)
  - Versión thumbnail 600x800 (para listados)

Las imágenes de origen deben ser >= max-width x max-height.
"""
import os
import sys
import argparse
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(PROJECT_ROOT, 'static', 'img', 'products')


def optimize_image(src_path, max_width, quality):
    if not os.path.exists(src_path):
        print(f"  ⚠️  No existe: {src_path}")
        return None

    img = Image.open(src_path)
    original_size = os.path.getsize(src_path) / 1024
    w, h = img.size
    filename = os.path.basename(src_path)
    name, ext = os.path.splitext(filename)

    if w > max_width:
        ratio = max_width / w
        new_size = (max_width, int(h * ratio))
        img_resized = img.resize(new_size, Image.LANCZOS)
    else:
        img_resized = img

    if img_resized.mode != 'RGB':
        img_resized = img_resized.convert('RGB')

    out_jpg = os.path.join(SOURCE_DIR, f"{name}.jpg")
    img_resized.save(out_jpg, 'JPEG', quality=quality, optimize=True, progressive=True)

    out_webp = os.path.join(SOURCE_DIR, f"{name}.webp")
    img_resized.save(out_webp, 'WEBP', quality=quality, method=6)

    thumb_size = (600, 800)
    img_thumb = img_resized.copy()
    img_thumb.thumbnail(thumb_size, Image.LANCZOS)
    out_thumb = os.path.join(SOURCE_DIR, f"{name}_thumb.webp")
    img_thumb.save(out_thumb, 'WEBP', quality=quality, method=6)

    new_size_kb = os.path.getsize(out_jpg) / 1024
    webp_size_kb = os.path.getsize(out_webp) / 1024
    thumb_size_kb = os.path.getsize(out_thumb) / 1024

    return {
        'original': filename,
        'original_kb': original_size,
        'original_size': (w, h),
        'new_size': img_resized.size,
        'jpg_kb': new_size_kb,
        'webp_kb': webp_size_kb,
        'thumb_kb': thumb_size_kb,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=1920, help='Ancho máximo (default: 1920)')
    parser.add_argument('--quality', type=int, default=85, help='Calidad JPG/WebP 1-100 (default: 85)')
    args = parser.parse_args()

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ No existe {SOURCE_DIR}")
        sys.exit(1)

    sources = [f for f in os.listdir(SOURCE_DIR)
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))
               and '_thumb' not in f and '.webp' not in f]

    if not sources:
        print(f"❌ No hay imágenes JPG/PNG en {SOURCE_DIR}")
        sys.exit(1)

    print("=" * 90)
    print(f"OPTIMIZANDO IMÁGENES — max-width={args.max_width}, quality={args.quality}")
    print("=" * 90)
    print()

    results = []
    for f in sorted(sources):
        src = os.path.join(SOURCE_DIR, f)
        result = optimize_image(src, args.max_width, args.quality)
        if result:
            results.append(result)
            print(f"✅ {result['original']:40s}  "
                  f"{result['original_size'][0]}x{result['original_size'][1]} ({result['original_kb']:.0f}KB)")
            print(f"   → {result['new_size'][0]}x{result['new_size'][1]} → "
                  f"JPG: {result['jpg_kb']:.0f}KB  |  WebP: {result['webp_kb']:.0f}KB  |  "
                  f"Thumb: {result['thumb_kb']:.0f}KB")
            print()

    print("=" * 90)
    print(f"✅ {len(results)} imágenes optimizadas")
    print("=" * 90)
    print("\n📋 Próximos pasos:")
    print("   1. Verificá las imágenes en /static/img/products/")
    print("   2. Ejecutá: python scripts/seed_products.py")
    print("   3. Verificá en el navegador que se vean correctamente")


if __name__ == '__main__':
    main()
