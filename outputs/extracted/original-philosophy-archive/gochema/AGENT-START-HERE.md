# AGENT START HERE

```bash
git clone https://github.com/prx0r/gochema.git && cd gochema
bash tools/r2.sh ls renders/   # needs /root/.r2-env on the box
```

Read in order: `README.md` → `series/README.md` (the bible) →
`series/BUILD-PIPELINE.md` → `essays/daimon-companion/ANALYSIS.md`.

## What you get
- `essays/daimon-companion/` — source essay (1,449w), 102-shot storyboard
  (638.6s), narration, alignment + integrity reports from the volume build.
- `imports/` — volume manifest + R2 bucket map. Media referenced by path,
  never vendored.

## Rules
Additive changes only. No binaries in git. No creds in repo. No invented
citations — every quote carries its RO passage tag.

## Compiler law (owner, 2026-10-19 — binding on every essay)
The agent is a COMPILER, not an author. For gochema videos:
- Narration voice = source material, verbatim where possible (damned readout
  discipline). Cutting to length yes; rewriting, compressing in own words, or
  "arguing" — never.
- Theories/arguments come from the teachers in their own words: quotes + clips
  (Wallace, Upton, Analayo, the texts). Our narrator bridges, never paraphrases
  a position the teacher could say themselves.
- Existing offender: `essays/rebirth-explained/script.md` was written in my
  words — flagged as DRAFT-SOURCE-MAP only. Convert to quote-and-clip
  compilation before any synth.
