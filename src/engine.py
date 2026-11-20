"""Senklot stroke engine.

A glyph is a set of skeleton paths (centre lines) plus free "ballast" dots.
Outlines are produced by offsetting each skeleton sample by a half-width that
comes from a *position field*: thickness depends on where the ink is, not on
the stroke's direction.  The field is linear in both design axes, and every
outline point is linear in the half-width, so gvar interpolation is exact.
"""
import math
from geom import clockwise, counter, arc_pts

EXP = 2.3            # superellipse exponent for all rounds
P = 2 / EXP
H0 = 39              # base half-width (78 unit stem)


def field(x, y, tx, adv, loc):
    """Half-width multiplier bracket at (x, y). loc = {'Y': -1..1, 'X': -1..1}."""
    v = (350 - y) / 550
    u = max(-1.0, min(1.0, (x - adv / 2) / 300))
    return 1 + 0.10 * v + 0.55 * loc.get("Y", 0) * v + 0.40 * loc.get("X", 0) * u


def h0(loc):
    """Base half-width from the weight axis W (-1 = 300, 0 = 400, +1 = 800)."""
    w = loc.get("W", 0)
    return H0 + (33 * w if w > 0 else 11 * w)


def weight_shift(loc):
    """Extra half-width relative to Regular (drives spacing and overshoot compensation)."""
    return h0(loc) - H0


ZONES = {"lc": (260, 260), "cap": (350, 350)}

# Italic: skeletons are sheared *before* offsetting, so strokes keep their
# perpendicular thickness (a true slant, not a squashed oblique).  The field and
# contrast are evaluated on the upright skeleton, so the ballast behaves the same.
SLANT = 0.0          # tan(italic angle); set by build.py before glyphs are imported
SLANT_Y0 = 260       # shear pivot (x-height middle) keeps glyphs centred in their advance


def shear(x, y):
    return x + SLANT * (y - SLANT_Y0)


def contrast(tx):
    return 1 - 0.12 * tx * tx


class Path:
    def __init__(self, bias=0.0, wscale=1.0, wgain=1.0):
        self.s = []       # samples: [x, y, tx, ty, w]
        self.k = []       # segment kinds between samples: 'L' | 'Q'
        self.closed = False
        self.cap0 = ("sq", 0)
        self.cap1 = ("sq", 0)
        self.bias = bias  # -1: left edge on skeleton, +1: right edge on skeleton
        self.wscale = wscale
        self.wgain = wgain   # how strongly this stroke follows the weight axis

    def _add(self, x, y, tx, ty, kind):
        L = math.hypot(tx, ty) or 1
        tx, ty = tx / L, ty / L
        if self.s and abs(self.s[-1][0] - x) < 0.5 and abs(self.s[-1][1] - y) < 0.5:
            return
        if self.s:
            self.k.append(kind)
        self.s.append([x, y, tx, ty, 1.0])

    def line(self, p0, p1):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        self._add(p0[0], p0[1], dx, dy, "L")
        self._add(p1[0], p1[1], dx, dy, "L")
        return self

    def to(self, p1):
        x0, y0 = self.s[-1][0], self.s[-1][1]
        return self.line((x0, y0), p1)

    def arc(self, cx, cy, rx, ry, a0, a1, segs=None, exp=None):
        if segs is None:
            segs = max(1, math.ceil(abs(a1 - a0) / 22.5 - 1e-9))
        sgn = 1 if a1 > a0 else -1
        for i in range(segs + 1):
            x, y, tx, ty = se_point(cx, cy, rx, ry, a0 + (a1 - a0) * i / segs, exp)
            self._add(x, y, tx * sgn, ty * sgn, "Q")
        return self

    def caps(self, c0=None, c1=None):
        if c0:
            self.cap0 = c0
        if c1:
            self.cap1 = c1
        return self

    def taper(self, start=None, end=None):
        n = len(self.s)
        if start is not None:
            self.s[0][4] = start
            if n > 2:
                self.s[1][4] = (1 + start) / 2
        if end is not None:
            self.s[-1][4] = end
            if n > 2:
                self.s[-2][4] = (1 + end) / 2
        return self

    def close(self):
        # drop duplicated end sample
        a, b = self.s[0], self.s[-1]
        if abs(a[0] - b[0]) < 0.5 and abs(a[1] - b[1]) < 0.5:
            self.s.pop()
        else:
            self.k.append("L")
        self.closed = True
        return self

    # --- outline -------------------------------------------------------
    def _movable(self, i):
        """Can sample i be pulled inward vertically as weight grows?"""
        if self.bias != 0:
            return False
        n = len(self.s)
        adj = []
        if i > 0 or self.closed:
            adj.append(self.k[(i - 1) % len(self.k)])
        if i < n - 1 or self.closed:
            adj.append(self.k[i % len(self.k)])
        if all(a == "L" for a in adj) and abs(self.s[i][3]) > 0.3:
            return False
        return True

    def outline(self, adv, loc, zone="lc"):
        hs = []
        base = H0 + self.wgain * (h0(loc) - H0)
        for x, y, tx, ty, w in self.s:
            hs.append(base * self.wscale * w * contrast(tx) * field(x, y, tx, adv, {**loc, "W": 0}))
        # keep round/horizontal outer edges on their zones as weight changes
        dw = weight_shift(loc)
        self._dw = dw
        zc, zh = ZONES[zone]
        orig = self.s
        moved = []
        for i, (x, y, tx, ty, w) in enumerate(orig):
            if dw and self._movable(i):
                k = max(-1.0, min(1.0, (y - zc) / zh))
                y = y - dw * contrast(tx) * (1 + 0.10 * (350 - y) / 550) * k
            if SLANT:
                x = shear(x, y)
                tx = tx + SLANT * ty
                L = math.hypot(tx, ty)
                tx, ty = tx / L, ty / L
            moved.append([x, y, tx, ty, w])
        self.s = moved
        try:
            return self._outline_core(hs)
        finally:
            self.s = orig

    def _outline_core(self, hs):
        left, right = [], []
        for (x, y, tx, ty, w), h in zip(self.s, hs):
            nx, ny = -ty, tx
            hl, hr = h * (1 + self.bias), h * (1 - self.bias)
            left.append([x + nx * hl, y + ny * hl])
            right.append([x - nx * hr, y - ny * hr])
        T = [(s[2], s[3]) for s in self.s]
        if not self.closed:
            for idx, cap in ((0, self.cap0), (-1, self.cap1)):
                kind, val = cap
                tx, ty = T[idx]
                sx, sy = self.s[idx][0], self.s[idx][1]
                L0, R0 = list(left[idx]), list(right[idx])
                for side in (left, right):
                    q = side[idx]
                    if kind == "sq":
                        d = val if idx == -1 else -val
                        q[0] += tx * d
                        q[1] += ty * d
                    elif kind == "x" and val is None:
                        # "snapped" cut: perpendicular, rotated toward nearest axis by <= 24 deg
                        nx_, ny_ = -ty, tx
                        ang = math.degrees(math.atan2(ny_, nx_))
                        tgt = round(ang / 90) * 90
                        diff = max(-12, min(12, tgt - ang))
                        a2 = math.radians(ang + diff)
                        dx_, dy_ = math.cos(a2), math.sin(a2)
                        cr = tx * dy_ - ty * dx_
                        tl = ((sx - L0[0]) * dy_ - (sy - L0[1]) * dx_) / cr
                        tr = ((sx - R0[0]) * dy_ - (sy - R0[1]) * dx_) / cr
                        # never shorten: slide the cut so the shorter side stays put
                        fwd = 1 if idx == -1 else -1
                        back = min(tl * fwd, tr * fwd)
                        t = ((sx - q[0]) * dy_ - (sy - q[1]) * dx_) / cr - back * fwd
                        q[0] += tx * t
                        q[1] += ty * t
                    elif kind == "h":
                        d = val * hs[idx]
                        d = d if idx == -1 else -d
                        q[0] += tx * d
                        q[1] += ty * d
                    elif kind == "dw":
                        d = val * self._dw
                        d = d if idx == -1 else -d
                        q[0] += tx * d
                        q[1] += ty * d
                    elif kind == "x":
                        # cut along a (sheared) vertical through x = val
                        t = (val - q[0] + SLANT * (q[1] - SLANT_Y0)) / (tx - SLANT * ty)
                        q[0] += tx * t
                        q[1] += ty * t
                    elif kind == "y":
                        yc = sy if val is None else val
                        t = (yc - q[1]) / ty
                        q[0] += tx * t
                        q[1] += ty * t
        n = len(self.s)
        nseg = n if self.closed else n - 1

        def side_pts(pts, forward):
            out = []
            segs = range(nseg) if forward else range(nseg - 1, -1, -1)
            if forward:
                for i in segs:
                    j = (i + 1) % n
                    out.append((pts[i][0], pts[i][1], True))
                    if self.k[i] == "Q":
                        out.append(_isect(pts[i], T[i], pts[j], T[j]) + (False,))
                if not self.closed:
                    out.append((pts[-1][0], pts[-1][1], True))
            else:
                if not self.closed:
                    out.append((pts[-1][0], pts[-1][1], True))
                for i in segs:
                    j = (i + 1) % n
                    if self.k[i] == "Q":
                        out.append(_isect(pts[i], T[i], pts[j], T[j]) + (False,))
                    out.append((pts[i][0], pts[i][1], True))
                if self.closed:
                    out = [out[-1]] + out[:-1]
            return out

        if self.closed:
            a = side_pts(left, True)
            b = side_pts(right, True)
            from geom import _signed_area
            if abs(_signed_area(a)) > abs(_signed_area(b)):
                return [clockwise(a), counter(b)]
            return [clockwise(b), counter(a)]
        return [clockwise(side_pts(left, True) + side_pts(right, False))]


def _isect(p, t, q, u):
    cr = t[0] * u[1] - t[1] * u[0]
    if abs(cr) < 1e-6:
        return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    s = ((q[0] - p[0]) * u[1] - (q[1] - p[1]) * u[0]) / cr
    return (p[0] + t[0] * s, p[1] + t[1] * s)


def se_point(cx, cy, rx, ry, deg, exp=None):
    P = 2 / exp if exp else globals()["P"]
    th = math.radians(deg)
    c, s = math.cos(th), math.sin(th)
    if abs(c) < 1e-12:
        c = 0.0
    if abs(s) < 1e-12:
        s = 0.0
    x = cx + rx * math.copysign(abs(c) ** P, c)
    y = cy + ry * math.copysign(abs(s) ** P, s)
    tx = -rx * s * abs(s) ** (1 - P)
    ty = ry * c * abs(c) ** (1 - P)
    return x, y, tx, ty


def se_angle_for_tangent_through(cx, cy, rx, ry, a_lo, a_hi, target):
    """Find angle in [a_lo, a_hi] where the tangent line passes through target."""
    def f(a):
        x, y, tx, ty = se_point(cx, cy, rx, ry, a)
        return tx * (target[1] - y) - ty * (target[0] - x)
    lo, hi = a_lo, a_hi
    flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


class Dot:
    """Loose ballast: grows/shrinks with the field and drifts toward the mass."""
    def __init__(self, cx, cy, r):
        self.cx, self.cy, self.r = cx, cy, r

    def outline(self, adv, loc, zone="lc"):
        v = (350 - self.cy) / 550
        u = max(-1.0, min(1.0, (self.cx - adv / 2) / 300))
        f = 0.55 * loc.get("Y", 0) * v + 0.40 * loc.get("X", 0) * u
        ws = 1 + 0.8 * weight_shift(loc) / H0
        r = self.r * ws * (1 + 0.10 * v + 0.30 * f)
        cx = self.cx + 14 * loc.get("X", 0)
        cy = self.cy - 14 * loc.get("Y", 0)
        cx = shear(cx, cy)
        return [clockwise(arc_pts(cx, cy, r, r, 0, 360, 8)[:-1])]


SPACE_K = 0.85   # how much of the extra stroke width goes into sidebearings


class G:
    def __init__(self, name, uni, adv, zone="lc"):
        self.name, self.uni, self.adv, self.zone = name, uni, adv, zone
        self.items = []
        self.extra_unis = []

    def add(self, *items):
        self.items.extend(items)
        return self

    def advance(self, loc):
        if not self.items:          # spaces scale gently
            return round(self.adv + 0.5 * weight_shift(loc))
        return round(self.adv + 2 * SPACE_K * weight_shift(loc))

    def contours(self, loc):
        dx = (self.advance(loc) - self.adv) / 2
        out = []
        for it in self.items:
            for c in it.outline(self.adv, loc, self.zone):
                out.append([(x + dx, y, on) for x, y, on in c])
        return out
