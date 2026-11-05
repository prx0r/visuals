# HANDOVER — Prayer Books & Publishing Pipeline (2026-11-05)

*Read this first. Repo: `prx0r/visuals` (main). Book work lives in `prints/`.
Corpus: `/home/box/repos/translation-work` (git — `git pull` before sourcing; it moves daily).*

---

## 1. What exists (all committed & pushed)

| Book | Format | Pages | State |
|---|---|---|---|
| `prints/practical-prayers` | **data-driven (bookkit)** | **108** | KDP-ready; "the introduction to prayer" — 11 sections × 4 = 44 prayers |
| `prints/tantric-prayer` | **data-driven (bookkit)** | **108** | KDP-ready; 9 navarasas × 4 = 36 + Sangha appendix 7 = 43 prayers; advanced register |
| `prints/anthology` | legacy compile.py | 99 | Anuttara I — Invocations of the Heart (42) |
| `prints/anthology2` | legacy compile.py | 162 | Anuttara II — Practitioner's Day (22 + Daily Ten) |
| `prints/recognition-dummies` | legacy build.py | 55 | 177 Q&A from the box archive |
| `prints/poems1` | legacy compile.py | 54 | Poems I — The Surrender (L4 craft-notebook spreads) |

**Data-driven book anatomy (PP & TP — canonical pattern):**
```
<book>/
  book.json      meta{title,subtitle,blurb,epi_iast,epi_en,epi_src} +
                 sections[{id,numeral,title,sub,gloss?,doctrine?}] + glyph:"rasa"|"activity"|null
  entries.json   [{id,section,title,source,source_ref,source_path,
                   brief,logic,howto,en(=lineated lowercase),iast+devanagari | corpus:[ch,verse]}]
  front.html     raw <section> blocks (intro/axiom pages) — after epigraph, before TOC
  back.html      raw <section> blocks (colophon etc.) — after spreads, before Sources
  sources/       linked files (L2 mds, L4 jsons, corpus json, Swamiji PDFs) — guides link them
  fonts/         Tiro Devanagari + Cormorant Garamond (OFL)
  compile.py     5 lines -> bookkit.engine.build(dir)
  stale.py       STALE = [retired entries] — NEVER delete; pull back when needed (43 right now)
```
- Engine: `prints/bookkit/engine.py` (all CSS + cover/epi/TOC/dividers/spreads/shanti/bib; features by book.json flags)
- Glyphs: `prints/stencils.py` (rasa rosette w/ petal-n highlight; activity glyphs incl. alone/flatness/gratitude)
- **Gate:** `python3 prints/kdp_preflight.py <pdfs>` must PASS (A5 trim, fonts embedded >=7pt, source CSS >=7pt). Both books PASS at **108pp** — KDP flat $2.30 tier is <=110pp, **never grow past 110**.
- Type scale locked in `prints/EDITIONS.md` (Tiro + Cormorant; guide body 11.5/1.55; min 8.5pt).

## 2. Build & verify loop (copy-paste ready)

```bash
cd /home/box/visuals/prints/<book>
/home/box/Documents/patala/.venv/bin/python3 compile.py      # needs venv (indic_transliteration)
cd /tmp/opencode && timeout 120 google-chrome-stable --headless=new --disable-gpu --no-sandbox \
  --disable-dev-shm-usage --disable-crash-reporter --no-pdf-header-footer \
  --print-to-pdf=/tmp/opencode/<book>.pdf http://127.0.0.1:8000/<book>/
pdfinfo /tmp/opencode/<book>.pdf | grep Pages
python3 /home/box/visuals/prints/kdp_preflight.py /tmp/opencode/<book>.pdf
cp /tmp/opencode/<book>.pdf /home/box/visuals/prints/<book>/<book>-preview.pdf
```
- Serve: prints is already served — `http://127.0.0.1:8000/<book>/`
- Push (NEVER block): `setsid nohup bash /tmp/opencode/push_visuals.sh > /tmp/opencode/push_visualsN.log 2>&1 </dev/null & disown`
  (script = git push origin main + notify-send). Commit style: `prints: <what and the numbers>`.
- **Verify via pdftotext, NEVER the image-read tool** (it serves stale frames — proven multiple times).
  PDF labels render letter-spaced (`W H AT I S H A P P E N I N G`) — strip whitespace + match lowercase.

## 3. Translation layers (the painfree resource for rewriting guides)

Per text in translation-work: `T1` word-gloss (term accuracy) · `L1/L2(+L2.v2)` plain prose
(accuracy base) · `SOURCE.txt` whole IAST · `L4-*.DRAFT.json` = crafted `lines` +
**`craft_notes`** (word-choice rationale) + `reads_against.argmap` (logic Q→A) + `c1_rasa`
(rasa tag) · `c1` essence+rasa · `argmap/` premises.
ST corpus: `/home/box/visuals/outputs/shivastotravali/shivastotravali_corpus.json`
(450 verses: iast + devanagari + Lakshmanjoo-witness EN — witness is copyrighted, write your own).

## 4. NEXT WORK (the brief, in order)

### A. Redesign the explainer page — ONE repeatable structure
Owner's mental model for each guide:
1. **What is it** — literal sense (was `logic`; rewrite FROM L2 prose + argmap; 2–3 plain sentences)
2. **How to perform it** — posture / breath / timing / count (was part of `howto`; source:
   VBT & Tantrasāra practice lines, the text's own instructions)
3. **How to know it's working** — NEW field `sign`: the sign/effect. Sources: the text's own
   claimed effects (Bahurūpa: 100/50/25 recitations; Swamiji's effects), c1 essence, rasa-tag,
   lore. Optional micro-line: **what to feel / visualise** (`feel`).
- Schema: `brief, logic, howto` → `brief, what, how, sign[, feel]` (old keys stay in stale.py).
- **Design it ONCE in bookkit engine** (single CSS block, labels "What is it · How to perform ·
  How to know it's working"), both books inherit. Page overflow is the risk: every spread must
  stay exactly 1+1 pages — re-run the §2 PDF check (guide count must stay 44/43).

### B. Quality pass over all writing (44 + 43 entries)
Per entry, from the layers: tighten `brief`; `what` from L2 (witness-verified — the 14-fix
precedent is in git log "witness-verification pass"); `how` concretised (counts, posture,
timing); `sign` new. Keep voice: lowercase prayer-English, "Feeling-tip:" fine.

### C. Fine-art postcard line (CONFIRMED: Prodigi fine-art postcard, both sides free)
- SKU `GLOBAL-POST-GLOS-6X4` (152×102mm, ~£0.40 print + ship, UK/EU/US) — classic postcard's
  back is postal-only (address/stamp/frank), fine-art is front+back free-form.
- Front = the type-filling prayer page; **back = the explainer (design ONCE)** — same content
  as guide page, re-laid to landscape card.
- Port `prints/print_template.py` + `render_brahmarpanam.py` (already had a POSTCARD4×6
  template!) to entries.json-driven: `render_postcards.py <book> [ids]` → PNG300dpi pairs.
- Then Etsy/Prodigi listing (wholesale math in `prints/EDITIONS.md`).

### D. Standing gates
- KDP: A5 custom trim 5.83×8.27, no bleed, white paper, matte cover, preflight PASS, <=110pp.
- KDP Select = NO (kills the Etsy PDF). Free ISBN first; own imprint later.
- Swamiji/Hughes material: quote briefly + attribute (© Hughes Family Trust), PDFs in sources/.
- Stale is for recycling, never deletion.

## 5. Quick file map
```
prints/EDITIONS.md          print spec, KDP research, type standard, prodigi options
prints/EMOTIONS-BOOK.md     Tantric Prayer research (navarasa, verse pools, taxonomy)
prints/kdp_preflight.py     the gate
prints/bookkit/engine.py    shared book builder
prints/stencils.py          SVG glyphs
prints/practical-prayers/INTRODUCTION.md   Swamiji intro compilation (keep appending)
prints/<book>/*-preview.pdf current PDFs (regenerate, don't hand-edit)
```

## 6. Decisions already made (do not relitigate)

- **Positioning:** Practical Prayers = the introduction to prayer (Lakshmanjoo's "what happens
  when you pray" register, beginner). Tantric Prayer = assumes well-versed, advanced, rasa-based.
  Registers must stay distinct in copy.
- PP's Negative section was cut (every prayer had an emotional twin in TP); the Sangha appendix
  (Aghora + Bahurūpa) moved from PP to TP as advanced material. Positive was replaced by
  **Gratitude**, plus **Alone** and **Flatness** added → 11×4=44=108pp.
- TP structure: navarasa9 (Nāṭyaśāstra, ninth śānta = Abhinavagupta's own) with three-layer
  naming on dividers: conventional term + literal MW gloss + sthāyin + doctrine line.
  Intro: "What is a rasa / The nine / How to use a doorway" + two axiom pages "Decoding the
  verses". PP also has two axiom pages (Śiva, Śakti, brahman, so'ham, pañcākṣara, anātha,
  anupāya, pratyabhijñā, svātantrya, pūjā, bhakti, māyā).
- TP translations were witness-verified (14 fixes — see commit "full witness-verification
  pass"); PP's44 still need the same treatment before print (same method: pull corpus EN,
  compare against ours, adjudicate Sanskrit).
- Titles: "Tantric Prayer — Thirty-Six Prayers for the Inner Weather" (TP meta) and PP
  "…for the moments of the day". Etsy e-book plan: £2.99 PDF, net ~£2.31. Keywords list for
  KDP lives in session (7 slots: swamiji / abhinavagupta-nondual / trika-practice / shiva-
  mantras-daily / prayers-sleep-anxiety / sanskrit-with-translation / beginner-hindu-meditation).

## 7. Servers, credentials, infra

- Static servers: prints → `127.0.0.1:8000` (http.server, dir /home/box/visuals/prints);
  outputs → `127.0.0.1:8600` (dir /home/box/visuals/outputs). Restart if dead:
  `setsid nohup python3 -m http.server 8000 --directory /home/box/visuals/prints & disown`
- Prodigi API key file: `/home/box/Documents/sec/prodigi` (test_ key works, sandbox only;
  live 401s). Sandbox base `https://api.sandbox.prodigi.com/v4.0`.
- Push script: `/tmp/opencode/push_visuals.sh` (recreate if missing — see §2).
- Hardware: 3GB RAM / 1 core / no GPU — background EVERYTHING long, `-j1`, never local ffmpeg
  (global AGENTS.md rules apply).

## 8. Known traps (cost us real time)

1. Image-read tool serves stale/wrong frames — verify renders with pdftotext only.
2. pdftotext letter-spaces text-transformed labels — strip whitespace, lowercase before matching.
3. Chrome print-to-pdf needs the Google-chrome-stable flags in §2 (plain `chromium` SIGTRAPs).
4. KDP flat tier ends at110pp — every new page must be budgeted.
5. `stale.py` list surgery: append INSIDE the brackets (a stray `]` broke it once).
6. L4/DRAFT "machine-proposed" content needs human/owner verdict notes before public print.
7. Don't pull translation-work without `git pull` first — texts land daily (gitarthasangraha,
   gold Tantrasāra āhṇikas, IPVV R2 all arrived during this work).
