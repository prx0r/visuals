#!/usr/bin/env python3
"""essay0_layouts — C-couplet single line (no attrib) + full-verse side-by-side."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
DEVA = FONTS / "TiroDevanagariSanskrit-Regular.ttf"
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
OUT = Path("/home/box/visuals/outputs/essay0_layouts")


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


def ctext(d, s, ft, y, fill=INK):
    lw = ft.getlength(s)
    d.text(((W - lw) / 2, y), s, font=ft, fill=fill)


def single_couplet():
    """C-couplet, no attribution: Sanskrit, IAST, hairline, English."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fd, fi = f(DEVA, 120), f(ITAL, 48)
    fe = f(SERIF, 64, 500)
    DEV, IAST, EN = "चैतन्यमात्मा", "caitanyamatma", "Consciousness is the Self."
    y = 300
    ctext(d, DEV, fd, y);          y += 155
    ctext(d, IAST, fi, y, INK50);  y += 85
    rw = 300
    d.line([(W/2 - rw/2, y + 20), (W/2 + rw/2, y + 20)], fill=INK50, width=1)
    y += 60
    ctext(d, EN, fe, y)
    return im


def full_verse_sidebyside():
    """Vatula SPLIT: multi-line Devanagari+IAST left, English right."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    # sūtra 1.11 tritayabhokta vresah (three-state enjoyer) — fuller verse
    dev_lines = ["त्रितयभोक्ता", "वृषः"]
    iast_lines = ["tritayabhokta", "vṛṣaḥ"]
    en = ("The enjoyer of the three states is the Lord "
          "of the Heroes.")
    fd, fi = f(DEVA, 88), f(ITAL, 40)
    fe = f(SERIF, 58, 500)
    M = 140
    col_l_x = M + 40
    col_r_cx = W * 0.70
    # left column: Devanagari lines with snug IAST under each
    y = 340
    pitch = 140
    for dev, ia in zip(dev_lines, iast_lines):
        d.text((col_l_x, y), dev, font=fd, fill=INK)
        d.text((col_l_x + 10, y + 100), ia, font=fi, fill=INK50)
        y += pitch
    # right column: English, wrapped, centred in its band
    lines = wrap(en, fe, 700)
    lh = int(58 * 1.45)
    y0 = 340 + (pitch * len(dev_lines) - len(lines) * lh) / 2
    for i, ln in enumerate(lines):
        lw = fe.getlength(ln)
        d.text((col_r_cx - lw / 2, y0 + i * lh), ln, font=fe, fill=INK)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"): f.unlink()
    opts = [
        ("single_couplet", single_couplet),
        ("full_verse_sidebyside", full_verse_sidebyside),
    ]
    html = ["<html><body style='font-family:sans-serif;background:#fafafa;max-width:1100px;margin:auto'>",
            "<h2>Essay 0 — single line vs full verse</h2>"]
    for name, fn in opts:
        fn().save(OUT / f"{name}.png")
        html.append(f"<h3>{name.replace('_', ' ')}</h3>"
                    f"<img src='{name}.png' style='max-width:100%;border:1px solid #ddd'>")
    html.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(html))
    print(f"{len(opts)} layouts -> {OUT}")


if __name__ == "__main__":
    main()
