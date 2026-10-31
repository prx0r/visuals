#!/bin/bash
set -u
LOG=/tmp/opencode/store_work.log
exec >>"$LOG" 2>&1
echo "=== store_work v2 $(date -Is)"
N() { runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "store_work" "$1"; }
FAIL() { echo "FAIL: $1"; N "store_work FAILED: $1"; echo "JOB_EXIT=1"; exit 1; }
OPTS="-o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password -o PubkeyAuthentication=no -o ConnectTimeout=10"
H=root@2.28.50.109
B=/mnt/HC_Volume_106427611/patala

echo "== 1. layout"
sshpass -p xx ssh $OPTS $H "mkdir -p $B/audio $B/renders $B/archive $B/docs $B/tests $B/backup" || FAIL mkdir-volume

echo "== 2. audio bulk"
ok=0
for i in 1 2 3; do
  if sshpass -p xx scp $OPTS -r /home/box/visuals/outputs/shivastotravali/ai_audio $H:$B/audio/ ; then ok=1; break; fi
  echo "sync shiva attempt $i failed"; sleep 10
done
[ "$ok" -eq 1 ] || FAIL sync-shiva
ok=0
for i in 1 2 3; do
  if sshpass -p xx scp $OPTS -r /home/box/visuals/outputs/spanda/ai_audio $H:$B/audio/ ; then ok=1; break; fi
  echo "sync spanda attempt $i failed"; sleep 10
done
[ "$ok" -eq 1 ] || FAIL sync-spanda
sshpass -p xx scp $OPTS -r /home/box/visuals/outputs/tests $H:$B/tests/ || echo "tests non-fatal"

echo "== 3. docs"
sshpass -p xx scp $OPTS /home/box/Downloads/ipvv/manifests/AUDIO-FORM-LIST.md $H:$B/docs/ || echo "list non-fatal"
sshpass -p xx scp $OPTS /home/box/Documents/patala/HANDOVER-shivastotravali.md $H:$B/docs/ || echo "handover non-fatal"

echo "== 4. inventory + ledger"
sshpass -p xx ssh $OPTS $H "cd $B && find . -type f | wc -l && du -sh audio tests docs 2>/dev/null && df -h /mnt/HC_Volume_106427611 | tail -1" || true
sshpass -p xx ssh $OPTS $H "cd $B && find . -type f -exec md5sum {} + > archive/LEDGER-\$(date +%Y%m%d).md5" || echo "ledger non-fatal"
N "store_work OK: fish audio + docs on HC volume (patala/audio, ledger in archive)"
echo "JOB_EXIT=0"
