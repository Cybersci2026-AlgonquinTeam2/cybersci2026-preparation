"""EPUB v2 builder: phone-first, dark-mode-safe, tables as cards, one chapter per section.

Used by build_offline.py. Differences from v1:
  - semi-transparent backgrounds and no hard-coded text colours (readable in Books' dark/sepia themes)
  - tables converted to stacked "cards" (no horizontal scrolling or squashed columns)
  - one chapter per h1/h2 so navigation and page turns are short; nested table of contents
  - PNG cover; broken in-book anchors and nav/link boilerplate removed
"""
import hashlib
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import date
from pathlib import Path

from lxml import etree, html as lhtml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_offline as B  # noqa: E402
import visual as V  # noqa: E402

CSS = """
html, body { margin: 0; padding: 0; }
body { font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; line-height: 1.55; margin: 0 1.1em; }
h1 { font-size: 1.6em; line-height: 1.2; margin: 1.1em 0 .6em; }
h2 { font-size: 1.3em; line-height: 1.25; margin: 1.5em 0 .5em; padding-bottom: .2em; border-bottom: 1px solid rgba(127,127,127,.45); }
h3 { font-size: 1.1em; margin: 1.3em 0 .4em; }
h4 { font-size: 1em; margin: 1.1em 0 .3em; }
p { margin: .7em 0; }
ul, ol { padding-left: 1.35em; }
li { margin: .35em 0; }
a { text-decoration: underline; }
hr { border: none; border-top: 1px solid rgba(127,127,127,.4); margin: 1.4em 0; }
pre { font-family: Menlo, "Courier New", monospace; font-size: .74em; line-height: 1.35;
      white-space: pre-wrap; word-wrap: break-word; padding: .7em; border-radius: 6px;
      background: rgba(127,127,127,.14); border: 1px solid rgba(127,127,127,.35); }
code { font-family: Menlo, "Courier New", monospace; font-size: .88em; word-wrap: break-word;
       background: rgba(127,127,127,.18); padding: 0 .25em; border-radius: 3px; }
pre code { background: none; padding: 0; font-size: 1em; }
blockquote { margin: 1em 0; padding: .2em .9em; border-left: 4px solid #d97706; background: rgba(217,119,6,.12); }
.card { margin: .9em 0; padding: .6em .8em; border: 1px solid rgba(127,127,127,.4);
        border-radius: 8px; background: rgba(127,127,127,.08); }
.card-title { font-weight: bold; margin: 0 0 .3em; }
.card p { margin: .3em 0; }
.lab { display: block; font-size: .74em; text-transform: uppercase; letter-spacing: .04em; opacity: .7; }
.fig { text-align: center; margin: 1.1em 0; }
.fig img { max-width: 100%; height: auto; }
.part { text-align: center; margin-top: 30%; }
.part h1 { font-size: 1.9em; }
.part p { opacity: .75; }
.cover img { width: 100%; height: auto; }
.fig.diagram img { width: 100%; }
.hero { margin: 1.2em 0 0; }
.hero img { width: 100%; height: auto; }
"""
ACCENTS = ["#2563eb", "#0d9488", "#d97706", "#7c3aed", "#dc2626", "#16a34a", "#db2777", "#0891b2",
           "#4f46e5", "#ca8a04", "#059669", "#9333ea", "#ea580c", "#0284c7", "#be185d"]
CSS = CSS + V.CSS_CALLOUTS + "".join(
    f".p{i} h1 {{ border-left: 6px solid {c}; padding-left: .5em; }} "
    f".p{i} h2 {{ border-bottom-color: {c}; }} "
    f".p{i} .part {{ border-top: 10px solid {c}; padding-top: 1em; }} "
    f".p{i} .card {{ border-left: 4px solid {c}; }} " for i, c in enumerate(ACCENTS))
HERO = ["m1-triage-loop.svg", "f-pcap.svg", "w-method.svg", "c-recognize.svg", "r-compile.svg", "p-ad-path.svg",
        "k-ports.svg", "fm-map.svg", "wc-template.svg", "wc-mock-plan.svg", "00-journey.svg", "05-pipes.svg",
        "09-setuid.svg", "fm-career.svg", "fm-certs.svg"]
IMG_DIRS = [B.ROOT / "curriculum" / "modules" / "img", B.ROOT / "curriculum" / "bandit" / "img-phone",
            B.ROOT / "curriculum" / "activities" / "img",
            B.ROOT / "curriculum" / "pastchallenges" / "img"]


def find_img(name):
    for d in IMG_DIRS:
        if (d / name).exists():
            return d / name
    return None


DROP_PREFIX = ("navigation:", "next:", "previous:", "continue with", "*continue with", "format note:")


def _cell_html(td):
    inner = (td.text or "") + "".join(etree.tostring(c, encoding="unicode", method="html") for c in td)
    return inner.strip()


def tables_to_cards(root):
    for table in list(root.iter("table")):
        heads = [(" ".join(th.text_content().split())) for th in table.xpath(".//thead//th | .//tr[1]/th")]
        rows = []
        for tr in table.xpath(".//tr"):
            tds = tr.xpath("./td")
            if tds:
                rows.append(tds)
        wrap = lhtml.Element("div")
        for tds in rows:
            card = etree.SubElement(wrap, "div", {"class": "card"})
            title = etree.SubElement(card, "p", {"class": "card-title"})
            title.text = None
            title.append(lhtml.fragment_fromstring(f"<span>{_cell_html(tds[0])}</span>"))
            for i, td in enumerate(tds[1:], 1):
                body = _cell_html(td)
                if not body:
                    continue
                label = heads[i] if i < len(heads) else ""
                para = etree.SubElement(card, "p")
                if label:
                    lab = etree.SubElement(para, "span", {"class": "lab"})
                    lab.text = label
                para.append(lhtml.fragment_fromstring(f"<span>{body}</span>"))
        table.getparent().replace(table, wrap)


def clean(root):
    # drop boilerplate nav paragraphs
    for p in list(root.iter("p")):
        t = " ".join(p.text_content().split()).lower()
        if t.startswith(DROP_PREFIX):
            p.getparent().remove(p)
    # in-book anchors would break after chapter splitting: unwrap
    for a in list(root.iter("a")):
        href = a.get("href", "")
        if href.startswith("#") or (href and not href.startswith("http")):
            a.drop_tag()
    # figures
    for img in root.iter("img"):
        par = img.getparent()
        if par is not None and par.tag == "p" and len(par) == 1 and not (par.text or "").strip():
            par.set("class", "fig")


def split_sections(root):
    """Yield (level, title, [elements]) split at h1/h2."""
    sections, cur = [], [1, None, []]
    for el in root:
        if el.tag in ("h1", "h2"):
            if cur[1] is not None or cur[2]:
                sections.append(tuple(cur))
            cur = [int(el.tag[1]), " ".join(el.text_content().split()), [el]]
        else:
            cur[2].append(el)
    if cur[1] is not None or cur[2]:
        sections.append(tuple(cur))
    return sections


def to_xhtml(elements):
    return "".join(etree.tostring(e, encoding="unicode", method="xml") for e in elements)


DEFAULT_COVER = {
    "title": "CyberSci<br>Offline<br>Library",
    "subtitle": "Study guide for the 2026 regionals",
    "bullets": ["Method and competition day", "Forensics · Web · Crypto · Rev/pwn",
                "Network, privesc and AD", "Field map · Worked writeups · Mock exam", "Bandit 0-33 walkthrough"],
    "g1": "#0f2742", "g2": "#1d4ed8",
}


def render_cover(path, spec=None):
    spec = {**DEFAULT_COVER, **(spec or {})}
    lis = "".join(f"<li>{b}</li>" for b in spec["bullets"])
    html = ("<!doctype html><meta charset='utf-8'><style>"
            f"body{{margin:0;width:1000px;height:1500px;background:linear-gradient(160deg,{spec['g1']},{spec['g2']});"
            "color:#fff;font-family:Segoe UI,Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box}"
            "h1{font-size:104px;line-height:1.05;margin:0 0 40px}h2{font-size:44px;font-weight:400;margin:0 0 90px;opacity:.9}"
            "li{font-size:40px;margin:14px 0;opacity:.92}ul{padding-left:40px}.tag{font-size:34px;margin-top:100px;opacity:.7}"
            f"</style><h1>{spec['title']}</h1><h2>{spec['subtitle']}</h2><ul>{lis}</ul>"
            f"<div class='tag'>Built {date.today().isoformat()}</div>")
    with B.safe_tmp() as td:
        hp = Path(td) / "cover.html"
        hp.write_text(html, encoding="utf-8")
        path.unlink(missing_ok=True)
        cmd = [str(B.EDGE[0]), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--hide-scrollbars", f"--user-data-dir={Path(td) / 'p'}", "--window-size=1000,1500",
               f"--screenshot={path}", hp.as_uri()]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    proc.wait(timeout=1)
                    break
                except subprocess.TimeoutExpired:
                    if path.exists() and path.stat().st_size > 1000:
                        s1 = path.stat().st_size
                        time.sleep(1.5)
                        if path.stat().st_size == s1:
                            break
        finally:
            if proc.poll() is None:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return path.exists()


def make_epub_v2(out_path, title, books, cover_spec=None, heroes=None):
    """books: [(book_title, [md paths or '__plan__'])]"""
    images = {}

    def sink(p, alt):
        key = str(p)
        if key not in images:
            tag = hashlib.md5(key.encode()).hexdigest()[:6]
            images[key] = f"{p.parent.parent.name}-{tag}-{p.name}"
        return f"![{alt}](images/{images[key]})"

    generated = {}     # name -> svg text (ASCII diagrams rendered to SVG)
    chapters = []      # (file, part_idx, title, xhtml)
    nav = []           # [(book_title, first_file, [(file, title)])]
    n = 0
    for bi, (btitle, files) in enumerate(books):
        parts = []
        for f in files:
            if f == "__plan__":
                text, base = B.build_plan_md(), B.ROOT / "tracker"
            else:
                text, base = B.read_md(f), f.parent
            parts.append(B.md_to_html(B.preprocess(text, base, sink), xhtml=True))
        root = lhtml.fragment_fromstring("\n".join(parts), create_parent="div")
        tables_to_cards(root)
        clean(root)
        V.callouts(root)

        def emit(svg_text):
            name = f"diag-{V.digest(svg_text)}.svg"
            generated[name] = svg_text
            return f"images/{name}"
        V.convert_ascii_blocks(root, emit)
        # part title page
        n += 1
        part_file = f"ch{n:03d}.xhtml"
        hero = find_img((heroes or HERO)[bi % len(heroes or HERO)])
        hero_html = ""
        if hero is not None:
            key = str(hero)
            if key not in images:
                tag = hashlib.md5(key.encode()).hexdigest()[:6]
                images[key] = f"{hero.parent.parent.name}-{tag}-{hero.name}"
            hero_html = f'<div class="fig hero"><img src="images/{images[key]}" alt=""/></div>'
        part_x = (f'<div class="part"><h1>{btitle}</h1><p>Part {bi + 1} of {len(books)}</p></div>{hero_html}')
        chapters.append((part_file, bi, btitle, part_x))
        entry = (btitle, part_file, [])
        for lvl, stitle, els in split_sections(root):
            if not els:
                continue
            n += 1
            fn = f"ch{n:03d}.xhtml"
            chapters.append((fn, bi, stitle or btitle, to_xhtml(els)))
            if stitle:
                entry[2].append((fn, stitle))
        nav.append(entry)

    # cover
    cover_png = Path(tempfile.gettempdir()) / f"cybersci_cover_{hashlib.md5(title.encode()).hexdigest()[:6]}.png"
    has_cover = render_cover(cover_png, cover_spec)

    uid = "urn:uuid:" + hashlib.md5((title + date.today().isoformat()).encode()).hexdigest()
    manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
    spine = []
    if has_cover:
        manifest.append('<item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>')
        manifest.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
        spine.append('<itemref idref="cover"/>')
    for fn, _, _, _ in chapters:
        manifest.append(f'<item id="{fn[:-6]}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fn[:-6]}"/>')
    for k, name in enumerate(sorted(set(images.values()) | set(generated))):
        manifest.append(f'<item id="img{k}" href="images/{name}" media-type="image/svg+xml"/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           f'<dc:identifier id="uid">{uid}</dc:identifier><dc:title>{title}</dc:title><dc:language>en</dc:language>'
           f'<dc:creator>CyberSci prep</dc:creator><meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta>'
           + ('<meta name="cover" content="cover-img"/>' if has_cover else '') +
           f'</metadata><manifest>{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>')

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    nav_items = ""
    for btitle, first, secs in nav:
        sub = "".join(f'<li><a href="{fn}">{esc(t)}</a></li>' for fn, t in secs)
        nav_items += f'<li><a href="{first}">{esc(btitle)}</a>' + (f"<ol>{sub}</ol>" if sub else "") + "</li>"
    nav_x = ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" '
             'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Contents</title></head><body>'
             f'<nav epub:type="toc"><h1>Contents</h1><ol>{nav_items}</ol></nav></body></html>')
    container = ('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles></container>')
    cover_x = ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml">'
               '<head><title>Cover</title><link rel="stylesheet" href="style.css"/></head>'
               '<body class="cover"><img src="images/cover.png" alt="Cover"/></body></html>')

    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_x, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        if has_cover:
            z.write(cover_png, "OEBPS/images/cover.png", compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/cover.xhtml", cover_x, compress_type=zipfile.ZIP_DEFLATED)
        for fn, bi, t, body in chapters:
            x = ('<?xml version="1.0" encoding="utf-8"?>'
                 '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
                 f'<head><meta charset="utf-8"/><title>{esc(t)}</title><link rel="stylesheet" href="style.css"/></head>'
                 f'<body class="p{bi % len(ACCENTS)}">{body}</body></html>')
            z.writestr(f"OEBPS/{fn}", x, compress_type=zipfile.ZIP_DEFLATED)
        for src, name in images.items():
            z.write(src, f"OEBPS/images/{name}", compress_type=zipfile.ZIP_DEFLATED)
        for name, svg in generated.items():
            z.writestr(f"OEBPS/images/{name}", svg, compress_type=zipfile.ZIP_DEFLATED)
    return out_path, len(chapters)


# ---------------------------------------------------------------------------
# Flashcard EPUB: each card is two "pages" (question, then answer)
# ---------------------------------------------------------------------------
CARD_CSS = """
.qa { page-break-after: always; break-after: page; padding-top: 14%; }
.qa:last-child { page-break-after: auto; }
.tagline { font-size: .75em; letter-spacing: .08em; text-transform: uppercase; opacity: .65; margin-bottom: .6em; }
.badge { display: inline-block; padding: .1em .6em; border-radius: 6px; font-size: .75em; font-weight: bold; margin-bottom: .9em; }
.bq { background: rgba(37,99,235,.18); color: #2563eb; }
.ba { background: rgba(22,163,74,.18); color: #16a34a; }
.qtext { font-size: 1.45em; line-height: 1.35; font-weight: 600; }
.atext { font-size: 1.15em; line-height: 1.5; }
.counter { margin-top: 2em; font-size: .75em; opacity: .55; }
"""


def make_cards_epub(out_path, title, cards, cover_spec=None, hero="m1-triage-loop.svg", group_order=None):
    import html as H
    import re as _re
    IMG_RE = _re.compile(r"(?:<br>)?img:([\w\-.]+\.svg)")
    images = {}
    decks = {}
    for deck, front, back in cards:
        decks.setdefault(deck, []).append((front, back))
    order = group_order or list(decks)
    total = len(cards)
    chapters, nav = [], []
    n_all = 0
    for di, deck in enumerate(order):
        body = [f'<h1>{H.escape(deck)}</h1><p>{len(decks[deck])} cards. Read the question, answer in your head, turn the page.</p>',
                '<div style="page-break-after: always"></div>']
        for front, back in decks[deck]:
            n_all += 1
            btxt = IMG_RE.sub("", back).strip()
            ftxt = IMG_RE.sub("", front).strip()
            imgs = IMG_RE.findall(back)
            figs = ""
            for name in imgs:
                path = find_img(name)
                if path is None:
                    continue
                images.setdefault(str(path), f"{path.parent.parent.name}-{name}")
                figs += f'<div class="fig"><img src="images/{images[str(path)]}" alt=""/></div>'
            body.append(f'<div class="qa"><div class="tagline">{H.escape(deck)}</div><span class="badge bq">QUESTION</span>'
                        f'<div class="qtext">{ftxt}</div><div class="counter">card {n_all} of {total}</div></div>')
            body.append(f'<div class="qa"><div class="tagline">{H.escape(deck)}</div><span class="badge ba">ANSWER</span>'
                        f'<div class="atext">{btxt}</div>{figs}<div class="counter">card {n_all} of {total}</div></div>')
        chapters.append((f"deck{di + 1:02d}.xhtml", deck, "".join(body)))
        nav.append((f"deck{di + 1:02d}.xhtml", deck))

    cover_png = Path(tempfile.gettempdir()) / f"cybersci_cover_{hashlib.md5(title.encode()).hexdigest()[:6]}.png"
    has_cover = render_cover(cover_png, cover_spec)
    hero_path = find_img(hero)
    uid = "urn:uuid:" + hashlib.md5((title + date.today().isoformat()).encode()).hexdigest()

    manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
    spine = []
    if has_cover:
        manifest += ['<item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>',
                     '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>']
        spine.append('<itemref idref="cover"/>')
    for fn, _, _ in chapters:
        manifest.append(f'<item id="{fn[:-6]}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fn[:-6]}"/>')
    for k, name in enumerate(sorted(set(images.values()))):
        manifest.append(f'<item id="img{k}" href="images/{name}" media-type="image/svg+xml"/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           f'<dc:identifier id="uid">{uid}</dc:identifier><dc:title>{title}</dc:title><dc:language>en</dc:language>'
           f'<dc:creator>CyberSci prep</dc:creator><meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta>'
           + ('<meta name="cover" content="cover-img"/>' if has_cover else '') +
           f'</metadata><manifest>{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>')
    nav_x = ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" '
             'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Contents</title></head><body><nav epub:type="toc"><h1>Decks</h1><ol>'
             + "".join(f'<li><a href="{fn}">{H.escape(t)}</a></li>' for fn, t in nav) + '</ol></nav></body></html>')
    container = ('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    cover_x = ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Cover</title>'
               '<link rel="stylesheet" href="style.css"/></head><body class="cover"><img src="images/cover.png" alt="Cover"/></body></html>')

    def wrap(t, b):
        return ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml">'
                f'<head><meta charset="utf-8"/><title>{H.escape(t)}</title><link rel="stylesheet" href="style.css"/></head>'
                f'<body class="p0">{b}</body></html>')

    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_x, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS + CARD_CSS, compress_type=zipfile.ZIP_DEFLATED)
        if has_cover:
            z.write(cover_png, "OEBPS/images/cover.png", compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/cover.xhtml", cover_x, compress_type=zipfile.ZIP_DEFLATED)
        for fn, t, b in chapters:
            # validate/normalise fragment as XML
            frag = "".join(etree.tostring(c, encoding="unicode", method="xml")
                           for c in lhtml.fragment_fromstring(b, create_parent="div"))
            z.writestr(f"OEBPS/{fn}", wrap(t, frag), compress_type=zipfile.ZIP_DEFLATED)
        for src, name in images.items():
            z.write(src, f"OEBPS/images/{name}", compress_type=zipfile.ZIP_DEFLATED)
    return out_path, total, len(images)
