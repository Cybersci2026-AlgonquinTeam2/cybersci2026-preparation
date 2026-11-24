# Roadmap: Nov 2026 to Dec 2027, built around competition milestones

Generated from `roadmap.csv`. Same 4 h/day + commute reading cadence; weekly granularity.

## P5 Debrief + gap closure

### 2026-11-23 → 2026-11-29 · Debrief the qualifier + warm-up · target L2 · 28 h

- **Practice:** Mon: write the run record (what you solved, what stalled, minutes per flag, tools you reached for). Rank weaknesses by category. Redo every failed item. Advent of Cyber opens Dec 1: 30 min a day as a warm-up. Check CyberSci Regionals results.
- **Reading:** Your qualifier notes; Hacker Playbook 3 (web + AD chapters)
- **Backlog pulled in:** W08 W13 W14 W15
- **Events:** CyberSci Regionals results (check email/site); SANS Holiday Hack open Nov 18-Jan 5 (confirmed)
- **Gate:** Run record + top 3 weaknesses ranked; Advent of Cyber days 1-7 done

### 2026-11-30 → 2026-12-06 · Boxes + manual privesc · target L3 · 28 h

- **Practice:** VulnHub + Metasploitable; 2 HTB easy boxes; manual Linux privesc until linpeas is redundant. Use the mangui pages (man nmap, man getcap, man crontab) instead of searching the web.
- **Reading:** HackTricks: Linux + Windows privesc
- **Backlog pulled in:** L05 L06 L07 L13
- **Events:** Advent of Cyber Dec 1-24 (confirmed, free, daily)
- **Gate:** 4 boxes rooted with written methodology

### 2026-12-07 → 2026-12-13 · AD fundamentals + first team CTF · target L3 · 28 h

- **Practice:** GOAD or own Server 2022 lab; BloodHound; Kerberoast; pivoting with chisel/ligolo. Weekend: HTB University CTF (if your team is eligible) or niteCTF; do one, not both.
- **Reading:** The Hacker Recipes AD; ired.team notes
- **Backlog pulled in:** L11 L12 L09
- **Events:** HTB University CTF ~mid Dec (expected; needs academic email + team); niteCTF ~Dec 11-13 (expected)
- **Gate:** Domain admin via 2 paths from a cold start; first team-CTF results written up

### 2026-12-14 → 2026-12-20 · Forensics + blue deepen (exam buffer) · target L3 · 20 h

- **Practice:** HTB Sherlocks; CyberDefenders medium; Sigma/Sysmon/Suricata; 3 one-page IR reports. Confirm your exam dates and cut hours if finals fall here.
- **Reading:** NIST 800-61; SANS DFIR posters; MITRE ATT&CK
- **Backlog pulled in:** F08 F10 F12
- **Events:** Advent of Cyber finishing; school finals (confirm dates)
- **Gate:** 3 IR reports <1 page each

## P6 Deepen

### 2026-12-21 → 2026-12-27 · Break + light maintenance · target L2 · 14 h

- **Practice:** Light CTFs for fun; maintain notes; sleep. ASIS CTF Finals Dec 27-28 is hard: play for an hour if you want, no target.
- **Reading:** Podcasts + books of choice
- **Events:** ASIS CTF Finals Dec 27-28 (confirmed, hard)
- **Gate:** Rested; notes up to date

### 2026-12-28 → 2027-01-03 · Reverse engineering · target L3 · 28 h

- **Practice:** Managed code, packers, anti-debug, angr/z3, malware triage in a VM. Ghidra daily (see man ghidra).
- **Reading:** Reverse Engineering for Beginners; Practical Malware Analysis
- **Backlog pulled in:** R04 R05
- **Events:** SANS Holiday Hack closes Jan 5, winners Jan 20 (confirmed)
- **Gate:** 10 crackmes solved incl. 3 medium

### 2027-01-04 → 2027-01-10 · Binary exploitation · target L3 · 28 h

- **Practice:** ROP Emporium 5-8; format strings; heap basics; pwn.college modules; pwntools scripts.
- **Reading:** Nightmare; Hacking: The Art of Exploitation; how2heap
- **Backlog pulled in:** P03 P04 P05 P06
- **Gate:** A ROP chain + a format-string write from scratch

### 2027-01-11 → 2027-01-17 · Cryptography · target L3 · 28 h

- **Practice:** Finish CryptoHack courses; ECC and lattices intro; padding oracle script; Cryptopals sets 2-3.
- **Reading:** Serious Cryptography; Boneh-Shoup (selected chapters)
- **Backlog pulled in:** C06
- **Gate:** CryptoHack score 60%+ of challenges

### 2027-01-18 → 2027-01-24 · Web expert · target L3 · 28 h

- **Practice:** PortSwigger expert labs; request smuggling; deserialisation; Burp extensions (man burpsuite).
- **Reading:** Web Application Hacker's Handbook (selected)
- **Events:** NCL Spring registration opens ~Jan 25 (expected)
- **Gate:** 20 PortSwigger practitioner + 5 expert labs

### 2027-01-25 → 2027-01-31 · Team formation + recon speed · target L3 · 28 h

- **Practice:** Recruit and test your team: roles per category, shared notes, one comms channel. Recon drill: full enumeration of a box in under 15 min with saved scripts.
- **Reading:** NorthSec rules + past writeups
- **Events:** Insomni'hack Feb 1-5 (onsite Switzerland, skip; watch writeups); LACTF ~Feb (expected)
- **Gate:** Team list agreed (aim for 8 for NorthSec); recon script set in repo

### 2027-02-01 → 2027-02-07 · AD advanced · target L3 · 28 h

- **Practice:** ADCS, delegation, trusts, cross-forest; detection side with Sysmon/ELK.
- **Reading:** ired.team + SpecterOps papers
- **Gate:** Domain compromise through ADCS in a lab, with the detection written

### 2027-02-08 → 2027-02-14 · Cloud + containers · target L2 · 28 h

- **Practice:** Docker escape basics, K8s misconfig lab, AWS/S3 IAM labs (free tier). man docker, man bash.
- **Reading:** OWASP Docker/Kubernetes cheat sheets
- **Gate:** Escape one container lab; one IAM path to admin

## P7 Spring season

### 2027-02-15 → 2027-02-21 · Timed mixed sets + first spring CTF · target L3 · 28 h

- **Practice:** Timed 4-hour sets: 2 web, 2 pwn/rev, 2 crypto, 2 forensics. Play DiceCTF/other spring qualifier as practice.
- **Reading:** Past-year writeups for the CTFs on the calendar
- **Events:** DiceCTF 2027 quals ~early Mar (expected); picoCTF registration opens Feb (expected)
- **Gate:** Timed set: 6/10 solved in 4 h

### 2027-02-22 → 2027-02-28 · picoCTF Gym + registration · target L3 · 28 h

- **Practice:** picoCTF 2027 (expected March, ~10 days, Gym practice before). Aim for a top-tier score as a guaranteed milestone.
- **Reading:** picoGym archive
- **Events:** picoCTF registration opens ~Feb (expected); LACTF ~Feb (expected)
- **Gate:** picoCTF: finish with all Web/Crypto/Forensics solved; log time per flag

### 2027-03-01 → 2027-03-07 · DiceCTF quals + picoCTF opens · target L3 · 28 h

- **Practice:** Play DiceCTF quals as team practice (Fri-Sun). Start picoCTF as soon as it opens: Web, Crypto, Forensics first, log minutes per flag.
- **Reading:** DiceCTF past writeups
- **Events:** DiceCTF 2027 quals ~Mar 5-7 (expected); picoCTF 2027 ~March (expected)
- **Gate:** DiceCTF: 3+ flags; picoCTF: first 10 challenges logged

### 2027-03-08 → 2027-03-14 · Attack/defend · target L3 · 28 h

- **Practice:** Run an attack/defend drill with the team: defend a Juice Shop/DVWA stack, patch, monitor logs, then attack your teammates'.
- **Reading:** SANS blue team material; CCDC study guides
- **Gate:** One full attack/defend session; defence runbook updated

### 2027-03-15 → 2027-03-21 · Medium boxes + registration check · target L3 · 28 h

- **Practice:** Medium HTB boxes. Register NCL Spring (about $45 individual); confirm NorthSec registration process and team tickets.
- **Reading:** HackTricks as reference only
- **Events:** NCL Spring registration closes ~late Mar (expected)
- **Gate:** NCL registered; NorthSec team registered or waitlist status known

### 2027-03-22 → 2027-03-28 · Web + forensics medium + NCL practice · target L3 · 28 h

- **Practice:** Medium web and forensics sets; NCL gym and practice game when open. Register for NCL Spring now if you have not.
- **Reading:** PortSwigger Web Security Academy; SANS DFIR posters
- **Events:** NCL Spring registration closes ~Mar 27 (expected; a late fee applies after)
- **Gate:** 6 medium web/forensics solved in timed sets; NCL registered

### 2027-03-29 → 2027-04-04 · Pwn medium + reverse medium · target L3 · 28 h

- **Practice:** Heap + stack mix, reverse medium sets, angr/z3 where useful. Daily timed 90-minute set.
- **Reading:** how2heap; Reverse Engineering for Beginners
- **Gate:** 3 medium pwn + 3 medium reverse solved from scratch

### 2027-04-05 → 2027-04-11 · NCL Spring individual + reverse medium · target L3 · 28 h

- **Practice:** NCL Spring individual game (3-day window; expected mid April). Reverse medium sets.
- **Reading:** 
- **Events:** NCL Spring individual game ~Apr 9-11 (expected); team game ~Apr 23-25
- **Gate:** NCL individual: top-bracket percentile target (set after the practice game)

### 2027-04-12 → 2027-04-18 · NorthSec rehearsal 1 · target L3 · 28 h

- **Practice:** Full-day team rehearsal on an old NorthSec-style set (tracks: web, hardware/IoT, network, forensics, reverse). Fix roles and notes.
- **Reading:** NorthSec past writeups
- **Gate:** Rehearsal debrief: points/hour per person, 3 fixes

### 2027-04-19 → 2027-04-25 · Exam buffer + NCL team game · target L2 · 20 h

- **Practice:** Keep maintenance only if exams. NCL team game with your team (late April, expected).
- **Reading:** 
- **Events:** NCL Spring team game ~Apr 23-25 (expected); school finals (confirm)
- **Gate:** NCL team game played; exam hours protected

### 2027-04-26 → 2027-05-02 · NorthSec rehearsal 2 + tool freeze · target L3 · 28 h

- **Practice:** Second rehearsal. Freeze tools and notes: offline mirror, cheat sheets, mangui installed in the VM.
- **Reading:** 
- **Events:** NorthSec 2027 CTF May 14-16, Montreal (confirmed; regular + AI experience)
- **Gate:** Tool freeze committed; travel/lodging booked

### 2027-05-03 → 2027-05-09 · NorthSec final prep · target L3 · 28 h

- **Practice:** Web medium, OSINT, scripting speed; final team rehearsal Saturday; print/offline everything.
- **Reading:** 
- **Events:** Travel + lodging for NorthSec confirmed
- **Gate:** Timed OSINT + scripting set: 5/8 in 2 h

### 2027-05-10 → 2027-05-16 · NorthSec taper + play · target L3 · 20 h

- **Practice:** Light review Mon-Wed, rest Thu, then play. NorthSec CTF Fri May 14 to Sun May 16.
- **Reading:** None: sleep
- **Events:** NorthSec CTF May 14-16 (confirmed); NorthSec conference ~May 17-23 (unconfirmed)
- **Gate:** MILESTONE: NorthSec played; post-event debrief written within 48 h

## P8 Nationals + summer peak

### 2027-05-17 → 2027-05-23 · Debrief + DEF CON quals window · target L3 · 28 h

- **Practice:** Debrief NorthSec; fix the 3 weakest categories. DEF CON CTF qualifier is expected in late May: play if time allows.
- **Reading:** NorthSec winners' writeups
- **Events:** DEF CON 35 CTF qualifier ~late May (expected; organiser BBB birds)
- **Gate:** Debrief done; one weakness class closed

### 2027-05-24 → 2027-05-30 · Nationals prep or Plan B · target L3 · 28 h

- **Practice:** If you qualified: CyberSci Nationals prep (attack/defend + scenario chains). If not: pick Google CTF + HTB/Apocalypse as the June targets.
- **Reading:** CyberSci past finals writeups
- **Events:** CyberSci Nationals June 2027 (confirmed month; Ottawa hosted 2026, regional winners only)
- **Gate:** Decision made: Track A (Nationals) or Track B (Google CTF)

### 2027-05-31 → 2027-06-06 · Nationals prep 2: attack/defend + scenario chains · target L3 · 28 h

- **Practice:** Scenario chains (recon -> foothold -> pivot -> loot) and defend drills with the team. Skip if Track B; use the week for Google CTF prep.
- **Reading:** CyberSci past finals writeups
- **Gate:** Chain drill: foothold to domain admin in the time limit

### 2027-06-07 → 2027-06-13 · Nationals window / Plan B · target L3 · 20 h

- **Practice:** Track A: CyberSci Nationals (2026 was Jun 12-15; expect similar). Track B: full Google CTF prep.
- **Reading:** 
- **Events:** CyberSci Nationals ~mid Jun (expected); Google CTF quals ~late Jun (expected)
- **Gate:** MILESTONE: Nationals played, or Google CTF quals played

### 2027-06-14 → 2027-06-20 · Google CTF quals · target L3 · 24 h

- **Practice:** Google CTF quals weekend if not clashing with Nationals; then one rest day, one lab day, one writeup day.
- **Reading:** Last year's Google CTF writeups
- **Events:** Google CTF quals ~Jun 18-20 (expected)
- **Gate:** Writeups published for 3 solved challenges

### 2027-06-21 → 2027-06-27 · Summer reset · target L2 · 20 h

- **Practice:** Rest day, lab day, writeup day. Publish writeups for 3 challenges from the spring.
- **Reading:** 
- **Gate:** 3 writeups published

### 2027-06-28 → 2027-07-04 · Summer build 1: your own lab · target L3 · 28 h

- **Practice:** Build the dojo/lab you want: a home range with AD, web, and a monitored network (see dojo-platform-backlog).
- **Reading:** 
- **Gate:** Lab rebuildable from one command/script

### 2027-07-05 → 2027-07-11 · Summer build 2: tooling + notes · target L3 · 28 h

- **Practice:** Rewrite your notes as a searchable offline wiki; extend mangui guides from your real use; automate recon.
- **Reading:** 
- **Gate:** Recon automation tested on 5 boxes

### 2027-07-12 → 2027-07-18 · Hard targets · target L3 · 28 h

- **Practice:** Pick 3 hard challenges from archives (CTFtime 'hard' tag) and finish them over the week.
- **Reading:** 
- **Gate:** 3 hard challenges solved, writeups published

### 2027-07-19 → 2027-07-25 · UIUCTF + HTB Apocalypse window · target L3 · 28 h

- **Practice:** Play UIUCTF (late July expected); HTB Cyber Apocalypse date unconfirmed (2026 ran Jul 24-29).
- **Reading:** 
- **Events:** UIUCTF ~Jul 24-26 (expected); HTB Cyber Apocalypse (watch)
- **Gate:** UIUCTF: 3+ flags across 2 categories

### 2027-07-26 → 2027-08-01 · Writeups + maintenance · target L2 · 20 h

- **Practice:** Writeups from UIUCTF; update notes; light practice.
- **Reading:** 
- **Gate:** UIUCTF writeups published

### 2027-08-02 → 2027-08-08 · DEF CON week (watch or attend) · target L2 · 16 h

- **Practice:** DEF CON 35 Aug 5-8, Las Vegas (confirmed). Attending is optional and costly; watch talks/CTF writeups either way. Maintain: 2 h/day.
- **Reading:** DEF CON talks, Villages
- **Events:** DEF CON 35 Aug 5-8 (confirmed)
- **Gate:** One technique from a talk reproduced in your lab

## P9 Build + fall season

### 2027-08-09 → 2027-08-15 · Rest + term planning · target L2 · 14 h

- **Practice:** Rest, plan the fall term, register the team for NCL Fall and CyberSci Regionals as soon as they open.
- **Reading:** 
- **Events:** NCL Fall registration opens ~Aug (expected)
- **Gate:** Fall calendar copied into your own calendar

### 2027-08-16 → 2027-08-22 · Cert track or deep specialty (choose one) · target L3 · 28 h

- **Practice:** Choose a lane for the fall: OSCP-style boxes, a blue-team lane (BTL1/CySA), or reverse/pwn depth. Keep CTF practice on weekends.
- **Reading:** Chosen lane's official syllabus
- **Gate:** Lane chosen and week-by-week plan added

### 2027-08-23 → 2027-08-29 · Specialty week 1 · target L3 · 28 h

- **Practice:** Lane work: 3 days lane + 2 days CTF drills + 1 day writeups.
- **Reading:** 
- **Gate:** Lane checkpoint 1 met

### 2027-08-30 → 2027-09-05 · Specialty week 2 · target L3 · 28 h

- **Practice:** Lane work.
- **Reading:** 
- **Gate:** Lane checkpoint 2 met

### 2027-09-06 → 2027-09-12 · Team rebuild for Regionals · target L3 · 28 h

- **Practice:** Rebuild the team for CyberSci 2027-28 Regionals: roles, cheat sheets, runbook (competition-day-runbook.md refresh).
- **Reading:** CyberSci sponsors/regionals info
- **Events:** CyberSci Regionals 2027 ~Nov 20 (expected; register early)
- **Gate:** Team registered; runbook v2 tested

### 2027-09-13 → 2027-09-19 · CSAW quals + speed · target L3 · 28 h

- **Practice:** CSAW CTF quals (48 h, expected mid Sep). Speed drills.
- **Reading:** CSAW past challenges
- **Events:** CSAW quals ~Sep 17-19 (expected)
- **Gate:** CSAW: 5+ challenges solved

### 2027-09-20 → 2027-09-26 · Specialty week 3 · target L3 · 28 h

- **Practice:** Lane work.
- **Reading:** 
- **Gate:** Lane checkpoint 3 met

### 2027-09-27 → 2027-10-03 · Specialty week 4 · target L3 · 28 h

- **Practice:** Lane work.
- **Reading:** 
- **Gate:** Lane checkpoint 4 met

### 2027-10-04 → 2027-10-10 · Regionals runbook + NCL practice · target L3 · 28 h

- **Practice:** Refresh operations/competition-day-runbook.md for a team; NCL Fall practice game (expected early-mid Oct).
- **Reading:** CyberSci sponsors/regionals info
- **Events:** NCL Fall practice game ~Oct 11-17 (expected)
- **Gate:** Runbook v2 tested in a rehearsal

### 2027-10-11 → 2027-10-17 · NCL individual game prep + Hackfest prep · target L3 · 28 h

- **Practice:** Timed sets in NCL categories (crypto, log analysis, network traffic, OSINT, password cracking, scanning, web). Decide Hackfest travel.
- **Reading:** NCL gym
- **Events:** Hackfest trainings Oct 18-21 (confirmed)
- **Gate:** Decision made: Hackfest or NCL individual

### 2027-10-18 → 2027-10-24 · Hackfest CTF + NCL individual · target L3 · 28 h

- **Practice:** Hackfest Quebec City Oct 21-23 (confirmed; CTF details unannounced; tickets sold separately) clashes with the NCL individual game: pick Hackfest if you travel, NCL if not.
- **Reading:** 
- **Events:** Hackfest Oct 21-23 (confirmed); NCL Fall individual ~Oct 22-24 (expected)
- **Gate:** MILESTONE: one of the two played; writeups within 48 h

### 2027-10-25 → 2027-10-31 · Debrief + specialty wrap · target L3 · 28 h

- **Practice:** Debrief the October event; close the lane checkpoint.
- **Reading:** 
- **Gate:** Lane wrapped with an evidence note

### 2027-11-01 → 2027-11-07 · NCL team + CSAW finals window · target L3 · 28 h

- **Practice:** NCL Fall team game (expected early Nov). CSAW finals (invite only; expected Nov).
- **Reading:** 
- **Events:** NCL Fall team game ~Nov 5-7 (expected)
- **Gate:** NCL team game played; debrief written

### 2027-11-08 → 2027-11-14 · Regionals sprint · target L3 · 28 h

- **Practice:** Full-day rehearsals; timed mixed sets; rest the day before.
- **Reading:** 
- **Gate:** Rehearsal: 8/12 in the Regionals time limit

### 2027-11-15 → 2027-11-21 · CyberSci Regionals + BSides Ottawa · target L3 · 24 h

- **Practice:** BSides Ottawa ~Nov 18-19 (expected, has a CTF); CyberSci Regionals ~Sat Nov 20 (expected).
- **Reading:** None: sleep
- **Events:** CyberSci Regionals ~Nov 20 (expected); BSides Ottawa ~Nov 18-19 (expected)
- **Gate:** MILESTONE: Regionals played; qualified for Nationals 2028?

### 2027-11-22 → 2027-11-28 · Debrief Regionals + Holiday Hack · target L2 · 20 h

- **Practice:** Debrief Regionals; start SANS Holiday Hack (usually opens mid-Nov); rest.
- **Reading:** 
- **Events:** SANS Holiday Hack 2027 opens ~mid Nov (expected)
- **Gate:** Regionals debrief written

### 2027-11-29 → 2027-12-05 · Advent of Cyber starts + team rehearsal · target L3 · 28 h

- **Practice:** Advent of Cyber 2027 Dec 1+ (expected); HTB University CTF mid-Dec (expected).
- **Reading:** 
- **Events:** Advent of Cyber 2027 ~Dec 1 (expected); HTB University CTF 2027 ~mid Dec (expected)
- **Gate:** HTB University CTF played with the team

### 2027-12-06 → 2027-12-12 · HTB University CTF 2027 week · target L3 · 24 h

- **Practice:** Team rehearsal Mon-Thu; play Dec 10-12 (expected).
- **Reading:** 
- **Events:** HTB University CTF 2027 ~Dec 10-12 (expected)
- **Gate:** MILESTONE: played; writeups within 48 h

### 2027-12-13 → 2027-12-19 · Exam buffer · target L1 · 14 h

- **Practice:** Protect exams; maintenance only.
- **Reading:** 
- **Events:** School finals (confirm)
- **Gate:** Exams done

### 2027-12-20 → 2027-12-26 · Year review · target L2 · 14 h

- **Practice:** Write the 12-month review: milestones hit/missed, points per hour, skills ladder; plan 2028.
- **Reading:** Your own run records
- **Events:** ASIS CTF Finals ~late Dec (expected)
- **Gate:** Year review + 2028 roadmap draft
