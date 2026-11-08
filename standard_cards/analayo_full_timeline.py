#!/usr/bin/env python3
"""analayo_full_timeline — transcript + cutplan → full kept timeline.

Kept sentences = transcript sentences whose midpoint falls outside every cut
span in the cutplan. Output: timeline.json for stills.py.
"""
import argparse, json, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lecture", help="lecture number (e.g. 01)")
    ap.add_argument("--min-gap", type=float, default=0.8,
                    help="merge sentences closer than this")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()

    n = a.lecture.zfill(2) if a.lecture.isdigit() else a.lecture
    repo = Path("/home/box/repos/analayo-nibbana")
    tr = json.load(open(repo / f"lecture-{n}.transcript.cf.json"))
    cp = json.load(open(repo / f"lecture-{n}.cutplan.json"))

    cuts = [(c["start"], c["end"]) for c in cp["cuts"]]
    src_end = cp["source_min"] * 60

    def in_cut(mid):
        return any(s <= mid <= e for s, e in cuts)

    # kept sentences (midpoint outside all cuts)
    kept = [s for s in tr["sentences"]
            if not in_cut((s["t"] + s["end"]) / 2)]

    # merge very close sentences into one card
    merged = []
    for s in kept:
        if merged and s["t"] - merged[-1]["end"] < a.min_gap:
            merged[-1]["end"] = s["end"]
            merged[-1]["text"] = (merged[-1]["text"] + " " + s["text"]).strip()
        else:
            merged.append({"t": s["t"], "end": s["end"], "text": s["text"]})

    rows = []
    for i, m in enumerate(merged, 1):
        rows.append({
            "id": f"s{i:03d}",
            "start": round(m["t"], 2),
            "end": round(m["end"], 2),
            "text": m["text"],
        })

    out = Path(a.out or f"/tmp/opencode/analayo_l{n}_full_timeline.json")
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    dur = rows[-1]["end"] - rows[0]["start"] if rows else 0
    print(f"{len(rows)} kept rows ({len(kept)} raw sentences, "
          f"{len(cuts)} cuts, source {src_end/60:.0f}min, kept ~{dur/60:.0f}min) -> {out}")


if __name__ == "__main__":
    main()
