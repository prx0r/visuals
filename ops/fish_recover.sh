#!/bin/bash
set -u
LOG=/tmp/opencode/fish_recover.log
exec >>"$LOG" 2>&1
echo "=== fish_recover hub $(date -Is)"
N() { runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send "fish_recover" "$1"; }
FAIL() { echo "FAIL: $1"; N "fish_recover FAILED: $1"; echo "JOB_EXIT=1"; exit 1; }
SSH="ssh -o ConnectTimeout=10 -o ServerAliveInterval=4 -o BatchMode=yes vps"
SCP="scp -o ConnectTimeout=10 -o ServerAliveInterval=4 -C"
REPO=/home/box/Downloads/kashaudio
SRC=/home/box/visuals/outputs/shivastotravali/ai_audio

echo "== 1. remote dirs FIRST + fresh md5 + upload"
$SSH 'mkdir -p /home/ubuntu/fish_audio/shivastotravali /home/ubuntu/fish_audio/spanda /home/ubuntu/kashmir_audio/stotras' || FAIL mkdir
cd "$SRC" || FAIL cd
md5sum *.mp3 > /tmp/opencode/rec450.md5 || FAIL md5gen
echo "md5 entries: $(wc -l < /tmp/opencode/rec450.md5)"
$SCP /tmp/opencode/rec450.md5 vps:/tmp/rec450.md5 || FAIL md5-up
ok=0
for i in 1 2 3; do
  if $SCP *.mp3 vps:/home/ubuntu/fish_audio/shivastotravali/ ; then ok=1; break; fi
  echo "upload attempt $i failed"; sleep 10
done
[ "$ok" -eq 1 ] || FAIL upload
$SCP "$REPO/stotras/shivastotravali_full.json" "$REPO/stotras/spanda.json" \
     "$REPO/stotras/spanda_meta.json" vps:/home/ubuntu/kashmir_audio/stotras/ || FAIL shards
$SCP /tmp/opencode/remote_fish_recover.sh vps:/home/ubuntu/remote_fish_recover.sh || FAIL push
$SSH 'cd /home/ubuntu/fish_audio/shivastotravali && md5sum -c --quiet /tmp/rec450.md5' || FAIL md5-verify
echo "upload + md5 OK"

echo "== 2. launch remote"
$SSH 'setsid nohup bash /home/ubuntu/remote_fish_recover.sh >/dev/null 2>&1 </dev/null & disown' || FAIL launch

echo "== 3. poll with dir-watchdog (3.5h cap)"
st=""
for i in $(seq 1 210); do
  $SSH '[ -d /home/ubuntu/fish_audio/shivastotravali ]' || FAIL "WORK-DIR-DELETED mid-run (git race again?)"
  st=$($SSH 'sed -n "/=== fish_recover remote/,\$p" /home/ubuntu/kashmir_audio/fish_recover.log 2>/dev/null | grep -E "^REMOTE_EXIT=" | tail -1' || true)
  case "$st" in
    REMOTE_EXIT=0) break ;;
    REMOTE_EXIT=*) FAIL "remote:$st" ;;
  esac
  sleep 60
done
[ "$st" = "REMOTE_EXIT=0" ] || FAIL "poll-timeout last='$st'"
echo "remote OK — collect"
$SCP vps:/home/ubuntu/fish_audio/shivastotravali/word_timings.json "$SRC/word_timings_450.json" || echo "collect shiva non-fatal"
$SCP vps:/home/ubuntu/fish_audio/spanda/word_timings.json \
     /home/box/visuals/outputs/spanda/ai_audio/word_timings.json || echo "collect spanda non-fatal"
N "fish_recover OK: 450+52 aligned behind protected dirs, all stills done"
echo "JOB_EXIT=0"
