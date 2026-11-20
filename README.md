# Senklot

> I was on my construction site, working with a plumb bob. Watching it swing, I wondered: what if a typeface could sway and settle like that? That’s Senklot.

A sans-serif with a **movable centre of mass**, in Roman and a true Italic. Stroke thickness is a *position field* over each glyph, not a function of stroke direction. Three variable axes:

| Axis | Range | Default | Effect |
|------|-------|---------|--------|
| `wght` | 300 … 800 | 400 | Light → ExtraBold (standard CSS `font-weight` works) |
| `BLSY` | −100 … 100 | 0 | mass rises (−) / sinks to the baseline (+) |
| `BLSX` | −100 … 100 | 0 | mass drifts left (−) / right (+) |

The italic is a separate file (`font-style: italic` picks it). It slants the skeleton by 9° before stroking and redraws several letters: single-storey a, descending f, exit strokes on a d i h m n u.

The ballast axes never change advance widths, so animating them never reflows text. Dots (i, j, punctuation, umlauts) are "loose ballast": they grow, shrink and drift with the mass.

## Use on a website
Copy `fonts/senklot.css`, `fonts/Senklot[wght,BLSY,BLSX].woff2` and `fonts/Senklot-Italic[wght,BLSY,BLSX].woff2` into the same folder on your site:

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
- `fonts/Senklot[wght,BLSY,BLSX].woff2`: variable web font with all weights and both ballast axes (≈72 KB)
- `fonts/Senklot-Italic[wght,BLSY,BLSX].woff2`: the italic counterpart (≈80 KB)
- `fonts/Senklot[wght,BLSY,BLSX].ttf`, `fonts/Senklot-Italic[wght,BLSY,BLSX].ttf`: variable TTFs (desktop apps)
- `fonts/static/Senklot-{Light,Regular,Medium,SemiBold,Bold,ExtraBold}{,Italic}.{ttf,woff2}`: 12 static fallbacks (≈10 KB each)
- `fonts/senklot.css`: ready-to-use `@font-face`
- `docs/`: the GitHub Pages site (demo, playground, docs, download zip) in English, German (`docs/de/`) and French (`docs/fr/`). Edit the English page; `src/i18n.py` holds the translations and regenerates the other two. Serve it over HTTP (for example `python3 -m http.server --directory docs`) rather than opening the file directly.

## GitHub Pages
Push the repository, then in **Settings → Pages** choose *Deploy from a branch*, branch `main`, folder `/docs`. The site is fully static and self-contained.

## Character set (175 glyphs)
A–Z, a–z, 0–9, Western European accents (À–Ý, à–ÿ, Ç, Ñ, Ø), ß, German and French quotes („“ ‚‘ « » ‹ ›), punctuation, and `@ # % $ € © ° • … − × ~ ^ | \ { } [ ] < >`.

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
Every outline is generated from original parametric skeletons written for this project (lines plus superellipse arcs, offset by the field). No existing font's outlines, metrics or data were used, traced or derived.

## Licence
Senklot is licensed under the [SIL Open Font License 1.1](OFL.txt): free to use, embed, modify and redistribute, including commercially. The fonts may not be sold on their own. Modified versions must stay under the OFL.

"Senklot" is a **Reserved Font Name**: modified versions must not use the name Senklot. Unmodified copies keep the name. 
The OFL covers the fonts only. The build scripts in `src/` and the website in `docs/` are under the [MIT licence](src/LICENSE.txt).

When you redistribute the font files (in a theme, app or download), include `OFL.txt`. The zip already has a copy in `web/` next to the web fonts.

## Known limits
- No TrueType hinting, so rendering at small sizes on Windows is softer. On macOS, iOS and Android it makes no difference.
- No small caps, ligatures or alternate figures.
- Coverage is Western European Latin only.
