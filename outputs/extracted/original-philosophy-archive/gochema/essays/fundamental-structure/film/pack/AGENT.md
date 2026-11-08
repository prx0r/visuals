# Rendering Agent Guide

## Install

Extract this pack over the repository root.

```bash
cd MOTHERFUCKER
node ../tools/apply-pack.mjs
node ../tools/validate.mjs ..
```

## Audio

Generate each entry in `narration.json` separately.

Measure actual durations with `ffprobe`, then run:

```bash
python3 ../tools/compile-timed-pack.py ..
```

For exact source narration, replace the concise scene narration with selected
passages from `SOURCE-DYNAMIC.txt` and the supplied Static Aspect source. Do not
change the proof-state order.

## Contact sheets

Render at:

```text
0.08
0.28
0.55
0.82
0.96
```

Review Static and Dynamic sections separately before rendering the whole film.

## Required checks

- `o`, `x`, `T`, frame, and weight retain stable meanings.
- Spatial placement is never the sole distinction.
- All three tetrad interchanges are readable.
- 4-member and 16-member structures share one grammar.
- Dynamic replacement is irreversible.
- Weight diagrams preserve unity.
- The final scene is explicitly unfinished.
