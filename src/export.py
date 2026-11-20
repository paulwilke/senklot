"""Export static instances (TTF + WOFF2) from the variable font: python src/export.py"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.join(os.path.dirname(__file__), "..", "fonts")
VFS = [(os.path.join(ROOT, "Senklot[wght,BLSY,BLSX].ttf"), False),
       (os.path.join(ROOT, "Senklot-Italic[wght,BLSY,BLSX].ttf"), True)]
STATIC = os.path.join(ROOT, "static")
os.makedirs(STATIC, exist_ok=True)

STYLES = [(300, "Light"), (400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"), (800, "ExtraBold")]


def main():
    for vf_path, italic in VFS:
        for w, style in STYLES:
            export(vf_path, italic, w, style)


def export(vf_path, italic, w, style):
        vf = TTFont(vf_path)
        f = instancer.instantiateVariableFont(vf, {"wght": w, "BLSY": 0, "BLSX": 0}, updateFontNames=True)
        os2, head = f["OS/2"], f["head"]
        os2.usWeightClass = w
        # RIBBI style linking: Regular/Italic/Bold/BoldItalic get proper flags
        os2.fsSelection &= ~((1 << 0) | (1 << 5) | (1 << 6))
        head.macStyle = 0
        if style == "Bold":
            os2.fsSelection |= 1 << 5
            head.macStyle = 1
        elif style == "Regular" and not italic:
            os2.fsSelection |= 1 << 6
        if italic:
            os2.fsSelection |= 1
            head.macStyle |= 2
            name = "Italic" if style == "Regular" else style + "Italic"
        else:
            name = style
        base = os.path.join(STATIC, f"Senklot-{name}")
        f.save(base + ".ttf")
        f.flavor = "woff2"
        f.save(base + ".woff2")
        print("wrote", base)


if __name__ == "__main__":
    main()
