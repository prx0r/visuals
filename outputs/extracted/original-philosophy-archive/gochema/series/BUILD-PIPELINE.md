# BUILD PIPELINE — source essay to rendered film

Proven on the volume build (zeus-test-1, 102 shots, 638.6s). Deterministic,
staged, gated. No stage starts until the previous gate passes.

## Stages + gates

### 1. SOURCE LOCK
Verbatim essay with RO passage tags. Word + sentence counts banked.
GATE: every quote tagged; counts recorded in ANALYSIS.md.

### 2. STORYBOARD
`storyboard.json`: one row per shot — id, start/end/duration, spoken passage,
chapter, visual_mode, visual_mechanism, continuity_object, transition,
caption_restriction.
GATE: durations sum to narration runtime ±5%; one mode per shot.

### 3. RENDER (PIL, 6fps)
`render_<slug>.py` draws frames per shot into `scenes/sNNN/`, concats to
per-scene mp4s. Palette constants only (VOID/GOLD/CRIMSON/LAPIS/INK).
GATE: all scene mp4s exist; `draft.mp4` assembles.

### 4. VOICE
Per-shot wavs (`s001.wav`…) + `full_audio.wav` via `audio.txt` concat.
TTS: Edge cache (`tts-cache/`) or Fish. Cache by (text, voice).
GATE: every shot has audio; durations feed stage 5.

### 5. ALIGNMENT + INTEGRITY
`alignment_report.json` (expected vs actual per shot; tolerance 1s) and
`script_integrity.json` (source-vs-spoken sentence match).
GATE: sentence_match PASS, max drift <1s. FAIL blocks publish (see
daimon-companion ANALYSIS: s001 drift 1.9s, 86/87 sentences).

### 6. FINAL
Mux scenes + full audio → `final.mp4`. AV drift must be 0.
GATE: watch-through at 1x before publish.
