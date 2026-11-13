# 29. picoCTF / picoGym activity book

picoCTF is a free, beginner-friendly CTF from Carnegie Mellon. **picoGym** keeps past challenges open year-round, organised by category, with difficulty tags. Its categories (General Skills, Cryptography, Web Exploitation, Forensics, Reverse Engineering, Binary Exploitation) mirror CyberSci's.

> **Verify names.** I can't reliably list current picoGym challenge titles. Use the **filters** instead: choose a category, sort by most solved or easiest, and pick the ones that match the skill in the "Read first" column. A few names that appeared in community guides: **Insp3ct0r** (web), **Warmed Up** and **First Grep** (general skills): check each in picoGym.

## Rules for yourself

- Don't copy flags or share solutions (platform policy).
- Time-box each challenge to 30-45 minutes for Attempt 1.
- Log the highest hint rung you used.

## Activities (5 challenges per set)

| ID | Category filter | Pick | Read first | Time | Attempt 2 |
|---|---|---|---|---|---|
| PICO-01 | **General Skills** | 5 easiest by solves | Module 7 §7.1; Bandit commands | 60 min | 5 different ones in 35 min |
| PICO-02 | **Cryptography** | 5 easiest (encodings, classical, XOR, small RSA) | Module 4 §4.1-4.6 | 90 min | Labs 2-4 variant B |
| PICO-03 | **Web Exploitation** | 5 easiest (view source, cookies, robots, SQLi) | Module 3 §3.1-3.3 | 90 min | Lab 8 variant B |
| PICO-04 | **Forensics** | 5 easiest (strings, exiftool, binwalk, pcap) | Module 2 §2.2-2.3 | 90 min | Lab 7 variant B |
| PICO-05 | **Reverse Engineering** | 3 easiest | Module 5 §5.2-5.5 | 90 min | Lab 14 variant B |
| PICO-06 | **Binary Exploitation** | 2 easiest | Module 5 §5.7 | P2 | |

## Attempt, review, reinforce

After each set:

1. Write a five-line writeup for every challenge you solved.
2. List every tool/command you had to look up and make a flashcard.
3. Re-read the linked section.
4. Attempt 2: a fresh set at the same difficulty, in 60% of the time.

## Mock CTF day (once, before Nov 21)

Pick **one hour**, **10 challenges across categories**, and run the triage routine (rank by points per estimated minute, 30-minute rule). This rehearses the real event.

## Logging

```bash
python scripts/activity.py log PICO-02 1 B 85
python scripts/activity.py log PICO-02 2 A 50
```

## Check yourself

1. Why filter by "most solved" for early practice?
2. How do you decide when to stop and swap?
3. Which category gave you the biggest time leak?
