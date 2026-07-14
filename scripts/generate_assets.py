"""Genera todos los assets visuales desde los logos del PDF:
- favicon.ico multi-resolución
- apple-touch-icon
- og:image (1200x630)
- Versiones del logo: azul, blanco, negro
- Convierte todo a WebP para mejor performance
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
LOGOS_DIR = os.path.join(PROJECT_ROOT, 'static', 'img', 'logos')
BRANDING_DIR = os.path.join(PROJECT_ROOT, 'static', 'img', 'branding')
FAVICON_DIR = os.path.join(PROJECT_ROOT, 'static', 'img', 'favicons')

os.makedirs(BRANDING_DIR, exist_ok=True)
os.makedirs(FAVICON_DIR, exist_ok=True)

# Brand colors
COLOR_PRIMARY = (107, 139, 200)  # #6B8BC8
COLOR_NEUTRAL = (245, 239, 235)  # #F5EFEB
COLOR_TEXT = (44, 62, 80)  # #2C3E50
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (26, 26, 26)


def load_source(name):
    return Image.open(os.path.join(LOGOS_DIR, name)).convert('RGBA')


def make_white_version(img):
    """Convert logo to white (for dark backgrounds like hero)."""
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if a > 0 and (r < 240 or g < 240 or b < 240):
            new_data.append((255, 255, 255, a))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img


def optimize_logo(src_name, dest_name, size=None, mode='RGBA'):
    """Copy and optimize a logo PNG."""
    img = load_source(src_name)
    if size:
        img = img.resize(size, Image.LANCZOS)
    out_path = os.path.join(BRANDING_DIR, dest_name)
    img.save(out_path, 'PNG', optimize=True)

    webp_path = os.path.join(BRANDING_DIR, dest_name.replace('.png', '.webp'))
    img.save(webp_path, 'WEBP', quality=90, method=6)
    print(f"  {dest_name} ({img.size[0]}x{img.size[1]})")
    return img


def generate_favicon():
    """Generate multi-resolution favicon.ico from logo."""
    src = load_source('page_2.png')

    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    images = []
    for size in sizes:
        resized = src.resize(size, Image.LANCZOS)
        images.append(resized)

    favicon_ico_path = os.path.join(FAVICON_DIR, 'favicon.ico')
    images[0].save(
        favicon_ico_path,
        format='ICO',
        sizes=[(s.width, s.height) for s in images],
        append_images=images[1:]
    )
    print(f"  favicon.ico (multi-resolución: {[s[0] for s in sizes]})")

    apple_path = os.path.join(FAVICON_DIR, 'apple-touch-icon.png')
    src.resize((180, 180), Image.LANCZOS).save(apple_path, 'PNG', optimize=True)
    print(f"  apple-touch-icon.png (180x180)")

    src_16 = src.resize((16, 16), Image.LANCZOS)
    src_16.save(os.path.join(FAVICON_DIR, 'favicon-16x16.png'), 'PNG', optimize=True)
    src_32 = src.resize((32, 32), Image.LANCZOS)
    src_32.save(os.path.join(FAVICON_DIR, 'favicon-32x32.png'), 'PNG', optimize=True)
    print(f"  favicon-16x16.png, favicon-32x32.png")


def generate_og_image():
    """Generate og:image 1200x630 with logo + tagline."""
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), color=COLOR_NEUTRAL)
    draw = ImageDraw.Draw(img)

    logo = load_source('page_2.png')
    target_w = 600
    ratio = target_w / logo.width
    target_h = int(logo.height * ratio)
    logo_resized = logo.resize((target_w, target_h), Image.LANCZOS)
    logo_x = (W - target_w) // 2
    logo_y = (H - target_h) // 2 - 40
    img.paste(logo_resized, (logo_x, logo_y), logo_resized)

    og_path = os.path.join(BRANDING_DIR, 'og-image.png')
    img.save(og_path, 'PNG', optimize=True)
    print(f"  og-image.png (1200x630)")

    img.save(os.path.join(BRANDING_DIR, 'og-image.webp'), 'WEBP', quality=88, method=6)


def generate_manifest():
    """Generate site.webmanifest for PWA."""
    manifest = """{
  "name": "MARPLATA — Diseña tu estilo, resalta tu esencia",
  "short_name": "MARPLATA",
  "description": "Vestidos de baño pensados para cada cuerpo y cada historia.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F5EFEB",
  "theme_color": "#6B8BC8",
  "icons": [
    {
      "src": "/static/img/favicons/favicon-32x32.png",
      "sizes": "32x32",
      "type": "image/png"
    },
    {
      "src": "/static/img/favicons/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ]
}
"""
    path = os.path.join(PROJECT_ROOT, 'static', 'site.webmanifest')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(manifest)
    print(f"  site.webmanifest")


def main():
    print("=" * 60)
    print("Generando assets visuales MARPLATA")
    print("=" * 60)

    print("\n[1/4] Generando favicons...")
    generate_favicon()

    print("\n[2/4] Optimizando logos...")
    optimize_logo('page_1.png', 'logo-black.png')
    optimize_logo('page_2.png', 'logo-blue.png')
    optimize_logo('page_3.png', 'tagline.png')
    optimize_logo('page_6.png', 'logo-blue-beachwear.png')

    print("\n[3/4] Generando versión blanca del logo...")
    logo_blue = load_source('page_2.png')
    logo_white = make_white_version(logo_blue)
    white_path = os.path.join(BRANDING_DIR, 'logo-white.png')
    logo_white.save(white_path, 'PNG', optimize=True)
    logo_white.save(os.path.join(BRANDING_DIR, 'logo-white.webp'), 'WEBP', quality=90, method=6)
    print(f"  logo-white.png + .webp")

    print("\n[4/4] Generando og:image 1200x630...")
    generate_og_image()

    print("\n[5/5] Generando site.webmanifest...")
    generate_manifest()

    print("\n" + "=" * 60)
    print("Assets generados en static/img/branding/ y static/img/favicons/")
    print("=" * 60)


if __name__ == '__main__':
    main()
