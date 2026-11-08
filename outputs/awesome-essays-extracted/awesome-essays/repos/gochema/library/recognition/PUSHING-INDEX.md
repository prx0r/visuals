# PUSHING-INDEX — provenance for the three `pushing-*` collections

> The "pushing" method = hound a primary text with *why*, force its own
> reasoning to carry the conclusion, extract the gems it cannot escape.
> Same method runs on the Tantrāloka and on the IPVV. One index, three dirs.

## The three directories

| Dir | Files | Source (verified byte-identical) |
|---|---|---|
| `pushing-tantraloka/` | 35 | `damn/research-library/recognition/pushing-tantraloka/` — identical copies also at `tantraloka/notes/pushing-tantraloka/` and the volume. **Pre-existing, already tracked.** |
| `pushing-ipvv/` | 10 | `damn/research-library/nanavira-extra/pushing-ipvv/` — identical to the volume copy. **New.** |
| `pushing/` | 5 specs + `_source/` 11 | `damn/research-library/pushing/`. **New.** |

### `pushing-ipvv/` — the 10
`PUSHING-IPVV.md` · `IPVV-reflexion-vs-nanavira.md` · `IPVV-recognition-formulations-vs-mepit.md` ·
`IPVV-internal-arc-vimarsas.md` · `IPVV-felt-to-ground-argument.md` ·
`IPVV-internal-method-opponents-agama.md` · `IPVV-buddhist-co-opting.md` ·
`IPVV-probe-tantraloka-cruxes.md` · `IPVV-MEMORY-vs-whattheheckismemory.md` ·
`LOGICVID-session-ipvv-v3i-parallels-counters.md`

### `pushing/` — the method layer
`PUSHING_GUIDE.md` · `AUTONOMOUS_PUSHING_AGENT_SPEC.md` ·
`DESIGN_LAYERED_COMPARATIVE_QUESTIONNAIRE.md` · `QUESTIONNAIRE_REAL_DNA.md` ·
`SPEC_COMPARATIVE_PUSHING.md`
`_source/` = the logic-session seeds (`logic5–7`, `logicdog`, `logicframework*`,
`logicvid3`, `logicvidsmethod`, `logicvid-postmortem`) + the two master scaffolds.

## Dedupe log (decisions made at import, hashes checked)

1. **`_source/PUSHING-TANTRALOKA.md` SKIPPED** — byte-identical
   (`8df022d7…`) to the already-tracked `pushing-tantraloka/PUSHING-TANTRALOKA.md`.
   Importing it would have been a pure duplicate.
2. **TWO VERSIONS OF `PUSHING-IPVV.md` — both kept.** They share their first
   75 lines; `_source/` (12.2KB) is a **strict superset** adding
   *"The essay-hounds (2026-08-11) — the tough questions, and the gems"*
   (Q1–Q10: proof-chain · σ-flip · three-kinds · transcendental argument …).
   The shorter `pushing-ipvv/` copy (6.8KB) is the one the Ñāṇavīra audiobook
   was built from (section `13-pushing-ipvv` in the TTS manifest). Shorter =
   what was narrated; longer = what was argued. Don't collapse them.
3. **`_source/logicvid-postmortem.md` duplicates `nanavira-extra/tractatus/logicvid-postmortem.md`**
   (identical `defb784f…`). Kept here; the `nanavira-extra` copy arrives later
   with `library/nanavira/`. When that lands, drop **one** — not this one, since
   it sits in the method lineage.

## Not in this index
`IPVV-PLAIN-ENGLISH-BRIDGE.md` and the `r2-audio-transcripts/` IPVV talks live
at the `library/recognition/` level — they are recognition material that
*happens* to be IPVV, not part of a pushing session.
