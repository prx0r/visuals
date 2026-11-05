#!/usr/bin/env python3
"""render_postcards.py — Prodigi fine-art postcards from a book's entries.json.

Product: GLOBAL-POST-GLOS-6X4 (fine-art postcard, 6x4in = 152x102mm, 300dpi,
front AND back free-form — the classic postcard back is postal-only, so the
guide goes here). Front = the prayer, back = the explainer (the same four
blocks as the book guide: What is it / How to perform it / How to know it's
working [/ What to feel]). Designed ONCE — both books inherit.

Usage:
  python3 prints/postcards/render_postcards.py practical-prayers
  python3 prints/postcards/render_postcards.py tantric-prayer mpa-1 sst-16-8
  python3 prints/postcards/render_postcards.py all            # both books
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRINTS = os.path.dirname(HERE)
ROOT = os.path.dirname(PRINTS)
TIO = "/root/.fonts/TiroDevanagariSanskrit-Regular.ttf"
COR = "/root/.fonts/CormorantGaramond[wght].ttf"
OUT = os.path.join(ROOT, "outputs", "print_products", "postcards")
W, H = 1800, 1200           # 6 x 4 in @ 300dpi  (GLOBAL-POST-GLOS-6X4)
SKU = "GLOBAL-POST-GLOS-6X4"

CSS = f"""
@page {{ size: 6in 4in; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ background:#fff; }}
@font-face {{ font-family:'Tiro'; src:url('file://{TIO}'); }}
@font-face {{ font-family:'Cormorant'; src:url('file://{COR}'); font-weight:300 700; }}
.page {{ width:6in; height:4in; overflow:hidden; background:#fff;
  color:#17140f; font-family:'Cormorant',serif; position:relative;
  padding:.37in .4in; page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
.label {{ font-size:7.5pt; letter-spacing:.24em; text-transform:uppercase;
  color:#76736e; font-weight:600; }}
.rule {{ height:2px; background:#17140f; opacity:.75; margin:.09in 0 .11in; }}

/* ---- FRONT: the prayer ---- */
.f .src {{ font-size:7.5pt; letter-spacing:.18em; text-transform:uppercase; color:#76736e; margin-top:.05in; font-weight:600; }}
.f .cols {{ display:flex; gap:.23in; margin-top:.15in; height:2.53in; }}
.f .left {{ width:45%; }}
.f .right {{ flex:1; }}
.f .dev {{ font-family:'Tiro',serif; font-size:16pt; line-height:1.6; }}
.f .iast {{ font-size:9.5pt; line-height:1.5; color:#76736e; font-style:italic; margin-top:.15in; }}
.f .en {{ font-size:14pt; line-height:1.5; font-weight:500; }}
.f .en.sm {{ font-size:11pt; }}
.f .en.xs {{ font-size:9.5pt; }}
.f .foot, .b .foot {{ position:absolute; left:.4in; right:.4in; bottom:.25in;
  display:flex; justify-content:space-between; align-items:baseline;
  border-top:1.5px solid #17140f; padding-top:.07in; }}
.f .foot .sec, .b .foot .sec {{ font-size:7.5pt; letter-spacing:.2em; text-transform:uppercase; color:#76736e; font-weight:600; }}
.f .foot .bk, .b .foot .bk {{ font-size:7.5pt; letter-spacing:.3em; text-transform:uppercase; font-weight:600; }}

/* ---- BACK: the explainer (once, both books) ---- */
.b {{ padding-bottom:.95in; }}
.b h1 {{ font-size:16pt; font-weight:600; line-height:1.1; letter-spacing:.01em; }}
.b .brief {{ font-size:9.5pt; font-style:italic; color:#3d382f; line-height:1.4; margin-top:.07in; }}
.b .rule {{ margin:.08in 0 .1in; }}
.b .cols2 {{ column-count:2; column-gap:.23in; }}
.b .blk {{ break-inside:avoid; margin-bottom:.11in; }}
.b .blk .bl {{ font-size:7pt; letter-spacing:.2em; text-transform:uppercase;
  color:#76736e; font-weight:600; display:block; margin-bottom:.04in; }}
.b .blk p {{ font-size:9.5pt; line-height:1.45; }}
.f .dev.sm {{ font-size:13.5pt; }}
.f .iast.sm {{ font-size:8.5pt; margin-top:.1in; }}
"""


def corpus_index(book_dir):
    p = os.path.join(book_dir, "sources", "shivastotravali_corpus.json")
    if not os.path.exists(p):
        return {}
    import json
    d = json.load(open(p))
    idx = {}
    for ch in d["chapters"]:
        for v in ch["verses"]:
            idx[(int(ch["number"]), int(v["number"]))] = v
    return idx


def sanskrit_of(e, idx):
    if "iast" in e:
        iast = e["iast"]
    elif "corpus" in e:
        rec = idx.get((int(e["corpus"][0]), int(e["corpus"][1])))
        if not rec:
            return None, None
        iast = rec["iast"]
    else:
        return None, None
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    dev = transliterate(iast, sanscript.IAST, sanscript.DEVANAGARI)
    return dev, iast


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def front(e, idx, book_title, section_name):
    dev, iast = sanskrit_of(e, idx)
    en_lines = esc(e.get("en", "")).replace("\n", "<br>")
    n = len(e.get("en", ""))
    cls = "en" if n < 190 else ("en sm" if n < 300 else "en xs")
    left = ""
    if dev:
        long_sanskrit = len(iast or "") > 150
        dcls = "dev sm" if long_sanskrit else "dev"
        icls = "iast sm" if long_sanskrit else "iast"
        dev_p = dev.replace("।", "।").replace("/", "<br>")
        left = f'<div class="{dcls}">{dev_p}</div><div class="{icls}">{esc(iast).replace("/", "<br>")}</div>'
    return f"""<section class="page f">
<div class="label">{esc(e.get('title',''))}</div>
<div class="src">{esc(e.get('source',''))} · {esc(e.get('source_ref',''))}</div>
<div class="cols"><div class="left">{left}</div><div class="right"><div class="{cls}">{en_lines}</div></div></div>
<div class="foot"><span class="sec">{esc(section_name)}</span><span class="bk">{esc(book_title)}</span></div>
</section>"""


def back(e, idx, book_title, section_name):
    blocks = []
    what = e.get("what") or e.get("logic", "")
    how = e.get("how") or e.get("howto", "")
    for label, text in (("What is it", what), ("How to perform it", how),
                        ("How to know it's working", e.get("sign", "")),
                        ("What to feel / visualise", e.get("feel", ""))):
        if text:
            blocks.append(f'<div class="blk"><span class="bl">{label}</span><p>{esc(text)}</p></div>')
    src = (e.get("source_path", "").replace("sources/", "") + " · " +
           e.get("source_ref", ""))
    return f"""<section class="page b">
<h1>{esc(e.get('title',''))}</h1>
<div class="brief">{esc(e.get('brief',''))}</div>
<div class="rule"></div>
<div class="cols2">{"".join(blocks)}</div>
<div class="foot"><span class="sec">{esc(src)}</span><span class="bk">{esc(book_title)}</span></div>
</section>"""


def build(book, ids=None):
    import json
    book_dir = os.path.join(PRINTS, book)
    entries = json.load(open(os.path.join(book_dir, "entries.json")))
    book_title = json.load(open(os.path.join(book_dir, "book.json")))["meta"]["title"]
    idx = corpus_index(book_dir)
    sections = {s["id"]: s.get("title", s["id"]) for s in
                json.load(open(os.path.join(book_dir, "book.json")))["sections"]}
    if ids:
        want = set(ids)
        entries = [e for e in entries if e["id"] in want]
        if not entries:
            raise SystemExit(f"no entries matched {ids}")
    pages, order = [], []
    for e in entries:
        sec = sections.get(e["section"], e["section"])
        pages.append(front(e, idx, book_title, sec))
        pages.append(back(e, idx, book_title, sec))
        order.append(e["id"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    os.makedirs("/tmp/opencode", exist_ok=True)
    src = f"/tmp/opencode/postcards_{book}.html"
    open(src, "w").write(html)
    pdf = f"/tmp/opencode/postcards_{book}.pdf"
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([
        "google-chrome-stable", "--headless=new", "--disable-gpu", "--no-sandbox",
        "--disable-dev-shm-usage", "--disable-crash-reporter", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}", f"file://{src}"], check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    out_dir = os.path.join(OUT, book)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "300", "-png", pdf,
                    os.path.join(out_dir, "_pg")], check=True)
    made = []
    for i, eid in enumerate(order):
        for k, side in ((2 * i + 1, "front"), (2 * i + 2, "back")):
            pg = os.path.join(out_dir, f"_pg-{k:02d}.png")
            if not os.path.exists(pg):       # pdftoppm width depends on page count
                pg = os.path.join(out_dir, f"_pg-{k}.png")
            dst = os.path.join(out_dir, f"{eid}__{side}.png")
            os.replace(pg, dst)
            made.append(dst)
    index = os.path.join(out_dir, "index.html")
    rows = "".join(
        f"<div style='display:flex;gap:24px;margin-bottom:40px;align-items:flex-start'>"
        f"<div><h3 style='font-family:serif'>{eid} — front</h3>"
        f"<img src='{eid}__front.png' width='600'></div>"
        f"<div><h3 style='font-family:serif'>{eid} — back</h3>"
        f"<img src='{eid}__back.png' width='600'></div></div>"
        for eid in order)
    open(index, "w").write(
        f"<!doctype html><meta charset='utf-8'><title>{book} postcards — {SKU}</title>"
        f"<body style='background:#ddd;font-family:sans-serif;padding:30px'>"
        f"<h1>{book} · fine-art postcards · {SKU} ({W}×{H}px @300dpi)</h1>{rows}</body>")
    for f in os.listdir(out_dir):
        if f.startswith("_pg"):
            os.remove(os.path.join(out_dir, f))
    print(f"{book}: {len(order)} cards x2 sides -> {len(made)} PNGs")
    print(f"  index: {index}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    if args[0] == "all":
        build("practical-prayers")
        build("tantric-prayer")
    else:
        build(args[0], args[1:] or None)
