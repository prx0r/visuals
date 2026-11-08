# Notes 2026-11-05 — yantra borders + prayer-book visuals (for the next agent)

## What landed (uncommitted — repo has unborn HEAD, do not commit without owner)

- `prints/templates/bhupura-border.svg` — bhūpura gate stencil, traced 1:1
  from the PD Sri Yantra diagrammatic SVG
  (`/root/sleepdraw/assets/refs-yantra/The_Sri_Yantra_in_diagrammatic_form.svg`,
  author-released worldwide PD). 2×36-point gate polygons, stroke #17140F
  (house ink), no fill. Zero invention: pure trace + uniform scale.
- `prints/templates/BORDER-NOTE.md` — provenance + use rule.
- Proof: `/tmp/brahmarpanam-bordered2.png` (NOT in repo — regenerate anytime).
- Met CC0 Ekamukhalinga photo + CC BY-SA yantra SVGs (Bhairavi, Kali, Trident
  of Parama Siva) live in `/root/sleepdraw/assets/refs-yantra/` with
  `LICENSES.md`. PD diagrammatic SVG there too.

## How the proof was made (reproducible)

1. Fonts: engine hardcodes `/root/.fonts/`; box lacked Tiro + Cormorant.
   Fixed with repo-bundled copies (env only):
   `cp prints/anthology/fonts/{TiroDevanagariSanskrit-Regular.ttf,'CormorantGaramond[wght].ttf'} /root/.fonts/`
2. Render: `python3 prints/prayer_engine.py prints/prayers/brahmarpanam.json`
   → `outputs/print_products/brahmarpanam/*_1200x1800.png` (also uncommitted, regenerable).
3. Border: stencil viewBox 516.316×515.691 scaled to 1200×1800 minus 64px
   margins, PIL polyline width 6; type block uniformly scaled to fit inside
   (house ratios preserved). v1 full-bleed collided with type — v2 insets,
   gates clear all type (same rule as video safe zone).

## Theory constraint (owner directive — do not freestyle)

- Practical prayers (food/sleep/japa/equanimity): bordered postcard only,
  or act-vignettes. No yantra except mālā for japa (the practice's own tool).
- Tantric prayers: one geometry each, verse-anchored. Canonical so far:
  mirror = recognition (Become-Śiva). Everything else waits on the bought
  books (Adyar Varivasyarahasya INR 300 in stock; Exotic India Setubandha
  vol $41–55), NOT imagination.
- Spine: bahiryāga→antaryāga — every yantra plate ships with its
  gaze-then-close-eyes instruction or it is decor and gets cut.
- Geometry grammar (conservative): bhūpura = earth/stability (borders),
  lotus = unfolding, triangles = Śiva-Śakti interplay, bindu = rest.
  Etch direction out-from-center then pratisaṃcara return (TĀ-a28).

## Open (yours)

1. Batch-border all 8 prayer postcards (script the §How loop).
2. Bhūpura as video-thumbnail frame (same stencil, both media).
3. Mala stencil from Met refs; mirror/knot/sun/jar/door/sea per bank queue
   (`videofactory/core/art_bank/REGISTRY.json`, 46 entries).
4. Yantra plates per tantric prayer once books land (mantra→avaraṇa
   mapping needs Dipika/Setubandha text, not guesses).
5. Met CC0 pull: 17 more Kashmiri hits queued (object 38246 proven pattern).
   Smithsonian CC0 needs a free API key signup (owner action).
6. Full art-pipeline runbook: `videofactory/docs/ART-PIPELINE.md`.
   Seal craft: `translation-work/paramarthasara/P1-SONG04-SEAL.md`
   (spider exemplar) + P1-INDEX (37 seals).
