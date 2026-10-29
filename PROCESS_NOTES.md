# PROCESS NOTES — how we got to canonical v3 (the journey, 2026-10-29)

The session that ended with `NORTHSTAR.md` v3 + `outputs/scene_frame.png` as
the canonical look. Written as it actually happened, wrong turns included —
shiva-sutras' PROCESS_NOTES convention: state claims live here, mistakes keep
their scars.

## Act 1 — two repos and an ontology that lasted half a day
- Started as a review of `~/visuals` + `~/Downloads/yt/baumer` (Vātūlanātha).
- Owner set ontology #1: **black ground, white light reveals, text appears as
  light finds it.** Saved to AGENTS.md + NORTHSTAR. Within hours the owner
  reversed it: *"white background always, no animation, just the verse on the
  screen."* The whole black/light apparatus (light regions, per-object reveals,
  mirror axis, vermillion dot) was built, rendered, judged — then retired.
  Lesson: the spec file is the only durable thing; renders are disposable.

## Act 2 — process law written in blood (AGENTS.md mistakes log, 4 entries)
1. **Full render fired before design confirmation** → dev ceiling: without an
   explicit "render full", the largest artifact = stills + ≤20s clip.
2. **43-frame storyboard during iteration** → one-frame loop:
   `scene.py frame` = the unit of work; judge it, fix, re-render. Storyboards
   are a deliverable AFTER lock, never a probe.
3. **Deliverables handed over as prose paths** → one-link delivery: everything
   ships via the outputs server (`127.0.0.1:8600`) as ONE link or index page
   (birth of `voice_shootout/index.html`).
4. Plus the standing **NEVER BLOCK** protocol: synchronous scp/ffmpeg in a tool
   call = killed at 2 min mid-transfer; everything >10s is a job script with
   its own log, md5-verify, poll, collect, `notify-send`.

## Act 3 — the fleet saga (renders never touch this box again)
- Two local ffmpeg encodes died SIGKILL (box load + my own tool-timeout
  killing chained commands — I violated my own protocol inside the fire call).
- Dispatch v1→v5 to **opencode3**, each killed a specific bug:
  - forgot to `tar xzf` the bundle → `scene.py not found`
  - `[ -f scene.py ] || tar` guard → stale code after bundle update (always extract)
  - watcher `pgrep -f "scene.py render"` matched its own cmdline → blind to
    failure (bracket trick `[s]cene.py` — bit me twice afterwards)
  - `ve/glosscard.py` rendered 6 demo cards **at import** with hardcoded
    `/root/.fonts/` → remote death → now env-driven, `__main__`-guarded
  - root pushing a box-owned repo → git `safe.directory` dance
- Result: render fleet-ready; first real fleet artifact = `clip_0-60.mp4`
  (owner asked for first minute; computed entirely on opencode3).

## Act 4 — the qwen judge (and the day it earned its keep)
- The `pilots/qwen_design_loop.py` studio survived every redesign; I bypassed
  it all morning (eyeballing frames) until the owner called it out: *"our qwen
  judge should be a full git repo, not a py file."* → **`~/qwen-judge`** repo:
  `judge.py` (strict JSON, exit-gated), `qwen.py` (gateway), `loop.py`,
  `chat.py` (direct omni chat), `specs/northstar.md`.
- Verdict trail on the same frame: pass/7 → *fail/5* ("fill the canvas to
  ~100px margins, columns feel mis-anchored") → FILL mode → pass/8 → then the
  owner's ear found things no model did (see Act 5). Model verdict = a hint;
  owner ear = the gate (shiva-sutras READ-THIS-FIRST says the same).

## Act 5 — layout archaeology (every owner note = one surgical fix)
Owner notes in order, each re-rendering THE one frame:
1. *"English starts below and ends below it… Sanskrit contains the English"* →
   mirrored containers, shared optical band.
2. *"subtle gap so we know which phrase corresponds"* → English split at
   punctuation, phrases anchored to Sanskrit rows; then the **equal-span gap
   bug** (short phrase inherited two rows → 300px hole) → length-proportional
   spans.
3. *"why is there a huge gap"* → the bug above, fixed live.
4. *"no middle part"* → stale Falkon tab (disk file was right) + restored the
   mirror hairline; later **removed by owner order** — "no funny business" won.
5. *"mathematical precision… like a grid"* → searched typography theory:
   **Vignelli Canon** (centered = lapidary/rhetorical text ✓ sūtras qualify;
   type-size↔column ratios; contrast = scale) + **φ modular scale**
   (36 → 44 → 72; display ≈ 2× secondary). No more fill-the-band stretching —
   size is a function of the column.
6. *"hyphens… no"* (they came, they went — word separation = space only),
   *"sanskrit itself not separated, textually perfect as written"*, *"romanised
   tight underneath the exact character, smaller"*, *"compress both sides"* →
   the grid: continuous Devanagari run, grey IAST snug under each akshara,
   layout advances by Devanagari width so alignment cannot drift, compressed
   leading, content-based stacked/split decision (≤15 units = stacked).

## Act 6 — the side quests that fed the design
- **Transcripts**: `transcripts/ph-intro.txt` = raw ASR sludge (duplicating
  windows, inline word stamps, `schloka`/`AB inag Gupta`/`kashm shis`) —
  proofread queued; it's Śiva-Sūtra-lineage material, not Vātūlanātha's own.
- **Voice shootout**: 3 owner-locked Fish seats (Sadhguru primary, Osho@0.85,
  Gurudeep) read sūtra 1 → one index page (`voice_shootout/index.html`).
- **Text validation vs sanskritdocuments.org proofread edition**: 10/13 exact;
  v2 = edition apparatus (KSTS brackets kept), v3 = open (oddhaṭṭa/oddhvāṭṭa),
  v5 = **adopted theirs: saṅghaṭṭān** (surface sandhi, proofread Devanagari,
  TTS-safe) → `baumer/text/VALIDATION.md`.
- **Modern scholarship survey**: no post-1923 English translation exists;
  Kaul 1923 IS the canonical translation; watch Muktabodha's 2025 Translation
  Series. Sanskritdocuments ITRANS saved as `text/vatula_sanskritdocuments.itx`.

## Where it stands (end of session)
- Canonical: `NORTHSTAR.md` v3 + `outputs/scene_frame.png` (reference still).
- Renderer: `standard_cards/scene.py` (`frame`/`storyboard`/`clip`/`render`).
- Judge: `~/qwen-judge` (grading against northstar v3).
- Not yet done: ph-intro proofread, TTS seat pick → verse+Kaul reading track,
  v3 scan check (oddhaṭṭa), full storyboard → fleet render (owner's word only).
