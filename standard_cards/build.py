#!/usr/bin/env python3
"""standard_cards — Vatulanatha verse cards under the LOCKED 3-layer ontology.

  layer 1  BLACK   primary ground, always there, the resting state
  layer 2  WHITE   illumination ONLY — a region of light, never a "background"
  layer 3  TEXT    verse (Devanagari), romanised, English — pre-drawn in black ink,
                   final position, NEVER moves/fades/draws itself

There is no white card. Black is the frame; white is light arriving to reveal
text that was already present in the dark. Between verses = pure black.

  python3 standard_cards/build.py stills    # cards + black only (qwen/owner review)
  python3 standard_cards/build.py render    # concat to mp4 + mux dual-reading master
"""
import json, os, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/home/box/essay-visual-engine")
sys.path.insert(0, "/home/box/Documents/patala/.venv/lib/python3.13/site-packages")
from ve.glosscard import f, wrap, para_words, draw_para
from PIL import Image, ImageDraw

from indic_transliteration import sanscript
def to_dev(s): return sanscript.transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)

BAUMER = Path("/home/box/Downloads/yt/baumer")
OUT = Path("/home/box/visuals/standard_cards")
CARDS = OUT / "cards"
W, H = 1920, 1080

DEVA = "/root/.fonts/TiroDevanagariSanskrit-Regular.ttf"
SERIF = "/root/.fonts/CormorantGaramond[wght].ttf"
ITAL = "/root/.fonts/CormorantGaramond-Italic[wght].ttf"

BLACK = (0, 0, 0)
INK, INK50, VERM, LIGHT = (23, 20, 15), (118, 115, 110), (160, 43, 30), (255, 255, 255)

TITLE_ROM = "Vātūlanātha Sūtrāṇi"
TITLE_EN = "the thirteen sūtras"
PAD = 72  # breathing room of light around the text block


def clean_roman(s):
    s = re.sub(r"\s*\|\|\s*\d+\s*\|\|\s*$", "", s.strip())
    s = re.sub(r"\s+:", ":", s)
    return re.sub(r"\s+", " ", s).strip()


def load():
    tl = json.load(open(BAUMER / "build/dual_reading/production_sheet.built.json"))["timeline"]
    verses = {}
    for line in open(BAUMER / "text/sutra_verses.txt"):
        m = re.match(r"(.+?)\s*\|\|\s*(\d+)\s*\|\|", line.strip())
        if m:
            verses[m.group(2)] = clean_roman(m.group(1))
    kaul = json.load(open(BAUMER / "text/kaul_sutras_en.json"))
    hap = json.load(open(BAUMER / "build/template_13.json"))["sutra"]
    return tl, verses, kaul, hap


def ground():
    """layer 1 — the black frame."""
    return Image.new("RGB", (W, H), BLACK)


def light_region(img, box):
    """layer 2 — white light over the text block. Only where text lives."""
    ImageDraw.Draw(img).rectangle(box, fill=LIGHT)


def intro_card():
    im = ground()
    dev, rom, en = "वातुलनाथसूत्राणि", TITLE_ROM, TITLE_EN
    fd, fr, fe = f(DEVA, 96), f(ITAL, 52), f(SERIF, 40, 500)
    ys = [350, 540, 650]
    box = (W // 2 - 560, ys[0] - PAD, W // 2 + 560, ys[2] + 100 + PAD)
    light_region(im, box)                       # illuminate first
    d = ImageDraw.Draw(im)
    d.text(((W - d.textlength(dev, font=fd)) / 2, ys[0]), dev, font=fd, fill=INK)
    d.text(((W - d.textlength(rom, font=fr)) / 2, ys[1]), rom, font=fr, fill=INK)
    d.text(((W - d.textlength(en, font=fe)) / 2, ys[2]), en, font=fe, fill=INK50)
    d.ellipse([W / 2 - 6, 745, W / 2 + 6, 757], fill=VERM)
    return im


def verse_card(n, roman, eng):
    im = ground()
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
    # layer 2: light over both text blocks (union, with breathing room)
    top = int(min(ys, ye) - PAD)
    bot = int(max(ys + left_h, ye + right_h) + PAD)
    light_region(im, (90, top, W - 90, bot))
    # layer 3: text, already in place, black ink on the light
    d = ImageDraw.Draw(im)
    draw_para(d, 140, ys, [(dev, sd)], 720, lh_s)
    draw_para(d, 140, ys + len(slines) * lh_s + 20, [(roman, sr)], 720, lh_r)
    d.line([(960, top + 24), (960, bot - 24)], fill=INK50, width=1)
    d.ellipse([954, (top + bot) // 2 - 6, 966, (top + bot) // 2 + 6], fill=VERM)
    draw_para(d, 1040, ye, [(eng, se)], 720, lh_e)
    return im


def states(tl, verses, kaul, hap):
    """Verse card appears when Baumer starts the verse and holds through the
    paired Hareesh read; every other moment is pure black (layer 1 alone)."""
    runs, cards = [], {}
    cur = None
    held = None

    def push(name, start, builder):
        nonlocal cur
        if name == cur:
            return
        cur = name
        if name not in cards:
            cards[name] = builder()
            cards[name].save(CARDS / f"{name}.png")
        runs.append((name, start))

    def black(start):
        if held is not None:
            return
        push("black", start, ground)

    for r in tl:
        rid, k = r["id"], r["kind"]
        if k == "speech" and rid == "intro":
            held = None
            push("intro", r["start"], intro_card)
        elif k == "speech" and rid.startswith("b") and r.get("speaker") == "BAUMER":
            n = str(int(rid[1:]))
            held = f"v{n}"
            push(f"v{n}", r["start"], lambda n=n: verse_card(n, verses[n], kaul[n]))
        elif k == "speech" and rid.startswith("h") and r.get("speaker") == "HAREESH":
            n = str(int(rid[1:]))
            push(f"v{n}", r["start"], lambda n=n: verse_card(n, verses[n], kaul[n]))
            held = None
        else:
            black(r["start"])
    return runs


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
    CARDS.mkdir(parents=True, exist_ok=True)
    tl, verses, kaul, hap = load()
    runs = states(tl, verses, kaul, hap)
    end = tl[-1]["end"]
    durs = [(runs[i + 1][1] - t) for i, (n, t) in enumerate(runs[:-1])] + [end - runs[-1][1]]
    print(f"{len(runs)} states, total {sum(durs):.3f}s (audio {end:.3f}s)")
    for (n, t), du in zip(runs, durs):
        print(f"  {t:8.3f} +{du:7.3f}  {n}")
    if mode == "stills":
        print("stills in", CARDS)
        return
    lines = []
    for (n, _), du in zip(runs, durs):
        lines.append(f"file '{CARDS / (n + '.png')}'")
        lines.append(f"duration {du:.4f}")
    lines.append(f"file '{CARDS / (runs[-1][0] + '.png')}'")
    (OUT / "concat.txt").write_text("\n".join(lines) + "\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(OUT / "concat.txt"), "-i",
                    str(BAUMER / "build/dual_reading/vatula_full_dual_reading.mp3"),
                    "-map", "0:v", "-map", "1:a",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(OUT / "standard_v3.mp4")], check=True)
    print("rendered", OUT / "standard_v3.mp4")


if __name__ == "__main__":
    main()
