# VISUAL SPEC — Buddhist Reincarnation v1 (the vision, in buildable form)

## 0. One-line visual thesis
A single **element-fluid body** on black; every tradition is a different
*behavior* of the same fluid; the camera never leaves the body.

## 1. The base body (shared across all stops)
- Silhouette: simple, front-facing, no face, no labels — outline from
  anatomy figure or hand path. Stroke: ink `#f3f1ec` 1.5px, no fill.
- Interior: live fluid — FlowField/CurlNoise particle drift, color-mapped to
  five elements: earth ochre `#c9a45c` slow/dense · water silver `#cfd8e3`
  flow · fire crimson `#e8102e` flicker · wind smoke-grey `#8d8b93` drift ·
  space void `#07070a` stillness. (Palette = gochema VOID/GOLD/CRIMSON/LAPIS
  + two neutrals — consistent with fire-simile film.)
- Rule: **no text ever on the body.** Cards carry all language.

## 2. The six transfer animations (per stop, 30–75s each)
| Stop | Fluid behavior | Signature moment | Camera |
|---|---|---|---|
| 1 Theravāda | staggered node-darkening as *dimmings in the fluid* (momentary death), then ONE pulse hand-off across nothing (cuti→paṭisandhi) | the pulse that jumps without a gap | slow push-in, hold on the jump |
| 2 Yogācāra | bright seed-particles assemble under the skin, then drain inward as hue cools | the withdrawal: one package exits as body goes cold-blue | pull back as seeds leave |
| 3 Pure Land | fluid calm; foreign gold light enters from off-screen; lotus closes around it | no mechanic — arrival | static, warmest frame of the film |
| 4 Madhyamaka | playhead sweeps trying to find the moment, slips; fluid loses fill → contour-only | denial of the fill (the toddler's-why card lands) | slight orbit — the body can't be pinned |
| 5 Tibetan | elements dissolve in canonical order with their external signs (heavy→dry→wheeze→red→white→black) → **gold luminosity flash** → thin light-figure walks off; winds (FlowField) carry it to a womb-door | the flash (700ms, screen-wide) | the one long take: dissolve front-to-back |
| 6 HH | everything already flowing from frame 1; animation *reverses* — no dissolve ever happened; breath loop runs | hard cut on "birth is present" | cut to close, no dolly |

## 3. Frame language (the tour's connective tissue)
- Cold open (binary 0/1): hard cut, one shot — a body-silhouette snapping to
  a flat 0/1 glyph, then back to body as "dying process starts."
- WHO segment: kinetic type only (words ARE the picture) — the sentence
  "the determination of death is the final event" types and *the last word
  freezes*, then the body appears behind it.
- Three-deaths card: three small body glyphs in a row, each pulsing at a
  different rate (every-moment / at-the-end / arahant = still).
- Between stops: fluid ripple wipe (same field, no hard cuts except HH).
- FAQ: cards on black (ugly-truth treatment — no body).
- Cliffhanger: body close-up, nodes of birth *retrospectively lit*, hold,
  cut to black on the last clause.

## 4. Typography & overlays
- Anton titles / Inter Tight body (gochema grammar). Gold = measurements
  and citations only. Pali in quoted serif, never in narration.
- Death-moment cards format: `moment of death: <definition> — <cite>`.

## 5. Motion laws (from the GCOMEDY lock + film-structure doc)
- Dissolves ONLY for ontological transitions (the Tibetan stop). Hard cuts
  for jokes, cards, jokes. Never a dissolve on a punchline-equivalent.
- One long take per video max (Tibetan stop claims it).
- Beat changes on music-bar if a bed exists (TBD: bed = silent or drone?).

## 6. Build order (20s → film)
1. PROTOTYPE: Theravāda stop only (spec in TRANSFER-VISUALS) — SVG + JS timing.
2. Element-fluid pass on the prototype (shader in).
3. Tibetan dissolve (money shot) + gold flash.
4. Remaining four stops on the same body.
5. Typography/frames pass (WHO, cards, FAQ, cliff).
6. Sync: Fish word-timestamps → stop boundaries.
Stack: hyperframes (or film.html) + gcomedy tools/shaders. No new engine.
anatomy generator ONLY if silhouette hand-drawing undersells.
