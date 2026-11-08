# FILM — Ñāṇavīra Fundamental Structure video build (2026-10-24)

> Working folder for today's project. Source lock stays in `../` (fs-static.txt,
> fs-dynamic.txt, fs-TIME-PASSAGES.txt + VIDEO.md/STRUCTURE.md). This `film/`
> folder holds the imported renderer pack + pasted docs + build refs.
> Additive only. No binaries in git (see `/root/gochema/.gitignore`).

## Layout

```text
essays/fundamental-structure/
  fs-static.txt            SOURCE LOCK (3,965w, verbatim CtP)
  fs-dynamic.txt           SOURCE LOCK (5,168w, verbatim CtP)
  fs-TIME-PASSAGES.txt     TIME DOCTRINE bank (6,346w, feeds rebirth ch.9)
  STRUCTURE.md             v1/v2 file plan
  VIDEO.md                 thesis + spine
  film/
    00-MANIFEST.md         this file
    refs.md                media referenced by absolute path, never vendored
    pack/                  EssayViz pack, imported verbatim from old volume
    docs/                  relevant docs pasted from gcomedy + old volume
    related/               related essays copied from elsewhere in repo (read in place originals)
```

## PACK — imported verbatim

Source: `/mnt/HC_Volume_106959365/root/projects/essayviz-workspace/packs/fundamental-structure/`
(SHA256SUMS preserved in `pack/SHA256SUMS`; hashes refer to original MOTHERFUCKER layout)

| File | What |
|---|---|
| `pack/README.md` | 27 scenes (13 static + 14 dynamic), one o/x alphabet, build cmds |
| `pack/PROCESS-NOTES.md` | genre = constructive-formal-treatise; persistent alphabet (o/x/T/frame/weight); 13 static + 14 dynamic compositions; epistemic restraint; audio design; 5-checkpoints-per-scene review |
| `pack/AGENT.md` | render agent guide (apply-pack → TTS per narration.json → ffprobe → compile-timed-pack) |
| `pack/analysis.json` | central thesis + continuity objects (o/x/T/frame/weight) + staticBeats + dynamicBeats |
| `pack/storyboard.json` | 27 shots: s01–s13 + d01–d14 (recursive-proof-construction) |
| `pack/narration.json` + `narration.txt` | one concise line per scene (27 lines, NOT verbatim CtP — must be replaced by source passages per AGENT.md) |
| `pack/SOURCE-DYNAMIC.txt` | complete uploaded Dynamic Aspect, verbatim (4,582w) |
| `pack/SOURCE-STATIC-OUTLINE.md` | numbered static construction (compact; full static text NOT in pack — use `../fs-static.txt`) |
| `pack/skills/CONSTRUCTIVE-FORMAL-TREATISE-SKILL.md` | renderer skill for this genre |
| `pack/tools/` | apply-pack.mjs, validate.mjs, render-pack.mjs, compile-timed-pack.py, build-film.sh |
| `pack/src/fundamental-structure-motif.mjs` | renderer motif |
| `pack/src/fundamental-structure-visuals.mjs` | visuals (14KB) |
| `pack/src/fundamental-structure.template.json` | MOTHERFUCKER template |
| `pack/src/fundamental-structure-capability-pack.json` | capability pack (renamed from `MOTHERFUCKER/capability-packs/fundamental-structure/pack.json`) |

Scene list (from storyboard.json):
s01 One thing · s02 Another thing · s03 This and that · s04 Difference as
operation · s05 First and second · s06 The tetrad · s07 Row, column, diagonal ·
s08 Four-member thing · s09 Sixteen-member reflexion · s10 Indefinite expansion ·
s11 Invariant whole · s12 Structure of structure · s13 Infinite hierarchy ·
d01 Duration · d02 Repeated moments · d03 No finite duration ·
d04 Accelerating infinity · d05 Three temporal levels · d06 No absolute outside ·
d07 Irreversible alternation · d08 Intensity hierarchy · d09 Generality as time ·
d10 Past-present-future · d11 Three weighted interchanges ·
d12 Identity by negation · d13 Selection by repeated squaring ·
d14 Unfinished frontier

## DOCS — pasted relevant docs

| File | Origin |
|---|---|
| `docs/NANAVIRA-FUNDAMENTAL-STRUCTURE-SYNTHESIS.md` | `/root/gcomedy/library/nanavira/` — ground-truth synthesis: parasite = Ñāṇavīra's own term (footnote j), duration = invariance, reflexivity guarantee (footnote g), tetrahedron 4/16/64/256 |
| `docs/LOGICAL-ARGUMENT-NANAVIRA.md` | gcomedy nanavira — formal argument |
| `docs/nanavira-dependent-arising.md` | gcomedy nanavira — skeleton (structure + intention as movement) |
| `docs/tractatus-nanavira-abhinavagupta.md` | gcomedy nanavira — reflexion vs IPVV bridge |
| `docs/static-aspect.txt` / `dynamic-aspect.txt` | gcomedy nanavira short versions (1,235w / 895w) |
| `docs/NANAVIRA-NANANANDA-MATERIAL.md` | old volume `research-library/` — Ñāṇavīra × Ñāṇananda combo (vortex bridge) |
| `docs/nanavira-vs-tantraloka-campbell-revisited.md` | old volume `tantraloka/notes/` — comparative mapping |

Also in-repo (originals live elsewhere; working copies in `related/`):
- `../VIDEO.md` — thesis: existence has structure before things; static = framework, dynamic = movement
- `../STRUCTURE.md` — v1 reading (sculpt to ~2.5k w, ~17 min, o/x spoken "oh/ex" + card) · v2 analysis (~1.4k w, ~14 min, every claim tagged to Note § / CtP page)
- `../../dependent-origination/SOURCE.md` — Nanavira × Ñāṇananda combo (skeleton + vortex) → `related/dependent-origination-SOURCE.md`
- `../../dependent-origination/STRUCTURE.md` → `related/dependent-origination-STRUCTURE.md`
- `../../fire-simile/library/clearing-the-path.pdf` — full CtP book (4.0 MB, referenced only)
- `../../../library/hillside-hermitage/HILLSIDE-HERMITAGE.md` — living Ñāṇavira school → `related/HILLSIDE-HERMITAGE.md`
- `../../../library/recognition/` — reflexion debate (RECOGNITION-HANDOVER, ESSAY-RECOGNITION); `pushing-ipvv/IPVV-reflexion-vs-nanavira.md` → `related/IPVV-reflexion-vs-nanavira.md`

## REFS — media by path (see refs.md, never vendored)

- Full book: `/root/gochema/essays/fire-simile/library/clearing-the-path.pdf`
- Old pack origin: `/mnt/HC_Volume_106959365/root/projects/essayviz-workspace/packs/fundamental-structure/`
- Old motif/visuals live copy: `/mnt/HC_Volume_106959365/root/projects/essayviz-workspace/motherfucker/fundamental-structure-{motif,visuals}.mjs`
- Smoke-test render only: `/mnt/HC_Volume_106959365/root/projects/essayviz-workspace/motherfucker/build/test-video.mp4` (165 KB, NOT FS)
- No FS `.mp4` exists anywhere yet — pack was never rendered to film.

## Do we have all the pieces? YES for text, NO for film

- [x] Verbatim sources (static + dynamic + time passages + full CtP PDF)
- [x] Explanation layer (synthesis + logical argument + dependent-arising + tractatus + Ñāṇananda bridge)
- [x] Renderer pack (27-scene storyboard, motif, visuals, template, tools, skill, process notes)
- [ ] v1 READING-ABRIDGED.md (sculpt ~2.5k w verbatim, Pali pinned) — TO WRITE
- [ ] v2 ESSAY.md + script.md + STORYBOARD.md (gochema format per BUILD-PIPELINE) — TO DRAFT
- [ ] Voice decision (Louis vs old-man per fire-simile verdict; STRUCTURE.md: s2.1-pro-free, speed 1)
- [ ] Render (PIL 6fps per series/BUILD-PIPELINE.md) + TTS + alignment + integrity + final mux

## Next actions (BUILD-PIPELINE order)

1. SOURCE LOCK: confirm `../fs-static.txt` + `../fs-dynamic.txt` = pack `SOURCE-DYNAMIC.txt` + CtP (diff banked below); tag RO passages.
2. STORYBOARD: map pack `storyboard.json` (27 scenes) → gochema `storyboard.json` (102-shot style per daimon-companion) OR adopt pack scenes directly.
3. NARRATION: replace pack concise lines with verbatim CtP selections (compiler law: cutting yes, rewriting never).
4. RENDER → VOICE → ALIGNMENT → FINAL per `series/BUILD-PIPELINE.md`.
