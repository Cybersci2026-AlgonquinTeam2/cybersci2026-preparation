#!/usr/bin/env python3
"""Copy a topic folder and plant known defects in it (for the Critic's planted-defect control, standards section 9).

    python tools/plant_defects.py TOPIC_DIR OUT_DIR   -> writes OUT_DIR/*.md and OUT_DIR/planted.json
Defect kinds: quiz-verdict-flipped, hint-4-removed, claim-with-unrelated-quote, sentence-negated, off-topic-sentence, skip-word-inserted.
"""
import json
import re
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
for f in src.glob("[1-9]-*.md"):
    shutil.copy(f, dst / f.name)
planted = []


def edit(fname, fn, kind):
    p = dst / fname
    if not p.exists():
        return
    lines = p.read_text(encoding="utf-8").splitlines()
    r = fn(lines)
    if r is None:
        return
    idx, new, old = r
    if new is None:
        del lines[idx]
        marker = lines[min(idx, len(lines) - 1)]
    else:
        lines[idx] = new
        marker = new
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    planted.append({"kind": kind, "file": fname, "line_after_edit": idx, "anchor_text": marker[:200], "original": old[:200]})


def flip_verdict(lines):
    for i, ln in enumerate(lines):
        if re.match(r"\s*- \([A-D]\) .* — right:", ln):
            return i, ln.replace("— right:", "— wrong:", 1), ln


def drop_hint4(lines):
    for i, ln in enumerate(lines):
        if re.match(r"\s*- Hint 4", ln):
            return i, None, ln


def bad_claim(lines):
    for i, ln in enumerate(lines):
        m = re.match(r"\| (C\d+) \| (.*?) \| VERIFY \| (Run|Not run) \| (.*) \|$", ln)
        if m:
            q = '"The weather in the northern region was mild for most of the autumn season."'
            return i, f"| {m.group(1)} | {m.group(2)} | {q} | Read | {m.group(4)} |", ln


def negate(lines):
    for i, ln in enumerate(lines):
        if re.match(r"^[A-Z][^|`#>*-].{50,200}\.$", ln) and " is " in ln:
            return i, ln.replace(" is ", " is not ", 1), ln


def off_topic(lines):
    for i, ln in enumerate(lines):
        if re.match(r"^[A-Z][^|`#>*-].{60,}\.$", ln) and i > 5:
            return i, ln + " The mitochondria is the powerhouse of the cell and was first described in the nineteenth century.", ln


def skip_word(lines):
    for i, ln in enumerate(lines):
        if re.match(r"^[A-Z][^|`#>*-].{60,}\.$", ln) and i > 12:
            return i, ln + " This is obviously the only correct way to do it.", ln


edit("3-retrieve.md", flip_verdict, "quiz-verdict-flipped")
edit("2-do.md", drop_hint4, "hint-4-removed")
edit("5-reference.md", bad_claim, "claim-with-unrelated-quote")
edit("1-learn.md", negate, "sentence-negated")
edit("4-transfer.md", off_topic, "off-topic-sentence")
edit("1-learn.md", skip_word, "skip-word-inserted")
(dst / "planted.json").write_text(json.dumps(planted, indent=1), encoding="utf-8")
print(f"planted {len(planted)} defects: {[p['kind'] for p in planted]}")
