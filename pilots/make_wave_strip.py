"""VOICE-WAVE STRIP — scaffold for qwen_design_loop.
Renders a 10s scrolling waveform band of white_s1a_audio.wav (the voice wave, NOT a spectrogram):
white paper, warm-ink mirrored silhouette, stable baseline, smoothed envelope.
Contract with the loop: output experiments/wave_strip.mp4 + wave_strip_t4.5.png + wave_strip_t9.5.png."""
import math, os, subprocess, sys, shutil, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "/home/box/visuals/pilots")
from make_pilot import f, ease, blend, INK, WHITE, VERM

OUT = "/home/box/visuals/experiments"
W, H, FPS, DUR = 1920, 1080, 30, 10.0
N = int(DUR * FPS)
AUDIO = f"{OUT}/white_s1a_audio.wav"
BAND = (110, 872, 1810, 1032)   # same band rect as white S1A
PX_PER_S = 260                  # horizontal resolution of the wave image

FINE_PPS = PX_PER_S * 6          # sub-column resolution for oscillation texture
SOFT = (74, 60, 50)              # warm-ink silhouette body (lighter than the trace line)

def load_env():
    w = wave.open(AUDIO)
    raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(axis=1)
    sr = w.getframerate()
    step = sr / PX_PER_S
    n = int(len(x) / step)
    # RMS per column -> stable silhouette body (never saturates into a fat blob)
    rms = np.empty(n, dtype=np.float32)
    for i in range(n):
        a = int(i * step); b = max(a + 1, int((i + 1) * step))
        s = x[a:b]
        rms[i] = math.sqrt(float(np.mean(s * s)))
    ref_r = np.percentile(rms[rms > 0], 99.0) if (rms > 0).any() else 1.0
    env = np.clip(rms / (ref_r + 1e-6), 0, 1) ** 0.65     # gentle, controlled breathing room
    k = np.hanning(3); k /= k.sum()
    env = np.convolve(env, k, mode="same")
    # fine oscillation: store per-column min AND max of RAW samples (preserves sine shape)
    fstep = sr / FINE_PPS
    nf = int(len(x) / fstep)
    fine_min = np.empty(nf, dtype=np.float32)
    fine_max = np.empty(nf, dtype=np.float32)
    for i in range(nf):
        a = int(i * fstep); b = max(a + 1, int((i + 1) * fstep))
        s = x[a:b]
        fine_min[i] = float(np.min(s)) if len(s) else 0.0
        fine_max[i] = float(np.max(s)) if len(s) else 0.0
    ref_f = max(
        np.percentile(np.abs(fine_max[fine_max != 0]), 99.5) if (fine_max != 0).any() else 1.0,
        np.percentile(np.abs(fine_min[fine_min != 0]), 99.5) if (fine_min != 0).any() else 1.0,
    )
    fine_min = np.clip(fine_min / (ref_f + 1e-6), -1, 1)
    fine_max = np.clip(fine_max / (ref_f + 1e-6), -1, 1)
    return env, (fine_min, fine_max), PX_PER_S, FINE_PPS

ENV, FINE_PAIR, PPS, FPPS = load_env()
FINE_MIN, FINE_MAX = FINE_PAIR

def wave_slice(t):
    bw, bh = BAND[2] - BAND[0], BAND[3] - BAND[1]
    cy = bh // 2
    amp_fill = (bh // 2 - 8) * 0.38      # silhouette body: narrow, leaves clear whitespace
    amp_line = (bh // 2 - 8) * 0.72      # oscillation ticks: extend well beyond body for ring legibility
    img = Image.new("RGB", (bw, bh), WHITE)
    d = ImageDraw.Draw(img)
    d.line([(0, cy), (bw, cy)], fill=(228, 224, 216), width=1)
    c_now = int(t * PPS)
    if c_now <= 0:
        return img
    # --- silhouette (RMS body), right-aligned, constant speed ---
    c_left = max(0, c_now - bw + 1)
    seg = ENV[c_left:c_now + 1]
    n = len(seg)
    if n >= 2:
        xs = np.arange(bw - n, bw, dtype=float)
        top = [(float(x), cy - float(v) * amp_fill) for x, v in zip(xs, seg)]
        bot = [(float(x), cy + float(v) * amp_fill) for x, v in zip(xs, seg)][::-1]
        d.polygon(top + bot, fill=SOFT)
    # --- fine oscillation: bin raw min/max into pixel columns, draw vertical tick marks ---
    f_now = int(t * FPPS)
    f_left = max(0, f_now - bw + 1)
    fm = FINE_MIN[f_left:f_now + 1]
    fx = FINE_MAX[f_left:f_now + 1]
    m = len(fm)
    if m >= 2:
        spp = m / bw  # float samples-per-pixel (~6 at current settings)
        for px in range(bw):
            s0 = int(px * spp)
            s1 = int((px + 1) * spp)
            if s1 <= s0:
                s1 = s0 + 1
            s1 = min(s1, m)
            lo = float(np.min(fm[s0:s1]))
            hi = float(np.max(fx[s0:s1]))
            y_lo = cy - hi * amp_line
            y_hi = cy - lo * amp_line
            if abs(y_hi - y_lo) < 0.5:
                y_hi = y_lo + 0.5
            d.line([(px, y_lo), (px, y_hi)], fill=INK, width=1)
    return img

def frame(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), WHITE)
    sp = wave_slice(t)
    img.paste(sp, (BAND[0], BAND[1]))
    d = ImageDraw.Draw(img)
    d.line([(BAND[0], BAND[1] - 6), (BAND[2], BAND[1] - 6)], fill=(225, 220, 210), width=1)
    return img

def main():
    frames = f"{OUT}/_wf2"
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames)
    for i in range(N):
        frame(i).save(f"{frames}/{i:04d}.png")
        if i % 90 == 0:
            print("frame", i, flush=True)
    out = f"{OUT}/wave_strip.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-pattern_type", "glob", "-i", f"{frames}/*.png",
                    "-i", AUDIO, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    shutil.rmtree(frames)
    print("OK", out, os.path.getsize(out) // 1024, "KB")
    frame(int(4.5 * FPS)).save(f"{OUT}/wave_strip_t4.5.png")
    frame(int(9.5 * FPS)).save(f"{OUT}/wave_strip_t9.5.png")
    print("previews saved")

if __name__ == "__main__":
    main()
