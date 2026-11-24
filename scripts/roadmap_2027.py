#!/usr/bin/env python3
"""Write tracker/roadmap.csv (weekly plan Nov 2026 -> Dec 2027) and tracker/milestones.csv (competition calendar).

Run:  python scripts/roadmap_2027.py   then   python scripts/tracker.py render && python scripts/export_xlsx.py
The previous roadmap (to Jun 2027, aimed at CyberSci Nationals only) is kept as tracker/roadmap.v1.csv.

Dates marked 'confirmed' come from the organiser's own page when this was written (2026-11-24). 'expected' means
the date is inferred from last year's pattern: confirm it before planning travel, fees or a team. Same cadence as the
original plan: 4 h study per day + ~1 h weekday commute reading = 28 h/week; taper and exam-buffer weeks are lower.
"""
import csv
import shutil
from datetime import date, timedelta
from pathlib import Path

T = Path(__file__).resolve().parent.parent / "tracker"
START = date(2026, 11, 23)  # a Monday

# (phase, theme, practice, reading, backlog_ids, events, gate, level, hours)
P5 = "P5 Debrief + gap closure"
P6 = "P6 Deepen"
P7 = "P7 Spring season"
P8 = "P8 Nationals + summer peak"
P9 = "P9 Build + fall season"

W = [
 (P5, "Debrief the qualifier + warm-up", "Mon: write the run record (what you solved, what stalled, minutes per flag, tools you reached for). Rank weaknesses by category. Redo every failed item. Advent of Cyber opens Dec 1: 30 min a day as a warm-up. Check CyberSci Regionals results.", "Your qualifier notes; Hacker Playbook 3 (web + AD chapters)", "W08 W13 W14 W15", "CyberSci Regionals results (check email/site); SANS Holiday Hack open Nov 18-Jan 5 (confirmed)", "Run record + top 3 weaknesses ranked; Advent of Cyber days 1-7 done", "L2", 28),
 (P5, "Boxes + manual privesc", "VulnHub + Metasploitable; 2 HTB easy boxes; manual Linux privesc until linpeas is redundant. Use the mangui pages (man nmap, man getcap, man crontab) instead of searching the web.", "HackTricks: Linux + Windows privesc", "L05 L06 L07 L13", "Advent of Cyber Dec 1-24 (confirmed, free, daily)", "4 boxes rooted with written methodology", "L3", 28),
 (P5, "AD fundamentals + first team CTF", "GOAD or own Server 2022 lab; BloodHound; Kerberoast; pivoting with chisel/ligolo. Weekend: HTB University CTF (if your team is eligible) or niteCTF; do one, not both.", "The Hacker Recipes AD; ired.team notes", "L11 L12 L09", "HTB University CTF ~mid Dec (expected; needs academic email + team); niteCTF ~Dec 11-13 (expected)", "Domain admin via 2 paths from a cold start; first team-CTF results written up", "L3", 28),
 (P5, "Forensics + blue deepen (exam buffer)", "HTB Sherlocks; CyberDefenders medium; Sigma/Sysmon/Suricata; 3 one-page IR reports. Confirm your exam dates and cut hours if finals fall here.", "NIST 800-61; SANS DFIR posters; MITRE ATT&CK", "F08 F10 F12", "Advent of Cyber finishing; school finals (confirm dates)", "3 IR reports <1 page each", "L3", 20),
 (P6, "Break + light maintenance", "Light CTFs for fun; maintain notes; sleep. ASIS CTF Finals Dec 27-28 is hard: play for an hour if you want, no target.", "Podcasts + books of choice", "", "ASIS CTF Finals Dec 27-28 (confirmed, hard)", "Rested; notes up to date", "L2", 14),
 (P6, "Reverse engineering", "Managed code, packers, anti-debug, angr/z3, malware triage in a VM. Ghidra daily (see man ghidra).", "Reverse Engineering for Beginners; Practical Malware Analysis", "R04 R05", "SANS Holiday Hack closes Jan 5, winners Jan 20 (confirmed)", "10 crackmes solved incl. 3 medium", "L3", 28),
 (P6, "Binary exploitation", "ROP Emporium 5-8; format strings; heap basics; pwn.college modules; pwntools scripts.", "Nightmare; Hacking: The Art of Exploitation; how2heap", "P03 P04 P05 P06", "", "A ROP chain + a format-string write from scratch", "L3", 28),
 (P6, "Cryptography", "Finish CryptoHack courses; ECC and lattices intro; padding oracle script; Cryptopals sets 2-3.", "Serious Cryptography; Boneh-Shoup (selected chapters)", "C06", "", "CryptoHack score 60%+ of challenges", "L3", 28),
 (P6, "Web expert", "PortSwigger expert labs; request smuggling; deserialisation; Burp extensions (man burpsuite).", "Web Application Hacker's Handbook (selected)", "", "NCL Spring registration opens ~late Jan (expected)", "20 PortSwigger practitioner + 5 expert labs", "L3", 28),
 (P6, "Team formation + recon speed", "Recruit and test your team: roles per category, shared notes, one comms channel. Recon drill: full enumeration of a box in under 15 min with saved scripts.", "NorthSec rules + past writeups", "", "Insomni'hack Feb 1-5 (onsite Switzerland, skip; watch writeups); LACTF ~Feb (expected)", "Team list agreed (aim for 8 for NorthSec); recon script set in repo", "L3", 28),
 (P6, "AD advanced", "ADCS, delegation, trusts, cross-forest; detection side with Sysmon/ELK.", "ired.team + SpecterOps papers", "", "", "Domain compromise through ADCS in a lab, with the detection written", "L3", 28),
 (P6, "Cloud + containers", "Docker escape basics, K8s misconfig lab, AWS/S3 IAM labs (free tier). man docker, man bash.", "OWASP Docker/Kubernetes cheat sheets", "", "", "Escape one container lab; one IAM path to admin", "L2", 28),
 (P7, "Timed mixed sets + first spring CTF", "Timed 4-hour sets: 2 web, 2 pwn/rev, 2 crypto, 2 forensics. Play DiceCTF/other spring qualifier as practice.", "Past-year writeups for the CTFs on the calendar", "", "DiceCTF 2027 quals ~early Mar (expected); picoCTF registration opens Feb (expected)", "Timed set: 6/10 solved in 4 h", "L3", 28),
 (P7, "picoCTF + beginner-bracket points", "picoCTF 2027 (expected March, ~10 days, Gym practice before). Aim for a top-tier score as a guaranteed milestone.", "picoGym archive", "", "picoCTF 2027 ~Mar (expected; dates unannounced)", "picoCTF: finish with all Web/Crypto/Forensics solved; log time per flag", "L3", 28),
 (P7, "Attack/defend", "Run an attack/defend drill with the team: defend a Juice Shop/DVWA stack, patch, monitor logs, then attack your teammates'.", "SANS blue team material; CCDC study guides", "", "", "One full attack/defend session; defence runbook updated", "L3", 28),
 (P7, "Medium boxes + registration check", "Medium HTB boxes. Register NCL Spring (about $45 individual); confirm NorthSec registration process and team tickets.", "HackTricks as reference only", "", "NCL Spring registration closes ~late Mar (expected)", "NCL registered; NorthSec team registered or waitlist status known", "L3", 28),
 (P7, "Pwn medium + NCL practice", "Heap + stack mix; NCL practice game when it opens. Gym.", "how2heap; ROP Emporium recap", "", "", "3 medium pwn solved from scratch", "L3", 28),
 (P7, "NCL Spring individual + reverse medium", "NCL Spring individual game (3-day window; expected mid April). Reverse medium sets.", "", "", "NCL Spring individual ~mid Apr (expected); team game ~late Apr", "NCL individual: top-bracket percentile target (set after the practice game)", "L3", 28),
 (P7, "Exam buffer + NCL team game", "Keep maintenance only if exams. NCL team game with your team (late April, expected).", "", "", "NCL team game ~late Apr (expected); school finals (confirm)", "NCL team game played; exam hours protected", "L2", 20),
 (P7, "Web medium + OSINT + scripting", "Web medium sets, OSINT drills, Python/bash speed (man bash, man printf).", "", "", "", "Timed OSINT + scripting set: 5/8 in 2 h", "L3", 28),
 (P7, "NorthSec rehearsal 1", "Full-day team rehearsal on an old NorthSec-style set (tracks: web, hardware/IoT, network, forensics, reverse). Fix roles and notes.", "NorthSec past writeups", "", "", "Rehearsal debrief: points/hour per person, 3 fixes", "L3", 28),
 (P7, "NorthSec rehearsal 2 + tool freeze", "Second rehearsal. Freeze tools and notes: offline mirror, cheat sheets, mangui installed in the VM.", "", "", "NorthSec 2027 CTF May 14-16, Montreal (confirmed; regular + AI experience)", "Tool freeze committed; travel/lodging booked", "L3", 28),
 (P7, "NorthSec taper + play", "Light review Mon-Wed, rest Thu, then play. NorthSec CTF Fri May 14 to Sun May 16.", "None: sleep", "", "NorthSec CTF May 14-16 (confirmed); NorthSec conference ~May 17-23 (unconfirmed)", "MILESTONE: NorthSec played; post-event debrief written within 48 h", "L3", 20),
 (P8, "Debrief + DEF CON quals window", "Debrief NorthSec; fix the 3 weakest categories. DEF CON CTF qualifier is expected in late May: play if time allows.", "NorthSec winners' writeups", "", "DEF CON 35 CTF qualifier ~late May (expected; organiser BBB birds)", "Debrief done; one weakness class closed", "L3", 28),
 (P8, "Nationals prep or Plan B", "If you qualified: CyberSci Nationals prep (attack/defend + scenario chains). If not: pick Google CTF + HTB/Apocalypse as the June targets.", "CyberSci past finals writeups", "", "CyberSci Nationals June 2027 (confirmed month; Ottawa hosted 2026, regional winners only)", "Decision made: Track A (Nationals) or Track B (Google CTF)", "L3", 28),
 (P8, "Nationals window / Plan B", "Track A: CyberSci Nationals (2026 was Jun 12-15; expect similar). Track B: full Google CTF prep.", "", "", "CyberSci Nationals ~mid Jun (expected); Google CTF quals ~late Jun (expected)", "MILESTONE: Nationals played, or Google CTF quals played", "L3", 20),
 (P8, "Google CTF + summer reset", "Google CTF quals weekend if not clashing with Nationals; then one rest day, one lab day, one writeup day.", "Last year's Google CTF writeups", "", "Google CTF quals ~Jun 18-20 (expected)", "Writeups published for 3 solved challenges", "L3", 24),
 (P8, "Summer build 1: your own lab", "Build the dojo/lab you want: a home range with AD, web, and a monitored network (see dojo-platform-backlog).", "", "", "", "Lab rebuildable from one command/script", "L3", 28),
 (P8, "Summer build 2: tooling + notes", "Rewrite your notes as a searchable offline wiki; extend mangui guides from your real use; automate recon.", "", "", "", "Recon automation tested on 5 boxes", "L3", 28),
 (P8, "UIUCTF + HTB Apocalypse window", "Play UIUCTF (late July expected); HTB Cyber Apocalypse date unconfirmed (2026 ran Jul 24-29).", "", "", "UIUCTF ~Jul 24-26 (expected); HTB Cyber Apocalypse (watch)", "UIUCTF: 3+ flags across 2 categories", "L3", 28),
 (P8, "Hard targets", "Pick 3 hard challenges from archives (CTFtime 'hard' tag) and finish them over the week.", "", "", "", "3 hard challenges solved, writeups published", "L3", 28),
 (P8, "DEF CON week (watch or attend)", "DEF CON 35 Aug 5-8, Las Vegas (confirmed). Attending is optional and costly; watch talks/CTF writeups either way. Maintain: 2 h/day.", "DEF CON talks, Villages", "", "DEF CON 35 Aug 5-8 (confirmed)", "One technique from a talk reproduced in your lab", "L2", 16),
 (P9, "Rest + term planning", "Rest, plan the fall term, register the team for NCL Fall and CyberSci Regionals as soon as they open.", "", "", "NCL Fall registration opens ~Aug (expected)", "Fall calendar copied into your own calendar", "L2", 14),
 (P9, "Cert track or deep specialty (choose one)", "Choose a lane for the fall: OSCP-style boxes, a blue-team lane (BTL1/CySA), or reverse/pwn depth. Keep CTF practice on weekends.", "Chosen lane's official syllabus", "", "", "Lane chosen and week-by-week plan added", "L3", 28),
 (P9, "Specialty week 1", "Lane work: 3 days lane + 2 days CTF drills + 1 day writeups.", "", "", "", "Lane checkpoint 1 met", "L3", 28),
 (P9, "Specialty week 2", "Lane work.", "", "", "CSAW CTF quals ~mid Sep (expected)", "Lane checkpoint 2 met", "L3", 28),
 (P9, "CSAW quals + speed", "CSAW CTF quals (48 h, expected mid Sep). Speed drills.", "CSAW past challenges", "", "CSAW quals ~Sep 17-19 (expected)", "CSAW: 5+ challenges solved", "L3", 28),
 (P9, "Specialty week 3", "Lane work.", "", "", "", "Lane checkpoint 3 met", "L3", 28),
 (P9, "Team rebuild for Regionals", "Rebuild the team for CyberSci 2027-28 Regionals: roles, cheat sheets, runbook (competition-day-runbook.md refresh).", "CyberSci sponsors/regionals info", "", "CyberSci Regionals 2027 ~Nov 20 (expected; register early)", "Team registered; runbook v2 tested", "L3", 28),
 (P9, "Specialty week 4", "Lane work.", "", "", "NCL Fall practice game ~mid Oct (expected)", "Lane checkpoint 4 met", "L3", 28),
 (P9, "Hackfest CTF + NCL individual", "Hackfest Quebec City Oct 21-23 (confirmed; CTF details unannounced; tickets sold separately) clashes with the NCL individual game: pick Hackfest if you travel, NCL if not.", "", "", "Hackfest Oct 21-23 (confirmed); NCL Fall individual ~Oct 22-24 (expected)", "MILESTONE: one of the two played; writeups within 48 h", "L3", 28),
 (P9, "NCL team + CSAW finals window", "NCL Fall team game (expected early Nov). CSAW finals (invite only; expected Nov).", "", "", "NCL Fall team game ~Nov 5-7 (expected)", "NCL team game played; debrief written", "L3", 28),
 (P9, "Regionals sprint", "Full-day rehearsals; timed mixed sets; rest the day before.", "", "", "SANS Holiday Hack opens mid-Nov (expected)", "Rehearsal: 8/12 in the Regionals time limit", "L3", 28),
 (P9, "CyberSci Regionals + BSides Ottawa", "BSides Ottawa ~Nov 18-19 (expected, has a CTF); CyberSci Regionals ~Sat Nov 20 (expected).", "None: sleep", "", "CyberSci Regionals ~Nov 20 (expected); BSides Ottawa ~Nov 18-19 (expected)", "MILESTONE: Regionals played; qualified for Nationals 2028?", "L3", 24),
 (P9, "Advent of Cyber + HTB University CTF", "Advent of Cyber 2027 Dec 1+ (expected); HTB University CTF mid-Dec (expected).", "", "", "Advent of Cyber 2027 ~Dec 1 (expected); HTB University CTF 2027 ~mid Dec (expected)", "HTB University CTF played with the team", "L3", 28),
 (P9, "Year review", "Write the 12-month review: milestones hit/missed, points per hour, skills ladder; plan 2028.", "Your own run records", "", "ASIS CTF Finals ~late Dec (expected)", "Year review + 2028 roadmap draft", "L2", 14),
]

# id, start, end, event, type, format, eligibility/where, confidence, prep_from, primary, goal, notes
M = [
 ("M01", "2026-11-18", "2027-01-05", "SANS Holiday Hack Challenge 2026", "puzzle/CTF", "online, free, solo", "Open worldwide", "confirmed", "2026-11-23", "optional", "Complete the objectives; submit the report before Jan 5 (winners Jan 20)", "Good low-pressure web/forensics practice"),
 ("M02", "2026-12-01", "2026-12-24", "TryHackMe Advent of Cyber 2026", "beginner daily", "online, free, solo", "Open", "confirmed", "2026-12-01", "optional", "All 24 days done (30 min a day), notes written", "Beginner-level; warm-up only"),
 ("M03", "2026-12-11", "2026-12-13", "HTB University CTF 2026 (mid-Dec, unconfirmed)", "team CTF", "online, jeopardy", "University teams; academic email verified on HTB", "expected", "2026-11-30", "yes", "Team registered by registration deadline; solve 3+ challenges across 2 categories", "A page lists 'Dec 12, 2026' but I could not confirm it is this event; 2023: Dec 8-10, 2024: Dec 13-15"),
 ("M04", "2026-12-11", "2026-12-13", "niteCTF 2026 (alternative that weekend)", "team CTF", "online, jeopardy", "Open", "expected", "2026-11-30", "alt", "Play if HTB University CTF is not available; 2+ flags", "niteCTF 2025 ran Dec 12-14"),
 ("M05", "2026-12-27", "2026-12-28", "ASIS CTF Finals 2026", "team CTF", "online, jeopardy", "Qualified/open per CTFtime", "confirmed", "2026-12-21", "optional", "Play 1-2 h; goal is exposure to hard challenges", "Hard; no target"),
 ("M06", "2027-02-01", "2027-02-05", "Insomni'hack 2027 (conference week)", "conference + CTF", "onsite, Lausanne", "Onsite only", "confirmed", "", "skip", "Read the writeups when published", "CTF is onsite; may be a different week than the conference"),
 ("M07", "2027-03-01", "2027-03-31", "picoCTF 2027", "beginner-friendly CTF", "online, solo/team", "Open (CMU)", "expected", "2027-02-15", "yes", "Finish the Web/Crypto/Forensics sets; log time per flag", "2026 ran Mar 9-19, registration Feb 1-Mar 17; 2027 dates not yet announced"),
 ("M08", "2027-03-05", "2027-03-07", "DiceCTF 2027 Quals (early March)", "team CTF", "online, jeopardy", "Open", "expected", "2027-02-22", "optional", "3+ flags; solo or with team", "2026 quals were Mar 7-8"),
 ("M09", "2027-01-25", "2027-03-31", "NCL Spring 2027 registration", "league", "online", "Students; ~US$45", "expected", "2027-01-25", "yes", "Registered before the late fee", "2026 registration Jan 26-Mar 27"),
 ("M10", "2027-04-09", "2027-04-25", "NCL Spring 2027 games (individual + team)", "league", "online, individual then team", "Students", "expected", "2027-03-15", "yes", "Individual: set a percentile target after the practice game; team: play with your team", "2025: individual Apr 11-13, team Apr 25-27"),
 ("M11", "2027-05-14", "2027-05-16", "NorthSec 2027 CTF", "team CTF", "onsite Montreal (Bonsecours Market), teams of 8", "Teams of 8; regular and AI experiences", "confirmed", "2027-02-01", "yes", "Team of 8 registered; 1+ flag in each track; every member scores", "Official dates May 14-16; venue 'to be confirmed' on the registration page; the conference is ~May 17-23 (unconfirmed)"),
 ("M12", "2027-05-21", "2027-05-23", "DEF CON 35 CTF Qualifier (late May)", "team CTF", "online, jeopardy-style", "Open", "expected", "2027-05-17", "optional", "Play for exposure", "DC34 qualifier ran May 22-24, 2026; 2027 dates not yet announced"),
 ("M13", "2027-06-11", "2027-06-14", "CyberSci Nationals 2027", "national finals", "onsite, jeopardy + defence", "Regional winners; Ottawa hosted 2026 (Jun 12-15)", "expected", "2027-04-19", "yes (if qualified)", "Prep if you qualified; otherwise Track B (Google CTF)", "Official site: next national event June 2027; exact dates not posted"),
 ("M14", "2027-06-18", "2027-06-20", "Google CTF 2027 Quals (late June)", "team CTF", "online, jeopardy", "Open", "expected", "2027-06-01", "optional", "1+ flag", "2026 quals Jun 19-21"),
 ("M15", "2027-07-24", "2027-07-26", "UIUCTF 2027 (late July)", "team CTF", "online, jeopardy", "Open", "expected", "2027-07-12", "optional", "3+ flags across 2 categories", "2026 ran Jul 25-27"),
 ("M16", "2027-08-05", "2027-08-08", "DEF CON 35", "conference", "Las Vegas", "Paid; optional", "confirmed", "", "optional", "Watch talks and CTF/village writeups", ""),
 ("M17", "2027-09-17", "2027-09-19", "CSAW CTF Quals 2027 (mid-September)", "team CTF", "online, 48 h jeopardy", "Open", "expected", "2027-09-06", "yes", "5+ challenges solved", "2026 quals Sep 18-20; finals invite-only in Nov"),
 ("M18", "2027-10-15", "2027-11-07", "NCL Fall 2027 (practice, individual, team)", "league", "online", "Students", "expected", "2027-08-23", "yes", "Individual then team game; register in Aug-Oct", "2026: individual Oct 23-25, team Nov 6-8"),
 ("M19", "2027-10-21", "2027-10-23", "Hackfest 2027 (Quebec City), CTF + StealthCup", "conference + CTF", "onsite", "Paid ticket; CTF may need a separate ticket", "confirmed", "2027-09-20", "optional", "Pick Hackfest or the NCL individual game for that weekend", "Dates confirmed by the organiser; CTF lineup not yet announced; trainings Oct 18-21"),
 ("M20", "2027-11-18", "2027-11-19", "BSides Ottawa 2027 (CTF)", "conference + CTF", "onsite", "Paid ticket", "expected", "2027-11-01", "optional", "Play the CTF if tickets are available", "2026 was Nov 19-20; tickets sold out fast"),
 ("M21", "2027-11-20", "2027-11-20", "CyberSci Regionals 2027-28", "regional qualifier", "onsite per region", "Student teams; regional winners to Nationals", "expected", "2027-09-06", "yes", "Team registered; qualify for Nationals 2028", "2026 Regionals were Sat Nov 21, 2025 Nov 22; sponsors page for 2027-28 not yet posted"),
 ("M22", "2027-12-01", "2027-12-24", "TryHackMe Advent of Cyber 2027", "beginner daily", "online, free", "Open", "expected", "2027-12-01", "optional", "Finish all days", ""),
 ("M23", "2027-12-10", "2027-12-12", "HTB University CTF 2027 (mid-Dec)", "team CTF", "online, jeopardy", "University teams", "expected", "2027-11-22", "yes", "Team result in the top third; writeups", "2023: Dec 8-10; 2024: Dec 13-15"),
]


def _new(phase, theme, prac, read, bl, ev, gate, lvl, hrs):
    return (phase, theme, prac, read, bl, ev, gate, lvl, hrs)


# Final order: ints index the rows in W above; tuples are extra weeks needed so each event lands in the right week.
ORDER = [
 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
 _new(P7, "DiceCTF quals + picoCTF opens", "Play DiceCTF quals as team practice (Fri-Sun). Start picoCTF as soon as it opens: Web, Crypto, Forensics first, log minutes per flag.", "DiceCTF past writeups", "", "DiceCTF 2027 quals ~Mar 5-7 (expected); picoCTF 2027 ~March (expected)", "DiceCTF: 3+ flags; picoCTF: first 10 challenges logged", "L3", 28),
 14, 15, 16,
 _new(P7, "Pwn medium + reverse medium", "Heap + stack mix, reverse medium sets, angr/z3 where useful. Daily timed 90-minute set.", "how2heap; Reverse Engineering for Beginners", "", "NCL Spring registration closes ~Mar 27 (expected)", "3 medium pwn + 3 medium reverse solved from scratch", "L3", 28),
 17, 20, 18, 21, 19, 22, 23, 24,
 _new(P8, "Nationals prep 2: attack/defend + scenario chains", "Scenario chains (recon -> foothold -> pivot -> loot) and defend drills with the team. Skip if Track B; use the week for Google CTF prep.", "CyberSci past finals writeups", "", "", "Chain drill: foothold to domain admin in the time limit", "L3", 28),
 25, 26,
 _new(P8, "Summer reset", "Rest day, lab day, writeup day. Publish writeups for 3 challenges from the spring.", "", "", "", "3 writeups published", "L2", 20),
 27, 28, 30, 29,
 _new(P8, "Writeups + maintenance", "Writeups from UIUCTF; update notes; light practice.", "", "", "", "UIUCTF writeups published", "L2", 20),
 31, 32, 33, 34, 35, 38, 36, 37, 39,
 _new(P9, "Regionals runbook + NCL practice", "Refresh operations/competition-day-runbook.md for a team; NCL Fall practice game (expected early-mid Oct).", "CyberSci sponsors/regionals info", "", "NCL Fall practice game ~Oct 11-17 (expected)", "Runbook v2 tested in a rehearsal", "L3", 28),
 _new(P9, "NCL individual game prep + Hackfest prep", "Timed sets in NCL categories (crypto, log analysis, network traffic, OSINT, password cracking, scanning, web). Decide Hackfest travel.", "NCL gym", "", "Hackfest trainings Oct 18-21 (confirmed)", "Decision made: Hackfest or NCL individual", "L3", 28),
 40,
 _new(P9, "Debrief + specialty wrap", "Debrief the October event; close the lane checkpoint.", "", "", "", "Lane wrapped with an evidence note", "L3", 28),
 41, 42, 43,
 _new(P9, "Debrief Regionals + Holiday Hack", "Debrief Regionals; start SANS Holiday Hack (usually opens mid-Nov); rest.", "", "", "SANS Holiday Hack 2027 opens ~mid Nov (expected)", "Regionals debrief written", "L2", 20),
 44,
 _new(P9, "HTB University CTF 2027 week", "Team rehearsal Mon-Thu; play Dec 10-12 (expected).", "", "", "HTB University CTF 2027 ~Dec 10-12 (expected)", "MILESTONE: played; writeups within 48 h", "L3", 24),
 _new(P9, "Exam buffer", "Protect exams; maintenance only.", "", "", "School finals (confirm)", "Exams done", "L1", 14),
 45,
]
OVERRIDES = {  # (index in W or text) -> field overrides applied after assembly, keyed by week_start
 "2027-08-30": {"events": ""},      # specialty week: remove the stray CSAW event line
 "2027-09-27": {"events": ""},
 "2027-11-08": {"events": ""},
 "2027-04-05": {"events": "NCL Spring individual game ~Apr 9-11 (expected); team game ~Apr 23-25"},
 "2027-04-19": {"events": "NCL Spring team game ~Apr 23-25 (expected); school finals (confirm)"},
 "2027-05-03": {"events": "Travel + lodging for NorthSec confirmed", "theme": "NorthSec final prep", "practice": "Web medium, OSINT, scripting speed; final team rehearsal Saturday; print/offline everything."},
 "2027-02-22": {"theme": "picoCTF Gym + registration", "events": "picoCTF registration opens ~Feb (expected); LACTF ~Feb (expected)"},
 "2027-01-18": {"events": "NCL Spring registration opens ~Jan 25 (expected)"},
 "2027-03-22": {"theme": "Web + forensics medium + NCL practice", "practice": "Medium web and forensics sets; NCL gym and practice game when open. Register for NCL Spring now if you have not.", "reading": "PortSwigger Web Security Academy; SANS DFIR posters", "gate": "6 medium web/forensics solved in timed sets; NCL registered", "events": "NCL Spring registration closes ~Mar 27 (expected; a late fee applies after)"},
 "2027-03-29": {"events": ""},
 "2027-06-14": {"theme": "Google CTF quals"},
 "2027-11-29": {"theme": "Advent of Cyber starts + team rehearsal"},
}


def assemble():
    rows = []
    for item in ORDER:
        rows.append(list(W[item] if isinstance(item, int) else item))
    return rows


def main():
    old = T / "roadmap.csv"
    v1 = T / "roadmap.v1.csv"
    if old.exists() and not v1.exists():
        shutil.copy(old, v1)
    cols = ["week_start", "week_end", "phase", "theme", "practice", "reading", "backlog_ids", "events", "gate", "level_target", "hours"]
    with old.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        d = START
        rows = assemble()
        for ph, theme, prac, read, bl, ev, gate, lvl, hrs in rows:
            assert d.weekday() == 0
            ov = OVERRIDES.get(d.isoformat(), {})
            theme, prac, ev = ov.get("theme", theme), ov.get("practice", prac), ov.get("events", ev)
            read, gate = ov.get("reading", read), ov.get("gate", gate)
            w.writerow([d.isoformat(), (d + timedelta(days=6)).isoformat(), ph, theme, prac, read, bl, ev, gate, lvl, hrs])
            d += timedelta(days=7)
        assert d - timedelta(days=1) == date(2027, 12, 26), d
        print(f"roadmap.csv: {len(rows)} weeks, {START} -> {d - timedelta(days=1)}, {sum(x[8] for x in rows)} h")
    mc = ["id", "start", "end", "event", "type", "format", "who_can_play", "confidence", "prep_from", "priority", "goal", "notes"]
    with (T / "milestones.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(mc)
        for r in M:
            w.writerow(r)
    print(f"milestones.csv: {len(M)} events")


if __name__ == "__main__":
    main()
