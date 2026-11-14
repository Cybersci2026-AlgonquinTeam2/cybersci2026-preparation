#!/usr/bin/env python3
"""Build the themed EPUB set (plus the master library) into dist/epub/.

    python scripts/build_epubs.py [--copy FOLDER]
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "flashcards"))
import build_offline as B  # noqa: E402
import epub_builder as E  # noqa: E402
import cards as MAIN  # noqa: E402
import bandit_cards as BANDIT  # noqa: E402

OUT = B.ROOT / "dist" / "epub"
BOOK = {name[:2]: (title, files) for name, title, files in B.BOOKS}   # '01' -> (title, files)


def pick(*nums):
    return [BOOK[n] for n in nums]


SETS = [
    ("CyberSci-1-Core-Skills.epub", "CyberSci 1: Core Skills", pick("01", "02", "03", "04", "05", "06"),
     dict(title="Core<br>Skills", subtitle="Method · Forensics · Web · Crypto · Rev/pwn · Privesc/AD",
          bullets=["How to attack any challenge", "Packets, memory and logs", "Web: SQLi, XSS, JWT, SSRF",
                   "Crypto and encodings", "Reverse engineering and pwn", "Privesc and Active Directory"],
          g1="#0f2742", g2="#2563eb"),
     ["m1-triage-loop.svg", "f-pcap.svg", "w-method.svg", "c-recognize.svg", "r-compile.svg", "p-ad-path.svg"]),
    ("CyberSci-2-Field-Map-and-Writeups.epub", "CyberSci 2: Field Map and Worked Writeups", pick("08", "09"),
     dict(title="Field Map<br>and Worked<br>Writeups", subtitle="The wide view and how experts think",
          bullets=["Offense · Defense · Engineering · Governance", "Frameworks and careers", "Glossary of 50 terms",
                   "CyberSci cases explained", "10 archetype cases you can check by hand"],
          g1="#1f2a44", g2="#7c3aed"),
     ["fm-map.svg", "wc-template.svg"]),
    ("CyberSci-3-Exam-Prep-and-Cheat-Sheets.epub", "CyberSci 3: Exam Prep and Cheat Sheets", pick("07", "10"),
     dict(title="Exam Prep<br>and Cheat<br>Sheets", subtitle="Read the night before",
          bullets=["One-pagers per category", "Ports and magic bytes", "60-minute mock exam",
                   "Answer key and score map"],
          g1="#3b1d0f", g2="#d97706"),
     ["k-ports.svg", "wc-mock-plan.svg"]),
    ("CyberSci-4-Bandit-Complete.epub", "CyberSci 4: Bandit Complete", pick("17", "18", "19"),
     dict(title="Bandit<br>Complete", subtitle="Levels 0-33: practice, commands, full walkthrough",
          bullets=["Hint → solution practice guide", "Every command and flag explained",
                   "Per-level walkthrough with diagrams", "Retrieval questions and mastery checks"],
          g1="#052e2b", g2="#0d9488"),
     ["00-journey.svg", "05-pipes.svg", "09-setuid.svg"]),
    ("CyberSci-8-Extra-Skills.epub", "CyberSci 8: Scripting, OSINT, Windows Forensics, Cloud", pick("11", "12", "13", "14"),
     dict(title="Extra<br>Skills", subtitle="Scripting · OSINT · Windows forensics · Cloud",
          bullets=["Python and Bash for CTFs", "OSINT method and geolocation", "Windows artifacts and event logs",
                   "Cloud IAM, misconfigurations, metadata"],
          g1="#1a1a2e", g2="#0891b2"),
     ["s-loop.svg", "o-method.svg", "wf-artifacts.svg", "cl-iam.svg"]),
    ("CyberSci-9-Labs-and-Review-System.epub", "CyberSci 9: Labs and Review System", pick("15", "16"),
     dict(title="Labs and<br>Review<br>System", subtitle="Practice safely, remember everything",
          bullets=["Home lab layout and Docker labs", "Offline reference pack", "Spaced repetition and Leitner boxes",
                   "Weekly loop, skill ladder, logs"],
          g1="#14281d", g2="#16a34a"),
     ["lab-network.svg", "rv-leitner.svg"]),
    ("CyberSci-10-Learn-by-Doing-Activity-Books.epub", "CyberSci 10: Learn by Doing", pick("23", "24", "25", "26", "27", "28", "29", "30"),
     dict(title="Learn by<br>Doing", subtitle="Read, do, review, reinforce, repeat",
          bullets=["The workflow and 16 written labs", "Official skills and defence challenges", "CyberSci past challenges",
                   "TryHackMe · OverTheWire · VulnHub", "picoCTF · Parrot CTFs · Cybrary"],
          g1="#2b1055", g2="#7c3aed"),
     ["a-workflow.svg", "os-map.svg", "d-formats.svg", "a-room.svg", "a-ladders.svg", "a-box.svg", "a-platforms.svg", "a-card.svg"]),
    ("CyberSci-11-Past-Challenges-Writeups-and-Drills.epub", "CyberSci 11: Past Challenges", pick("25", "31", "32", "33"),
     dict(title="Past<br>Challenges", subtitle="Writeups, primers and drills from the organizers' releases",
          bullets=["Where to start and how to attempt", "Regionals 2025/26 writeups", "Regionals 2024/25 writeups",
                   "Primers: Enigma, PCBC, gopher, JWT, prompt injection", "8 runnable drills"],
          g1="#3b0f0f", g2="#dc2626"),
     ["pc-roadmap.svg", "pc-corpo.svg", "pc-pcbc.svg", "pc-trc.svg"]),
    ("CyberSci-12-OverTheWire-Complete.epub", "CyberSci 12: OverTheWire Complete", pick("34", "35", "36", "37", "38"),
     dict(title="OverTheWire<br>Complete", subtitle="Natas · Krypton · Leviathan · Narnia · binary primer",
          bullets=["Binary exploitation primer", "Natas 0-34 (web)", "Krypton 0-6 (crypto)", "Leviathan 0-7",
                   "Narnia 0-8 (verified live)"],
          g1="#102a43", g2="#0ea5e9"),
     ["os-map.svg"]),
    ("CyberSci-13-Skill-Deep-Dives.epub", "CyberSci 13: Skill Deep Dives", pick("39", "40", "41", "42"),
     dict(title="Skill<br>Deep Dives", subtitle="Memory forensics, defence challenge, Nmap and networking",
          bullets=["Memory forensics with Volatility 3", "Triage table and red flags", "Build your own memory image",
                   "Defence runbook and defender view", "Nmap and networking, incl. other subnets", "Basic SQL lab (offline)"],
          g1="#1f2937", g2="#f59e0b"),
     ["f-volatility.svg"]),
    ("CyberSci-5-Intel-and-Study-Plan.epub", "CyberSci 5: Intel and Study Plan", pick("20", "21"),
     dict(title="Intel and<br>Study Plan", subtitle="Past events, skills, sources, daily plan",
          bullets=["Past CyberSci challenge shapes", "Skills x methods x exercises", "Sources catalogue",
                   "Daily plan, roadmap, reading list"],
          g1="#2a0f1f", g2="#db2777"),
     ["fm-career.svg", "fm-certs.svg"]),
]

CARD_SETS = [
    ("CyberSci-6-Flashcards-Core.epub", "CyberSci 6: Flashcards (Core)", MAIN.CARDS,
     dict(title="Flashcards<br>Core", subtitle=f"{len(MAIN.CARDS)} cards across 11 decks",
          bullets=["Linux and Bandit", "Web · Crypto · Forensics", "Reverse and pwn", "Privesc and AD", "Field map and glossary"],
          g1="#0f2742", g2="#16a34a"), "m1-triage-loop.svg"),
    ("CyberSci-7-Flashcards-Bandit.epub", "CyberSci 7: Flashcards (Bandit)", BANDIT.CARDS,
     dict(title="Flashcards<br>Bandit", subtitle=f"{len(BANDIT.CARDS)} cards, level by level",
          bullets=["Task and first command", "Why it works", "Command to level", "Concepts"],
          g1="#052e2b", g2="#16a34a"), "00-journey.svg"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copy")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    outs = []
    for fname, title, books, cover, heroes in SETS:
        out, nch = E.make_epub_v2(OUT / fname, title, books, cover_spec=cover, heroes=heroes)
        print("epub", fname, f"{out.stat().st_size/1024:.0f} KB,", nch, "chapters")
        outs.append(out)
    for fname, title, cards, cover, hero in CARD_SETS:
        order = []
        for d, _, _ in cards:
            if d not in order:
                order.append(d)
        out, n, nimg = E.make_cards_epub(OUT / fname, title, cards, cover_spec=cover, hero=hero, group_order=order)
        print("epub", fname, f"{out.stat().st_size/1024:.0f} KB,", n, "cards,", nimg, "images")
        outs.append(out)
    master = OUT / "CyberSci-0-Complete-Library.epub"
    out, nch = E.make_epub_v2(master, "CyberSci Complete Library", [(t, f) for _, t, f in B.BOOKS])
    print("epub", master.name, f"{out.stat().st_size/1024:.0f} KB,", nch, "chapters")
    outs.append(out)
    if a.copy:
        dst = Path(a.copy)
        dst.mkdir(parents=True, exist_ok=True)
        for o in outs:
            shutil.copy2(o, dst / o.name)
        print("copied", len(outs), "files to", dst)


if __name__ == "__main__":
    main()
