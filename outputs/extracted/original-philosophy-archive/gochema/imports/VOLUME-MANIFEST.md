# VOLUME MANIFEST — /mnt/data (attached volume)

> Inventoried 2026-10-19. 8,030 files, 217MB.

## Tree

```
tantra_animation_packs/
  selected_expansion_essays/
    content/publishing/renders/
      zeus-test-1/v1/        — full build (see below)
      zeus-test-direct/v1/   — full build, essay+storyboard IDENTICAL to zeus-test-1
```

## Per-build contents (v1)

`source_essay.md` (1,449w) · `storyboard.json` (102 shots) ·
`narration_script.txt` · per-shot `sNNN.wav` + `full_audio.wav` ·
`scenes/sNNN/*.png` (6fps frames) + per-scene mp4s · `draft.mp4` ·
`final.mp4` · `render_*.py` · `alignment_report.json` ·
`script_integrity.json` · `audio.txt` + `concat.txt` manifests.

## Import policy

- IN REPO (`essays/daimon-companion/`): all text/JSON/scripts (10 files).
- REFERENCED ONLY: `*.mp4 *.wav *.png`, `scenes/` (binaries, gitignored).
- Canonical: `zeus-test-1` (variant difference with `-direct` unconfirmed).

## Also on this box (not imported, noted)

- `/mnt/HC_Volume_106959365/` — old system disk (coolify data, skia-framework
  sources, 4 mock mp4s in outputs/). Revisit only if skia sources needed.
- `/mnt/data` holds ONLY the tantra packs above. The other ~120 essay packs
  live on R2 (`imports/R2-INVENTORY.md`), not on any attached volume.
