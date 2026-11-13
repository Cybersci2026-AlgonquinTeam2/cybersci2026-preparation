#!/usr/bin/env python3
"""Log and review learn-by-doing activity attempts (tracker/activities.csv).

  python scripts/activity.py status                     progress by platform
  python scripts/activity.py next [N]                   next N P1 activities not finished
  python scripts/activity.py list [PLATFORM-substring]  list activities
  python scripts/activity.py log ID ATTEMPT GRADE MIN [YYYY-MM-DD]
        ATTEMPT 1 or 2; GRADE A/B/C/D (A unaided .. D needed the solution); MIN minutes spent
  python scripts/activity.py note ID "text"
"""
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "tracker" / "activities.csv"
GRADES = "ABCD"


def load():
    with CSV.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def save(fields, rows):
    with CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def state(r):
    if r["a2_grade"] in ("A", "B"):
        return "done"
    if r["a2_grade"]:
        return "repeat"
    if r["a1_grade"]:
        return "needs attempt 2"
    return "todo"


def main(a):
    if not a:
        print(__doc__)
        return
    fields, rows = load()
    cmd = a[0]
    if cmd == "log":
        i, att, grade, mins = a[1], a[2], a[3].upper(), a[4]
        when = a[5] if len(a) > 5 else date.today().isoformat()
        if att not in ("1", "2") or grade not in GRADES:
            sys.exit("ATTEMPT must be 1 or 2; GRADE must be A, B, C or D")
        r = next((x for x in rows if x["id"] == i), None)
        if not r:
            sys.exit(f"unknown id {i}")
        r[f"a{att}_date"], r[f"a{att}_grade"], r[f"a{att}_min"] = when, grade, mins
        r["status"] = state(r)
        save(fields, rows)
        print(f"{i} attempt {att}: grade {grade}, {mins} min -> {r['status']}")
    elif cmd == "note":
        r = next((x for x in rows if x["id"] == a[1]), None)
        if not r:
            sys.exit("unknown id")
        r["notes"] = a[2]
        save(fields, rows)
    elif cmd == "status":
        by = defaultdict(list)
        for r in rows:
            by[r["platform"]].append(r)
        tot_done = tot = 0
        for plat, rs in by.items():
            done = sum(state(r) == "done" for r in rs)
            a1 = sum(bool(r["a1_grade"]) for r in rs)
            mins = sum(int(r["a1_min"] or 0) + int(r["a2_min"] or 0) for r in rs)
            print(f"{plat:26s} done {done:2d}/{len(rs):2d}   attempt-1 {a1:2d}   minutes {mins}")
            tot_done += done
            tot += len(rs)
        p1 = [r for r in rows if r["priority"] == "P1"]
        print(f"\nP1 done {sum(state(r) == 'done' for r in p1)}/{len(p1)} | all done {tot_done}/{tot}")
    elif cmd == "next":
        n = int(a[1]) if len(a) > 1 else 5
        todo = [r for r in rows if r["priority"] == "P1" and state(r) != "done"]
        for r in todo[:n]:
            print(f"{r['id']:8s} {state(r):16s} {r['platform']:24s} {r['title']}  (read: {r['reading']}; ~{r['est_min']} min)")
    elif cmd == "list":
        key = a[1].lower() if len(a) > 1 else ""
        for r in rows:
            if key in r["platform"].lower() or key in r["id"].lower():
                print(f"{r['id']:8s} {r['priority']} {state(r):16s} {r['title']}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
