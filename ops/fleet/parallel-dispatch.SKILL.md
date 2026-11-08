---
name: parallel-dispatch
description: Fan CPU work across our boxes — split a job set, capacity-check each host (load/RAM/disk), dispatch over ssh detached, pipe renders to ffmpeg stdin (no frame dumps), poll logs, collect outputs. Use whenever a task could run on more than one machine, or when this box is loaded and debz/other VPS could take the work: renders, ffmpeg, transcodes, batch analysis, atlas generation, long python jobs.
---

# parallel-dispatch — our boxes as one machine

## The fleet (as of 2026-10) — canonical names: **opencode1/2/3**

The owner types `opencode1|2|3` (from `/usr/local/bin/`) — identify boxes by THESE names:

| name | how to reach (non-interactive) | cpu/ram | disk | watch-outs |
|---|---|---|---|---|
| **opencode1** (debz, Hetzner) | `ssh -o BatchMode=yes hetzner` (root, key `vps_ed25519`) | 4c / ~4.5G free | **97% (2.8G)** | docker ✓; load ~1-3 |
| **opencode2** (server2) | `sshpass -p 'xx' ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@2.28.50.109` | 4c / ~3.4G free | **98% (1.5G!)** | tightest disk — stdin-pipe only, never frame dumps |
| **opencode3** (old OVH) | `ssh -o BatchMode=yes vps` (ubuntu, key `vps_ed25519`) | 6c / ~7.8G free | 96% (4.6G) | fastest idle box (load ~1), best render target |
| local hub | — | 4c / ~2G free | 89% | **yt-dlp + cookies + bridges + code-server live here** — keep light; small/serial only |
| spyagent (tor) | `ssh spyagent` (nc via 127.0.0.1:9050) | ? | ? | separate from opencode1/2/3; onion — probe before use, was unreachable 2026-10 |

Proven 2026-10-27: 3-way simultaneous dispatch (1 unit each, dd150MB) → wall 5s, units 437/458/443ms, all exit 0.

## Rules (learned the hard way)

1. **Capacity before dispatch**: `ssh hetzner 'uptime; free -m | sed -n 2p; df -h / | tail -1'` + local `uptime; free -m`. Skip a host if load>6 or free<500M or temp wouldn't fit.
2. **Never dump frame PNGs on disk.** Pipe frames straight into ffmpeg stdin:
   `render | ffmpeg -f image2pipe -framerate 30 -i - -i audio.wav out.mp4` — temp files were the disk destroyer.
3. **Always detached + log**: `setsid nohup bash -c '…job… 2>&1 | tee /tmp/opencode/<job>.log' &>/dev/null & disown` then poll the log. (Local box: one job at a time. debz: 1-2 concurrent.)
4. **Split by unit, not by hope**: separate renders/segments/files into independent units → dispatch list → one ssh per unit → poll each log → collect outputs to hub (`scp` back to `/home/box/visuals/experiments/` or target dir).
5. **Scripts travel with the job**: `ssh hetzner 'bash -s' < script.sh` or pipe the script; don't assume remote paths — pass paths as args (dffmpeg's "path-blind" lesson).
6. **Kill by PID, verify after**: `pgrep -af <job>` on BOTH boxes when done/failing.
7. Local renders follow the cheap-review law: **stills-only previews during iteration; full render once, final pass.**

## Skeleton

```bash
# 1. probe
local: uptime && free -m | sed -n 2p && df -h / | tail -1
ssh hetzner 'uptime && free -m | sed -n 2p && df -h / | tail -1'
# 2. dispatch unit i (example: render job N on debz)
ssh hetzner "setsid nohup bash -c 'python3 /root/jobs/render.py --unit $i \
  > /tmp/opencode/job$i.log 2>&1' &" 
# 3. poll
ssh hetzner "tail -3 /tmp/opencode/job$i.log"
# 4. collect
scp hetzner:/root/jobs/out_$i.mp4 /home/box/visuals/experiments/
```

## Built since (2026-10-29) — use these first
- **dagu web UI = the dashboard**: `http://127.0.0.1:8090` (single Go binary, no docker, file state).
  DAGs in `/root/.config/dagu/dags/`: `fleet-ping.yaml` (smoke), `scene-render.yaml` (ship → wait →
  collect+notify). Server log `/tmp/opencode/dagu_server.log`. Full map + postmortem in
  `~/visuals/DESKTOP.md` (dashboard + lessons sections).
- **Job-script dispatchers** (NEVER BLOCK pattern, root AGENTS.md): `/tmp/opencode/dispatch_scene_v*.sh`
  + `bootstrap.sh` — upload with md5-retry, remote launch, poll, collect, `notify-send`. Logs alongside.
- **Path-blind renders**: `standard_cards/{build,scene}.py` take `VE_PATH/TRANSLIT_PATH/BAUMER/OUT/
  FONTS_DIR/EXP/FRAMES` env roots; `ve/glosscard.py` is import-side-effect-free (demos under `__main__`).
- Load-bearing bug patterns: bracket ALL pgrep/pkill patterns (`[s]cene.py render`) — patterns match
  their own cmdline; always re-`tar xzf` bundles (no `[ -f ] ||` guards — stale code).

## Later upgrades (still parked)
- **dstack**: server + fleets once docker exists hub-side (debz first) — tasks via `*.dstack.yml`.
- **jobd** (PyPI): capacity-routed queue across opencode1/2/3 if auto host-picking is wanted.
- **dffmpeg** for ffmpeg-shaped jobs (coordinator+workers+dashboard, path-blind).
- agent-dashboard / qdw federation for session-level fan-out (podman-compose + per-host daemons).

When offload targets something heavier than ssh (GPU, containers), STOP and check this skill's "later upgrades" — don't improvise new infra mid-task.
