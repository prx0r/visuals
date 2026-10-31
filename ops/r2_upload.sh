#!/bin/bash
set -u
LOG=/tmp/opencode/r2_upload.log
exec >>"$LOG" 2>&1
echo "=== start $(date -Is)"

export CLOUDFLARE_API_TOKEN=$(grep -oE '[A-Za-z0-9_-]{40,}' "/home/box/Documents/UK/cloudflare worker api.txt" | head -1)
export CLOUDFLARE_ACCOUNT_ID=954612afb5a97bb15dddcdc70176813d
export CI=true WRANGLER_SEND_METRICS=false
BUCKET=atlas-sources
D=/home/box/Downloads

# src | key
LIST=$(cat <<'EOF'
The Hindu Tantric World An Overview (André Padoux) (z-library.sk, 1lib.sk, z-lib.sk).pdf|text/hindu-tantric-world-padoux.pdf
TANTRA IN PRACTICE Edited by David Gordon White (David Gordon White) (z-library.sk, 1lib.sk, z-lib.sk).epub|text/tantra-in-practice-david-gordon-white.epub
dokumen.pub_the-philosophy-of-illumination-1nbsped-9780842524576.pdf|text/sufi/philosophy-of-illumination-walbridge.pdf
پرتو نامه_The Book of Radiance -- Yaḥyá ibn Ḥabash Suhrawardī, Hossein Ziai -- f8bd58e306ffdf2638d63309358d13ae -- Anna’s Archive.pdf|text/sufi/the-book-of-radiance-suhrawardi-ziai.pdf
پرتو نامه_The Book of Radiance -- Yaḥyá ibn Ḥabash Suhrawardī, Hossein Ziai -- f8bd58e306ffdf2638d63309358d13ae -- Anna’s Archive.md|text/sufi/the-book-of-radiance-suhrawardi-ziai.md
Hakayal-Al-Nur-ny-Shihabuddin-Yahya-al-Suhrawardi.pdf|text/sufi/hayakil-al-nur-suhrawardi.pdf
Man-of-Light-in-Iranian-Sufism-by-Henry-Corbin.pdf|text/sufi/man-of-light-iranian-sufism-corbin.pdf
Academia.edu_Bundle_-_The_Philosophy_of_Illumination_Esoterici.zip|text/sufi/philosophy-of-illumination-academia-bundle.zip
Fusus Al-Hikam_ Ismail Hakki Bursevi’s Translation and -- Ibn al-Arabi, Ismail Hakki Bursevi -- 1-4, 1986 -- Muhyiddin Ibn ’Arabi Society -- isbn13 9780950952710 -- a890b2d6a616ca432fd9763897cfd4f4 -- Anna’s Archive.pdf|text/sufi/fusus-al-hikam-bursevi-v1-4.pdf
EOF
)

FAIL=0
while IFS='|' read -r src key; do
  [ -z "$src" ] && continue
  f="$D/$src"
  if [ ! -s "$f" ]; then echo "SKIP (missing/empty): $src"; FAIL=1; continue; fi
  sz=$(stat -c%s "$f")
  echo "--- put $key ($sz bytes)"
  if wrangler r2 object put "$BUCKET/$key" --file "$f" --remote; then
    echo "PUT OK: $key"
  else
    echo "PUT FAIL: $key"; FAIL=1
  fi
done <<< "$LIST"

echo "=== verify: list text/ prefix"
curl -s "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/r2/buckets/$BUCKET/objects?prefix=text/" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | python3 -c "
import json,sys
d=json.load(sys.stdin)
r=d.get('result') or []
objs=r if isinstance(r,list) else r.get('objects',[])
tot=0
for o in objs:
    k=o.get('key',''); s=o.get('size',0); tot+=s
    print(f'  {k}  {s}')
print(f'  {len(objs)} objects, {tot} bytes total')" 2>&1

if [ "$FAIL" -eq 0 ]; then echo "JOB_EXIT=0"; else echo "JOB_EXIT=1"; fi
runuser -u box -- env DISPLAY=:0 XAUTHORITY=/home/box/.Xauthority \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus \
  notify-send "R2 upload" "atlas-sources/text: $(grep -c 'PUT OK' $LOG) ok, exit=$FAIL (r2_upload.log)"
