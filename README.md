# CyberSci Preparation

Preparation repository for the 2026 CyberSci Regional Qualifiers and the dress-rehearsal CTFs leading up to them.

## Objective

Build independent competition skill. CyberSci's organizers have said AI tools are not allowed, so competition-day capability is the laptop, your own notes and your own scripts, working offline. AI is a study-time tutor only. The second machine is training-time capacity (hashcat, lab VMs) and is never required for a valid run.

## Operating principles

- Separate observed facts, source claims, assumptions, plans, and results.
- Keep the laptop path functional without VPN, Machine B, hosted APIs, or venue internet.
- Use scripted pipelines for reliable transformations; reserve model judgement for places where a human can review it.
- Log model/tool calls and require human approval before actions against scoring infrastructure.
- Never let an agent operate outside an explicit challenge-scope allowlist.
- Treat scores as measurements, not proof that a tool or model is generally useful.

## Team entry points

- [Competition day](competition-day/README.md): preparation checklist, team roles, challenge board and private-work templates.
- [Practice resources](practice-resources/README.md): curriculum coverage map and a team rehearsal procedure.

Team: **Algonquin Cybersci Team #2** (working name: AlgonquinTeam#2), hosted by [Cybersci2026-AlgonquinTeam2](https://github.com/Cybersci2026-AlgonquinTeam2).

- [Private competition workspace](https://github.com/Cybersci2026-AlgonquinTeam2/competition-day-2026) (team access required).
- [Contribution guide](CONTRIBUTING.md): local setup, practice tasks, changes and review.

This is a student team workspace, not an official CyberSci or Algonquin College account.

## Existing resource layout

```text
cybersci-prep/
├── README.md
├── PLAN.md                         # Current preparation strategy
├── STATUS.md                       # Decisions, blockers, and next actions
├── events.yaml                     # Event register and rehearsal intent
├── evidence/
│   └── claims.md                   # Source-backed facts and unresolved claims
├── tracker/
│   ├── tracker.csv                 # Source of truth: daily plan Oct 14 → Nov 21
│   ├── roadmap.csv                 # Weekly plan Nov 22 → Jun 2027 toward advanced
│   ├── reading.csv                 # Commute reading/listening catalogue
│   ├── toolkit.csv                 # Tools, AI tools, MCP servers, agents, repos
│   ├── CyberSci-Tracker.xlsx       # Styled workbook view (export_xlsx.py)
│   └── DAILY/WEEKLY/MONTHLY/ROADMAP.md   # Generated views (tracker.py render)
├── curriculum/
│   ├── checklist.md                # Skills and practice progression
│   ├── practice-suite.md           # Skills × methods × exercises × done-when
│   ├── sources.md                  # Sites, archives, tools, books, offline pack
│   ├── cybersci-writeups.md        # Past CyberSci writeups and challenge-shape intel
│   ├── dojo-platform-backlog.md    # Post-qualifier plan: one self-hosted platform
│   └── bandit/                     # README (practice mode), commands.md, walkthrough-1..4, img/ SVGs
├── operations/
│   ├── competition-day-runbook.md  # Offline-first runbook
│   └── machine-b.md                # Training-capacity-box design
├── runs/
│   └── README.md                   # Reproducible CTF run records
├── notes/
│   └── README.md                   # Writeups, concepts, and reusable knowledge
├── tools/
│   └── README.md                   # Planned local tools and MCP boundaries
├── dist/offline/                   # Built PDFs/EPUB for iPhone (scripts/build_offline.py)
└── scripts/
    └── README.md                   # Small validation/recording helpers
```

## First milestone

Before building agents, complete the FortID baseline with no AI and record:

1. start and finish times;
2. challenges attempted and category;
3. points, time spent, and first useful observation;
4. what blocked progress;
5. what evidence would have made the next step obvious.

Then use DEADFACE as the first AI-assisted comparison, keeping the same run-record format.

## Status vocabulary

Use explicit states: `proposed` → `scaffolded` → `parsed` → `locally-validated` → `booted` → `traffic-tested` → `deployed` → `production-ready`.

Documentation, file counts, and schema validation do not prove that a tool works at runtime.


## Sources and attribution

- Past-challenge study notes summarise the organizers' public releases at <https://github.com/CyberSCI/PastChallenges> (AGPL-3.0, "released for education"), the Defence CTF 101 workshop at <https://github.com/CyberSCI/Workshops>, and the organizers' CTFd fork at <https://github.com/CyberSCI/CTFd>. Those repositories are **not** included here (`external/` is git-ignored); clone them yourself and read them as untrusted data.
- Writeups are concept-level summaries in my own words and omit flags.
- Third-party platforms (TryHackMe, OverTheWire, VulnHub, picoCTF, Parrot CTFs, Cybrary) are linked, not copied. Verify names, access levels and prices on their sites.
- Bandit solution walkthroughs and the Bandit flashcard source are intentionally **not published** (OverTheWire asks players not to share solutions). Build scripts that reference them will skip or fail for those files.
- The generated pack (`dist/`) is not committed; rebuild it with the scripts in `scripts/`.
