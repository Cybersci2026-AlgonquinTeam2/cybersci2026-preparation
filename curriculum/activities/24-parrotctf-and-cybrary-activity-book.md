# 30. Parrot CTFs and Cybrary activity book

Two different kinds of resources: **Parrot CTFs** (hands-on challenges) and **Cybrary** (mostly video courses). Treat both as supplements to the platforms that cost nothing.

> **Verify access and pricing.** My information comes from the companies' own materials and third-party pages, not their sites. **Check each site for what is free before planning around it.**

## Parrot CTFs

What the public descriptions say: a training platform with **virtual-machine challenges** that simulate real vulnerabilities, downloadable **reverse-engineering/fuzzing labs**, "hacking rooms" that resemble a penetration-test scope rather than simple flag hunts, and categories including **web, Active Directory, cryptography and forensics**. They also publish a free standalone **Micro Labs** application with focused exercises (for example XSS and brute-forcing logins). Some content is free for a limited period. (Source: Parrot CTFs help centre, company listings, and the Micro Labs repository.)

### Activities

| ID | What | Read first | Time | Attempt 2 |
|---|---|---|---|---|
| PAR-01 | **Micro Labs: XSS** exercises | Module 3 §3.4 | 45 min | redo and write each payload from memory |
| PAR-02 | **Micro Labs: login brute-forcing** | Module 3 §3.5, Module 11 §11.3 | 45 min | write your own script instead of using a tool |
| PAR-03 | A free **web** challenge (VM or room) | Module 3 | 60 min | the second web challenge |
| PAR-04 | A free **crypto** or **forensics** challenge | Module 4 / 2 | 60 min | |
| PAR-05 | A **fuzzing/reverse-engineering** lab (if free) | Module 5 | P2 | |

Run any downloaded VM on your **isolated host-only lab**; read the platform's rules first.

## Cybrary

From third-party summaries: the **free tier is video-based** (security fundamentals, compliance, tool introductions) with a **limit on daily activities**, while hands-on labs and practice tests are in the **paid** plan. Because the free content is video-heavy, use it for *concepts*, and do the hands-on work elsewhere in this pack.

### How to use a video course actively (so it isn't passive)

1. **Before** the video: read the pack section on the same topic (10 minutes).
2. **During:** pause at each new term; write it and a one-line definition.
3. **After:** do a mini-exercise (a lab or flashcards) on that concept.
4. **Next day:** explain the concept aloud in two minutes.

### Activities

| ID | Topic to search | Read first | Time |
|---|---|---|---|
| CYB-01 | A beginner **networking / security fundamentals** course | Module 6 §6.1; Module 8 §8.3 | 2 h |
| CYB-02 | **Incident response / SOC** introduction | Module 8 §8.5; Module 13 | 2 h |
| CYB-03 | **Frameworks / compliance** (NIST, ISO) | Module 8 §8.7 | 1 h |

If a course is paid, skip it and use the corresponding module and labs.

## Logging

```bash
python scripts/activity.py log PAR-01 1 B 50
python scripts/activity.py log CYB-01 1 B 120
```

## Check yourself

1. What's the difference between a hands-on lab and a video?
2. How do you turn a video into active learning?
3. Which of these two resources is most relevant to the regionals, and why?
