# Senklot

> Job site. Plumb bob in my hand. I watched it swing, then settle dead still. And I thought: what if type could do that? So I built it. Meet Senklot.

A sans-serif with a **movable centre of mass**, in Roman and a true Italic. Besides a mild stroke contrast (horizontals about 12 % lighter), stroke thickness comes from a *position field* over each glyph, and two axes move its centre. Three variable axes:

| Axis | Range | Default | Effect |
|------|-------|---------|--------|
| `wght` | 300 … 800 | 400 | Light → ExtraBold (standard CSS `font-weight` works) |
| `BLSY` | −100 … 100 | 0 | mass rises (−) / sinks to the baseline (+) |
| `BLSX` | −100 … 100 | 0 | mass drifts left (−) / right (+) |

The italic is a separate file (`font-style: italic` picks it). It slants the skeleton by 9° before stroking and redraws several letters: single-storey a, descending f, exit strokes on a d i h m n u.

The ballast axes never change advance widths, so animating them never reflows text. Dots (i, j, punctuation, umlauts) are "loose ballast": they grow, shrink and drift with the mass.

## Use on a website
Copy these five files into the same folder on your site (they are all in `web/` in the download):
`senklot.css`, `Senklot[wght,BLSY,BLSX].woff2`, `Senklot-Italic[wght,BLSY,BLSX].woff2`, `OFL.txt` and `LICENSE-CODE.txt`.

```html
<link rel="stylesheet" href="/fonts/senklot.css">
```
```css
body   { font-family: "Senklot", system-ui, sans-serif; }
strong { font-weight: 700; }
em     { font-style: italic; }
h1     { font-weight: 600; font-variation-settings: "BLSY" 60, "BLSX" 0; }
```
Note: `font-variation-settings` replaces itself as a whole. If you set it, always give both `BLSY` and `BLSX`, and use `font-weight` for weight.

## Files
- `fonts/Senklot[wght,BLSY,BLSX].woff2`: variable web font with all weights and both ballast axes (≈78 KB)
- `fonts/Senklot-Italic[wght,BLSY,BLSX].woff2`: the italic counterpart (≈85 KB)
- `fonts/Senklot[wght,BLSY,BLSX].ttf`, `fonts/Senklot-Italic[wght,BLSY,BLSX].ttf`: variable TTFs (desktop apps)
- `fonts/static/Senklot-{Light,Regular,Medium,SemiBold,Bold,ExtraBold}{,Italic}.{ttf,woff2}`: 12 static fallbacks (≈10 KB each)
- `fonts/senklot.css`: ready-to-use `@font-face`
- `docs/`: the GitHub Pages site (demo, playground, docs, download zip) in English, German (`docs/de/`) and French (`docs/fr/`). Edit the English page; `src/i18n.py` holds the translations and regenerates the other two. Serve it over HTTP (for example `python3 -m http.server --directory docs`) rather than opening the file directly.

## GitHub Pages
Push the repository, then in **Settings → Pages** choose *Deploy from a branch*, branch `main`, folder `/docs`. The site is fully static and self-contained.

## Character set (182 glyphs)
A–Z, a–z, 0–9, German umlauts and ß, accented letters (À–Ý, à–ÿ, Ç, Ñ, Ø, Ÿ), Œ œ Æ æ, ¡ ¿, German and French quotes („“ ‚‘ « » ‹ ›), punctuation, and `@ # % $ € © ° • … − × ~ ^ | \ { } [ ] < >`.

## Rebuild
```bash
.venv/bin/python src/build.py            # Roman variable font + woff2
.venv/bin/python src/build.py --italic   # Italic variable font + woff2
.venv/bin/python src/export.py           # 12 static instances
.venv/bin/python src/site.py             # copy web fonts + zip into docs/, generate docs/de and docs/fr
```
- `src/engine.py`: stroke/field engine
- `src/glyphs.py`: glyph skeletons
- `src/kern.fea`: kerning
- `src/build_lib.py`: gvar assembly. There are 15 masters, with interaction corners for wght×BLSY and wght×BLSX, so interpolation is exact.

All fonts pass the OpenType Sanitizer (OTS), the check browsers run on web fonts.

## Provenance
The outlines are generated from the letter skeletons defined in [`src/glyphs.py`](src/glyphs.py) (lines and superellipse arcs, offset by the field in [`src/engine.py`](src/engine.py)). The build does not use any existing font file as a template.

## Licence
| What | Licence |
|------|---------|
| Font files, `src/glyphs.py` (letter skeletons), `src/kern.fea` (kerning) | [SIL Open Font License 1.1](OFL.txt), Reserved Font Name "Senklot" |
| Build tools in `src/`, the website in `docs/`, `fonts/senklot.css` | [MIT](src/LICENSE.txt) |

In short: use, embed, modify and redistribute the fonts freely, including commercially. Don't sell the font files on their own. When you redistribute them (in a theme, app or download), include `OFL.txt`. If you distribute a modified version, including a subset you make yourself, give it a different family name unless you have written permission to use "Senklot". The full licence text is what applies.

## Known limits
- No TrueType hinting, so rendering at small sizes on Windows is softer. On macOS, iOS and Android it makes no difference.
- No small caps, ligatures or alternate figures.
- No capital ẞ yet.
- No Central European letters yet (Polish, Czech, Hungarian …).
