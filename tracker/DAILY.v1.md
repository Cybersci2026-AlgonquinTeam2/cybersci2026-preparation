# Daily tracker: Oct 14 → Nov 21, 2026

Generated 2026-10-14. Competition: **Sat Nov 21** (T-38). Dates and times for events come from [`events.yaml`](../events.yaml); the qualifier's start time is unverified (CTFtime says 15:00 UTC; cybersci.ca says hacking in the morning, interviews in the afternoon).

**Assumed budget:** ~2 h on weekdays, 5-6 h on weekends. Scale blocks down on heavy school days, but never skip **Close**. A skipped day is logged as skipped, not backfilled silently.

**Every day has the same shape:**
- **Learn**: one concept, read or watch, produce a 5-line note in `notes/`.
- **Practice**: hands-on labs or challenges, manual first.
- **Drill**: a timed or repeated exercise that builds speed.
- **Build**: AI-stack or tooling work (≤30 min), one small deliverable.
- **Close**: update `curriculum/checklist.md` status, fill the log line, commit.

Per-day log line: `Log: min __ · solved __ · stuck on __ · AI used? y/n`

Resources named below are catalogued with URLs in [`curriculum/sources.md`](../curriculum/sources.md); exercises and "done when" criteria are in [`curriculum/practice-suite.md`](../curriculum/practice-suite.md).

---

## Phase 1: Foundations and first AI-assisted run (Oct 14-20)

### Wed Oct 14 · D01 · T-38 · Admin and baseline
- [ ] **Admin (30 m):** email the organizers (via cybersci.ca contact or your instructor): is AI/LLM tooling allowed, is venue internet available, do we bring our own laptops? Ask your instructor about school registration and teammates (max 4; 5 with a woman or Indigenous member).
- [ ] **Admin:** if you played FortID (Oct 9-11), fill `runs/2026-10-09-fortid/README.md` honestly, even if you scored little. If you didn't play, write "not played" there.
- [ ] **Learn (20 m):** the CTF method card in `curriculum/practice-suite.md` §0 (observe → hypothesize → smallest test → verify).
- [ ] **Practice (40 m):** OverTheWire Bandit levels 0-10.
- [ ] **Build (20 m):** Kali VM: create a clean snapshot named `base-2026-10-14`.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Oct 15 · D02 · T-37 · Linux CLI + scripting
- [ ] **Learn (20 m):** grep/awk/sed/cut/sort/uniq pipelines; `file`, `strings`, `xxd`, `base64`.
- [ ] **Practice (45 m):** Bandit 10-20.
- [ ] **Drill (25 m):** CyberChef: decode 5 layered encodings (base64 → hex → rot13 → gzip → XOR) from scratch, then recreate one in a Python script.
- [ ] **Build (20 m):** write the interface sketch for the local model router (inputs, outputs, which model answered, fallback reason). No code yet.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Fri Oct 16 · D03 · T-36 · Web I + DEADFACE prep
- [ ] **Learn (25 m):** PortSwigger SQL injection reading (all subsections).
- [ ] **Practice (50 m):** PortSwigger SQLi labs 1-5 (WHERE bypass, login bypass, UNION column count, UNION text, DB version).
- [ ] **Drill (15 m):** `docker run -p 3000:3000 bkimminich/juice-shop`; solve scoreboard + 2 one-star challenges.
- [ ] **Build (20 m):** DEADFACE kit: shared notes file, role assignment, run-record copy from the FortID template, "AI used: yes/no per challenge" column.
- [ ] **Close** · sleep early.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Oct 17 · D04 · T-35 · DEADFACE day 1 (AI-assisted)
- [ ] Event start ~10:00 EDT (14:00 UTC), verify on [CTFtime](https://ctftime.org/event/3279).
- [ ] Record the start time and AI mode before opening the first challenge.
- [ ] Triage first: read all challenge titles, rank by points per estimated effort, assign roles.
- [ ] 30-minute rule: no challenge gets more than 30 min alone before you swap or ask.
- [ ] For each AI use: log what it was asked, whether it was right, what time it saved or cost.
- [ ] **Close** (30 m): record solves, blockers, and the one thing to change tomorrow.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sun Oct 18 · D05 · T-34 · DEADFACE day 2
- [ ] Continue from the triage board. Prioritize unsolved items where you have a concrete hypothesis.
- [ ] Spend at least one block on the weakest category from yesterday, manually first.
- [ ] **Close** (30 m): update run record; copy each solved challenge into `notes/` as a 5-line writeup.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Mon Oct 19 · D06 · T-33 · DEADFACE end + recovery
- [ ] Final hours only if time allows (ends ~Oct 19; verify exact end time).
- [ ] **Learn (20 m):** read 3 public writeups for challenges you did not solve; note what first-observation you missed.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Tue Oct 20 · D07 · T-32 · Post-run review
- [ ] **Review (45 m):** complete the DEADFACE record: points/hour, category totals, time lost to setup, time lost to dead ends, what the AI helped with and where it misled.
- [ ] **Practice (30 m):** replay one unsolved challenge with a fresh approach.
- [ ] **Build (30 m):** shell-in-container MCP: write the allowlist and threat model (what it may run, what it must never touch). Document before coding.
- [ ] **Close** · weekly review: update the checklist table and `STATUS.md`.
- Log: min __ · solved __ · stuck on __ · AI used? __

---

## Phase 2: Breadth across categories (Oct 21-Nov 5)

### Wed Oct 21 · D08 · T-31 · Forensics: pcap
- [ ] **Learn (25 m):** Wireshark display filters, Follow TCP stream, Export Objects, Statistics → Conversations/Protocol Hierarchy; tshark equivalents.
- [ ] **Practice (60 m):** two exercises from malware-traffic-analysis.net (start with the oldest, beginner ones); answer the questions in the exercise first, check the answers after.
- [ ] **Drill (15 m):** extract a file from HTTP traffic with tshark only.
- [ ] **Build (20 m):** pcap summarizer script: tshark stats → JSON → (later) model summary.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Oct 22 · D09 · T-30 · Crypto I
- [ ] **Learn (25 m):** XOR, base-N, modular arithmetic, RSA basics (n, e, d, c).
- [ ] **Practice (60 m):** CryptoHack: Introduction + General (all), Mathematics intro.
- [ ] **Drill (15 m):** write `xor_bruteforce.py` and `rsa_basic.py` helpers from memory.
- [ ] **Build (20 m):** pre-Hack.lu: choose roles; decide which categories to attempt (easiest two per category only).
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Fri Oct 23 · D10 · T-29 · Hack.lu / HITCON day 1 (learning)
- [ ] Start one event only; the second is optional.
- [ ] Goal: **2 observations per challenge, not flags.** Record the first useful observation, and the technique you did not know.
- [ ] After 45 min per challenge: read hints, then writeups if available.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Oct 24 · D11 · T-28 · Hack.lu / HITCON day 2
- [ ] Attempt every category's easiest challenge.
- [ ] Add every unknown technique to a "to learn" list in `notes/`.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sun Oct 25 · D12 · T-27 · Hack.lu / HITCON day 3 + weekly review
- [ ] Finish; no pressure to solve.
- [ ] **Review (60 m):** take the "to learn" list, rank by how often each technique appears in easy CTFs, pick the top 3 for next week.
- [ ] Weekly review: update checklist statuses with evidence.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Mon Oct 26 · D13 · T-26 · Web II
- [ ] **Learn (25 m):** PortSwigger: authentication, access control/IDOR.
- [ ] **Practice (60 m):** 5 labs from each of the two topics.
- [ ] **Drill (15 m):** Juice Shop: finish all one- and two-star challenges you haven't done.
- [ ] **Build (20 m):** notes/RAG: ingest your own writeups into the search index; test 5 queries.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Tue Oct 27 · D14 · T-25 · Web III
- [ ] **Learn (25 m):** XSS types (reflected/stored/DOM), SSTI, command injection.
- [ ] **Practice (60 m):** PortSwigger: XSS (10 labs), OS command injection (all), SSTI (all).
- [ ] **Drill (15 m):** write a Python `requests` script that automates one of the above.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Wed Oct 28 · D15 · T-24 · Linux privesc + network services
- [ ] **Learn (25 m):** sudo -l, SUID, cron, capabilities, writable PATH; GTFOBins lookup flow.
- [ ] **Practice (60 m):** TryHackMe "Linux PrivEsc" (or a VulnHub box such as Basic Pentesting 1 / Kioptrix 1) — enumerate manually before running linpeas.
- [ ] **Drill (15 m):** Nmap: full TCP scan → targeted scripts → service notes; write the one-liner you'll reuse.
- [ ] **Build (20 m):** Ghidra headless wrapper: decompile one function to text on a sample binary.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Oct 29 · D16 · T-23 · Windows + AD
- [ ] **Learn (25 m):** Kerberos at 10,000 feet; AS-REP roasting, Kerberoasting; BloodHound graph reading.
- [ ] **Practice (60 m):** TryHackMe "Active Directory Basics" + "Attacktive Directory"; or your own Server 2022 AD lab on Machine B.
- [ ] **Drill (15 m):** SMB enumeration with smbclient/enum4linux-ng/crackmapexec on a lab target.
- [ ] **Build (20 m):** hashcat on Machine B's GPU: run a benchmark and confirm it works over SSH.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Fri Oct 30 · D17 · T-22 · Reverse I
- [ ] **Learn (25 m):** x86-64 calling convention, stack frames, `strings`/`ltrace`/`strace` first, Ghidra project setup.
- [ ] **Practice (60 m):** crackmes.one: 3 easy (difficulty 1-2) Linux crackmes; solve each with static analysis first.
- [ ] **Drill (15 m):** rename + retype variables in Ghidra until the decompilation reads cleanly.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Oct 31 · D18 · T-21 · 4-hour mock (no AI)
- [ ] Pick a solved-by-others set: picoCTF 2023-2025 mixed categories (or Hackropole). Time-box 4 h, team roles active.
- [ ] Record points/hour, category time split, where time leaked.
- [ ] **Close** (30 m): compare to DEADFACE run record.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sun Nov 1 · D19 · T-20 · Pwn I + weekly review (DST ended: clocks back 1 h)
- [ ] **Learn (30 m):** ELF basics, stack layout, protections (NX/PIE/canary/RELRO) via `checksec`.
- [ ] **Practice (75 m):** pwn.college "Intro to Cybersecurity" + early "Shellcode Injection" or ROP Emporium ret2win (x64).
- [ ] **Review (45 m):** weekly review; update checklist; adjust the next week's focus to the lowest-status categories.
- [ ] **Build (20 m):** write the competition-day runbook gaps list in `operations/competition-day-runbook.md`.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Mon Nov 2 · D20 · T-19 · Crypto II
- [ ] **Learn (25 m):** RSA attacks (small e, common modulus, Wiener, factordb), AES-ECB/CBC pitfalls.
- [ ] **Practice (60 m):** CryptoHack: RSA starter + symmetric ciphers; Cryptopals Set 1-2 (first 4 challenges).
- [ ] **Drill (15 m):** solve one RSA challenge using only Python + sympy, no external solver.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Tue Nov 3 · D21 · T-18 · Blue team / IR
- [ ] **Learn (25 m):** Windows event IDs (4624, 4625, 4688, 4768/4769, 7045), Sysmon event IDs (1, 3, 11), Linux auth.log patterns.
- [ ] **Practice (60 m):** CyberDefenders: two easy labs (or Blue Team Labs Online free challenges); build a timeline before answering.
- [ ] **Drill (15 m):** write one Sigma-style detection rule for a technique you practiced.
- [ ] **Build (20 m):** log-triage pipeline: parse → filter → timeline → (model) summary.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Wed Nov 4 · D22 · T-17 · Web IV (SSRF/deserialization/files)
- [ ] **Learn (25 m):** SSRF, file upload bypasses, insecure deserialization (PHP/Python pickle).
- [ ] **Practice (60 m):** PortSwigger: SSRF (all), file upload (all), insecure deserialization (first 3).
- [ ] **Drill (15 m):** timed: solve 2 labs in 20 min total.
- [ ] **Close**
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Nov 5 · D23 · T-16 · Pre-weekend prep
- [ ] **Review (30 m):** the rehearsal weekend plan: which event(s), roles, AI mode (decide per event, record).
- [ ] **Practice (45 m):** your weakest category, targeted: one easy challenge, manual first.
- [ ] **Build (30 m):** tool freeze v1: anything unstable gets disabled for the weekend; record what is enabled.
- [ ] **Close** · rest.
- Log: min __ · solved __ · stuck on __ · AI used? __

---

## Phase 3: Volume and rehearsal (Nov 6-15)

### Fri Nov 6 · D24 · T-15 · CSCTF / PINK+ / HKCERT start
- [ ] Choose the one that fits best (check categories on CTFtime). Don't split attention across all three.
- [ ] Triage and roles; record AI mode.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Nov 7 · D25 · T-14 · Volume day
- [ ] 6-hour focused block + one hour on a second event's easiest challenges.
- [ ] Log points/hour by category.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sun Nov 8 · D26 · T-13 · Volume day 2
- [ ] Same shape as Saturday.
- [ ] Weekly review at end of day.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Mon Nov 9 · D27 · T-12 · End + recovery
- [ ] Finish events; write-ups for everything solved.
- [ ] Rest block: 30 min away from the keyboard.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Tue Nov 10 · D28 · T-11 · Weakness deep dive 1
- [ ] Pick the lowest category from the weekend's data. 90 min of structured practice from `curriculum/practice-suite.md`.
- [ ] **Build (20 m):** AI benchmark: replay 3 solved challenges with model A/B/none; record time and correctness.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Wed Nov 11 · D29 · T-10 · Weakness deep dive 2 + offline test
- [ ] Second-lowest category, 60 min.
- [ ] **Offline test (45 m):** airplane mode; cold-start Ollama, run RAG search, run shell MCP, open Ghidra and Wireshark. Write down everything that fails.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Nov 12 · D30 · T-9 · Bundle v1 + pre-rehearsal
- [ ] Freeze competition bundle v1: models, RAG index, wordlists, cheat sheets, tool installers, offline docs on a USB drive and laptop.
- [ ] Team call: roles, communication, who owns submissions.
- [ ] 45-min light practice.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Fri Nov 13 · D31 · T-8 · Light day
- [ ] Platypwn / WolvCTF: easy tier only, evenings, max 2 hours. Protect tomorrow.
- [ ] Early sleep.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Nov 14 · D32 · T-7 · InIt CTF: full dress rehearsal
- [ ] Event 15:30-23:30 UTC (10:30-18:30 EST); confirm on [CTFtime](https://ctftime.org/event/3467).
- [ ] Treat it as the real day: same laptop, same bundle, same roles, same AI mode you plan to use on Nov 21, same snacks.
- [ ] Offline mode if you plan to be offline.
- [ ] Log time-stamped decisions: what you tried, when you switched, what blocked.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sun Nov 15 · D33 · T-6 · Debrief
- [ ] **Review (90 m):** top-3 issues (process, tool, knowledge). Decide one fix each.
- [ ] Finish WolvCTF only if you feel good.
- Log: min __ · solved __ · stuck on __ · AI used? __

---

## Phase 4: Taper and competition (Nov 16-21)

### Mon Nov 16 · D34 · T-5 · Fixes + drill
- [ ] Apply the three fixes from the debrief; re-test each.
- [ ] 60 min: timed 3-challenge drill in the weakest category.
- [ ] Resume and interview prep (1 page, project stories: lab, CTFs, AI stack).
- Log: min __ · solved __ · stuck on __ · AI used? __

### Tue Nov 17 · D35 · T-4 · Cheat sheets + offline bundle
- [ ] One-page cheat sheet per category (print or PDF).
- [ ] Re-run offline test; fix remaining failures.
- [ ] 45 min light practice.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Wed Nov 18 · D36 · T-3 · Freeze
- [ ] **Bundle v2 frozen.** No new tools after today.
- [ ] 60 min: one easy box or CTF challenge, just to keep sharp.
- [ ] Confirm laptop OS updates are paused/disabled for the weekend.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Thu Nov 19 · D37 · T-2 · Logistics
- [ ] Venue address, start time, ID, student card, charger, Ethernet adapter, USB drive, snacks, water.
- [ ] Team sync: roles, submission owner, communication, break plan.
- [ ] Read the competition rules once more, specifically AI/internet/tools.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Fri Nov 20 · D38 · T-1 · Rest
- [ ] Skip GlacierCTF (already decided).
- [ ] Pack. Charge everything. Verify the laptop boots and the VM starts.
- [ ] Sleep 8 h.
- Log: min __ · solved __ · stuck on __ · AI used? __

### Sat Nov 21 · D39 · T-0 · CyberSci Regional Qualifiers
- [ ] Arrive early; check network, rules, platform login.
- [ ] Triage first. Roles. 30-minute rule. Logs.
- [ ] Interviews in the afternoon: bring resumes, tell the CTF-and-lab story.
- Log: min __ · solved __ · stuck on __ · AI used? __
