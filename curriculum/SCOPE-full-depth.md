# Full-depth scope: every platform, every level

Agreed 2026-11-13. Supersedes the "thin activity book" approach for everything except Bandit and the CyberSci past challenges (already deep).

## Rules

- **Depth per item:** primer (plain language + diagram), hints ladder (nudge, method, full solution), explained walkthrough (every command, flags, alternatives, use cases), linked reading, attempt-2 variant, flashcards, tracker row.
- **Verification:** OverTheWire is NOT run over SSH by the assistant. Solutions come from the site and research and are marked `researched-unverified` until the learner confirms them in play. Other platforms: verify where a local/offline artefact allows it, else the same label.
- **Copyright:** original explanations, link out, no copied room text or writeups.
- **Publishing:** the repo is public. Solutions live in git-ignored `solutions/` folders. Hints and primers can be public.
- **Layout:** hints ladder and full solutions in one book per platform (solutions section last).
- **TryHackMe cutoff:** learning paths + free rooms.

## Phases

| # | Phase | Status |
|---|---|---|
| 0 | Inventory manifests per platform | OverTheWire done (`curriculum/overthewire/manifest.csv`, 179 rows) |
| 1 | OverTheWire, all games | in progress (Natas, Krypton, Leviathan drafted; Narnia 0-8 verified live; Behemoth, Manpage, Utumno, Maze, Vortex, FormulaOne, Drifter outline only) |
| 2 | picoCTF archive by category | todo |
| 3 | TryHackMe paths + free rooms | todo |
| 4 | VulnHub curated list, Parrot CTFs, Cybrary | todo |
| 5 | Cross-links, platform EPUBs/PDFs, flashcards, trackers | todo |

## Phase 1: OverTheWire inventory (from overthewire.org, 2026-11-13)

Online games: Bandit 34 (0-33, done separately), Natas 35 (0-34, to verify), Krypton 7 (to verify), Leviathan 8, Narnia 9 (0-8, verified), Behemoth 9, Utumno 10, Maze 9 (verify), Manpage 7, Vortex 27. Also listed online with unknown level counts: FormulaOne, Drifter. Offline/released (Semtex, HES2010, Abraxas, Monxla, Kishi): out of scope unless the learner asks.

Batch order (easy to hard, web/crypto first because CyberSci tests them): 1 Natas, 2 Krypton, 3 Leviathan, 4 Narnia, 5 Behemoth, 6 Manpage, 7 Utumno, 8 Maze, 9 Vortex, 10 FormulaOne + Drifter (after counts are confirmed).

Open verification items: Natas final level, Krypton port/count, Maze 8 vs 9, Vortex numbering/port, FormulaOne and Drifter counts.
