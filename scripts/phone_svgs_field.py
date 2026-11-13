"""Phone-first diagrams: cybersecurity field map + worked challenges -> curriculum/modules/img/"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phone_svg import P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "curriculum" / "modules" / "img"


def chain(name, title, sub, steps, note=""):
    p = P(title, sub)
    cols = ["blue", "green", "amber", "purple", "teal", "red"]
    for i, s in enumerate(steps):
        p.box(s, cols[i % len(cols)], size=13)
        if i < len(steps) - 1:
            p.arrow()
    if note:
        p.note(note)
    p.save(OUT, name)


# ---------------- Field map ----------------
p = P("The cybersecurity field", "five neighbourhoods, one shared foundation")
p.box("OFFENSE (find weaknesses)\npentest · red team · exploit research · bug bounty", "red", size=13)
p.box("DEFENSE (detect and respond)\nSOC · incident response · threat hunting · DFIR · threat intel", "blue", size=13)
p.box("ENGINEERING (build it secure)\nappsec · cloud security · network security · IAM · crypto/PKI", "green", size=13)
p.box("GOVERNANCE (decide and prove)\nrisk · compliance · privacy · audit · policy · awareness", "amber", size=13)
p.box("SPECIALIST\nmalware analysis · OT/ICS · mobile · IoT · hardware · AI security", "purple", size=13)
p.box("FOUNDATION: networking · operating systems · programming · crypto basics · writing", "gray", size=13, weight="bold")
p.save(OUT, "fm-map.svg")

p = P("CIA triad", "what security protects")
p.box("CONFIDENTIALITY\nonly the right people can read it\n(encryption, access control)", "blue", size=13)
p.box("INTEGRITY\nit has not been altered\n(hashes, signatures, change control)", "green", size=13)
p.box("AVAILABILITY\nit works when needed\n(backups, redundancy, DDoS defence)", "amber", size=13)
p.note("Every attack and every control maps back to one of these three.")
p.save(OUT, "fm-cia.svg")

chain("fm-lifecycle.svg", "Attack lifecycle (MITRE ATT&CK tactics)", "the attacker's to-do list, in rough order",
      ["Reconnaissance → Resource development",
       "Initial access (phish, exposed service, stolen creds)",
       "Execution → Persistence → Privilege escalation",
       "Defense evasion → Credential access → Discovery",
       "Lateral movement → Collection",
       "Command & control → Exfiltration → Impact"],
      "Defenders map detections to these tactics. CTF skills live mostly in the middle rows.")

chain("fm-ir.svg", "Incident response lifecycle", "NIST SP 800-61",
      ["1 PREPARE: tools, playbooks, logging, contacts",
       "2 DETECT & ANALYZE: alerts → triage → scope",
       "3 CONTAIN: isolate hosts, disable accounts",
       "4 ERADICATE & RECOVER: remove, rebuild, restore",
       "5 LEARN: post-incident review, fix the root cause"],
      "Loop back: lessons feed preparation.")

chain("fm-soc.svg", "Inside a SOC", "how an alert becomes a decision",
      ["Telemetry: endpoints (EDR), network, cloud, identity, email",
       "SIEM: collect, normalise, correlate, alert",
       "Tier 1: triage; true or false positive?",
       "Tier 2: investigate; scope; contain",
       "Tier 3 / IR / hunting: deep analysis, new detections",
       "Report, tune rules, close the loop"])

p = P("NIST CSF 2.0", "six functions every programme covers")
p.row([("GOVERN\nstrategy, roles, risk", "purple"), ("IDENTIFY\nassets, risks", "blue")])
p.row([("PROTECT\nsafeguards", "green"), ("DETECT\nfind events", "amber")])
p.row([("RESPOND\ncontain, communicate", "red"), ("RECOVER\nrestore, improve", "teal")])
p.note("A common language between security teams, executives and auditors.")
p.save(OUT, "fm-csf.svg")

p = P("Defence in depth", "no single control is enough")
for t, c in [("People: training, phishing resistance", "purple"), ("Policy: rules, access reviews", "amber"),
             ("Perimeter: firewall, WAF, email filter", "blue"), ("Network: segmentation, IDS/IPS", "green"),
             ("Host: patching, EDR, hardening", "teal"), ("Application: secure code, input validation", "red"),
             ("Data: encryption, backups, DLP", "gray")]:
    p.box(t, c, size=13)
p.save(OUT, "fm-depth.svg")

p = P("Risk in one picture", "likelihood × impact")
p.row([("low × low\naccept", "green"), ("med × low\nmonitor", "green"), ("high × low\nmitigate", "amber")])
p.row([("low × med\nmonitor", "green"), ("med × med\nmitigate", "amber"), ("high × med\nfix soon", "red")])
p.row([("low × high\nplan/insure", "amber"), ("med × high\nfix soon", "red"), ("high × high\nURGENT", "red")])
p.note("Treatments: avoid · reduce (mitigate) · transfer (insure) · accept.\nA vulnerability alone is not risk.")
p.save(OUT, "fm-risk.svg")

p = P("Cloud shared responsibility", "who secures what")
p.box("PROVIDER: physical, hardware, hypervisor, managed-service internals", "blue", size=13)
p.box("SHARED: identity, network config, patching (varies: IaaS/PaaS/SaaS)", "amber", size=13)
p.box("YOU: data, accounts and keys, configuration, access policies", "red", size=13)
p.note("Most cloud breaches are customer misconfigurations: public storage, over-broad IAM, leaked keys.")
p.save(OUT, "fm-cloud.svg")

chain("fm-appsec.svg", "Secure software lifecycle", "shift security left",
      ["Requirements: abuse cases, data classification",
       "Design: threat modelling (STRIDE), trust boundaries",
       "Build: secure coding, secrets management, SAST, dependency scanning",
       "Test: DAST, fuzzing, code review, pentest",
       "Release and run: logging, WAF, patching, incident response"])

p = P("Certification ladder", "check current requirements before booking")
p.box("START: Security+ · Network+ · CCNA (you are studying)", "green", size=13)
p.box("PRACTICAL ENTRY: eJPT · PNPT · BTL1 · CompTIA CySA+/PenTest+", "blue", size=13)
p.box("INTERMEDIATE: OSCP · GCIH · GCFA · cloud security (AWS/Azure)", "amber", size=13)
p.box("ADVANCED/MANAGEMENT: CISSP · CISM · OSEP · GXPN · CCSP", "purple", size=13)
p.note("Certs open doors; portfolios (labs, CTFs, writeups) prove skill. Employers at CyberSci watch both.")
p.save(OUT, "fm-certs.svg")

p = P("From CyberSci skills to jobs", "which CTF category feeds which role")
for a, b, c in [("Forensics + logs", "SOC analyst · DFIR · incident responder", "blue"),
                ("Web", "appsec engineer · pentester · bug bounty", "red"),
                ("Crypto", "security engineer · PKI · applied crypto", "green"),
                ("Reverse + pwn", "malware analyst · exploit dev · vuln research", "purple"),
                ("Network + AD", "internal pentester · red team · detection engineer", "amber"),
                ("Scripting + notes", "every role: automation and reporting", "gray")]:
    p.box(f"{a}  →  {b}", c, size=12.5)
p.save(OUT, "fm-career.svg")

p = P("OT/ICS in one picture", "the Purdue model, simplified")
for t, c in [("L5-4 enterprise IT: email, ERP", "blue"), ("L3.5 DMZ: buffer between IT and OT", "amber"),
             ("L3 site operations: historian, engineering workstation", "green"),
             ("L2 HMI/SCADA: operators watch and control", "teal"),
             ("L1 PLCs/controllers: run the process", "purple"), ("L0 sensors and actuators: pumps, valves, motors", "red")]:
    p.box(t, c, size=12.5)
p.note("Priorities flip: safety and availability first.")
p.save(OUT, "fm-ot.svg")

# ---------------- Worked challenges (explanations of public/archetype material) ----------------
chain("wc-onion.svg", "Layered encodings (the 'onion')", "warmup shape",
      ["Given a long string ending in = and made of letters/digits",
       "Looks like base64 → decode → only 0-9a-f",
       "Hex → bytes → English-like text with wrong letters",
       "ROT13 → readable flag"],
      "Each step is chosen by LOOKING at the output, not guessing.")

p = P("Oracle leak", "CyberSci 2022 'String Storage' shape")
p.box("Secret sits right after your data in memory", "gray", size=12.5)
p.box("search(prefix) answers FOUND / NOT FOUND\nbut compares one byte too many", "amber", size=12.5)
p.arrow()
p.box("guess the next character c: is prefix+c FOUND?", "blue", size=12.5)
p.arrow("repeat per position")
p.box("secret recovered one character at a time", "red", size=12.5)
p.note("Cost: length × alphabet size, not alphabet size to the power of length.")
p.save(OUT, "wc-oracle.svg")

chain("wc-vhost.svg", "Virtual hosts", "one IP, many websites",
      ["Browser asks the IP for 'warmup.example'",
       "Server picks the site by the Host header",
       "You send Host: internal.example instead",
       "The hidden site answers; flag is there"],
      "Clue source: names in the TLS certificate or page source.")

chain("wc-pcap-story.svg", "Reading a capture as a story", "turn packets into a timeline",
      ["00:01 DNS lookup: files.corp.test",
       "00:02 HTTP GET /tools/update.zip (200, 1.2 MB)",
       "00:09 FTP login as anonymous; STOR notes.txt",
       "00:14 DNS TXT queries with long random names",
       "Story: download → run → staging → covert channel"],
      "Question first, then the filter that answers it.")

chain("wc-chain.svg", "A multi-stage chain", "Nationals 2021 'Command and Control' shape",
      ["Recon: chatbot leaks hints → VPN credentials",
       "Scan: service with a known remote-code flaw",
       "Foothold: shell; find the C2 program",
       "Reverse: decompile the Python; see what the check does",
       "Crypto: sign the shutdown message with the found key",
       "Flag: the termination code"],
      "Real engagements look like this: small wins compounding.")

p = P("RSA with a tiny modulus", "why factoring breaks it")
p.box("n = 3233 (public)", "blue", mono=True)
p.arrow("factor (easy when small)")
p.box("p = 61 , q = 53", "green", mono=True)
p.arrow("φ = 60 × 52 = 3120")
p.box("d = 17⁻¹ mod 3120 = 2753", "amber", mono=True, size=12.5)
p.arrow("m = c^d mod n")
p.box("2790^2753 mod 3233 = 65 → 'A'", "red", mono=True, size=12.5)
p.save(OUT, "wc-rsa-small.svg")

p = P("Whitespace binary", "two symbols, eight bits per letter")
p.box("space = 0   tab = 1", "gray", size=13)
p.box("01000011 → 67 → 'C'", "blue", mono=True)
p.box("01010100 → 84 → 'T'", "green", mono=True)
p.box("01000110 → 70 → 'F'", "amber", mono=True)
p.note("Tell-tale: only two distinct byte values (0x20, 0x09).\nxxd -p f | fold -w2 | sort | uniq -c")
p.save(OUT, "wc-whitespace.svg")

p = P("The writeup template", "write it so future-you can reuse it")
for t, c in [("1 Title · category · points · time spent", "gray"), ("2 What I was given", "blue"),
             ("3 First observation (the thing that mattered)", "green"), ("4 Steps with exact commands", "amber"),
             ("5 Why it works (one paragraph)", "purple"), ("6 Mistakes and dead ends", "red"),
             ("7 How I'd spot this again", "teal")]:
    p.box(t, c, size=13)
p.save(OUT, "wc-template.svg")

p = P("Mock exam time budget", "60 minutes, no notes")
p.box("A  Quick recall: 20 questions, 1 point each\n10 minutes", "blue", size=13)
p.box("B  Read the evidence: 10 questions, 3 points each\n20 minutes", "green", size=13)
p.box("C  Decode and calculate: 6 questions, 5 points each\n20 minutes", "amber", size=13)
p.box("D  Judgement: 4 questions, 5 points each\n10 minutes", "purple", size=13)
p.note("Total 100 points. Use the 30-minute rule inside the exam too: skip and return.")
p.save(OUT, "wc-mock-plan.svg")

p = P("What your score means", "and what to do next")
p.box("85-100  Competition-ready: keep timing yourself and rehearse team roles", "green", size=13)
p.box("70-84  Solid: patch the two weakest categories this week", "teal", size=13)
p.box("50-69  Developing: redo the modules for every category you missed", "amber", size=13)
p.box("under 50  Foundation first: Bandit 0-20, module 1, cheat sheets, then retake", "red", size=13)
p.note("Retake after 3 days with the answer key closed; track the delta, not just the score.")
p.save(OUT, "wc-score-bands.svg")

print(len(list(OUT.glob("*.svg"))), "module SVGs ->", OUT)
