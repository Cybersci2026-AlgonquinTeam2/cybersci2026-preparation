# CyberSci Dojo: one self-hosted platform (BACKLOG, build after Nov 21)

Status: **backlog**, owner: you. Not part of the pre-qualifier plan. Revisit on Sun Nov 22 (debrief day).

## Goal

One offline-capable, self-hosted stack that holds the plan, notes, practice labs and mock competitions in one place. Hosted sites (PortSwigger, TryHackMe, HTB, picoGym, CryptoHack, OverTheWire) cannot be hosted inside it: they are linked and tracked.

```text
                       ┌────────────────────────────────────────────┐
                       │          CyberSci Dojo (your laptop)        │
   ┌─────────────┐     │  ┌─────────────┐   ┌────────────────────┐  │
   │ DASHBOARD   │◀────┼──│ tracker.csv │   │ NOTES + CHEATSHEETS│  │
   │ today/plan  │     │  │ roadmap.csv │   │ markdown, rg/fzf   │  │
   └─────────────┘     │  │ reading.csv │   └────────────────────┘  │
   ┌─────────────┐     │  │ toolkit.csv │                           │
   │ MOCK EVENTS │◀────┼──┴─────────────┘   ┌────────────────────┐  │
   │ scoreboard  │     │  ┌─────────────┐   │ YOUR CHALLENGES    │  │
   └─────────────┘     │  │   CTFd      │◀──│ warmups/forensics/ │  │
                       │  └─────────────┘   │ vault rev/pwn/cry  │  │
                       │  ┌──────────────────────────────────────┐  │
                       │  │ LAB (Docker): Bandit-hard, vulnerable│  │
                       │  │ web app, small AD target             │  │
                       │  └──────────────────────────────────────┘  │
                       │  ┌──────────────────────────────────────┐  │
                       │  │ KALI VM + OFFLINE BUNDLE (USB)       │  │
                       │  └──────────────────────────────────────┘  │
                       └────────────────────────────────────────────┘
```

## Components and tracker IDs

| ID | Component | Effort | Done when |
|---|---|---|---|
| D01 | Dashboard (static HTML from the CSVs) | 2 h | one page shows today's plan + progress offline |
| D02 | CTFd + 5-10 own challenges | 2 h | a teammate can log in, solve, see scoreboard |
| D03 | Bandit-hard Docker lab (10+ levels, generator) | 8 h | `docker run` → ssh into level0; all levels solvable |
| D04 | Realistic target (vulnerable web app + small AD) | 4 h | web → pivot → AD chain solvable |
| D05 | Mock-event runner (timer, roles, run record) | 2 h | one command starts a mock and writes the record |
| D06 | Offline bundle script | 2 h | rebuilt in <15 min; hashes match runbook |
| D07 | Team hosting on Machine B over Tailscale | 2 h | teammate connects; factory unaffected |

Total about 22 h. Tracked as undated backlog items in `tracker/tracker.csv` (`category=dojo`, tier C).

## Design decisions already made

- **Assemble, don't write a custom app:** CTFd + Docker + generated dashboard + markdown notes. A bespoke app would take weeks and compete with study time.
- **Offline first:** everything runs on the laptop; Machine B is optional capacity for team access.
- **No AI in the competition-facing bundle** (organizers: AI tools not allowed, 2026-10-15). AI is fine as a study tutor.
- **Keep it in this git repo** so the stack is reproducible on another machine.
- **Security:** bind services to localhost/Tailscale only; lab containers isolated; never expose CTFd publicly.

## Reference projects (inspected 2026-10-15, not adopted)

| Project | Use | Caveat |
|---|---|---|
| CTFd (Apache-2.0) | the platform for mock events | check docs for container-per-player support |
| Bandito | read for how a Bandit clone is structured | no license shown; level authoring is "TODO" |
| Isolet (MIT) | only if hosting for many players | Kubernetes, Kafka, Postgres: heavy |
| Docker-War | skip | early-stage, needs host Docker socket |

## Suggested slots after the qualifier

| When | Items |
|---|---|
| Week of Nov 23 | D01 dashboard, D02 CTFd |
| Dec 21 break week | D03 lab (a weekend), D05 |
| Early January | D04, D06, D07 |

## Open questions for later

1. Will teammates use it? (decides D07)
2. Do you want the lab to mirror CyberSci categories exactly, or be broader?
3. Should the dashboard also export a weekly report for your instructor/club?

## Note (2026-11-10): the organizers' own repos

- `CyberSCI/PastChallenges` (AGPL-3.0): every past challenge, with CTFd names, walkthroughs and solve files. Cloned at `external/PastChallenges`.
- `CyberSCI/Workshops`: Defence CTF 101 (Docker Compose lab). Cloned at `external/Workshops`.
- `CyberSCI/CTFd`: the organizers' fork of CTFd (the platform used to run events; README fields say "CTFd name"). Cloned at `external/CTFd`; use it as the reference for the Dojo's CTFd (D02).
