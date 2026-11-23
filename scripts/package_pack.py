#!/usr/bin/env python3
"""Validate + package the full offline pack and sync it to OneDrive.

    python scripts/package_pack.py [--dest "C:/path/CyberSci-Offline"]
Run after build_offline.py, build_flashcards.py (both sets) and build_epubs.py.
"""
import argparse
import re
import shutil
import zipfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
OD, FC, EP = ROOT / "dist" / "offline", ROOT / "dist" / "flashcards", ROOT / "dist" / "epub"
DEFAULT_DEST = Path(r"C:\Users\jredj\OneDrive - Algonquin College\CyberSci-Offline")

README = """CyberSci offline study pack (built for iPhone 15, portrait)
===========================================================

START HERE: PDF 07 (cheat sheets), then 01 (method), then follow the order below.
For reading on the phone, the EPUB/ folder is nicer (font size, dark mode, search).

PDFs
  01 CTF method and competition day        12 OSINT and misc
  02 Forensics and network analysis        13 Windows forensics
  03 Web exploitation                      14 Cloud security basics
  04 Cryptography and encodings            15 Labs and offline references
  05 Reverse engineering and pwn           16 Review system and progress log
  06 Network, privesc and Active Directory 17 Bandit practice guide (0-33)
  07 Cheat sheets                          18 Bandit command encyclopedia
  08 The cybersecurity field map           19 Bandit full walkthrough
  09 Worked writeups                       20 CyberSci intel, skills, sources
  10 Mock exam (60 min, 100 points)        21 Study plan: daily plan, roadmap, readings
  11 Scripting for CTFs                    22 Flashcards flip deck (swipe: question, answer)
  LEARN BY DOING (read, do, review, reinforce, attempt 2):
  23 Workflow + 16 written labs            27 OverTheWire activity book
  24 Official skills + defence challenges  28 VulnHub activity book
  25 CyberSci past challenges              29 picoCTF activity book
  26 TryHackMe activity book               30 Parrot CTFs + Cybrary activity book
  PAST CHALLENGES (CyberSci's own releases):
  25 Past challenges: where to start       32 Writeups: Regionals 2024/25
  31 Writeups: Regionals 2025/26           33 Primers and 8 runnable drills
  OVERTHEWIRE (hints + solutions, private, for you only):
  34 Binary primer + advanced games        37 Leviathan
  35 Natas (web)                           38 Narnia (verified live 0-8)
  36 Krypton (crypto)
  SKILL DEEP DIVES:
  39 Memory forensics (Volatility 3)       40 Defence challenge lab runbook
  41 Nmap and networking deep book         42 Basic SQL lab
  43 TryHackMe free-room guide (117 rooms)  44 picoCTF guide
  45 VulnHub, Parrot CTFs, Cybrary guide
  50 Command Atlas (grep, find, sed, awk, file/xxd/strings, curl, nc, openssl)
  TEAM FIELD GUIDE (from the team repo): 46 triage and playbooks, 47-48 domain manuals, 49 competition day and team

EPUB/ (Apple Books)
  0 Complete Library          5 Intel and Study Plan
  1 Core Skills               6 Flashcards (Core, 456 cards)
  2 Field Map and Writeups    7 Flashcards (Bandit, 107 cards)
  3 Exam Prep and Cheat Sheets  8 Extra Skills (scripting, OSINT, Windows forensics, cloud)
  4 Bandit Complete           9 Labs and Review System
  10 Learn by Doing (workflow, labs, defence, platform books)
  11 Past Challenges (writeups, primers, drills)
  12 OverTheWire Complete (Natas, Krypton, Leviathan, Narnia, binary primer)
  13 Skill Deep Dives (memory forensics, defence runbook, Nmap)
  14 Field Guide and Competition Day (team repo material)
  15 Command Atlas

Flashcards/  Anki decks (.apkg, spaced repetition + diagrams), CSVs, flip-deck PDFs, review routine

Getting it onto the phone
  1. OneDrive app (Algonquin College account) -> CyberSci-Offline -> "..." -> Make available offline.
  2. Or save CyberSci-Offline-All.zip to Files (iOS unzips it) / AirDrop / email it to yourself.
  3. Test in Airplane mode.

Notes
  - AI tools are NOT allowed at CyberSci (organizers, 2026-10-15). Confirm the rules on notes and offline
    material before bringing anything into the event.
  - The study plan is a snapshot; the live tracker is tracker.csv in the cybersci-prep repo.
  - Bandit passwords are intentionally not included: you earn each one yourself.
  - Past challenges (external/PastChallenges), Workshops and CTFd repos are cloned in external/ (read-only study;
    do not run them outside a lab).
  - Labs (labs/docker-compose.yml) and the offline-reference script (scripts/fetch_offline_refs.py) are in
    the repo and are untested on your machine.
"""


def check_epub(p):
    z = zipfile.ZipFile(p)
    names = set(z.namelist())
    errs = 0
    for n in names:
        if n.endswith((".xhtml", ".opf")):
            try:
                etree.fromstring(z.read(n))
            except Exception:
                errs += 1
    miss = 0
    for n in names:
        if n.endswith(".xhtml"):
            try:
                root = etree.fromstring(z.read(n))
            except Exception:
                continue
            for img in root.iter("{http://www.w3.org/1999/xhtml}img"):   # real elements only, not code text
                s = img.get("src", "")
                if s and "OEBPS/" + s not in names:
                    miss += 1
    return errs, miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    a = ap.parse_args()
    dest = Path(a.dest)

    # flip deck gets the final number
    flip = FC / "CyberSci-Flashcards-FlipDeck.pdf"
    for old in OD.glob("*Flashcards-FlipDeck.pdf"):
        old.unlink()
    shutil.copy2(flip, OD / "22-Flashcards-FlipDeck.pdf")
    (OD / "README.txt").write_text(README, encoding="utf-8")

    bad = []
    for e in sorted(EP.glob("*.epub")):
        errs, miss = check_epub(e)
        print(f"{e.name:46s} xml_errors={errs} missing_images={miss}")
        if errs or miss:
            bad.append(e.name)
    if bad:
        raise SystemExit(f"EPUB validation failed: {bad}")

    pdfs = sorted(OD.glob("*.pdf"))
    fcfiles = sorted(p for p in FC.iterdir() if p.is_file() and p.suffix in {".apkg", ".csv", ".pdf", ".txt"})
    z = OD / "CyberSci-Offline-All.zip"
    z.unlink(missing_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in pdfs + [OD / "README.txt"]:
            zf.write(f, f"CyberSci-Offline/{f.name}")
        for f in sorted(EP.glob("*.epub")):
            zf.write(f, f"CyberSci-Offline/EPUB/{f.name}")
        for f in fcfiles:
            zf.write(f, f"CyberSci-Offline/Flashcards/{f.name}")
    # Command Atlas man pages: copy to the VM / Kali and run install-man.sh
    atlas = ROOT / "curriculum" / "atlas"
    man_files = sorted((atlas / "man" / "man1").glob("*.1")) + [atlas / "install-man.sh"]
    with zipfile.ZipFile(OD / "Atlas-Man.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for f in man_files:
            zf.write(f, ("man/man1/" if f.suffix == ".1" else "") + f.name)
        zf.writestr("README.txt", "Copy this zip into your Kali VM or WSL, unzip it, run: bash install-man.sh\nThen open a new terminal and try: man atlas   |   man atlas-grep   |   gm grep\n")
    ezip = EP / "CyberSci-EPUBs.zip"
    ezip.unlink(missing_ok=True)
    with zipfile.ZipFile(ezip, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(EP.glob("*.epub")):
            zf.write(f, f"CyberSci-EPUB/{f.name}")

    # sync: clear stale top-level files first so renumbered names don't linger
    dest.mkdir(parents=True, exist_ok=True)
    for old in list(dest.glob("*.pdf")) + list(dest.glob("*.epub")) + list(dest.glob("*.zip")):
        old.unlink()
    for f in pdfs + [OD / "README.txt", z, OD / "Atlas-Man.zip"]:
        shutil.copy2(f, dest / f.name)
    (dest / "EPUB").mkdir(exist_ok=True)
    for old in (dest / "EPUB").glob("*"):
        old.unlink()
    for f in list(EP.glob("*.epub")) + [ezip]:
        shutil.copy2(f, dest / "EPUB" / f.name)
    (dest / "Flashcards").mkdir(exist_ok=True)
    for old in (dest / "Flashcards").glob("*"):
        old.unlink()
    for f in fcfiles:
        shutil.copy2(f, dest / "Flashcards" / f.name)
    print(f"pdfs={len(pdfs)} epubs={len(list(EP.glob('*.epub')))} flashcard files={len(fcfiles)} "
          f"zip={z.stat().st_size // 1024} KB -> {dest}")


if __name__ == "__main__":
    main()
