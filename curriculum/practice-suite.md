# Practice suite

Every skill has: the **manual method**, the **tool** that speeds it up, a **model-assisted method** (what a local LLM may do and what it must not), **exercises** in order, and a **done-when** test. Mark a skill `reliable` in `checklist.md` only when you have passed its done-when test twice, on different days, without notes.

Use only legal targets: your own labs, the platforms below, and competition infrastructure within scope.

## 0. Method card (applies to every challenge)

1. **Observe**: what exactly was given (files, URLs, ports, hints)? Run `file`, `strings`, `curl -i`, `nmap`, whatever applies, before thinking.
2. **Classify**: category and probable technique. Write one sentence.
3. **Hypothesize**: list up to 3 causes ranked by likelihood.
4. **Smallest test**: pick the single cheapest command that separates hypotheses.
5. **Verify**: confirm the flag format and test the answer independently before submitting.
6. **Record**: 5-line writeup in `notes/`: what it was, first useful observation, technique, tool, mistake.
7. **Time-box**: 30 minutes alone, then swap or ask. Note the point you gave up.

**Study-time rule (AI is banned at the competition, so train without it):** the model may propose hypotheses, write throwaway scripts, and summarize large output. A human runs the test and checks the answer. A model's offset, address, CVE number or flag is a claim, never a result.

---

## 1. Foundations

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Linux CLI | pipe `grep/awk/sed/cut/sort/uniq`, `find`, permissions, processes | bash, coreutils, tmux | generate one-liners; you must explain each flag | Bandit 0-33, Linux Journey | Solve 5 text-processing tasks in <10 min each without searching |
| Encodings and transforms | recognise base64/32/58, hex, URL, rot, XOR, gzip, magic bytes | CyberChef, `xxd`, `base64`, `file` | suggest a decode chain from sample | CyberChef recipes, Bandit, picoGym "General skills" | Decode a 4-layer chain in <5 min |
| Python for CTF | sockets, `requests`, `struct`, `re`, files, loops, `subprocess` | pwntools, requests, pycryptodome, sympy | draft a script, then read it line by line | write helpers: `xor.py`, `rsa.py`, `fetch.py`, `pcap_urls.py` | Write a working socket/HTTP automation script from a blank file in <15 min |
| Networking | TCP/IP, DNS, HTTP, TLS, ports, subnetting, ARP | Nmap, Wireshark, `nc`, `curl`, `dig` | explain unfamiliar protocol fields | Nmap Network Scanning, THM "Network Fundamentals", your CCNA labs | Explain a pcap's story in 5 min; scan a /24 and report services |
| Git, Docker, VMs | clone, branch, run containers, snapshot VMs | git, docker, VMware | none needed | Juice Shop container, Kali VM snapshots | Rebuild the lab from scratch in <30 min |
| Note-taking | 5-line writeups, searchable tags | Markdown, Obsidian or the repo `notes/` | summarize your notes for retrieval only | one writeup per solved challenge | 30 writeups by Nov 14 |

## 2. Web exploitation (highest priority)

Method: map the app (routes, params, auth, roles), identify trust boundaries, test each input class, then chain.

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Recon | view-source, JS/source maps, robots.txt, hidden dirs, error messages, response headers | Burp, ffuf/gobuster, browser devtools | summarize large JS bundles; list endpoints | Juice Shop scoreboard, Natas 0-10 | Find hidden route/param on 5 apps in <10 min each |
| SQL injection | quote test, comment syntax, UNION column count, boolean/time blind, DB fingerprint | sqlmap (last), Burp | write a boolean-blind extractor script | PortSwigger SQLi (all labs), Juice Shop SQLi, DVWA, bWAPP | Union + blind extraction by hand on 3 targets |
| XSS | reflect context (HTML/attr/JS), encode, bypass filters, DOM sinks | Burp, browser console | propose payloads per context | PortSwigger XSS (all), Juice Shop DOM XSS, DVWA | Pop XSS in 5 different contexts without a cheat sheet |
| Auth and sessions | cookies, JWT (none alg, weak key, kid), password reset, MFA flaws, brute-force limits | jwt_tool, Burp, hashcat | explain a JWT header/claims | PortSwigger authentication, JWT; Juice Shop auth | Forge a JWT two ways |
| Access control | IDOR, forced browsing, method/role switching | Burp Autorize | none | PortSwigger access control, Juice Shop | Find IDOR in 3 apps manually |
| Command injection and file inclusion | `;`, `&&`, `$()`, backticks, path traversal, LFI wrappers | Burp | generate bypass variants | PortSwigger OS command injection, path traversal; DVWA | Read an arbitrary file via 3 different bypasses |
| File upload | extension, content-type, magic bytes, polyglots, path | Burp | none | PortSwigger file upload | Upload bypass in 4 variants |
| SSRF/XXE | internal URLs, cloud metadata (conceptual), XML entities, blind/OOB | Burp Collaborator alternatives (interactsh), curl | none | PortSwigger SSRF, XXE | Reach an internal service via SSRF |
| SSTI | engine fingerprint (`{{7*7}}`), sandbox escapes | tplmap (careful), manual | suggest engine-specific payloads | PortSwigger SSTI, THM SSTI | RCE via SSTI on Jinja2 and one other engine |
| Deserialization | PHP unserialize gadget, Python pickle, Java basics | ysoserial (Java), PHPGGC | explain a gadget chain | PortSwigger deserialization | Pickle RCE from scratch |
| API/GraphQL | enumerate endpoints, introspection, mass assignment, BOLA | Postman, Burp, InQL | none | crAPI, Damn Vulnerable GraphQL | 3 findings on crAPI |
| Prototype pollution, race conditions, request smuggling | read the lab theory | Burp | explain theory only | PortSwigger (stretch topics) | At least one lab each (P3) |

## 3. Network, infrastructure and AD

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Service enumeration | full TCP scan, per-service enumeration, banner/version research | Nmap, nc, smbclient, enum4linux-ng, snmpwalk, ldapsearch | summarize scan output | THM "Nmap", "Network Services", VulnHub Basic Pentesting, Kioptrix | Enumerate a box and list 5 attack paths in 15 min |
| Exploitation | match version → public exploit; read the exploit before running | searchsploit, Metasploit, manual PoCs | explain what an exploit does; never run unseen code | VulnHub, Metasploitable 2, THM "Blue", "Ice" | Exploit one service manually and one with Metasploit |
| Password attacks | wordlist + rules, hash identification, spraying | hashcat, john, hydra, ncrack, hashid | suggest candidate wordlists from context | THM "Crack the Hash", HTB crypto/hash boxes | Crack 5 hash types; use rules |
| Linux privesc | sudo, SUID, cron, caps, writable files/PATH, kernel | linpeas (after manual), GTFOBins | explain linpeas findings | THM "Linux PrivEsc", HTB easy boxes, Bandit/Narnia | Root 3 boxes via 3 different techniques |
| Windows privesc | services, tokens, unquoted paths, AlwaysInstallElevated, scheduled tasks | winpeas, PowerUp, Seatbelt | explain output | THM "Windows PrivEsc", HTB easy Windows | Escalate on 2 Windows boxes |
| Active Directory | enumerate users/SPNs, Kerberoast, AS-REP roast, PtH/PtT, ACL abuse | BloodHound, impacket, crackmapexec/netexec, Rubeus | explain BloodHound path | THM "Attacktive Directory", "Active Directory Basics", your own AD lab, GOAD | Domain admin in a lab via two paths |
| Pivoting | SSH forwards, SOCKS, port forwarding | chisel, ligolo-ng, proxychains | none | THM "Wreath", HTB boxes | Pivot to an internal subnet |
| Shells | reverse/bind, TTY upgrade, file transfer | nc, socat, revshells.com, python | none | any box | Stabilise a shell in <2 min |

## 4. Forensics and incident response

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| PCAP | protocol hierarchy → conversations → follow streams → extract objects | Wireshark, tshark, NetworkMiner, zeek | summarize conversations; suggest filters | Malware-Traffic-Analysis.net exercises, picoGym, CyberDefenders | Answer 10 questions about an unseen pcap in <20 min |
| Files and stego | `file`, `exiftool`, `binwalk`, `strings`, carve, LSB | binwalk, foremost, zsteg, steghide, stegsolve, audacity | none | picoGym forensics, Root-Me stego | 10 stego challenges, name tool order |
| Disk | partitions, deleted files, timeline, registry hives | Autopsy, Sleuth Kit, FTK Imager, RegRipper | summarize timeline | CyberDefenders disk labs, THM "Autopsy" | Timeline a disk image |
| Memory | process list, netscan, cmdline, dump files, malfind | Volatility 3 | explain plugin output | CyberDefenders memory labs, THM "Volatility" | Find malware process + C2 in a memory image |
| Logs | grep patterns, timeline, anomalies, auth events | grep/awk, jq, Splunk-lite, Chainsaw/Hayabusa | summarize log clusters | CyberDefenders, BTLO, LetsDefend | Identify attacker IP, time, technique from 1k lines |
| Malware triage | strings, PE headers, imports, packers, sandbox report | PE-bear, DIE, strings, CAPA, YARA, CyberChef | deobfuscate scripts (check output) | MalwareBazaar samples in a VM, Practical Malware Analysis labs | Triage 3 samples in 10 min each, no execution |
| Deobfuscation | JS/PowerShell/VBA macro layers | CyberChef, node, olevba | explain each layer; you execute in sandbox | THM "Malware" rooms, CyberDefenders | Deobfuscate a PowerShell downloader |
| IR process | triage → scope → contain → eradicate → report | notes, timeline template | draft report for you to edit | BTLO, HTB Sherlocks | Write a 1-page incident report with timeline in 20 min |
| Detection | Sysmon/Windows event IDs, Sigma rules, Suricata | Sigma, Suricata, Sysmon config | draft a rule; you test it | THM SOC Level 1 path, Blue Team Labs | Write and test 3 detections |

## 5. Reverse engineering

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Static analysis | `file`, `strings`, imports, main → decompile → rename | Ghidra, rizin/cutter, objdump | summarize decompiled function; check against the asm | crackmes.one (difficulty 1-3), pwn.college RE, picoGym RE | Solve 5 crackmes <20 min each |
| Dynamic analysis | breakpoints, watchpoints, registers, `ltrace`/`strace` | gdb + pwndbg/GEF | none | same | Extract a password via debugger |
| Assembly | x86-64 registers, calling convention, stack, jumps | ref card, Compiler Explorer | explain asm in plain language (spot-check) | Reverse Engineering for Beginners (first chapters) | Read 30 lines of asm and describe behavior |
| Managed code | .NET, Java, Python bytecode decompile | dnSpy/ILSpy, jadx, uncompyle6/pycdc | none | crackmes.one, picoGym | Decompile & solve 3 |
| Packers and obfuscation | UPX, simple XOR stubs, control-flow flattening basics | upx, DIE, x64dbg | none | picoGym, crackmes.one | Unpack UPX and solve |
| Symbolic execution | angr/Z3 for constraint puzzles | angr, z3-solver | generate a z3 script; you validate | pwn.college, CTF writeups | Solve 2 with Z3 |

## 6. Binary exploitation

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Stack overflow / ret2win | find offset (cyclic), control RIP, call win | pwntools, gdb, checksec | none | ROP Emporium ret2win, pwn.college, Narnia, picoGym | 3 ret2win solves from scratch |
| Shellcode | write/modify shellcode, NX off | pwntools shellcraft | none | pwn.college "Shellcode Injection" | Execve shellcode working |
| ROP | gadget chain, ret2libc, PIE/ASLR leak | ROPgadget, pwntools, one_gadget | none | ROP Emporium (all) | Solve ROP Emporium 1-4 |
| Format string | `%p` leak, `%n` write | pwntools fmtstr | none | pwn.college, picoGym, Protostar | Leak + overwrite GOT |
| Heap basics | tcache poisoning, use-after-free | gdb, pwndbg heap | none | pwn.college heap, how2heap (P3) | Stretch only |

## 7. Cryptography

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| Classical | frequency analysis, Caesar/Vigenère/XOR | CyberChef, dcode.fr | none | CryptoHack intro, picoGym | 10 solved |
| RSA | small e, common modulus, Wiener, factorization, Fermat, Hastad | Python, sympy, RsaCtfTool, factordb | none | CryptoHack RSA, picoGym | Solve 8 RSA variants by recognising the weakness |
| Symmetric | ECB detection, CBC bit-flip, padding oracle, CTR nonce reuse | pycryptodome | none | CryptoHack Symmetric, Cryptopals 1-2 | Padding oracle script from scratch |
| Hashes and MACs | length extension, collision basics | hashpump, hashcat | none | CryptoHack Hashes | Length extension attack |
| Randomness | weak PRNG (Python `random`, LCG), seeding | randcrack, Z3 | none | CryptoHack, picoGym | Predict next outputs |
| Elliptic curves / lattices | read-only introduction | Sage | none | CryptoHack ECC (P3) | Stretch |

## 8. OSINT and miscellaneous

| Skill | Manual method | Tools | Model-assisted | Exercises | Done when |
|---|---|---|---|---|---|
| OSINT | metadata, reverse image, geolocation, social, DNS, cert transparency, Wayback | exiftool, Google Lens, crt.sh, Wayback, sherlock | summarize findings; never accuse real people | Sourcing.games, GeoGuessr, TryOSINT, CTF OSINT | 5 geolocation puzzles |
| Scripting puzzles | read spec, write parser/solver quickly | Python | write skeleton; you debug | picoGym, CTF "programming" | 3 under 20 min |
| Jail escapes | Python/bash restricted shells | manual | none | picoGym, CTF writeups | 2 escapes |
| Web3/Blockchain (rare) | skip unless time | | | | P3 |

## 9. AI use (study-time only: **not allowed at CyberSci**)

These skills apply to learning and to other CTFs whose rules permit AI. Do not use them in CyberSci rehearsals.

| Skill | What to practise | Done when |
|---|---|---|
| Triage prompting | paste challenge text + artefact list; ask for category, 3 hypotheses, cheapest test | In 3 mock events, the model's top hypothesis is right ≥50% |
| Artefact summarization | give large output in chunks; require quotes of line numbers | No summary contains an unverifiable claim in your spot checks |
| Script generation | request a script from a one-sentence spec; run in sandbox; fix | Working script in <5 min for 5 recurring tasks |
| RAG retrieval | question your notes/cheat sheets offline | Retrieve right snippet for 8/10 queries |
| Model routing | pick model by task size; record latency and wrong answers | Benchmark table complete (3 models × 10 tasks) |
| Failure awareness | note every wrong model claim and its type (offset, CVE, flag, command syntax) | Written "never trust the model for…" list in your runbook |
| Tool-calling reliability | run the shell MCP with small models; measure malformed calls | <10% malformed calls or switch to scripted pipeline |
| Guardrails | allowlist, command log, scope check, no secrets in prompts | Dry-run verifies a blocked command is blocked |

## 10. Competition and team skills

| Skill | Practice | Done when |
|---|---|---|
| Triage | rank by points ÷ estimated minutes within 10 min of start | Used in every mock |
| Time-boxing | 30-minute rule with a visible timer | ≤1 challenge per mock exceeds the box |
| Communication | one shared board: unsolved / in progress / solved / blocked | No two people on the same challenge unintentionally |
| Submission discipline | one owner submits; verify flag format | Zero invalid-flag penalties in mocks |
| Stamina | 8-hour InIt CTF rehearsal, food/water plan | You can write the plan from memory |
| Interview readiness | 60-second self-intro, one lab story, one CTF story, one AI-stack story | Told to a teammate without notes |
