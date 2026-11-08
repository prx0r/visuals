#!/usr/bin/env python3
"""essay0_analayo_stills — full Essay 0 storyboard for analayo-nibbana.

Reads build/assembly_s0_seed.json (the six Q→A units — the actual product).
Cell law: Q → VERBATIM (Pali, anchored) → PLAIN (English, swaps) → ANALAYO (audio, hold).
C-couplet design: Pali top, hairline, English below. White ground, hard cuts.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
ASM = Path("/home/box/repos/analayo-nibbana/build/assembly_s0_seed.json")
OUT = Path("/home/box/visuals/outputs/analayo_essay0_stills")


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


def state_question(q):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    size = 80
    while size > 40:
        ft = f(SERIF, size, 500)
        lines = wrap(q, ft, W - 360)
        if len(lines) * int(size * 1.4) <= H - 240:
            break
        size -= 4
    ft = f(SERIF, size, 500)
    lh = int(size * 1.4)
    lines = wrap(q, ft, W - 360)
    y0 = (H - len(lines) * lh) / 2
    for i, ln in enumerate(lines):
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y0 + i * lh), ln, font=ft, fill=INK)
    return im


def state_verbatim(text, plain=None):
    """Pali verbatim anchored top at FINAL size/pos; plain English below swaps. No hairline."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    text = " ".join(text.split())
    # always reserve the plain's space so the text NEVER resizes between states
    size = 54
    while size > 30:
        ft = f(SERIF, size, 500)
        lines = wrap(text, ft, W - 360)
        block_h = len(lines) * int(size * 1.4)
        if block_h <= H * 0.52 - 160:
            break
        size -= 2
    ft = f(SERIF, size, 500)
    lh = int(size * 1.4)
    lines = wrap(text, ft, W - 360)
    y = 160
    for ln in lines:
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y), ln, font=ft, fill=INK)
        y += lh
    if plain:
        plain = " ".join(plain.split())
        y += 50
        size2 = 46
        while size2 > 28:
            ft2 = f(ITAL, size2)
            lines2 = wrap(plain, ft2, W - 400)
            if y + len(lines2) * int(size2 * 1.4) <= H - 120:
                break
            size2 -= 2
        ft2 = f(ITAL, size2)
        lh2 = int(size2 * 1.4)
        lines2 = wrap(plain, ft2, W - 400)
        for ln in lines2:
            lw = ft2.getlength(ln)
            d.text(((W - lw) / 2, y), ln, font=ft2, fill=INK50)
            y += lh2
    return im


def main():
    asm = json.loads(ASM.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob("*.png"): p.unlink()

    # collect the six units: question + verbatim(+plain) per unit
    units = {}
    cur = None
    for it in asm:
        t = it.get("t")
        if t == "fish" and it.get("role") == "question":
            cur = it.get("unit")
            units[cur] = {"q": it["say"]}
        elif t == "verbatim" and cur:
            units[cur]["text"] = it["text"]
            units[cur]["plain"] = it.get("plain", "")

    html = ["<html><body style='font-family:sans-serif;background:#fafafa;max-width:1100px;margin:auto'>",
            "<h2>Analayo-Nibbāna — Essay 0 (seed) · 6 Q→A units</h2>",
            "<p>Cell law: Q → VERBATIM (Pali, anchored) → PLAIN (English, swaps). "
            "Hard cuts. Data: assembly_s0_seed.json</p>"]

    n = 0
    for unit in sorted(units, key=int):
        u = units[unit]
        uid = f"u{int(unit):02d}"
        states = [
            (f"{uid}_1_question", lambda u=u: state_question(u["q"])),
            (f"{uid}_2_verbatim", lambda u=u: state_verbatim(u["text"])),
            (f"{uid}_3_plain", lambda u=u: state_verbatim(u["text"], u["plain"])),
        ]
        html.append(f"<hr><h3>Unit {unit} — {u['q']}</h3>")
        for name, fn in states:
            fn().save(OUT / f"{name}.png")
            html.append(f"<h4>{name.split('_', 1)[1].replace('_', ' ')}</h4>"
                        f"<img src='{name}.png' style='max-width:100%;border:1px solid #eee'>")
            n += 1

    html.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(html))
    print(f"{n} stills ({len(units)} units × 3 states) -> {OUT}")


if __name__ == "__main__":
    main()
