# Tracker

| File | What it is | Edit? |
|---|---|---|
| `tracker.csv` | Daily plan Oct 14 → Nov 21 (4 h/day study + 1 h weekday commute reading) plus 26 undated backlog items | **Yes**: source of truth |
| `roadmap.csv` | Weekly plan Nov 23 2026 → Dec 26 2027 (57 weeks, same 4 h/day cadence) built around competition milestones; the earlier plan to Jun 2027 is `roadmap.v1.csv` | Yes (or regenerate with `python scripts/roadmap_2027.py`) |
| `milestones.csv` | 23 competitions Nov 2026 → Dec 2027 with dates, confidence (confirmed / expected), who can play, prep start and goal | Yes |
| `reading.csv` | 51 books, guides, papers, podcasts and videos with commute suitability | Yes |
| `toolkit.csv` | 91 tools, AI tools, MCP servers, agents, repos, benchmarks with install-by dates and safety notes | Yes |
| `CyberSci-Tracker.xlsx` | Styled workbook view of all four, with weekly/category roll-ups (formulas) | Rebuild with `python scripts/export_xlsx.py` |
| `DAILY.md` `WEEKLY.md` `MONTHLY.md` `ROADMAP.md` `MILESTONES.md` | Generated markdown views | No: `python scripts/tracker.py render` |
| `DAILY.v1.md` | Earlier hand-written plan, superseded | No |

Daily commands:

```bash
python scripts/tracker.py today
python scripts/tracker.py done W01 2.5     # mark done, 2.5 h actually spent
python scripts/tracker.py skip L09
python scripts/tracker.py move W05 2026-11-10
python scripts/tracker.py report
python scripts/tracker.py check            # budget / cutoff sanity
python scripts/tracker.py render && python scripts/export_xlsx.py
```

Columns in `tracker.csv`: `block` is Learn / Practice / Drill / Build / Review / Admin / Event / Commute.
`tier` is A core, B breadth, C backlog, E event, R reading. `level` is L1 touch, L2 working, L3 advanced.
`done_when` is the evidence that counts as finished; don't mark `done` without it.
