# VISUALS — the visual-engine workbench (est. 2026-10-27)

Everything for "all this stuff" lives here: reference skills, official toolkits,
evaluators, and the locked architecture. The renderers stay where they were
(see map at the bottom).

## What's imported

| path | what | why |
|---|---|---|
| `skills/awesome-design-md/` | 84 brand DESIGN.md files (Claude, Stripe, Nike…) | design language drops — an agent (or prompt) can be told "make it like X" |
| `skills/taste-skill/` | anti-slop art-direction skill: researched direction library (247 award sites), no-slop house rules, `draw.mjs` deals 3 directions, look-and-fix on screenshots | taste codified — feeds card/engine generation prompts |
| `Qwen-MM-Plugins/` (85M) | **official Qwen multimodal toolkit** — `video-edit` (Watch→Plan→Generate→Assemble→Review; **FFmpeg + HyperFrames + GSAP**), `edu-agent` (problem→storyboard→HTML scenes→HyperFrames→35 checks), `blender`, `video-memory`, `omni-memory`, `omni-skill-creator` (demo video → reusable skill), `core` | the workflow we proposed, official. **`install.sh` inspected, NOT run** (it writes harness configs + API keys — owner go required) |
| `references/JAVEdit/` | Qwen-as-video-judge research: generate→score→diagnose→repair→**store fixes** (36%→83% over 3 rounds) | the evaluator/QA-loop design, incl. structured verdicts |
| `skills/taste-skill` · `video-edit/skill/looks/` | ready-made motion looks: **paper-collage, brush-calligraphy**, film-reel-carousel, freeze-punch-intro | kinetic vocabulary for our cards — paper/ink looks = our aesthetic |

## Architecture (locked direction, 2026-10-27)

```
coding agent writes animation code (engine / GSAP / SVG / Blender / HyperFrames)
  → CPU render, low-res review clip (HyperFrames — skills already installed here)
    → Qwen3.8-Omni critic via API (hosted, no GPU) — watches + listens
      → structured verdict: {shot_id, pass, issues:[{time, severity, category,
        observation, fix}], recommended_action}   (JAVEdit pattern)
        → fail: revise affected shots only → re-render just those
          → pass: final resolution
```

- Our `listen.py` (baumer tools) = the critic seed — upgrade its output to
  this JSON verdict schema; our DONE-rule stays the calibration law:
  **deterministic checks catch measurable defects; omni taste is calibrated
  against owner-approved fixtures** (v1/v3-style).
- No local GPU, ever, to start: qwen via API (already doing this), render CPU
  (HyperFrames low-memory), Blender CPU. Rent GPU only after measuring a
  bottleneck.

## First steps

1. Read `Qwen-MM-Plugins/src/capabilities/video-edit/` + `edu-agent/` cookbooks —
   distill their Watch/Plan/Generate/Review + 35-check patterns into our docs.
2. Upgrade the critic: `listen.py` → JSON verdict schema (timestamp · defect ·
   severity · fix), clip-scoped re-reviews.
3. **First live run = the S1A upgrade** (white typography · spectrogram rail ·
   fluid right panel) under this loop.
4. Later: `omni-skill-creator` — feed it demo videos (our card animations,
   page turns) → reusable skills; `blender` plugin for the book-stage set.

## Map (things that did NOT move)

- renderer + book spec + typography: `~/essay-visual-engine/` (fonts/ there too)
- art language: `~/whitebeauty/` · card renders: `baumer/build/visual_mocks/`
- audio QA (the ears): `baumer/tools/listen.py` + `process/19,20`
- frames/render harness: HyperFrames skills (installed) · animation refs: whitebeauty + refs in engine

## Rules

1. Never run a repo's installer without the owner reading it first.
2. Visuals follow audio events (sheet/timeline = source of truth) — the
   critic reviews *conformance + feel*, never invents new timing.
3. Taste verdicts need fixtures; the owner is taste-of-record.

## Added 2026-10-27: `visualizers/` — the experiment shelf (12 repos, ~157MB)

Voice-reactive visualizers, Oct-2026 cohort, to find our medium:
**run-first (headless-capable):** `voice-garden-render` (audio→deterministic MP4, has agent skill) · `speech-timestamp-viewer` (portable speech spectrogram HTML) · `tonescope` (log-freq waterfall).
**adaptable (need file-input wrappers, currently live/mic):** `orbloom` (voice orb, 36 variants, transparent compositing) · `waveform-react` (pitch/loudness-driven 1800-dot sphere) · `saystack` (spectral aura + read-along) · `audiogram-studio` (5 styles + word captions + video export — YouTube-shaped) · `voice-garden` (100k particles) · `FluxGraph-Studio` (particles/contours + PNG/WebM/MP4 export) · `webgpu-visualizer` (low-latency tech base) · `liquid-glass-recorder` (aesthetic inspiration) · `audiolens-seekbar` (spectrogram themes, Windows-only).
Loop: candidate → feed our narration audio → qwen judges (beauty + does-it-stay-under-the-voice) → owner ear → winner becomes the rail/right-panel medium.
