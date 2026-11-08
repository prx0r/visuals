"""WHITE S1A v0 — the three-zone spec: left verse (wipes only), right drawing, bottom spectrogram.
Audio = real slice (bell + Baumer's sūtra-3 read), so card, drawing and spectrum all belong to one moment."""
import math, os, subprocess, sys, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageChops

sys.path.insert(0, "/home/box/visuals/pilots")
from make_pilot import (f, ease, blend, INK, WHITE, VERM, INK50, X as CARD_X,
                        CARDS, balance_wrap)

OUT = "/home/box/visuals/experiments"
W, H, FPS, DUR = 1920, 1080, 30, 10.0
N = int(DUR * FPS)
AUDIO = f"{OUT}/white_s1a_audio.wav"
RAW = f"{OUT}/white_s1a_analysis.raw"
INK_G = (70, 67, 62)

# ---------------- spectrogram precompute ----------------
SR, HOP, NFFT = 22050, 256, 1024
COLS_PER_S = SR / HOP
def build_spectrogram():
    x = np.fromfile(RAW, dtype=np.float32)
    n = (len(x) - NFFT) // HOP + 1
    win = np.hanning(NFFT)
    S = np.empty((n, NFFT // 2 + 1), dtype=np.float32)
    for i in range(n):
        S[i] = np.abs(np.fft.rfft(x[i * HOP:i * HOP + NFFT] * win))
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    ROWS, FMIN, FMAX = 240, 80.0, 4200.0   # voice/formant band, finer grid, keep HF harmonics
    fr = np.exp(np.linspace(np.log(FMIN), np.log(FMAX), ROWS))
    idx = np.clip(np.searchsorted(freqs, fr) - 1, 0, len(freqs) - 1)
    S = S[:, idx]                      # (n, ROWS) log-frequency
    S = np.log1p(S * 10.0)
    ref = np.percentile(S, 99.0)
    v = np.clip(S / (ref + 1e-6), 0, 1)
    v = np.clip((v - 0.20) / 0.80, 0, 1) ** 0.82   # deeper floor: crisp ink ridges, no white voids
    _ma = lambda arr, k: np.apply_along_axis(lambda m: np.convolve(m, np.ones(k) / k, mode='same'), 0, arr)
    v = _ma(v, 4)             # time-smooth: narrow window keeps formant ridges + bell transient sharp
    v = _ma(v.T, 2).T         # light freq-smooth: band continuity without merging harmonics
    v = np.clip(v * 1.95, 0, 1)                 # ridge brightness: strong ink bands, no black saturation
    v = v.T[::-1]                      # image: height=ROWS (top=high freq), width=time
    white = np.array(WHITE, dtype=np.float32)
    ink = np.array(INK, dtype=np.float32)
    verm = np.array(VERM, dtype=np.float32)
    rgb = white[None, None, :] * (1 - v[..., None]) + ink[None, None, :] * v[..., None]
    # no vermillion in the spectrum — red belongs to the dots and nodes only
    return Image.fromarray(rgb.astype(np.uint8))

SPEC = build_spectrogram()
BAND = (110, 872, 1810, 1032)   # x0,y0,x1,y1

def spectro_slice(t):
    c_end = int((t + 0.30) * COLS_PER_S)
    w_cols = int(3.3 * COLS_PER_S)
    c0 = max(0, c_end - w_cols)
    c1 = min(SPEC.width, max(c_end, c0 + 8))
    crop = SPEC.crop((c0, 0, c1, SPEC.height))
    return crop.resize((BAND[2] - BAND[0], BAND[3] - BAND[1]), Image.LANCZOS)

# ---------------- left verse (wipes) ----------------
C = CARDS["verse_3"]
FONT_DEV = f("RozhaOne-Regular.ttf", C["devsize"])
FONT_IA = f("CormorantGaramond-Italic[wght].ttf", 40, 500)
FONT_DEF = f("CormorantGaramond[wght].ttf", 50, 500)
FONT_SRC = f("CormorantGaramond[wght].ttf", 24, 400)

def text_mask(lines, font, lh, maxw=940):
    """L mask of wrapped/multi lines starting at 0,0"""
    imgs = []
    for ln in lines:
        wl = balance_wrap(ln, font, maxw) if len(ln) > 40 else [ln]
        for w_ in wl:
            imgs.append(w_)
    total_h = lh * len(imgs)
    m = Image.new("L", (960, total_h + 40), 0)
    d = ImageDraw.Draw(m)
    for i, w_ in enumerate(imgs):
        d.text((0, i * lh), w_, font=font, fill=255)
    return m, len(imgs), imgs

DEV_M, DEV_N, _ = text_mask(C["dev"], FONT_DEV, int(C["devsize"] * 1.36))
IA_M, _, _ = [text_mask([C["ia"]], FONT_IA, 50)[0], 1, None][:3]
DEF_LINES = balance_wrap(C["definition"], FONT_DEF, 930)
DEF_M, _, _ = text_mask(" ".join(DEF_LINES) if False else DEF_LINES, FONT_DEF, 64)
SRC_M, _, _ = text_mask([C["source"]], FONT_SRC, 34)

def prog(t, s, e):
    return ease((t - s) / (e - s))

def wipe(img, m, pos, p, direction="x"):
    """reveal mask: x=left→right per whole block, y=top→bottom"""
    if p <= 0: return
    w_, h_ = m.size
    rev = Image.new("L", (w_, h_), 0)
    d = ImageDraw.Draw(rev)
    if direction == "x":
        d.rectangle([0, 0, int(w_ * min(p, 1)) + 2, h_], fill=255)
    else:
        d.rectangle([0, 0, w_, int(h_ * min(p, 1)) + 2], fill=255)
    mask = ImageChops.multiply(m, rev)
    ink_layer = Image.new("RGB", (w_, h_), INK)
    img.paste(ink_layer, pos, mask)

LX, LY = 110, 150
DEV_LH = int(C["devsize"] * 1.36)
DEV_Y = LY
IA_Y = DEV_Y + DEV_LH * DEV_N + 18
RULE_Y = IA_Y + 66
DEF_Y = RULE_Y + 52
SRC_Y = DEF_Y + 64 * len(DEF_LINES) + 44

def draw_left(img, t):
    d = ImageDraw.Draw(img)
    wipe(img, DEV_M, (LX, DEV_Y), prog(t, 1.25, 3.25), "x")
    wipe(img, IA_M, (LX, IA_Y), prog(t, 3.3, 4.1), "x")
    # rule draws (the one line motion the owner likes)
    rp = prog(t, 3.0, 4.0)
    if rp > 0:
        d.rectangle([LX, RULE_Y, LX + int(185 * rp), RULE_Y + 2], fill=INK50)
    dp = prog(t, 4.05, 4.4)
    if dp > 0.02:
        breath = 1.0 if t < 5.0 else 0.85 + 0.15 * math.sin((t - 5.0) * 2 * math.pi / 3.0)
        r = 4.5 * min(dp, 1.0)
        cx, cy = LX + 201, RULE_Y + 1
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=blend(VERM, min(dp, 1.0) * breath))
    wipe(img, DEF_M, (LX, DEF_Y), prog(t, 5.6, 7.4), "x")
    wipe(img, SRC_M, (LX, SRC_Y), prog(t, 8.5, 9.3), "x")

# ---------------- right: drawing being drawn ----------------
RX0, RY0, RW, RH = 1150, 150, 660, 600
CX, CY = RX0 + RW // 2, RY0 + RH // 2

def lerp(a, b, p): return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)

def draw_right(img, t):
    d = ImageDraw.Draw(img)
    gray = (140, 136, 128)
    # axes extend from center
    p = prog(t, 0.8, 2.6)
    if p > 0:
        dx = RW * 0.46 * p
        dy = RH * 0.44 * p
        d.line([(CX - dx, CY), (CX + dx, CY)], fill=gray, width=1)
        d.line([(CX, CY - dy), (CX, CY + dy)], fill=gray, width=1)
    # big circle draws clockwise from top
    p = prog(t, 1.6, 4.6)
    if p > 0:
        r = RH * 0.40
        d.arc([CX - r, CY - r, CX + r, CY + r], -90, -90 + 359.9 * p, fill=INK, width=2)
    # second circle (construction, lighter) counterclockwise from bottom
    p = prog(t, 2.6, 5.2)
    if p > 0:
        r = RH * 0.26
        d.arc([CX - r, CY - r, CX + r, CY + r], 90, 90 + 359.9 * p, fill=gray, width=1)
    # inscribed triangle, edges stroked in sequence
    V = [(CX, CY - RH * 0.40), (CX + RH * 0.36, CY + RH * 0.30),
         (CX - RH * 0.36, CY + RH * 0.30)]
    for k in range(3):
        p = prog(t, 4.0 + k * 0.7, 4.7 + k * 0.7)
        if p > 0:
            d.line([V[k], lerp(V[k], V[(k + 1) % 3], p)], fill=INK, width=2)
    # mid-lines (centre to vertices, partial)
    for k in range(3):
        p = prog(t, 5.3 + k * 0.5, 5.9 + k * 0.5)
        if p > 0:
            d.line([(CX, CY), lerp((CX, CY), V[k], p)], fill=gray, width=1)
    # petals: arcs at 60° spacing, staggered
    for k in range(6):
        p = prog(t, 5.6 + k * 0.35, 6.5 + k * 0.35)
        if p > 0:
            r = RH * 0.33
            a0 = -90 + k * 60
            d.arc([CX - r, CY - r, CX + r, CY + r], a0, a0 + 46 * p, fill=INK_G, width=1)
    # inner spanda arcs
    p = prog(t, 7.0, 8.2)
    if p > 0:
        r = RH * 0.13
        d.arc([CX - r, CY - r, CX + r, CY + r], 200, 200 + 300 * p, fill=INK, width=1)
    # vermillion nodes pop
    nodes = [(CX, CY - RH * 0.40), (CX + RH * 0.36, CY + RH * 0.30),
             (CX - RH * 0.36, CY + RH * 0.30)]
    for k, (nx, ny) in enumerate(nodes):
        p = prog(t, 7.2 + k * 0.4, 7.55 + k * 0.4)
        if p > 0:
            r = 5 * min(p, 1.0)
            d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=VERM)
    # centre dot + breath
    p = prog(t, 8.6, 8.95)
    if p > 0:
        br = 1.0 if t < 9.2 else 0.82 + 0.18 * math.sin((t - 9.2) * 2 * math.pi / 2.5)
        r = 6 * min(p, 1.0)
        a = min(p, 1.0) * br
        d.ellipse([CX - r, CY - r, CX + r, CY + r], fill=blend(VERM, a))
    # final thin completion ring
    p = prog(t, 8.8, 9.8)
    if p > 0:
        r = RH * 0.47
        d.arc([CX - r, CY - r, CX + r, CY + r], -90, -90 + 359.9 * p, fill=gray, width=1)

# ---------------- assemble ----------------
def frame(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WHITE)
    draw_left(img, t)
    draw_right(img, t)
    sp = spectro_slice(t)
    img.paste(sp, (BAND[0], BAND[1]))
    d = ImageDraw.Draw(img)
    d.line([(BAND[0], BAND[1] - 6), (BAND[2], BAND[1] - 6)], fill=(225, 220, 210), width=1)
    return img

def main():
    frames = f"{OUT}/_wf"
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames)
    for i in range(N):
        frame(i).save(f"{frames}/{i:04d}.png")
        if i % 60 == 0:
            print("frame", i, flush=True)
    out = f"{OUT}/white_s1a_v0.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-pattern_type", "glob", "-i", f"{frames}/*.png",
                    "-i", AUDIO, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    shutil.rmtree(frames)
    print("OK", out, os.path.getsize(out) // 1024, "KB")
    # previews
    frame(int(4.5 * FPS)).save(f"{OUT}/white_s1a_t4.5.png")
    frame(int(9.5 * FPS)).save(f"{OUT}/white_s1a_t9.5.png")
    print("previews saved")

if __name__ == "__main__":
    main()
