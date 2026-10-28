#!/usr/bin/env python3
"""reveal_variations — owner demo reel under the 3-layer ontology.

layer 1 BLACK ground · layer 3 TEXT pre-drawn in black ink, final position,
never moves · layer 2 WHITE light grows to illuminate it. You never leave
the black screen; the light arrives.

  python3 reveal_variations.py   # -> experiments/reveal_variations.mp4
                                 #    + experiments/reveal_stills/*.png
"""
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from build import (W, H, BLACK, INK, INK50, VERM, LIGHT, PAD, ground,
                   clean_roman, load, to_dev,
                   f, wrap, para_words, draw_para)

OUT = Path("/home/box/visuals/experiments")
STILLS = OUT / "reveal_stills"
SEGS = Path("/tmp/opencode/reveal_segs")
FPS = 30
REVEAL_F = 20          # 0.67s — light arrives
HOLD_F = 55            # 1.83s — settled


def ease(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3


def verse_layers(roman, eng):
    """Build the static layers once: (text_layer RGBA, light_box, spine_x).
    Text is drawn once and never touched again — only the light moves."""
    roman = clean_roman(roman)
    eng = eng.replace("'", "\u2019")
    dev = to_dev(roman)
    sd, sr, se = f(DEVA, 58), f(ITAL, 34), f(SERIF, 44, 500)
    slines = wrap(para_words([(dev, sd)]), 720)
    rlines = wrap(para_words([(roman, sr)]), 720)
    elines = wrap(para_words([(eng, se)]), 720)
    lh_s, lh_r, lh_e = 82, 48, 60
    left_h = len(slines) * lh_s + 20 + len(rlines) * lh_r
    right_h = len(elines) * lh_e
    mid = (220 + (H - 180)) / 2
    ys, ye = mid - left_h / 2, mid - right_h / 2
    top, bot = int(min(ys, ye) - PAD), int(max(ys + left_h, ye + right_h) + PAD)

    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    draw_para(d, 140, ys, [(dev, sd)], 720, lh_s)
    draw_para(d, 140, ys + len(slines) * lh_s + 20, [(roman, sr)], 720, lh_r)
    d.line([(960, top + 24), (960, bot - 24)], fill=INK50 + (255,), width=1)
    d.ellipse([954, (top + bot) // 2 - 6, 966, (top + bot) // 2 + 6],
              fill=VERM + (255,))
    draw_para(d, 1040, ye, [(eng, se)], 720, lh_e)
    return txt, (90, top, W - 90, bot)


DEVA = "/root/.fonts/TiroDevanagariSanskrit-Regular.ttf"
SERIF = "/root/.fonts/CormorantGaramond[wght].ttf"
ITAL = "/root/.fonts/CormorantGaramond-Italic[wght].ttf"


def frame(txt, light_box, rects, label):
    """black ground -> light rects (layer 2) -> text (layer 3, already present)."""
    im = ground()
    d = ImageDraw.Draw(im)
    for r in rects:
        d.rectangle(r, fill=LIGHT)
    im.paste(txt, (0, 0), txt)
    ImageDraw.Draw(im).text((60, H - 72), label, font=f(SERIF, 26, 500), fill=VERM)
    return im


def clip_to(box, r):
    x0, y0 = max(box[0], r[0]), max(box[1], r[1])
    x1, y1 = min(box[2], r[2]), min(box[3], r[3])
    return (x0, y0, x1, y1) if x0 < x1 and y0 < y1 else None


def lr_sweep(p, box):
    x0, y0, x1, y1 = box
    r = clip_to(box, (x0, y0, x0 + int((x1 - x0) * p), y1))
    return [r] if r else []


def lr_band(p, box):
    # light band is the box itself; only its horizontal growth moves
    return lr_sweep(p, box)


def tb_sweep(p, box):
    x0, y0, x1, y1 = box
    r = clip_to(box, (x0, y0, x1, y0 + int((y1 - y0) * p)))
    return [r] if r else []


def center_out(p, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    half = int((x1 - x0) * p / 2)
    r = clip_to(box, (cx - half, y0, cx + half, y1))
    return [r] if r else []


def spine_open(p, box):
    x0, y0, x1, y1 = box
    cx = 960
    if p < 0.45:
        q = p / 0.45
        h = int((y1 - y0) * q / 2)
        cy = (y0 + y1) // 2
        r = clip_to(box, (cx - 8, cy - h, cx + 8, cy + h))
        return [r] if r else []
    q = ease((p - 0.45) / 0.55)
    half = int((x1 - x0) * q / 2)
    r = clip_to(box, (cx - half, y0, cx + half, y1))
    return [r] if r else []


def cols_stagger(p, box):
    x0, y0, x1, y1 = box
    midx = 960
    if p < 0.5:
        q = ease(p / 0.5)
        r = clip_to(box, (x0, y0, x0 + int((midx - x0) * q), y1))
        return [r] if r else []
    q = ease((p - 0.5) / 0.5)
    r1 = clip_to(box, (x0, y0, midx, y1))
    r2 = clip_to(box, (midx, y0, midx + int((x1 - midx) * q), y1))
    return [r for r in (r1, r2) if r]


VARIATIONS = [
    ("1_lr_sweep",   "1 · light sweeps left to right",   lr_sweep),
    ("2_tb_sweep",   "2 · light sweeps top to bottom",   tb_sweep),
    ("3_center_out", "3 · light opens from centre",      center_out),
    ("4_spine_open", "4 · spine first, then opens",      spine_open),
    ("5_cols",       "5 · left column, then right",      cols_stagger),
]


def main():
    STILLS.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(SEGS, ignore_errors=True)
    SEGS.mkdir(parents=True)

    tl, verses, kaul, hap = load()
    txt, box = verse_layers(verses["1"], kaul["1"])

    seg_paths = []
    for key, label, mask_fn in VARIATIONS:
        fdir = SEGS / key
        fdir.mkdir()
        total = REVEAL_F + HOLD_F
        for i in range(total):
            p = ease(i / REVEAL_F) if i < REVEAL_F else 1.0
            img = frame(txt, box, mask_fn(p, box), label)
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


if __name__ == "__main__":
    main()
