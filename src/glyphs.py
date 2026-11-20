"""Senklot glyph skeletons. All coordinates are original, constructed here.

Part of the Senklot Font Software.
Copyright 2026 The Senklot Project Authors, with Reserved Font Name "Senklot".
Licensed under the SIL Open Font License 1.1 (see OFL.txt), not under the MIT licence of the build tools.
"""
import engine
from engine import G, Path, Dot, se_point, se_angle_for_tangent_through

ITALIC = engine.SLANT != 0          # build.py sets engine.SLANT before importing this module
TAIL = 24                           # extra advance for italic exit tails

XH, CAP, ASC, DSC, OV = 520, 700, 750, -200, 10
V, HH = 39, 34                      # nominal half widths (vertical / horizontal)
LT, LB = XH + OV - HH, -OV + HH     # lowercase round centre-line top/bottom: 496 / 24
CT, CB = CAP + OV - HH, -OV + HH    # caps round centre-line: 676 / 24
DOT_R = 47

GLYPHS = []


def glyph(name, uni, adv, zone=None):
    if zone is None:
        ch = uni if isinstance(uni, str) else (chr(uni) if uni else "")
        zone = "cap" if (ch.isupper() or ch.isdigit()) else "lc"
    g = G(name, uni, adv, zone)
    GLYPHS.append(g)
    return g


def stem(x, y0, y1, **kw):
    return Path(**kw).line((x, y0), (x, y1))


def bar(y_edge, x0, x1, top=True):
    """Horizontal bar whose outer edge sits exactly on y_edge."""
    # tangent +x: left normal points up. top edge on skeleton -> bias -1
    return Path(bias=-1 if top else 1).line((x0, y_edge), (x1, y_edge))


def hbar(y, x0, x1):
    return Path().line((x0, y), (x1, y))


def diag(p0, p1, y0=None, y1=None):
    p = Path().line(p0, p1)
    p.caps(("y", y0) if y0 is not None else None, ("y", y1) if y1 is not None else None)
    return p


def ring(cx, cy, rx, ry, wscale=1.0):
    return Path(wscale=wscale).arc(cx, cy, rx, ry, 0, 360, 16).close()


def x_at(p0, p1, y):
    return p0[0] + (p1[0] - p0[0]) * (y - p0[1]) / (p1[1] - p0[1])


def tilde_path(cx, y, rx, ry, w=0.75, a=30, wgain=0.45):
    """Sine-like wave from two partial elliptical humps (no tight turns)."""
    x1, y1, _, _ = se_point(0, 0, rx, ry, a, 2)
    x2, y2, _, _ = se_point(0, 0, rx, ry, 180 + a, 2)
    c1 = (cx - x1, y - y1)
    c2 = (cx - x2, y - y2)
    return (Path(wscale=w, wgain=wgain).arc(c1[0], c1[1], rx, ry, 180 - a, a, exp=2)
            .arc(c2[0], c2[1], rx, ry, 180 + a, 360 - a, exp=2))


# ---------------------------------------------------------------- lowercase
def bowl_right_of_stem(L, rx=200, cy=260, ry=236):
    return Path().arc(L + rx, cy, rx, ry, 163, -163).taper(0.62, 0.62)


def bowl_left_of_stem(R, rx=200, cy=260, ry=236):
    return Path().arc(R - rx, cy, rx, ry, 17, 343).taper(0.62, 0.62)


def arch(L, R, top=LT, cy=300, start=172, tail=False):
    rx = (R - L) / 2
    p = Path().arc(L + rx, cy, rx, top - cy, start, 0)
    if tail:
        return add_tail(p.to((R, 110)), R).taper(start=0.55)
    return p.to((R, 0)).taper(start=0.55)


def add_tail(p, x):
    """Italic exit stroke: the stem rolls out to the right at the baseline."""
    return p.arc(x + 64, 110, 64, 110 - LB, 180, 292).caps(None, ("x", None))


def tail_stem(x, top):
    return add_tail(Path().line((x, top), (x, 110)), x)


def lc():
    # o
    g = glyph("o", "o", 572)
    g.add(ring(286, 260, 205, 236))
    # c
    g = glyph("c", "c", 520)
    g.add(Path().arc(280, 260, 198, 236, 42, 318).caps(("x", None), ("x", None)))
    # e
    g = glyph("e", "e", 560)
    cx, rx = 282, 200
    g.add(Path().arc(cx, 260, rx, 236, -2, 322).caps(None, ("x", None)))
    g.add(hbar(248, cx - rx, cx + rx).caps(None, ("h", 1.0)))
    # n h m
    L = 99
    t = TAIL if ITALIC else 0
    g = glyph("n", "n", 566 + t)
    g.add(stem(L, 0, XH), arch(L, 467, tail=ITALIC))
    g = glyph("h", "h", 566 + t)
    g.add(stem(L, 0, ASC), arch(L, 467, tail=ITALIC))
    g = glyph("m", "m", 818 + t)
    g.add(stem(L, 0, XH), arch(L, 408, cy=310), arch(408, 717, cy=310, tail=ITALIC))
    # u
    g = glyph("u", "u", 566 + t)
    R = 467
    rx = (R - L) / 2
    g.add(Path().line((L, XH), (L, 220)).arc(L + rx, 220, rx, 220 - LB, 180, 352).taper(end=0.55),
          tail_stem(R, XH) if ITALIC else stem(R, 0, XH))
    # r
    g = glyph("r", "r", 372)
    g.add(stem(L, 0, XH), Path().arc(L + 150, 300, 150, LT - 300, 172, 62).taper(0.55).caps(None, ("x", None)))
    # b d p q
    g = glyph("b", "b", 583)
    g.add(stem(L, 0, ASC), bowl_right_of_stem(L))
    g = glyph("p", "p", 583)
    g.add(stem(L, DSC, XH), bowl_right_of_stem(L))
    R = 484
    g = glyph("d", "d", 583 + t)
    g.add(tail_stem(R, ASC) if ITALIC else stem(R, 0, ASC), bowl_left_of_stem(R))
    g = glyph("q", "q", 583)
    g.add(stem(R, DSC, XH), bowl_left_of_stem(R))
    # g (single storey)
    g = glyph("g", "g", 583)
    hk_rx, hk_y = 190, -40
    g.add(bowl_left_of_stem(R, cy=270, ry=226),
          Path().line((R, XH), (R, hk_y)).arc(R - hk_rx, hk_y, hk_rx, hk_y - (DSC - OV + HH), 0, -142)
          .caps(None, ("x", None)))
    # i j
    ti = 40 if ITALIC else 0
    g = glyph("i", "i", 237 + ti)
    g.add(tail_stem(L, XH) if ITALIC else stem(L, 0, XH), Dot(L, 668, DOT_R))
    g = glyph("dotlessi", 0x131, 237 + ti)
    g.add(tail_stem(L, XH) if ITALIC else stem(L, 0, XH))
    g = glyph("j", "j", 262)
    J = 165
    g.add(Path().line((J, XH), (J, -60)).arc(J - 120, -60, 120, -60 - (DSC - OV + HH), 0, -118)
          .caps(None, ("x", None)), Dot(J, 668, DOT_R))
    # l t f
    g = glyph("l", "l", 300)
    g.add(Path().line((L, ASC), (L, 130)).arc(L + 96, 130, 96, 130 - LB, 180, 302).caps(None, ("x", None)))
    T = 150
    g = glyph("t", "t", 352)
    g.add(Path().line((T, 650), (T, 130)).arc(T + 96, 130, 96, 130 - LB, 180, 302).caps(None, ("x", None)),
          bar(XH, T - 112, T + 168))
    if ITALIC:
        # italic f drops through the baseline and hooks back, like j
        Tf = 176
        g = glyph("f", "f", 352)
        g.add(Path().arc(Tf + 112, 590, 112, ASC + OV - HH - 590, 52, 180).to((Tf, -60))
              .arc(Tf - 112, -60, 112, -60 - (DSC - OV + HH), 0, -118).caps(("x", None), ("x", None)),
              bar(XH, Tf - 112, Tf + 156))
    else:
        g = glyph("f", "f", 340)
        g.add(Path().line((T, 0), (T, 590)).arc(T + 112, 590, 112, ASC + OV - HH - 590, 180, 52)
              .caps(None, ("x", None)),
              bar(XH, T - 112, T + 168))
    # k
    g = glyph("k", "k", 520)
    g.add(stem(L, 0, ASC),
          diag((L, 150), (L + 340, XH), None, XH),
          diag((L + 112, 268), (L + 368, 0), None, 0))
    # v w x y z
    g = glyph("v", "v", 520)
    g.add(diag((78, XH), (246, 0), XH, 0), diag((274, 0), (442, XH), 0, XH))
    g = glyph("w", "w", 780)
    g.add(diag((70, XH), (212, 0), XH, 0), diag((236, 0), (378, XH), 0, XH),
          diag((402, XH), (544, 0), XH, 0), diag((568, 0), (710, XH), 0, XH))
    g = glyph("x", "x", 510)
    g.add(diag((72, 0), (438, XH), 0, XH), diag((72, XH), (438, 0), XH, 0))
    g = glyph("y", "y", 520)
    rt, rb = (444, XH), (160, DSC)
    jx = x_at(rt, rb, 6)
    g.add(diag(rt, rb, XH, DSC), diag((76, XH), (jx + 14, 6), XH, None))
    g = glyph("z", "z", 500)
    g.add(bar(XH, 70, 428).caps(("dw", 1.4), ("dw", 1.4)), bar(0, 64, 440, top=False).caps(("dw", 1.4), ("dw", 1.4)), diag((428 - 50, XH), (64 + 50, 0), XH, 0))
    if ITALIC:
        # a (single storey, italic)
        g = glyph("a", "a", 560 + t)
        R = 460
        g.add(bowl_left_of_stem(R, rx=192), tail_stem(R, XH))
        lc_tail()
        return
    # a (double storey)
    g = glyph("a", "a", 530)
    R, cx = 432, 266
    g.add(Path().line((R, -OV), (R, 330)).arc(R - 166, 330, 166, LT - 330, 0, 148).caps(None, ("x", None)))
    bx = 232
    g.add(Path().line((R, 292), (bx, 292)).arc(bx, (292 + LB) / 2, 148, (292 - LB) / 2, 90, 270)
          .to((R, LB)))
    lc_tail()


def lc_tail():
    # s
    g = glyph("s", "s", 500)
    cx, sp = 250, 254
    yt, ryt = (LT + sp) / 2, (LT - sp) / 2
    yb, ryb = (sp + LB) / 2, (sp - LB) / 2
    g.add(Path().arc(cx, yt, 158, ryt, 26, 270).arc(cx, yb, 174, ryb, 90, -152)
          .caps(("x", None), ("x", None)))
    # ß
    g = glyph("germandbls", 0xDF, 600)
    L2 = 99
    g.add(stem(L2, 0, 560),
          Path().arc(L2 + 140, 560, 140, ASC + OV - HH - 560, 180, -90).to((L2 + 110, 396)),
          Path().line((L2 + 110, 396), (L2 + 150, 396)).arc(L2 + 150, (396 + LB) / 2, 196, (396 - LB) / 2, 90, -112)
          .caps(None, ("x", None)))


# ---------------------------------------------------------------- uppercase
def uc():
    L = 109
    g = glyph("H", "H", 746)
    g.add(stem(L, 0, CAP), stem(637, 0, CAP), hbar(336, L, 637))
    g = glyph("I", "I", 238)
    g.add(stem(119, 0, CAP))
    g = glyph("E", "E", 594)
    g.add(stem(L, 0, CAP), bar(CAP, L, 532), hbar(336, L, 492), bar(0, L, 540, top=False))
    g = glyph("F", "F", 574)
    g.add(stem(L, 0, CAP), bar(CAP, L, 532), hbar(326, L, 492))
    g = glyph("L", "L", 548)
    g.add(stem(L, 0, CAP), bar(0, L, 520, top=False))
    g = glyph("T", "T", 610)
    g.add(bar(CAP, 36, 574), stem(305, 0, CAP - 20))
    g = glyph("O", "O", 750)
    g.add(ring(375, 350, 291, 326))
    g = glyph("Q", "Q", 750)
    g.add(ring(375, 350, 291, 326), diag((455, 150), (690, -70), None, -70))
    g = glyph("C", "C", 646)
    g.add(Path().arc(372, 350, 288, 326, 40, 320).caps(("x", None), ("x", None)))
    g = glyph("G", "G", 724)
    cx, rx = 372, 288
    g.add(Path().arc(cx, 350, rx, 326, 40, 356).caps(("x", None)),
          hbar(328, cx + 40, cx + rx).caps(None, ("h", 1.0)))
    D_x1 = L + 150
    g = glyph("D", "D", 628)
    g.add(stem(L, 0, CAP),
          Path().line((L, 666), (D_x1, 666)).arc(D_x1, 350, 272, 316, 90, -90).to((L, 34)))
    g = glyph("B", "B", 572)
    w = 366
    g.add(stem(L, 0, CAP),
          Path().line((L, 666), (L + 168, 666)).arc(L + 168, (666 + w) / 2, 152, (666 - w) / 2, 90, -90).to((L, w)),
          Path().line((L, w), (L + 182, w)).arc(L + 182, (w + 34) / 2, 178, (w - 34) / 2, 90, -90).to((L, 34)))
    g = glyph("P", "P", 568)
    w = 322
    g.add(stem(L, 0, CAP),
          Path().line((L, 666), (L + 170, 666)).arc(L + 170, (666 + w) / 2, 190, (666 - w) / 2, 90, -90).to((L, w)))
    g = glyph("R", "R", 608)
    w = 330
    g.add(stem(L, 0, CAP),
          Path().line((L, 666), (L + 170, 666)).arc(L + 170, (666 + w) / 2, 186, (666 - w) / 2, 90, -90).to((L, w)),
          diag((L + 214, w), (L + 430, 0), None, 0))
    g = glyph("S", "S", 610)
    cx, sp = 305, 342
    g.add(Path().arc(cx, (CT + sp) / 2, 200, (CT - sp) / 2, 28, 270)
          .arc(cx, (sp + CB) / 2, 220, (sp - CB) / 2, 90, -152).caps(("x", None), ("x", None)))
    g = glyph("U", "U", 718)
    L2, R2 = 105, 613
    rx = (R2 - L2) / 2
    g.add(Path().line((L2, CAP), (L2, 284)).arc(L2 + rx, 284, rx, 284 - CB, 180, 360).to((R2, CAP)))
    g = glyph("J", "J", 520)
    R2 = 410
    g.add(Path().line((R2, CAP), (R2, 236)).arc(R2 - 186, 236, 186, 236 - CB, 0, -158).caps(None, ("x", None)))
    g = glyph("A", "A", 700)
    a0, a1, b0, b1 = (60, 0), (328, CAP), (372, CAP), (640, 0)
    yb = 216
    g.add(diag(a0, a1, 0, CAP), diag(b0, b1, CAP, 0), hbar(yb, x_at(a0, a1, yb), x_at(b0, b1, yb)))
    g = glyph("V", "V", 680)
    g.add(diag((52, CAP), (318, 0), CAP, 0), diag((362, 0), (628, CAP), 0, CAP))
    g = glyph("W", "W", 1000)
    g.add(diag((50, CAP), (250, 0), CAP, 0), diag((288, 0), (482, CAP), 0, CAP),
          diag((518, CAP), (712, 0), CAP, 0), diag((750, 0), (950, CAP), 0, CAP))
    g = glyph("M", "M", 846)
    R = 846 - L
    g.add(stem(L, 0, CAP), stem(R, 0, CAP),
          diag((L + 10, CAP), (403, 0), CAP, 0), diag((443, 0), (R - 10, CAP), 0, CAP))
    g = glyph("N", "N", 742)
    R = 742 - L
    g.add(stem(L, 0, CAP), stem(R, 0, CAP), diag((L + 12, CAP), (R - 12, 0), CAP, 0))
    g = glyph("K", "K", 660)
    g.add(stem(L, 0, CAP), diag((L, 210), (L + 470, CAP), None, CAP), diag((L + 168, 386), (L + 500, 0), None, 0))
    g = glyph("X", "X", 664)
    g.add(diag((62, 0), (602, CAP), 0, CAP), diag((62, CAP), (602, 0), CAP, 0))
    g = glyph("Y", "Y", 650)
    cx, jy = 325, 300
    g.add(diag((50, CAP), (cx, jy), CAP, None), diag((600, CAP), (cx, jy), CAP, None), stem(cx, 0, jy + 20))
    g = glyph("Z", "Z", 620)
    g.add(bar(CAP, 66, 556).caps(("dw", 1.4), ("dw", 1.4)), bar(0, 56, 572, top=False).caps(("dw", 1.4), ("dw", 1.4)), diag((556 - 48, CAP), (56 + 48, 0), CAP, 0))


# ---------------------------------------------------------------- figures
def figures():
    W = 590
    g = glyph("zero", "0", W)
    g.add(ring(W / 2, 350, 214, 326))
    g = glyph("one", "1", W)
    x = 330
    g.add(stem(x, 0, CAP), Path().line((x + 10, CAP - 30), (146, 548)).taper(1.0, 0.9))
    g = glyph("two", "2", W)
    cx, cy, rx, ry = 292, 486, 196, CT - 486
    tgt = (96, 0)
    a = se_angle_for_tangent_through(cx, cy, rx, ry, -10, -80, tgt)
    g.add(Path().arc(cx, cy, rx, ry, 158, a).to(tgt).caps(("x", None), ("y", 0)),
          bar(0, 30, 520, top=False).caps(("dw", 1.4)))
    g = glyph("three", "3", W)
    cx = 284
    w = 366
    g.add(Path().arc(cx, (CT + w) / 2, 176, (CT - w) / 2, 152, -90).to((cx - 56, w)).caps(("x", None)),
          Path().line((cx - 56, w), (cx, w)).arc(cx, (w + CB) / 2, 206, (w - CB) / 2, 90, -152)
          .caps(None, ("x", None)))
    g = glyph("four", "4", W)
    sx, by = 410, 210
    g.add(stem(sx, 0, CAP), hbar(by, 52, 546), diag((sx, CAP), (56, by - 10), CAP, None))
    g = glyph("five", "5", W)
    cx, cy, rx = 286, 230, 210
    ry = cy - CB
    sxp = se_point(cx, cy, rx, ry, 150)[0]
    g.add(bar(CAP, sxp + 8, 500), Path().line((sxp + 8, CAP), (sxp, 300)),
          Path().arc(cx, cy, rx, 446 - cy, 162, -152).taper(0.7).caps(None, ("x", None)))
    g = glyph("six", "6", W)
    cx, rx = 296, 214
    g.add(ring(cx, 230, rx, 230 - CB),
          Path().arc(cx, 350, rx, CT - 350, 48, 180).to((cx - rx, 230)).caps(("x", None)))
    g = glyph("nine", "9", W)
    cx = W - 296
    g.add(ring(cx, 470, rx, CT - 470),
          Path().arc(cx, 350, rx, 350 - CB, 228, 360).to((cx + rx, 470)).caps(("x", None)))
    g = glyph("eight", "8", W)
    cx, w = W / 2, 368
    g.add(ring(cx, (CT + w) / 2, 180, (CT - w) / 2), ring(cx, (w + CB) / 2, 208, (w - CB) / 2 + 4))
    g = glyph("seven", "7", W)
    g.add(bar(CAP, 66, 532).caps(None, ("dw", 1.4)), diag((532 - 44, CAP), (214, 0), CAP, 0))


# ---------------------------------------------------------------- punctuation
def punct():
    glyph("space", " ", 250)
    g = glyph("period", ".", 236)
    g.add(Dot(118, DOT_R, DOT_R))
    g = glyph("comma", ",", 236)
    g.add(Dot(118, DOT_R, DOT_R), Path().line((138, 40), (82, -130)).taper(1.0, 0.55))
    g = glyph("colon", ":", 236)
    g.add(Dot(118, DOT_R, DOT_R), Dot(118, XH - DOT_R, DOT_R))
    g = glyph("semicolon", ";", 236)
    g.add(Dot(118, XH - DOT_R, DOT_R), Dot(118, DOT_R, DOT_R), Path().line((138, 40), (82, -130)).taper(1.0, 0.55))
    g = glyph("exclam", "!", 252)
    g.add(Path().line((126, CAP), (126, 210)).taper(1.0, 0.72), Dot(126, DOT_R, DOT_R))
    g = glyph("question", "?", 500)
    cx, cy, rx = 248, 516, 170
    g.add(Path().arc(cx, cy, rx, CT - cy, 160, -90).caps(("x", None)),
          Path().line((cx, cy - (CT - cy) + 4), (cx, 210)).taper(None, 0.8), Dot(cx, DOT_R, DOT_R))
    g = glyph("hyphen", "-", 360)
    g.add(hbar(270, 62, 298))
    g = glyph("endash", 0x2013, 520)
    g.add(hbar(270, 40, 480))
    g = glyph("emdash", 0x2014, 900)
    g.add(hbar(270, 40, 860))
    g = glyph("quotesingle", "'", 220)
    g.add(Path().line((110, CAP), (110, 500)).taper(1.0, 0.7))
    g = glyph("quotedbl", '"', 360)
    g.add(Path().line((110, CAP), (110, 500)).taper(1.0, 0.7), Path().line((250, CAP), (250, 500)).taper(1.0, 0.7))

    def high_comma(x, flip=False):
        y = 640
        if not flip:
            return [Dot(x, y, DOT_R * 0.92), Path().line((x + 20, y - 6), (x - 34, y - 160)).taper(1.0, 0.5)]
        return [Dot(x, y - 100, DOT_R * 0.92), Path().line((x - 20, y - 94), (x + 34, y + 60)).taper(1.0, 0.5)]

    glyph("quoteright", 0x2019, 236).add(*high_comma(118))
    glyph("quoteleft", 0x2018, 236).add(*high_comma(118, True))
    glyph("quotedblright", 0x201D, 380).add(*high_comma(118), *high_comma(262))
    glyph("quotedblleft", 0x201C, 380).add(*high_comma(118, True), *high_comma(262, True))
    g = glyph("parenleft", "(", 300)
    g.add(Path().arc(300, 280, 196, 520, 130, 230))
    g = glyph("parenright", ")", 300)
    g.add(Path().arc(0, 280, 196, 520, 50, -50))
    g = glyph("bracketleft", "[", 300)
    g.add(stem(110, -160, 760), bar(760, 110, 250), bar(-160, 110, 250, top=False))
    g = glyph("bracketright", "]", 300)
    g.add(stem(190, -160, 760), bar(760, 50, 190), bar(-160, 50, 190, top=False))
    g = glyph("slash", "/", 400)
    g.add(diag((40, -120), (360, 760), -120, 760))
    g = glyph("plus", "+", 560)
    g.add(hbar(300, 70, 490), stem(280, 90, 510))
    g = glyph("equal", "=", 560)
    g.add(hbar(392, 70, 490), hbar(208, 70, 490))
    g = glyph("underscore", "_", 520)
    g.add(bar(-80, 20, 500))
    g = glyph("asterisk", "*", 440)
    import math
    for k in range(5):
        a = math.radians(90 + 72 * k)
        g.add(Path().line((220, 560), (220 + 130 * math.cos(a), 560 + 130 * math.sin(a))).taper(0.9, 0.75))
    g = glyph("ampersand", "&", 680)
    cx = 284
    g.add(ring(cx, 552, 128, CT - 552),
          Path().line((cx - 78, 456), (cx + 330, 0)).caps(None, ("y", 0)),
          Path().arc(cx + 10, 200, 214, 200 - CB, 128, 372).caps(None, ("x", None)))


# ---------------------------------------------------------------- marks & composites
LC_MB, UC_MB = 590, 760          # bottom of the mark zone


def mark(kind, cx, cap=False):
    b = UC_MB if cap else LC_MB
    hgt = 112 if cap else 140
    if kind == "acute":
        return [Path().line((cx - 40, b + 4), (cx + 52, b + hgt + 16)).taper(0.72, 1.0)]
    if kind == "grave":
        return [Path().line((cx + 40, b + 4), (cx - 52, b + hgt + 16)).taper(0.72, 1.0)]
    if kind == "circumflex":
        return [diag((cx - 96, b + 4), (cx - 12, b + hgt), b + 4, b + hgt),
                diag((cx + 12, b + hgt), (cx + 96, b + 4), b + hgt, b + 4)]
    if kind == "tilde":
        y = b + hgt * 0.5
        return [tilde_path(cx, y, 56, 40 if cap else 46, w=0.6)]
    if kind == "dieresis":
        return [Dot(cx - 100, b + 78, 42), Dot(cx + 100, b + 78, 42)]
    if kind == "ring":
        return [ring(cx, b + (70 if cap else 84), 66, 60 if cap else 66, wscale=0.62)]
    if kind == "cedilla":
        return [Path().line((cx + 10, 30), (cx + 10, -50)).arc(cx - 40, -50, 50, 66, 0, -150)
                .caps(None, ("x", None))]
    raise KeyError(kind)


MARK_UNI = {"grave": "GRAVE", "acute": "ACUTE", "circumflex": "CIRCUMFLEX", "tilde": "TILDE",
            "dieresis": "DIAERESIS", "ring": "RING ABOVE", "cedilla": "CEDILLA"}
COMPOSITES = {
    "a": ("grave acute circumflex tilde dieresis ring", 268 if ITALIC else 250),
    "c": ("cedilla", 280), "e": ("grave acute circumflex dieresis", 282),
    "i": ("grave acute circumflex dieresis", 99), "n": ("tilde", 283),
    "o": ("grave acute circumflex tilde dieresis", 286), "u": ("grave acute circumflex dieresis", 283),
    "y": ("acute dieresis", 262),
    "A": ("grave acute circumflex tilde dieresis ring", 350), "C": ("cedilla", 372),
    "E": ("grave acute circumflex dieresis", 320), "I": ("grave acute circumflex dieresis", 119),
    "N": ("tilde", 371), "O": ("grave acute circumflex tilde dieresis", 375),
    "U": ("grave acute circumflex dieresis", 359), "Y": ("acute dieresis", 325),
}


def accents():
    import unicodedata
    by = {g.name: g for g in GLYPHS}
    for base, (marks, cx) in COMPOSITES.items():
        cap = base.isupper()
        src = by["dotlessi" if base == "i" else base]
        for m in marks.split():
            name = f"LATIN {'CAPITAL' if cap else 'SMALL'} LETTER {base.upper()} WITH {MARK_UNI[m]}"
            uni = ord(unicodedata.lookup(name))
            gname = base + ("ring" if m == "ring" else m)
            g = glyph(gname, uni, src.adv, zone=src.zone)
            g.items = list(src.items)
            mx = cx
            if m == "dieresis" and base == "i":
                g.items = list(src.items)
                g.add(Dot(cx - 84, LC_MB + 78, 40), Dot(cx + 84, LC_MB + 78, 40))
                continue
            g.add(*mark(m, mx, cap))
    # slashed o
    g = glyph("oslash", 0xF8, by["o"].adv)
    g.items = list(by["o"].items)
    g.add(diag((86, -30), (486, 550), -30, 550))
    g = glyph("Oslash", 0xD8, by["O"].adv)
    g.items = list(by["O"].items)
    g.add(diag((90, -30), (660, 730), -30, 730))
    # spacing marks
    glyph("grave", "`", 300, zone="lc").add(*mark("grave", 150))
    glyph("acute", 0xB4, 300, zone="lc").add(*mark("acute", 150))
    glyph("dieresis", 0xA8, 400, zone="lc").add(*mark("dieresis", 200))


def symbols():
    from engine import G  # noqa
    sp = next(g for g in GLYPHS if g.name == "space")
    sp.extra_unis = [0xA0, 0x2009 - 0x2009 + 0xA0]
    hy = next(g for g in GLYPHS if g.name == "hyphen")
    hy.extra_unis = [0x2010, 0x2011, 0xAD]

    def comma_at(x):
        return [Dot(x, DOT_R, DOT_R), Path().line((x + 20, 40), (x - 36, -130)).taper(1.0, 0.55)]

    glyph("quotesinglbase", 0x201A, 236).add(*comma_at(118))
    glyph("quotedblbase", 0x201E, 380).add(*comma_at(118), *comma_at(262))

    def chevron(x0, x1, ymid, half):
        return [Path().line((x1, ymid + half), (x0, ymid)).caps(None, ("x", x0 - 10)),
                Path().line((x0, ymid), (x1, ymid - half)).caps(("x", x0 - 10))]

    def chevron_r(x0, x1, ymid, half):
        return [Path().line((x0, ymid + half), (x1, ymid)).caps(None, ("x", x1 + 10)),
                Path().line((x1, ymid), (x0, ymid - half)).caps(("x", x1 + 10))]

    glyph("guilsinglleft", 0x2039, 320).add(*chevron(80, 230, 270, 160))
    glyph("guilsinglright", 0x203A, 320).add(*chevron_r(90, 240, 270, 160))
    glyph("guillemotleft", 0xAB, 500).add(*chevron(80, 230, 270, 160), *chevron(250, 400, 270, 160))
    glyph("guillemotright", 0xBB, 500).add(*chevron_r(100, 250, 270, 160), *chevron_r(270, 420, 270, 160))
    glyph("less", "<", 560).add(*chevron(90, 470, 300, 220))
    glyph("greater", ">", 560).add(*chevron_r(90, 470, 300, 220))
    glyph("ellipsis", 0x2026, 640).add(Dot(110, DOT_R, DOT_R), Dot(320, DOT_R, DOT_R), Dot(530, DOT_R, DOT_R))
    glyph("periodcentered", 0xB7, 236).add(Dot(118, 300, DOT_R))
    glyph("bullet", 0x2022, 360).add(Dot(180, 300, 92))
    glyph("degree", 0xB0, 340, zone="cap").add(ring(170, 576, 86, 88, wscale=0.7))
    glyph("bar", "|", 260).add(stem(130, -160, 760))
    glyph("backslash", "\\", 400).add(diag((40, 760), (360, -120), 760, -120))
    glyph("minus", 0x2212, 560).add(hbar(300, 70, 490))
    glyph("multiply", 0xD7, 560).add(Path().line((120, 100), (440, 420)), Path().line((120, 420), (440, 100)))
    glyph("asciitilde", "~", 560).add(tilde_path(280, 300, 72, 56, 0.72))
    glyph("asciicircum", "^", 520).add(diag((80, 300), (248, CAP), 300, CAP), diag((272, CAP), (440, 300), CAP, 300))
    g = glyph("numbersign", "#", 640, zone="cap")
    g.add(hbar(470, 60, 580), hbar(230, 60, 580),
          diag((196, 0), (290, CAP), 0, CAP), diag((350, 0), (444, CAP), 0, CAP))
    g = glyph("percent", "%", 720, zone="cap")
    g.add(ring(170, 536, 102, 130), ring(550, 164, 102, 130), diag((130, 0), (590, CAP), 0, CAP))
    g = glyph("dollar", "$", 590, zone="cap")
    cx, sp_ = 295, 342
    g.add(Path().arc(cx, (CT + sp_) / 2, 186, (CT - sp_) / 2, 28, 270)
          .arc(cx, (sp_ + CB) / 2, 204, (sp_ - CB) / 2, 90, -152).caps(("x", None), ("x", None)),
          stem(cx, CAP - 20, 800), stem(cx, -100, 20))
    g = glyph("Euro", 0x20AC, 640, zone="cap")
    g.add(Path().arc(360, 350, 262, 326, 40, 320).caps(("x", None), ("x", None)),
          hbar(410, 30, 430), hbar(282, 30, 400))
    g = glyph("at", "@", 920)
    cx, cy = 450, 270
    g.add(ring(cx, cy + 20, 120, 142),
          Path().line((cx + 120, 440), (cx + 120, cy)).arc(cx + 200, cy, 80, 110, 180, 360)
          .arc(cx, cy, 280, 350, 0, 318).caps(None, ("x", None)))
    g = glyph("copyright", 0xA9, 860, zone="cap")
    g.add(Path(wscale=0.8).arc(430, 350, 330, 330, 0, 360, 16).close(),
          Path(wscale=0.8).arc(440, 350, 140, 156, 42, 318).caps(("x", None), ("x", None)))
    g = glyph("braceleft", "{", 330)
    g.add(Path().line((260, 760), (230, 760)).arc(230, 640, 60, 120, 90, 180).to((170, 400))
          .arc(110, 400, 60, 100, 0, -90).caps(None, ("sq", 6)),
          Path().line((110, 300), (170, 300)).caps(("sq", 6)),
          Path().arc(110, 200, 60, 100, 90, 0).to((170, -40)).arc(230, -40, 60, 120, 180, 270).to((260, -160)))
    g = glyph("braceright", "}", 330)
    g.add(Path().line((70, 760), (100, 760)).arc(100, 640, 60, 120, 90, 0).to((160, 400))
          .arc(220, 400, 60, 100, 180, 270).caps(None, ("sq", 6)),
          Path().line((220, 300), (160, 300)).caps(("sq", 6)),
          Path().arc(220, 200, 60, 100, 90, 180).to((160, -40)).arc(100, -40, 60, 120, 0, -90).to((70, -160)))

def extras():
    """Œ œ Æ æ ¡ ¿: built from the same skeleton pieces as their parent letters."""
    # œ: an o and an e sharing their middle stroke
    g = glyph("oe", 0x153, 860)
    g.add(ring(266, 260, 190, 236))
    cx, rx = 456 + 190, 190
    g.add(Path().arc(cx, 260, rx, 236, -2, 322).caps(None, ("x", None)),
          hbar(248, cx - rx, cx + rx).caps(None, ("h", 1.0)))
    # æ: a bowl (single-storey in italic) joined to an e
    if ITALIC:
        g = glyph("ae", 0xE6, 850)
        R = 420
        g.add(bowl_left_of_stem(R, rx=180), stem(R, 0, XH))
    else:
        g = glyph("ae", 0xE6, 840)
        R = 420
        g.add(Path().line((R, 248), (R, 330)).arc(R - 160, 330, 160, LT - 330, 0, 148).caps(None, ("x", None)))
        bx = 226
        g.add(Path().line((R, 292), (bx, 292)).arc(bx, (292 + LB) / 2, 142, (292 - LB) / 2, 90, 270)
              .to((R - 40, LB)))
    cx, rx = R + 190, 190
    g.add(Path().arc(cx, 260, rx, 236, -2, 200).caps(None, ("x", None)),
          Path().arc(cx, 260, rx, 236, 200, 322).caps(None, ("x", None)),
          hbar(248, R, cx + rx).caps(None, ("h", 1.0)))
    # Œ: left half of an O closed by an E
    S = 384
    g = glyph("OE", 0x152, 836)
    g.add(Path().arc(S, 350, 262, 326, 90, 270), stem(S, 0, CAP),
          bar(CAP, S, S + 330), hbar(336, S, S + 290), bar(0, S, S + 340, top=False))
    # Æ: the A's left leg leaning on an E
    S = 430
    g = glyph("AE", 0xC6, 880)
    a0, a1 = (60, 0), (S, CAP)
    g.add(diag(a0, a1, 0, CAP), stem(S, 0, CAP), hbar(216, x_at(a0, a1, 216), S),
          bar(CAP, S - 20, S + 330), hbar(336, S, S + 290), bar(0, S, S + 340, top=False))
    # ¡ ¿: the ! and ? turned upside down, hanging from the x-height
    g = glyph("exclamdown", 0xA1, 252)
    g.add(Dot(126, XH - DOT_R, DOT_R), Path().line((126, 310), (126, DSC)).taper(0.72, 1.0))
    g = glyph("questiondown", 0xBF, 500)
    cx, cy = 252, 4
    g.add(Path().arc(cx, cy, 170, 160, 340, 90).caps(("x", None)),
          Path().line((cx, cy + 160 - 4), (cx, 310)).taper(None, 0.8), Dot(cx, XH - DOT_R, DOT_R))


lc()
uc()
figures()
punct()
accents()
symbols()
extras()
