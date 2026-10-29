#!/usr/bin/env python3
"""scene — Vatulanatha screen renderer (CANONICAL, v4 type-first layout).

Owner spec (2026-10-29, supersedes all earlier visual experiments):
  ground    PAPER WHITE always — every frame, silence included
  text      Devanagari = ink black; romanised = grey under each akshara part;
            English = ink black (Kaul 1923 during Baumer, Hareesh during his)
  layout    TYPE FILLS THE FRAME (autofit to region):
              short/medium verse -> CENTRED verse, English below
              long verse         -> full verse LEFT, full English RIGHT
  motion    NONE — objects hard-cut in at their audio window. Since nothing
            animates, DESIGN REVIEW IS STILLS: `storyboard` mode screenshots
            every state. Full renders only on explicit owner approval
            (root AGENTS.md mistakes log: dev ceiling = stills + <=20s clip).

  python3 scene.py frame [vN|t]   # ONE frame (design-iteration unit) -> outputs/scene_frame.png
  python3 scene.py dump        # object table -> experiments/scene_objects.json
  python3 scene.py stills      # quick samples -> outputs/scene_v4_stills/
  python3 scene.py storyboard  # EVERY state -> outputs/storyboard/  (only AFTER design lock)
  python3 scene.py render      # full mp4 (ONLY after owner approval)
"""
import json, math, os, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import build
from build import (W, H, BLACK, INK, INK50, VERM, LIGHT, DEVA, SERIF, ITAL,
                   clean_roman, load, to_dev, to_iast, aksharas, ground,
                   f, wrap, para_words, draw_para)

OUT = Path(os.environ.get("OUT", "/home/box/visuals/standard_cards"))
EXP = Path(os.environ.get("EXP", "/home/box/visuals/experiments"))
FRAMES = Path(os.environ.get("FRAMES", "/tmp/opencode/scene_frames"))
FPS = 30
AUDIO = build.BAUMER / "build/dual_reading/vatula_full_dual_reading.mp3"

M = 100                              # page margin
CENTER_VW, CENTER_VH = 1740, 460     # centred verse region (stack must fit)
CENTER_EW, CENTER_EH = 1300, 280     # centred english region
LEFT_VW, RIGHT_EW = 810, 810         # mirrored containers: 100..910 | 1010..1820, axis 960
COL_H = 900                          # split column height

# English cue evidence (cues.json inside her b window)
OVERRIDES = {"1": {"eng_a_on_offset": 16.0}}
DEFAULT_ENG_ON_OFFSET = 1.0


# ---------------------------------------------------------------- layout ----
def flow_aksharas(roman, s, maxw):
    """Flow akshara parts at display size s, wrapping inside/between words.
    slot = (dev_part, iast_part, dev_w, iast_w, slot_w, gap_after, word_id).
    word_id tags which parts belong to the same word.
    GRID layout: parts flow with near-zero gap (continuous Devanagari, as
    written) and each romanised syllable sits tight under its own akshara."""
    fd, fr = f(DEVA, s), f(ITAL, max(20, round(s * 0.40)))   # rom visibly smaller
    gap_p, gap_w = s * 0.04, s * 0.42   # continuous within word; space = word break
    words = roman.split()
    lines, cur, x, lw = [], [], 0.0, 0.0
    widths = []

    def flush_line():
        nonlocal cur, x, lw
        widths.append(lw)
        lines.append(cur)
        cur, x, lw = [], 0.0, 0.0

    wid = 0
    for w in words:
        parts = aksharas(to_dev(w))
        # whole-word width (internal gaps) — wrap BEFORE the word if it won't
        # fit the current line; only break inside a word when it cannot fit any line
        ww = 0.0
        for pi, p in enumerate(parts):
            ww += fd.getlength(p)                       # dev governs the grid
            if pi < len(parts) - 1:
                ww += gap_p
        if cur and x + ww > maxw and ww <= maxw:
            flush_line()
        for pi, p in enumerate(parts):
            ia = to_iast(p)
            dw, iw = fd.getlength(p), fr.getlength(ia)
            sw = max(dw, iw)
            g = gap_p if pi < len(parts) - 1 else gap_w
            if cur and x + dw > maxw:
                flush_line()
            cur.append((p, ia, dw, iw, sw, g, wid))
            x += dw + g                        # advance by DEVANAGARI width (exact grid)
            lw = x
        wid += 1
    if cur:
        widths.append(lw)
        lines.append(cur)
    dev_lh, rom_lh = int(s * 1.3), int(s * 0.62)   # tight grid rows
    return dict(lines=lines, widths=widths, dev_lh=dev_lh, rom_lh=rom_lh,
                rom_top=int(s * 1.12),              # IAST snug under the glyphs
                fd=fd, fr=fr, height=len(lines) * (dev_lh + rom_lh))


def autofit_verse(roman, maxw, maxh, lo=36, hi=175):
    """Largest display size whose flowed block fits the region."""
    for s in range(hi, lo - 1, -2):
        fl = flow_aksharas(roman, s, maxw)
        if fl["lines"] and fl["height"] <= maxh and max(fl["widths"]) <= maxw:
            return s, fl
    return None


def autofit_para(text, maxw, maxh, lo=30, hi=96):
    for s in range(hi, lo - 1, -2):
        ft = f(SERIF, s, 500)
        lns = wrap(para_words([(text, ft)]), maxw)
        if not lns:
            continue
        lh = int(s * 1.35)
        h = len(lns) * lh
        w = max(sum(ft.getlength(t) for t, _ in ln) for ln in lns)
        if h <= maxh and w <= maxw:
            return s, lns, lh, ft
    return None


# ---- fill mode (qwen judge: "fill the canvas to ~100px margins") -----------
BAND_Y, BAND_H = 100, 880          # both columns occupy exactly y 100..980

# ---- typographic scale (Vignelli Canon + φ modular scale, 2026-10-29) -----
# display : secondary = 72 : 36 (=2×, Vignelli "contrast comes from scale");
# english body 44 (φ-ish step from 36); measure ≤ ~60 chars (BBC GEL).
# Alignment = CENTRED — Vignelli: "centered for lapidary text, rhetorical
# composition"; a sūtra is exactly that. Type size is a function of the
# COLUMN, not a fill-the-band stretch.
S_DEV, S_ROM, S_EN = 72, 36, 44
LH_EN, GAP_PHRASE = 58, 40
ROW_GAP = int(S_DEV * 0.20)         # air between verse rows (compressed)


def fill_fl(roman, maxw, budget=BAND_H):
    """Largest verse size that fits the column; leading then STRETCHED so the
    block fills the band exactly (extra air goes BETWEEN dev+romanised pairs)."""
    best = None
    for s in range(175, 35, -1):
        fl = flow_aksharas(roman, s, maxw)
        if fl["lines"] and fl["height"] <= budget:
            best = (s, fl)
            break
    if not best:
        return None
    s, fl = best
    fl["pitch"] = budget / len(fl["lines"])
    return s, fl


def fill_para(text, maxw, budget=BAND_H, lo=30, hi=96):
    """Largest english size that fits; line-leading stretched to fill the band."""
    for s in range(hi, lo - 1, -1):
        ft = f(SERIF, s, 500)
        lns = wrap(para_words([(text, ft)]), maxw)
        if not lns:
            continue
        if len(lns) * int(s * 1.35) <= budget:
            return s, lns, budget // len(lns), ft
    return None


def split_phrases(text):
    """English chunks at commas/semicolons/colons — the correspondence units."""
    parts = re.split(r"(?<=[,;:])\s+", text.strip())
    return [p for p in parts if p]


def fill_eng_phrases(text, maxw, gap=56, band=BAND_H, lo=28, hi=96):
    """DEAD — superseded by eng_block (fixed φ scale, centred). Kept for ref."""
    return None


def verse_block(roman, maxw):
    """Fixed display scale72; lines centred per line (centre passed at draw);
    block vertically centred in the band. Returns (fl, line_widths, pitch, vy)."""
    fl = flow_aksharas(roman, S_DEV, maxw)
    pitch = fl["dev_lh"] + fl["rom_lh"] + ROW_GAP
    lws = [sum(sl[2] + sl[5] for sl in ln) - ln[-1][5] for ln in fl["lines"]]
    total_h = len(fl["lines"]) * pitch - ROW_GAP
    return fl, lws, pitch, (BAND_Y + (BAND_H - total_h) / 2)


def eng_block(text, maxw, y0=None):
    """Fixed size 44/lh62, phrases in order with subtle gap; lines centred
    (cx stored on the object). Block vertically centred in band unless y0 given.
    Returns ([(phrase, y, lines)], lh, ft)."""
    ph = split_phrases(text)
    ft = f(SERIF, S_EN, 500)
    blocks = [wrap(para_words([(t, ft)]), maxw) for t in ph]
    total = sum(len(b) for b in blocks) * LH_EN + GAP_PHRASE * (len(ph) - 1)
    if y0 is None:
        y0 = BAND_Y + (BAND_H - total) / 2
    out, y = [], y0
    for t, b in zip(ph, blocks):
        out.append((t, y, b))
        y += len(b) * LH_EN + GAP_PHRASE
    return out, LH_EN, ft


# ---------------------------------------------------------------- objects ---
class Obj:
    def __init__(self, oid, kind, text, x, y, t_on, t_off, source,
                 fill=INK, **kw):
        self.id, self.kind, self.text, self.fill = oid, kind, text, fill
        self.x, self.y, self.t_on, self.t_off, self.source = x, y, t_on, t_off, source
        self.__dict__.update(kw)
        self.cx = getattr(self, "cx", None)     # line-centre for centred text
        self.lw = getattr(self, "lw", 0.0)      # pairline: this line's width

    def draw(self, d):
        if self.kind == "axis":
            # mirror axis: hairline + vermillion dot between the containers
            d.line([(960, self.y0 + 24), (960, self.y1 - 24)], fill=INK50, width=1)
            cy = (self.y0 + self.y1) // 2
            d.ellipse([954, cy - 6, 966, cy + 6], fill=VERM)
            return
        if self.kind == "pairline":
            # centred line: block starts at cx - line_width/2 (lapidary centre)
            sx = self.x - self.lw / 2
            slots = self.slots
            i = 0
            while i < len(slots):
                wid = slots[i][6]
                j = i
                while j + 1 < len(slots) and slots[j + 1][6] == wid:
                    j += 1
                group = slots[i:j + 1]
                dev_text = "".join(g0[0] for g0 in group)
                d.text((sx, self.y), dev_text, font=self.fd, fill=INK)
                ox = sx
                for (ptxt, ia, dw, iw, sw, g, _wid) in group:
                    rx = ox + (dw - iw) / 2      # centred on the akshara's own span
                    d.text((rx, self.y + self.rom_top), ia, font=self.fr, fill=INK50)
                    ox += dw + g
                sx = ox
                i = j + 1
            return
        # text lines (centred when cx set)
        for i, ln in enumerate(self.lines):
            if self.cx is not None:                # centred line
                lw_ = sum(ft.getlength(tok) for tok, ft in ln)
                base = self.cx - lw_ / 2
            else:
                base = self.x
            cx = base
            for tok, ft in ln:
                d.text((cx, self.y + i * self.lh), tok, font=ft, fill=self.fill)
                cx += ft.getlength(tok)

    def to_json(self):
        return dict(id=self.id, kind=self.kind, text=self.text,
                    t_on=round(self.t_on, 3), t_off=round(self.t_off, 3),
                    source=self.source)


def build_objects():
    tl, verses, kaul, hap = load()
    objs, row = [], {r["id"]: r for r in tl}

    # ---- intro: title stack, autofit big, all present from her first word
    ir = row["intro"]
    dev, rom, en = "वातुलनाथसूत्राणि", build.TITLE_ROM, build.TITLE_EN
    fdv = f(DEVA, 170)
    while fdv.getlength(dev) > 1720 and fdv.size > 80:
        fdv = f(DEVA, fdv.size - 4)
    sd = fdv.size
    fr_, fe = f(ITAL, int(sd * 0.40)), f(SERIF, int(sd * 0.27), 500)
    y_dev = 300
    y_rom = y_dev + int(sd * 1.45) + 30
    y_en = y_rom + int(sd * 0.40 * 1.5) + 24
    objs += [
        Obj("intro.dev", "text", dev, (W - fdv.getlength(dev)) / 2, y_dev,
            ir["start"], ir["end"], "sheet intro (instant)",
            lines=[[(dev, fdv)]], lh=sd, fill=INK),
        Obj("intro.rom", "text", rom, (W - fr_.getlength(rom)) / 2, y_rom,
            ir["start"], ir["end"], "sheet intro (instant)",
            lines=[[(rom, fr_)]], lh=int(sd * 0.4), fill=INK50),
        Obj("intro.en", "text", en, (W - fe.getlength(en)) / 2, y_en,
            ir["start"], ir["end"], "sheet intro (instant)",
            lines=[[(en, fe)]], lh=int(sd * 0.27), fill=INK50),
    ]

    # ---- verses: autofit, CENTRED (short) or SPLIT L/R (long)
    for n in range(1, 14):
        k = f"{n:02d}"
        b, h = row[f"b{k}"], row[f"h{k}"]
        roman = clean_roman(verses[str(n)])
        kaul_en, h_en = kaul[str(n)], hap[str(n)]["hareesh_spoken"]
        ov = OVERRIDES.get(str(n), {})
        base, src = b["start"], f"sheet b{k}.start={b['start']:.3f}"
        eng_on = base + ov.get("eng_a_on_offset", DEFAULT_ENG_ON_OFFSET)

        # typographic decision (fixed φ scale): short verse (fits one line,
        # ≤15 syllable units) => stacked centre, english below; longer verse =>
        # mirrored split columns, lines centred within each column.
        probe = flow_aksharas(roman, S_DEV, CENTER_VW)
        centred = (len(probe["lines"]) == 1
                   and sum(len(ln) for ln in probe["lines"]) <= 15)

        if centred:
            fl = probe
            pitch = fl["dev_lh"] + fl["rom_lh"] + ROW_GAP
            verse_h = len(fl["lines"]) * pitch - ROW_GAP
            _ft = f(SERIF, S_EN, 500)
            _blocks = [wrap(para_words([(t, _ft)]), CENTER_EW)
                       for t in split_phrases(kaul_en)]
            eng_h = (sum(len(b) for b in _blocks) * LH_EN
                     + GAP_PHRASE * max(0, len(_blocks) - 1))
            total_h = verse_h + 70 + eng_h
            vy = (H - total_h) / 2           # whole composition optically centred
            bx = W / 2
            ey_base = vy + verse_h + 70
            layout = f"{src} STACKED s={S_DEV}"
        else:
            fl, lws, pitch, vy = verse_block(roman, LEFT_VW)
            bx = M + LEFT_VW / 2
            ey_base = None                        # eng_block centres in band
            layout = f"{src} SPLIT s={S_DEV} centred-lines"

        lws = [sum(sl[2] + sl[5] for sl in ln) - ln[-1][5] for ln in fl["lines"]]
        for i, line in enumerate(fl["lines"]):
            objs.append(Obj(f"v{n}.l{i+1}", "pairline",
                            f"{roman} line {i+1}", bx, vy + i * pitch,
                            base, h["end"], layout,
                            slots=line, fd=fl["fd"], fr=fl["fr"],
                            dev_lh=fl["dev_lh"], rom_top=fl["rom_top"], lw=lws[i]))

        def emit_eng(tag, text, ton, toff, note):
            """english: fixed 44/lh62, lines centred, block below (stacked) or
            band-centred (split); phrase gaps = order correspondence."""
            maxw = CENTER_EW if centred else RIGHT_EW
            cx = W / 2 if centred else (W - M - RIGHT_EW / 2)
            phs, lh, ft = eng_block(text, maxw, y0=ey_base)
            for j, (t, py, lns) in enumerate(phs):
                oid = f"v{n}.{tag}" + (f".p{j+1}" if len(phs) > 1 else "")
                objs.append(Obj(oid, "text", t, cx, py, ton, toff,
                                f"{layout} {note} es={S_EN}",
                                lines=lns, lh=lh, fill=INK, cx=cx))

        emit_eng("eng_a", kaul_en, eng_on, b["end"],
                 "kaul 1923 until her voice stops")
        emit_eng("eng_b", h_en, h["start"], h["end"],
                 f"hareesh rendering (sheet h{k}.start)")
    return objs, tl


def frame_at(objs, t):
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    for o in objs:
        if o.t_on <= t < o.t_off:
            o.draw(d)
    return im


# ---------------------------------------------------------------- commands --
def cmd_dump():
    objs, tl = build_objects()
    EXP.mkdir(exist_ok=True)
    (EXP / "scene_objects.json").write_text(
        json.dumps([o.to_json() for o in objs], indent=1, ensure_ascii=False))
    for o in objs:
        print(f"{o.t_on:8.3f} -> {o.t_off:8.3f}  {o.id:<14} {o.source}")
    print(f"\n{len(objs)} objects -> experiments/scene_objects.json")


def cmd_stills():
    objs, tl = build_objects()
    d = Path("/home/box/visuals/outputs/scene_v4_stills")
    d.mkdir(parents=True, exist_ok=True)
    row = {r["id"]: r for r in tl}
    scene_t = [("intro", 13.5)]
    for n in (1, 3, 8, 11):
        k = f"{n:02d}"
        scene_t.append((f"v{n}", row[f"b{k}"]["start"] + 3))
    for name, t in scene_t:
        frame_at(objs, t).save(d / f"{name}.png")
    print("stills in", d)


def cmd_storyboard():
    """Screenshot EVERY distinct state — this replaces video for design review."""
    objs, tl = build_objects()
    d = Path("/home/box/visuals/outputs/storyboard")
    d.mkdir(parents=True, exist_ok=True)
    row = {r["id"]: r for r in tl}
    shots = [(1, "intro", 13.5), (2, "silence_before_v1", row["b01"]["start"] - 1.0)]
    idx = 3
    for n in range(1, 14):
        k = f"{n:02d}"
        b, h = row[f"b{k}"], row[f"h{k}"]
        shots.append((idx, f"v{n:02d}_verse", b["start"] + 1.2)); idx += 1
        # english-on shot (kaul) if it starts materially later than the verse
        ov = OVERRIDES.get(str(n), {})
        eng_on = b["start"] + ov.get("eng_a_on_offset", DEFAULT_ENG_ON_OFFSET)
        if eng_on > b["start"] + 2.0 and eng_on + 1 < b["end"]:
            shots.append((idx, f"v{n:02d}_english", eng_on + 1.0)); idx += 1
        # hareesh segment shot
        if h["start"] + 1 < h["end"]:
            shots.append((idx, f"v{n:02d}_hareesh", h["start"] + 1.0)); idx += 1
        # the white gap after this verse
        nxt = row[f"b{n+1:02d}"]["start"] if n < 13 else row["colo"]["start"]
        shots.append((idx, f"v{n:02d}_gap", (h["end"] + nxt) / 2)); idx += 1
    shots.append((idx, "colophon_white", row["colo"]["start"] + 5))
    for i, name, t in shots:
        frame_at(objs, t).save(d / f"{i:02d}_{name}.png")
    print(f"{len(shots)} storyboard frames -> {d}")


def cmd_render():
    objs, tl = build_objects()
    dur = tl[-1]["end"]
    events = {0.0, dur}
    for o in objs:
        events.update([o.t_on, o.t_off])
    ev = sorted(t for t in events if 0 <= t <= dur)
    uniq = [ev[0]]
    for t in ev[1:]:
        if t - uniq[-1] > 1e-3:
            uniq.append(t)
    import shutil
    shutil.rmtree(FRAMES, ignore_errors=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    entries, idx = [], 0
    for t0, t1 in zip(uniq, uniq[1:]):
        frame_at(objs, (t0 + t1) / 2).save(FRAMES / f"{idx:06d}.png")
        entries.append((idx, t1 - t0))
        idx += 1
    lines = []
    for i, du in entries:
        lines.append(f"file '{FRAMES / f'{i:06d}.png'}'")
        lines.append(f"duration {du:.4f}")
    lines.append(f"file '{FRAMES / f'{entries[-1][0]:06d}.png'}'")
    (FRAMES / "concat.txt").write_text("\n".join(lines) + "\n")
    out = OUT / "scene_v4.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(FRAMES / "concat.txt"), "-i", str(AUDIO),
                    "-map", "0:v", "-map", "1:a",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
                    "-threads", "2", "-movflags", "+faststart",
                    "-shortest", str(out)], check=True)
    print("rendered", out)


def cmd_frame(argv):
    """ONE representative frame — the design-iteration unit (AGENTS.md
    mistakes log: never bulk-render while iterating). Default target = the
    hardest layout case (longest verse, split mode).
      python3 scene.py frame            # v8 (split mode) -> outputs/scene_frame.png
      python3 scene.py frame v3         # a named verse
      python3 scene.py frame 99.5       # a timestamp in seconds
    """
    objs, tl = build_objects()
    row = {r["id"]: r for r in tl}
    target = argv[0] if argv else "v8"
    out = Path("/home/box/visuals/outputs/scene_frame.png")
    if re.fullmatch(r"\d+(\.\d+)?", target):
        t = float(target)
        frame_at(objs, t).save(out)
        print(f"frame t={t} -> {out}")
        return
    m = re.fullmatch(r"v(\d+)", target)
    if not m:
        print(f"unknown target {target!r} — use vN, a number, or nothing")
        return
    n = int(m.group(1))
    b = row[f"b{n:02d}"]
    frame_at(objs, b["start"] + 3.0).save(out)
    print(f"frame {target} (b start+3) -> {out}")


def cmd_clip(argv):
    """Owner-requested time-range render (static-state encode — one frame per
    state, so minutes cost the same as seconds).
      python3 scene.py clip               # 0..60 -> outputs/clip_0-60.mp4
      python3 scene.py clip 60 120
    """
    s = float(argv[0]) if argv else 0.0
    e = float(argv[1]) if len(argv) > 1 else 60.0
    objs, tl = build_objects()
    e = min(e, tl[-1]["end"])
    events = {s, e}
    for o in objs:
        events.update([t for t in (o.t_on, o.t_off) if s < t < e])
    ev = sorted(events)
    uniq = [ev[0]]
    for t in ev[1:]:
        if t - uniq[-1] > 1e-3:
            uniq.append(t)

    import shutil
    shutil.rmtree(FRAMES, ignore_errors=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    entries, idx = [], 0
    for t0, t1 in zip(uniq, uniq[1:]):
        frame_at(objs, (t0 + t1) / 2).save(FRAMES / f"{idx:06d}.png")
        entries.append((idx, t1 - t0))
        idx += 1
    lines = []
    for i, du in entries:
        lines.append(f"file '{FRAMES / f'{i:06d}.png'}'")
        lines.append(f"duration {du:.4f}")
    lines.append(f"file '{FRAMES / f'{entries[-1][0]:06d}.png'}'")
    (FRAMES / "concat.txt").write_text("\n".join(lines) + "\n")

    outdir = Path(os.environ.get("CLIP_DIR", "/home/box/visuals/outputs"))
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"clip_{s:g}-{e:g}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-f", "concat", "-safe", "0", "-i", str(FRAMES / "concat.txt"),
                    "-ss", str(s), "-t", str(e - s), "-i", str(AUDIO),
                    "-map", "0:v", "-map", "1:a",
                    "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k",
                    "-threads", "2", "-movflags", "+faststart",
                    "-shortest", str(out)], check=True)
    print(f"clip {s:g}-{e:g} ({len(entries)} states) -> {out}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "frame"
    rest = sys.argv[2:]
    if mode == "frame":
        cmd_frame(rest)
    elif mode == "clip":
        cmd_clip(rest)
    else:
        {"dump": cmd_dump, "stills": cmd_stills, "storyboard": cmd_storyboard,
         "render": cmd_render}[mode]()
