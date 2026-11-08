# Series bible — gochema essay-films

> Same discipline as gcomedy, different subject. Each film: the best version
> of one idea from the recognition traditions, taken apart next to the sources.
> Narration carries the idea; overlays carry the evidence (RO passage tags,
> never bare assertions). Music and ritual are presented as technologies,
> never as vibes.

## The template (one folder per essay)

```
essays/<slug>/
  SOURCE.md            — verbatim source essay (immutable import)
  STORYBOARD.md         — shot table grouped by chapter (generated from json)
  storyboard.json       — machine shots: id/start/end/duration/spoken/visual
  narration_script.txt  — exact TTS input
  alignment_report.json — per-shot expected-vs-actual drift
  script_integrity.json — source-vs-spoken sentence match
  render_<slug>.py      — PIL renderer (paths retargeted per box)
  ANALYSIS.md           — audit: counts, gates, fix list
  ESSAY.md              — gcomedy-style beat adaptation (when commissioned)
```

## Rhythm law

- Chapters, not beats: I–VII style arcs, ~60–125s per chapter.
- One visual mode per shot (61-mode library: stone_eye, serpent_coil, …).
  Motif-preserving dissolve or motion handoff between shots; hard cuts only
  on chapter breaks.
- No full narration captions; technical terms only.
- Palette: VOID (13,17,23) / GOLD (212,165,116) / CRIMSON (141,44,57) /
  LAPIS (42,70,110) / INK (230,225,220).

## Citation law

Every quoted claim keeps its RO tag (`ro-daimon-guidance, p_002`) in SOURCE
and on its overlay card. Narration may paraphrase; cards carry the tag.
Untagged claims fail the gate.
