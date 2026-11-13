# 11-day sprint: Nov 10 → Nov 21 (competition day)

Updated 2026-11-10 after reading the organizers' official skills list, the **Defence CTF 101 workshop**, and the **PastChallenges** repo. The tracker shows almost nothing logged since Oct 15, so this sprint keeps only the highest-yield material and uses the **learn-by-doing loop** (Read → Attempt 1 → Review → Reinforce → Attempt 2 → Review 2). Activity IDs are in `tracker/activities.csv`; log with `python scripts/activity.py log ID ATTEMPT GRADE MINUTES`.

## What the organizers say to prepare (priorities)

1. **Networking + Nmap (including outside the local subnet)**: THM-02, LAB-17-style output reading.
2. **Web exploits** (SQLi, file include, command injection, traversal) and **basic SQL** (`SHOW`, `DESCRIBE`, `SELECT`, wildcards): LAB-08, LAB-09, SKL-01, THM-04.
3. **Memory forensics**: THM-07, LAB-11.
4. **Reverse engineering + beginner binary exploitation**: LAB-14, one picoGym RE set.
5. **Crypto algorithms and weaknesses**: LAB-02/03/04, PC-01/02/05.
6. **Application vulnerability analysis + a Defence challenge** (patch a service while it's attacked): **DEF-01** (the workshop).
7. **Hacker tools and a reverse shell**: THM-16 (or Module 6 §6.2) in a lab VM.
8. **Basic programming**: LAB-12.
9. **Security news**: 10 minutes a day (sources in chapter 24 §7).

## Day by day (4 h/day unless noted)

| Day | Focus | Do (IDs) |
|---|---|---|
| **Tue Nov 10** (T-11) | Baseline | **Cold mock exam (60 min)** → LAB-01, LAB-02 → Bandit OTW-B1, OTW-B2 (levels 0-9) → admin (below) |
| **Wed Nov 11** (T-10) | Linux + SQL | OTW-B3, OTW-B4, OTW-B5 (Bandit 10-20) → SKL-01 (basic SQL) → 15 flashcards |
| **Thu Nov 12** (T-9) | CyberSci-style warmups + forensics | PC-01, PC-02, PC-04 (past challenges) → LAB-05, LAB-06 → THM-07 (memory) |
| **Fri Nov 13** (T-8) | **Defence** + Nmap | **DEF-01** (Defence CTF 101, Attempt 1, 90 min) → THM-02 → easy-tier CTF ≤ 1 h; team call |
| **Sat Nov 14** (T-7) | **Dress rehearsal** | **InIt CTF, 8 h** (10:30-18:30 EST per CTFtime): roles, notes, laptop, offline test |
| **Sun Nov 15** (T-6) | Debrief + web | Debrief (2 h): top-3 issues, one fix each → LAB-08, LAB-09 → PC-17 / PC-21 |
| **Mon Nov 16** (T-5) | Second baseline | **Mock exam #2** → **DEF-01 Attempt 2** (reset, source review + logging first) → LAB-03, LAB-04 |
| **Tue Nov 17** (T-4) | Web chain + crypto | PC-13 (Secret Rally) or PC-11 → PICO-02 (crypto set) → THM-04 (SQLi) |
| **Wed Nov 18** (T-3) | Taper | 3 h: weakest category only; cheat sheets; freeze the bundle |
| **Thu Nov 19** (T-2) | Logistics | venue, ID, charger, USB, team sync, rules (1.5 h) |
| **Fri Nov 20** (T-1) | Rest | pack, check the laptop boots, sleep 8 h |
| **Sat Nov 21** | **CyberSci regionals** | triage first, 30-minute rule, roles, interviews after |

## Past challenges: writeups and primers

For every PC-* item the writeups are in chapters 31 (2025/26) and 32 (2024/25); primers and 8 runnable drills are in chapter 33 (PCD-01..08). Read the primer first, attempt the challenge from `external/PastChallenges`, then read the writeup, then do a related one as Attempt 2.

## Admin this week (blocking if skipped)

- [ ] **Register through your school** (instructor or student club).
- [ ] **Confirm the rules in writing**: offline notes/cheat sheets? own scripts? internet at the venue? own laptop? what counts as "AI"?
- [ ] **Team of up to 4**, a submission owner, a communication channel.
- [ ] **Docker + Compose installed and tested** (the defence challenge assumes you know them).
- [ ] Venue and start time (CTFtime says 15:00-22:00 UTC; the site says hacking in the morning).

## Daily minimum (even on a bad day)

15 flashcards · 1 hands-on item · 5 lines of notes · 10 minutes of security news.

## Log

| Day | Done | Minutes | Mock score | Weakest |
|---|---|---|---|---|
| Nov 10 | | | | |
| Nov 11 | | | | |
| Nov 12 | | | | |
| Nov 13 | | | | |
| Nov 14 | | | | |
