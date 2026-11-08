# HANDOVER — visuals workbench (2026-10-28)

Read order: `README.md` (architecture) → `CREATING.md` (owner flow) →
`DESKTOP.md` (desktop ops) → this.

## State
- 4→5 commits, **local only — no remote yet** (only project repo without one;
  vatulanatha/tantracola are on github.com/prx0r).
- Architecture locked and working: code → CPU render → qwen-omni critic →
  structured verdict → revise-shots-only. No GPU. Sheet/timeline = timing
  truth; owner = taste-of-record; installers owner-gated (Qwen-MM
  `install.sh` still NOT run, by law).

## This session's batch (committed here)
- **Wave-strip design loop ran 4 rounds** on `pilots/make_wave_strip.py`
  (`experiments/design_loop_log.json`): scores 2→3→3→2 — **not converged**.
  Round-1 caught a real bug (linspace stretch → fat diamonds instead of a
  scrolling trace) and handed exact old→new edits; later rounds oscillated,
  defect classes: window sizing/lookahead, Hanning smoothing too wide,
  missing right-alignment scroll. Loop = source-editor, not yet a
  fix-verify-against-render loop.
- **Outputs**: `wave_strip.mp4` (10s), `waveA_white_cline.mp4`,
  `waveB_dark_cline.mp4`, frames `wave_strip_t{4.5,9.5}.png`.
  A = white ground, B = dark — both still carry the round-1 defects until
  the edits are applied to the script and re-rendered.

## Queue (was CREATING.md §What's left — unchanged except #2 progress)
1. **Apply the loop's round-1 edits to `make_wave_strip.py`, re-render,
   then compose the waveform band into the white S1A three-zone proof**
   (`make_white_s1a.py` — swap numpy spectrogram → voice waveform,
   loop at 3/4).
2. **Stills-only loop mode** in `qwen_design_loop.py` (full renders never
   per-round — owner rule) + qwen's deep S1A notes (phoneme/word-sync wipes,
   geometry that *means* the verse).
3. Fetch `prx0r/shiva-sutras` + Baumer Śiva Sūtras mp3s (R2) → OPERATOR.md
   S1A full run.
4. Pick the rail/right-panel medium from `visualizers/` via the documented
   loop (candidate → our narration → qwen judges → owner picks).
5. Owner: read+go `Qwen-MM-Plugins/install.sh`; push this repo to a remote.

## Laws worth repeating
- Never run a repo installer without the owner reading it.
- Visuals follow audio events; the critic reviews conformance + feel.
- Taste verdicts need fixtures; owner is taste-of-record.
- Stills-first: approve frames before any full render burns CPU.
- Fleet for heavy renders (opencode1/2/3), never melt the hub.

## Key paths
| what | where |
|---|---|
| engine + book spec + fonts | `~/essay-visual-engine/` (OPERATOR.md, SPEC-BOOK-STAGE.md) |
| art language | `~/whitebeauty/` |
| approved gloss-card renders | `baumer/build/visual_mocks/` |
| audio ears (flow/junction probes) | `baumer/tools/listen.py` (`ask-qwen`, `LISTEN_MIX`) |
| film judge (tantracola) | `~/repos/tantracola/factory/src/factory.py judge --mode …` |
| typography pilots | `pilots/*.py` · outputs manifest `outputs.json` |
