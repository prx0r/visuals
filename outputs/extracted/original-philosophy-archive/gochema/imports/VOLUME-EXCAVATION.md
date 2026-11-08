# VOLUME EXCAVATION — full dig report (2026-10-19)

> Every attached volume walked. Paths are absolute on this box. Import = copy
> text into repo; reference = read in place; ignore = leave alone.

## The four volumes

| Volume | Size | Verdict |
|---|---|---|
| `/mnt/data` | 217 MB, 8,030 files | DONE — tantra packs, see VOLUME-MANIFEST.md |
| `/mnt/HC_Volume_106959365` | ~19 GB in `/root/projects` + 1.1 GB content-sources + 642 MB library | THE DIG — previous-gen box, catalogued below |
| `/mnt/HC_Volume_106427611` | 83 MB, 712 files | easy-cache: TTS segment mp3s, reference only |
| `/mnt/snapshot` | empty | Nothing there |

## Old-box `/root/projects` — what matters for gochema

### 1. `projects/tantraloka/` (883 MB) — THE SOURCE ★★★
- `goldrender/` — 255 pack-builder `.py` scripts (abhasa, aham, amnayas,
  atalanta, alchemy…): these GENERATED the R2 film packs. Import priority 1.
- `platinum/` — 22 platinum pack scripts. `expansion-packs/unpacked/`.
- `notes/` — 25 comparative-mapping notes (ficino-sun-tantraloka,
  proclus-mapped-to-tantraloka, nanavira-vs-tantraloka, my-big-toe…).
- `essaylist.md` — ranked visual-essay candidate list (Tier 1/2 with visual angles).
- `explained/hareesh/`, `camatkara-rasa-passages.md`, `passages-vol7-8.md`.
- EMPTY (already harvested to R2): `essays/`, `expansion-essays/`, `narration/`, `newpacks/`.

### 2. `projects/source-library/` (4.2 GB) — THE LIBRARY ★★★
By tradition: tantra (abhinavagupta, dyczkowski-translations, lakshmanjoo,
ksemaraja, jayaratha, texts-clean, hareesh-blog, matter-of-wonder…) +
alchemy, astrology, buddhism, consciousness, hermetica, occult, platonism,
sufism, vedic + `INDEX.md` + `agent/` + `acquisitions/`. Reference in place.

### 3. `projects/renderio/` (1.8 GB) — THE FACTORY ★★☆
`catalog/` (MECHANISM-CATALOG.md, PIL-INDEX.md, primitives, renderers, gen-topics.py),
`gold-examples/GOLD-MANIFEST.md`, `process/` (pipeline.md, OUTPUT-PATHWAYS.md),
`rasa/RASA.md`, `style/STYLE-MANIFEST.md`, 27 `transmissions/`
(ESSAY_TO_VISUAL_WORKFLOW.md, FULL-CREATION-PROCESS.md, 22-FAILURE-MODES.md…),
`output/mechanism-gallery/`, `EXCAVATION-GUIDE.md`, `GRAND-INTEGRATION-SPEC.md`.

### 4. `projects/essayviz-workspace/` (1.5 GB) — THE STUDIO ★★☆
`packs/` (cymatics, fundamental-structure, math), `shorts/` (atalanta, blake-marriage,
emerald-tablet, poimandres, greene-lyon… + HANDOVER), `notes/` (ra-system,
ecology-of-souls taxonomy, entities-by-density), `core/` renderer,
`examples/essay-05`, `build/` (tetrahedron), `synergetics/`.

### 5. `projects/research-library/` (150 MB) — THE COMMENTARY ★★☆
COMMENTARY-NODE/STAGE files, `DAIMON-CONTACT-AS-RECOGNITION.md` (directly on-theme),
comparative models (7-FOLD, 5-STAGE-LENS), `CURRENT-STATE-OF-PROJECT.md`.

### 6. `projects/clean/` (1.6 GB) — bundles + analyses ★☆☆
`.bundle` composition packs, ANALYSIS-TYMOCZKO/ALBERS/DOCZI.md, CODEX-TRUTHMAP*,
chatgpt-logicvid-package. Mine selectively.

### 7. `projects/reception/` — THE UPLOAD PATH ★★☆
`ingest_producer.py` + `postiz_client.py` (how things got to R2),
`spec/` (staging: same PDFs now in R2 uploads/), `upload-data/` (40 KB),
README + AGENTS. Read before any new upload work.

### 8. Supporting
- `content-sources/` (1.1 GB): tantra, occult, platonism, sufism, hermetica,
  astrology, science, modern, tools + `_index.json`. `content/` (6.7 MB): glossary, works.
- `library/` (642 MB): frontier. `vidyut-0.4.0/` (78 MB): Sanskrit TTS
  (sandhi/chandas/kosha/prakriya/cheda). `scripts/` + `search_results/` +
  `source_atlas_papers.md`: PubMed/PMC paper pipeline (create/search/fix/download scripts).
- `workspace/skia-framework/`: 5 gemma-primitives JS (≡ R2 skia-framework).
- `outputs/`: 4 mock mp4s, 24 bytes each — stubs, ignore.
- `easy-cache/` (other volume): 712 TTS segment mp3s — reference only.

### Out of scope (noted, not touched)
`projects/patala/` (5.6 GB app platform), `data/coolify/` (docker state),
`win11React`, `media-os`, `zohomail`, `blog` (empty), dotfiles/caches.

## Import plan for gochema

1. tantraloka: `essaylist.md` + all of `notes/` + `goldrender/*.md` + platinum list (text only)
2. research-library: DAIMON-CONTACT + COMMENTARY index + CURRENT-STATE
3. renderio: `transmissions/ESSAY_TO_VISUAL_WORKFLOW.md` + MECHANISM-CATALOG + STYLE-MANIFEST + RASA.md
4. reception: README + ingest producer (read-only study)
5. essayviz: shorts HANDOVER + CHECKPOINT + notes 01–10 (study, no code yet)
6. source-library/content-sources: index files only (`INDEX.md`, `_index.json`) — bodies stay referenced
