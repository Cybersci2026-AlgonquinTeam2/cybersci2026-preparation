#!/usr/bin/env python3
"""Planted-defect control for a Critic configuration (standards section 9).

    python tools/critic_control.py PASSING_TOPIC_DIR WORK_DIR [--model M] [--url U] [--pack P] [--min-recall 0.5]
Plants 6 defects in a copy, runs the Critic, scores recall: a defect counts as found when a finding quotes text on or within 3 lines of the planted line.
Exit 0 only if recall >= --min-recall. A Critic that fails is not used for promotion; re-run when the model or its prompt changes.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gatelib as L  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("topic")
ap.add_argument("work")
ap.add_argument("--model")
ap.add_argument("--url")
ap.add_argument("--pack")
ap.add_argument("--min-recall", type=float, default=0.5)
ap.add_argument("--config")
a = ap.parse_args()
here = Path(__file__).parent
work = Path(a.work)
copy = work / "planted-copy"
subprocess.run([sys.executable, str(here / "plant_defects.py"), a.topic, str(copy)], check=True)
cmd = [sys.executable, str(here / "critic.py"), str(copy), "--out", str(work / "findings.json")]
for flag, val in (("--model", a.model), ("--url", a.url), ("--pack", a.pack), ("--config", a.config)):
    if val:
        cmd += [flag, val]
subprocess.run(cmd, check=True)
planted = json.loads((copy / "planted.json").read_text(encoding="utf-8"))
findings = json.loads((work / "findings.json").read_text(encoding="utf-8"))["findings"]
hits = []
for p in planted:
    lines = (copy / p["file"]).read_text(encoding="utf-8").splitlines()
    lo, hi = max(p["line_after_edit"] - 3, 0), p["line_after_edit"] + 4
    window = L.norm("\n".join(lines[lo:hi]))
    ok = any(f["file"] == p["file"] and L.norm(f["quote"]) in window for f in findings)
    hits.append((p["kind"], ok))
recall = sum(1 for _, ok in hits if ok) / max(len(hits), 1)
res = {"recall": recall, "found": [k for k, ok in hits if ok], "missed": [k for k, ok in hits if not ok], "total_findings": len(findings), "min_recall": a.min_recall, "pass": recall >= a.min_recall}
(work / "control.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
sys.exit(0 if res["pass"] else 1)
