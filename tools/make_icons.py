"""Draws the Daily Spend icons with Pillow.  Run:  python3 tools/make_icons.py

The mark is original and deliberately plain: a white coin on teal with a teal plus sign
("add an expense"). No maple leaf, no bank or card network symbols.
"""
import os

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
TEAL = (11, 122, 117, 255)
WHITE = (255, 255, 255, 255)
SCALE = 4  # draw large, then shrink for smooth edges


def draw(size, coin=0.30, rounded=True, opaque=False):
    s = size * SCALE
    img = Image.new("RGBA", (s, s), TEAL if opaque else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if not opaque:
        if rounded:
            d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=TEAL)
        else:
            d.rectangle([0, 0, s, s], fill=TEAL)
    c, r = s / 2, s * coin
    d.ellipse([c - r, c - r, c + r, c + r], fill=WHITE)
    arm, thick = r * 0.52, r * 0.20
    d.rounded_rectangle([c - arm, c - thick, c + arm, c + thick], radius=thick, fill=TEAL)
    d.rounded_rectangle([c - thick, c - arm, c + thick, c + arm], radius=thick, fill=TEAL)
    out = img.resize((size, size), Image.LANCZOS)
    return out.convert("RGB") if opaque else out


def main():
    os.makedirs(OUT, exist_ok=True)
    draw(192).save(os.path.join(OUT, "icon-192.png"))
    draw(512).save(os.path.join(OUT, "icon-512.png"))
    # Maskable: full-bleed background, mark inside the central safe zone (80% circle).
    draw(512, coin=0.24, opaque=True).save(os.path.join(OUT, "icon-maskable-512.png"))
    # iOS rounds the corners itself and does not want transparency.
    draw(180, opaque=True).save(os.path.join(OUT, "apple-touch-icon.png"))
    print("\n".join(sorted(os.listdir(OUT))))


if __name__ == "__main__":
    main()
