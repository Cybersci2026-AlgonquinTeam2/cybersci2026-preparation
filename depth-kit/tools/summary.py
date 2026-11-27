#!/usr/bin/env python3
"""Summarise gate results for a trial directory: pass rate and which checks fail most. Usage: summary.py DIR"""
import json
import sys
from collections import Counter
from pathlib import Path

d = Path(sys.argv[1])
res = [(p, json.loads(p.read_text(encoding="utf-8"))) for p in sorted(d.glob("cand-*.gate.json")) if p.stat().st_size]
if not res:
    sys.exit("no gate results")
fails = Counter()
rows = []
for p, r in res:
    bad = [c["name"] for c in r["checks"] if c["level"] == "FAIL" and not c["ok"]]
    fails.update(bad)
    rows.append((p.name.replace(".gate.json", ""), r["words"], len(bad), r["pass"]))
n = len(res)
ok = sum(1 for r in rows if r[3])
out = [f"# Trial result: {d.name}", "", f"{ok} of {n} candidates passed every FAIL-level check ({100 * ok / n:.0f}%).", "",
       "| Candidate | Words | Failed checks | Passed |", "|---|---:|---:|---|"]
out += [f"| {a} | {b} | {c} | {'yes' if e else 'no'} |" for a, b, c, e in rows]
out += ["", "## Checks that fail most", "", "| Check | Candidates failing |", "|---|---:|"]
out += [f"| {k} | {v} of {n} |" for k, v in fails.most_common()]
(d / "RESULT.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
