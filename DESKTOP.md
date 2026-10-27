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

Proven 2026-10-27: **3 units dispatched simultaneously → wall clock 5 s** (437/458/443 ms).

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
