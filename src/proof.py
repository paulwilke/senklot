"""Render proof PNGs at several axis locations: python src/proof.py out.png [size]"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT = "fonts/Senklot[wght,BLSY,BLSX].ttf"
LINES = [
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789 .,:;!? -–— '\"’“” ()[]/+=*& ÄÖÜäöüß",
    "Hamburgefonstiv Senklot quiet",
]
LOCS = [(0, 0), (100, 0), (-100, 0), (0, 100), (0, -100)]


def main(out, size=64):
    rows = []
    for y, x in LOCS:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_axes([y, x])
        lab = ImageFont.load_default()
        rows.append((f"BLSY {y} BLSX {x}", f, lab))
    lh = int(size * 1.35)
    H = len(rows) * (len(LINES) * lh + 50) + 20
    img = Image.new("L", (int(size * 17), H), 255)
    d = ImageDraw.Draw(img)
    yy = 10
    for label, f, lab in rows:
        d.text((20, yy), label, font=lab, fill=120)
        yy += 30
        for ln in LINES:
            d.text((20, yy), ln, font=f, fill=0)
            yy += lh
        yy += 20
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 64)
