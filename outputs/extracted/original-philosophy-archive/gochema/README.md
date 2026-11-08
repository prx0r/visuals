# gochema — The Geometry of the Companion

Essay-films on the daimon / tantra / recognition traditions, built with the
gcomedy essay→storyboard→render discipline and the tantra render stack.

## What this repo is

| Area | Dir | State |
|---|---|---|
| Essay-film bible | `series/` | Bible + pipeline + R2 map |
| Seed essay: daimon companion | `essays/daimon-companion/` | Imported from volume, audited |
| Volume manifest | `imports/VOLUME-MANIFEST.md` | What's on /mnt/data, what came in |
| R2 inventory | `imports/R2-INVENTORY.md` | Bucket prefix map (paths only) |
| R2 helper | `tools/r2.sh` | List/fetch via `/root/.r2-env` (never committed) |

## Method (from gcomedy)

One essay = `SOURCE.md` (verbatim) + `STORYBOARD.md` (shot table) +
`storyboard.json` (machine shots) + narration + alignment/integrity reports.
Gates before render: sentence-match PASS, per-shot drift <1s, no invented
citations (RO passages only).

## Credentials (never in repo)

- R2: `/root/.r2-env` (600, gitignored elsewhere) — see `series/R2.md`
- TTS: Fish (`FISH_AUDIO` in freaktown env) or Edge cache in `tts-cache/`

## Disk discipline

Binaries stay out of git: `*.mp4 *.wav *.png`, `scenes/`, per-shot audio.
Repo holds text + manifests + scripts. Media lives on volume (`/mnt/data`)
and R2 (`renders/`).
