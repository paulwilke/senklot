"""Build Senklot variable fonts: python src/build.py [--italic]"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import engine  # noqa: E402

ITALIC = "--italic" in sys.argv
ANGLE = 9.0
if ITALIC:
    engine.SLANT = math.tan(math.radians(ANGLE))

from glyphs import GLYPHS, XH, CAP, ASC, DSC  # noqa: E402
from build_lib import build  # noqa: E402
from engine import Path  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "fonts")
os.makedirs(OUT, exist_ok=True)

LOCS = [{}]
for ax in ("W", "Y", "X"):
    LOCS += [{ax: 1}, {ax: -1}]
for w in (1, -1):
    for ax in ("Y", "X"):
        for v in (1, -1):
            LOCS.append({"W": w, ax: v})
TAG = {"W": "wght", "Y": "BLSY", "X": "BLSX"}
WEIGHTS = [(300, "Light"), (400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"), (800, "ExtraBold")]


def notdef():
    from engine import G
    g = G(".notdef", None, 500)
    for p in (Path().line((60, 0), (60, CAP)), Path().line((440, 0), (440, CAP)),
              Path(bias=-1).line((60, CAP), (440, CAP)), Path(bias=1).line((60, 0), (440, 0))):
        g.add(p)
    return g


def main():
    glyphs = [notdef()] + GLYPHS
    cmap = {}
    for g in glyphs:
        if g.uni is None:
            continue
        cmap[ord(g.uni) if isinstance(g.uni, str) else g.uni] = g.name
        for u in getattr(g, "extra_unis", []):
            cmap[u] = g.name
    masters = []
    for loc in LOCS:
        d = {g.name: (g.advance(loc), g.contours(loc)) for g in glyphs}
        masters.append(({TAG[k]: v for k, v in loc.items()}, d))
    axes = [("wght", 300, 400, 800, "Weight"),
            ("BLSY", -100, 0, 100, "Ballast Vertical"), ("BLSX", -100, 0, 100, "Ballast Horizontal")]
    def iname(n):
        if not ITALIC:
            return n
        return "Italic" if n == "Regular" else n + " Italic"
    instances = [dict(location={"wght": w, "BLSY": 0, "BLSX": 0}, stylename=iname(n)) for w, n in WEIGHTS]
    ital = (dict(value=1, name="Italic") if ITALIC
            else dict(value=0, name="Roman", flags=2, linkedValue=1))
    stat = [dict(tag="wght", name="Weight", values=[dict(value=w, name=n, flags=2 if w == 400 else 0) for w, n in WEIGHTS]),
            dict(tag="BLSY", name="Ballast Vertical", values=[dict(value=0, name="Rest", flags=2)]),
            dict(tag="BLSX", name="Ballast Horizontal", values=[dict(value=0, name="Centered", flags=2)]),
            dict(tag="ital", name="Italic", values=[ital])]
    fea = open(os.path.join(os.path.dirname(__file__), "kern.fea")).read() \
        if os.path.exists(os.path.join(os.path.dirname(__file__), "kern.fea")) else None
    stem_name = "Senklot-Italic" if ITALIC else "Senklot"
    path = os.path.join(OUT, stem_name + "[wght,BLSY,BLSX].ttf")
    build("Senklot", "Italic" if ITALIC else "Regular", 1000, 900, 260, XH, CAP, cmap, masters, axes, path,
          fea=fea, instances=instances, stat=stat)
    from fontTools.ttLib import TTFont
    f = TTFont(path)
    if ITALIC:
        f["post"].italicAngle = -ANGLE
        f["hhea"].caretSlopeRise = 1000
        f["hhea"].caretSlopeRun = round(1000 * engine.SLANT)
        f["OS/2"].fsSelection = (f["OS/2"].fsSelection & ~(1 << 6)) | 1
        f["head"].macStyle |= 2
        f.save(path)
    f.flavor = "woff2"
    f.save(os.path.join(OUT, stem_name + "[wght,BLSY,BLSX].woff2"))
    print("built", path, len(glyphs), "glyphs")


if __name__ == "__main__":
    main()
