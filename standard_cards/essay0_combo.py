#!/usr/bin/env python3
"""essay0_combo — Sanskrit + English in ONE frame, design options."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
DEVA = FONTS / "TiroDevanagariSanskrit-Regular.ttf"
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
OUT = Path("/home/box/visuals/outputs/essay0_combo_options")

DEV = "चैतन्यमात्मा"
IAST = "caitanyamatma"
EN = "Consciousness is the Self."
ATTRIB = "Dyczkowski · Aphorisms of Śiva"
SUTRA = "Sūtra 1.1"


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


def option_stacked():
    """A — one centered column: Devanagari, IAST, Sūtra, then English + attrib."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fd, fi, fs = f(DEVA, 130), f(ITAL, 52), f(SERIF, 36, 500)
    fe, fa = f(SERIF, 56, 500), f(SERIF, 34, 500)
    y = 220
    ctext(d, DEV, fd, y);           y += 165
    ctext(d, IAST, fi, y, INK50);   y += 80
    ctext(d, SUTRA, fs, y, INK50);  y += 90
    ctext(d, EN, fe, y);            y += 90
    ctext(d, ATTRIB, fa, y, INK50)
    return im


def option_split():
    """B — vatula SPLIT: Devanagari+IAST left, English right, mirrored."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fd, fi = f(DEVA, 120), f(ITAL, 48)
    fe, fa = f(SERIF, 60, 500), f(SERIF, 34, 500)
    cx_l, cx_r = W * 0.28, W * 0.72
    y_dev = 400
    dw = fd.getlength(DEV)
    d.text((cx_l - dw / 2, y_dev), DEV, font=fd, fill=INK)
    iw = fi.getlength(IAST)
    d.text((cx_l - iw / 2, y_dev + 160), IAST, font=fi, fill=INK50)
    lines = wrap(EN, fe, 700)
    lh = int(60 * 1.4)
    y0 = y_dev + 40
    for i, ln in enumerate(lines):
        lw = fe.getlength(ln)
        d.text((cx_r - lw / 2, y0 + i * lh), ln, font=fe, fill=INK)
    aw = fa.getlength(ATTRIB)
    d.text((cx_r - aw / 2, y0 + len(lines) * lh + 20), ATTRIB, font=fa, fill=INK50)
    return im


def option_couplet():
    """C — tight dictionary couplet: Sanskrit block, hairline, English block."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fd, fi = f(DEVA, 120), f(ITAL, 48)
    fe, fa = f(SERIF, 64, 500), f(SERIF, 34, 500)
    y = 280
    ctext(d, DEV, fd, y);          y += 155
    ctext(d, IAST, fi, y, INK50);  y += 85
    # hairline rule
    rw = 300
    d.line([(W/2 - rw/2, y + 20), (W/2 + rw/2, y + 20)], fill=INK50, width=1)
    y += 60
    ctext(d, EN, fe, y);           y += 100
    ctext(d, ATTRIB, fa, y, INK50)
    return im


def option_question_small():
    """D — question small on top, Sanskrit+English together below."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fq, fd, fi = f(ITAL, 42), f(DEVA, 120), f(ITAL, 48)
    fe, fa = f(SERIF, 60, 500), f(SERIF, 34, 500)
    ctext(d, "What is consciousness?", fq, 180, INK50)
    y = 340
    ctext(d, DEV, fd, y);          y += 155
    ctext(d, IAST, fi, y, INK50);  y += 85
    ctext(d, EN, fe, y);           y += 90
    ctext(d, ATTRIB, fa, y, INK50)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"): f.unlink()
    opts = [
        ("A_stacked", option_stacked),
        ("B_split", option_split),
        ("C_couplet", option_couplet),
        ("D_question_small", option_question_small),
    ]
    html = ["<html><body style='font-family:sans-serif;background:#fafafa;max-width:1100px;margin:auto'>",
            "<h2>Essay 0 HEAD — Sanskrit + English in one frame (options)</h2>"]
    for name, fn in opts:
        fn().save(OUT / f"{name}.png")
        html.append(f"<h3>{name.replace('_', ' ')}</h3>"
                    f"<img src='{name}.png' style='max-width:100%;border:1px solid #ddd'>")
    html.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(html))
    print(f"{len(opts)} options -> {OUT}")


if __name__ == "__main__":
    main()
