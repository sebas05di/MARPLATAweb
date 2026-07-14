"""Generate a simple OG default image (1200x630) using PIL."""
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed, skipping")
    sys.exit(0)

W, H = 1200, 630
PRIMARY = (107, 139, 200)
PRIMARY_DARK = (90, 123, 181)
NEUTRAL = (245, 239, 235)
TEXT = (44, 62, 80)

img = Image.new('RGB', (W, H), PRIMARY)
draw = ImageDraw.Draw(img)

for y in range(0, H, 4):
    alpha = int(40 * (y / H))
    color = tuple(
        PRIMARY_DARK[i] + (NEUTRAL[i] - PRIMARY_DARK[i]) * (y / H) for i in range(3)
    )
    draw.rectangle([(0, y), (W, y + 4)], fill=tuple(int(c) for c in color))

try:
    font_title = ImageFont.truetype("arialbd.ttf", 84)
    font_sub = ImageFont.truetype("arial.ttf", 36)
except OSError:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

text = "MARPLATA"
bbox = draw.textbbox((0, 0), text, font=font_title)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text(((W - tw) / 2, H / 2 - th - 20), text, fill="white", font=font_title)

text2 = "Diseña tu estilo, resalta tu esencia"
bbox2 = draw.textbbox((0, 0), text2, font=font_sub)
tw2 = bbox2[2] - bbox2[0]
draw.text(((W - tw2) / 2, H / 2 + 30), text2, fill="white", font=font_sub)

out = os.path.join(os.path.dirname(__file__), "..", "static", "img", "og-default.jpg")
out = os.path.abspath(out)
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, "JPEG", quality=85)
print(f"Saved: {out}")
