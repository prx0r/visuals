#!/usr/bin/env python3
"""analayo_essay0_timeline — assembly_s0_seed.json → timeline.json for stills + render.

Exact windows from the assembly (verified). States per unit:
  Q (fish) → VERBATIM+PLAIN hold → ANALAYO archival (exact lec/start/end) → water
"""
import json
from pathlib import Path

ASM = Path("/home/box/repos/analayo-nibbana/build/assembly_s0_seed.json")
OUT = Path("/tmp/opencode/analayo_essay0_timeline.json")

asm = json.loads(ASM.read_text())

# grammar constants (from process docs)
G = {"q": 4.0, "pause": 3.0, "verbatim": 3.0, "water": 2.5, "bell": 2.0}

rows = []
t = G["bell"]  # motto-bell opens
cur_unit = None
unit_state = {}  # unit -> {q_start, verbatim_start, analayo: (start,end,dur,lec)}

for it in asm:
    kind = it.get("t")
    if kind == "fish" and it.get("role") == "question":
        cur_unit = it["unit"]
        unit_state[cur_unit] = {"q_start": t, "q_text": it["say"]}
        t += G["q"]
    elif kind == "pause" and cur_unit:
        t += G["pause"]
    elif kind == "verbatim" and cur_unit:
        unit_state[cur_unit]["verbatim_start"] = t
        unit_state[cur_unit]["text"] = it["text"]
        unit_state[cur_unit]["plain"] = it.get("plain", "")
        t += G["verbatim"]
    elif kind == "analayo" and cur_unit:
        # archival: exact window from source lecture
        u = unit_state[cur_unit]
        u["analayo"] = {"lec": it["lec"], "src_start": it["start"],
                        "src_end": it["end"], "dur": it["dur"]}
        u["analayo_timeline_start"] = t
        t += float(it["dur"])
    elif kind == "water" and cur_unit:
        t += G["water"]
    elif kind == "zoom-bell":
        t += G["bell"]

# emit rows: each state = one still
for unit in sorted(unit_state, key=int):
    u = unit_state[unit]
    uid = f"u{int(unit):02d}"
    q0 = u["q_start"]
    v0 = u["verbatim_start"]
    a0 = u["analayo_timeline_start"]
    a1 = a0 + u["analayo"]["dur"]
    # Q card: question appears at q0, holds until verbatim
    rows.append({"id": f"{uid}_1_question", "start": round(q0, 2),
                 "end": round(v0, 2), "state": "question", "unit": unit})
    # Verbatim: appears at v0, plain swaps in shortly after (same card, english appears)
    # v0..a0 = verbatim+plain region (fish reads plain during this)
    rows.append({"id": f"{uid}_2_verbatim", "start": round(v0, 2),
                 "end": round(v0 + G["verbatim"], 2), "state": "verbatim", "unit": unit})
    # Plain: same visual as verbatim+plain (the3rd still), holds through analayo
    rows.append({"id": f"{uid}_3_plain", "start": round(v0 + G["verbatim"], 2),
                 "end": round(a1, 2), "state": "plain", "unit": unit})

rows.sort(key=lambda r: r["start"])
total = rows[-1]["end"] if rows else 0

# audio map: archival cuts needed from lecture mp3s
audio_cuts = []
for unit in sorted(unit_state, key=int):
    u = unit_state[unit]
    a = u["analayo"]
    audio_cuts.append({
        "unit": unit, "lec": a["lec"],
        "src_start": a["src_start"], "src_end": a["src_end"],
        "timeline_start": u["analayo_timeline_start"],
        "dur": a["dur"],
    })

sheet = {
    "meta": {"name": "analayo_essay0_seed", "total": round(total, 2),
             "grammar": G, "note": "exact windows from assembly_s0_seed.json"},
    "timeline": rows,
    "audio_cuts": audio_cuts,
}
OUT.write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
print(f"{len(rows)} states, {len(audio_cuts)} archival cuts, total {total/60:.1f}min -> {OUT}")
