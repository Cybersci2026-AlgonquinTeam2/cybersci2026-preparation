# Sources catalogue

URLs are given where I'm confident of them; for anything else search the name. Verify availability, since platforms change (VulnHub in particular has had outages). Prefer free resources first.

## Official CyberSci
- Site: https://cybersci.ca/ (also cybersecuritychallenge.ca)
- Students/rules/prep: https://cybersci.ca/students/
- Past events: https://cybersecuritychallenge.ca/en/past-events/
- CTFtime qualifier page: https://ctftime.org/event/3436
- CTFtime past CyberSci events: https://ctftime.org/ctf/643/

## Event calendars
- CTFtime upcoming: https://ctftime.org/event/list/upcoming
- CTFtime writeups: https://ctftime.org/writeups
- ctfhelper calendar: https://ctfhelper.com/calendar
- Tech Learning Collective CTF list: https://techlearningcollective.com/events/ctfs.html

## Rehearsal events (see `events.yaml`)
FortID (3440), DEADFACE (3279), Hack.lu (3207), HITCON (3340), CSCTF (3333), PINK+ (3331), HKCERT Quals (3418), Platypwn (3082), WolvCTF (3049), InIt CTF (3467); CTFtime URL pattern `https://ctftime.org/event/<id>`.

## Beginner-to-intermediate wargames and labs

| Name | URL / pointer | Best for |
|---|---|---|
| OverTheWire | https://overthewire.org/wargames/ | Bandit (Linux), Natas (web), Leviathan, Krypton, Narnia (pwn), Behemoth, Utumno |
| OWASP Juice Shop | https://owasp.org/www-project-juice-shop/ ; `docker run -p 3000:3000 bkimminich/juice-shop` ; free book "Pwning OWASP Juice Shop" | Modern web app, all OWASP Top 10, scoreboard |
| OWASP WebGoat | https://owasp.org/www-project-webgoat/ | Guided lessons |
| DVWA | https://github.com/digininja/DVWA | Classic web vulns |
| bWAPP | http://www.itsecgames.com/ | 100+ web bugs |
| PortSwigger Web Security Academy | https://portswigger.net/web-security | Best free web curriculum + labs |
| picoCTF / picoGym | https://picoctf.org/ | All categories, graded |
| TryHackMe | https://tryhackme.com/ | Guided paths: Pre-Security, Jr Pentester, SOC Level 1 |
| Hack The Box (Academy, Machines, Sherlocks, CTF) | https://www.hackthebox.com/ | Boxes, DFIR scenarios, modules |
| Root-Me | https://www.root-me.org/ | 400+ challenges, all categories |
| Hackropole (ANSSI) | https://hackropole.fr/ | Archived FCSC challenges, self-hostable |
| VulnHub | https://www.vulnhub.com/ | Offline vulnerable VMs: Kioptrix, Basic Pentesting, Mr-Robot, DC series |
| Metasploitable 2/3 | Rapid7 / GitHub | Intentionally vulnerable Linux/Windows |
| crAPI | https://github.com/OWASP/crAPI | API testing |
| Damn Vulnerable GraphQL Application | https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application | GraphQL |
| GOAD | https://github.com/Orange-Cyberdefense/GOAD | AD lab (heavy; consider if resources allow) |
| Proving Grounds Practice | OffSec | Paid; optional |

## Category specialists

| Category | Resources |
|---|---|
| Pwn / RE | pwn.college https://pwn.college/ ; ROP Emporium https://ropemporium.com/ ; Nightmare https://guyinatuxedo.github.io/ ; crackmes.one https://crackmes.one/ ; how2heap (GitHub) ; Reverse Engineering for Beginners (free book, Dennis Yurichev) ; Ghidra docs |
| Crypto | CryptoHack https://cryptohack.org/ ; Cryptopals https://cryptopals.com/ ; Crypton (GitHub, reference) |
| Forensics / DFIR | Malware-Traffic-Analysis.net https://www.malware-traffic-analysis.net/ ; CyberDefenders https://cyberdefenders.org/ ; Blue Team Labs Online https://blueteamlabs.online/ ; LetsDefend https://letsdefend.io/ ; 13Cubed (YouTube) ; SANS posters ; DFIR Diva |
| Malware | MalwareBazaar https://bazaar.abuse.ch/ (samples; analyze only in an isolated VM) ; Practical Malware Analysis labs ; any.run (free tier) |
| OSINT | Sourcing.games ; Trace Labs ; GeoGuessr ; OSINT Framework https://osintframework.com/ ; IntelTechniques |
| Detection engineering | SigmaHQ (GitHub) ; Sysmon-modular ; Chainsaw / Hayabusa |

## Archives to mine for practice (solved-by-others, with writeups)
- picoCTF past years (picoGym)
- Google CTF, DEF CON CTF Quals, CSAW, HITCON, PlaidCTF, DiceCTF, UIUCTF, BuckeyeCTF, LA CTF, ångstromCTF, Cyber Apocalypse (HTB)
- CTFtime writeups indexed by event/category
- GitHub: `ctfs/`, `awesome-ctf`, per-team writeup repos
- Past CyberSci regionals and nationals (ctftime events 2511, 2689, 2909, 3125) and team writeups, if published

## Cheat sheets and references
- HackTricks https://book.hacktricks.xyz/
- PayloadsAllTheThings https://github.com/swisskyrepo/PayloadsAllTheThings
- GTFOBins https://gtfobins.github.io/ ; LOLBAS https://lolbas-project.github.io/
- RevShells https://www.revshells.com/
- CyberChef https://gchq.github.io/CyberChef/
- SecLists (wordlists) https://github.com/danielmiessler/SecLists
- Wireshark display filter reference ; Nmap reference guide
- MITRE ATT&CK https://attack.mitre.org/

## Books
- The Hacker Playbook 3 (official CyberSci recommendation)
- Hacking: The Art of Exploitation
- The Web Application Hacker's Handbook (2nd ed.)
- Black Hat Python
- Practical Malware Analysis
- Serious Cryptography
- The Art of Memory Forensics

## YouTube and video
- IppSec (HTB walkthroughs, with searchable index at ippsec.rocks)
- LiveOverflow (binary exploitation, web)
- John Hammond (CTF walkthroughs, malware)
- The Cyber Mentor / TCM Security
- NahamSec (bug bounty, recon)
- 13Cubed (forensics)
- Gynvael Coldwind (CTF livestreams)
- stacksmashing (reverse engineering)

## Offline pack for competition day
Subject to current organizer rules, download, hash, and store on the laptop and a USB drive: HackTricks mirror, PayloadsAllTheThings, GTFOBins/LOLBAS, SecLists, RsaCtfTool, CyberChef (offline HTML), tool installers (Ghidra, Wireshark, Burp Community), your permitted writeups and per-category cheat sheets. Record the SHA-256 of each in `operations/competition-day-runbook.md`.

Ollama model files, embedding models and AI retrieval/RAG indexes are study-time resources only. Do not include them in the competition environment: the repository records an organizer reply prohibiting AI tools. See the [competition-day runbook](../operations/competition-day-runbook.md).

## Tools to have installed and tested
Kali (or equivalent) VM, Burp Community, ffuf, gobuster, sqlmap, nmap, netcat, socat, Wireshark/tshark, NetworkMiner, Volatility 3, Autopsy, binwalk, exiftool, steghide/zsteg, Ghidra, pwntools, pwndbg/GEF, ROPgadget, one_gadget, angr/z3, hashcat, john, hydra, impacket, BloodHound, NetExec, chisel/ligolo-ng, linpeas/winpeas, CyberChef, Python venv with requests/pycryptodome/sympy/pwntools, Docker.
