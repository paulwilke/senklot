"""Generic variable-font assembly from per-master contour dicts."""
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.TupleVariation import TupleVariation
from fontTools.ttLib.tables import _g_l_y_f


def contours_to_glyph(contours):
    """Write contours verbatim (no point merging) so all masters stay compatible."""
    from array import array
    from fontTools.ttLib.tables import ttProgram
    g = Glyph()
    pts, flags, ends = [], [], []
    for c in contours:
        for x, y, on in c:
            pts.append((round(x), round(y)))
            flags.append(1 if on else 0)
        ends.append(len(pts) - 1)
    g.numberOfContours = len(contours)
    g.coordinates = GlyphCoordinates(pts)
    g.flags = array("B", flags)
    g.endPtsOfContours = ends
    g.program = ttProgram.Program()
    g.program.fromBytecode(b"")
    if contours:
        g.flags[0] |= _g_l_y_f.flagOverlapSimple
    return g


def build(family, style, upm, ascent, descent, xh, caph, cmap, masters, axes,
          out_path, fea=None, version="1.000", instances=None, stat=None, weight_class=400):
    """masters: list of (location dict, {glyph: (advance, contours)}); first is default."""
    default_loc, default_glyphs = masters[0]
    order = [".notdef"] + [g for g in default_glyphs if g != ".notdef"]
    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    glyf = {}
    metrics = {}
    for g in order:
        adv, cs = default_glyphs[g]
        glyf[g] = contours_to_glyph(cs)
        metrics[g] = (adv, 0)
    fb.setupGlyf(glyf)
    for g in order:
        gl = fb.font["glyf"][g]
        gl.recalcBounds(fb.font["glyf"])
        metrics[g] = (default_glyphs[g][0], getattr(gl, "xMin", 0))
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ascent, descent=-descent)
    fb.setupNameTable({"familyName": family, "styleName": style,
                       "uniqueFontIdentifier": f"{family}-{style}-{version}",
                       "version": f"Version {version}",
                       "copyright": "Copyright 2026 The Senklot Project Authors (https://github.com/paulwilke/senklot), with Reserved Font Name \"Senklot\".",
                       "manufacturer": "The Senklot Project Authors",
                       "description": "Original design, generated procedurally. No third-party outlines used.",
                       "vendorURL": "https://github.com/paulwilke/senklot",
                       "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
                                             "This license is available with a FAQ at: https://openfontlicense.org",
                       "licenseInfoURL": "https://openfontlicense.org"})
    fb.setupOS2(sTypoAscender=ascent, sTypoDescender=-descent, sTypoLineGap=0,
                usWinAscent=ascent + 100, usWinDescent=descent + 100,
                sxHeight=xh, sCapHeight=caph, fsType=0, achVendID="NONE")
    fb.setupPost()
    fb.font['OS/2'].usWeightClass = weight_class
    fb.setupHead(unitsPerEm=upm)
    if len(masters) > 1:
        fb.setupFvar(axes, instances or [])
        coords = {}
        for loc, glyphs in masters:
            key = tuple(sorted(loc.items()))
            coords[key] = {}
            for g in order:
                adv, cs = glyphs[g]
                mg = contours_to_glyph(cs)
                mc = list(mg.getCoordinates(None)[0]) if mg.numberOfContours else []
                coords[key][g] = [(float(x), float(y)) for x, y in mc] + [(0, 0), (adv, 0), (0, 0), (0, 0)]
        base = coords[()]

        def region(loc):
            return {k: (min(0.0, v), v, max(0.0, v)) for k, v in loc.items() if v != 0}

        def scalar(reg, loc):
            sc = 1.0
            for ax, (lo, pk, hi) in reg.items():
                v = loc.get(ax, 0)
                if v == pk:
                    continue
                if v <= lo or v >= hi or (v == 0):
                    return 0.0
                sc *= (v - lo) / (pk - lo) if v < pk else (hi - v) / (hi - pk)
            return sc

        # process masters by number of active axes so corners get residuals
        ordered = sorted([m for m in masters[1:]], key=lambda m: len([v for v in m[0].values() if v]))
        variations = {g: [] for g in order}
        done = []  # (region, {glyph: deltas})
        for loc, _ in ordered:
            key = tuple(sorted(loc.items()))
            reg = region(loc)
            dset = {}
            for g in order:
                tgt = coords[key][g]
                b = base[g]
                assert len(tgt) == len(b), f"incompatible {g}: {len(tgt)} vs {len(b)}"
                pred = [[0.0, 0.0] for _ in b]
                for preg, pd in done:
                    sc = scalar(preg, loc)
                    if sc:
                        for k, (dx, dy) in enumerate(pd[g]):
                            pred[k][0] += sc * dx
                            pred[k][1] += sc * dy
                d = [(t[0] - bb[0] - pr[0], t[1] - bb[1] - pr[1]) for t, bb, pr in zip(tgt, b, pred)]
                dset[g] = d
                rd = [(round(x), round(y)) for x, y in d]
                if any(x or y for x, y in rd):
                    variations[g].append(TupleVariation(reg, rd))
            done.append((reg, dset))
        fb.setupGvar(variations)
    if fea:
        fb.addOpenTypeFeatures(fea)
    if stat:
        fb.setupStat(stat)
    fb.font.save(out_path)
    return fb.font
