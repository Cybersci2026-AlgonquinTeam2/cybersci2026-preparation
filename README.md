# CyberSci Preparation

Preparation repository for the 2026 CyberSci Regional Qualifiers and the dress-rehearsal CTFs leading up to them.

## Objective

Build independent competition skill first, then measure whether a carefully bounded local AI stack improves speed and accuracy. The competition-day baseline is the laptop working offline. The second machine is training-time capacity only and must never be required for a valid run.

## Operating principles

- Separate observed facts, source claims, assumptions, plans, and results.
- Keep the laptop path functional without VPN, Machine B, hosted APIs, or venue internet.
- Use scripted pipelines for reliable transformations; reserve model judgement for places where a human can review it.
- Log model/tool calls and require human approval before actions against scoring infrastructure.
- Never let an agent operate outside an explicit challenge-scope allowlist.
- Treat scores as measurements, not proof that a tool or model is generally useful.

## Repository map

```text
cybersci-prep/
├── README.md
├── PLAN.md                         # Current preparation strategy
├── STATUS.md                       # Decisions, blockers, and next actions
├── events.yaml                     # Event register and rehearsal intent
├── evidence/
│   └── claims.md                   # Source-backed facts and unresolved claims
├── curriculum/
│   └── checklist.md                # Skills and practice progression
├── operations/
│   ├── competition-day-runbook.md  # Offline-first runbook
│   └── machine-b.md                # Training-capacity-box design
├── runs/
│   └── README.md                   # Reproducible CTF run records
├── notes/
│   └── README.md                   # Writeups, concepts, and reusable knowledge
├── tools/
│   └── README.md                   # Planned local tools and MCP boundaries
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

