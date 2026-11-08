#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
template=root/"MOTHERFUCKER/packs/fundamental-structure.template.json"
out=root/"MOTHERFUCKER/packs/fundamental-structure.json"
audio=root/"build/audio-scenes"
pack=json.loads(template.read_text(encoding="utf-8"))
for scene in pack["scenes"]:
 f=audio/f'{scene["id"]}.mp3'
 r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
 "-of","default=noprint_wrappers=1:nokey=1",str(f)],capture_output=True,text=True,check=True)
 scene["duration"]=round(float(r.stdout.strip()),3)
out.write_text(json.dumps(pack,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(out)
