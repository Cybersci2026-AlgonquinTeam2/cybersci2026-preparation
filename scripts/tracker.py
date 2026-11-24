#!/usr/bin/env python3
"""Daily/weekly/monthly tracker driven by tracker/tracker.csv (stdlib only).

  python scripts/tracker.py today            rows for today + progress
  python scripts/tracker.py day 2026-11-02   rows for a date
  python scripts/tracker.py week [1-6]       rows + progress for a week
  python scripts/tracker.py month [10|11]    totals by category/tier
  python scripts/tracker.py report           overall progress
  python scripts/tracker.py done ID [HOURS]  mark done (spent defaults to planned)
  python scripts/tracker.py skip ID          mark skipped
  python scripts/tracker.py move ID DATE     reschedule (use '' for backlog)
  python scripts/tracker.py check            budget / sanity checks
  python scripts/tracker.py render           regenerate DAILY/WEEKLY/MONTHLY/ROADMAP.md
  python scripts/export_xlsx.py              regenerate the styled workbook
"""
import csv
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TDIR = ROOT / "tracker"
CSV = TDIR / "tracker.csv"
WEEK1 = date(2026, 10, 12)          # Monday of week 1
COMP = date(2026, 11, 21)
SOURCE_CUTOFF = date(2026, 11, 14)  # new source work should be done a week before
WEEKDAY_BUDGET, WEEKEND_BUDGET = 4.0, 8.0   # excludes commute reading
TIERS = {"A": "core", "B": "breadth", "C": "backlog", "E": "event", "R": "reading"}
STUDY_CATS = ("web", "linux", "crypto", "pwn", "rev", "forensics", "ad")


def load():
    with CSV.open(newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    for r in rows:
        r["hours"] = float(r["hours"])
        r["spent"] = float(r["spent"]) if r["spent"] else 0.0
    return fields, rows


def save(fields, rows):
    with CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            r = dict(r)
            r["hours"] = f"{r['hours']:g}"
            r["spent"] = f"{r['spent']:g}" if r["spent"] else ""
            w.writerow(r)


def d(r):
    return date.fromisoformat(r["date"]) if r["date"] else None


def week_of(day):
    return (day - WEEK1).days // 7 + 1


def mark(r):
    return {"done": "x", "skipped": "-"}.get(r["status"], " ")


def line(r):
    return (f"- [{mark(r)}] **{r['id']}** · {r['hours']:g} h · {r['block']} · {r['level']} · "
            f"{r['category']}/{TIERS[r['tier']]} · {r['source']}: {r['task']}"
            + (f" _(done when: {r['done_when']})_" if r.get("done_when") else ""))


def spent(r):
    return r["spent"] or r["hours"]


def progress(rows, label):
    plan = sum(r["hours"] for r in rows if r["status"] != "skipped")
    done = sum(spent(r) for r in rows if r["status"] == "done")
    pct = 100 * done / plan if plan else 0
    return (f"{label}: {done:g}/{plan:g} h ({pct:.0f}%) · "
            f"{sum(r['status'] == 'done' for r in rows)}/{len(rows)} items")


def by(rows, key):
    out = defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return out


def dated(rows):
    return [r for r in rows if r["date"]]


def show_day(rows, day):
    todays = [r for r in rows if r["date"] == day.isoformat()]
    print(f"\n{day:%a %b %d} · T-{(COMP - day).days} · week {week_of(day)}")
    for r in todays:
        print(line(r))
    if not todays:
        print("(nothing scheduled)")
    print(progress(todays, "day"))


def category_table(rows):
    cats = by(rows, lambda r: r["category"])
    return [f"| {c} | {sum(r['hours'] for r in cats[c]):g} | "
            f"{sum(spent(r) for r in cats[c] if r['status'] == 'done'):g} |" for c in sorted(cats)]


def cmd_check(rows):
    problems = 0
    ids = [r["id"] for r in rows]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        print("duplicate id:", i); problems += 1
    for day, rs in sorted(by(dated(rows), lambda r: r["date"]).items()):
        dd = date.fromisoformat(day)
        study = [r for r in rs if r["block"] != "Commute"]
        budget = WEEKEND_BUDGET if dd.weekday() >= 5 or any(r["tier"] == "E" for r in rs) else WEEKDAY_BUDGET
        total = sum(r["hours"] for r in study)
        if total > budget:
            print(f"{day}: {total:g} h > budget {budget:g} h"); problems += 1
        if SOURCE_CUTOFF < dd < COMP and any(
                r["tier"] in "AB" and r["category"] in STUDY_CATS for r in rs):
            print(f"{day}: new source work after cutoff {SOURCE_CUTOFF}"); problems += 1
    tot = {t: sum(r["hours"] for r in rows if r["tier"] == t) for t in TIERS}
    print(" · ".join(f"{TIERS[t]} {h:g} h" for t, h in tot.items()))
    print("OK" if not problems else f"{problems} problem(s)")


def roadmap_rows():
    p = TDIR / "roadmap.csv"
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cmd_render(rows):
    out = ["# Daily tracker", "",
           "Generated from `tracker.csv` by `scripts/tracker.py render`. Edit the CSV (or use `done`/`move`), not this file.", "",
           f"Competition: **{COMP:%a %b %d, %Y}**. Source-completion cutoff: **{SOURCE_CUTOFF:%b %d}**.",
           "Budget: 4 h study per day + ~1 h commute reading on weekdays; events/weekends as scheduled.", ""]
    for day, rs in sorted(by(dated(rows), lambda r: r["date"]).items()):
        dd = date.fromisoformat(day)
        study = sum(r["hours"] for r in rs if r["block"] != "Commute")
        out += [f"## {dd:%a %b %d} · T-{(COMP - dd).days} · {rs[0]['phase']} · {study:g} h study", ""]
        out += [line(r) for r in rs]
        out += ["", "- [ ] **Close**: log below; update `curriculum/checklist.md`; commit", "",
                "`Log: min __ · solved __ · stuck on __ · AI used? __`", ""]
    (TDIR / "DAILY.md").write_text("\n".join(out), encoding="utf-8")

    out = ["# Weekly tracker", "", "Generated from `tracker.csv`.", ""]
    weeks = by(dated(rows), lambda r: week_of(d(r)))
    for w in sorted(weeks):
        rs = weeks[w]
        start = WEEK1 + timedelta(days=7 * (w - 1))
        out += [f"## Week {w}: {start:%b %d} - {start + timedelta(days=6):%b %d}", "",
                progress(rs, "plan"), "", "| Category | Planned h | Done h |", "|---|---:|---:|"]
        out += category_table(rs)
        out += ["", "**Core goals:** " + "; ".join(f"{r['id']} {r['source']}" for r in rs if r["tier"] == "A"), "",
                "**Sunday review:**", "",
                "- [ ] Re-mark skill statuses in `curriculum/checklist.md` with evidence",
                "- [ ] Points/hour and AI-vs-no-AI notes updated",
                "- [ ] Reschedule missed items with `tracker.py move`; drop what no longer fits",
                "- [ ] Next week's top 3 weaknesses named", ""]
    (TDIR / "WEEKLY.md").write_text("\n".join(out), encoding="utf-8")

    out = ["# Monthly tracker", "", "Generated from `tracker.csv`.", ""]
    months = by(dated(rows), lambda r: d(r).strftime("%Y-%m"))
    for m in sorted(months):
        rs = months[m]
        out += [f"## {m}", "", progress(rs, "plan"), "",
                "| Tier | Items | Planned h | Done h |", "|---|---:|---:|---:|"]
        for t in "ABERC":
            ts = [r for r in rs if r["tier"] == t]
            if ts:
                out.append(f"| {TIERS[t]} | {len(ts)} | {sum(r['hours'] for r in ts):g} | "
                           f"{sum(spent(r) for r in ts if r['status'] == 'done'):g} |")
        out += ["", "| Category | Planned h | Done h |", "|---|---:|---:|"] + category_table(rs) + [""]
    undated = [r for r in rows if not r["date"]]
    out += ["## Backlog (unscheduled; pulled in by the roadmap)", "",
            f"{len(undated)} items · {sum(r['hours'] for r in undated):g} h", ""]
    out += [line(r) for r in undated]
    (TDIR / "MONTHLY.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    rm = roadmap_rows()
    if rm:
        out = ["# Roadmap: Nov 2026 to Dec 2027, built around competition milestones", "",
               "Generated from `roadmap.csv`. Same 4 h/day + commute reading cadence; weekly granularity.", ""]
        for ph, items in by(rm, lambda r: r["phase"]).items():
            out += [f"## {ph}", ""]
            for r in items:
                out += [f"### {r['week_start']} → {r['week_end']} · {r['theme']} · target {r['level_target']} · {r['hours']} h", "",
                        f"- **Practice:** {r['practice']}", f"- **Reading:** {r['reading']}"]
                if r["backlog_ids"]:
                    out.append(f"- **Backlog pulled in:** {r['backlog_ids']}")
                if r["events"]:
                    out.append(f"- **Events:** {r['events']}")
                if r["gate"]:
                    out.append(f"- **Gate:** {r['gate']}")
                out.append("")
        (TDIR / "ROADMAP.md").write_text("\n".join(out), encoding="utf-8")
    mp = TDIR / "milestones.csv"
    if mp.exists():
        with mp.open(newline="", encoding="utf-8") as f:
            ms = sorted(csv.DictReader(f), key=lambda r: r["start"])
        out = ["# Competition milestones: Nov 2026 to Dec 2027", "",
               "Generated from `milestones.csv`. **confirmed** = the organiser's own page said so; **expected** = inferred from last year's pattern, so confirm before you pay or travel.",
               "Priority: yes = a planned milestone, optional = play if the week allows, alt = an alternative to the event that weekend, skip = not for you.", "",
               "| When | Event | Format | Confidence | Priority | Goal |", "|---|---|---|---|---|---|"]
        for r in ms:
            when = r["start"] if r["start"] == r["end"] else f"{r['start']} to {r['end']}"
            out.append(f"| {when} | {r['event']} | {r['format']} | {r['confidence']} | {r['priority']} | {r['goal']} |")
        out.append("")
        for r in ms:
            out += [f"### {r['id']} {r['event']}", "", f"- **Dates:** {r['start']} to {r['end']} ({r['confidence']})",
                    f"- **Who can play:** {r['who_can_play']}", f"- **Start preparing:** {r['prep_from'] or 'n/a'}",
                    f"- **Goal:** {r['goal']}"] + ([f"- **Notes:** {r['notes']}"] if r["notes"] else []) + [""]
        (TDIR / "MILESTONES.md").write_text("\n".join(out), encoding="utf-8")
    print("rendered DAILY.md, WEEKLY.md, MONTHLY.md, ROADMAP.md, MILESTONES.md")


def main(argv):
    if not argv:
        print(__doc__); return
    cmd, args = argv[0], argv[1:]
    fields, rows = load()
    if cmd == "today":
        show_day(rows, date.today()); print(progress(rows, "overall"))
    elif cmd == "day":
        show_day(rows, date.fromisoformat(args[0]))
    elif cmd == "week":
        w = int(args[0]) if args else week_of(date.today())
        rs = [r for r in dated(rows) if week_of(d(r)) == w]
        for day in sorted({r["date"] for r in rs}):
            show_day(rows, date.fromisoformat(day))
        print("\n" + progress(rs, f"week {w}"))
    elif cmd == "month":
        m = int(args[0]) if args else date.today().month
        rs = [r for r in dated(rows) if d(r).month == m]
        print(progress(rs, f"month {m}"))
        print("\n".join(["category | planned | done"] + category_table(rs)))
    elif cmd == "report":
        print(progress(rows, "all items (incl. backlog)"))
        print(progress(dated(rows), "scheduled"))
        for t in TIERS:
            print(progress([r for r in rows if r["tier"] == t], TIERS[t]))
        print("\ncategory | planned | done")
        print("\n".join(category_table(rows)))
    elif cmd in ("done", "skip", "move"):
        r = next((x for x in rows if x["id"] == args[0]), None)
        if not r:
            sys.exit(f"unknown id {args[0]}")
        if cmd == "done":
            r["status"] = "done"
            r["spent"] = float(args[1]) if len(args) > 1 else r["hours"]
        elif cmd == "skip":
            r["status"] = "skipped"
        else:
            nd = args[1] if len(args) > 1 else ""
            r["date"] = nd
            if nd:
                dd = date.fromisoformat(nd)
                r["day"], r["week"] = f"{dd:%a}", f"W{week_of(dd)}"
            else:
                r["day"] = r["week"] = ""
        save(fields, rows); print("updated", r["id"], r["status"], r["date"])
    elif cmd == "check":
        cmd_check(rows)
    elif cmd == "render":
        cmd_render(rows)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
