"""Assemble the GitHub Pages site in docs/: python src/site.py

Copies the web fonts next to docs/index.html and packs a download zip.
Run after build.py (both styles) and export.py.
"""
import glob
import os
import shutil
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONTS = os.path.join(ROOT, "fonts")
DOCS = os.path.join(ROOT, "docs")


def main():
    out = os.path.join(DOCS, "fonts")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, "static"))
    for p in glob.glob(os.path.join(FONTS, "*.woff2")) + [os.path.join(FONTS, "senklot.css")]:
        shutil.copy(p, out)
    shutil.copy(os.path.join(ROOT, "OFL.txt"), out)
    for p in glob.glob(os.path.join(FONTS, "static", "*.woff2")):
        shutil.copy(p, os.path.join(out, "static"))

    dl = os.path.join(DOCS, "downloads")
    os.makedirs(dl, exist_ok=True)
    zpath = os.path.join(dl, "Senklot.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(ROOT, "README.md"), "Senklot/README.md")
        z.write(os.path.join(ROOT, "OFL.txt"), "Senklot/OFL.txt")
        z.write(os.path.join(ROOT, "OFL.txt"), "Senklot/web/OFL.txt")
        z.write(os.path.join(ROOT, "src", "LICENSE.txt"), "Senklot/LICENSE-CODE.txt")
        for p in sorted(glob.glob(os.path.join(FONTS, "*.*"))):
            z.write(p, "Senklot/web/" + os.path.basename(p) if p.endswith((".woff2", ".css"))
                    else "Senklot/variable/" + os.path.basename(p))
        for p in sorted(glob.glob(os.path.join(FONTS, "static", "*"))):
            sub = "web/static/" if p.endswith(".woff2") else "static/"
            z.write(p, "Senklot/" + sub + os.path.basename(p))
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    print("site assembled:", DOCS, f"(zip {os.path.getsize(zpath) // 1024} KB)")


if __name__ == "__main__":
    main()
