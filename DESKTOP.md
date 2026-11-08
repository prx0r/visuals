# THE PATALA DESKTOP — operator manual (v1, 2026-10-27)

> Creating a Baumer visual/movie? → **`CREATING.md`** (the flow) · engine steps → `essay-visual-engine/docs/OPERATOR.md`

This box (hub) is a desktop for **coding with agents, seeing outputs, and fanning work
out to our VPSes**. Light on purpose: VS Code desktop measured 752 MB / 82% CPU here and
was rejected; the stack below idles at ~1–2% CPU.

## The pieces

| piece | what | where / how |
|---|---|---|
| **IDE** | VS Code core in a browser (code-server), no electron | Falkon → `http://127.0.0.1:8080` · systemd `code-server@box` (auto-starts) · **auto-opens `~/visuals`** (302 deep-link) · no password (localhost only) |
| **Chat panel** | OpenCode extension v2 sidebar (sessions, models, tools) | opens by default; shortcut hint `Ctrl+Alt+I` · ⚠ default provider = **Copilot sign-in** → use **Models** picker, or just use the terminal `opencode` (your configured brain) |
| **Terminal** | integrated bash as user `box` | `Ctrl+\`` — prompt `box@debian11:~/visuals$` |
| **Media viewing** | images + mp4 INSIDE the IDE | click a `.png/.jpg` → **Image Preview** tab · click `.mp4/.mov` → **Video Player (with Audio)** tab (ext `yutabee.unmute-video`: play, loop, A/B, speed, fullscreen) · workspace trust **disabled server-side** so audio works |
| **Git** | Source Control panel + history graph | `Ctrl+Shift+G` — see screenshot below · commit from the panel |
| **opencode TUI** | the real coding sessions (kitty) | `opencode` in a terminal; sessions for other boxes via `opencode1/2/3` |
| **Dispatch** | fan CPU jobs to the fleet | see *Dispatch* below + agent skill **`parallel-dispatch`** (auto-loaded by any session) |
| **Render-landed ping** | notify when a render finishes | `notify-send "render" "done: $FILE"` (Outbox viewer was retired — viewing lives in the IDE now) |

## Feature cheatsheet

| action | key |
|---|---|
| quick open file | `Ctrl+P` (type part of name, Enter) |
| command palette | `Ctrl+Shift+P` |
| terminal | `Ctrl+\`` |
| chat panel | `Ctrl+Alt+I` (or opens by default) |
| source control | `Ctrl+Shift+G` |
| view an output | click it in the Explorer tree |

## Dispatch — `opencode1 / opencode2 / opencode3`

The owner's names (scripts in `/usr/local/bin/`):

| name | box | reach (non-interactive) | cpu / free ram | disk |
|---|---|---|---|---|
| **opencode1** | debz, Hetzner | `ssh -o BatchMode=yes hetzner` (root, key) | 4c / 4.5G | 97% ⚠ |
| **opencode2** | server2 | `sshpass -p '…' ssh root@2.28.50.109` (password auth) | 4c / 3.4G | **98% ⚠⚠** |
| **opencode3** | old OVH | `ssh -o BatchMode=yes vps` (ubuntu, key) | **6c / 7.8G** | 96% ⚠ |
| **work volume** | HC_Volume on opencode2 | `sshpass -p 'xx' ssh root@2.28.50.109` → `/mnt/HC_Volume_106427611/patala/` | ext4, **59G (56G free)** | 1% ✓ |

**STORAGE LAW (owner, 2026-10-31): bulk work lives on the volume.** All renders, takes,
stills, archives land in `/mnt/HC_Volume_106427611/patala/{audio,renders,archive,docs,tests,backup}`
(written directly by fleet jobs on opencode2; hub pushes audio via the sshpass hop and keeps
only hot serving copies in `~/visuals/outputs/`). The three box disks sit at 95–98% — new
render dispatch scripts MUST output to the volume path, not box-local disk.
**Full note + file lists + moved-from table: `patala/docs/VOLUME.md` on the volume**
(regenerable listing: `find . -type f` there; checksums in `patala/archive/LEDGER-<date>.md5`;
breadcrumb where bulk left the hub: `~/Downloads/MOVED.md`).
Access from hub: `sshpass -p xx ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@2.28.50.109`
· opencode3 pushes its `publish_r2.sh` third target to `patala/backup/` (key generated, owner adds).
Job scripts (persistent): `~/visuals/ops/{store_work,shift_to_volume}.sh` (logs `/tmp/opencode/`, notify).

Proven 2026-10-27: **3 units dispatched simultaneously → wall clock 5 s** (437/458/443 ms).

### The dashboard — dagu (browser) — NEW 2026-10-29

| what | where |
|---|---|
| **web UI (run/monitor DAGs, step logs, history)** | **http://127.0.0.1:8090** (Falkon) — 127.0.0.1 only; port avoids 8080 code-server / 7800 quill / 18787 deploy |
| server process | `dagu start-all --host 127.0.0.1 --port 8090` (setsid nohup, log `/tmp/opencode/dagu_server.log`) |
| DAG files | `/root/.config/dagu/dags/` — `fleet-ping.yaml` (smoke), `scene-render.yaml` (ship → wait → collect+notify) |
| install log | `/tmp/opencode/install_dagu.log` — single Go binary, no docker, file state (hub stays light) |
| outputs land | `~/visuals/experiments/` → click in the IDE (8080) to play |
| desktop pings | `notify-send` on collect success and on remote failure |

**Under the hood (scene-render DAG):** `ship-and-launch` (scp `bootstrap.sh` → vps, `setsid nohup`
remote) → remote `~/job_scene/`: always `tar xzf` the bundle → `pip --user indic-transliteration` →
env-rooted `python3 scene.py render` (PIL frames → ffmpeg `-threads 2`, niced) →
`wait-for-render` (poll `vps:~/job_scene/run.log` every 15s, pgrep uses the `[s]cene` bracket trick)
→ `collect-and-notify` (scp mp4 → `experiments/`, chown box, `notify-send`).

One-off dispatchers using the same pattern (NEVER BLOCK protocol, root AGENTS.md):
`/tmp/opencode/dispatch_scene_v{1..4}.sh` + `bootstrap.sh`, logs alongside them.

### Lessons — the bugs this system was built over (postmortem 2026-10-29)

| # | mistake | fix (now load-bearing) |
|---|---|---|
| 1 | long ops run synchronously inside a tool call → tool kills at ~2 min, chained `&& verify` dies too | **NEVER BLOCK protocol** — root `AGENTS.md`; job scripts own lifecycle + notify |
| 2 | remote bootstrap forgot to `tar xzf` the bundle → `scene.py not found` | bootstrap always extracts first |
| 3 | extract guard `[ -f scene.py ] \|\| tar` → stale code ran after bundle updates | always extract (idempotent overwrite) |
| 4 | watcher `pgrep -f "scene.py render"` matched its own cmdline → blind to failures | bracket trick `pgrep -f "[s]cene.py render"` (same for pkill / any self-referential pattern) |
| 5 | `ve/glosscard.py` rendered 6 demo cards **at import** with hardcoded `/root/.fonts/` → died on remote | env roots (`FONTS_DIR`/`GLOSSCARD_OUT`), demos under `__main__`, lazy makedirs — import side-effect-free |
| 6 | `pkill -f` pattern matched my own shell → killed the tool call mid-run | kill by PID (Global Rules #7), bracket all patterns |
| 7 | `timeout 240 scp && md5` → transfer truncated, verify never ran | upload lives in the job script with md5-retry loop |

Rules (all in the skill, repeated here because they're load-bearing):
1. **Probe first**: load / free / `df` on the target; all three disks are nearly full —
   outputs are tiny, **temp is not**: pipe frames into ffmpeg stdin, never frame dumps.
2. **Detached + logged**: `setsid nohup bash -c '… 2>&1 | tee /tmp/opencode/job.log' &`
3. **Collect back** with `scp` to `~/visuals/experiments/`.
4. opencode3 (idle 6-core) = preferred render target.

## Hub services (all green 2026-10-27)

| service | addr | status |
|---|---|---|
| code-server IDE | `127.0.0.1:8080` | systemd active |
| quill bridge (gallery, ask-qwen) | `127.0.0.1:7800` | active, /gallery 200 |
| deploy bridge (auth-free proxy) | `127.0.0.1:18787` | active, /health 200 |
| yt-dlp | binary | `2026.08.19` · cookies: `/home/box/Downloads/cookies.txt` |

## Ops rules of this desktop

- **Hub stays light**: heavy/parallel compute goes to opencode1/2/3, not here.
- **Eyes before ship**: renders go through qwen review (gallery/`/api/qwen` or the loop) before the owner sees "done".
- **Renders on the owner's word** (iteration stills-only while looping).
- Git panel ownership: big root-run renders re-create root-owned files →
  `sudo chown -R box:box /home/box/visuals` restores the Git panel.
- Falkon = the browser for the IDE (Firefox/Chrome rejected on RAM). Close it when idle.

## Test log — every feature exercised headless (playwright),2026-10-27

| # | feature | result | evidence |
|---|---|---|---|
| 1 | IDE loads, deep-links folder | ✅ title `visuals - code-server` | docs/screenshots/t1_workbench.png |
| 2 | image preview inline | ✅ | docs/screenshots/t3_image.png |
| 3 | mp4 player in tab (0:10, audio ungated) | ✅ | docs/screenshots/t5_video.png |
| 4 | chat panel opens, input accepts, pipeline runs | ✅ (default = Copilot sign-in → switch model) | f4 |
| 5 | integrated terminal | ✅ bash prompt | f1/f3 |
| 6 | editor/monaco typing | ✅ | f2 |
| 7 | git: changes (8), commit UI, history graph | ✅ after chown | docs/screenshots/f5_git2.png |
| 8 | 3-way parallel dispatch (opencode1/2/3) | ✅ wall 5 s | this doc |
| 9 | bridges + services + yt-dlp/cookies/notify-send | ✅ | above table |
| 10 | Outbox retirement → RAM recovered | ✅ ~1.5–2.1 G free | — |

## Troubleshooting

- **IDE won't load** → `systemctl status code-server@box` · restart: `systemctl restart code-server@box`
- **Chat panel asks to sign in to Copilot** → it's the ext default; pick your provider in **Models**, or ignore and use terminal `opencode` (all keys/rules live there).
- **Git panel says "unsafe repositories"** → files owned by root; run the chown above.
- **A VPS job fails instantly** → probe disk first (all 96–98% full); `ssh … 'df -h / | tail -1'`.
- **spyagent (tor) unreachable** → not part of opencode1/2/3; check `nc -x 127.0.0.1:9050` path before use.
