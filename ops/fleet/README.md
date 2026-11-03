# ops/fleet — dispatch to opencode1 / opencode2 / opencode3

Everything needed for an agent to fan work out to the fleet, consolidated here
2026-11-03 (the one-off `/tmp/opencode/dispatch_scene_v*.sh` and `dispatch.sh`
stubs were lost to tmp wipes — this dir is the persistent home).

| file | what it is | lives normally at |
|---|---|---|
| `opencode1.sh` | interactive TUI into debz (Hetzner) | `/usr/local/bin/opencode1` |
| `opencode2.sh` | interactive TUI into server2 (password auth) | `/usr/local/bin/opencode2` |
| `opencode3.sh` | interactive TUI into old OVH (primary render box) | `/usr/local/bin/opencode3` |
| `dagu/fleet-ping.yaml` | smoke DAG (hub + vps uptime) | `/root/.config/dagu/dags/` |
| `dagu/scene-render.yaml` | ship → remote render → poll → collect → notify | `/root/.config/dagu/dags/` |
| `parallel-dispatch.SKILL.md` | THE fleet reference: reach table, capacity rules, skeleton, postmortems | `/root/.config/opencode/skills/parallel-dispatch/` |

## Reach (non-interactive)

```bash
opencode1  ssh -o BatchMode=yes hetzner                          # root, key
opencode2  sshpass -p 'xx' ssh -o PreferredAuthentications=password \
                -o PubkeyAuthentication=no root@2.28.50.109      # password auth
opencode3  ssh -o BatchMode=yes vps                              # ubuntu, key
volume     root@2.28.50.109:/mnt/HC_Volume_106427611/patala/     # 56G free — OUTPUT HERE
```

## Rules (from SKILL.md — read it before dispatching)

1. Capacity-check first (load<6, free>500M, disk fits) — all three box disks
   are 96–98% full; **new render jobs must write to the volume, not box disk**.
2. Never dump frame PNGs — pipe frames straight into ffmpeg stdin.
3. Always detached: `setsid nohup … &>/dev/null & disown` + own log + notify-send.
4. Split work into independent units, one ssh each, poll logs, collect to hub.
5. Bracket all pgrep patterns (`[s]cene.py`), re-`tar xzf` bundles unconditionally.
6. Proven load: 3-way simultaneous dispatch (1 unit each) → wall clock 5s.

## DAG (dagu)

Server: `dagu start-all --host 127.0.0.1 --port 8090` → dashboard
`http://127.0.0.1:8090`. Scene-render pattern: scp bootstrap → `setsid nohup`
remote → poll `run.log` (bracket pgrep) → scp mp4 back → notify-send.
