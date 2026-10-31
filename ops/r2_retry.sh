#!/bin/bash
set -u
LOG=/tmp/opencode/r2_retry.log
exec >>"$LOG" 2>&1
echo "=== start $(date -Is)"
export CLOUDFLARE_API_TOKEN=$(grep -oE '[A-Za-z0-9_-]{40,}' "/home/box/Documents/UK/cloudflare worker api.txt" | head -1)
export CLOUDFLARE_ACCOUNT_ID=954612afb5a97bb15dddcdc70176813d
export CI=true WRANGLER_SEND_METRICS=false
D=/home/box/Downloads
fail=0
for try in 1 2 3; do
  echo "--- attempt $try"
  wrangler r2 object put "atlas-sources/text/hindu-tantric-world-padoux.pdf" \
    --file "$D/The Hindu Tantric World An Overview (André Padoux) (z-library.sk, 1lib.sk, z-lib.sk).pdf" --remote \
    && echo "OK tantra1" || { fail=1; sleep 8; continue; }
  wrangler r2 object put "atlas-sources/text/tantra-in-practice-david-gordon-white.epub" \
    --file "$D/TANTRA IN PRACTICE Edited by David Gordon White (David Gordon White) (z-library.sk, 1lib.sk, z-lib.sk).epub" --remote \
    && echo "OK tantra2" || { fail=1; sleep 8; continue; }
  fail=0; break
done
echo "=== verify text/ (top level)"
curl -s "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/r2/buckets/atlas-sources/objects?prefix=text/" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | python3 -c "
import json,sys
d=json.load(sys.stdin); r=d.get('result') or []
objs=[o for o in (r if isinstance(r,list) else r.get('objects',[])) if o.get('key','').count('/')==1]
for o in objs: print('  ',o['key'],o['size'])
print(' top-level text/ objects:',len(objs))
need=['text/hindu-tantric-world-padoux.pdf','text/tantra-in-practice-david-gordon-white.epub']
have={o['key'] for o in objs}
missing=[k for k in need if k not in have]
print(' MISSING:',missing if missing else 'none')"
if [ "$fail" -eq 0 ]; then echo "JOB_EXIT=0"; else echo "JOB_EXIT=1"; fi
runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus \
  notify-send "R2 retry" "tantra files: exit=$fail (r2_retry.log)"
