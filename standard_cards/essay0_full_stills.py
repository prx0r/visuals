#!/usr/bin/env python3
"""essay0_full_stills — full Essay 0 storyboard: 6 spine cells × 5 states.

Cell law: Q → SANSKRIT → TRANSLATION → PLAIN → BÄUMER (hard cuts).
Locked design: C-couplet (Sanskrit+IAST+hairline+English), Sanskrit anchored,
English swaps only. White ground, no motion.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/box/Documents/patala/.venv/lib/python3.13/site-packages")
from indic_transliteration import sanscript

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
DEVA = FONTS / "TiroDevanagariSanskrit-Regular.ttf"
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
OUT = Path("/home/box/visuals/outputs/essay0_full_stills")

# the six spine cells (from ESSAY0_OUTPUT.md + essay0_lock.json)
CELLS = [
    dict(id="S1", q="What is consciousness?",
         iast="caitanyamatma", sutra="Sūtra 1.1",
         translation="Consciousness is the Self.",
         plain="consciousness is the self",
         baumer="…it means universal consciousness… but this is consciousness "
                "is not something you are doing — it is something which is there."),
    dict(id="S2", q="What keeps consciousness from being realised?",
         iast="jnanambandhah", sutra="Sūtra 1.2",
         translation="Knowledge is bondage.",
         plain="knowledge is bondage",
         baumer="…they are not inherent in the soul they are superficial… "
                "it is an incomplete knowledge."),
    dict(id="S3", q="How does realisation happen?",
         iast="udyamo bhairavah", sutra="Sūtra 1.5",
         translation="Bhairava is upsurge.",
         plain="bhairava is upsurge",
         baumer="…it is not made by any human effort, it is not created by "
                "any human effort."),
    dict(id="S4", q="What does realisation do to experience?",
         iast="tritayabhokta vṛṣaḥ", sutra="Sūtra 1.11",
         translation="The enjoyer of the three states is the Lord of the Heroes.",
         plain="the enjoyer of the three states is the lord of the heroes",
         baumer="…when this heroic yogi wanders about in this world with the "
                "rays of his knowledge he purifies and fills it with supreme "
                "bliss right from hell to shiva."),
    dict(id="S5", q="What does the mind have to do with consciousness?",
         iast="cittam mantrah", sutra="Sūtra 2.1",
         translation="The mind is Mantra.",
         plain="the mind is mantra",
         baumer="…the mind of the devotee … acquires identity with the deity "
                "and thus becomes that mantra itself."),
    dict(id="S6", q="What happens after realisation?",
         iast="nartaka atma", sutra="Sūtra 3.9",
         translation="The Self is the actor.",
         plain="the self is the actor",
         baumer="…the place where the self takes delight with the intention "
                "of exhibiting the world drama is the stage."),
]


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


def to_dev(iast):
    return sanscript.transliterate(iast, sanscript.IAST, sanscript.DEVANAGARI)


def draw_sanskrit_block(d, dev, iast, y_dev=300):
    """Devanagari + snug IAST — the ANCHORED block. Same position every state."""
    fd, fi = f(DEVA, 110), f(ITAL, 46)
    ctext(d, dev, fd, y_dev)
    ctext(d, iast, fi, y_dev + 145, INK50)
    return y_dev + 145 + 75  # y after IAST block (hairline goes here)


def draw_english(d, text, y, italic=False, max_chars=260):
    """English below the hairline — the ONLY thing that swaps."""
    size = 56
    while size > 32:
        ft = f(ITAL if italic else SERIF, size, 400 if italic else 500)
        lines = wrap(text, ft, W - 400)
        if len(lines) * int(size * 1.4) <= H - y - 120:
            break
        size -= 4
    ft = f(ITAL if italic else SERIF, size, 400 if italic else 500)
    lh = int(size * 1.4)
    lines = wrap(text, ft, W - 400)
    for i, ln in enumerate(lines):
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y + i * lh), ln, font=ft, fill=INK)


def state_question(cell):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    ft = f(SERIF, 76, 500)
    lines = wrap(cell["q"], ft, W - 360)
    lh = int(76 * 1.4)
    total = len(lines) * lh
    ctext(d, "", ft, 0)  # noop
    y0 = (H - total) / 2
    for i, ln in enumerate(lines):
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y0 + i * lh), ln, font=ft, fill=INK)
    return im


def state_sanskrit_alone(cell):
    """Sanskrit appears — Devanagari + IAST at FINAL position (never moves)."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    dev = to_dev(cell["iast"])
    draw_sanskrit_block(d, dev, cell["iast"], y_dev=280)
    return im


def state_with_english(cell, en_text, italic=False):
    """Couplet: anchored Sanskrit (same pos/size as alone) + English below. No hairline."""
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    dev = to_dev(cell["iast"])
    y_hair = draw_sanskrit_block(d, dev, cell["iast"], y_dev=280)
    draw_english(d, en_text, y_hair + 60, italic=italic)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob("*.png"): p.unlink()

    html = ["<html><body style='font-family:sans-serif;background:#fafafa;max-width:1100px;margin:auto'>",
            "<h2>Essay 0 — full storyboard · 6 spine cells × 5 states</h2>",
            "<p>Cell law: Q → SANSKRIT → TRANSLATION → PLAIN → BÄUMER (hard cuts). "
            "Sanskrit anchored; English swaps only.</p>"]

    n = 0
    for cell in CELLS:
        cid = cell["id"]
        states = [
            (f"{cid}_1_question", lambda c=cell: state_question(c)),
            (f"{cid}_2_sanskrit", lambda c=cell: state_sanskrit_alone(c)),
            (f"{cid}_3_translation", lambda c=cell: state_with_english(c, c["translation"])),
            (f"{cid}_4_plain", lambda c=cell: state_with_english(c, c["plain"])),
            (f"{cid}_5_baumer", lambda c=cell: state_with_english(c, c["baumer"], italic=True)),
        ]
        html.append(f"<hr><h3>{cid} — {cell['q']}</h3>")
        for name, fn in states:
            fn().save(OUT / f"{name}.png")
            html.append(f"<h4>{name.split('_', 1)[1].replace('_', ' ')}</h4>"
                        f"<img src='{name}.png' style='max-width:100%;border:1px solid #eee'>")
            n += 1

    html.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(html))
    print(f"{n} stills ({len(CELLS)} cells × 5 states) -> {OUT}")


if __name__ == "__main__":
    main()
