#!/bin/bash
set -u
# shift big archival files hub -> HC volume (verify before delete), owner 2026-10-31
LOG=/tmp/opencode/shift_to_volume.log
exec >>"$LOG" 2>&1
echo "=== shift_to_volume $(date -Is)"
N() { runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "shift_to_volume" "$1"; }
FAIL() { echo "FAIL: $1"; N "shift_to_volume FAILED: $1"; echo "JOB_EXIT=1"; exit 1; }
OPTS="-o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password -o PubkeyAuthentication=no -o ConnectTimeout=10"
H=root@2.28.50.109
B=/mnt/HC_Volume_106427611/patala
RS="rsync -a --partial --inplace --info=stats2 -e sshpass\ -p\ xx\ ssh\ $OPTS"

echo "== 0. wait for store_work (same link)"
for i in $(seq 1 160); do
  pgrep -f "[s]tore_work.sh" >/dev/null || break
  sleep 15
done
echo "store_work done/absent — starting $(date -Is)"

sshpass -p xx ssh $OPTS $H "mkdir -p $B/archive/yt $B/archive/sources $B/archive/media" || FAIL mkdir

move() {  # $1=src dir (absolute) $2=remote parent dir
  local src=$1 dest=$2 name bytes files rbytes rfiles
  name=$(basename "$src")
  case "$src" in /home/box/Downloads/*) : ;; *) FAIL "refusing non-Downloads path $src" ;; esac
  [ -d "$src" ] || { echo "skip (gone): $src"; return 0; }
  bytes=$(du -sb "$src" | cut -f1)
  files=$(find "$src" -type f | wc -l)
  echo "-- $name ($bytes bytes, $files files) -> $dest"
  rsync -a --partial --inplace -e "sshpass -p xx ssh $OPTS" "$src" "$H:$dest/" || FAIL "rsync $name"
  rbytes=$(sshpass -p xx ssh $OPTS $H "du -sb $dest/$name | cut -f1")
  rfiles=$(sshpass -p xx ssh $OPTS $H "find $dest/$name -type f | wc -l")
  if [ "$rbytes" != "$bytes" ] || [ "$rfiles" != "$files" ]; then
    FAIL "verify $name: local $bytes/$files vs remote $rbytes/$rfiles"
  fi
  rm -rf "$src"
  echo "MOVED+VERIFIED $name ($bytes bytes) — local removed"
}

D=/home/box/Downloads
for d in yt/baumer yt/analayo-nibbana yt/rebirth yt/huangpo yt/cuts; do
  move "$D/$d" "$B/archive/yt"
done
for d in tantralokaa abhinavagupta_trans; do
  move "$D/$d" "$B/archive/sources"
done
for d in gold3 goldfiles2 goldfiles camedy; do
  move "$D/$d" "$B/archive/media"
done

echo "== summary"
df -h / | tail -1
sshpass -p xx ssh $OPTS $H "du -sh $B/archive/* ; df -h /mnt/HC_Volume_106427611 | tail -1"
N "shift_to_volume OK: ~19G of archives on the volume, hub freed (see log for per-dir verify lines)"
echo "JOB_EXIT=0"
