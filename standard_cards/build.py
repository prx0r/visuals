#!/usr/bin/env python3
"""standard_cards — clear Sanskrit + English verse cards, on-screen only while spoken.

NORTHSTAR (locked): no animation, no transitions, no decoration beyond the type stack.
  INTRO  : Sanskrit name of the text -> romanised -> English (stacked, centered).
  VERSES : LEFT  = Sanskrit line (Tiro) above romanised line (Cormorant italic)
           RIGHT = English (Cormorant).
           The card appears exactly when Baumer's block for that verse starts, and
           holds through the paired Hareesh read; timing derived from the production
           sheet (never by eye). Hard cut between states.

  python3 standard_cards/build.py stills   # render PNGs only (qwen review these)
  python3 standard_cards/build.py render   # concat to mp4 + mux dual-reading master
"""
import json, os, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/home/box/essay-visual-engine")
from ve.glosscard import f, wrap, para_words, draw_para
from PIL import Image, ImageDraw

BAUMER = Path("/home/box/Downloads/yt/baumer")
OUT = Path("/home/box/visuals/standard_cards")
CARDS = OUT / "cards"
W, H = 1920, 1080

DEVA = "/root/.fonts/TiroDevanagariSanskrit-Regular.ttf"
SERIF = "/root/.fonts/CormorantGaramond[wght].ttf"
ITAL = "/root/.fonts/CormorantGaramond-Italic[wght].ttf"

INK, INK50, VERM, PAPER = (23, 20, 15), (118, 115, 110), (160, 43, 30), (255, 255, 255)

TITLE_DEV = "वातुलनाथसूत्राणि"
TITLE_ROM = "Vātūlanātha Sūtrāṇi"
TITLE_EN = "the thirteen sūtras"


def clean_roman(s):
    # sutra_verses.txt keeps the "|| n ||" tail and a stray space before visarga
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


def base():
    im = Image.new("RGB", (W, H), PAPER)
    return im, ImageDraw.Draw(im)


def intro_card():
    im, d = base()
    big_dev = f(DEVA, 96)
    d.text(((W - d.textlength(TITLE_DEV, font=big_dev)) / 2, 360), TITLE_DEV,
           font=big_dev, fill=INK)
    big_rom = f(ITAL, 52)
    d.text(((W - d.textlength(TITLE_ROM, font=big_rom)) / 2, 540), TITLE_ROM,
           font=big_rom, fill=INK)
    big_en = f(SERIF, 40, 500)
    d.text(((W - d.textlength(TITLE_EN, font=big_en)) / 2, 650), TITLE_EN,
           font=big_en, fill=INK50)
    d.ellipse([W / 2 - 6, 740, W / 2 + 6, 752], fill=VERM)
    return im


def verse_card(n, sans, roman, eng):
    im, d = base()
    roman = clean_roman(roman)
    eng = eng.replace("'", "\u2019")
    sd, sr, se = f(DEVA, 58), f(ITAL, 34), f(SERIF, 44, 500)
    # LEFT column: Sanskrit line, then romanised line under it. RIGHT: English.
    slines = wrap(para_words([(sans, sd)]), 720)
    rlines = wrap(para_words([(roman, sr)]), 720)
    elines = wrap(para_words([(eng, se)]), 720)
    lh_s, lh_r, lh_e = 82, 48, 60
    left_h = len(slines) * lh_s + 20 + len(rlines) * lh_r
    right_h = len(elines) * lh_e
    y0, y1 = 200, H - 160
    mid = (y0 + y1) / 2
    ys = mid - left_h / 2
    ye = mid - right_h / 2
    # left: sanskrit block then romanised block
    draw_para(d, 140, ys, [(sans, sd)], 720, lh_s)
    yr = ys + len(slines) * lh_s + 20
    draw_para(d, 140, yr, [(roman, sr)], 720, lh_r)
    # thin vertical rule + vermillion dot, the one accent
    d.line([(960, y0), (960, y1)], fill=INK50, width=1)
    d.ellipse([954, (y0 + y1) // 2 - 6, 966, (y0 + y1) // 2 + 6], fill=VERM)
    # right: english
    draw_para(d, 1040, ye, [(eng, se)], 720, lh_e)
    return im


def label_card(title, sub):
    im, d = base()
    big = f(SERIF, 72, 500)
    d.text(((W - d.textlength(title, font=big)) / 2, 470), title, font=big, fill=INK)
    sb = f(ITAL, 34)
    d.text(((W - d.textlength(sub, font=sb)) / 2, 600), sub, font=sb, fill=INK50)
    d.ellipse([W / 2 - 6, 690, W / 2 + 6, 702], fill=VERM)
    return im


def black_card():
    return Image.new("RGB", (W, H), (0, 0, 0))


def states(tl, verses, kaul, hap):
    """BLACK for every non-speech moment (bell, silence, switches, colophon).
    Verse card (white, black text) hard-cuts in when Baumer starts the verse
    and holds through the paired Hareesh read. No transitions anywhere."""
    runs = []
    cards = {}
    cur = None
    held = None  # verse card currently held across gaps (no flash on voice switch)

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
        # a pause/marker only goes black if we are NOT holding a verse card
        # across a voice-switch; the verse stays up through the paired read.
        if held is not None:
            return
        push("black", start, black_card)

    for r in tl:
        rid, k = r["id"], r["kind"]
        if k == "speech" and rid == "intro":
            held = None
            push("intro", r["start"], intro_card)
        elif k == "speech" and rid.startswith("b") and r.get("speaker") == "BAUMER":
            n = str(int(rid[1:]))
            held = f"v{n}"
            push(f"v{n}", r["start"],
                 lambda n=n: verse_card(n, verses[n], verses[n], kaul[n]))
        elif k == "speech" and rid.startswith("h") and r.get("speaker") == "HAREESH":
            # verse card already up (Baumer's) — dedupe holds it; clear the hold
            n = str(int(rid[1:]))
            push(f"v{n}", r["start"],
                 lambda n=n: verse_card(n, verses[n], verses[n], kaul[n]))
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
                    "-shortest", str(OUT / "standard_v2.mp4")], check=True)
    print("rendered", OUT / "standard_v2.mp4")


if __name__ == "__main__":
    main()
