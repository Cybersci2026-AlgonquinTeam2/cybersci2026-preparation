# TryHackMe: the free-room guide (full depth)

Status: written from TryHackMe's own list of free rooms (their blog page 'free TryHackMe training to learn cyber security in 2026', read 2026-11-14), the room titles, and general knowledge of each topic. **Room contents change and the rooms were not played by the assistant**, so treat every description as a guide, not a transcript. This book gives you hints and a method, not room answers: TryHackMe asks learners to earn their own answers, and the point is to learn.

Pricing and access change (free tier limits, Premium, MAX). Check tryhackme.com/pricing; the AttackBox time limit on the free tier can cap your day.

**Scope:** 117 rooms listed as free by TryHackMe; **22 P1** (do for CyberSci Regionals), 60 P2 (useful), 35 P3 (later or beyond Regionals). Manifest: `curriculum/tryhackme/manifest.csv`.

## How to work a room (the loop)

1. **Read** the room description and tasks once (5 min). 2. **Attempt:** do the task yourself; answer from what you see. 3. **Hint ladder:** use the three rungs below in order. 4. **Review:** write two lines: what the room taught, and which tool/flag mattered. 5. **Reinforce:** read the linked book section. 6. **Attempt 2:** next day, no room text, same objective.

## Time plan (P1 only)

The P1 set totals about **22 hours**. Do them in the order below; it follows the CyberSci skills list.

| # | Room | Category | Min |
|---|---|---|---:|
| 1 | [Passive Recon](https://tryhackme.com/room/passiverecon) | Networking and Nmap | 45 |
| 2 | [Active Recon](https://tryhackme.com/room/activerecon) | Networking and Nmap | 60 |
| 3 | [Nmap](https://tryhackme.com/room/nmap02) | Networking and Nmap | 60 |
| 4 | [Further Nmap](https://tryhackme.com/room/furthernmap) | Networking and Nmap | 60 |
| 5 | [Network Services](https://tryhackme.com/room/networkservices) | Networking and Nmap | 75 |
| 6 | [HTTP in Detail](https://tryhackme.com/room/httpindetail) | Web exploits and SQL | 45 |
| 7 | [Intro to Web Application Security](https://tryhackme.com/room/introwebapplicationsecurity) | Application vulnerability analysis | 45 |
| 8 | [Vulnerabilities 101](https://tryhackme.com/room/vulnerabilities101) | Application vulnerability analysis | 30 |
| 9 | [Burp Suite: Repeater](https://tryhackme.com/room/burpsuiterepeater) | Web exploits and SQL | 45 |
| 10 | [ffuf](https://tryhackme.com/room/ffuf) | Web exploits and SQL | 45 |
| 11 | [Juicy Details](https://tryhackme.com/room/juicydetails) | Web exploits and SQL | 90 |
| 12 | [Pickle Rick](https://tryhackme.com/room/picklerick) | Web exploits and SQL | 60 |
| 13 | [Basic Pentesting](https://tryhackme.com/room/basicpentestingjt) | Web exploits and SQL | 120 |
| 14 | [Python Basics](https://tryhackme.com/room/pythonbasics) | Basic programming | 60 |
| 15 | [CyberChef: The Basics](https://tryhackme.com/room/cyberchefbasics) | Crypto and encodings | 45 |
| 16 | [CTF Collection Vol. 1](https://tryhackme.com/room/ctfcollectionvol1) | CTF warm-up (crypto, encodings, stego) | 90 |
| 17 | [c4ptur3th3fl4g](https://tryhackme.com/room/c4ptur3th3fl4g) | Forensics and memory forensics | 60 |
| 18 | [Crack the Hash](https://tryhackme.com/room/crackthehash) | Crypto (hashes) | 60 |
| 19 | [Hydra](https://tryhackme.com/room/hydra) | Hacker tools | 45 |
| 20 | [h4cked](https://tryhackme.com/room/h4cked) | Forensics and memory forensics | 60 |
| 21 | [Memory Analysis Introduction](https://tryhackme.com/room/memoryanalysisintroduction) | Forensics and memory forensics | 45 |
| 22 | [Memory Forensics](https://tryhackme.com/room/memoryforensics) | Forensics and memory forensics | 75 |

## P1 rooms in depth

### Passive Recon
- Link: https://tryhackme.com/room/passiverecon   - Category: Networking and Nmap   - About 45 min
- **What it teaches:** Gathering information without touching the target (whois, DNS, search).
- **Why it matters for CyberSci:** Feeds both OSINT and network tasks.
- **Hint ladder (no answers):**
  1. Use whois, nslookup/dig and search engines on a domain you own.
  2. Record what each source tells you.
  3. Note what could be sensitive.
- **Attempt 2:** Do a passive recon of a fictional company in a CTF.

### Active Recon
- Link: https://tryhackme.com/room/activerecon   - Category: Networking and Nmap   - About 60 min
- **What it teaches:** Using ping, traceroute, telnet and netcat/browser tools to probe a target directly.
- **Why it matters for CyberSci:** First step of every network task; teaches what each tool proves.
- **Hint ladder (no answers):**
  1. Before each question, decide which tool answers it (reachability, path, service banner).
  2. Run the tool yourself in the AttackBox and read the raw output, not just the summary.
  3. For banners, connect with a raw TCP client and send a minimal request.
- **Attempt 2:** Redo it using only `nc` and `curl`, no browser.

### Nmap
- Link: https://tryhackme.com/room/nmap02   - Category: Networking and Nmap   - About 60 min
- **What it teaches:** Scan types, port states, timing and output formats in Nmap.
- **Why it matters for CyberSci:** The organizers' list names Nmap first; this is the core tool.
- **Hint ladder (no answers):**
  1. Run the default scan first, then change one flag at a time and compare.
  2. For questions about scan behaviour, scan a lab host while watching packets (Wireshark) to see what each flag sends.
  3. Save every scan with `-oA` and read the saved files.
- **Attempt 2:** Do the whole room again from your own notes without opening the lesson text.

### Further Nmap
- Link: https://tryhackme.com/room/furthernmap   - Category: Networking and Nmap   - About 60 min
- **What it teaches:** Scripts (NSE), firewall evasion options, OS and version detection.
- **Why it matters for CyberSci:** Separates 'open port' from 'what is running and what is wrong with it'.
- **Hint ladder (no answers):**
  1. Read `nmap --script-help` for a script before you run it.
  2. Use `-sV -sC -p-` combos and note which output came from which flag.
  3. For evasion questions, remember what a firewall sees, then match the option to that.
- **Attempt 2:** Scan one of your own lab VMs and write a one-page report from the output.

### Network Services
- Link: https://tryhackme.com/room/networkservices   - Category: Networking and Nmap   - About 75 min
- **What it teaches:** Enumerating and interacting with SMB, Telnet and FTP.
- **Why it matters for CyberSci:** Common services on CTF machines; enumeration is the first attack step.
- **Hint ladder (no answers):**
  1. Enumerate before you attack: list shares/users/anonymous access.
  2. Try the service client by hand (smbclient, ftp, telnet) before reaching for a framework.
  3. Note credentials you find and try them on the other services.
- **Attempt 2:** Repeat against a local lab VM (Samba/FTP) you set up yourself.

### HTTP in Detail
- Link: https://tryhackme.com/room/httpindetail   - Category: Web exploits and SQL   - About 45 min
- **What it teaches:** HTTP requests, responses, methods, status codes and headers.
- **Why it matters for CyberSci:** You cannot attack the web without reading raw HTTP.
- **Hint ladder (no answers):**
  1. Use `curl -v` to view a full exchange.
  2. Change the method and see how responses differ.
  3. Learn the status code families by heart.
- **Attempt 2:** Send three different requests by hand with `nc`.

### Intro to Web Application Security
- Link: https://tryhackme.com/room/introwebapplicationsecurity   - Category: Application vulnerability analysis   - About 45 min
- **What it teaches:** How web apps work and where they break.
- **Why it matters for CyberSci:** Vocabulary for every web challenge.
- **Hint ladder (no answers):**
  1. Draw the request/response flow yourself.
  2. List the inputs an attacker controls.
  3. Match each input to a bug class.
- **Attempt 2:** Explain the OWASP top categories without notes.

### Vulnerabilities 101
- Link: https://tryhackme.com/room/vulnerabilities101   - Category: Application vulnerability analysis   - About 30 min
- **What it teaches:** Basics of vulnerabilities, CVEs and scoring.
- **Why it matters for CyberSci:** Needed for application vulnerability analysis and security news.
- **Hint ladder (no answers):**
  1. Learn the difference between a vulnerability and an exploit.
  2. Look up one real CVE and read its entry.
  3. Practise reading a CVSS vector.
- **Attempt 2:** Pick a recent CVE from the news and summarise it in 3 lines.

### Burp Suite: Repeater
- Link: https://tryhackme.com/room/burpsuiterepeater   - Category: Web exploits and SQL   - About 45 min
- **What it teaches:** Intercepting, editing and resending requests.
- **Why it matters for CyberSci:** Web challenges are mostly about changing requests and watching responses.
- **Hint ladder (no answers):**
  1. Capture a normal request first, then change one parameter at a time.
  2. Compare responses side by side.
  3. Keep a note of which change produced which behaviour.
- **Attempt 2:** Replicate a Natas level using only Repeater.

### ffuf
- Link: https://tryhackme.com/room/ffuf   - Category: Web exploits and SQL   - About 45 min
- **What it teaches:** Fuzzing web paths, parameters and virtual hosts.
- **Why it matters for CyberSci:** Finding hidden endpoints is step one of most web challenges.
- **Hint ladder (no answers):**
  1. Start with a small wordlist and filter by response size or status to cut noise.
  2. Fuzz one position at a time.
  3. Check what makes a hit different (status, size, words).
- **Attempt 2:** Use it on a Juice Shop container you run locally.

### Juicy Details
- Link: https://tryhackme.com/room/juicydetails   - Category: Web exploits and SQL   - About 90 min
- **What it teaches:** Exploring a deliberately vulnerable web shop (OWASP Juice Shop).
- **Why it matters for CyberSci:** Hands-on practice with injection, access control and info leaks.
- **Hint ladder (no answers):**
  1. Browse as a normal user first and note every input.
  2. Use the browser dev tools Network tab to see requests.
  3. Come back to harder items after you finish the easy ones.
- **Attempt 2:** Run Juice Shop locally and solve 5 challenges without the room.

### Pickle Rick
- Link: https://tryhackme.com/room/picklerick   - Category: Web exploits and SQL   - About 60 min
- **What it teaches:** A beginner box chain: enumerate, find a login, get a shell, escalate.
- **Why it matters for CyberSci:** Teaches the full enumerate-exploit-escalate loop.
- **Hint ladder (no answers):**
  1. Enumerate the web service for hidden files before guessing logins.
  2. Read page source and robots.txt.
  3. Once you have command execution, look at what you can run with sudo.
- **Attempt 2:** Do it again and write the exact commands as a runbook.

### Basic Pentesting
- Link: https://tryhackme.com/room/basicpentestingjt   - Category: Web exploits and SQL   - About 120 min
- **What it teaches:** A longer beginner box: service enumeration, credential guessing, privilege escalation.
- **Why it matters for CyberSci:** Integrates Nmap, enumeration and escalation in one run.
- **Hint ladder (no answers):**
  1. Write the open-ports table first.
  2. For each service, list one thing to check.
  3. When stuck, enumerate again from a different angle (users, shares, versions).
- **Attempt 2:** Repeat in 60 minutes with only your notes.

### Python Basics
- Link: https://tryhackme.com/room/pythonbasics   - Category: Basic programming   - About 60 min
- **What it teaches:** Variables, loops, functions and files in Python.
- **Why it matters for CyberSci:** The CyberSci list includes basic programming; solvers are small Python scripts.
- **Hint ladder (no answers):**
  1. Type every example yourself instead of copying.
  2. After each section, write a 5-line script that uses it on a made-up file.
  3. Print intermediate values to see what your code does.
- **Attempt 2:** Write a script that reads a file and prints lines containing a word.

### CyberChef: The Basics
- Link: https://tryhackme.com/room/cyberchefbasics   - Category: Crypto and encodings   - About 45 min
- **What it teaches:** Chaining decoding and encoding operations in CyberChef.
- **Why it matters for CyberSci:** Fast triage of encodings in crypto and forensics challenges.
- **Hint ladder (no answers):**
  1. Identify the encoding first (look at the alphabet and length), then pick one operation.
  2. Chain operations in the order they were applied, reversed.
  3. Use the Magic operation as a hint, not an answer.
- **Attempt 2:** Take three encoded strings of your own and decode them without Magic.

### CTF Collection Vol. 1
- Link: https://tryhackme.com/room/ctfcollectionvol1   - Category: CTF warm-up (crypto, encodings, stego)   - About 90 min
- **What it teaches:** A grab-bag of beginner CTF puzzles: encodings, steganography, hashes.
- **Why it matters for CyberSci:** Exactly the warm-up category in CyberSci.
- **Hint ladder (no answers):**
  1. Look for the encoding clue in the challenge text.
  2. Try quick tools first (CyberChef, `strings`, `exiftool`, `binwalk`).
  3. Timebox each puzzle to 15 minutes, then take one hint.
- **Attempt 2:** Time yourself on the ones you finished and aim to halve it.

### c4ptur3th3fl4g
- Link: https://tryhackme.com/room/c4ptur3th3fl4g   - Category: Forensics and memory forensics   - About 60 min
- **What it teaches:** A CTF warm-up on encodings and simple steganography.
- **Why it matters for CyberSci:** Quick wins that teach decoding and tool use.
- **Hint ladder (no answers):**
  1. Identify the encoding by its alphabet.
  2. Try the simple tools before exotic ones.
  3. Look for hidden data in files with `strings` and `binwalk`.
- **Attempt 2:** Solve it again in half the time.

### Crack the Hash
- Link: https://tryhackme.com/room/crackthehash   - Category: Crypto (hashes)   - About 60 min
- **What it teaches:** Identifying hash types and cracking them with wordlists.
- **Why it matters for CyberSci:** Hashes appear in crypto and forensics challenges.
- **Hint ladder (no answers):**
  1. Identify the hash type from length and format.
  2. Pick the right hashcat mode or John format.
  3. Try a wordlist before a brute force.
- **Attempt 2:** Hash your own passwords with different algorithms and crack them.

### Hydra
- Link: https://tryhackme.com/room/hydra   - Category: Hacker tools   - About 45 min
- **What it teaches:** Online password guessing with Hydra.
- **Why it matters for CyberSci:** Teaches why rate limiting and lockouts matter.
- **Hint ladder (no answers):**
  1. Start with a tiny wordlist against a lab service.
  2. Read the module syntax for the service.
  3. Note the speed and what a lockout looks like.
- **Attempt 2:** Write down how you would defend against what you just did.

### h4cked
- Link: https://tryhackme.com/room/h4cked   - Category: Forensics and memory forensics   - About 60 min
- **What it teaches:** Investigating a packet capture of an intrusion.
- **Why it matters for CyberSci:** Packet analysis is core CyberSci forensics.
- **Hint ladder (no answers):**
  1. Open Statistics > Conversations to see who talked to whom.
  2. Follow TCP streams for readable sessions.
  3. Build a timeline of what the attacker did.
- **Attempt 2:** Write a 5-line incident summary from the capture.

### Memory Analysis Introduction
- Link: https://tryhackme.com/room/memoryanalysisintroduction   - Category: Forensics and memory forensics   - About 45 min
- **What it teaches:** What memory is and what you can learn from it.
- **Why it matters for CyberSci:** Memory forensics is on the organizers' list.
- **Hint ladder (no answers):**
  1. Read the concept sections before touching the tool.
  2. Write in your own words what each plugin shows.
  3. Link each concept to a question it can answer.
- **Attempt 2:** Explain pslist vs psscan to a friend in 60 seconds.

### Memory Forensics
- Link: https://tryhackme.com/room/memoryforensics   - Category: Forensics and memory forensics   - About 75 min
- **What it teaches:** Applying Volatility to a memory image.
- **Why it matters for CyberSci:** Direct practice for the memory forensics question type.
- **Hint ladder (no answers):**
  1. Run the triage sequence from the memory forensics book: info, pstree, cmdline, netscan, malfind.
  2. Write a one-line finding after each command.
  3. Use strings with the UTF-16 option when plugins fail.
- **Attempt 2:** Make your own image from a VM and answer five questions you invented.

## Atlas: every other free room

P2 = useful, P3 = later or beyond Regionals. Titles are as TryHackMe lists them.

### Networking

| Room | Priority | Category | Min |
|---|---|---|---:|
| [What Is Networking?](https://tryhackme.com/room/whatisnetworking) | P2 | Networking and Nmap | 30 |
| [Intro to Networking](https://tryhackme.com/room/introtonetworking) | P2 | Networking and Nmap | 30 |
| [Networking Concepts](https://tryhackme.com/room/networkingconcepts) | P2 | Networking and Nmap | 30 |
| [Beginner Path Intro](https://tryhackme.com/room/beginnerpathintro) | P3 | Networking and Nmap | 20 |
| [Network Traffic Basics](https://tryhackme.com/room/networktrafficbasics) | P2 | Networking and Nmap | 30 |
| [DNS in Detail](https://tryhackme.com/room/dnsindetail) | P2 | Networking and Nmap | 30 |
| [Layer 2](https://tryhackme.com/room/layer2) | P3 | Networking and Nmap | 20 |
| [OpenVPN](https://tryhackme.com/room/openvpn) | P3 | Networking and Nmap | 20 |
| [Network Security Essentials](https://tryhackme.com/room/networksecurityessentials) | P2 | Networking and Nmap | 30 |
| [Network Services 2](https://tryhackme.com/room/networkservices2) | P2 | Networking and Nmap | 30 |
| [Guided Pentest: Infrastructure](https://tryhackme.com/room/guidedpentestinfrastructure) | P2 | Networking and Nmap | 30 |
| [Brute It](https://tryhackme.com/room/bruteit) | P2 | Networking and Nmap | 30 |
| [Hijack](https://tryhackme.com/room/hijack) | P2 | Networking and Nmap | 30 |
| [Bugged](https://tryhackme.com/room/bugged) | P2 | Networking and Nmap | 30 |
| [Publisher](https://tryhackme.com/room/publisher) | P2 | Networking and Nmap | 30 |
| [Lookup](https://tryhackme.com/room/lookup) | P2 | Networking and Nmap | 30 |
| [ChillHack](https://tryhackme.com/room/chillhack) | P2 | Networking and Nmap | 30 |
| [Printer Hacking 101](https://tryhackme.com/room/printerhacking101) | P3 | Networking and Nmap | 20 |
| [Cowboy Hacker](https://tryhackme.com/room/cowboyhacker) | P2 | Networking and Nmap | 30 |
| [Brooklyn Nine Nine](https://tryhackme.com/room/brooklynninenine) | P2 | Networking and Nmap | 30 |
| [Agent Sudo](https://tryhackme.com/room/agentsudoctf) | P2 | Networking and Nmap | 30 |
| [Lianyu](https://tryhackme.com/room/lianyu) | P2 | Networking and Nmap | 30 |

### Tooling

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Search Skills](https://tryhackme.com/room/searchskills) | P2 | Method | 30 |
| [Custom Tooling with Python](https://tryhackme.com/room/customtoolingpython) | P2 | Basic programming | 30 |
| [OhSINT](https://tryhackme.com/room/ohsint) | P2 | OSINT | 30 |
| [Intro to Cyber Threat Intel](https://tryhackme.com/room/cyberthreatintel) | P2 | Hacker tools / programming | 30 |
| [Metasploit: Introduction](https://tryhackme.com/room/metasploitintro) | P2 | Hacker tools / reverse shell | 30 |
| [Become a Hacker](https://tryhackme.com/room/becomeahackeroa) | P3 | Hacker tools / programming | 20 |

### Web

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Web Application Basics](https://tryhackme.com/room/webapplicationbasics) | P2 | Web exploits and SQL | 30 |
| [Web Security Essentials](https://tryhackme.com/room/websecurityessentials) | P2 | Web exploits and SQL | 30 |
| [Web Hacking Using curl (Advent of Cyber 2025)](https://tryhackme.com/room/webhackingusingcurl-aoc2025-w8q1a4s7d0) | P2 | Web exploits and SQL | 30 |
| [XSS (Advent of Cyber 2025)](https://tryhackme.com/room/xss-aoc2025-c5j8b1m4t6) | P2 | Web exploits and SQL | 30 |
| [Race Conditions (Advent of Cyber 2025)](https://tryhackme.com/room/race-conditions-aoc2025-d7f0g3h6j9) | P2 | Web exploits and SQL | 30 |
| [NoSQL Injection Tutorial](https://tryhackme.com/room/nosqlinjectiontutorial) | P2 | Web exploits and SQL | 30 |
| [Breaking Crypto the Simple Way](https://tryhackme.com/room/breakingcryptothesimpleway) | P2 | Crypto | 30 |
| [Detecting Web Attacks](https://tryhackme.com/room/detectingwebattacks) | P2 | Defence challenge | 30 |
| [Writing Pentest Reports](https://tryhackme.com/room/writingpentestreports) | P3 | Web exploits and SQL | 20 |
| [Guided Pentest: Web](https://tryhackme.com/room/guidedpentestweb) | P2 | Web exploits and SQL | 30 |
| [ColddBox: Easy](https://tryhackme.com/room/colddboxeasy) | P2 | Web exploits and SQL | 30 |
| [Cyborg](https://tryhackme.com/room/cyborgt8) | P2 | Web exploits and SQL | 30 |
| [Tech Supp0rt 1](https://tryhackme.com/room/techsupp0rt1) | P2 | Web exploits and SQL | 30 |

### Forensics

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Intro to Digital Forensics](https://tryhackme.com/room/introdigitalforensics) | P2 | Forensics and memory forensics | 30 |
| [Intro to DFIR](https://tryhackme.com/room/introductoryroomdfirmodule) | P2 | Forensics and memory forensics | 30 |
| [Intro to Logs](https://tryhackme.com/room/introtologs) | P2 | Defence challenge | 30 |
| [Intro to Cold System Forensics](https://tryhackme.com/room/introtocoldsystemforensics) | P3 | Forensics and memory forensics | 20 |
| [Forensic Imaging](https://tryhackme.com/room/forensicimaging) | P3 | Forensics and memory forensics | 20 |
| [Linux Filesystem Analysis](https://tryhackme.com/room/linuxfilesystemanalysis) | P2 | Forensics and memory forensics | 30 |
| [Linux Incident Surface](https://tryhackme.com/room/linuxincidentsurface) | P2 | Defence challenge | 30 |
| [macOS Forensics Basics](https://tryhackme.com/room/macosforensicsbasics) | P3 | Forensics and memory forensics | 20 |
| [Mobile Acquisition](https://tryhackme.com/room/mobileacquisition) | P3 | Forensics and memory forensics | 20 |
| [Autopsy](https://tryhackme.com/room/autopsy2ze0) | P2 | Forensics and memory forensics | 30 |
| [IR Playbooks](https://tryhackme.com/room/irplaybooks) | P2 | Forensics and memory forensics | 30 |
| [Critical](https://tryhackme.com/room/critical) | P2 | Forensics and memory forensics | 30 |
| [Case B4DM755](https://tryhackme.com/room/caseb4dm755) | P2 | Forensics and memory forensics | 30 |

### Windows

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Operating Systems Introduction](https://tryhackme.com/room/operatingsystemsintroduction) | P2 | Windows and defence | 30 |
| [Windows Command Line](https://tryhackme.com/room/windowscommandline) | P2 | Windows and defence | 30 |
| [Windows API](https://tryhackme.com/room/windowsapi) | P2 | Windows and defence | 30 |
| [Defensive Security Intro](https://tryhackme.com/room/defensivesecurityintroQR) | P2 | Windows and defence | 30 |
| [Intro to Endpoint Security](https://tryhackme.com/room/introtoendpointsecurity) | P2 | Windows and defence | 30 |
| [Introduction to EDRs](https://tryhackme.com/room/introductiontoedrs) | P2 | Windows and defence | 30 |
| [Intro to SIEM](https://tryhackme.com/room/introtosiem) | P2 | Defence challenge | 30 |
| [Windows Logging for SOC](https://tryhackme.com/room/windowsloggingforsoc) | P2 | Defence challenge | 30 |
| [Pyramid of Pain](https://tryhackme.com/room/pyramidofpainax) | P2 | Windows and defence | 30 |
| [Investigating Windows](https://tryhackme.com/room/investigatingwindows) | P2 | Windows and defence | 30 |
| [Servidae](https://tryhackme.com/room/servidae) | P3 | Windows and defence | 20 |
| [Ice](https://tryhackme.com/room/ice) | P2 | Windows and defence | 30 |
| [Blue](https://tryhackme.com/room/blue) | P2 | Windows and defence | 30 |
| [Blaster](https://tryhackme.com/room/blaster) | P3 | Windows and defence | 20 |
| [Blueprint](https://tryhackme.com/room/blueprint) | P3 | Windows and defence | 20 |
| [Atlas](https://tryhackme.com/room/atlas) | P3 | Windows and defence | 20 |

### Malware

| Room | Priority | Category | Min |
|---|---|---|---:|
| [History of Malware](https://tryhackme.com/room/historyofmalware) | P3 | Reverse engineering / malware | 20 |
| [MalMal: Introductory](https://tryhackme.com/room/malmalintroductory) | P3 | Reverse engineering / malware | 20 |
| [Malware Classification](https://tryhackme.com/room/malwareclassification) | P3 | Reverse engineering / malware | 20 |
| [Common Attacks](https://tryhackme.com/room/commonattacks) | P3 | Reverse engineering / malware | 20 |
| [Intro to Antivirus](https://tryhackme.com/room/introtoav) | P3 | Reverse engineering / malware | 20 |
| [Malware Researching](https://tryhackme.com/room/malresearching) | P3 | Reverse engineering / malware | 20 |
| [x86-64 Architecture](https://tryhackme.com/room/x8664arch) | P3 | Reverse engineering | 20 |
| [Phishing Emails 1](https://tryhackme.com/room/phishingemails1tryoe) | P3 | Reverse engineering / malware | 20 |
| [Phishing Emails 2](https://tryhackme.com/room/phishingemails2rytmuv) | P3 | Reverse engineering / malware | 20 |
| [Parrot Post](https://tryhackme.com/room/parrotpost) | P3 | Reverse engineering / malware | 20 |
| [Android Malware Analysis](https://tryhackme.com/room/androidmalwareanalysis) | P3 | Reverse engineering / malware | 20 |
| [HTA & PowerShell (Advent of Cyber 2025)](https://tryhackme.com/room/htapowershell-aoc2025-p2l5k8j1h4) | P3 | Reverse engineering / malware | 20 |

### Reverse engineering

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Valley PE](https://tryhackme.com/room/valleype) | P2 | Reverse engineering | 30 |
| [MMA (Malware Analysis)](https://tryhackme.com/room/mma) | P2 | Reverse engineering | 30 |
| [0x41haz](https://tryhackme.com/room/0x41haz) | P2 | Reverse engineering | 30 |
| [Dear QA](https://tryhackme.com/room/dearqa) | P2 | Reverse engineering | 30 |

### Active Directory

| Room | Priority | Category | Min |
|---|---|---|---:|
| [Introduction to Active Directory Authentication](https://tryhackme.com/room/introtoactivedirectoryauthentication) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [AD Basics: Enumeration](https://tryhackme.com/room/adbasicenumeration) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [Introduction to Active Directory Breaching](https://tryhackme.com/room/introductiontoactivedirectorybreaching) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [VulnNet: Roasted](https://tryhackme.com/room/vulnnetroasted) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [AD Certificate Templates](https://tryhackme.com/room/adcertificatetemplates) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [Post-Exploitation Basics](https://tryhackme.com/room/postexploit) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [Soupedecode 01](https://tryhackme.com/room/soupedecode01) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |
| [Monitoring Active Directory](https://tryhackme.com/room/monitoringactivedirectory) | P3 | Privilege escalation and AD (beyond Regionals) | 20 |

## Also in your pack

Nmap and networking deep book (PDF 41), memory forensics book (PDF 39), basic SQL lab (PDF 42), the defence runbook (PDF 40) and the flashcards cover the same skills from the reading side.
