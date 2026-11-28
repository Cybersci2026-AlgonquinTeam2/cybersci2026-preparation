#!/usr/bin/env python3
"""Planted-defect control for a Critic configuration (standards section 9).

    python tools/critic_control.py PASSING_TOPIC_DIR WORK_DIR [--model M] [--url U] [--pack P] [--cpu] [--threads N] [--max-checks K] [--no-model] [--min-recall 0.5]
1. Plants 6 defects in a copy and runs the Critic on it. Recall = defects with a finding that quotes text on or near the planted line.
2. Runs the Critic on the UNPLANTED topic as well: the reference topic passed the gate and its labs ran, so findings there are mostly false alarms;
   the count is reported as the false-alarm burden.
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
ap.add_argument("--cpu", action="store_true")
ap.add_argument("--threads")
ap.add_argument("--max-checks")
ap.add_argument("--no-model", action="store_true")
ap.add_argument("--min-recall", type=float, default=0.5)
ap.add_argument("--config")
a = ap.parse_args()
here = Path(__file__).parent
work = Path(a.work)
work.mkdir(parents=True, exist_ok=True)
copy = work / "planted-copy"
subprocess.run([sys.executable, str(here / "plant_defects.py"), a.topic, str(copy)], check=True)


def run_critic(target, out):
    cmd = [sys.executable, str(here / "critic.py"), str(target), "--out", str(out)]
    for flag, val in (("--model", a.model), ("--url", a.url), ("--pack", a.pack), ("--threads", a.threads), ("--max-checks", a.max_checks), ("--config", a.config)):
        if val:
            cmd += [flag, val]
    if a.cpu:
        cmd.append("--cpu")
    if a.no_model:
        cmd.append("--no-model")
    subprocess.run(cmd, check=True)


run_critic(copy, work / "findings.json")
run_critic(a.topic, work / "findings-unplanted.json")
planted = json.loads((copy / "planted.json").read_text(encoding="utf-8"))
findings = json.loads((work / "findings.json").read_text(encoding="utf-8"))["findings"]
fa = json.loads((work / "findings-unplanted.json").read_text(encoding="utf-8"))["findings"]
hits = []
for p in planted:
    lines = (copy / p["file"]).read_text(encoding="utf-8").splitlines()
    lo, hi = max(p["line_after_edit"] - 6, 0), p["line_after_edit"] + 7
    window = L.norm("\n".join(lines[lo:hi]))
    match = [f for f in findings if f["file"] == p["file"] and L.norm(f["quote"]) in window]
    hits.append((p["kind"], bool(match), match[0].get("method") if match else None))
recall = sum(1 for _, ok, _ in hits if ok) / max(len(hits), 1)
res = {"recall": round(recall, 2), "found": {k: m for k, ok, m in hits if ok}, "missed": [k for k, ok, _ in hits if not ok],
       "findings_on_planted_copy": len(findings), "false_alarms_on_unplanted_topic": len(fa),
       "false_alarms_by_method": {m: sum(1 for f in fa if f.get("method") == m) for m in ("mechanical", "model")},
       "min_recall": a.min_recall, "pass": recall >= a.min_recall}
(work / "control.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
sys.exit(0 if res["pass"] else 1)
