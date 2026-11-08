#!/bin/bash
set -u
# hub: move the owner's named big projects -> volume projects/hub/ (waits for shift_to_volume)
LOG=/tmp/opencode/hub_move_projects.log
exec >>"$LOG" 2>&1
echo "=== hub_move_projects $(date -Is)"
N() { runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "hub_move_projects" "$1"; }
FAIL() { echo "FAIL: $1"; N "hub_move_projects FAILED: $1"; echo "JOB_EXIT=1"; exit 1; }
OPTS="-o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password -o PubkeyAuthentication=no -o ConnectTimeout=10"
H=root@2.28.50.109
B=/mnt/HC_Volume_106427611/patala

echo "== wait for shift_to_volume (same link)"
for i in $(seq 1 400); do
  pgrep -f "[s]hift_to_volume.sh" >/dev/null || break
  sleep 20
done
pgrep -f "[s]hift_to_volume.sh" >/dev/null && FAIL "shift still running after 2.2h"
echo "shift done/absent — starting $(date -Is)"
sshpass -p xx ssh $OPTS $H "mkdir -p $B/projects/hub" || FAIL mkdir

move() {
  local name=$1 src=/home/box/repos/$1 t p
  [ -d "$src" ] || { echo "skip missing $name"; return 0; }
  for p in /proc/[0-9]*/cwd; do
    t=$(readlink "$p" 2>/dev/null) || continue
    case "$t" in "$src"|"$src"/*) echo "SKIP-running $name ($t)"; return 0 ;; esac
  done
  local bytes files rb rf
  bytes=$(du -sb "$src" | cut -f1); files=$(find "$src" -type f | wc -l)
  echo "-- $name ($bytes, $files files)"
  rsync -a --partial -e "sshpass -p xx ssh $OPTS" "$src" "$H:$B/projects/hub/" || { echo "RSYNC_FAIL $name"; return 1; }
  rb=$(sshpass -p xx ssh $OPTS $H "du -sb $B/projects/hub/$name | cut -f1")
  rf=$(sshpass -p xx ssh $OPTS $H "find $B/projects/hub/$name -type f | wc -l")
  if [ "$rb" != "$bytes" ] || [ "$rf" != "$files" ]; then
    echo "VERIFY_FAIL $name local=$bytes/$files remote=$rb/$rf"; return 1
  fi
  rm -rf "$src"
  echo "MOVED+VERIFIED $name"
  printf -- "- %s  %sB  ~/repos/%s (hub) -> patala/projects/hub/%s\n" "$(date +%F)" "$bytes" "$name" "$name" >> /home/box/repos/MOVED-projects.md
}
rc=0
for d in abhidhamma earshot characters gcomedy analayo-nibbana; do move "$d" || rc=1; done

echo "== after:"; df -h / | tail -1
sshpass -p xx ssh $OPTS $H "df -h $B | tail -1" || true
[ $rc -eq 0 ] || { N "hub_move_projects: some dirs failed (see log)"; echo "JOB_EXIT=1"; exit 1; }
N "hub_move_projects OK: abhidhamma/earshot/characters/gcomedy/analayo on the volume (projects/hub/)"
echo "JOB_EXIT=0"
