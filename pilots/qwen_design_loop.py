#!/usr/bin/env python3
"""qwen_design_loop — qwen as eyes AND hands.
Sees the current render (video + preview frames), returns STRICT JSON:
  {pass, score, defects[], rationale, edits:[{old,new}]}
Edits are exact unique substring replacements of the target source file.
We apply -> render -> show qwen again -> repeat until pass or MAX_ROUNDS.
Only preview-scale renders. Owner remains taste-of-record.
"""
import base64, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

TARGET = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/box/visuals/pilots/make_white_s1a.py")
MAX_ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 3
OUT = Path("/home/box/visuals/experiments")
LOG = OUT / f"design_loop_{TARGET.stem}.json"
SHOOTOUT = Path("/tmp/opencode/qwen_shootout_results.txt")

def _load_env(path):
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out

_dotenv = _load_env(Path(__file__).resolve().parents[1] / ".env")
QWEN_URL = (_dotenv.get("QWEN_BASE_URL")
            or "https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com"
            "/compatible-mode/v1/chat/completions")
QWEN_MODEL = _dotenv.get("QWEN_MODEL") or "qwen3.8-omni-flash"
QWEN_KEY = (_dotenv.get("QWEN_API_KEY")
            or next((Path(p).read_text().strip() for p in ("/home/box/.qwen_key", "/tmp/opencode/qwen/key")
                     if Path(p).exists()), None))

BRIEF = """You are the DESIGNER-ENGINEER of a white proof page video (White S1A).
Zones (owner's spec, fixed): LEFT = verse card revealed ONLY by ink wipes / rule draw — no fades, no rise;
RIGHT = geometry that draws itself stage by stage, vermillion only on nodes/dots;
BOTTOM = a real spectrogram strip of a spoken-Sanskrit read (must READ as a spectrogram:
visible harmonic/formant bands, bell-vs-voice structure — not gray mush).
Palette: paper white, warm ink, single vermillion. Motion law: construction only (writes, draws,
scrolls) — any fade/slide = PowerPoint = FAIL. Fonts fixed (Tiro/Rozha/Cormorant).
The audio is fixed; timing anchors can move but total stays 10.0s.
You will SEE: current video + two preview frames. Then the CURRENT SOURCE.

Return STRICT JSON ONLY (no fences, no prose outside):
{
 "pass": true/false,
 "score": 1-5,
 "defects": ["terse, worst first"],
 "rationale": "max 300 chars",
 "edits": [{"old": "EXACT unique substring from current source", "new": "replacement"}]
}
Rules for edits: every "old" must appear EXACTLY ONCE in the source as given; keep edits minimal and
independent; prefer retiming constants / geometry / spectrum params over restructuring; you MAY replace
whole functions if needed (old = full function text). If nothing to fix, edits=[]."""

def qwen(parts, timeout=300):
    body = json.dumps({"model": QWEN_MODEL, "modalities": ["text"],
                       "reasoning_effort": "low",
                       "messages": [{"role": "user", "content": parts}]}).encode()
    req = urllib.request.Request(QWEN_URL, data=body,
                                 headers={"Authorization": f"Bearer {QWEN_KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return ((data.get("choices") or [{}])[0].get("message", {}).get("content")) or ""

def media_part(path: Path):
    ext = path.suffix.lower().lstrip(".")
    mime = {"mp4": "video/mp4", "png": "image/png", "jpg": "image/jpeg"}[ext]
    b64 = base64.b64encode(path.read_bytes()).decode()
    if mime.startswith("video"):
        return {"type": "video_url", "video_url": {"url": f"data:{mime};base64,{b64}"}}
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}

def parse_json(txt):
    t = txt.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        t = t[4:] if t.startswith("json") else t
    i, j = t.find("{"), t.rfind("}")
    return json.loads(t[i:j + 1])

def render():
    r = subprocess.run([sys.executable, str(TARGET)], capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return r.stdout[-300:]

def previews():
    return [OUT / "white_s1a_t4.5.png", OUT / "white_s1a_t9.5.png"]

log = {"target": str(TARGET), "rounds": []}
src = TARGET.read_text()
history = ""
verdict = {"pass": False, "score": 0, "defects": ["never ran"], "edits": []}
for rnd in range(1, MAX_ROUNDS + 1):
    print(f"--- round {rnd}", flush=True)
    mp4 = Path(os.environ.get("LOOP_MP4") or "white_s1a_v0.mp4")
    if not mp4.is_absolute():
        mp4 = OUT / mp4
    prev = [OUT / p for p in os.environ.get(
        "LOOP_PREVIEWS", "white_s1a_t4.5.png,white_s1a_t9.5.png").split(",")]
    parts = [media_part(mp4)] + [media_part(p) for p in prev if p.exists()]
    brief = Path(os.environ["LOOP_BRIEF"]).read_text() if os.environ.get("LOOP_BRIEF") else BRIEF
    ctx = brief + f"\n\nCURRENT SOURCE ({TARGET}):\n\"\"\"\n{src}\n\"\"\""
    if SHOOTOUT.exists():
        ctx += "\n\nSPECTROGRAM SHOOTOUT RESULTS (you judged these):\n" + SHOOTOUT.read_text()[:1500]
    if history:
        ctx += "\n\nYOUR PREVIOUS ROUNDS:\n" + history
    t0 = time.time()
    txt = qwen(parts + [{"type": "text", "text": ctx}])
    try:
        verdict = parse_json(txt)
    except Exception as e:
        history += f"\nround {rnd}: JSON PARSE FAIL ({e}). raw head: {txt[:200]}"
        print("parse fail", flush=True)
        continue
    ok = verdict.get("pass") is True
    log["rounds"].append({"rnd": rnd, "score": verdict.get("score"),
                          "defects": verdict.get("defects"), "edits": verdict.get("edits"),
                          "rationale": verdict.get("rationale"), "secs": round(time.time() - t0)})
    LOG.write_text(json.dumps(log, indent=1))
    history += f"\nround {rnd}: score={verdict.get('score')} pass={ok} defects={verdict.get('defects')} rationale={verdict.get('rationale')}"
    print("score", verdict.get("score"), "pass", ok, flush=True)
    if ok or not verdict.get("edits"):
        break
    new_src = src
    fail = None
    for e in verdict["edits"]:
        old, new = e.get("old", ""), e.get("new", "")
        if not old or old not in new_src:
            fail = f"edit old not found (len={len(old)})"
            break
        if new_src.count(old) != 1:
            fail = f"edit old not unique ({new_src.count(old)}x)"
            break
        new_src = new_src.replace(old, new, 1)
    if fail:
        history += f"\nround {rnd}: EDITS REJECTED — {fail}"
        print("edits rejected:", fail, flush=True)
        continue
    TARGET.write_text(new_src)
    src = new_src
    print("edits applied, rendering...", flush=True)
    try:
        out = render()
        print("render:", out, flush=True)
    except Exception as e:
        history += f"\nround {rnd}: RENDER FAILED — {e}"
        print("render failed", e, flush=True)
        TARGET.write_text(src)  # keep patched; next round sees failure
        continue

log["final"] = "pass" if verdict.get("pass") else "max_rounds"
LOG.write_text(json.dumps(log, indent=1))
print("LOOP DONE", log["final"], flush=True)
