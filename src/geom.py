"""Stroke-skeleton geometry -> quadratic TrueType contours.

Every primitive yields a fixed number of points regardless of parameters,
so masters built from the same skeleton are always interpolation-compatible.
A contour is a list of (x, y, on_curve) tuples, clockwise for filled shapes.
"""
import math

ARC_SEGS = 8  # quadratic segments per full turn (<=45 deg each)


def _signed_area(pts):
    a = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i][0], pts[i][1]
        x1, y1 = pts[(i + 1) % n][0], pts[(i + 1) % n][1]
        a += x0 * y1 - x1 * y0
    return a / 2


def clockwise(pts):
    """Return contour oriented clockwise (TrueType outer)."""
    if _signed_area(pts) > 0:
        pts = list(reversed(pts))
        # keep first point on-curve
        while not pts[0][2]:
            pts = pts[1:] + pts[:1]
    return pts


def counter(pts):
    return list(reversed(clockwise(pts)))


def arc_pts(cx, cy, rx, ry, a0, a1, segs):
    """Quadratic approximation of an elliptical arc from a0 to a1 (degrees).
    Returns on/off alternating points, starting and ending on-curve."""
    out = []
    da = (a1 - a0) / segs
    for i in range(segs + 1):
        t = math.radians(a0 + da * i)
        out.append((cx + rx * math.cos(t), cy + ry * math.sin(t), True))
        if i < segs:
            tm = math.radians(a0 + da * (i + 0.5))
            k = 1 / math.cos(math.radians(da / 2))
            out.append((cx + rx * k * math.cos(tm), cy + ry * k * math.sin(tm), False))
    return out


def poly(*xy):
    return clockwise([(x, y, True) for x, y in xy])


def stem(p0, p1, w, cap0=0.0, cap1=0.0):
    """Straight stroke of width w from p0 to p1 (centre line).
    cap0/cap1 extend the stroke beyond its endpoints."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy * w / 2, ux * w / 2
    x0, y0 = x0 - ux * cap0, y0 - uy * cap0
    x1, y1 = x1 + ux * cap1, y1 + uy * cap1
    return poly((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny))


def ring(cx, cy, rx, ry, w):
    """Closed elliptical stroke (two contours)."""
    outer = arc_pts(cx, cy, rx + w / 2, ry + w / 2, 0, 360, ARC_SEGS)[:-1]
    inner = arc_pts(cx, cy, max(rx - w / 2, 1), max(ry - w / 2, 1), 0, 360, ARC_SEGS)[:-1]
    return [clockwise(outer), counter(inner)]


def arc(cx, cy, rx, ry, a0, a1, w, segs=None):
    """Open elliptical stroke between angles a0 and a1 (degrees, CCW)."""
    if segs is None:
        segs = max(1, math.ceil(abs(a1 - a0) / 45))
    outer = arc_pts(cx, cy, rx + w / 2, ry + w / 2, a0, a1, segs)
    inner = arc_pts(cx, cy, max(rx - w / 2, 1), max(ry - w / 2, 1), a1, a0, segs)
    return [clockwise(outer + inner)]


def dot(cx, cy, r):
    return [clockwise(arc_pts(cx, cy, r, r, 0, 360, ARC_SEGS)[:-1])]
