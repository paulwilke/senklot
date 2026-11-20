"""Render a seamless looping clip of the swinging title: python src/clip.py

Writes media/senklot-swing.mp4 (1080x1080, 30 fps, 8 s loop).
Each letter swings like the playground's "Swing" mode, slightly delayed
from its neighbour so the mass travels through the word.
"""
import math
import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT = os.path.join(ROOT, "fonts", "Senklot[wght,BLSY,BLSX].ttf")
OUT = os.path.join(ROOT, "media", "senklot-swing.mp4")
W = H = 1080
FPS, SECONDS = 30, 8
BG, INK, MUTED = (244, 241, 234), (22, 21, 15), (111, 107, 96)
WORD, SIZE = "Senklot", 250


def font(size, wght, y=0, x=0):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([wght, y, x])
    return f


def main():
    base = font(SIZE, 600)
    # ballast axes never change advances, so the layout is fixed
    xs, x = [], 0
    for ch in WORD:
        xs.append(x)
        x += base.getlength(ch)
    left = (W - x) / 2
    asc, _ = base.getmetrics()
    top = H / 2 - asc * 0.78
    tag = font(38, 400)
    tag_text = "a typeface with a movable centre of mass"
    tag_x = (W - tag.getlength(tag_text)) / 2

    tmp = tempfile.mkdtemp()
    try:
        n = FPS * SECONDS
        for k in range(n):
            t = k / FPS
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            for i, ch in enumerate(WORD):
                lag = 0.45 * i
                by = 95 * math.sin(2 * math.pi * t / 4 - lag)
                bx = 75 * math.sin(2 * math.pi * t / 8 + 1 - lag / 2)
                d.text((left + xs[i], top), ch, font=font(SIZE, 600, by, bx), fill=INK)
            d.text((tag_x, H / 2 + 170), tag_text, font=tag, fill=MUTED)
            img.save(os.path.join(tmp, f"f{k:04d}.png"))
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(tmp, "f%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-crf", "18", "-movflags", "+faststart", OUT], check=True)
        Image.open(os.path.join(tmp, "f0060.png")).save(OUT.replace(".mp4", "-still.png"))
    finally:
        shutil.rmtree(tmp)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
