#!/usr/bin/env python3
"""Build phone-friendly offline books (PDF + EPUB) from the markdown study material.

PDF: Markdown -> HTML (phone CSS, inline-able SVG) -> Microsoft Edge headless print-to-pdf.
EPUB: hand-assembled EPUB3 (zipfile) so Apple Books can reflow text and render SVG.

    python scripts/build_offline.py            # builds into dist/offline/
    python scripts/build_offline.py --copy "C:/path/to/OneDrive/CyberSci-Offline"
"""
import argparse
import csv
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import date
from pathlib import Path

import markdown
from lxml import etree, html as lhtml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import visual as V  # noqa: E402

import contextlib


@contextlib.contextmanager
def safe_tmp():
    """Temp dir that never raises on cleanup (a lingering browser can hold files on Windows)."""
    d = tempfile.mkdtemp()
    try:
        yield d
    finally:
        try:
            shutil.rmtree(d, ignore_errors=True)
        except Exception:
            pass


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "offline"
C = ROOT / "curriculum"
# Chrome first: headless print-to-pdf did not produce output with Edge on this machine.
EDGE = [Path(p) for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                          r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                          r"C:\Program Files\Microsoft\Edge\Application\msedge.exe") if Path(p).exists()]

PAGE_W_MM, PAGE_H_MM = 130, 240   # fits an iPhone 15 portrait at ~1:1 text scale

CSS_PDF = f"""
@page {{ size: {PAGE_W_MM}mm {PAGE_H_MM}mm; margin: 9mm 7mm 10mm 7mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Segoe UI", Arial, Helvetica, sans-serif; font-size: 10.6pt; line-height: 1.42;
       color: #0f172a; margin: 0; }}
h1 {{ font-size: 18pt; margin: 0 0 4mm; padding-top: 2mm; border-bottom: 0.5mm solid #2563eb; page-break-before: always; }}
h1.first {{ page-break-before: avoid; }}
h2 {{ font-size: 14pt; margin: 6mm 0 2mm; color: #1d4ed8; }}
h3 {{ font-size: 12pt; margin: 5mm 0 1.5mm; }}
h4 {{ font-size: 11pt; margin: 4mm 0 1mm; }}
p, li {{ orphans: 2; widows: 2; }}
a {{ color: #1d4ed8; text-decoration: none; }}
img {{ max-width: 100%; height: auto; display: block; margin: 3mm auto; break-inside: avoid; }}
pre {{ background: #f1f5f9; border: 0.25mm solid #cbd5e1; border-radius: 2mm; padding: 2.2mm;
      font-family: Consolas, "Courier New", monospace; font-size: 6.3pt; line-height: 1.3;
      white-space: pre-wrap; word-break: break-word; }}
code {{ font-family: Consolas, "Courier New", monospace; font-size: 8.6pt; background: #eef2f7;
       padding: 0 0.8mm; border-radius: 1mm; word-break: break-word; }}
pre code {{ background: none; padding: 0; font-size: inherit; }}
table {{ border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 8.6pt; }}
th, td {{ border: 0.25mm solid #94a3b8; padding: 1.2mm 1.5mm; vertical-align: top; word-break: break-word; }}
th {{ background: #dbeafe; text-align: left; }}
tr {{ break-inside: avoid; }}
td code {{ font-size: 7.6pt; }}
blockquote {{ margin: 3mm 0; padding: 1.5mm 3mm; border-left: 1mm solid #d97706; background: #fffbeb; }}
kbd {{ border: 0.25mm solid #94a3b8; border-bottom-width: 0.6mm; border-radius: 1mm; padding: 0 1mm;
      font-size: 8.6pt; background: #fff; }}
hr {{ border: none; border-top: 0.3mm solid #cbd5e1; margin: 5mm 0; }}
.cover {{ text-align: center; padding-top: 55mm; }}
.cover h1 {{ border: none; font-size: 24pt; page-break-before: avoid; }}
.toc li {{ margin: 0.8mm 0; }}
"""

CSS_EPUB = """
body { font-family: -apple-system, Helvetica, Arial, sans-serif; line-height: 1.45; margin: 0 4%; }
h1 { font-size: 1.5em; border-bottom: 2px solid #2563eb; padding-bottom: .2em; }
h2 { font-size: 1.25em; color: #1d4ed8; margin-top: 1.4em; }
h3 { font-size: 1.1em; }
img { max-width: 100%; height: auto; display: block; margin: .8em auto; }
pre { background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: .6em;
      font-family: Menlo, Courier, monospace; font-size: .72em; white-space: pre-wrap; word-wrap: break-word; }
code { font-family: Menlo, Courier, monospace; font-size: .85em; background: #eef2f7; padding: 0 .2em; border-radius: 3px; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: .85em; }
th, td { border: 1px solid #94a3b8; padding: .3em .4em; vertical-align: top; word-wrap: break-word; }
th { background: #dbeafe; text-align: left; }
blockquote { margin: .8em 0; padding: .3em .8em; border-left: 4px solid #d97706; background: #fffbeb; }
"""

CSS_PDF += V.CSS_CALLOUTS + """
.fig.diagram img { width: 100%; max-height: none; margin: 3mm 0; }
"""


# ---------------------------------------------------------------- content
def csv_table(path, cols, headers, limit=None):
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows[:limit]:
        out.append("| " + " | ".join(str(r.get(c, "")).replace("|", "\\|") for c in cols) + " |")
    return "\n".join(out)


def build_plan_md():
    t = ROOT / "tracker"
    parts = ["# Study plan and trackers\n",
             f"Snapshot built {date.today().isoformat()}. The live plan is `tracker/tracker.csv` on your laptop.\n"]
    daily = (t / "DAILY.md").read_text(encoding="utf-8")
    parts.append(re.sub(r"^# .*\n", "", daily, count=1).replace("## ", "### "))
    parts.append("\n# Roadmap after the qualifier\n")
    rm = (t / "ROADMAP.md").read_text(encoding="utf-8")
    parts.append(re.sub(r"^# .*\n", "", rm, count=1).replace("## ", "## ").replace("### ", "### "))
    parts.append("\n# Reading and listening list\n")
    parts.append(csv_table(t / "reading.csv", ["id", "title", "type", "cost", "est_hours"],
                           ["ID", "Title", "Type", "Cost", "Hours"]))
    parts.append("\n# Toolkit checklist\n")
    parts.append(csv_table(t / "toolkit.csv", ["type", "name", "priority", "status"],
                           ["Type", "Name", "Pri", "Status"]))
    return "\n".join(parts)


def read_md(p):
    return p.read_text(encoding="utf-8")


BOOKS = [
    ("01-CTF-Method-and-Competition-Day", "1. CTF method and competition day", [C / "modules/01-ctf-method-and-competition-day.md"]),
    ("02-Forensics-and-Network", "2. Forensics and network analysis", [C / "modules/02-forensics-and-network.md"]),
    ("03-Web-Exploitation", "3. Web exploitation", [C / "modules/03-web-exploitation.md"]),
    ("04-Crypto-and-Encodings", "4. Cryptography and encodings", [C / "modules/04-crypto-and-encodings.md"]),
    ("05-Reverse-and-Pwn", "5. Reverse engineering and pwn", [C / "modules/05-reverse-and-pwn.md"]),
    ("06-Privesc-Network-and-AD", "6. Network, privesc and AD", [C / "modules/06-privesc-network-and-ad.md"]),
    ("07-Cheat-Sheets", "7. Cheat sheets", [C / "modules/07-cheat-sheets.md"]),
    ("08-Cybersecurity-Field-Map", "8. The cybersecurity field map", [C / "modules/08-cybersecurity-field-map.md"]),
    ("09-Worked-Writeups", "9. Worked writeups", [C / "modules/09-worked-writeups.md"]),
    ("10-Mock-Exam", "10. Mock exam", [C / "modules/10-mock-exam.md"]),
    ("11-Scripting-for-CTF", "11. Scripting for CTFs", [C / "modules/11-scripting-for-ctf.md"]),
    ("12-OSINT-and-Misc", "12. OSINT and misc", [C / "modules/12-osint-and-misc.md"]),
    ("13-Windows-Forensics", "13. Windows forensics", [C / "modules/13-windows-forensics.md"]),
    ("14-Cloud-Security-Basics", "14. Cloud security basics", [C / "modules/14-cloud-security-basics.md"]),
    ("15-Labs-and-Offline-References", "15. Labs and offline references", [C / "modules/15-labs-and-offline-references.md"]),
    ("16-Review-System-and-Progress-Log", "16. Review system and progress log", [C / "modules/16-review-system-and-progress-log.md"]),
    ("17-Bandit-Practice-Guide", "Bandit practice guide (0-33)", [C / "bandit/README.md"]),
    ("18-Bandit-Command-Encyclopedia", "Bandit command encyclopedia", [C / "bandit/commands.md"]),
    ("19-Bandit-Walkthrough", "Bandit full walkthrough", [C / "bandit/walkthrough-1-basics.md", C / "bandit/walkthrough-2-keys-network.md",
                                                       C / "bandit/walkthrough-3-cron-escape.md", C / "bandit/walkthrough-4-git-finish.md"]),
    ("20-CyberSci-Intel-and-Sources", "CyberSci intel, skills and sources", [C / "cybersci-writeups.md", C / "practice-suite.md", C / "sources.md"]),
    ("21-Study-Plan", "Study plan and trackers", ["__plan__"]),
    ("23-Learn-by-Doing-and-Written-Labs", "23. Learn by doing: workflow and written labs", [C / "activities/17-learning-by-doing-workflow-and-written-labs.md"]),
    ("24-Official-Skills-and-Defence", "24. Official skills and defence challenges", [C / "activities/18-official-skills-and-defence-challenges.md"]),
    ("25-CyberSci-Past-Challenges", "25. CyberSci past challenges", [C / "activities/19-past-challenges-activity-book.md"]),
    ("26-TryHackMe-Activity-Book", "26. TryHackMe activity book", [C / "activities/20-tryhackme-activity-book.md"]),
    ("27-OverTheWire-Activity-Book", "27. OverTheWire activity book", [C / "activities/21-overthewire-activity-book.md"]),
    ("28-VulnHub-Activity-Book", "28. VulnHub activity book", [C / "activities/22-vulnhub-activity-book.md"]),
    ("29-picoCTF-Activity-Book", "29. picoCTF activity book", [C / "activities/23-picoctf-activity-book.md"]),
    ("30-Parrot-and-Cybrary-Activity-Book", "30. Parrot CTFs and Cybrary activity book", [C / "activities/24-parrotctf-and-cybrary-activity-book.md"]),
    ("31-Writeups-Regionals-2025-26", "31. Writeups: Regionals 2025/26", [C / "pastchallenges/01-regionals-2025-26-writeups.md"]),
    ("32-Writeups-Regionals-2024-25", "32. Writeups: Regionals 2024/25", [C / "pastchallenges/02-regionals-2024-25-writeups.md"]),
    ("33-Past-Challenge-Primers-and-Drills", "33. Past-challenge primers and drills", [C / "pastchallenges/03-past-challenge-primers-and-drills.md"]),
    # OverTheWire full-depth books (hints + private solutions; for the learner's own phone only)
    ("34-OTW-Binary-Primer-and-Advanced-Games", "34. OverTheWire: binary primer and advanced games",
     [C / "overthewire/binary-primer.md", C / "overthewire/advanced-games.md", C / "overthewire/behemoth.md", C / "overthewire/manpage.md"]),
    ("35-OTW-Natas", "35. OverTheWire Natas (web)",
     [C / "overthewire/natas.md", C / "overthewire/solutions/natas-deep-1-levels-0-14.md", C / "overthewire/solutions/natas-solutions.md"]),
    ("36-OTW-Krypton", "36. OverTheWire Krypton (crypto)",
     [C / "overthewire/krypton.md", C / "overthewire/solutions/krypton-deep.md", C / "overthewire/solutions/krypton-solutions.md"]),
    ("37-OTW-Leviathan", "37. OverTheWire Leviathan (reverse basics)",
     [C / "overthewire/leviathan.md", C / "overthewire/solutions/leviathan-deep.md", C / "overthewire/solutions/leviathan-solutions.md"]),
    ("38-OTW-Narnia", "38. OverTheWire Narnia (binary exploitation, verified)",
     [C / "overthewire/narnia.md", C / "overthewire/solutions/narnia-solutions.md"]),
    ("39-Memory-Forensics-Deep-Book", "39. Memory forensics: the deep book", [C / "activities/25-memory-forensics-deep-book.md"]),
    ("40-Defence-Lab-Runbook", "40. Defence challenge lab runbook", [C / "activities/26-defence-lab-runbook.md"]),
    ("41-Nmap-and-Networking-Deep-Book", "41. Nmap and networking: the deep book", [C / "activities/27-nmap-and-networking-deep-book.md"]),
    ("42-Basic-SQL-Lab", "42. Basic SQL lab", [C / "activities/28-basic-sql-lab.md"]),
]


# ---------------------------------------------------------------- markdown -> html
DETAILS_OPEN = re.compile(r"<details>\s*<summary>(.*?)</summary>", re.S | re.I)


def preprocess(md_text, base_dir, image_sink):
    s = md_text
    s = DETAILS_OPEN.sub(lambda m: f"**▶ {m.group(1).strip()}**\n", s)
    s = re.sub(r"</details>", "", s, flags=re.I)
    s = re.sub(r"^(\s*)- \[ \] ", r"\1- ☐ ", s, flags=re.M)
    s = re.sub(r"^(\s*)- \[x\] ", r"\1- ☑ ", s, flags=re.M)
    # links to other markdown files become plain text; keep external and in-page anchors
    s = re.sub(r"\[([^\]]+)\]\((?!https?:)(?!#)[^)]*\.md[^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\((?!https?:)(?!#)(?!img)[^)]*/\)", r"\1", s)

    def img(m):
        alt, src = m.group(1), m.group(2)
        if src.startswith("http"):
            return m.group(0)
        p = (base_dir / src).resolve()
        phone = p.parent.parent / (p.parent.name + "-phone") / p.name
        if phone.exists():
            p = phone
        if not p.exists():
            return ""
        return image_sink(p, alt)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img, s)
    return s


def md_to_html(md_text, xhtml=False):
    return markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
                             extension_configs={"toc": {"permalink": False}},
                             output_format="xhtml" if xhtml else "html5")


def book_html(title, files, css, image_mode):
    body_parts = []
    for i, f in enumerate(files):
        if f == "__plan__":
            text, base = build_plan_md(), ROOT / "tracker"
        else:
            text, base = read_md(f), f.parent

        def sink(p, alt):
            return f"![{alt}]({p.as_uri()})"
        raw = md_to_html(preprocess(text, base, sink))
        root = lhtml.fragment_fromstring(raw, create_parent="div")
        V.callouts(root)
        V.convert_ascii_blocks(root, V.data_uri)
        body_parts.append((root.text or "") + "".join(etree.tostring(c, encoding="unicode", method="html") for c in root))
    body = "\n<hr/>\n".join(body_parts)
    body = body.replace("<h1", "<h1", 1)
    # mark the first h1 so it doesn't force a blank page
    body = re.sub(r"<h1", '<h1 class="first"', body, count=1)
    toc = "".join(f"<li>{t}</li>" for t in re.findall(r"<h1[^>]*>(.*?)</h1>", body))
    cover = (f'<div class="cover"><h1>{title}</h1><p>CyberSci 2026 offline study guide</p>'
             f'<p>Built {date.today().isoformat()} · iPhone-sized pages · vector diagrams</p></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{css}</style></head><body>{cover}{body}</body></html>')


# ---------------------------------------------------------------- PDF
def make_pdf(name, title, files):
    if not EDGE:
        sys.exit("Edge/Chrome not found")
    html = book_html(title, files, CSS_PDF, "file")
    with safe_tmp() as td:
        hp = Path(td) / "book.html"
        hp.write_text(html, encoding="utf-8")
        out = DIST / f"{name}.pdf"
        prof = Path(td) / "profile"      # separate profile so it never hands off to a running browser
        cmd = [str(EDGE[0]), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--disable-background-networking", "--disable-component-update",
               "--disable-sync", f"--user-data-dir={prof}", "--no-pdf-header-footer",
               "--generate-pdf-document-outline", f"--print-to-pdf={out}", hp.as_uri()]
        out.unlink(missing_ok=True)   # never mistake a stale file for fresh output
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(180):                      # up to ~3 minutes
                try:
                    proc.wait(timeout=1)
                    break
                except subprocess.TimeoutExpired:
                    # the browser can linger after writing the file: accept a stable, non-empty PDF
                    if out.exists() and out.stat().st_size > 1000:
                        s1 = out.stat().st_size
                        time.sleep(1.5)
                        if out.stat().st_size == s1:
                            break
        finally:
            if proc.poll() is None:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not out.exists():
            raise RuntimeError(f"PDF not produced for {name}")
    return out


# ---------------------------------------------------------------- EPUB
def xml_clean(fragment_html):
    root = lhtml.fragment_fromstring(fragment_html, create_parent="div")
    return "".join(etree.tostring(c, encoding="unicode", method="xml") for c in root) if len(root) else ""


def make_epub(out_path, title, chapters):
    """chapters: [(chapter_title, [md paths or '__plan__'])]"""
    images = {}   # source path -> epub name

    def sink_factory():
        def sink(p, alt):
            key = str(p)
            if key not in images:
                tag = hashlib.md5(key.encode()).hexdigest()[:6]
                images[key] = f"{p.parent.parent.name}-{tag}-{p.name}"
            return f"![{alt}](images/{images[key]})"
        return sink

    sink = sink_factory()
    items = []
    for n, (ctitle, files) in enumerate(chapters, 1):
        parts = []
        for f in files:
            if f == "__plan__":
                text, base = build_plan_md(), ROOT / "tracker"
            else:
                text, base = read_md(f), f.parent
            parts.append(md_to_html(preprocess(text, base, sink), xhtml=True))
        frag = xml_clean("\n".join(parts))
        xhtml = ('<?xml version="1.0" encoding="utf-8"?>'
                 '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
                 f'<head><meta charset="utf-8"/><title>{ctitle}</title><link rel="stylesheet" href="style.css"/></head>'
                 f'<body>{frag}</body></html>')
        items.append((f"ch{n:02d}.xhtml", ctitle, xhtml))

    uid = "urn:uuid:" + hashlib.md5(title.encode()).hexdigest()
    manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
    spine = []
    for fn, _, _ in items:
        manifest.append(f'<item id="{fn[:-6]}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fn[:-6]}"/>')
    for k, name in enumerate(sorted(set(images.values()))):
        manifest.append(f'<item id="img{k}" href="images/{name}" media-type="image/svg+xml"/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
           f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{uid}</dc:identifier>'
           f'<dc:title>{title}</dc:title><dc:language>en</dc:language>'
           f'<meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta></metadata>'
           f'<manifest>{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>')
    nav = ('<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" '
           'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Contents</title></head><body>'
           '<nav epub:type="toc"><h1>Contents</h1><ol>'
           + "".join(f'<li><a href="{fn}">{t}</a></li>' for fn, t, _ in items) + '</ol></nav></body></html>')
    container = ('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles></container>')
    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS_EPUB, compress_type=zipfile.ZIP_DEFLATED)
        for fn, _, x in items:
            z.writestr(f"OEBPS/{fn}", x, compress_type=zipfile.ZIP_DEFLATED)
        for src, name in images.items():
            z.write(src, f"OEBPS/images/{name}", compress_type=zipfile.ZIP_DEFLATED)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copy", help="also copy outputs to this folder (e.g. OneDrive)")
    ap.add_argument("--only", help="build only the PDF whose name starts with this prefix")
    ap.add_argument("--no-epub", action="store_true")
    ap.add_argument("--epub-only", action="store_true")
    a = ap.parse_args()
    DIST.mkdir(parents=True, exist_ok=True)
    outs = []
    for name, title, files in BOOKS:
        if a.epub_only or (a.only and not name.startswith(a.only)):
            continue
        for attempt in range(3):          # Chrome occasionally fails to print; retry
            try:
                out = make_pdf(name, title, files)
                break
            except RuntimeError:
                if attempt == 2:
                    raise
                time.sleep(3)
        print("pdf ", out.name, f"{out.stat().st_size/1024:.0f} KB")
        outs.append(out)
    if not a.no_epub and (a.epub_only or not a.only):
        from epub_builder import make_epub_v2
        ep, nch = make_epub_v2(DIST / "CyberSci-Offline-Library.epub", "CyberSci Offline Library",
                               [(t, f) for _, t, f in BOOKS])
        print("epub", ep.name, f"{ep.stat().st_size/1024:.0f} KB,", nch, "chapters")
        outs.append(ep)
    if a.copy:
        dst = Path(a.copy)
        dst.mkdir(parents=True, exist_ok=True)
        for o in outs:
            shutil.copy2(o, dst / o.name)
        print("copied to", dst)


if __name__ == "__main__":
    main()
