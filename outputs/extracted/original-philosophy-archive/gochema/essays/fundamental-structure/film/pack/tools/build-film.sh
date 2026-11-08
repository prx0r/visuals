#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p build/audio-scenes MOTHERFUCKER/build/fundamental-structure
python3 - <<'PY'
import json, subprocess
from pathlib import Path
for e in json.loads(Path("narration.json").read_text()):
 out=Path("build/audio-scenes")/f'{e["id"]}.mp3'
 subprocess.run(["edge-tts","--voice","en-GB-SoniaNeural","--text",e["text"],"--write-media",str(out)],check=True)
PY
python3 tools/compile-timed-pack.py "$ROOT"
python3 - <<'PY'
import json
from pathlib import Path
es=json.loads(Path("narration.json").read_text())
Path("build/audio-scenes/concat.txt").write_text("\n".join(f"file '{(Path('build/audio-scenes')/(e['id']+'.mp3')).resolve()}'" for e in es)+"\n")
PY
ffmpeg -y -loglevel error -f concat -safe 0 -i build/audio-scenes/concat.txt -c:a libmp3lame -q:a 2 MOTHERFUCKER/build/fundamental-structure/narration.mp3
python3 MOTHERFUCKER/tools/analyse-audio.py MOTHERFUCKER/build/fundamental-structure/narration.mp3 MOTHERFUCKER/build/fundamental-structure/features.json
node tools/render-pack.mjs
ffmpeg -y -loglevel error -i MOTHERFUCKER/build/fundamental-structure/video.mp4 -i MOTHERFUCKER/build/fundamental-structure/narration.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest MOTHERFUCKER/build/fundamental-structure/final.mp4
