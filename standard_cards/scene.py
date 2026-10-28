#!/usr/bin/env python3
"""scene — object-based renderer for the Vatulanatha screen (CANONICAL).

Replaces card baking. Every line is its own OBJECT with an independent time
window matched programmatically to the audio (production sheet; cue evidence
where available). The renderer composes per t:

  layer 1  BLACK ground
  layer 2  per-object WHITE light, grown left->right over ~0.67s from t_on
  layer 3  that object's text, static, drawn only inside its own window

Objects never overlap in time at the same slot (english swaps A->B across the
voice switch), so light never leaks onto uninvited text.

  python3 scene.py dump      # object table + matched windows -> experiments/scene_objects.json
  python3 scene.py stills    # sample frames -> experiments/scene/
  python3 scene.py render    # full mp4 muxed with the dual-reading master
"""
import json, math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import build
from build import (W, H, BLACK, INK, INK50, VERM, LIGHT, DEVA, SERIF, ITAL,
                   clean_roman, load, to_dev, ground,
                   f, wrap, para_words, draw_para)

OUT = Path("/home/box/visuals/standard_cards")
EXP = Path("/home/box/visuals/experiments")
FRAMES = Path("/tmp/opencode/scene_frames")
FPS = 30
REVEAL = 0.67
AUDIO = build.BAUMER / "build/dual_reading/vatula_full_dual_reading.mp3"

X_L, X_R, COLW = 140, 1040, 720
Y_L, Y_R = 430, 470
LH_S, LH_R, LH_E = 82, 48, 60
RULE_X0, RULE_X1, RULE_Y0, RULE_Y1 = 946, 974, 250, 830

# Per-verse timing overrides, evidence-backed (cues.json inside the b window).
# v1: cue at +16.0 "my translation by the mode of great intensity one attains"
#     = her English read begins (cues +1/+10 are Sanskrit + announcement).
OVERRIDES = {
    "1": {"eng_a_on_offset": 16.0},
}
DEFAULT_ENG_ON_OFFSET = 1.0


def ease(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3


def block(x, y, text, font, lh, pad=14):
    """wrapped token-lines + light rect for one text object"""
    lines = wrap(para_words([(text, font)]), COLW)
    maxw = max((sum(ft.getlength(tok) for tok, ft in ln) for ln in lines),
               default=0)
    rect = (x - 24, y - pad, int(x + maxw) + 24, y + lh * len(lines) - pad)
    return lines, rect


class Obj:
    def __init__(self, oid, kind, text, font, x, y, lh, t_on, t_off,
                 source, lines=None, rect=None):
        self.id, self.kind, self.text = oid, kind, text
        self.font, self.x, self.y, self.lh = font, x, y, lh
        self.t_on, self.t_off, self.source = t_on, t_off, source
        self.lines = lines if lines is not None else []
        self.rect = rect

    def draw(self, d, p):
        """text layer: static; p = light progress (gates rule/dot to lit frames)"""
        if self.kind == "rule":
            x0 = self.rect[0] + int((self.rect[2] - self.rect[0]) * p)
            if x0 >= 966:           # light has reached the spine content
                d.line([(960, RULE_Y0 + 24), (960, RULE_Y1 - 24)], fill=INK50, width=1)
                cy = (RULE_Y0 + RULE_Y1) // 2
                d.ellipse([954, cy - 6, 966, cy + 6], fill=VERM)
            return
        if self.kind == "dot":
            x0 = self.rect[0] + int((self.rect[2] - self.rect[0]) * p)
            if x0 >= self.rect[2] - 14:
                d.ellipse([954, 745, 966, 757], fill=VERM)
            return
        for i, ln in enumerate(self.lines):
            cx = self.x
            for tok, ft in ln:
                d.text((cx, self.y + i * self.lh), tok, font=ft, fill=INK)
                cx += ft.getlength(tok)

    def to_json(self):
        return dict(id=self.id, kind=self.kind, text=self.text,
                    t_on=round(self.t_on, 3), t_off=round(self.t_off, 3),
                    light_rect=list(self.rect), source=self.source)


def build_objects():
    tl, verses, kaul, hap = load()
    objs = []
    row = {r["id"]: r for r in tl}

    # ---- intro: three stacked title objects, staggered line by line
    ir = row["intro"]
    dev, rom, en = "वातुलनाथसूत्राणि", build.TITLE_ROM, build.TITLE_EN
    for i, (oid, txt, font, size, dy) in enumerate([
        ("intro.dev", dev, f(DEVA, 96), 96, 350),
        ("intro.rom", rom, f(ITAL, 52), 52, 540),
        ("intro.en", en, f(SERIF, 40, 500), 40, 650),
    ]):
        w = font.getlength(txt)
        rect = (W / 2 - w / 2 - 24, dy - 18, W / 2 + w / 2 + 24, dy + size + 20)
        objs.append(Obj(oid, "text", txt, font, W / 2 - w / 2, dy, size,
                        ir["start"] + i * 0.6, ir["end"],
                        f"sheet intro.start={ir['start']} +{i*0.6} stagger",
                        lines=[[(txt, font)]], rect=rect))
    objs.append(Obj("intro.dot", "dot", None, None, 0, 0, 0,
                    ir["start"] + 2.4, ir["end"],
                    f"sheet intro.start={ir['start']} +2.4 (signature dot)",
                    rect=(940, 731, 980, 771)))

    # ---- verses: rule, sanskrit, romanised, english(Baumer/Kaul), english(Hareesh)
    for n in range(1, 14):
        k = f"{n:02d}"
        b, h = row[f"b{k}"], row[f"h{k}"]
        roman = clean_roman(verses[str(n)])
        dev, kaul_en, h_en = to_dev(roman), kaul[str(n)], hap[str(n)]["hareesh_spoken"]
        ov = OVERRIDES.get(str(n), {})
        base = b["start"]
        src = f"sheet b{k}.start={base:.3f}"

        rule = Obj(f"v{n}.rule", "rule", None, None, 0, 0, 0,
                   base + 0.15, h["end"], f"{src} +0.15",
                   rect=(RULE_X0, RULE_Y0, RULE_X1, RULE_Y1))
        sd, sr, se = f(DEVA, 58), f(ITAL, 34), f(SERIF, 44, 500)

        l1, r1 = block(X_L, Y_L, dev, sd, LH_S)
        l2, r2 = block(X_L, Y_L + LH_S * len(l1) + 24, roman, sr, LH_R)
        eng_on = base + ov.get("eng_a_on_offset", DEFAULT_ENG_ON_OFFSET)
        l3, r3 = block(X_R, Y_R, kaul_en, se, LH_E)
        l4, r4 = block(X_R, Y_R, h_en, se, LH_E)

        objs += [
            rule,
            Obj(f"v{n}.dev", "text", dev, sd, X_L, Y_L, LH_S,
                base, h["end"], f"{src} (sanskrit at her onset)",
                lines=l1, rect=r1),
            Obj(f"v{n}.rom", "text", roman, sr, X_L, Y_L + LH_S * len(l1) + 24, LH_R,
                base + 0.5, h["end"], f"{src} +0.5 stagger",
                lines=l2, rect=r2),
            Obj(f"v{n}.eng_a", "text", kaul_en, se, X_R, Y_R, LH_E,
                eng_on, b["end"],
                (f"{src} +{ov['eng_a_on_offset']:.1f} cue-matched"
                 if "eng_a_on_offset" in ov else f"{src} +{DEFAULT_ENG_ON_OFFSET} default")
                + " until her voice stops",
                lines=l3, rect=r3),
            Obj(f"v{n}.eng_b", "text", h_en, se, X_R, Y_R, LH_E,
                h["start"], h["end"], f"sheet h{k}.start={h['start']:.3f} (his render)",
                lines=l4, rect=r4),
        ]
    return objs, tl


def frame_at(objs, t):
    im = ground()
    d = ImageDraw.Draw(im)
    for o in objs:
        if not (o.t_on <= t < o.t_off):
            continue
        p = 1.0 if t >= o.t_on + REVEAL else ease((t - o.t_on) / REVEAL)
        x0, y0, x1, y1 = o.rect
        d.rectangle([x0, y0, x0 + max(1, int((x1 - x0) * p)), y1], fill=LIGHT)
        o.draw(d, p)
    return im


def cmd_dump():
    objs, tl = build_objects()
    data = [o.to_json() for o in objs]
    EXP.mkdir(exist_ok=True)
    (EXP / "scene_objects.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    for o in objs:
        print(f"{o.t_on:8.3f} -> {o.t_off:8.3f}  {o.id:<14} {o.source}")
    print(f"\n{len(objs)} objects -> experiments/scene_objects.json")


def cmd_stills():
    objs, tl = build_objects()
    d = EXP / "scene"
    d.mkdir(parents=True, exist_ok=True)
    row = {r["id"]: r for r in tl}
    samples = {
        "00_black": 5.0,
        "01_intro_reveal": row["intro"]["start"] + 0.9,
        "02_intro_held": row["intro"]["start"] + 4.0,
        "03_v1_mid_reveal": row["b01"]["start"] + 0.33,
        "04_v1_held": row["b01"]["start"] + 3.0,
        "05_v1_switch_air": (row["h01"]["start"] + row["b01"]["end"]) / 2,
        "06_v1_hareesh_en": row["h01"]["start"] + 1.2,
        "07_gap_black": row["b02"]["start"] - 1.5,
    }
    for name, t in samples.items():
        frame_at(objs, t).save(d / f"{name}.png")
        print("still", name, f"t={t:.2f}")
    print("in", d)


def cmd_render():
    objs, tl = build_objects()
    dur = tl[-1]["end"]
    events = {0.0, dur}
    for o in objs:
        events.update([o.t_on, min(o.t_on + REVEAL, o.t_off), o.t_off])
    ev = sorted(t for t in events if 0 <= t <= dur)
    uniq = [ev[0]]
    for t in ev[1:]:
        if t - uniq[-1] > 1e-3:
            uniq.append(t)

    shutil_rm = __import__("shutil").rmtree
    shutil_rm(FRAMES, ignore_errors=True)
    FRAMES.mkdir(parents=True)
    entries, idx, n_anim, n_stat = [], 0, 0, 0
    for t0, t1 in zip(uniq, uniq[1:]):
        animated = any(o.t_on < t1 and o.t_on + REVEAL > t0 and o.t_off > t0
                       for o in objs)
        if animated:
            t = t0
            while t < t1 - 1e-6:
                frame_at(objs, t).save(FRAMES / f"{idx:06d}.png")
                entries.append((idx, min(1.0 / FPS, t1 - t)))
                idx, n_anim, t = idx + 1, n_anim + 1, t + 1.0 / FPS
        else:
            frame_at(objs, (t0 + t1) / 2).save(FRAMES / f"{idx:06d}.png")
            entries.append((idx, t1 - t0))
            idx, n_stat = idx + 1, n_stat + 1

    lines = []
    for i, du in entries:
        lines.append(f"file '{FRAMES / f'{i:06d}.png'}'")
        lines.append(f"duration {du:.4f}")
    lines.append(f"file '{FRAMES / f'{entries[-1][0]:06d}.png'}'")
    (FRAMES / "concat.txt").write_text("\n".join(lines) + "\n")
    out = OUT / "scene_v1.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(FRAMES / "concat.txt"), "-i", str(AUDIO),
                    "-map", "0:v", "-map", "1:a",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(out)], check=True)
    print(f"{len(objs)} objects · {n_anim} anim + {n_stat} static frames")
    print("rendered", out)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "dump"
    {"dump": cmd_dump, "stills": cmd_stills, "render": cmd_render}[mode]()
