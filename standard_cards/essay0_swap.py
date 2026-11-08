#!/usr/bin/env python3
"""essay0_swap — Sanskrit fixed, English hard-cuts: translation → plain → baumer."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
DEVA = FONTS / "TiroDevanagariSanskrit-Regular.ttf"
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
OUT = Path("/home/box/visuals/outputs/essay0_swap")


def f(path, size, wght=400):
    return ImageFont.truetype(str(path), size, index=0)


def wrap(text, ft, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if ft.getlength(t) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def frame(en_text, en_italic=False):
    """Sanskrit left (fixed), English right (swappable)."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    DEV, IAST = "चैतन्यमात्मा", "caitanyamatma"
    fd, fi = f(DEVA, 120), f(ITAL, 48)
    fe = f(ITAL if en_italic else SERIF, 58, 400 if en_italic else 500)
    # left: Sanskrit + IAST
    dw = fd.getlength(DEV)
    lx = W * 0.28
    d.text((lx - dw / 2, 400), DEV, font=fd, fill=INK)
    iw = fi.getlength(IAST)
    d.text((lx - iw / 2, 540), IAST, font=fi, fill=INK50)
    # right: English, wrapped, centred in band
    lines = wrap(en_text, fe, 700)
    lh = int(58 * 1.45)
    y0 = 400 + (160 - len(lines) * lh) / 2 + 20
    rx = W * 0.70
    for i, ln in enumerate(lines):
        lw = fe.getlength(ln)
        d.text((rx - lw / 2, y0 + i * lh), ln, font=fe, fill=INK)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"): f.unlink()
    states = [
        ("01_translation", "Consciousness is the Self.", False),
        ("02_plain", "consciousness is the nature of self, which truly "
                     "is the divine self, freed of all limiting conditions", False),
        ("03_baumer", "…it means universal consciousness… but this is "
                      "consciousness is not something you are doing — "
                      "it is something which is there.", True),
    ]
    html = ["<html><body style='font-family:sans-serif;background:#fafafa;max-width:1100px;margin:auto'>",
            "<h2>English swap — Sanskrit fixed, right column hard-cuts</h2>"]
    for name, text, italic in states:
        frame(text, italic).save(OUT / f"{name}.png")
        html.append(f"<h3>{name.replace('_', ' ')}</h3>"
                    f"<img src='{name}.png' style='max-width:100%;border:1px solid #ddd'>")
    html.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(html))
    print(f"{len(states)} swap states -> {OUT}")


if __name__ == "__main__":
    main()
