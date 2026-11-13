"""Phone-first diagrams for modules 11-16 -> curriculum/modules/img/"""
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


# ---------------- 11 Scripting ----------------
chain("s-loop.svg", "The scripting loop", "automate only what you understand",
      ["Do it by hand once (so you know the steps)",
       "Write down input → transform → output",
       "Script the transform; test on a known example",
       "Run on the real data; print intermediate values",
       "Keep the script in your toolbox with a 1-line usage note"],
      "A script that you can't explain is a liability under time pressure.")

p = P("Talking to a service", "sockets and pwntools in one picture")
p.box("your script", "blue", weight="bold")
p.arrow("remote('host', 1337)")
p.box("service: banner, prompt, menu", "green")
p.arrow("recvuntil(b'> ')")
p.box("parse the prompt (regex / split)", "amber")
p.arrow("sendline(answer)")
p.box("repeat N rounds → flag", "red")
p.note("Always set a timeout and print what you received while developing.")
p.save(OUT, "s-service.svg")

chain("s-brute.svg", "Brute force without melting", "search-space thinking",
      ["Estimate the space: length × alphabet, or a wordlist",
       "Prune: known prefix, charset, constraints",
       "Parallelise only if it helps; keep it simple",
       "Stop at the first hit; log progress"],
      "10^4 is instant; 10^9 needs a smarter idea (oracle, meet-in-the-middle, GPU).")

p = P("Python modules to know cold", "CTF scripting toolbox")
p.row([("base64\nbinascii\nstruct", "blue"), ("hashlib\nhmac\nsecrets", "green")])
p.row([("requests\nsocket\nre", "amber"), ("itertools\ncollections\nsubprocess", "purple")])
p.row([("pwntools\nz3-solver\npycryptodome", "teal"), ("scapy\nPIL\nzipfile", "red")])
p.save(OUT, "s-toolbox.svg")

# ---------------- 12 OSINT ----------------
chain("o-method.svg", "OSINT method", "question first, sources second",
      ["Write the exact question and what a good answer looks like",
       "List what you already have (names, images, handles, places)",
       "Pivot: each new fact becomes a new search",
       "Verify with two independent sources",
       "Record the path; stop when the question is answered"],
      "Public information only. Never log in to, guess into, or attack anything.")

p = P("Geolocation clue ladder", "from a single photo")
for t, c in [("Text and language: signs, scripts, plates", "blue"), ("Infrastructure: road markings, poles, bollards", "green"),
             ("Nature: vegetation, terrain, sun and shadows", "amber"), ("Architecture and vehicles", "purple"),
             ("Landmarks: reverse image search, maps, street view", "teal"), ("Cross-check against time, season, direction", "red")]:
    p.box(t, c, size=13)
p.save(OUT, "o-geo.svg")

chain("o-domain.svg", "Investigating a domain", "all public sources",
      ["WHOIS / RDAP: registrar, dates, contacts (often redacted)",
       "DNS: A, MX, TXT, NS records; subdomains",
       "Certificate transparency (crt.sh): names issued for the domain",
       "Wayback Machine: old pages, removed files",
       "Search engines: dorks for exposed documents",
       "Metadata: exiftool on downloaded files"],
      "Example dork: site:example.com filetype:pdf")

p = P("OSINT ethics line", "where the line is")
p.box("OK: public posts, public records, maps, archives; for a defined, legitimate question", "green", size=13)
p.box("CAREFUL: private individuals, minors, medical or financial data; minimise and redact", "amber", size=13)
p.box("NO: hacking accounts, doxxing, stalking, social-engineering real people", "red", size=13)
p.note("CTF OSINT uses fictional or opt-in targets. Treat real people with care even then.")
p.save(OUT, "o-ethics.svg")

# ---------------- 13 Windows forensics ----------------
p = P("Windows artifact map", "what happened on this machine?")
p.box("EXECUTION: Prefetch · Amcache · ShimCache · UserAssist · BAM", "blue", size=12.5)
p.box("PERSISTENCE: Run keys · services · scheduled tasks · WMI · startup folder", "red", size=12.5)
p.box("USER ACTIVITY: Recent files · LNK · Jump Lists · browser history · Recycle Bin", "green", size=12.5)
p.box("FILE SYSTEM: $MFT · $UsnJrnl · timestamps · deleted files", "amber", size=12.5)
p.box("LOGS: Security · System · PowerShell · Sysmon · Task Scheduler", "purple", size=12.5)
p.box("NETWORK/ACCOUNTS: SAM · cached creds · RDP/WinRM events", "teal", size=12.5)
p.save(OUT, "wf-artifacts.svg")

p = P("Logon types", "Security event 4624 field 'Logon Type'")
for a, b, c in [("2", "Interactive: at the keyboard", "blue"), ("3", "Network: SMB shares, remote admin", "green"),
                ("4", "Batch: scheduled tasks", "amber"), ("5", "Service: service start", "purple"),
                ("7", "Unlock: workstation unlocked", "teal"), ("10", "RemoteInteractive: RDP", "red"),
                ("11", "CachedInteractive: offline domain logon", "gray")]:
    p.box(f"{a}   {b}", c, size=13)
p.note("Type 10 from an unexpected IP + 4672 (special privileges) is a classic intrusion pair.")
p.save(OUT, "wf-logon.svg")

chain("wf-timeline.svg", "Building a Windows timeline", "from artifacts to a story",
      ["Collect: $MFT, event logs, registry hives, Prefetch, browser DBs",
       "Normalise: one timezone (UTC), one format (CSV/Plaso)",
       "Anchor: pick a known event (alert time, first suspicious logon)",
       "Expand: what ran, what files, what network, what accounts",
       "Summarise: first access → persistence → impact"],
      "Tools: Eric Zimmerman suite, Plaso/log2timeline, Chainsaw/Hayabusa, Autopsy.")

# ---------------- 14 Cloud ----------------
chain("cl-iam.svg", "Cloud IAM in one line", "who may do what to which resource",
      ["PRINCIPAL: user, role, service account, application",
       "POLICY: allow/deny actions (read, write, delete, assume)",
       "RESOURCE: bucket, VM, database, secret, key",
       "CONDITION: from where, when, with MFA?"],
      "Over-broad policies (Action: *, Resource: *) are the most common finding.")

chain("cl-metadata.svg", "Why SSRF is worse in the cloud", "metadata service",
      ["App fetches attacker-chosen URL (SSRF)",
       "Request reaches 169.254.169.254 inside the VM",
       "Metadata returns temporary credentials for the VM's role",
       "Attacker uses them from outside, with that role's permissions"],
      "Defences: IMDSv2/session tokens, least-privilege roles, egress controls, input validation.")

p = P("Top cloud misconfigurations", "check these first in a review")
for t, c in [("Public storage buckets / containers", "red"), ("Over-privileged roles and wildcard policies", "amber"),
             ("Leaked access keys in repos or images", "purple"), ("No MFA on privileged accounts", "blue"),
             ("Open management ports to 0.0.0.0/0", "teal"), ("Logging off or not retained", "green")]:
    p.box(t, c, size=13)
p.save(OUT, "cl-misconfig.svg")

# ---------------- 15 Labs ----------------
p = P("A safe home lab", "keep attacks inside it")
p.box("Your laptop (host)", "gray", weight="bold")
p.arrow("VMware host-only / NAT")
p.row([("Kali (attacker)", "red"), ("Targets: Juice Shop, DVWA, VulnHub VMs", "green")])
p.row([("Windows Server AD lab", "blue"), ("Snapshots before every session", "amber")])
p.note("Never bridge vulnerable machines onto your home or school network.")
p.save(OUT, "lab-network.svg")

chain("lab-cycle.svg", "Lab cycle", "so you can break things and recover fast",
      ["Snapshot clean state", "Attack, take notes with commands", "Write the 5-line writeup",
       "Revert to snapshot", "Try again faster, or try a variation"])

# ---------------- 16 Review system ----------------
p = P("Leitner boxes", "spaced repetition on paper or in Anki")
p.box("Box 1: every day", "red", size=13)
p.box("Box 2: every 3 days", "amber", size=13)
p.box("Box 3: every week", "green", size=13)
p.box("Box 4: every 2 weeks", "blue", size=13)
p.box("Box 5: monthly → graduated", "purple", size=13)
p.note("Correct → move up a box. Wrong → back to box 1. 15 new cards/day is plenty.")
p.save(OUT, "rv-leitner.svg")

chain("rv-weekly.svg", "Weekly review loop", "Sunday, 45 minutes",
      ["Score: what did I finish? (tracker + minutes)",
       "Evidence: re-do 3 failed items without notes",
       "Weak spots: name the bottom two categories",
       "Plan: schedule next week's top three tasks",
       "Reflect: one thing to start, one to stop"])

print(len(list(OUT.glob("*.svg"))), "module SVGs ->", OUT)
