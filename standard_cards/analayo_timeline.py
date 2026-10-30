#!/usr/bin/env python3
"""analayo_timeline — transcript.cf.json → timeline.json (stills.py format).

  python3 analayo_timeline.py lecture-01 [--from 0 --to 60] [--min-gap 0.5] [-o out.json]
"""
import argparse, json, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lecture", help="lecture number or path to transcript.cf.json")
    ap.add_argument("--from", dest="t0", type=float, default=0)
    ap.add_argument("--to", dest="t1", type=float, default=60)
    ap.add_argument("--min-gap", type=float, default=0.6,
                    help="merge sentences closer than this")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()

    p = Path(a.lecture)
    if not p.exists():
        n = a.lecture.zfill(2) if a.lecture.isdigit() else a.lecture
        p = Path(f"/home/box/repos/analayo-nibbana/lecture-{n}.transcript.cf.json")
    if not p.exists():
        sys.exit(f"no transcript: {p}")

    tr = json.load(open(p))
    sents = [s for s in tr["sentences"]
             if s["end"] > a.t0 and s["t"] < a.t1]

    # merge very close sentences into one card
    merged = []
    for s in sents:
        if merged and s["t"] - merged[-1]["end"] < a.min_gap:
            merged[-1]["end"] = s["end"]
            merged[-1]["text"] = (merged[-1]["text"] + " " + s["text"]).strip()
        else:
            merged.append({"t": s["t"], "end": s["end"], "text": s["text"]})

    # trim to window
    for m in merged:
        m["t"] = max(m["t"], a.t0)
        m["end"] = min(m["end"], a.t1)

    rows = []
    for i, m in enumerate(merged, 1):
        rows.append({
            "id": f"s{i:02d}",
            "start": round(m["t"], 2),
            "end": round(m["end"], 2),
            "text": m["text"],
        })

    out = Path(a.out or f"/tmp/opencode/analayo_l{p.stem.split('-')[1].split('.')[0]}_timeline.json")
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(f"{len(rows)} rows [{a.t0}-{a.t1}s] -> {out}")


if __name__ == "__main__":
    main()
