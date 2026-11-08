# TRANSFER-VISUALS — the owner's vision, unpacked (2026-10-19)

## The vision (from owner, live)
One body on screen. The dying process STARTS (the binary 0/1 opening lands:
"actually the dying process is now starting"). Then — **five/six transfer
animations**: each tradition shows how "the transfer" happens IN THAT
TRADITION, each with its own animation, same body. Plus: use **deitybody code
as waves/shaders/fluid, not just phonemes** — the body is a living field,
and the transfer ripples through it.

## The five bodies (six stops — same body, six physics)

| Stop | Tradition | The transfer animation (what moves) | Assets we own |
|---|---|---|---|
| 1 | **Theravāda** | Nodes of the body flicker out MOMENT BY MOMENT (cognitive series), then one node pair hands over: cuti → paṭisandhi, same object — a single pulse jumps across a gap with NO gap in it. Body conventional-darkens; the pulse never stops. | element-fluid body: pulses through the fluid (staggered = momentary death; one pulse hand-off = relinking) |
| 2 | **Yogācāra** | Seeds light up under the skin (subliminal glow, granary-in-body), then the WHOLE seed-glow withdraws inward as the body cools — one package slides out carrying the lights. | shaders: FloatingParticles (seeds) + NoiseDissolve (withdrawal); element-fluid as cooling filter (hue → cold) |
| 3 | **Pure Land** | No transfer mechanic — instead: the deathbed lights UP. Body as receiver: a lotus-platform beam arrives from off-screen, warm light enters, the lotus closes on the light. The most beautiful stop = deliberately mechanic-less. | hyperframes type + lotus (new draw) + golden section; calm camera |
| 4 | **Madhyamaka** | Anti-animation: the body tries to outline "the moment" — a playhead sweeping the death timestamp — and the playhead keeps slipping (time can't be located); then the whole figure becomes designation-only (contour lines without fill). | shaders ContourLines (fill removed); the toddler's-why critique sits on this stop |
| 5 | **Tibetan** | THE full dissolve: earth ochre (body heavy/sags) → water white (throat dry) → fire red (warmth converges) → wind smoke (last breath wheeze) → red/white/black visions → GOLD luminosity flash → after-image body walks on as thin light-figure (mental body) → winds push it to a womb-door. 49-day mini-cycle inside the shot. | anatomy-generated exploded body + dissolution table (library/tibetan) + shaders NoiseDissolve + FlowField (winds) + gold flash |
| 6 | **Nāṇavīra/HH** | The cut: instead of anything moving — the animation REVERSES the premise: the body's "birth-nodes" were lit the whole time; nothing transferred because birth/death were never an event. Flash cut to the present: the body breathes, nodes already on. | element-fluid already flowing from frame 1 (retrospective); hard cut, no dissolve |

## Deitybody as the field (owner: "waves etc shaders fluid not just phenomes")
- `/root/deitybody` corpus + mālinī node data = the label/geometry source.
- Replace static nodes with a **wave body**: position nodes on the existing
  axis/flow paths, drive them with FlowField/CurlNoise — the body reads as
  standing waves (aggregates as interference patterns).
- Transfer = wave handed off between regions (Theravāda pulse), wave drained
  (Yogācāra), wave receiving (Pure Land), wave that can't be localized
  (Madhyamaka), wave cascading through elements (Tibetan), wave never left
  (HH). Six physics, one field language.


## BASE BODY — CORRECTION (owner 2026-10-19): NOT mātṛkā, THE ELEMENT FIELD
Mātṛkā = Śaiva letter-labels — wrong tradition on screen. The base shared
body is the **pañca-mahābhūta fluid**: a human silhouette whose interior is
a moving five-element field — earth(ochre, dense/slow) · water(silver, flow)
· fire(crimson, flicker) · wind(smoke-grey, drift) · space(void, stillness).
WHY this is the smart base: the five great elements are shared by EVERY stop
of the tour (Abhidhamma rūpa, the Tibetan dissolution, even science's
body-as-machine) — the base body IS the shared-ontology table made flesh.
- Construction: silhouette (hand SVG or anatomy figure outline) filled with
  shaders FlowField/CurlNoise color-mapped to the five palette stops; no
  text labels on the body ever.
- Every tradition then animates the SAME element-fluid differently:
  Theravāda = pulse through the fluid · Yogācāra = seeds drift out of the
  fluid · Pure Land = foreign light enters the fluid · Madhyamaka = contour
  of the fluid, fill denied · Tibetan = elements dissolve in their OWN order
  (native mapping, the money shot) · HH = the fluid never stopped.
- deitybody code stays: pipeline/knowledge source for wave/nyāsa mechanics
  AND the Abhinavagupta critique card in v2 — never the default body.

## The spin-off (parked)
**"The Tibetan Book of the Dead — animated"** = separate full video
(49-day bardo journey as a narrative film). Listed in TRILOGY future shelf.
NOTE: the Tibetan stop above is the 60–75s teaser version; the spin-off is
the whole Bardo Thödol with deities.

## Dying-process beat (owner's parenthetical notes → placement)
- "tibetans and their training to keep the body upright / tukdam" → at
  Tibetan stop (S13) — their practices ARE the animation's frame story.
- "levins bacteria thing coherance in body speculaion" → Levin coherence
  speculation. Science was cut from v1 — FLAG: owner's own note pulls it
  back slightly. Resolution options: (a) one card at Tibetan stop citing
  Levin's coherence thought as speculation, sourced, no numbers; (b) defer
  to Science-of-Rebirth video. DEFAULT: (a) minimal card — owner's words
  made the request; owner decides at review.

## Prototype spec (20s, first)
One body, Theravāda stop only: staggered node-off (6s) → cuti/patisandhi
pulse jump (4s) → body goes conventional-dark, pulse keeps beating (6s) →
black + "actually the dying process is now starting" (4s).
Stack: body SVG + CSS/JS timing in hyperframes composition. No engine write.

## Pipeline (all proven on this box)
body SVG/deitybody data → shader effects (gcomedy tools/shaders) →
composition with seek(t) (hyperframes or claude-motion-design film.html) →
probe stills → render (hyperframes render, ~30s/20s clip) → Fish word-
timestamps sync the six stops. No new engine. anatomy builds the Tibetan
exploded body only if the SVG field approach undersells — decide at prototype.
