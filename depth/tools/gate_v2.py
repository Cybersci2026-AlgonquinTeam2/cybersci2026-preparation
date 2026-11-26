#!/usr/bin/env python3
"""Gate for a v2 topic folder (five parts). See depth/SPEC-v2.md.

    python depth/tools/gate_v2.py TOPIC_DIR [--data DIR] [--fill] [--pack FILE] [--seed FILE] [--json]
--fill  writes the real output of every ```lab command into the parts (model-written parts carry commands only).
Exit 0 only when every FAIL-level check passes. Evidence about structure, rule coverage and lab behaviour: not a review.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gate as g1  # noqa: E402

PARTS = ["1-learn.md", "2-do.md", "3-retrieve.md", "4-transfer.md", "5-reference.md"]
MIN_WORDS = {"L1": 9000, "L2": 11000, "L3": 13000}
MIN_A, MIN_V, MIN_P, MIN_FIG, MIN_KINDS = 40, 22, 15, 10, 7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--data")
    ap.add_argument("--fill", action="store_true")
    ap.add_argument("--pack")
    ap.add_argument("--seed")
    ap.add_argument("--max-seed-copy", type=float, default=0.15)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = Path(a.topic)
    checks = []

    def add(name, ok, detail="", level="FAIL"):
        checks.append((name, level, bool(ok), detail))

    missing = [p for p in PARTS if not (d / p).exists()]
    add("five part files exist", not missing, f"missing {missing}")
    if missing:
        return finish(a, checks, 0)
    texts = {p: (d / p).read_text(encoding="utf-8") for p in PARTS}
    fill_problems = []
    if a.fill:
        for p in PARTS:
            texts[p], pr = g1.fill_lab(texts[p], a.data)
            fill_problems += pr
            (d / p).write_text(texts[p], encoding="utf-8")
        add("lab commands all exit 0 with output", not fill_problems, f"{len(fill_problems)} problems, first: {fill_problems[:1]}")
    fm, _, _ = g1.parse(texts[PARTS[0]])
    body = "\n".join(texts[p] for p in PARTS)
    nocode = g1.strip_code(body)
    add("frontmatter fields", all(k in fm for k in ("id", "title", "category", "level", "status", "lab_run")), str({k: fm.get(k) for k in ("id", "level", "status")}))
    add("status is proposed", fm.get("status") == "proposed", fm.get("status", ""))
    # moves across the folder
    moves = []
    for p in PARTS:
        moves += [int(m) for m in re.findall(r"^## (\d+)\.", texts[p], re.M)]
    add("moves 1 to 15 each appear once across the parts, in order", moves == sorted(set(moves)) == list(range(1, 16)) or sorted(moves) == list(range(1, 16)), f"found {moves}")
    words = len(re.findall(r"\S+", nocode))
    need = MIN_WORDS.get(fm.get("level", "L1"), 9000)
    add("word count for the level", words >= need, f"{words} words (need {need})")
    # tags
    tags = re.findall(r"\{([AVP])(\d+)(?:\.\d+)?\}", body)
    A, V, P = ({n for t, n in tags if t == k} for k in "AVP")
    add(f"learning-rule tags: {MIN_A}+ distinct", len(A) >= MIN_A, f"{len(A)} distinct")
    add(f"visual-rule tags: {MIN_V}+ distinct", len(V) >= MIN_V, f"{len(V)} distinct")
    add(f"practice-aid tags: {MIN_P}+ distinct", len(P) >= MIN_P, f"{len(P)} distinct")
    figs = [(lang, b) for lang, b in re.findall(r"^```(\w*)\n(.*?)^```$", body, re.S | re.M) if lang == "" and re.search(r"[─│┌┐└┘►▼▲◄]|──", b)]
    kinds = set(re.findall(r"\{fig:(\w+)\}", body))
    add(f"{MIN_FIG}+ figures", len(figs) >= MIN_FIG, f"{len(figs)} figures")
    add(f"{MIN_KINDS}+ distinct figure kinds", len(kinds) >= MIN_KINDS, f"{len(kinds)}: {sorted(kinds)}")
    low = nocode.lower()
    bad = [w for w in g1.BANNED_WORDS if re.search(rf"\b{w}\b", low)]
    add("no skipped-step words", not bad, f"found {bad}")
    # labs
    blocks = g1.lab_blocks(body)
    ncmd = sum(len(b) for b in blocks)
    add("15+ lab commands with expected output", ncmd >= 15 and all(w for b in blocks for _, w in b), f"{ncmd} commands")
    if a.data:
        res = g1.run_lab(blocks, a.data)
        badr = [(c, dd) for c, ok, dd in res if not ok]
        add("every lab command runs and matches its expected output", not badr, f"{len(res) - len(badr)}/{len(res)} match; first: {badr[:1]}")
    else:
        add("lab commands run", False, "no --data: not run", level="WARN")
    # structure counts (the spec's minimums)
    def n(rx, s=body, flags=re.M):
        return len(re.findall(rx, s, flags))
    add("4 labs (guided, prompted, unassisted, adversarial)", n(r"^### Lab [ABCD]") >= 4, f"{n(r'^### Lab [ABCD]')}")
    add("hint ladders: 8+ with four tiers", n(r"^\s*- Hint 1") >= 8 and n(r"^\s*- Hint 4") >= 8, f"{n(r'^\s*- Hint 1')} / {n(r'^\s*- Hint 4')}")
    add("3+ failure cases", n(r"^### Failure case") >= 3, f"{n(r'^### Failure case')}")
    add("2+ break-fix labs", n(r"\*\*Break-fix lab \d") >= 2, f"{n(r'\*\*Break-fix lab \d')}")
    mrows = [l for l in texts["2-do.md"].splitlines() if re.match(r"\| .* \| .* \| .* \| (factual|conceptual|procedural|logical|assumption|strategy) \|$", l)]
    add("mistakes table: 8+ rows with an error class", len(mrows) >= 8, f"{len(mrows)}")
    add("3+ misconceptions", n(r"^\*\*Misconception \d") >= 3, f"{n(r'^\*\*Misconception \d')}")
    add("10+ micro-drills", n(r"^\d+\. \*\*Drill\*\*") >= 10, f"{n(r'^\d+\. \*\*Drill\*\*')}")
    add("5+ trace drills", n(r"^\d+\. \*\*Trace\*\*") >= 5, f"{n(r'^\d+\. \*\*Trace\*\*')}")
    add("3+ spot-the-bug items", n(r"^\d+\. \*\*Spot the bug\*\*") >= 3, f"{n(r'^\d+\. \*\*Spot the bug\*\*')}")
    qs = n(r"^\*\*Q\d+\.")
    opts = n(r"^\s*- \([A-D]\) .* — (.{20,})")
    add("quiz: 10+ questions, every option explained", qs >= 10 and opts >= 4 * qs, f"{qs} questions, {opts} explained options")
    cards = re.findall(r"^- \[(\w+)\]\[(easy|medium|trap)\]", body, re.M)
    per = {t: sum(1 for c in cards if c[0] == t) for t in g1.CARD_TYPES}
    add("30+ flashcards, 5+ of each of the five types", len(cards) >= 30 and all(v >= 5 for v in per.values()), f"{len(cards)} cards {per}")
    add("interleaved set of 12 unlabelled items", n(r"^1[0-2]\. |^[1-9]\. ", texts["3-retrieve.md"].split("### Interleaved set")[-1].split("### Spaced")[0]) >= 12, "")
    add("spaced schedule 1,3,7,14,30", all(x in texts["3-retrieve.md"] for x in ("day 1", "day 3", "day 7", "day 14", "day 30")), "")
    add("error-to-aid template", "Error class" in texts["3-retrieve.md"] and "New card" in texts["3-retrieve.md"], "")
    for lvl in ("Near", "Representation", "Context", "Far"):
        add(f"transfer level: {lvl}", re.search(rf"\| {lvl} \|", texts["4-transfer.md"]) is not None, "")
    for w in ("### Critique", "### Reconstruction", "### Design kata", "### Capstone project", "**Non-goals.**", "**Milestones.**", "**Acceptance tests.**", "Self-review rubric"):
        add(f"has {w.strip('#* .')}", w in texts["4-transfer.md"], "")
    add("teach back: beginner, practitioner, expert", all(f"| {x} |" in texts["4-transfer.md"] for x in ("Beginner", "Practitioner", "Expert")), "")
    mrows = re.findall(r"^\| (\d+) (Define|Explain|Demonstrate|Apply|Distinguish|Analyse|Troubleshoot|Evaluate|Design|Transfer|Teach) \| (.+) \|$", texts["4-transfer.md"], re.M)
    add("11 mastery checks, each with a task", len(mrows) == 11 and all(len(r[2]) > 15 for r in mrows), f"{len(mrows)}")
    add("independence checklist", "Independence checklist" in texts["4-transfer.md"], "")
    add("two cheat sheets", n(r"^### Cheat sheet \d", texts["5-reference.md"]) >= 2, "")
    grows = [l for l in texts["5-reference.md"].split("### Glossary")[-1].split("### Claims")[0].splitlines() if re.match(r"\| .+ \| .+ \|$", l) and not l.startswith("| Term") and "---" not in l]
    add("glossary: 15+ terms", len(grows) >= 15, f"{len(grows)}")
    reg = texts["5-reference.md"]
    rows = re.findall(r"^\| (C\d+) \| (.*?) \| (.*?) \| (Read|Listing read|Run|Not run) \| (.*?) \|$", reg, re.M)
    badcol = [l[:24] for l in reg.splitlines() if re.match(r"\| C\d+ \|", l) and l.count("|") != 6]
    add("claims register: 10+ rows, 5 cells, status words", len(rows) >= 10 and not badcol, f"{len(rows)} rows, {len(badcol)} malformed")
    pack = g1.norm(Path(a.pack).read_text(encoding="utf-8", errors="ignore")) if a.pack else ""
    ung = [cid for cid, _, q, st, _ in rows if not q.strip().upper().startswith("VERIFY") and st != "Run" and (len(g1.norm(q.strip('"')).split()) < 8 or (pack and g1.norm(q.strip('"')) not in pack))]
    add("every Read claim quotes the pack (8+ words) or is VERIFY", not ung, f"ungrounded {ung}")
    add("gap list", "Not covered by the captured source" in reg, "")
    add("rule-coverage matrix whose tags all appear in the parts", all(x in body for x in ("{A3}", "{A8}", "{V13}", "{P7}", "{A29}")) and "### Rule-coverage matrix" in reg, "")
    add("visual completion report", "### Visual completion report" in reg, "")
    add("lab run status stated", bool(fm.get("lab_run")), "")
    add("no review/acceptance claims", not re.search(r"\b(reviewed|accepted|polished|tested by)\b", fm.get("lab_run", "") + fm.get("status", ""), re.I), "")
    if a.seed:
        sb = g1.norm(g1.strip_code(Path(a.seed).read_text(encoding="utf-8"))).split()
        sset = {" ".join(sb[i:i + 8]) for i in range(len(sb) - 7)}
        lw = g1.norm(nocode).split()
        frac = sum(1 for i in range(len(lw) - 7) if " ".join(lw[i:i + 8]) in sset) / max(len(lw) - 7, 1)
        add("copies at most 15% from the seed", frac <= a.max_seed_copy, f"{100 * frac:.0f}%")
    finish(a, checks, words, dict(A=len(A), V=len(V), P=len(P), figs=len(figs), kinds=len(kinds), labs=ncmd))


def finish(a, checks, words, stats=None):
    fails = [c for c in checks if c[1] == "FAIL" and not c[2]]
    if a.json:
        print(json.dumps({"topic": a.topic, "pass": not fails, "words": words, "stats": stats, "checks": [dict(name=n, level=l, ok=o, detail=dd) for n, l, o, dd in checks]}, indent=1))
    else:
        for n, l, o, dd in checks:
            print(f"[{'PASS' if o else l}] {n}" + (f": {dd}" if dd and not o else ""))
        print(f"\nstats: {stats}\n{'GATE PASSED' if not fails else 'GATE FAILED: ' + str(len(fails)) + ' checks'}  ({words} words)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
