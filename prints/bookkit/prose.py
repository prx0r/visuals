#!/usr/bin/env python3
"""Bookkit's A5 draft layout for a scholar's own saved prose.

The source text stays in its packet; Markdown is safely formatted for the
proof. This is a review proof, not a KDP-approved layout.
"""
from html import escape
from pathlib import Path
import shutil

CSS = '''
@font-face { font-family: Cormorant; src: url("fonts/CormorantGaramond%5Bwght%5D.ttf"); font-weight: 400 700; }
@font-face { font-family: Tiro; src: url("fonts/TiroDevanagariSanskrit-Regular.ttf"); }
@page { size: 148mm 210mm; margin: 20mm 18mm; @bottom-center { content: "DRAFT  ·  " counter(page); font: 9pt Cormorant; color: #76736e; } }
html,body { background:#fff; color:#17140f; font-family:Cormorant,Tiro,serif; }
body { max-width:112mm; margin:0 auto; font-size:11.5pt; line-height:1.5; }
header { border-bottom:.5pt solid #d9d5cc; margin-bottom:7mm; padding-bottom:5mm; }
h1 { font-size:25pt; line-height:1.15; font-weight:600; margin:4mm 0; }
h2 { font-size:16pt; line-height:1.2; margin:6mm 0 2mm; }
h3 { font-size:13pt; line-height:1.2; margin:4mm 0 2mm; }
p,li { margin:0 0 3mm; } ul,ol { padding-left:5mm; }
table { width:100%; border-collapse:collapse; table-layout:fixed; margin:4mm 0; }
th,td { border-bottom:.5pt solid #d9d5cc; padding:2mm; text-align:left; vertical-align:top; overflow-wrap:anywhere; }
blockquote { border-left:1pt solid #d9d5cc; padding-left:4mm; margin:4mm 0; }
code { overflow-wrap:anywhere; }
.refs { border-top:.5pt solid #d9d5cc; margin-top:8mm; padding-top:3mm; }
.refs li { font-size:9.5pt; word-break:break-all; }
.meta { font-size:9pt; letter-spacing:.06em; color:#76736e; }
.body { overflow-wrap:anywhere; }
@media screen { body { padding:20mm 18mm; box-shadow:0 0 8px #bbb; } }
'''


def make_html(document):
    try:
        import mistune
    except ImportError as exc:
        raise RuntimeError('install mistune to format the book proof') from exc
    title = escape(document.get('title') or 'Untitled')
    author = escape(document.get('author') or 'Author not specified')
    work = escape(document.get('work') or '')
    revision = document.get('revision')
    tag = f' · revision {revision}' if isinstance(revision, int) and revision > 0 else ''
    class PrivateRenderer(mistune.HTMLRenderer):
        def image(self, text, url, title=None):
            # No network fetch or arbitrary local-file inclusion from a draft.
            return '<span>[Image reference: '+text+' · '+escape(url)+']</span>'
    body = mistune.create_markdown(renderer=PrivateRenderer(escape=True), plugins=['table'])(document['text'])
    citations = document.get('citations') or []
    references = ''
    if citations:
        items=''.join('<li>'+escape(c['work'])+' · '+escape(c['target'])+'<br>T1: '+escape(c['t1_sha256'])+'<br>Projection: '+escape(c['projection_sha256'])+'</li>' for c in citations)
        references = '<section class="refs"><h2>Passage references</h2><ul>'+items+'</ul></section>'
    has_title = document['text'].lstrip().startswith('# ' + (document.get('title') or 'Untitled') + '\n')
    header_title = '' if has_title else f'<h1>{title}</h1>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — draft</title>
<style>{CSS}</style></head><body><header><div class="meta">DRAFT · PRIVATE PROOF</div>
{header_title}<div class="meta">{author} · {work}{tag}</div></header>
<main class="body">{body}{references}</main></body></html>'''


def write_book(document, output, fonts_dir):
    output = Path(output)
    fonts = output / 'fonts'
    fonts.mkdir(parents=True, exist_ok=True)
    for name in ('CormorantGaramond[wght].ttf', 'TiroDevanagariSanskrit-Regular.ttf'):
        source = Path(fonts_dir) / name
        if not source.is_file():
            raise FileNotFoundError(f'missing bookkit font: {source}')
        shutil.copyfile(source, fonts / name)
    destination = output / 'index.html'
    destination.write_text(make_html(document), encoding='utf-8')
    return destination
