#!/usr/bin/env python3
"""Competition content backlog: every category each milestone event draws on, broken into topics, for content to be made.

Run after roadmap_2027.py:   python scripts/content_backlog.py   then   python scripts/tracker.py render
Writes tracker/content_backlog.csv and tracker/CONTENT-BACKLOG.md and appends the K-ids to roadmap.csv backlog_ids.
Category lists per event come from each event's own category structure where known; others are inferred and tagged.
'basis': listed = organiser publishes categories (NCL, picoCTF, NorthSec tracks); typical = what that CTF series usually runs.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

T = Path(__file__).resolve().parent.parent / "tracker"

# code: (name, default content, [(topic, level, study_hours)])
CATS = {
 "GEN": ("General skills (Linux, Python, encodings)", "primer chapter + 6 drills", [
   ("Linux shell fluency: find, grep, awk, sed, pipes", "L1", 4), ("File types, magic bytes, file/xxd/strings", "L1", 3),
   ("Encodings chain: base64/32/58, hex, URL, rot, morse, braille", "L1", 3), ("Python for CTFs: sockets, requests, struct, pwntools basics", "L2", 6),
   ("Git, archives and compression tricks (tar, zip, 7z, nested)", "L1", 2), ("Reading source: C, Python, JS, PHP at speed", "L2", 4)]),
 "WEB": ("Web exploitation", "chapter + 3 labs + flashcards", [
   ("SQL injection: union, blind, error, second-order, filters bypass", "L2", 6), ("XSS: reflected, stored, DOM, CSP bypass, bot/admin-visit challenges", "L2", 6),
   ("SSRF and internal-service pivots (cloud metadata, gopher)", "L3", 4), ("Authentication and sessions: JWT, cookies, password reset, IDOR", "L2", 5),
   ("File upload, LFI/RFI, path traversal, PHP wrappers", "L2", 5), ("Server-side template injection (Jinja2, Twig, Freemarker)", "L3", 4),
   ("Deserialization: PHP, Java, Python pickle, .NET", "L3", 6), ("XXE and XML parsers", "L3", 3), ("Request smuggling, cache poisoning, host-header attacks", "L3", 6),
   ("Prototype pollution, NoSQL injection, mass assignment", "L3", 4), ("GraphQL and API testing", "L3", 4), ("Race conditions and logic flaws", "L3", 4),
   ("OAuth/SAML/SSO flaws", "L3", 4), ("CSRF, CORS, clickjacking, WebSockets", "L2", 4), ("Framework quirks: PHP juggling, Node, Flask, Spring", "L3", 5),
   ("Web recon and content discovery speed (ffuf, gobuster, Burp)", "L2", 3)]),
 "PWN": ("Binary exploitation (pwn)", "chapter + lab binaries + pwntools templates", [
   ("Stack overflow basics: ret2win, offsets, cyclic patterns", "L2", 4), ("Shellcode and NX/ASLR/PIE/canary protections", "L2", 5),
   ("ROP chains and ret2libc, one_gadget", "L3", 8), ("Format-string bugs: read, write, GOT overwrite", "L3", 6), ("Heap: tcache, fastbin, use-after-free, double free", "L3", 12),
   ("SROP, ret2dlresolve, ret2csu", "L3", 6), ("Seccomp and sandbox escapes (ORW chains)", "L3", 5), ("Kernel pwn intro (modules, LKM bugs)", "L3", 10),
   ("Other architectures: ARM, MIPS, RISC-V emulation with qemu", "L3", 6), ("Browser and JS-engine pwn intro (V8 basics)", "L3", 10),
   ("Windows pwn basics", "L3", 6), ("Exploit workflow: gdb/pwndbg, pwntools, remote vs local debug", "L2", 4)]),
 "REV": ("Reverse engineering", "chapter + 10 crackmes + radare2/ghidra drills", [
   ("Static analysis workflow in Ghidra and radare2", "L2", 5), ("Dynamic analysis: gdb, ltrace, strace, Frida", "L2", 5),
   ("Anti-debug, obfuscation and packers (UPX, control-flow flattening)", "L3", 6), ("Managed code: .NET (dnSpy), Java (jadx), Python bytecode", "L2", 5),
   ("Custom VMs and bytecode interpreters", "L3", 8), ("Symbolic execution: z3 and angr", "L3", 6), ("Android APK reversing (jadx, apktool, frida)", "L3", 6),
   ("WebAssembly and JavaScript obfuscation", "L3", 4), ("Rust and Go binaries", "L3", 4), ("Firmware images and embedded binaries", "L3", 5),
   ("Game hacking and memory tools (Cheat Engine)", "L2", 3), ("Keygens and crackme patterns", "L2", 4)]),
 "CRY": ("Cryptography", "chapter + Python notebooks + drills", [
   ("Classical ciphers and frequency analysis", "L1", 3), ("XOR, repeating-key XOR, one-time-pad reuse", "L1", 3), ("RSA basics and attacks: small e, common modulus, Wiener, factorisation", "L2", 8),
   ("AES modes: ECB, CBC bit-flip, padding oracle, CTR reuse", "L2", 8), ("Hash functions, length extension, collisions, MACs", "L2", 4), ("Elliptic curves and ECDSA nonce reuse", "L3", 8),
   ("Lattices, LLL and Coppersmith", "L3", 10), ("PRNG attacks: Mersenne Twister, LCG, state recovery", "L3", 5), ("Diffie-Hellman and discrete log", "L3", 4),
   ("Z3/SAT for custom ciphers", "L3", 4), ("Side channels and timing", "L3", 3), ("Zero-knowledge, post-quantum and signatures intro", "L3", 5)]),
 "FOR": ("Digital forensics", "chapter + sample images + tool sheets", [
   ("Disk images and file systems (Autopsy, sleuthkit, deleted files)", "L2", 5), ("Memory forensics with Volatility 3", "L3", 6),
   ("Network forensics: pcap triage in Wireshark/tshark", "L2", 5), ("File carving and file-format repair (foremost, binwalk, magic bytes)", "L2", 4),
   ("Steganography: image, audio, video, text (steghide, zsteg, sox, ffmpeg)", "L2", 5), ("Windows artefacts: registry, event logs, prefetch, shellbags", "L3", 6),
   ("Linux artefacts and timeline analysis", "L2", 4), ("Email and phishing analysis, Office macros, PDF analysis", "L2", 4), ("Mobile and USB forensics basics", "L3", 4),
   ("Cloud and container forensics logs", "L3", 4)]),
 "NET": ("Network, scanning and enumeration", "chapter + lab network + nmap/ldap sheets", [
   ("Nmap scanning strategy and NSE scripts", "L2", 4), ("Service enumeration: SMB, FTP, SSH, SNMP, NFS, DNS, SMTP", "L2", 6),
   ("Wireless: WPA handshakes, aircrack, deauth, evil-twin concepts", "L3", 6), ("Pivoting and tunnelling: chisel, ssh -D, proxychains, ligolo", "L3", 5),
   ("Protocol analysis and custom protocols (netcat, scapy)", "L3", 5), ("Sniffing, ARP and MITM concepts in a lab", "L2", 3), ("IPv6, VLANs and routing for CTF networks", "L3", 4)]),
 "PWD": ("Password cracking", "chapter + wordlist/rule drills", [
   ("Hash identification and hashcat/john modes", "L1", 3), ("Wordlists, rules and masks", "L2", 4), ("Cracking archives and documents: ZIP, PDF, Office, KeePass, SSH keys", "L2", 4),
   ("Windows and AD hashes: NTLM, NetNTLMv2, Kerberos", "L3", 4), ("Linux shadow, bcrypt, scrypt, argon2 and cost", "L2", 3)]),
 "OSI": ("OSINT", "chapter + 10 timed puzzles", [
   ("Image geolocation and reverse image search", "L2", 5), ("People, username and social-media research", "L2", 4), ("Domains, IPs, certificates, Shodan and passive DNS", "L2", 4),
   ("Metadata, archives (Wayback) and document leaks", "L1", 3), ("Maps, satellite and street-level tools", "L2", 3), ("Methodology and OPSEC for investigations", "L1", 2)]),
 "LOG": ("Log analysis and blue-team data", "chapter + log sets + query sheets", [
   ("Web server and application logs with grep/awk/jq", "L2", 4), ("Windows event IDs and Sysmon", "L2", 5), ("Sigma rules, Splunk/ELK queries", "L3", 5),
   ("Zeek and Suricata logs", "L3", 4), ("Authentication and cloud audit logs", "L3", 4)]),
 "BLU": ("Defence, incident response and attack/defend", "runbook + defence lab", [
   ("Hardening Linux and Windows quickly", "L2", 5), ("Patching a vulnerable web app under time pressure", "L2", 4), ("Incident-response workflow and one-page reports", "L2", 4),
   ("Detection engineering: write a rule for each attack you practise", "L3", 6), ("Attack/defend game rules, scoring and patch-vs-exploit strategy", "L3", 5)]),
 "AD": ("Active Directory and Windows/Linux privilege escalation", "chapter + GOAD-style lab", [
   ("AD enumeration (ldapsearch, rpcclient, BloodHound)", "L2", 6), ("Kerberos attacks and defences", "L3", 6), ("ADCS and delegation misconfigurations", "L3", 6),
   ("Lateral movement and credential reuse", "L3", 5), ("Windows privilege escalation", "L3", 6), ("Linux privilege escalation (SUID, sudo, cron, capabilities)", "L2", 5),
   ("NTLM relay and signing defences", "L3", 5)]),
 "CLD": ("Cloud and containers", "chapter + free-tier lab", [
   ("AWS IAM, S3 and metadata service misconfigurations", "L2", 5), ("Azure and GCP basics", "L3", 4), ("Docker escapes and Kubernetes misconfigurations", "L3", 6),
   ("CI/CD and secrets in git", "L2", 3), ("Serverless and cloud logging", "L3", 3)]),
 "HW": ("Hardware, IoT, RF and physical", "chapter + kit list + firmware samples", [
   ("UART, JTAG, SPI/I2C: identify and connect", "L3", 6), ("Firmware extraction and analysis (binwalk, firmadyne)", "L3", 5), ("Arduino/ESP/microcontroller code and serial protocols", "L2", 5),
   ("Software-defined radio and RF signals (SDR basics, rtl_433)", "L3", 6), ("Bluetooth Low Energy and badges (NorthSec-style)", "L3", 5), ("NFC/RFID and card cloning concepts", "L3", 4),
   ("CAN bus and automotive basics", "L3", 4), ("Logic analyser and protocol decoding (sigrok)", "L3", 3), ("Lock picking and physical security basics (legal practice)", "L2", 4)]),
 "MSC": ("Misc, scripting and puzzles", "chapter + 20 mini-puzzles", [
   ("Python jails and restricted shells", "L3", 4), ("Esoteric languages, QR/barcodes, ciphers in images", "L1", 3), ("Programming puzzles under time (parsing, graph, maths)", "L2", 5),
   ("Automating servers and sockets: solve scripts", "L2", 4), ("CyberChef recipes and scripting speed", "L1", 3), ("Scoreboard and flag-submission strategy", "L1", 2)]),
 "BCH": ("Blockchain and smart contracts", "chapter + Foundry/Hardhat labs", [
   ("Solidity and EVM basics", "L3", 5), ("Reentrancy, overflow, access-control bugs", "L3", 5), ("Transaction and storage analysis", "L3", 4), ("Foundry/Hardhat tooling", "L3", 3)]),
 "AI": ("AI and LLM security", "chapter + prompt-injection labs", [
   ("Prompt injection and jailbreak challenges", "L2", 4), ("LLM agent and tool-use attacks", "L3", 4), ("Adversarial examples and model extraction basics", "L3", 4),
   ("Using AI tools within the rules (NorthSec AI experience, allowed events)", "L2", 3), ("Policy: which events allow AI, how to train without it", "L1", 1)]),
 "MOB": ("Mobile (Android and iOS)", "chapter + lab APKs", [
   ("Android app structure and APK reversing", "L2", 5), ("Frida hooking and certificate-pinning bypass", "L3", 5), ("Mobile storage, intents and deep-link bugs", "L3", 4), ("iOS basics for CTFs", "L3", 3)]),
 "MAL": ("Malware analysis and deobfuscation", "chapter + safe samples in a VM", [
   ("Static triage: strings, imports, YARA", "L2", 4), ("Dynamic analysis in a sandbox VM", "L2", 4), ("Script deobfuscation: JavaScript, PowerShell, VBA", "L2", 5),
   ("Ransomware and loader patterns (CTF-style)", "L3", 4), ("Network indicators and C2 traffic reading", "L3", 4)]),
 "SOC": ("Social engineering and physical (rules-bound)", "chapter + rules-of-engagement checklist", [
   ("Phishing simulation concepts and detection (no real targets)", "L1", 2), ("Physical-security challenges: lock types, badges, tailgating concepts", "L1", 3), ("Rules of engagement for onsite events", "L1", 1)]),
 "TEAM": ("Team operations (team of 8)", "team handbook + templates", [
   ("Roles per category and a shared notes system", "L2", 3), ("Comms, handoffs and the scoreboard routine", "L2", 2), ("Rehearsal format, time boxes and post-event debrief template", "L2", 3),
   ("Onsite logistics (NorthSec, Hackfest): travel, kit, power, food, sleep", "L1", 2), ("Writeup pipeline: notes during, publish within 48 h", "L1", 2)]),
}

# event -> (basis, categories). ids refer to tracker/milestones.csv.
EVENTS = {
 "M01": ("typical", "WEB AI CLD MSC FOR REV NET"), "M02": ("typical", "NET WEB FOR LOG MAL CLD AI OSI"), "M03": ("typical", "WEB PWN REV CRY FOR HW BCH MSC"),
 "M04": ("typical", "WEB PWN REV CRY FOR MSC BCH"), "M05": ("typical", "PWN REV CRY WEB MSC"), "M07": ("listed", "GEN WEB CRY FOR REV PWN"),
 "M08": ("typical", "WEB PWN REV CRY MSC"), "M10": ("listed", "OSI CRY PWD LOG FOR NET WEB AD HW"), "M11": ("listed", "WEB PWN REV CRY FOR NET HW MOB AD MSC TEAM SOC AI BLU"),
 "M12": ("typical", "PWN REV CRY WEB MSC"), "M13": ("typical", "AD BLU WEB FOR NET CLD"), "M14": ("typical", "WEB PWN REV CRY MSC HW"),
 "M15": ("typical", "WEB PWN REV CRY FOR MSC OSI"), "M17": ("typical", "WEB PWN REV CRY FOR MSC HW AI"), "M18": ("listed", "OSI CRY PWD LOG FOR NET WEB AD HW"),
 "M19": ("typical", "WEB NET HW SOC MSC"), "M20": ("typical", "GEN WEB FOR OSI HW MSC"), "M21": ("listed", "WEB PWN REV CRY FOR NET OSI MSC BLU AD CLD"),
 "M23": ("typical", "WEB PWN REV CRY FOR HW BCH MSC"), "M25": ("typical", "WEB PWN REV CRY FOR MSC"), "M26": ("typical", "MAL FOR WEB REV MSC OSI CRY GEN"),
 "M27": ("typical", "WEB PWN REV CRY MSC"),
}

# category -> regex on a roadmap week's theme+practice that suits it; backlog items are spread over the matching weeks.
WEEKS = {
 "GEN": r"warm-up|boxes|picoctf", "WEB": r"web", "PWN": r"binary|pwn", "REV": r"reverse", "CRY": r"crypto", "FOR": r"forensic", "NET": r"recon|boxes|network|nmap",
 "PWD": r"ncl", "OSI": r"osint|ncl", "LOG": r"ncl|forensics", "BLU": r"blue|attack/defend|defence", "AD": r"\bad\b|active directory|domain", "CLD": r"cloud",
 "HW": r"northsec", "MSC": r"scripting|timed|mixed", "BCH": r"hard targets|summer", "AI": r"northsec|team formation", "MOB": r"reverse medium|summer build",
 "MAL": r"reverse engineering|forensics|huntress", "SOC": r"northsec|hackfest", "TEAM": r"team|rehearsal",
}


def read(name):
    with (T / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ms = {r["id"]: r for r in read("milestones.csv")}
    need = defaultdict(list)       # category -> event ids
    for ev, (basis, cats) in EVENTS.items():
        assert ev in ms, ev
        for c in cats.split():
            assert c in CATS, c
            need[c].append(ev)
    items = []
    for code, (name, content, topics) in CATS.items():
        evs = need.get(code, [])
        yes = sum(1 for e in evs if ms[e]["priority"].startswith("yes"))
        for i, (topic, lvl, hrs) in enumerate(topics, 1):
            items.append(dict(id=f"K-{code}{i:02d}", category=code, category_name=name, topic=topic, level=lvl, study_hours=hrs, content=content,
                              events=" ".join(evs), n_events=len(evs), n_priority=yes, score=len(evs) + 2 * yes, week="", status="todo"))
    # schedule items into matching roadmap weeks (round-robin, highest score first within a category)
    rm = read("roadmap.csv")
    for code in CATS:
        its = sorted([x for x in items if x["category"] == code], key=lambda x: -x["score"])
        wks = [w for w in rm if re.search(WEEKS.get(code, "$^"), (w["theme"] + " " + w["practice"]).lower()) and w["week_start"] < "2027-10-01"]
        for k, it in enumerate(its):
            if wks:
                it["week"] = wks[k % len(wks)]["week_start"]
    # write csv
    cols = ["id", "category", "category_name", "topic", "level", "study_hours", "content", "events", "n_events", "n_priority", "score", "week", "status"]
    with (T / "content_backlog.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for it in sorted(items, key=lambda x: (-x["score"], x["id"])):
            w.writerow({c: it[c] for c in cols})
    # put the ids on the roadmap weeks (idempotent: drop old K- ids first)
    by_week = defaultdict(list)
    for it in items:
        if it["week"]:
            by_week[it["week"]].append(it["id"])
    with (T / "roadmap.csv").open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fields, rows = r.fieldnames, list(r)
    for row in rows:
        keep = [x for x in row["backlog_ids"].split() if not x.startswith("K-")]
        row["backlog_ids"] = " ".join(keep + by_week.get(row["week_start"], []))
    with (T / "roadmap.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    # markdown views
    out = ["# Competition content backlog", "",
           f"{len(items)} topics in {len(CATS)} categories, {sum(x['study_hours'] for x in items):g} study hours. Generated by `scripts/content_backlog.py` from `content_backlog.csv`.",
           "Each topic is something to learn **and** to write content for (chapter, lab, drills, flashcards). `events` lists the milestones that draw on it; `score` = events + 2 per planned (priority yes) event.",
           "`basis`: **listed** = the organiser publishes the categories; **typical** = what that CTF series usually runs (confirm when its page is up).", "",
           "## By competition", ""]
    for ev in sorted(EVENTS, key=lambda e: ms[e]["start"]):
        basis, cats = EVENTS[ev]
        hrs = sum(x["study_hours"] for x in items if x["category"] in cats.split())
        out += [f"### {ev} {ms[ev]['event']} ({ms[ev]['start']}, {basis} categories)", "",
                f"Categories: {', '.join(CATS[c][0] for c in cats.split())}.  Study hours if you cover all: {hrs:g}.", ""]
    out += ["## By category", ""]
    for code, (name, content, topics) in sorted(CATS.items(), key=lambda kv: -len(need.get(kv[0], []))):
        evs = need.get(code, [])
        out += [f"### {code} {name}", "", f"Needed by {len(evs)} events: {', '.join(evs) or 'none yet'}. Content to make: {content}.", "",
                "| Id | Topic | Level | Hours | Scheduled week |", "|---|---|---|---:|---|"]
        for x in [i for i in items if i["category"] == code]:
            out.append(f"| {x['id']} | {x['topic']} | {x['level']} | {x['study_hours']} | {x['week'] or 'unscheduled'} |")
        out.append("")
    (T / "CONTENT-BACKLOG.md").write_text("\n".join(out), encoding="utf-8")
    print(f"{len(items)} items, {sum(x['study_hours'] for x in items):g} h, {sum(1 for x in items if x['week'])} scheduled, {len(CATS)} categories")


if __name__ == "__main__":
    main()
