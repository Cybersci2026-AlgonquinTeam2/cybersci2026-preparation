#!/usr/bin/env python3
"""Render mermaid flowcharts found in the Markdown study material to standalone SVG files for the offline pack.

    python scripts/render_mermaid.py            # scans practice-resources/ and curriculum/, writes dist/mermaid/<sha1>.svg

Needs internet at BUILD time only (loads mermaid from jsdelivr, pinned version) and headless Chrome. The finished SVGs
contain plain SVG text (no foreignObject) so Apple Books and PDF viewers render them offline.
build_offline.py swaps each mermaid block for its SVG when the file exists.
"""
import hashlib
import re
import subprocess
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "mermaid"
CHROME = next((Path(p) for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                 r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") if Path(p).exists()), None)
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"
BLOCK = re.compile(r"^(~~~|```)mermaid\b[^\n]*\n(.*?)^\1[ \t]*$", re.M | re.S)


def key(src):
    return hashlib.sha1(src.strip().encode("utf-8")).hexdigest()[:16]


def find_blocks():
    blocks = {}
    for base in ("practice-resources", "curriculum"):
        for p in (ROOT / base).rglob("*.md"):
            for m in BLOCK.finditer(p.read_text(encoding="utf-8")):
                blocks[key(m.group(2))] = m.group(2).strip()
    return blocks


def main():
    if not CHROME:
        raise SystemExit("Chrome not found")
    blocks = find_blocks()
    OUT.mkdir(parents=True, exist_ok=True)
    todo = {k: v for k, v in blocks.items() if not (OUT / f"{k}.svg").exists()}
    print(f"{len(blocks)} flowcharts, {len(todo)} to render")
    if not todo:
        return
    # one page per batch of diagrams keeps ids unique
    items = list(todo.items())
    for start in range(0, len(items), 6):
        batch = items[start:start + 6]
        body = "".join(f'<div class="d" id="d_{k}"><pre class="mermaid">{v.replace("&", "&amp;").replace("<", "&lt;")}</pre></div>' for k, v in batch)
        html = ('<!doctype html><html><head><meta charset="utf-8"></head><body>' + body +
                f'<script src="{MERMAID}"></script><script>mermaid.initialize({{startOnLoad:true, theme:"neutral", '
                'flowchart:{htmlLabels:false, useMaxWidth:false}});</script></body></html>')
        td = Path(tempfile.mkdtemp())
        try:
            f = td / "m.html"
            f.write_text(html, encoding="utf-8")
            prof = td / "profile"
            r = subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--virtual-time-budget=25000",
                                "--dump-dom", f.as_uri()], capture_output=True, timeout=180)
            dom = r.stdout.decode("utf-8", "replace")
            for k, _ in batch:
                m = re.search(rf'<div class="d" id="d_{k}">.*?(<svg.*?</svg>)', dom, re.S)
                if not m:
                    print("  failed:", k)
                    continue
                svg = m.group(1)
                vb = re.search(r'viewBox="([\d.\- ]+)"', svg)
                if vb:
                    x, y, w, h = [float(v) for v in vb.group(1).split()]
                    head, rest = svg.split(">", 1)
                    head = re.sub(r'\s(width|height)="[^"]*"', "", head)      # drop mermaid's own sizes (would duplicate)
                    head = head.replace("<svg ", f'<svg width="{w:.0f}" height="{h:.0f}" ', 1)
                    svg = head + ">" + rest
                    svg = re.sub(r'style="max-width:[^"]*;?"', "", svg, count=1)
                if "xmlns=" not in svg[:200]:
                    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
                (OUT / f"{k}.svg").write_text(svg, encoding="utf-8")
                print("  ok:", k, len(svg), "bytes")
        finally:
            shutil.rmtree(td, ignore_errors=True)


if __name__ == "__main__":
    main()
