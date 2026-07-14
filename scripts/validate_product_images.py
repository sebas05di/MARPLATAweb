"""Valida las imágenes de productos: dimensiones mínimas, formato, peso.

Uso:
    python scripts/validate_product_images.py

Muestra una tabla con cada imagen y marca cuáles necesitan reemplazo.
"""
import os
import sys
from PIL import Image

# Forzar UTF-8 en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
STATIC_PRODUCTS = os.path.join(PROJECT_ROOT, 'static', 'img', 'products')
MEDIA_COVERS = os.path.join(PROJECT_ROOT, 'media', 'products', 'covers')
MEDIA_VARIANTS = os.path.join(PROJECT_ROOT, 'media', 'products', 'variants')

# Mínimos recomendados para e-commerce
MIN_WIDTH = 1200
MIN_HEIGHT = 1600
RECOMMENDED_WIDTH = 1920
RECOMMENDED_HEIGHT = 2560
MAX_SIZE_KB = 500


def analyze_image(path):
    try:
        img = Image.open(path)
        size_kb = os.path.getsize(path) / 1024
        w, h = img.size
        return {
            'path': path,
            'width': w,
            'height': h,
            'size_kb': size_kb,
            'format': img.format,
            'mode': img.mode,
        }
    except Exception as e:
        return {'path': path, 'error': str(e)}


def status_for(img_info):
    if 'error' in img_info:
        return '❌ ERROR'
    w, h = img_info['width'], img_info['height']
    size = img_info['size_kb']

    if w < MIN_WIDTH or h < MIN_HEIGHT:
        return '⚠️  BAJA RES'
    if w < RECOMMENDED_WIDTH or h < RECOMMENDED_HEIGHT:
        return '🟡 ACEPTABLE'
    if size > MAX_SIZE_KB:
        return '🟡 PESADA'
    return '✅ ÓPTIMA'


def scan_dir(path):
    if not os.path.exists(path):
        return []
    return [os.path.join(path, f) for f in os.listdir(path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]


def main():
    print("=" * 100)
    print("VALIDACIÓN DE IMÁGENES DE PRODUCTOS")
    print("=" * 100)
    print(f"\nEstándares:")
    print(f"  Mínimo:     {MIN_WIDTH}x{MIN_HEIGHT} px")
    print(f"  Recomendado: {RECOMMENDED_WIDTH}x{RECOMMENDED_HEIGHT} px")
    print(f"  Peso máx:    {MAX_SIZE_KB} KB\n")

    dirs = [
        ('STATIC (seed source)', STATIC_PRODUCTS),
        ('MEDIA covers', MEDIA_COVERS),
        ('MEDIA variants', MEDIA_VARIANTS),
    ]

    all_images = []
    for label, d in dirs:
        files = scan_dir(d)
        if not files:
            print(f"📁 {label}: (vacío)")
            continue
        print(f"📁 {label}: {len(files)} archivos")
        for f in files:
            info = analyze_image(f)
            status = status_for(info)
            all_images.append((label, info, status))
            if 'error' in info:
                print(f"   {status}  {os.path.basename(f)}  — {info['error']}")
            else:
                print(f"   {status}  {os.path.basename(f):40s}  {info['width']}x{info['height']}  {info['size_kb']:.0f} KB")
        print()

    print("=" * 100)
    print("RESUMEN")
    print("=" * 100)
    needs_replacement = sum(1 for _, info, s in all_images if 'BAJA' in s or 'ERROR' in s)
    acceptable = sum(1 for _, info, s in all_images if 'ACEPTABLE' in s or 'PESADA' in s)
    optimal = sum(1 for _, info, s in all_images if 'ÓPTIMA' in s)

    print(f"  ✅ Óptimas:      {optimal}")
    print(f"  🟡 Aceptables:   {acceptable}")
    print(f"  ⚠️  A mejorar:    {needs_replacement}")
    print(f"  Total:           {len(all_images)}")

    if needs_replacement:
        print("\n📋 Imágenes que necesitan reemplazo:")
        for _, info, s in all_images:
            if 'BAJA' in s or 'ERROR' in s:
                print(f"   {os.path.basename(info['path'])}  ({info.get('width', '?')}x{info.get('height', '?')})")
        print("\n💡 Solicitá fotos HD al cliente (mín 1920x2560 px) y reemplazá en:")
        print(f"   {STATIC_PRODUCTS}")
        print("   Luego ejecutá: python scripts/optimize_product_images.py")
        print("   Y:            python scripts/seed_products.py")


if __name__ == '__main__':
    main()
