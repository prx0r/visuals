#!/usr/bin/env python3
"""Auto-generated render script for zeus-test-1."""
import sys, os, math, subprocess, json
sys.path.insert(0, '/root/projects/blog/scripts/renderer')
sys.path.insert(0, '/root/projects/blog/visual-library')
from PIL import Image, ImageDraw
from renderer import *

FPS = 6
OUT = r"/mnt/data/tantra_animation_packs/selected_expansion_essays/content/publishing/renders/zeus-test-1/v1"

with open(f"{OUT}/storyboard.json") as f:
    SHOTS = json.load(f)

VOID = (13,17,23); GOLD = (212,165,116); CRIMSON = (141,44,57)
LAPIS = (42,70,110); INK = (230,225,220); MUTED = (145,141,132)

def render_scene(d, cx, cy, t, u, variant):
    """Draw a scene that varies by variant index for visual variety."""
    th = 1 + 0.04 * math.sin(t * 0.8 + variant * 0.3)
    r = 4 + 3 * math.sin(t * 0.5 + variant)
    dot(d, cx, cy, r * th, GOLD, 0.7)
    for i in range(2):
        ri = (35 + i * 30 + variant * 5) * th + 3 * math.sin(t * 0.4 + i + variant)
        ring(d, cx, cy, ri, GOLD, max(0, 0.15 - i * 0.04) * (0.5 + 0.5 * math.sin(t * 0.3)), 1)
    if variant % 3 == 0:
        dot(d, cx - 40, cy - 20, 3, CRIMSON, 0.4 + 0.3 * math.sin(t * 0.6))
    elif variant % 3 == 1:
        dot(d, cx + 40, cy + 20, 3, LAPIS, 0.4 + 0.3 * math.sin(t * 0.5))
    else:
        for i in range(3):
            a = t * 0.2 + i * 2.094
            d.line([(cx, cy), (cx + 50 * math.cos(a), cy + 50 * math.sin(a))], fill = rgba(GOLD, 0.3), width = 1)

def render_all():
    for i, s in enumerate(SHOTS):
        sid = f"s{i+1:03d}"
        dur = s["duration"]
        sd = os.path.join(OUT, "scenes", sid)
        os.makedirs(sd, exist_ok = True)
        frames = int(dur * FPS)
        for fi in range(frames):
            im = canvas(VOID)
            d = ImageDraw.Draw(im)
            t = fi / FPS
            u = fi / frames if frames > 1 else 1
            render_scene(d, 640, 360, t, u, i)
            im.save(os.path.join(sd, f"frame_{fi:05d}.png"))
        
        mp4 = os.path.join(OUT, "scenes", f"{sid}.mp4")
        subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i",
            f"{sd}/frame_%05d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "ultrafast", "-crf", "28", "-t", str(dur), mp4],
            capture_output = True)
        if i % 10 == 0: print(f"  [{i+1}/{len(SHOTS)}] {sid}")
    
    # Assemble
    with open(os.path.join(OUT, "concat.txt"), "w") as f:
        for s in SHOTS:
            sid = f"s{SHOTS.index(s)+1:03d}"
            f.write(f"file '{os.path.join(OUT, 'scenes', sid)}.mp4'\\n")
    
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i",
        os.path.join(OUT, "concat.txt"), "-c", "copy",
        os.path.join(OUT, "draft.mp4")], capture_output = True)

if __name__ == "__main__":
    render_all()
    print("Done.")
