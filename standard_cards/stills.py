#!/usr/bin/env python3
"""stills — generic timeline→stills engine. Works for ANY text project.

Input: timeline.json — list of {"id","start","end","text"[,"text2"]}
Output: one PNG per state + index.html. White ground, hard cuts, no motion.

  python3 stills.py timeline.json --out dir [--max-chars 240] [--from 0 --to 60]
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
INK, INK50, LIGHT = (23, 20, 15), (118, 115, 110), (255, 255, 255)
FONTS = Path("/root/.fonts")
SERIF = FONTS / "CormorantGaramond[wght].ttf"
ITAL = FONTS / "CormorantGaramond-Italic[wght].ttf"
M = 140          # side margin
LH = 1.35        # line height factor


def f(size, italic=False, wght=400):
    return ImageFont.truetype(str(ITAL if italic else SERIF), size, index=0)


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


def render(state, max_chars):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    text = state["text"].strip()
    # font size: shrink to fit block
    size = 64
    while size > 32:
        ft = f(size)
        lines = wrap(text, ft, W - 2 * M)
        block_h = len(lines) * int(size * LH)
        if block_h <= H - 320 and (len(text) < max_chars or size == 32):
            break
        size -= 4
    ft = f(size)
    lh = int(size * LH)
    lines = wrap(text, ft, W - 2 * M)
    total = len(lines) * lh
    y0 = (H - total) / 2
    for i, ln in enumerate(lines):
        lw = ft.getlength(ln)
        d.text(((W - lw) / 2, y0 + i * lh), ln, font=ft, fill=INK)
    # optional second block (translation / gloss) in grey italic below
    t2 = (state.get("text2") or "").strip()
    if t2:
        ft2 = f(max(30, size - 16), italic=True)
        lh2 = int(ft2.size * LH)
        lines2 = wrap(t2, ft2, W - 2 * M - 80)
        y2 = y0 + total + 40
        for i, ln in enumerate(lines2):
            lw = ft2.getlength(ln)
            d.text(((W - lw) / 2, y2 + i * lh2), ln, font=ft2, fill=INK50)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timeline")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-chars", type=int, default=280)
    ap.add_argument("--from", dest="t0", type=float, default=0)
    ap.add_argument("--to", dest="t1", type=float, default=1e9)
    a = ap.parse_args()

    tl = json.loads(Path(a.timeline).read_text())
    rows = [r for r in tl if r["end"] > a.t0 and r["start"] < a.t1]
    rows.sort(key=lambda r: r["start"])

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"): f.unlink()

    idx_rows = []
    for i, r in enumerate(rows, 1):
        im = render(r, a.max_chars)
        fn = f"{i:03d}_{r['id']}.png"
        im.save(out / fn)
        idx_rows.append((fn, r))

    html = ["<html><body style='font-family:sans-serif;background:#fff;max-width:1100px;margin:auto'>",
            f"<h2>{a.timeline} — {len(rows)} states</h2>"]
    for fn, r in idx_rows:
        html.append(f"<h4>{r['id']} · {r['start']:.1f}–{r['end']:.1f}s</h4>"
                    f"<img src='{fn}' style='max-width:100%;border:1px solid #eee'>")
    html.append("</body></html>")
    (out / "index.html").write_text("\n".join(html))
    print(f"{len(rows)} stills -> {out}")


if __name__ == "__main__":
    main()
