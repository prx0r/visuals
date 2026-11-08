# CREATING VISUALS — the owner's how-to (Baumer movies & friends)

Three docs, one job each — start here, then dive:
- **this** = the flow from idea → finished visual
- `essay-visual-engine/docs/OPERATOR.md` = the exact render runbook (timeline → validate → stills → draft → render)
- `~/visuals/DESKTOP.md` = the desktop/IDE/dispatch cheatsheet

## The cast
| thing | where | state |
|---|---|---|
| Baumer audio (Śiva Sūtras) | R2 `longform-audio/bettina-baumer-shiva-sutras/` (pull per `shiva-sutras` repo NEXT.md B4; local repo = **not yet fetched — todo**) | inputs |
| White-pencil art (lora2) | `/home/box/sleepdraw/assets/*lora2-flux-pencil.jpg` | ✅ present |
| Rendering engine | `/home/box/essay-visual-engine` (`ve.cli`: validate/preview/render) | ✅ + OPERATOR.md runbook |
| Typography pilots (verse cards etc.) | `/home/box/visuals/pilots/make_pilot.py`, `make_white_s1a.py`, `make_wave_strip.py` | ✅ pattern proven |
| Fonts | Tiro Devanagari Sanskrit + Cormorant Garamond (`essay-visual-engine/fonts/`, `~/.fonts`) | ✅ locked |
| qwen eyes | `pilots/qwen_design_loop.py` (auto iterate) or bridge `POST /api/qwen` | ✅ used on every ship since v0 |
| Fleet for heavy renders | `opencode3` (6 idle cores first), skill **`parallel-dispatch`** | ✅ 3-way proven |
| View results | **the IDE**: open the output folder (`?folder=/home/box/essay-visual-engine`), click png/mp4 | ✅ |

## The flow (how you make one)
1. **Say the intent** (verse, mood, length) — sessions turn it into a timeline/pilot script.
2. **Inputs in place**: audio mp3 (R2 pull), art jpgs, manifest — OPERATOR.md step A.
3. **Run the runbook**: `timeline → validate (must PASS) → preview stills (cheap!) → draft → render`.
   Stills-first is the law: you approve frames before any full render burns CPU.
4. **Eyes before you see "done"**: qwen reviews stills/clip (loop or `/api/qwen`) — verdicts get fixed, not argued.
5. **View in the IDE**: click the outputs in Explorer (images inline, mp4 in the video player).
6. **Heavy renders go to the fleet** (opencode3 → opencode2 → opencode1), never melt the hub — skill `parallel-dispatch`.
7. **Ship**: commit scripts + manifest; owner's ear/taste = final (DONE-rule).

## Where each visual family lives
- **Baumer movie (book-stage)** → `essay-visual-engine` + OPERATOR.md (S1A section is the worked example).
- **Verse-card pilots** (the elegant Tiro/Cormorant cards) → `visuals/pilots/` (`pilot_verse3/10`, `pilot_svatantrya` mp4s).
- **Gloss cards** (approved set) → `essay-visual-engine` refs/qa (6 approved: shaktipata, mahashunyata, …).
- **White Śiva Sūtras proof** → `make_white_s1a.py` (three-zone: verse wipes · live drawing · bottom band).
- **Dual-reading v3** → DONE (owner: beautiful) — the reference for flow/timing taste.

## What's left (the queue)
1. **White S1A bottom band** → swap the numpy *spectrogram* for the **voice waveform** (`make_wave_strip.py`, loop at 3/4) and compose it into the three-zone proof.
2. **qwen's deep S1A notes**: wipes tied to phoneme/word boundaries, geometry that *means* the verse ("mood board, not a piece") — run the loop stills-only (build that mode first; full renders never again per-round).
3. **Fetch `shiva-sutras` repo + Baumer mp3s** → then OPERATOR.md S1A full run.
4. **Qwen-MM-Plugins**: `install.sh` inspected, **owner go** required (video-edit Watch→Plan→Generate→Review); JAVEdit verdict schema into the loop.
5. **Ops**: opencode2 → ssh key (password file is world-readable); disks on all three VPSes at 96–98% (clean or stdin-pipe forever); `dispatch.sh` job-queue stub; quill-app git push (held for stash→pull→pop); FLEET plan doc (parked).
6. Gallery/R2 publishing = **retired** (archive only) — viewing is the IDE now.

## Rules that don't bend
- stills before renders · renders on owner's word · qwen eyes before "done" · DONE-rule (deterministic checks for measurable stuff, qwen for taste, owner = taste-of-record) · hub stays light · dispatch by unit, collect back to `experiments/`.
