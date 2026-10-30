#!/usr/bin/env python3
"""essay0_stills — render the Essay 0 HEAD cell as hard-cut state cards.

Reads essay0_lock.json (the locked HEAD cell) →5 states per the cell law:
  Q → SANSKRIT → TRANSLATION → PLAIN → BÄUMER
White ground, v3 type stack (Devanagari + grey IAST + English), no motion.

  python3 essay0_stills.py [--out dir]
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
DEVA = FONTS / "TiroDevanagariSanskrit-Regular.ttf"
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
LOCK = Path("/home/box/repos/shiva-sutras/custom/essay0/essay0_lock.json")

# sūtra 1.1 — caitanyamatma (IAST) → Devanagari
DEV_S1 = "चैतन्यमात्मा"
IAST_S1 = "caitanyamatma"


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


def center_lines(d, lines, ft, y0, lh, fill=INK):
    for i, ln in enumerate(lines):
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y0 + i * lh), ln, font=ft, fill=fill)


def card_question(q):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    ft = f(SERIF, 88, 500)
    lines = wrap(q, ft, W - 320)
    lh = int(88 * 1.35)
    total = len(lines) * lh
    center_lines(d, lines, ft, (H - total) / 2, lh)
    return im


def card_sanskrit(dev, iast, sutra):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    fd = f(DEVA, 140)
    fi = f(ITAL, 56)
    fs = f(SERIF, 40, 500)
    y_dev = 340
    y_iast = y_dev + 180
    y_sutra = y_iast + 90
    dw = fd.getlength(dev)
    d.text(((W - dw) / 2, y_dev), dev, font=fd, fill=INK)
    iw = fi.getlength(iast)
    d.text(((W - iw) / 2, y_iast), iast, font=fi, fill=INK50)
    sw = fs.getlength(sutra)
    d.text(((W - sw) / 2, y_sutra), sutra, font=fs, fill=INK50)
    return im


def card_text(text, attrib=None, italic=False):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    size = 72
    ft = f(ITAL if italic else SERIF, size, 500 if not italic else 400)
    lines = wrap(text, ft, W - 360)
    lh = int(size * 1.4)
    total = len(lines) * lh + (70 if attrib else 0)
    y0 = (H - total) / 2
    center_lines(d, lines, ft, y0, lh)
    if attrib:
        fa = f(SERIF, 36, 500)
        aw = fa.getlength(attrib)
        d.text(((W - aw) / 2, y0 + len(lines) * lh + 30), attrib, font=fa, fill=INK50)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/home/box/visuals/outputs/essay0_head_stills")
    a = ap.parse_args()

    lock = json.loads(LOCK.read_text())
    q = lock["master_question"]
    translation = lock["translation_T1"].split(" (")[0].strip().rstrip(".")
    if not translation.endswith("."):
        translation += "."
    plain = lock["plain"]
    baumer = ("…it means universal consciousness… but this is consciousness "
              "is not something you are doing — it is something which is there.")
    attrib_b = "Bäumer · ss3-10"
    attrib_t = "Dyczkowski · Aphorisms of Śiva"

    states = [
        ("01_question", lambda: card_question(q)),
        ("02_sanskrit", lambda: card_sanskrit(DEV_S1, IAST_S1, "Sūtra 1.1")),
        ("03_translation", lambda: card_text(translation, attrib=attrib_t)),
        ("04_plain", lambda: card_text(plain)),
        ("05_baumer", lambda: card_text(baumer, attrib=attrib_b, italic=True)),
    ]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"): f.unlink()

    html = ["<html><body style='font-family:sans-serif;background:#fff;max-width:1100px;margin:auto'>",
            "<h2>Essay 0 — HEAD · Sūtra 1.1 · caitanyamatma</h2>",
            "<p>Cell law: Q → SANSKRIT → TRANSLATION → PLAIN → BÄUMER (hard cuts)</p>"]
    for name, fn in states:
        im = fn()
        im.save(out / f"{name}.png")
        html.append(f"<h4>{name.replace('_', ' ')}</h4>"
                    f"<img src='{name}.png' style='max-width:100%;border:1px solid #eee'>")
    html.append("</body></html>")
    (out / "index.html").write_text("\n".join(html))
    print(f"{len(states)} states -> {out}")


if __name__ == "__main__":
    main()
