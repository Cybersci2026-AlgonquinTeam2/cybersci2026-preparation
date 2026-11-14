# VulnHub, Parrot CTFs and Cybrary: platform guide

Status: written 2026-11-14 from search results and general knowledge. **Access, prices and free tiers change; verify on each site.** Names marked S below were named in sources I read today; names marked M are recalled from memory and need checking on vulnhub.com. Nothing here was played by the assistant. No solutions are included, only method.

## Part 1: VulnHub

### What it is

**Layman:** a library of deliberately broken computers that you download and attack on your own laptop. Nothing is online; you run each machine inside a virtual machine, so it is safe and legal.

**Technical:** each entry is a VM image (OVA/VMDK, sometimes inside a zip or rar). You import it into VMware or VirtualBox, put it on a **host-only network** (never bridged to your home or school network), find its IP, then enumerate and attack it from Kali. VulnHub says it cannot vet what the community uploads, so treat every image as hostile software.

### Safe setup (do this once)

1. Create a host-only network in VMware (VMnet1 or a new one) with DHCP enabled. 2. Attach Kali and the target to it; give the target no other adapter. 3. Snapshot Kali clean. 4. Take a snapshot of each target before you start so you can reset. 5. Find the target: `nmap -sn 192.168.X.0/24` or `arp-scan -l`. 6. Never leave a vulnerable VM running on a shared network.

### Your loop for every machine

1. **Plan (5 min):** write the target IP and your first three questions (what ports, what web app, what versions). 2. **Enumerate (30 min):** `nmap -p- -T4`, then `-sV -sC`; browse every web port; enumerate shares. 3. **Foothold:** match a service version or web bug to a weakness. 4. **Escalate:** `sudo -l`, SUID files, cron, kernel version. 5. **Write the runbook:** commands that worked, in order. 6. **Read one public walkthrough only after you have a runbook** and compare. 7. **Attempt 2:** redo it a week later from your runbook in half the time.

### The curated list

Tiers: **start** = begin here; **next** = after the start set; **later** = after CyberSci. Difficulty is approximate.

| Machine | Series | Difficulty | Skills | Src | Tier |
|---|---|---|---|---|---|
| Kioptrix: Level 1 | Kioptrix series | Easy | Nmap, web and Samba enumeration, searching public exploits | S | start |
| DC-1 | DC series | Easy | CMS enumeration, SUID privilege escalation | S | start |
| Basic Pentesting: 1 | Basic Pentesting | Easy | Service enumeration, credential guessing, privilege escalation | S | start |
| Mr-Robot: 1 | TV-themed | Easy | Web enumeration, hashes, SUID escalation | S | start |
| The Planets: Earth | Planets series | Easy | Web enumeration, decoding, simple escalation | S | start |
| DC-2 | DC series | Easy | WordPress enumeration, restricted shells | S | start |
| Lampiao | Single VM | Easy | Web CMS vulnerability, kernel exploit escalation | S | start |
| Kioptrix: Level 1.1 | Kioptrix series | Easy | Web SQL injection, local escalation | M | start |
| Stapler: 1 | Single VM | Easy-Medium | Many services, enumeration discipline | M | next |
| SickOs 1.2 | SickOs | Easy-Medium | Web methods, cron-based escalation | M | next |
| Brainpan: 1 | Single VM | Medium | Buffer overflow on a Windows-style service (beginner binary exploitation) | M | next |
| PwnLab: init | Single VM | Medium | LFI, file upload, local escalation | M | next |
| FristiLeaks: 1.3 | Single VM | Easy-Medium | Web enumeration, upload bypass, local escalation | M | next |
| Zico2 | Single VM | Medium | File inclusion, web app credentials | M | next |
| Droopy | Single VM | Medium | CMS exploitation and escalation | M | next |
| DerpNStink | Single VM | Medium | WordPress, credentials, packet capture | M | next |
| Symfonos: 1 | Symfonos series | Medium | SMB enumeration, mail, LFI | M | later |
| Billu: b0x | Single VM | Medium | File inclusion and SQL, kernel escalation | M | later |
| Vulnix | Single VM | Medium | NFS misconfiguration, escalation | M | later |
| Tr0ll: 1 | Tr0ll | Easy-Medium | Packet analysis, brute force, escalation | M | later |

Search each name on vulnhub.com; download sizes range from about 190 MB (Kioptrix Level 1) to over 2 GB (Basic Pentesting 1). Some are archives that must be extracted first. Newer VMs are built for x86; on your Windows machine with VMware that is fine.

### How VulnHub maps to CyberSci

| CyberSci skill | VulnHub practice |
|---|---|
| Networking and Nmap | Every machine starts with a scan and service enumeration |
| Web exploits | DC-1, DC-2, Mr-Robot, PwnLab, Kioptrix 1.1 |
| Beginner binary exploitation | Brainpan 1 |
| Hacker tools / reverse shells | Most machines end in a shell; practise in the lab only |
| Privilege escalation | Every machine, and it is the part CyberSci rarely asks for in Regionals |

CyberSci Regionals are jeopardy-style, so single-machine pentests are not the main format; use VulnHub as depth practice after the P1 items, not instead of them.

## Part 2: Parrot CTFs

**What it is (from what I could verify):** a commercial CTF/lab platform (parrot-ctfs.com) that describes itself as ethical-hacking labs and training, with an academy (academy.parrot-ctfs.com), a free **Release Arena** and a separate free **Micro Labs** project of isolated vulnerable web apps (github.com/Parrot-CTFs). Reports disagree on what is free versus paid (a 2024 comment mentioned a VIP price; newer posts mention labs free for a limited time). **Check the site and your account before planning around it.**

**How to use it:**

1. Create an account (use a throwaway email if you prefer) and list what is free today. 2. Start with Release Arena labs and any web-exploitation labs: they map to the web and SQL skills. 3. Use Micro Labs to practise one vulnerability class at a time. 4. Record each lab in the activity tracker (`python scripts/activity.py log ...`) with the time and a one-line lesson. 5. Skip anything that needs payment; there is enough free material elsewhere.

**Not verified:** exact challenge names, difficulty and which items are free.

## Part 3: Cybrary

**What it is:** a video-course platform. Its own pages say a free plan exists, but older and newer sources disagree on how much of the catalogue is free (anything from roughly 50 courses to the whole 1,200+ course and lab catalogue), so verify on cybrary.it before planning. Courses named in third-party lists as free include *Penetration Testing and Ethical Hacking* and *Advanced Penetration Testing*; availability may differ.

**Why it fits your commute:** video and audio lessons are good for the bus when you cannot type. They do not replace doing the exercises.

**A sane way to use it:**

1. Pick two courses that match a weak CyberSci category (networking, web, forensics). 2. Watch at 1.25x, one module per commute. 3. After each module write three lines: what it taught, one command, one thing you did not understand. 4. Within 24 hours do one hands-on item for that topic (a TryHackMe room, a picoCTF challenge, a lab from this pack). 5. Do not collect certificates for their own sake.

**Offline note:** Cybrary lessons need the app or site; download features, if any, depend on your plan. Do not rely on streaming at the competition: AI tools are not allowed, and you should not assume internet either.

## Part 4: Where all of this fits

For the CyberSci qualifiers on Nov 21, finish the P1 TryHackMe rooms and the picoGym Easy sets first. VulnHub, Parrot CTFs and Cybrary are for **after** the qualifiers or for days you have spare time. The tracker rows for them are P2 for that reason.

## Flashcard prompts

- Why use a host-only network for vulnerable VMs?
- What do you do first after a VulnHub VM boots?
- Why write a runbook before reading a walkthrough?
- Which three commands start Linux privilege escalation checks?
- Why snapshot a VM before attacking it?
