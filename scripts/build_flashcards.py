#!/usr/bin/env python3
"""Build the CyberSci flashcard deck: Anki .apkg, CSV, and a phone-sized PDF flip deck.

    python scripts/build_flashcards.py [--copy FOLDER]
Source cards: flashcards/cards.py
"""
import argparse
import csv
import hashlib
import html
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import genanki

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
sys.path.insert(0, str(ROOT / "flashcards"))
import cards as MAIN  # noqa: E402
import bandit_cards as BANDIT  # noqa: E402

C = MAIN                      # active card set (switched by --set)
BASE = "CyberSci-Flashcards"  # output base name
IMG_DIRS = [ROOT / "curriculum" / "modules" / "img", ROOT / "curriculum" / "bandit" / "img-phone",
            ROOT / "curriculum" / "activities" / "img",
            ROOT / "curriculum" / "pastchallenges" / "img"]


def find_img(name):
    for d in IMG_DIRS:
        if (d / name).exists():
            return d / name
    raise FileNotFoundError(name)
OUT = ROOT / "dist" / "flashcards"
CHROME = [Path(p) for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if Path(p).exists()]

TITLE = "CyberSci flashcards"
IMG_RE = re.compile(r"(?:<br>)?img:([\w\-.]+\.svg)")


def stable_id(s, mod=1 << 31):
    return int(hashlib.sha1(s.encode()).hexdigest()[:8], 16) % mod + (1 << 30)


def split_images(text):
    names = IMG_RE.findall(text)
    return IMG_RE.sub("", text).strip(), names


def plain(text):
    t = re.sub(r"<br\s*/?>", "\n", text)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


# ----------------------------------------------------------------------- Anki
CSS = """
.card { font-family: -apple-system, Helvetica, Arial, sans-serif; font-size: 20px; line-height: 1.4;
        text-align: left; color: #0f172a; background: #ffffff; padding: 8px; }
.nightMode .card, .night_mode .card { color: #e5e7eb; background: #111827; }
code { font-family: Menlo, Consolas, monospace; font-size: 0.85em; background: #eef2f7; color:#0f172a;
       padding: 0 3px; border-radius: 3px; }
.deck { font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: #64748b; margin-bottom: 6px; }
img { max-width: 100%; height: auto; display: block; margin: 10px auto; background:#f8fafc; border-radius: 10px; }
hr#answer { margin: 12px 0; }
"""

BASIC = genanki.Model(
    1607392319, "CyberSci Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Deck"}],
    templates=[{"name": "Card 1",
                "qfmt": '<div class="deck">{{Deck}}</div>{{Front}}',
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'}],
    css=CSS)

REVERSED = genanki.Model(
    1607392320, "CyberSci Basic (and reversed)",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Deck"}],
    templates=[{"name": "Card 1",
                "qfmt": '<div class="deck">{{Deck}}</div>{{Front}}',
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'},
               {"name": "Card 2 (reverse)",
                "qfmt": '<div class="deck">{{Deck}} (reverse)</div>{{Back}}',
                "afmt": '{{FrontSide}}<hr id="answer">{{Front}}'}],
    css=CSS)


def build_apkg():
    decks, media = {}, set()
    parent = genanki.Deck(stable_id("CyberSci"), "CyberSci")
    for deck, front, back in C.CARDS:
        name = f"CyberSci::{deck}"
        if name not in decks:
            decks[name] = genanki.Deck(stable_id(name), name)
        back_txt, imgs = split_images(back)
        front_txt, fimgs = split_images(front)
        for n in imgs + fimgs:
            media.add(n)
        back_html = back_txt + "".join(f'<img src="{n}">' for n in imgs)
        front_html = front_txt + "".join(f'<img src="{n}">' for n in fimgs)
        model = REVERSED if deck in C.REV_DECKS else BASIC
        tag = re.sub(r"\W+", "_", deck)
        note = genanki.Note(model=model, fields=[front_html, back_html, deck], tags=[tag],
                            guid=genanki.guid_for(deck, front))
        decks[name].add_note(note)
    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = [str(find_img(n)) for n in sorted(media)]
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{BASE}.apkg"
    pkg.write_to_file(str(out))
    return out, len(media)


# ----------------------------------------------------------------------- CSV
def build_csv():
    out = OUT / f"{BASE}.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["deck", "front", "back", "tags"])
        for deck, front, back in C.CARDS:
            back_txt, _ = split_images(back)
            w.writerow([deck, plain(front), plain(back_txt), re.sub(r"\W+", "_", deck)])
    return out


# ----------------------------------------------------------------------- PDF flip deck
PDF_CSS = """
@page { size: 130mm 200mm; margin: 8mm 7mm; }
body { font-family: "Segoe UI", Arial, sans-serif; color:#0f172a; margin:0; }
.page { page-break-after: always; min-height: 180mm; display: flex; flex-direction: column; justify-content: center; }
.deck { font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color:#64748b; margin-bottom: 4mm; }
.n { font-size: 8.5pt; color:#94a3b8; margin-top: 6mm; }
.q { font-size: 17pt; line-height: 1.3; font-weight: 600; }
.a { font-size: 13.5pt; line-height: 1.4; }
.tag { display:inline-block; padding: 0.6mm 2.2mm; border-radius: 2mm; font-size: 8pt; margin-bottom: 4mm; }
.qtag { background:#dbeafe; color:#1d4ed8; } .atag { background:#dcfce7; color:#15803d; }
code { font-family: Consolas, monospace; font-size: 0.82em; background:#eef2f7; padding: 0 1mm; border-radius: 1mm; word-break: break-word; }
img { max-width: 100%; max-height: 105mm; height: auto; display:block; margin: 4mm auto 0; }
h1 { font-size: 26pt; } .cover { text-align: center; }
"""


def build_pdf():
    parts = [f'<div class="page cover"><h1>{TITLE}</h1>'
             f'<p>{len(C.CARDS)} cards · swipe: question page, then answer page</p>'
             '<p>Review the ones you miss again tomorrow.</p></div>']
    for i, (deck, front, back) in enumerate(C.CARDS, 1):
        back_txt, imgs = split_images(back)
        front_txt, fimgs = split_images(front)
        imgs_html = "".join(f'<img src="{find_img(n).as_uri()}">' for n in imgs)
        parts.append(f'<div class="page"><div class="deck">{html.escape(deck)}</div>'
                     f'<span class="tag qtag">QUESTION</span><div class="q">{front_txt}</div>'
                     f'<div class="n">card {i} / {len(C.CARDS)}</div></div>')
        parts.append(f'<div class="page"><div class="deck">{html.escape(deck)}</div>'
                     f'<span class="tag atag">ANSWER</span><div class="a">{back_txt}</div>{imgs_html}'
                     f'<div class="n">card {i} / {len(C.CARDS)}</div></div>')
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{PDF_CSS}</style></head><body>{"".join(parts)}</body></html>'
    out = OUT / f"{BASE}-FlipDeck.pdf"
    with safe_tmp() as td:
        hp = Path(td) / "deck.html"
        hp.write_text(doc, encoding="utf-8")
        out.unlink(missing_ok=True)
        cmd = [str(CHROME[0]), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--disable-background-networking", f"--user-data-dir={Path(td) / 'p'}",
               "--no-pdf-header-footer", f"--print-to-pdf={out}", hp.as_uri()]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(240):
                try:
                    proc.wait(timeout=1)
                    break
                except subprocess.TimeoutExpired:
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
        raise RuntimeError("flip-deck PDF not produced")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copy")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--set", choices=["main", "bandit"], default="main")
    a = ap.parse_args()
    global C, BASE, TITLE
    if a.set == "bandit":
        C, BASE, TITLE = BANDIT, "CyberSci-Bandit-Flashcards", "Bandit flashcards"
    else:
        TITLE = "CyberSci flashcards"
    OUT.mkdir(parents=True, exist_ok=True)
    apkg, nimg = build_apkg()
    print("apkg", apkg.name, f"{apkg.stat().st_size/1024:.0f} KB,", len(C.CARDS), "cards,", nimg, "images")
    csvp = build_csv()
    print("csv ", csvp.name)
    outs = [apkg, csvp]
    if not a.no_pdf:
        pdf = build_pdf()
        print("pdf ", pdf.name, f"{pdf.stat().st_size/1024:.0f} KB")
        outs.append(pdf)
    if a.copy:
        dst = Path(a.copy)
        dst.mkdir(parents=True, exist_ok=True)
        for o in outs:
            shutil.copy2(o, dst / o.name)
        print("copied to", dst)


if __name__ == "__main__":
    main()
