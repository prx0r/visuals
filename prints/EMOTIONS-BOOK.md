# TANTRIC PRAYER — research spec (Prayers for Emotions)

*2026-11-05. Companion volume to Practical Prayers: PP = the moments of the day (situations);
this book = the weather of the feelings (rasas as doorways). Publish both together on KDP/Etsy.*

---

## 1. The thesis — three pillars, all already derived in-house

**Pillar A — Every emotion is a particular camatkāra of consciousness.**
- TĀ 15254: "The mental fluctuations of anger and the like exist because they are one with
  the wonder (that is the experience of consciousness)."
- TĀ (ad 1/53): camatkāra is the primary characteristic of consciousness itself; perception
  *is* camatkāra (TĀ 1260–1268).
- ⇒ Anxiety, grief, excitement are not intrusions into practice — they are consciousness
  already in a particular flavour. **The door is the emotion; no transmutation from scratch.**
- Source file: `gochema/library/recognition/pushing-tantraloka/RASA-AND-SANTA-derivation.md`
  (four-link mechanism, complete).

**Pillar B — All rasas are essentially pleasurable, even the painful ones.**
- Abhinavabhāratī I, 291–92: "All rasas are essentially pleasurable. Even the painful
  emotions of anger, fear, sorrow and disgust… when contemplated in their idealised form…
  yield pure joy." And: emotions "only lend variety to the enjoyment of this bliss."
- Tantrāloka 25585–94: "The nature of suffering is, essentially, a particular kind of
  wonder (camatkriyā)."
- ⇒ Depression isn't the absence of the doorway; it's the door in karuṇā-plate. The prayer
  doesn't kill the feeling — it converts felt-AT to savoured-AS (sādhāraṇīkaraṇa), which is
  recognition wearing that emotion's face.
- Source: `LOGICVID-session-suffering-as-rasa.md` (TĀ + A.Bh quotes with page refs).

**Pillar C — The obstacle is the way (the Tantra of the blockage).**
- Vijñāna Bhairava **v.127**: "Whatever unknowable, whatever ungraspable, whatever void,
  whatever gone to nonbeing — **that all as Bhairava to be contemplated** — at that end,
  awakening." (vbt-p13)
- VBT v.33: wherever thought goes — void, wall, supreme — enter there.
- VBT v.130: "**By fear all makes resound**" — fear literally resounds as Bhairava's word.
- Aghora door (Swamiji): anxiety is ghoratarī's down-pull; aghorā reverses it instantly
  (Tantrāloka 3.257-9 teaching, `sources/efficacy-aghora.pdf`).
- Fear's rope-snake (A.Bh I, 3599–603): fear is REAL even when its object is a rope —
  so the realness of the feeling is the thing to use, not the object to fix.
- `LOGICVID-session-fear-love-recoil.md`, `rasa-alaukika-felt.md` (rasa is felt yet
  beyond time/space — the "transmutation" is objectify → savour → the alaukika flicker).

## 2. Structure — eight doorways (proposal)

Each section = theory opener (the specific doctrine for THAT feeling) + 4–5 prayer spreads
(type-filling page + guide, same engine as Practical Prayers) + how-to: objectify → savour
→ recognition.

| # | Doorway | Rasa / sthāyin | Theory hook | Verse pool (real corpus hits) |
|---|---|---|---|---|
| I | **Fear / Anxiety** | bhayānaka / bhaya | rope-snake; aghora door; v.130 "by fear all resounds" | ŚSt fear: 1.12, 3.2, 8.9, 9.6, 9.18, 11.8, 12.8, 13.16 · VBT 118, 130 · Bhairavastava 4/5 (PP pool) |
| II | **Grief / Depression** | karuṇā / śoka | "suffering is a kind of wonder"; even karuṇā is joy | ŚSt grief: **44 hits** (1.10, 1.26, 2.4, 4.20, 5.3, 6.3, 6.11, 11.4…) · Anuttarāṣṭikā 4 (burden-lowering) · Bhairavastava colophon (instantly quenches) · Paramārthasāra 31 (address error) |
| III | **Anger** | raudra / krodha | emotion as camatkāra; not suppressed but re-timed | ŚSt: 5.18, 7.2, 13.11, 16.15, 16.16, 17.47 · Pañcaślokī 3 (reproach) · ŚSt 20.18 (destruction as līlā) · VBT 101 (the emotion-list) |
| IV | **Desire / Longing** | śṛṅgāra / rāga | eat the desire; desire as variety of bliss | ŚSt: **105 hits** (1.11, 1.17, 1.19, 3.5, 4.2…) · **VBT 96–98** (desire dissolves where it arose) · ŚSt 15.2 (devouring māyā) · MPA 8 (stale pool) |
| V | **Excitement / Joy** | hasya/utsāha | don't damp — liturgize (variety of bliss) | ŚSt: **31 hits** (1.6, 1.9, 1.18, 2.22, 3.6…) · ŚSt 1.5 (mad with nectar), 17.1 (festival), 20.8 (itch) · VBT 71 (magnify the bliss) |
| VI | **Loneliness / Abandonment** | anātha | refuge OF the refugeless; anātha as name of Śiva | ŚSt: 2.17, 4.23, 5.3, 14.3, 19.8, 20.1… (11) · Bhairavastava 1 · Pañcaślokī 5 (the plea) |
| VII | **Doubt / Restlessness** | vikalpa | doubt = door: "that all as Bhairava" (v.127) | VBT 127, 33 · Pañcaślokī 4 (cloud lifts) · Anuttarāṣṭikā 1 (no method) · ŚSt 16.8 (api-chain) |
| VIII | **Flatness / Boredom** | śūnya / ālasya | void-dhāraṇā: the blank IS the page | VBT 33, 103, 127 · VBT 74 (contentment-hold) · ŚSt 16.1 (the census) |

**Verse-selection tooling (built when we build):**
1. Emotion-keyword grep on `shivastotravali_corpus.json` (counts above — done).
2. **L4 `c1_rasa` filter — 988 tagged verses**: e.g. tag-hunt for
   "adbhuta strained toward bhayānaka" (fear), "raudra of devouring fire" (anger),
   "vīra of uprooted fears", "śānta with vīra". A 20-line selector script gives us
   rasa-exact verse picks per section.
3. VBT emotion dhāraṇās: 96–98 (desire), 101 (lust/anger/greed/delusion/pride/envy),
   103 (neither pain nor joy), 118 (fear/grief/abyss), 127 (all as Bhairava), 130 (fear
   resounds), 136 (senses + pleasure/pain).
4. **`stale.py` in practical-prayers is a free verse pool** for this book (svab-3, param-31,
   anu-1, mpa-12… were cut from PP for redundancy, not weakness).

## 3. The "theory of tantra" chapter (the opener essays)

1. **What a feeling is** (Pillar A): emotion = particular camatkāra; four-link mechanism
   from RASA-AND-SANTA (camatkāra = signature of consciousness → perception is camatkāra →
   emotion is particular camatkāra → registers: cognition / bliss / wonder).
2. **Why even the painful ones work** (Pillar B): alaukika-felt paradox + sādhāraṇīkaraṇa;
   felt-AT → savoured-AS → recognition.
3. **The obstacle technique** (Pillar C): enter where it is (VBT 33/127); the Aghora
   reversal (aghorā / ghorā / ghoratarī); rope-snake: use the realness, skip the object.
4. **How to use a doorway** (method page): NAMING (objectify the feeling) → STAYING
   (savour its texture1 breath) → RECOGNIZING (whose camatkāra is this?) → the verse as
   the re-tasting instrument.

All quotes in sessions carry page refs (Tantrāloka Vol 2, A.Bh I) — **verify against print
editions before publishing** (house rule: sessions are machine-consolidated).

## 4. Titles

- **Tantric Prayer: The Doorways of Feeling** ← favourite (user's "Tantric Prayer" + clear)
- Tantric Prayer: Using the Obstacle as the Way (the theory-forward variant)
- Prayers for Every Feeling: Kashmir Shaivism's Rasa Doorways (search-forward variant)
- Pair positioning: *Practical Prayers* = outer day / *Tantric Prayer* = inner weather;
  same cover system, shared back-cover cross-sell.

## 5. Build & publish plan (both at once)

1. Selector script (corpus rasa + emotion grep) → verse picks per doorway.
2. Reuse the Practical Prayers engine: sections = doorways, prayer + guide spreads, guide
   adds "Why this feeling is already the door" (theory) + how-to (objectify → savour).
3. Intro: the three pillars (from §3, quoted short + attributed).
4. KDP: same default format (A5 custom / or whatever we settle after PP's draft feedback),
   `kdp_preflight.py` gate, same keyword strategy + `rasa`, `camatkara`,
   `emotional healing meditation`, `tanic traditions`…
5. Ship: KDP paperback ×2 same week, Etsy PDF pair (bundle discount later), shared cover DNA.

## 6. Source stack (all on-box)

- Theory: `pushing-tantraloka/RASA-AND-SANTA-derivation.md`, `suffering-as-rasa`,
  `fear-love-recoil`, `rasa-alaukika-felt`, `rasa-santa`, `suffering-santa-reset`,
  `mothers-grief-honest` (gochema library)
- Essays: `ipvv/site/data/essays/ESSAY-RASA-IPVV-ABHINAVABHARATI.md`,
  `ESSAY-WHY-RECOGNITION-IS-FELT.md` · transcripts `rasa-abhinava.md`
- Corpus: L4 rasa tags (988), ŚSt emotion counts, VBT L2 p10–p14, stale.py pool
- Primary: Tantrāloka + Abhinavabhāratī (quoted in sessions — verify refs), VBT, ŚSt
- Swamiji: Aghora three-energies (sources/efficacy-aghora.pdf) — the anxiety doorway's
  opening move

*Next action when green-lit: run the selector, lock the 8×4 verse table, then build.*
