"""Phone-first diagrams for curriculum/modules/ -> curriculum/modules/img/"""
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


# ---------------- Method / competition day ----------------
chain("m1-triage-loop.svg", "The CTF loop", "use it on every challenge",
      ["1 OBSERVE\nwhat exactly was given? run file / strings / curl -i / nmap",
       "2 CLASSIFY\ncategory + likely technique in one sentence",
       "3 HYPOTHESIZE\nup to 3 causes, ranked",
       "4 SMALLEST TEST\none cheap command that separates them",
       "5 VERIFY\nconfirm flag format; test independently",
       "6 RECORD\n5-line writeup: what, first observation, technique, tool, mistake"],
      "Stuck for 30 minutes? Swap or ask. Note where you gave up.")

p = P("The 30-minute rule", "time-box every challenge")
p.box("0-10 min   read ALL challenge titles; rank points ÷ estimated minutes", "blue", size=13)
p.box("10-40 min  attack the best ratio; solo", "green", size=13)
p.box("40 min     STOP: write what you know, hand off or switch", "amber", size=13)
p.box("Every hour  look at the scoreboard; re-rank", "purple", size=13)
p.note("Warmups are cheap points: clear them first (the 2022 regionals had ~9 of them, down to 1-5 points each).")
p.save(OUT, "m1-time-box.svg")

p = P("CyberSci regional day", "shape of the day (confirm times with organizers)")
p.box("MORNING  hacking: jeopardy-style, realistic IT environment", "blue", size=13.5)
p.box("MIDDAY  transition (exact times unconfirmed)", "gray", size=13.5)
p.box("AFTERNOON  employer interviews: bring resumes", "green", size=13.5)
p.box("LATER  results; some offers same day (per cybersci.ca)", "amber", size=13.5)
p.note("Regionals: Nov 21, 2026, 6-7 sites across Canada.  Winner per region → Nationals (Ottawa, summer).")
p.save(OUT, "m1-competition-day.svg")

p = P("Team board", "who is doing what")
p.row([("UNSOLVED\nweb-3 (200)\nrev-2 (150)", "gray"), ("IN PROGRESS\nforensics-1\n(Sam, 20 min)", "amber")])
p.row([("BLOCKED\npwn-1 needs\nlibc version", "red"), ("SOLVED\nwarmup-1,2\ncrypto-1", "green")])
p.note("One person owns submissions. Write the owner and start time on every card.")
p.save(OUT, "m1-team-board.svg")

# ---------------- Forensics ----------------
chain("f-triage.svg", "Unknown file triage", "do this before anything clever",
      ["file X\nwhat kind of thing is it?",
       "strings X | head\nreadable text? URLs? flags?",
       "xxd X | head\nmagic bytes: 1f8b gzip, 504b zip, 7f45 ELF",
       "exiftool X\nmetadata: author, GPS, comments",
       "binwalk X\nanything embedded or appended?",
       "pick the specialist tool: pcap, memory, image, archive"])

p = P("Packet capture workflow", "Wireshark / tshark")
p.box("1. Statistics → Protocol Hierarchy\nwhat protocols exist?", "blue")
p.arrow()
p.box("2. Statistics → Conversations\nwho talks to whom, how much?", "green")
p.arrow()
p.box("3. Filter: http, dns, ftp, tcp.stream eq 5\nfollow TCP stream", "amber")
p.arrow()
p.box("4. Export Objects → HTTP/SMB\nfiles that crossed the wire", "purple")
p.arrow()
p.box("5. Look for creds, flags, odd DNS, big uploads", "red")
p.note("tshark -r f.pcap -q -z io,phs   (hierarchy)\ntshark -r f.pcap -Y http.request -T fields -e http.host -e http.request.uri", mono=True, size=11)
p.save(OUT, "f-pcap.svg")

p = P("Encapsulation", "what is inside a packet")
p.box("Ethernet frame  (MAC addresses)", "gray")
p.box("IP packet  (source/dest IP, TTL)", "blue")
p.box("TCP segment  (ports, flags SYN/ACK, seq)", "green")
p.box("Application data  (HTTP, DNS, FTP, TLS…)", "amber")
p.note("Filters read layers: ip.addr==10.0.0.5  tcp.port==80  http.host contains \"corp\"")
p.save(OUT, "f-layers.svg")

chain("f-volatility.svg", "Memory forensics with Volatility 3", "a RAM image is a snapshot of a running system",
      ["info\nwhich OS/build?   vol -f mem.raw windows.info",
       "windows.pslist / psscan\nprocesses (psscan finds hidden ones)",
       "windows.pstree\nparent/child: who spawned cmd.exe?",
       "windows.netscan\nconnections: which process talks where?",
       "windows.cmdline / windows.filescan\nwhat ran, which files were open",
       "windows.dumpfiles / memmap\npull the artefact out"],
      "Suspicious: powershell child of winword, svchost with no parent, odd ports.")

p = P("Reading a log line", "auth.log / web access log")
p.box("Oct 14 03:12:07 srv sshd[812]: Failed password for root from 203.0.113.9 port 51422", "white", mono=True, size=11.5)
p.row([("time", "blue"), ("host", "green"), ("process", "amber")])
p.row([("event", "purple"), ("user", "red"), ("source IP", "teal")])
p.note("Method: grep an indicator → sort by time → build a timeline → find first/last event.\nsort | uniq -c | sort -rn  finds the noisiest source.")
p.save(OUT, "f-logs.svg")

chain("f-stego.svg", "Hidden data in images", "check cheap things first",
      ["exiftool / strings\ncomments, URLs, base64",
       "binwalk / foremost\nappended zip or file inside",
       "file + xxd tail\ndata after the image end marker",
       "zsteg (PNG) / steghide (JPG)\nLSB and password-protected payloads",
       "stegsolve / view colour planes\nvisual patterns",
       "audio? spectrogram (Audacity)"])

# ---------------- Web ----------------
p = P("HTTP request and response", "know both halves")
p.box("GET /search?q=cat HTTP/1.1\nHost: shop.example\nCookie: session=abc123\nUser-Agent: …", "blue", mono=True, size=11.5, sub="REQUEST: method, path, headers, body")
p.arrow()
p.box("HTTP/1.1 200 OK\nSet-Cookie: session=…\nContent-Type: text/html\n\n<html>…</html>", "green", mono=True, size=11.5, sub="RESPONSE: status, headers, body")
p.note("Everything the browser sends is attacker-controlled: path, query, headers, cookies, body.")
p.save(OUT, "w-http.svg")

p = P("SQL injection", "your input becomes part of the query")
p.box("SELECT * FROM users\nWHERE name = '<INPUT>'", "blue", mono=True)
p.arrow("input:  ' OR 1=1 --")
p.box("SELECT * FROM users\nWHERE name = '' OR 1=1 --'", "red", mono=True)
p.note("1=1 is always true; -- comments out the rest → all rows returned.")
p.box("UNION: ' UNION SELECT username,password FROM users --", "amber", mono=True, size=11.5)
p.note("Steps: find the injection → count columns (ORDER BY n) → find text column → read tables (information_schema).")
p.save(OUT, "w-sqli.svg")

p = P("Three kinds of XSS", "script runs in someone else's browser")
p.box("REFLECTED  payload in the URL/request is echoed back immediately", "amber", size=13)
p.box("STORED  payload saved by the server (comment, profile), hits every viewer", "red", size=13)
p.box("DOM  client-side JS writes your input into the page unsafely", "purple", size=13)
p.note("Test: <script>alert(1)</script>, \"><svg onload=alert(1)>, then adapt to the context (HTML, attribute, JS string).\nGoal in CTFs: steal a cookie or call an admin-only endpoint.")
p.save(OUT, "w-xss.svg")

p = P("Sessions and JWT", "who are you, according to the server?")
p.box("Cookie: session=abc123\nserver looks it up in its store", "blue", mono=True, size=12.5)
p.gap(6)
p.box("JWT = header . payload . signature\n(three base64url parts)", "green", mono=True, size=12.5)
p.row([("header\nalg: HS256", "amber"), ("payload\nuser, role, exp", "purple"), ("signature\nHMAC(secret)", "red")])
p.note("Attacks: alg:none, weak secret (hashcat -m 16500), change role in payload if signature isn't checked, kid injection.")
p.save(OUT, "w-jwt.svg")

chain("w-ssrf.svg", "SSRF", "make the server fetch URLs for you",
      ["You submit url=http://127.0.0.1:8080/admin",
       "App server fetches it from INSIDE the network",
       "Internal service trusts the request (it came from localhost)",
       "Response is returned to you: admin page, metadata, files"],
      "Targets: 127.0.0.1, 169.254.169.254 (cloud metadata), internal hostnames, file://")

p = P("IDOR / broken access control", "the id is just a number")
p.box("GET /invoice?id=1001\n(your invoice)", "green", mono=True)
p.arrow("change id")
p.box("GET /invoice?id=1002\n(someone else's invoice)", "red", mono=True)
p.note("Test every id in URLs, JSON bodies and cookies. Try other methods (PUT/DELETE) and other roles.")
p.save(OUT, "w-idor.svg")

chain("w-method.svg", "Web challenge method", "map first, exploit second",
      ["MAP: pages, params, forms, cookies, JS files, robots.txt",
       "INPUTS: for each one, what does the server do with it?",
       "TEST classes: SQLi, XSS, LFI/path, command inj, SSTI, IDOR, auth",
       "EXPLOIT the smallest working proof; then escalate",
       "CHAIN: low-severity bugs combine (SSRF → internal admin → file read)"],
      "Tools: browser devtools, curl -i, Burp, ffuf, sqlmap (after manual).")

# ---------------- Crypto ----------------
p = P("Symmetric vs asymmetric", "")
p.row([("SYMMETRIC\none shared key\nAES, ChaCha20\nfast, bulk data", "blue"), ("ASYMMETRIC\npublic + private\nRSA, ECC\nkeys, signatures", "purple")])
p.note("Real protocols (TLS) use asymmetric to agree a key, then symmetric for the data.")
p.box("Encoding ≠ encryption: base64, hex, URL-encoding have no key.", "amber", size=13)
p.save(OUT, "c-sym-asym.svg")

p = P("XOR in four lines", "the most common CTF primitive")
p.box("plaintext  XOR  key  =  ciphertext", "blue", mono=True)
p.box("ciphertext XOR  key  =  plaintext", "green", mono=True)
p.box("ciphertext XOR plaintext = key   (known-plaintext attack)", "amber", mono=True, size=12)
p.note("Single-byte key: try all 256, score by English letters.\nRepeating key: find key length (Hamming distance), then solve each column.\nFlag format known (e.g. CTF{...}) → recover key bytes from the first characters.")
p.save(OUT, "c-xor.svg")

p = P("RSA at a glance", "know the parts, then the attacks")
p.box("n = p × q   (public)\ne = 65537  (public)\nd = e⁻¹ mod φ(n)  (private)", "blue", mono=True, size=12.5)
p.box("encrypt: c = mᵉ mod n\ndecrypt: m = cᵈ mod n", "green", mono=True, size=12.5)
p.note("Attack decision:")
p.box("n small / factorable → factordb, yafu", "amber", size=12.5)
p.box("e tiny (3) and m small → c is just mᵉ: take the e-th root", "amber", size=12.5)
p.box("same n, two e → common modulus", "amber", size=12.5)
p.box("d small → Wiener; p≈q → Fermat; shared prime across keys → gcd", "amber", size=12.5)
p.save(OUT, "c-rsa.svg")

p = P("AES modes", "why ECB leaks")
p.box("ECB: each 16-byte block encrypted independently\nsame plaintext block → same ciphertext block", "red", size=12.5)
p.row([("P1 P2 P1", "gray"), ("C1 C2 C1\n(repeat visible)", "red")])
p.box("CBC: each block XORed with the previous ciphertext\nflip a bit in C(n-1) → flips the same bit in P(n)", "green", size=12.5)
p.note("Tell-tale: repeated 16-byte blocks in ciphertext → ECB.\nPadding oracle: server says valid/invalid padding → decrypt byte by byte.")
p.save(OUT, "c-aes-modes.svg")

p = P("Hashes", "one-way, fixed size")
p.box("md5 32 hex · sha1 40 hex · sha256 64 hex", "blue", mono=True, size=12)
p.box("Same input → same hash. Tiny change → totally different hash.", "gray", size=12.5)
p.box("Crack: hashcat / john + wordlist + rules", "amber", size=12.5)
p.box("Length extension: H(secret‖msg) lets you append data (md5/sha1/sha256, not HMAC)", "red", size=12.5)
p.note("Identify: hashid, hash-identifier, length + charset. Salted hashes: unique per user, same wordlist but slower.")
p.save(OUT, "c-hash.svg")

chain("c-recognize.svg", "What is this string?", "recognition cheat flow",
      ["Only A-Z a-z 0-9 + / and ends with =  →  base64",
       "Only 0-9 a-f, even length  →  hex  (xxd -r -p)",
       "Looks like English with wrong letters  →  ROT13 / Caesar",
       "Starts eyJ…  →  JWT (base64url JSON)",
       "32/40/64 hex characters  →  md5 / sha1 / sha256 hash",
       "Starts 1f8b / 504b / 425a  →  gzip / zip / bzip2 file"])

# ---------------- Reverse / pwn ----------------
chain("r-compile.svg", "From source to running process", "what you are reversing",
      ["source.c   human-readable",
       "assembly   mov, add, call, jmp",
       "object .o   machine code + symbols",
       "linked ELF   libraries + entry point _start",
       "process   code, heap, stack in memory"],
      "Reverse engineering walks this chain backwards: bytes → assembly → pseudo-C (Ghidra).")

p = P("The stack", "why buffer overflows work")
p.box("high addresses", "gray", size=12)
p.box("return address\n(where the function goes back to)", "red", size=12.5)
p.box("saved rbp", "amber", size=12.5)
p.box("char buf[64]\n(your input is copied here)", "blue", size=12.5)
p.box("low addresses", "gray", size=12)
p.note("Writing more than 64 bytes grows UPWARD and overwrites saved rbp, then the return address. You choose where the function returns.")
p.save(OUT, "r-stack.svg")

p = P("ret2win", "the simplest exploit")
p.box("normal:  main → vuln() → returns to main", "green", size=13)
p.box("attack:  input = 'A'×offset + address_of(win)", "red", size=13, mono=True)
p.box("vuln() returns → jumps to win() → prints the flag", "amber", size=13)
p.note("Steps: checksec → find offset (cyclic pattern) → find win address → send payload with pwntools.")
p.save(OUT, "r-ret2win.svg")

p = P("Binary protections", "checksec tells you")
for n, d, c in [("NX", "stack not executable → no shellcode on stack (use ROP)", "blue"),
                ("Stack canary", "random value before return address → leak or avoid overwriting it", "green"),
                ("ASLR", "libraries/stack at random addresses → need an info leak", "amber"),
                ("PIE", "program itself at random base → leak a code pointer", "purple"),
                ("RELRO", "Full RELRO: GOT read-only → no GOT overwrite", "red")]:
    p.box(f"{n}: {d}", c, size=12.5)
p.save(OUT, "r-protections.svg")

chain("r-ghidra.svg", "Ghidra workflow", "static analysis first",
      ["Import binary; auto-analyze",
       "Symbol tree → main (or entry → __libc_start_main)",
       "Read decompiler; rename variables; retype",
       "Strings window + xrefs: who uses 'Correct!'",
       "Hypothesis → confirm with gdb breakpoints / ltrace",
       "Re-implement the check in Python (or use z3)"])

# ---------------- Privesc / AD ----------------
chain("p-linux-privesc.svg", "Linux privilege escalation checklist", "first 60 seconds in a shell",
      ["id; sudo -l   what may I run as root?",
       "find / -perm -4000 2>/dev/null   setuid binaries → GTFOBins",
       "cat /etc/crontab; ls /etc/cron.d   writable scripts?",
       "ls -la ~ ; history; .ssh; env   credentials lying around",
       "ss -tlnp   local-only services",
       "uname -a; linpeas.sh   kernel/known vulns (last)"])

p = P("Kerberos in one picture", "Active Directory authentication")
p.box("1  AS-REQ → KDC (domain controller)\n    you prove identity → get a TGT", "blue", size=12.5)
p.box("2  TGS-REQ with TGT → KDC\n    ask for a ticket for a service (SPN)", "green", size=12.5)
p.box("3  present service ticket → the service\n    it decrypts with ITS account's key", "amber", size=12.5)
p.note("Kerberoasting: any user can request tickets for SPNs; the ticket is encrypted with the service account password → crack offline.\nAS-REP roasting: accounts without pre-auth leak a crackable blob.")
p.save(OUT, "p-kerberos.svg")

chain("p-ad-path.svg", "A typical AD attack path", "you are a low-privileged domain user",
      ["Enumerate: users, groups, SPNs, shares (BloodHound, NetExec)",
       "Roast: Kerberoast / AS-REP → crack passwords",
       "Move: reuse creds; SMB/WinRM; pass-the-hash",
       "Escalate: ACL abuse, delegation, local admin → DA path",
       "Persist/prove: dump with DCSync (lab), read flag"],
      "Always map first: BloodHound shows the shortest path.")

# ---------------- Reference graphics ----------------
p = P("Ports to know", "service → default port")
for row in [("21 ftp · 22 ssh · 23 telnet", "blue"),
            ("25 smtp · 53 dns · 80 http · 443 https", "green"),
            ("88 kerberos · 135 rpc · 139/445 smb", "amber"),
            ("389 ldap · 636 ldaps · 3268 global catalog", "purple"),
            ("1433 mssql · 3306 mysql · 5432 postgres", "teal"),
            ("3389 rdp · 5985/5986 winrm · 6379 redis", "red"),
            ("8080/8443 web alt · 2049 nfs · 161 snmp(udp)", "gray")]:
    p.box(row[0], row[1], size=13, mono=True)
p.save(OUT, "k-ports.svg")

p = P("File magic bytes", "first bytes identify the format")
for a, b, c in [("1f 8b", "gzip", "blue"), ("42 5a 68  (BZh)", "bzip2", "green"),
                ("50 4b 03 04", "zip / docx / jar / apk", "amber"),
                ("7f 45 4c 46  (ELF)", "Linux executable", "purple"),
                ("4d 5a  (MZ)", "Windows PE (exe/dll)", "red"),
                ("89 50 4e 47", "PNG image", "teal"),
                ("ff d8 ff", "JPEG image", "gray"),
                ("25 50 44 46  (%PDF)", "PDF", "blue"),
                ("75 73 74 61 72  (ustar)", "tar at offset 257", "green")]:
    p.box(f"{a}  →  {b}", c, size=12.5, mono=True, gap=6)
p.save(OUT, "k-magic.svg")

print(len(list(OUT.glob("*.svg"))), "module SVGs ->", OUT)
