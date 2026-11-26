#!/usr/bin/env python3
"""Deterministic gate for a depth page (structure, grounding, copy limit, honest labels, and RUNNING the lab commands).

    python depth/tools/gate.py PAGE.md [--pack SOURCEPACK.txt] [--data DIR] [--min-words N] [--json]
Exit 0 only when every FAIL-level check passes. This is evidence about structure and about whether the lab commands behave as the
page says; it is not a review and never promotes a page past `proposed` (standards/COMPREHENSIVE-STUDY-STANDARD.md s10).
Lab blocks look like:
    ```lab
    $ cut -d, -f2 sales.csv | sort | uniq -c
    expected output line 1
    ```
Commands run in a throw-away copy of --data with LC_ALL=C, a 10 s limit, no network, and only allow-listed programs.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MOVES = ["Orient", "Prime", "Intuition", "Foundations", "Mechanics", "Worked", "Compare", "Do it", "Repair", "Break", "Zoom", "Retrieve", "Transfer", "Teach", "Close"]
ALLOW = {"grep", "egrep", "awk", "sed", "cut", "sort", "uniq", "tr", "head", "tail", "wc", "cat", "jq", "ls", "echo", "printf", "paste", "column", "nl", "tac", "rev", "comm", "join", "basename", "dirname"}
BANNED_WORDS = ["simply", "just", "obviously", "trivially", "clearly", "of course"]
CARD_TYPES = ["concept", "cloze", "scenario", "contrast", "trace"]


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def strip_code(t):
    return re.sub(r"```.*?```", " ", t, flags=re.S)


def parse(page):
    m = re.match(r"---\n(.*?)\n---\n", page, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    body = page[m.end():] if m else page
    secs = {}
    cur = None
    for line in body.splitlines():
        h = re.match(r"^## (\d+)\.\s+(.*)", line)
        if h:
            cur = int(h.group(1))
            secs[cur] = [h.group(2), []]
        elif cur:
            secs[cur][1].append(line)
    return fm, body, {k: (v[0], "\n".join(v[1])) for k, v in secs.items()}


def lab_blocks(body):
    out = []
    for m in re.finditer(r"```lab\n(.*?)```", body, re.S):
        cmds, cur = [], None
        for line in m.group(1).splitlines():
            if line.startswith("$ "):
                cur = [line[2:], []]
                cmds.append(cur)
            elif cur is not None:
                cur[1].append(line)
        out.append([(c, "\n".join(e).rstrip()) for c, e in cmds])
    return out


def allowed(cmd):
    s = re.sub(r"'[^']*'|\"[^\"]*\"", "''", cmd)          # ignore quoted text (awk programs contain > and ;)
    if re.search(r"[;&`]|\$\(|>|\bsudo\b|\.\./|~|/etc/|/dev/", s):
        return False
    for part in s.split("|"):
        w = part.strip().split()
        if not w or w[0] not in ALLOW:
            return False
    return True


def fill_lab(page, data):
    """Replace the output under every `$ cmd` line in ```lab blocks with the real output. Returns (page, problems)."""
    problems = []
    with tempfile.TemporaryDirectory() as td:
        if data:
            for f in Path(data).iterdir():
                if f.is_file():
                    shutil.copy(f, td)

        def one(m):
            out_lines, cmd = [], None
            for line in m.group(1).splitlines():
                if line.startswith("$ "):
                    cmd = line[2:]
                    out_lines.append(line)
                    if not allowed(cmd):
                        problems.append((cmd, "command not allowed"))
                        continue
                    try:
                        p = subprocess.run(["bash", "-c", cmd], cwd=td, capture_output=True, text=True, timeout=10, env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"})
                    except subprocess.TimeoutExpired:
                        problems.append((cmd, "timeout"))
                        continue
                    if p.returncode != 0 or not p.stdout.strip():
                        problems.append((cmd, f"exit {p.returncode}, empty output" if not p.stdout.strip() else f"exit {p.returncode}"))
                    out_lines.extend(p.stdout.rstrip().splitlines())
            return "```lab\n" + "\n".join(out_lines) + "\n```"
        page = re.sub(r"```lab\n(.*?)```", one, page, flags=re.S)
    return page, problems


def run_lab(blocks, data):
    results = []
    with tempfile.TemporaryDirectory() as td:
        if data:
            for f in Path(data).iterdir():
                if f.is_file():
                    shutil.copy(f, td)
        for b in blocks:
            for cmd, want in b:
                if not allowed(cmd):
                    results.append((cmd, False, "command not allowed in the sandbox"))
                    continue
                try:
                    p = subprocess.run(["bash", "-c", cmd], cwd=td, capture_output=True, text=True, timeout=10, env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"})
                    got = p.stdout.rstrip()
                except subprocess.TimeoutExpired:
                    results.append((cmd, False, "timeout"))
                    continue
                g, w = [x.rstrip() for x in got.splitlines()], [x.rstrip() for x in want.splitlines()]
                results.append((cmd, g == w, "" if g == w else f"expected {w[:3]}... got {g[:3]}..."))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--pack")
    ap.add_argument("--data")
    ap.add_argument("--min-words", type=int, default=2800)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fill", action="store_true", help="first replace lab outputs with the real output (model-written pages carry commands only)")
    a = ap.parse_args()
    page = Path(a.page).read_text(encoding="utf-8")
    fill_problems = []
    if a.fill:
        page, fill_problems = fill_lab(page, a.data)
        Path(a.page).write_text(page, encoding="utf-8")
    fm, body, secs = parse(page)
    pack = norm(Path(a.pack).read_text(encoding="utf-8", errors="ignore")) if a.pack else ""
    checks = []   # (name, level, ok, detail)

    def add(name, ok, detail="", level="FAIL"):
        checks.append((name, level, bool(ok), detail))

    add("frontmatter fields", all(k in fm for k in ("id", "title", "category", "level", "status")), str({k: fm.get(k) for k in ("id", "status")}))
    add("status is proposed", fm.get("status") == "proposed", fm.get("status", ""))
    nums = sorted(secs)
    add("15 move headings in order", nums == list(range(1, 16)), f"found {nums}")
    miss = [MOVES[i - 1] for i in nums if 1 <= i <= 15 and MOVES[i - 1].lower() not in secs[i][0].lower()]
    add("heading names match the moves", not miss, f"mismatch: {miss}")
    words = len(re.findall(r"\S+", strip_code(body)))
    add("word count", words >= a.min_words, f"{words} words (min {a.min_words}; standard 4,000-6,000)")
    add("word count reaches the standard", words >= 4000, f"{words}", level="WARN")
    figs = [b for lang, b in re.findall(r"^```(\w*)\n(.*?)^```$", body, re.S | re.M) if lang == "" and re.search(r"[─│┌┐└┘►▼▲◄]|-->|──", b)]
    add("at least 4 figures", len(figs) >= 4, f"{len(figs)} figures")
    low = strip_code(body).lower()
    bad = [w for w in BANNED_WORDS if re.search(rf"\b{w}\b", low)]
    add("no skipped-step words", not bad, f"found {bad}")
    if a.fill:
        add("lab commands all exit 0 with output", not fill_problems, f"{len(fill_problems)} problems, first: {fill_problems[:1]}")
    # labs
    blocks = lab_blocks(body)
    ncmd = sum(len(b) for b in blocks)
    add("at least 6 lab commands with expected output", ncmd >= 6 and all(want for b in blocks for _, want in b), f"{ncmd} commands")
    if a.data and ncmd:
        res = run_lab(blocks, a.data)
        bad = [(c, d) for c, ok, d in res if not ok]
        add("every lab command runs and matches its expected output", not bad, f"{len(res) - len(bad)}/{len(res)} match; first problem: {bad[:1]}")
    else:
        add("lab commands run", False, "no --data given or no lab blocks: not run", level="WARN")
    # cards
    cards = re.findall(r"^- \[(\w+)\]\[(easy|medium|trap)\]", body, re.M)
    types = {c[0] for c in cards}
    add("flashcards: 15+ cards, all five types, difficulty tags", len(cards) >= 15 and set(CARD_TYPES) <= types, f"{len(cards)} cards, types {sorted(types)}")
    # quiz
    qs = re.findall(r"^\*\*Q\d+\.", body, re.M)
    opts = re.findall(r"^\s*- \([A-D]\) .* — (.{20,})", body, re.M)
    add("quiz: 5+ questions, every option explained", len(qs) >= 5 and len(opts) >= 4 * len(qs), f"{len(qs)} questions, {len(opts)} explained options")
    drills = re.findall(r"^\d+\. \*\*Drill\*\*", body, re.M)
    add("micro-drills: 5+ with answers", len(drills) >= 5, f"{len(drills)}")
    ladders = len(re.findall(r"^\s*- Hint 1:", body, re.M)), len(re.findall(r"^\s*- Hint 4:", body, re.M))
    add("four-tier hint ladders (3+)", ladders[0] >= 3 and ladders[1] >= 3, f"{ladders}")
    add("cheat sheet present", "cheat sheet" in secs.get(15, ("", ""))[1].lower() or "cheat sheet" in secs.get(15, ("", ""))[0].lower(), "")
    add("gap list present", "not covered by the captured source" in low or "gap list" in low, "")
    add("lab run status stated", "lab_run" in fm and fm["lab_run"], fm.get("lab_run", "")[:80])
    add("no review/acceptance claims", not re.search(r"\b(reviewed|accepted|polished|tested by)\b", fm.get("lab_run", "") + fm.get("status", ""), re.I), "")
    # claims register + grounding
    reg = secs.get(15, ("", ""))[1]
    rows = re.findall(r"^\| (C\d+) \| (.*?) \| (.*?) \| (Read|Listing read|Run|Not run) \| (.*?) \|", reg, re.M)
    add("claims register: 5+ rows with status words", len(rows) >= 5, f"{len(rows)} rows")
    ungrounded = []
    for cid, claim, quote, status, _ in rows:
        q = quote.strip()
        if q.upper().startswith("VERIFY"):
            continue
        if status == "Run":
            continue
        qt = norm(q.strip('"'))
        if len(qt.split()) < 8 or (pack and qt not in pack):
            ungrounded.append(cid)
    add("every Read claim quotes the source (8+ words, found in the pack) or is VERIFY", not ungrounded, f"ungrounded: {ungrounded}")
    # copy limit against the pack (outside the claims register and code)
    if pack:
        learner = norm(strip_code(body.replace(reg, "")))
        w = learner.split()
        pw = pack.split()
        shingles = {" ".join(pw[i:i + 8]) for i in range(len(pw) - 7)}
        hits = [i for i in range(len(w) - 7) if " ".join(w[i:i + 8]) in shingles]
        add("no 8-word runs copied from the source pack", not hits, f"{len(hits)} copied runs" + (f", e.g. {' '.join(w[hits[0]:hits[0] + 8])!r}" if hits else ""))
    fails = [c for c in checks if c[1] == "FAIL" and not c[2]]
    if a.json:
        print(json.dumps({"page": a.page, "pass": not fails, "words": words, "checks": [dict(name=n, level=l, ok=o, detail=d) for n, l, o, d in checks]}, indent=1))
    else:
        for n, l, o, d in checks:
            print(f"[{'PASS' if o else l}] {n}" + (f": {d}" if d and not o else ""))
        print(f"\n{'GATE PASSED' if not fails else 'GATE FAILED: ' + str(len(fails)) + ' checks'}  ({words} words)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
