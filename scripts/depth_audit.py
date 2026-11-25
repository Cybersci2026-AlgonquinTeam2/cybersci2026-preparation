#!/usr/bin/env python3
"""Audit: what the depth standard asks for per backlog topic, how big that is, how long it takes by lane, and what already exists.

Run:  python scripts/depth_audit.py      (needs tracker/content_backlog.csv; run scripts/content_backlog.py first)
Writes tracker/DEPTH-AUDIT.md and tracker/depth_audit.csv. Sizes come from the standards:
  depth page 4,000-6,000 words (DEPTH-AND-RIGOR-STANDARD s2, s3), ~1 companion page of ~1,500 words per depth page (s3),
  exam arc extras per category (CURRICULUM-BLUEPRINT s2). Rates marked ASSUMPTION are not measured; the standard's measured
  figure is qwen3:8b on Machine B at 22.8 tokens/s. Existing content is counted from curriculum/ by file.
"""
import csv
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tracker"
WORDS = {"L1": 4000, "L2": 5000, "L3": 6000}         # depth page by level, inside the standard's 4,000-6,000
COMPANION = 1500                                    # words, one per depth page (standard s3: ~170 companions for 178 pages)
TOK_PER_WORD = 1.35                                 # standard s6
STRUCT_OVERHEAD = 1.3                               # tables, figures, code and cards cost more tokens per word (ASSUMPTION)
LOCAL_TPS = 22.8                                    # measured, qwen3:8b q4 on Machine B (standard s6)
LORA_TPS = (35, 45)                                 # 3-4B model with LoRA (ASSUMPTION in the standard)
RETRIES = (2, 4)                                    # passes a gated pipeline needs (standard s6)
FRONTIER_PAGES_PER_WINDOW = (6, 10)                 # depth pages per 5-hour usage window (ASSUMPTION: calibrate on the first 10)
LAB_RUN_H = (1, 2)                                  # standard s5.5: labs 1-2 h per domain page
REVIEW_MIN_PER_PAGE = 25                            # human or independent review per depth page (ASSUMPTION)

# existing files -> categories they cover (for the coverage comparison)
EXISTING = {
 "GEN": ["curriculum/modules/01-*", "curriculum/modules/11-*", "curriculum/bandit/*.md", "curriculum/atlas/*.md"],
 "WEB": ["curriculum/modules/03-*", "curriculum/activities/28-*"],
 "PWN": ["curriculum/modules/05-*"], "REV": ["curriculum/modules/05-*"],
 "CRY": ["curriculum/modules/04-*"],
 "FOR": ["curriculum/modules/02-*", "curriculum/modules/13-*", "curriculum/activities/25-*"],
 "NET": ["curriculum/modules/06-*", "curriculum/activities/27-*"],
 "AD": ["curriculum/modules/06-*"], "OSI": ["curriculum/modules/12-*"], "MSC": ["curriculum/modules/12-*", "curriculum/modules/11-*"],
 "CLD": ["curriculum/modules/14-*"], "BLU": ["curriculum/activities/26-*"],
}
SHARED = {"curriculum/modules/05-*": 2, "curriculum/modules/06-*": 2, "curriculum/modules/12-*": 2, "curriculum/modules/11-*": 2}


def words(p):
    return len(re.findall(r"\S+", p.read_text(encoding="utf-8", errors="ignore")))


def structure(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    return dict(words=len(re.findall(r"\S+", t)), h2=len(re.findall(r"^## ", t, re.M)), tables=len(re.findall(r"^\|[-: |]+\|$", t, re.M)),
                code=t.count("```") // 2, imgs=len(re.findall(r"!\[", t)),
                labs=len(re.findall(r"\blab\b", t, re.I)), quiz=len(re.findall(r"\b(quiz|drill|flashcard|hint)", t, re.I)))


def main():
    with (T / "content_backlog.csv").open(newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    with (T / "milestones.csv").open(newline="", encoding="utf-8") as f:
        ms = list(csv.DictReader(f))
    cats = defaultdict(list)
    for it in items:
        cats[it["category"]].append(it)
    names = {it["category"]: it["category_name"] for it in items}

    # ---- per-topic and per-category plan
    rows, plan = [], {}
    for c, its in cats.items():
        depth = sum(WORDS[i["level"]] for i in its)
        comp = COMPANION * len(its)
        n = len(its)
        extras = [("start-here page + entry diagnostic", 1, 1500), ("cumulative interleaved drills", math.ceil(n / 3), 1500),
                  ("integration: break-fix lab, design kata, capstone", 3, 1500), ("assessment: mastery ladder + mixed sets", 1, 1500),
                  ("category glossary", 1, 150 * n), ("source and gap register", 1, 1000)]
        ex_pages = sum(e[1] for e in extras)
        ex_words = sum(e[1] * e[2] for e in extras)
        plan[c] = dict(topics=n, depth_pages=n, companion_pages=n, extra_pages=ex_pages, depth_words=depth, companion_words=comp,
                       extra_words=ex_words, study_h=sum(float(i["study_hours"]) for i in its))
        for i in its:
            rows.append(dict(id=i["id"], category=c, topic=i["topic"], level=i["level"], depth_words=WORDS[i["level"]], companion_words=COMPANION,
                             pages=2, words=WORDS[i["level"]] + COMPANION, score=i["score"], study_hours=i["study_hours"]))
    event_pages = len(ms) - 1                         # one guide per event except the CyberSci debrief item
    event_words = event_pages * 1500
    tot = lambda k: sum(p[k] for p in plan.values())
    depth_pages, comp_pages, extra_pages = tot("depth_pages"), tot("companion_pages"), tot("extra_pages")
    total_pages = depth_pages + comp_pages + extra_pages + event_pages
    total_words = tot("depth_words") + tot("companion_words") + tot("extra_words") + event_words
    tokens = total_words * TOK_PER_WORD * STRUCT_OVERHEAD
    depth_tokens = (tot("depth_words") + tot("companion_words")) * TOK_PER_WORD * STRUCT_OVERHEAD

    # ---- time by lane
    def hours(tok, tps, retries):
        return tok / tps / 3600 * retries
    local_pass = tokens / LOCAL_TPS / 3600
    lanes = [("Local qwen3:8b, no LoRA, Machine B (22.8 tok/s measured)", local_pass * RETRIES[0], local_pass * RETRIES[1]),
             ("Local 3-4B + LoRA, Machine B (35-45 tok/s ASSUMPTION; training 1.5-4 h extra)", hours(tokens, LORA_TPS[1], RETRIES[0]) + 1.5, hours(tokens, LORA_TPS[0], RETRIES[1]) + 4)]
    windows = (math.ceil(depth_pages / FRONTIER_PAGES_PER_WINDOW[1]), math.ceil(depth_pages / FRONTIER_PAGES_PER_WINDOW[0]))
    lab_h = (depth_pages * LAB_RUN_H[0], depth_pages * LAB_RUN_H[1])
    review_h = depth_pages * REVIEW_MIN_PER_PAGE / 60

    # ---- existing content
    ex_rows, ex_words_by_cat = [], defaultdict(float)
    seen = {}
    for cat, pats in EXISTING.items():
        for pat in pats:
            for p in sorted(ROOT.glob(pat)):
                if p.is_file():
                    seen[p] = structure(p)
                    ex_words_by_cat[cat] += seen[p]["words"] / SHARED.get(pat, 1)
    for p, s in sorted(seen.items()):
        ex_rows.append((str(p.relative_to(ROOT)).replace("\\", "/"), s))

    # ---- write files
    with (T / "depth_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    o = ["# Depth audit: what the standard requires for the competition backlog", "",
         "Generated by `scripts/depth_audit.py` from `content_backlog.csv`. Sizes follow `standards/DEPTH-AND-RIGOR-STANDARD.md` (depth page 4,000-6,000 words, about one 1,500-word companion per depth page) and the exam arc in `standards/CURRICULUM-BLUEPRINT.md`. **Measured:** the 22.8 tokens/s of qwen3:8b on Machine B (from the standard). **Assumptions** are labelled; calibrate them on the first 10 pages.", "",
         "## 1. The headline", "",
         f"| Measure | Value |", "|---|---:|",
         f"| Backlog topics | {len(items)} in {len(cats)} categories |",
         f"| Depth pages (one per topic, 4,000 / 5,000 / 6,000 words by level L1 / L2 / L3) | {depth_pages} ({tot('depth_words'):,} words) |",
         f"| Companion pages (labs, drills, cheat sheet, cards; 1,500 words each) | {comp_pages} ({tot('companion_words'):,} words) |",
         f"| Category arc pages (start-here, cumulative drills, integration, assessment, glossary, gap register) | {extra_pages} ({tot('extra_words'):,} words) |",
         f"| Event guide pages (reading order, categories, diagnostic) for {event_pages} events | {event_pages} ({event_words:,} words) |",
         f"| **Total pages** | **{total_pages}** |", f"| **Total words** | **{total_words:,}** |",
         f"| Output tokens (words x 1.35 x 1.3 for tables and figures) | {tokens/1e6:.2f} million |",
         f"| Learner study time to work through it all (from the backlog) | {tot('study_h'):g} h |", "",
         "For scale: the current `curriculum/modules/` are 16 files and about 20,000 words; the whole `curriculum/` Markdown is about 103,000 words. The target is roughly "
         f"{total_words/103000:.0f} times everything written so far.", "",
         "## 2. Pages per category", "",
         "| Category | Topics | Depth pages | Companions | Arc pages | Words | Study h |", "|---|---:|---:|---:|---:|---:|---:|"]
    for c, p in sorted(plan.items(), key=lambda kv: -kv[1]["depth_words"]):
        o.append(f"| {c} {names[c]} | {p['topics']} | {p['depth_pages']} | {p['companion_pages']} | {p['extra_pages']} | "
                 f"{p['depth_words'] + p['companion_words'] + p['extra_words']:,} | {p['study_h']:g} |")
    o += ["", "Per topic the standard asks for one depth page built from the 15 moves (status banner, outcomes, predictions, intuition, foundations, mechanics, worked example with a faded copy, compare and decide, guided lab, mistakes, break-fix, zoom out, drills, quiz, five card types, transfer and design, teach-back and mastery ladder, cheat sheet, claims register, gap list) with at least 4 figures, plus one companion page. The per-topic list is in `tracker/depth_audit.csv`.", "",
          "## 3. How long it takes, by lane", "",
          f"Output volume is {tokens/1e6:.2f} million tokens. Pages are generated by section because they exceed the 8 thousand token context of the 8B setting.", "",
          "| Lane | Time | Basis |", "|---|---|---|"]
    for n, lo, hi in lanes:
        note = f"one pass is {local_pass:.0f} h at 22.8 tok/s; {RETRIES[0]}-{RETRIES[1]} passes with gates" if "no LoRA" in n else f"one pass is {tokens/LORA_TPS[1]/3600:.0f}-{tokens/LORA_TPS[0]/3600:.0f} h; {RETRIES[0]}-{RETRIES[1]} passes plus training"
        o.append(f"| {n} | {lo:.0f} to {hi:.0f} h of generation ({note}) | " + ("measured rate; retries from the standard" if "no LoRA" in n else "assumed rate; retries from the standard") + " |")
    o += [f"| Frontier agent writing the depth pages | about {windows[0]} to {windows[1]} five-hour usage windows ({FRONTIER_PAGES_PER_WINDOW[0]}-{FRONTIER_PAGES_PER_WINDOW[1]} depth pages per window) | **ASSUMPTION**, not measured |",
          f"| Running the labs and recording them | {lab_h[0]} to {lab_h[1]} h ({LAB_RUN_H[0]}-{LAB_RUN_H[1]} h per depth page) | standard s5.5 |",
          f"| Independent review of the depth pages | about {review_h:.0f} h ({REVIEW_MIN_PER_PAGE} min a page) | **ASSUMPTION** |", "",
          "Two things that change the plan: (1) a LoRA is only worth training after 40 to 60 reviewed frontier exemplars exist, so the first lane to run is frontier; (2) the local model should write only the derived blocks (flashcards, drills, quiz distractors and rationales, cheat-sheet tables, lab scaffolding, glossary), which is about a third of the words, so local time falls to roughly a third of the figures above.", "",
          "## 4. What already exists, measured against the standard", "",
          "| File | Words | `##` sections | Tables | Code blocks | Images | Lab mentions | Quiz/drill/card/hint mentions |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for path, s in ex_rows:
        o.append(f"| {path} | {s['words']:,} | {s['h2']} | {s['tables']} | {s['code']} | {s['imgs']} | {s['labs']} | {s['quiz']} |")
    o += ["", "The standard's benchmark page has about 5,400 words, 12.5 `##` sections, 5.6 tables and 8.4 code blocks. Today's modules average about 1,250 words and a handful of sections: they match the old short-lesson format, not the depth page.", "",
          "### Coverage by category (existing words against the depth target)", "",
          "| Category | Existing words (shared files split) | Depth + companion target | Covered |", "|---|---:|---:|---:|"]
    for c, p in sorted(plan.items(), key=lambda kv: kv[0]):
        have = ex_words_by_cat.get(c, 0)
        tgt = p["depth_words"] + p["companion_words"]
        o.append(f"| {c} {names[c]} | {have:,.0f} | {tgt:,} | {100 * have / tgt:.0f}% |")
    o += ["", "Existing material is not discarded: each existing module becomes a source for the depth pages in its category (the standard says the same about today's lessons). Counting words overstates coverage: none of it has labs with run status, five card types, per-option quiz rationales, claims registers or mastery ladders.", "",
          "## 5. What the standard requires that none of the existing content has", "",
          "- A claims register per page with Read / Listing read / Run / Not run status, and quotes or `VERIFY` for every factual claim. CTF topics have no certification blueprint, so the sources to capture are tool manual pages (the mangui guides are local copies), official tool and platform documentation and published writeups; none are captured yet.",
          "- Labs that were actually run, with the environment and result recorded. Free local labs can be run here; one SQL-injection lab exists in `labs/depth/` (21 of 21 checks run) but its page was not written.",
          "- Five flashcard types tagged easy, medium or trap, a four-tier hint ladder on every lab task, drill and quiz item, mastery ladder and teach-back to three audiences.",
          "- Figures: at least 4 per page; the existing modules have a few images each and no decision trees, sequence or trace figures.", "",
          "## 6. Recommended order", "",
          "1. **Safe-to-write categories first** (general skills, OSINT, log analysis, defence, misc, team ops, forensics, cloud): about a third of the topics; these seed the exemplar set.",
          "2. **Exemplars:** the 40 to 60 highest-score topics written by a frontier lane and reviewed (the LoRA training set).",
          "3. **Tooling:** page validator, figure helper, claims-register check, lab runner (the SQL lab runner is the pattern).",
          "4. **Local lane:** companions and derived blocks for every topic; depth prose for low-score topics only after the LoRA passes the held-out check.",
          "5. **Offensive categories** (web, pwn, reverse, crypto exploitation, AD, hardware) as defence-and-detection pages with hands-on labs run locally, subject to the safeguards noted in the conversation.", ""]
    (T / "DEPTH-AUDIT.md").write_text("\n".join(o), encoding="utf-8")
    print(f"{depth_pages} depth + {comp_pages} companion + {extra_pages} arc + {event_pages} event = {total_pages} pages, {total_words:,} words, {tokens/1e6:.2f} M tokens")
    for n, lo, hi in lanes:
        print(f"{n[:40]}: {lo:.0f}-{hi:.0f} h")
    print(f"frontier windows {windows}, labs {lab_h} h, review {review_h:.0f} h")


if __name__ == "__main__":
    main()
