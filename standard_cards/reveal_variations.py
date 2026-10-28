#!/usr/bin/env python3
"""reveal_variations — owner demo reel.

Core logic: canvas is BLACK. The verse card (white ground, black text) is
already fully present. A WHITE REGION grows to expose it. The text never
moves, fades, or draws — it was "always there"; only the light arrives.

  python3 reveal_variations.py          # -> experiments/reveal_variations.mp4
                                        #    + experiments/reveal_stills/*.png
"""
import os, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from build import (W, H, DEVA, SERIF, ITAL, VERM, verse_card, load,
                   f, wrap, para_words)

OUT = Path("/home/box/visuals/experiments")
STILLS = OUT / "reveal_stills"
SEGS = Path("/tmp/opencode/reveal_segs")
FPS = 30
REVEAL_F = 20          # 0.67s reveal
HOLD_F = 55            # 1.83s hold
BLACK = Image.new("RGB", (W, H), (0, 0, 0))


def ease(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3      # gentle ease-out; no bounce, no PowerPoint


def verse_metrics(sans, roman, eng):
    """same layout math as verse_card — needed to bound the reveal regions"""
    sd, sr, se = f(DEVA, 58), f(ITAL, 34), f(SERIF, 44, 500)
    slines = wrap(para_words([(sans, sd)]), 720)
    rlines = wrap(para_words([(roman, sr)]), 720)
    elines = wrap(para_words([(eng, se)]), 720)
    left_h = len(slines) * 82 + 20 + len(rlines) * 48
    right_h = len(elines) * 60
    mid = (200 + (H - 160)) / 2
    return mid - left_h / 2, left_h, mid - right_h / 2, right_h


def m_lr_full(p, m):
    return [(0, 0, int(W * p), H)]


def m_lr_band(p, m):
    ys, lh, ye, rh = m
    top, bot = int(min(ys, ye) - 48), int(max(ys + lh, ye + rh) + 48)
    return [(0, top, int(W * p), bot)]


def m_tb(p, m):
    return [(0, 0, W, int(H * p))]


def m_center(p, m):
    half = int(W * p / 2)
    return [(W // 2 - half, 0, W // 2 + half, H)]


def m_spine(p, m):
    # phase 1: hairline on the column rule grows from centre out (vertical)
    # phase 2: that bar widens horizontally into the full card
    if p < 0.45:
        q = p / 0.45
        h = int(H * q / 2)
        return [(952, H // 2 - h, 968, H // 2 + h)]
    q = ease((p - 0.45) / 0.55)
    half = int((W // 2) * q)
    return [(960 - half, 0, 960 + half, H)]


def m_cols(p, m):
    # left column zone first, then right column zone
    if p < 0.5:
        q = ease(p / 0.5)
        return [(80, 0, int(80 + 840 * q), H)]
    q = ease((p - 0.5) / 0.5)
    return [(80, 0, 920, H), (1000, 0, int(1000 + 840 * q), H)]


VARIATIONS = [
    ("1_fullheight_lr", "1 · full-height bar, left to right", m_lr_full),
    ("2_textband_lr",   "2 · text-band bar, left to right",   m_lr_band),
    ("3_topdown",       "3 · full-width bar, top to bottom",  m_tb),
    ("4_center_out",    "4 · opens from centre outward",      m_center),
    ("5_spine_first",   "5 · spine hairline, then opens",     m_spine),
    ("6_cols_stagger",  "6 · left column, then right column", m_cols),
]


def composite(card, rects):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for r in rects:
        d.rectangle(r, fill=255)
    return Image.composite(card, BLACK, mask)


def caption(img, text):
    d = ImageDraw.Draw(img)
    d.text((60, H - 72), text, font=f(SERIF, 26, 500), fill=VERM)


def main():
    STILLS.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(SEGS, ignore_errors=True)
    SEGS.mkdir(parents=True)

    tl, verses, kaul, hap = load()
    n = "1"
    card = verse_card(n, verses[n], verses[n], kaul[n])
    m = verse_metrics(verses[n], verses[n], kaul[n])

    seg_paths = []
    for key, label, mask_fn in VARIATIONS:
        fdir = SEGS / key
        fdir.mkdir()
        total = REVEAL_F + HOLD_F
        for i in range(total):
            p = ease(i / REVEAL_F) if i < REVEAL_F else 1.0
            img = composite(card, mask_fn(p, m))
            caption(img, label)
            img.save(f"{fdir}/{i:04d}.png")
            if i == REVEAL_F // 2:
                img.save(STILLS / f"{key}_mid.png")
            if i == total - 1:
                img.save(STILLS / f"{key}_final.png")
        seg = SEGS / f"{key}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                        "-pattern_type", "glob", "-i", str(fdir / "*.png"),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                        "-pix_fmt", "yuv420p", str(seg)], check=True)
        seg_paths.append(seg)
        print("seg", seg.name)

    concat = SEGS / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in seg_paths))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", str(OUT / "reveal_variations.mp4")],
                   check=True)
    print("reel", OUT / "reveal_variations.mp4")
    print("stills", STILLS)


if __name__ == "__main__":
    main()
