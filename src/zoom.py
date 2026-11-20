import sys
from PIL import Image, ImageDraw, ImageFont
import os
FONT = os.environ.get("FONT", "fonts/Senklot[wght,BLSY,BLSX].ttf")
def main(out, text, size, w=400, y=0, x=0):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([w, y, x])
    lines = text.split("|")
    W = max(int(f.getlength(l)) for l in lines) + 60
    img = Image.new("L", (W, int(size*1.3)*len(lines)+40), 255)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text((30, 20 + i*int(size*1.3)), l, font=f, fill=0)
    img.save(out)
if __name__ == "__main__":
    a = sys.argv; main(a[1], a[2], int(a[3]), *(float(v) for v in a[4:]))
