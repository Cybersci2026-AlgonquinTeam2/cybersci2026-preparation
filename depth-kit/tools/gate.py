#!/usr/bin/env python3
"""Topic gate (standards section 8). Config-driven: thresholds, allow-lists, banned words and forbidden facts come from config/project.json.

    python tools/gate.py TOPIC_DIR [--spec SPEC.json] [--data DIR] [--fill] [--pack FILE] [--seed FILE_OR_DIR] [--json] [--config PATH]
TOPIC_DIR holds 1-learn.md ... 5-reference.md and optional extension parts 6-*.md to 9-*.md.
--fill   write the real output of every ```lab command into the parts (model-written parts carry commands only).
--spec   the topic spec (keywords, must_not_contain) for the topic-fit check.
--seed   a format-example page or folder: fail if more than max_seed_copy of the text repeats it in 8-word runs.
Exit 0 only when every FAIL-level check passes. A pass is evidence about structure, coverage and lab behaviour, never a review.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gatelib as L  # noqa: E402
import kitconfig  # noqa: E402

PARTS = ["1-learn.md", "2-do.md", "3-retrieve.md", "4-transfer.md", "5-reference.md"]


def main():
    cfg = kitconfig.load()
    argv = kitconfig.strip_argv(sys.argv[1:], "--config")
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--spec")
    ap.add_argument("--data")
    ap.add_argument("--fill", action="store_true")
    ap.add_argument("--pack")
    ap.add_argument("--seed")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    T = cfg["thresholds"]
    d = Path(a.topic)
    checks = []

    def add(name, ok, detail="", level="FAIL"):
        checks.append((name, level, bool(ok), detail))

    missing = [p for p in PARTS if not (d / p).exists()]
    add("five core part files exist", not missing, f"missing {missing}")
    if missing:
        return finish(a, checks, 0)
    ext = sorted(x.name for x in d.glob("[6-9]-*.md"))
    names = PARTS + ext
    texts = {p: (d / p).read_text(encoding="utf-8") for p in names}
    fill_problems = []
    if a.fill:
        for p in names:
            texts[p], pr = L.fill_lab(texts[p], a.data, cfg)
            fill_problems += pr
            (d / p).write_text(texts[p], encoding="utf-8")
        add("lab commands all exit 0 with output", not fill_problems, f"{len(fill_problems)} problems, first: {fill_problems[:1]}")
    fm, _ = L.parse(texts[PARTS[0]])
    body = "\n".join(texts[p] for p in names)
    nocode = L.strip_code(body)
    n = lambda rx, s=body: len(re.findall(rx, s, re.M))  # noqa: E731

    add("frontmatter fields", all(k in fm for k in ("id", "title", "category", "level", "status", "lab_run")), str({k: fm.get(k) for k in ("id", "level", "status")}))
    add("status is proposed", fm.get("status") == "proposed", fm.get("status", ""))
    moves = []
    for p in PARTS:
        moves += [int(m) for m in re.findall(r"^## (\d+)\.", texts[p], re.M)]
    add("moves 1 to 15 each appear once across the core parts", sorted(moves) == list(range(1, 16)), f"found {moves}")
    words = len(re.findall(r"\S+", nocode))
    need = T["min_words"].get(fm.get("level", "L1"), min(T["min_words"].values()))
    add("word count for the level", words >= need, f"{words} words (need {need})")

    # rule coverage against the catalog
    tags = re.findall(cfg["rules"]["tag_pattern"], body)
    got = {k: {int(i) for t, i in tags if t == k} for k in "AVP"}
    app = kitconfig.applicable_rules(cfg)
    unknown = {k: sorted(got[k] - set(int(x) for x in kitconfig.rule_catalog(cfg)[k])) for k in "AVP"}
    add("tags refer to rules in the catalog", not any(unknown.values()), f"unknown {unknown}")
    for k in "AVP":
        have = len(got[k] & app[k])
        add(f"rule tags {k}: {T['min_tags'][k]}+ distinct applicable rules", have >= T["min_tags"][k], f"{have} of {len(app[k])} applicable")
    figs = [b for lang, b in re.findall(r"^```(\w*)\n(.*?)^```$", body, re.S | re.M) if lang == "" and re.search(r"[─│┌┐└┘►▼▲◄]|──", b)]
    kinds = set(re.findall(r"\{fig:(\w+)\}", body))
    add(f"{T['min_figures']}+ figures", len(figs) >= T["min_figures"], f"{len(figs)}")
    add(f"{T['min_figure_kinds']}+ distinct figure kinds", len(kinds) >= T["min_figure_kinds"], f"{len(kinds)}: {sorted(kinds)}")

    # honesty
    low = nocode.lower()
    bad = [w for w in cfg["banned_words"] if re.search(rf"\b{re.escape(w)}\b", low)]
    add("no skipped-step words", not bad, f"found {bad}")
    reg_all = texts["5-reference.md"] + "\n" + texts.get("9-extended-reference.md", "")
    learner = "\n".join(x for x in nocode.splitlines() if not re.match(r"\| C\d+ \|", x))   # claims rows hold quotes by design
    ff = []
    for pat in cfg["forbidden_facts"]["patterns"]:
        for m in re.finditer(pat, learner, re.I):
            ctx = m.group(0)
            if ctx not in reg_all:                              # allowed only when a claims-register row records it
                ff.append(ctx)
    add("no forbidden facts outside the claims register", not ff, f"{len(ff)} found, e.g. {ff[:3]}")
    add("no review/acceptance claims in status fields", not re.search(r"\b(reviewed|accepted|polished|tested by)\b", fm.get("lab_run", "") + fm.get("status", ""), re.I), "")
    add("lab run status stated", bool(fm.get("lab_run")), "")

    # execution
    blocks = L.lab_blocks(body)
    ncmd = sum(len(b) for b in blocks)
    add(f"{cfg['labs']['min_commands']}+ lab commands with expected output", ncmd >= cfg["labs"]["min_commands"] and all(w for b in blocks for _, w in b), f"{ncmd} commands")
    if a.data:
        res = L.run_lab(blocks, a.data, cfg)
        badr = [(c, dd) for c, ok, dd in res if not ok]
        add("every lab command runs and matches its expected output", not badr, f"{len(res) - len(badr)}/{len(res)} match; first: {badr[:1]}")
    else:
        add("lab commands run", False, "no --data: not run", level="WARN")

    # counted elements
    lab_letters = n(r"^### Lab [A-G]")
    add("labs A to G", lab_letters >= T["min_labs"], f"{lab_letters}")
    h1, h4 = n(r"^\s*- Hint 1"), n(r"^\s*- Hint 4")
    add(f"hint ladders: {T['min_hint_ladders']}+ with four tiers", h1 >= T["min_hint_ladders"] and h4 >= T["min_hint_ladders"], f"{h1} / {h4}")
    add("failure cases", n(r"^### Failure case") >= T["min_failure_cases"], f"{n(r'^### Failure case')}")
    add("break-fix labs", n(r"\*\*Break-fix lab \d") >= T["min_break_fix"], f"{n(r'\*\*Break-fix lab \d')}")
    err = "|".join(cfg["error_classes"])
    mrows = [x for x in body.splitlines() if re.match(rf"\| .* \| .* \| .* \| ({err}) \|$", x)]
    add("mistake rows with an error class", len(mrows) >= T["min_mistake_rows"], f"{len(mrows)}")
    add("misconceptions", n(r"^\*\*Misconception \d") >= T["min_misconceptions"], f"{n(r'^\*\*Misconception \d')}")
    add("micro-drills", n(r"^\d+\. \*\*Drill\*\*") >= T["min_drills"], f"{n(r'^\d+\. \*\*Drill\*\*')}")
    add("trace drills", n(r"^\d+\. \*\*Trace\*\*") >= T["min_trace_drills"], f"{n(r'^\d+\. \*\*Trace\*\*')}")
    add("spot-the-bug items", n(r"^\d+\. \*\*Spot the bug\*\*") >= T["min_spot_bug"], f"{n(r'^\d+\. \*\*Spot the bug\*\*')}")
    qs, opts = n(r"^\*\*Q\d+\."), n(r"^\s*- \([A-D]\) .* — (.{20,})")
    add("quiz questions, every option explained", qs >= T["min_quiz"] and opts >= 4 * qs, f"{qs} questions, {opts} explained options")
    cards = re.findall(r"^- \[(\w+)\]\[(easy|medium|trap)\]", body, re.M)
    per = {t: sum(1 for c in cards if c[0] == t) for t in cfg["card_types"]}
    add("flashcards by type", len(cards) >= T["min_cards"] and all(v >= T["min_cards_per_type"] for v in per.values()), f"{len(cards)} cards {per}")
    il1 = texts["3-retrieve.md"].split("### Interleaved set")[-1].split("### Spaced")[0]
    il2 = texts.get("8-practice-bank.md", "").split("## C6")[-1].split("## C7")[0]
    add("interleaved items", n(r"^\d+\. ", il1) + n(r"^\d+\. ", il2) >= T["min_interleaved"], f"{n(r'^\d+\. ', il1)} + {n(r'^\d+\. ', il2)}")
    add("spaced schedule 1,3,7,14,30", all(x in texts["3-retrieve.md"] for x in ("day 1", "day 3", "day 7", "day 14", "day 30")), "")
    add("error-to-aid template", "Error class" in texts["3-retrieve.md"] and "New card" in texts["3-retrieve.md"], "")
    for lvl in ("Near", "Representation", "Context", "Far"):
        add(f"transfer level: {lvl}", re.search(rf"\| {lvl} \|", texts["4-transfer.md"]) is not None, "")
    for w in ("### Reconstruction", "### Capstone project", "**Non-goals.**", "**Milestones.**", "**Acceptance tests.**", "Self-review rubric"):
        add(f"has {w.strip('#* .')}", w in texts["4-transfer.md"], "")
    add("design katas and critiques", n(r"Design kata") >= T["min_katas"] and n(r"(?:### |\*\*)Critique") >= T["min_critiques"], f"{n(r'Design kata')} / {n(r'(?:### |\*\*)Critique')}")
    add("case studies", n(r"^### Case study") >= T["min_case_studies"], f"{n(r'^### Case study')}")
    add("teach back: beginner, practitioner, expert", all(f"| {x} |" in texts["4-transfer.md"] for x in ("Beginner", "Practitioner", "Expert")), "")
    ml = re.findall(r"^\| (\d+) (Define|Explain|Demonstrate|Apply|Distinguish|Analyse|Troubleshoot|Evaluate|Design|Transfer|Teach) \| (.+) \|$", texts["4-transfer.md"], re.M)
    add("11 mastery checks, each with a task", len(ml) == 11 and all(len(r[2]) > 15 for r in ml), f"{len(ml)}")
    add("independence checklist", "Independence checklist" in texts["4-transfer.md"], "")
    add("cheat sheets", n(r"^#{2,3} Cheat sheet \d", reg_all) >= T["min_cheat_sheets"], f"{n(r'^#{2,3} Cheat sheet \d', reg_all)}")
    gl = texts["5-reference.md"].split("### Glossary")[-1].split("### Claims")[0] + "\n" + texts.get("9-extended-reference.md", "").split("## Extended glossary")[-1].split("## Cheat sheet")[0]
    grows = [x for x in gl.splitlines() if re.match(r"\| .+ \| .+ \|$", x) and not x.startswith("| Term") and "---" not in x]
    add("glossary terms", len(grows) >= T["min_glossary"], f"{len(grows)}")

    # grounding
    rows = re.findall(r"^\| (C\d+) \| (.*?) \| (.*?) \| (Read|Listing read|Run|Not run) \| (.*?) \|$", reg_all, re.M)
    badcol = [x[:24] for x in reg_all.splitlines() if re.match(r"\| C\d+ \|", x) and x.count("|") != 6]
    add("claims register: rows, 5 cells, status words", len(rows) >= T["min_claims"] and not badcol, f"{len(rows)} rows, {len(badcol)} malformed")
    pack = L.norm(Path(a.pack).read_text(encoding="utf-8", errors="ignore")) if a.pack else ""
    ung = [cid for cid, _, q, st, _ in rows if not q.strip().upper().startswith("VERIFY") and st != "Run" and (len(L.norm(q.strip('"')).split()) < 8 or (pack and L.norm(q.strip('"')) not in pack))]
    add("every Read claim quotes the pack (8+ words) or is VERIFY", not ung, f"ungrounded {ung}")
    if pack:
        pf = L.copy_fraction(learner, pack)
        add("no 8-word runs copied from the source pack", pf == 0, f"{100 * pf:.1f}% of runs")
    add("gap list", "Not covered by the captured source" in reg_all, "")
    add("rule-coverage matrix", "### Rule-coverage matrix" in reg_all, "")
    add("visual completion report", "### Visual completion report" in reg_all, "")

    # originality and topic fit
    if a.seed:
        sp = Path(a.seed)
        seed_text = "\n".join(x.read_text(encoding="utf-8") for x in sorted(sp.glob("*.md"))) if sp.is_dir() else sp.read_text(encoding="utf-8")
        frac = L.copy_fraction(nocode, seed_text)
        add(f"copies at most {int(T['max_seed_copy'] * 100)}% from the seed", frac <= T["max_seed_copy"], f"{100 * frac:.0f}%")
    if a.spec:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        kw = spec.get("keywords", [])
        if kw:
            hit = [k for k in kw if re.search(re.escape(k), body, re.I)]
            add("topic fit: the page contains the topic's keywords", len(hit) / len(kw) >= cfg["topic_fit"]["min_keyword_fraction"], f"{len(hit)}/{len(kw)}; missing {[k for k in kw if k not in hit][:5]}")
        mnc = [t for t in spec.get("must_not_contain", []) if re.search(re.escape(t), body, re.I)]
        add("topic fit: nothing from another topic", not mnc, f"found {mnc}")
    finish(a, checks, words, dict(A=len(got["A"]), V=len(got["V"]), P=len(got["P"]), figs=len(figs), kinds=len(kinds), labs=ncmd, cards=len(cards)))


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
