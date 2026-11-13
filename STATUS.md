# Status

## Current state

2026-10-15: study starts today. Organizers replied that **AI tools are not allowed** at the CyberSci qualifier (claim C-007; request the exact written wording). The plan is now fully manual on competition day. AI remains useful as a study-time tutor and for other CTFs whose rules permit it.

## Tracker

Daily plan: [`tracker/tracker.csv`](tracker/tracker.csv) (views: DAILY/WEEKLY/MONTHLY/ROADMAP.md, `CyberSci-Tracker.xlsx`). Oct 14 items were folded into Oct 15 because no study was done on Oct 14.

## Backlog (post-qualifier)

- **CyberSci Dojo**: one self-hosted platform (dashboard, CTFd mock events, Bandit-hard lab, offline bundle, team hosting). Design and items D01-D07 in [`curriculum/dojo-platform-backlog.md`](curriculum/dojo-platform-backlog.md). Build after Nov 21.

## Offline pack

2026-10-15: phone-sized PDFs + EPUB in `dist/offline/` (copy in OneDrive `CyberSci-Offline/`). Rebuild with `python scripts/build_offline.py --copy <folder>` after editing any module or the plan.

Modules 11-16 added 2026-10-15 (scripting, OSINT/misc, Windows forensics, cloud, labs, review system); rebuild with build_offline.py, build_flashcards.py, build_epubs.py, package_pack.py.

## Next actions

- [x] Verify qualifier date, event shape, eligibility, team size, registration path, and CTFtime classification.
- [x] Ask organizers about AI tools: **not allowed** (2026-10-15).
- [ ] Ask organizers (follow-up): is offline reference material (own notes, cheat sheets) allowed? own scripts? internet at the venue? bring own laptop? exact definition of "AI tools" (autocomplete, search engines)?
- [ ] Register through the school instructor or computer club.
- [ ] Create a FortID run record (or mark not played).
- [ ] Snapshot Kali VM; build notes search (ripgrep/fzf); write helper-script library.

## Decisions

- No AI tools in competition or in rehearsal events that mimic it (DEADFACE, CSCTF, InIt).
- AI may be used for study (explaining concepts, reviewing your writeups) but not as a crutch during timed drills.
- The local-model/MCP/agent work is deprioritized to after Nov 21 (see roadmap).
- Machine B is for hashcat, lab VMs and a vulnerable-target lab, not a competition dependency.
- Human approval before traffic touches scoring infrastructure.

## Open risks

- Event dates and rules may change; verify the written rule.
- Whether own notes/scripts/cheat sheets are allowed is unconfirmed.
- Venue internet and laptop policy are unconfirmed.
- Cross-event score comparison is confounded by difficulty and team composition.
