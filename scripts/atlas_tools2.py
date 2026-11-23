"""Second batch of Command Atlas definitions: python one-liners and readelf/objdump (captured here),
nmap, tcpdump, gdb, sqlite3 (written now, captured when run on a machine that has them, e.g. Kali)."""

TOOLS2 = []

TOOLS2.append(dict(
    name="python-oneliners", needs="python3", version="python3 --version",
    one_line="Use `python3 -c` for the small decode, convert and brute-force jobs that come up in every CTF.",
    when=["Decode or encode base64, hex, URL or binary text.", "Convert between number bases and byte orders.", "XOR, hash, brute-force a short secret, or work out tiny RSA.", "Parse a log with Counter instead of building a long shell pipeline."],
    anatomy="""python3  -c  "import base64; print(base64.b64decode('aGk=').decode())"
   |      |        |
   |      |        '--- a program in one string: statements separated by ;
   |      '--- -c = run the string as code (use -m for a module, - to read a script from stdin)
   '--- the interpreter""",
    flags=[("-c 'code'", "Run code given on the command line", "Quick transforms"),
           ("-m http.server 8000", "Run a module: a quick web server for transfers", "Serve files in a lab"),
           ("-i", "Stay interactive afterwards", "Explore the data you loaded"),
           ("-", "Read the script from stdin", "Here-documents with `<<'PY'`"),
           ("-I", "Isolated mode: ignore the current folder and user site", "Safe use inside an untrusted folder"),
           ("-u", "Unbuffered output", "Network scripts and pipes"),
           ("bytes.fromhex(s) / b.hex()", "Hex string to bytes and back", "Decode hex"),
           ("int(x, base) / bin() / hex() / oct()", "Convert between bases", "Binary, hex, octal puzzles"),
           ("struct.pack('<I', n)", "Pack a number as little-endian bytes (`>` = big-endian)", "Build payloads; read binary fields"),
           ("pow(a, -1, m)", "Modular inverse", "RSA private exponent"),
           ("itertools.product", "Every combination of a character set", "Short brute force")],
    recipes=[
     dict(title="Decode base64", cmd="python3 -c \"import base64; print(base64.b64decode('aGVsbG8gd29ybGQ=').decode())\"",
          why="Base64 turns bytes into text with `A-Z a-z 0-9 + /` and `=` padding. `b64decode` returns bytes; `.decode()` makes text.",
          read="You get `hello world`. If decoding fails, check for missing `=` padding, newlines or URL-safe `-_` characters."),
     dict(title="Hex and bytes", cmd="python3 -c \"print(bytes.fromhex('666c61677b6865787d')); print('flag'.encode().hex())\"",
          why="Two directions: hex text to bytes, and text to hex.",
          read="The first line is a `bytes` object (note the `b'...'`), the second the hex of the word `flag`."),
     dict(title="XOR with a repeating key", cmd="python3 -c \"d=bytes.fromhex('0b0d080c'); k=b'AB'; print(bytes(b ^ k[i % len(k)] for i, b in enumerate(d)))\"",
          why="`i % len(k)` repeats the key. XOR is its own inverse, so the same code encrypts and decrypts.",
          read="The result is readable text. In Natas 11 you recover the key the same way: key = ciphertext XOR known plaintext."),
     dict(title="Number bases", cmd="python3 -c \"n=0xdeadbeef; print(n); print(bin(10), oct(64), hex(255)); print(int('777', 8), int('1010', 2), int('ff', 16))\"",
          why="`int(text, base)` parses; `bin`, `oct`, `hex` format.",
          read="Decimal for the hex value, then conversions both ways. Handy for the picoCTF 'convertme' style tasks."),
     dict(title="Byte order (endianness)", cmd="python3 -c \"import struct; print(struct.pack('<I', 0xdeadbeef).hex(), struct.pack('>I', 0xdeadbeef).hex()); print(hex(struct.unpack('<I', bytes.fromhex('efbeadde'))[0]))\"",
          why="`<` = little-endian (x86), `>` = big-endian (network). `I` = 4-byte unsigned.",
          read="The same number gives two byte orders. This is the `ef be ad de` you typed in Narnia 0."),
     dict(title="Brute-force a short secret from its hash", cmd="python3 -c \"import hashlib, itertools; t = hashlib.md5(b'4821').hexdigest(); print(t); print(next(''.join(c) for c in itertools.product('0123456789', repeat=4) if hashlib.md5(''.join(c).encode()).hexdigest() == t))\"",
          why="Only 10,000 four-digit PINs exist, so trying them all is instant. Cost grows as alphabet^length.",
          read="It prints the hash and then recovers `4821`. Real password cracking uses hashcat or john, but the idea is the same."),
     dict(title="Count things in a log", cmd="python3 -c \"import collections; print(collections.Counter(l.split()[0] for l in open('access.log')).most_common(2))\"",
          why="`Counter` is awk's associative array with sorting built in.",
          read="The two busiest IPs with their counts."),
     dict(title="Tiny RSA", cmd="python3 -c \"p, q, e = 61, 53, 17; n = p * q; d = pow(e, -1, (p - 1) * (q - 1)); m = 65; c = pow(m, e, n); print(n, d, c, pow(c, d, n))\"",
          why="With the factors p and q you can compute the private exponent d. `pow(c, d, n)` decrypts.",
          read="`n=3233`, `d=2753`, a ciphertext, and the original message 65 again. CTF RSA tasks give you weak numbers where you must find p and q.")],
    gotchas=["Quote carefully: wrap the program in double quotes in bash and use single quotes inside (or the other way round).",
             "`print(bytes)` shows `b'...'`: call `.decode()` for text.", "Python 2 is gone: `print` needs parentheses.",
             "Integer division is `//`; `/` gives a float, which breaks big-number maths.", "For anything longer than three lines, write a file and add comments."],
    related=["CyberChef", "xxd", "base64", "pwntools", "pycryptodome", "sympy", "z3"],
    practice=["Decode a base64 string, then hex-decode the result.", "XOR two hex strings of equal length.", "Find the PIN whose sha1 equals a hash of your choice."],
    cards=["What does `python3 -c` do?", "What does `<I` mean in struct?", "How do you invert a number modulo m in Python?", "Why is XOR with a repeating key breakable?"]))

TOOLS2.append(dict(
    name="readelf-objdump", needs="readelf", version="readelf --version | head -1; objdump --version | head -1",
    one_line="Read a Linux program without running it: headers, symbols, sections, protections and disassembly.",
    when=["First look at a binary challenge: architecture, symbols, protections.", "Find the function that checks the password and read its assembly.", "See which strings and constants are stored in the file."],
    anatomy="""readelf  -h  hello           # ELF header: class (32/64-bit), machine, entry point
readelf  -s  hello           # symbol table: function and variable names
readelf  -lW hello           # program headers: look for GNU_STACK (executable stack?)
objdump  -d -M intel hello   # disassemble code, Intel syntax
objdump  -s -j .rodata hello # hex dump of one section""",
    flags=[("readelf -h", "ELF header", "32-bit or 64-bit? which CPU?"),
           ("readelf -S / -lW", "Section headers / program headers (wide)", "Stack flags, section layout"),
           ("readelf -s", "Symbols", "Function names in a non-stripped binary"),
           ("readelf -p .rodata", "Print a section as strings", "Constants and messages"),
           ("objdump -d", "Disassemble executable sections", "Read the logic"),
           ("-M intel", "Intel syntax instead of AT&T", "Easier to read, matches most tutorials"),
           ("--no-show-raw-insn", "Hide the machine-code bytes", "Shorter output"),
           ("objdump -s -j SECTION", "Hex dump of a section", "Data tables, embedded text"),
           ("nm / file / strings", "Related quick checks", "Symbols, type, text")],
    recipes=[
     dict(title="What kind of program is it?", cmd="readelf -h hello | grep -E 'Class|Machine|Type|Entry'",
          why="The ELF header tells you the word size, CPU, and whether the program is position independent.",
          read="64-bit x86-64 and a position-independent executable (type `DYN`). This decides which debugger setup and which addresses to expect."),
     dict(title="Which functions does it have or use?", cmd="readelf -s hello | grep -E ' main$| puts| strcmp'",
          why="Symbols list what the program defines (`main`) and imports from libc (`puts`, `strcmp`).",
          read="Seeing `strcmp` hints at a password comparison. A stripped binary has no names, so this shows less."),
     dict(title="Is the stack executable?", cmd="readelf -lW hello | grep -E 'GNU_STACK|GNU_RELRO'",
          why="`GNU_STACK` flags `RW` mean a non-executable stack (NX). `RWE` would allow shellcode on the stack, as in Narnia.",
          read="The stack segment is read-write only, which is the modern default. Narnia's binaries differ."),
     dict(title="Read the strings the program stores", cmd="readelf -p .rodata hello",
          why="`.rodata` holds constants such as string literals.",
          read="The secret passphrase, the denied message and the flag text, all visible without running anything."),
     dict(title="Disassemble main", cmd="objdump -d -M intel --no-show-raw-insn hello | sed -n '/<main>:/,/ret/p'",
          why="`-d` disassembles; `sed -n '/start/,/end/p'` prints just one function.",
          read="Look for `cmp`/`call strcmp` followed by a conditional jump (`je`/`jne`): that branch decides whether you get the secret. The `lea` instructions load the string addresses you saw in `.rodata`."),
     dict(title="Hex dump of a section", cmd="objdump -s -j .rodata hello",
          why="`-s` prints a section as hex and ASCII, so you can check offsets and hidden bytes.",
          read="The same constants in hex form with their addresses.")],
    gotchas=["Stripped binaries have no function names: you will see `sub_...` in decompilers and unnamed code here.",
             "AT&T syntax (the default) puts source before destination; add `-M intel` for the order most books use.",
             "PIE binaries show small addresses until loaded; the real addresses change each run unless ASLR is off.",
             "`objdump` shows what is in the file, not what a packed or obfuscated program does after it unpacks itself."],
    related=["ghidra", "gdb", "radare2 / cutter", "ltrace", "strace", "checksec", "nm", "strings"],
    practice=["Find the address of the string `access denied` and the instruction that loads it.", "Compile `hello.c` with `-no-pie -fno-stack-protector -z execstack` and compare the `GNU_STACK` line.", "Work out which register holds `argv[1]` at the `strcmp` call."],
    cards=["What does `readelf -h` tell you?", "What does `GNU_STACK RWE` mean?", "What does `-M intel` change?", "Where are string literals stored in an ELF file?"]))

TOOLS2.append(dict(
    name="nmap", needs="nmap", version="nmap --version | head -1",
    one_line="Discover hosts, open ports, services and versions on a network, and run scripts against them.",
    when=["The first command on any network challenge or lab machine.", "Find out which services run and which versions.", "Check what a firewall allows (open versus filtered)."],
    anatomy="""nmap  -sV  -sC  -p 22,80,443  -oA scan1  127.0.0.1
 |     |    |     |            |           '--- target: IP, name, CIDR (10.0.0.0/24), range, or -iL file
 |     |    |     |            '--- save in all formats (scan1.nmap/.xml/.gnmap)
 |     |    |     '--- ports (use -p- for all 65,535)
 |     |    '--- default NSE scripts
 |     '--- probe open ports for service and version
 '--- the program""",
    flags=[("-sn", "Host discovery only (ping sweep)", "Who is up on this subnet?"),
           ("-Pn", "Skip discovery, treat host as up", "ICMP blocked or crossing a firewall"),
           ("-p- / -p 1-1024 / --top-ports N", "Which ports to scan", "All ports first, then focus"),
           ("-sS / -sT / -sU", "SYN scan (root) / TCP connect / UDP", "Default, no-root or proxy use, UDP services"),
           ("-sV", "Service and version detection", "After you know the open ports"),
           ("-sC / --script NAME", "Default scripts / a chosen script", "Enumerate and check known issues"),
           ("-O / -A", "OS guess / aggressive (-sV -sC -O --traceroute)", "Quick profile of a lab box"),
           ("-T0..T5", "Timing template", "T4 in labs, slower on fragile or monitored networks"),
           ("-oA name / -oN / -oX", "Save output", "Always save"),
           ("--open / -v", "Show only open ports / more detail", "Cleaner output"),
           ("--script-help NAME", "Read what a script does", "Before running unfamiliar scripts")],
    recipes=[
     dict(title="Is the host up?", cmd="nmap -sn 127.0.0.1", expect="Starting Nmap ... Nmap scan report for localhost (127.0.0.1) / Host is up / Nmap done: 1 IP address (1 host up) scanned.",
          why="`-sn` does discovery without scanning ports.", read="One host up. On a LAN you would pass a CIDR such as `192.168.1.0/24`."),
     dict(title="Default scan of localhost", cmd="nmap 127.0.0.1", expect="A PORT STATE SERVICE table listing the open TCP ports among the top 1000 (for example 22/tcp ssh if sshd runs), and the number of closed ports not shown.",
          why="With no options Nmap scans the 1000 most common TCP ports.", read="Read the three columns: port/protocol, state (open, closed, filtered) and the service name guessed from the port number."),
     dict(title="Every port, then look closely", cmd="nmap -p- -T4 127.0.0.1 && nmap -sV -sC -p 22 127.0.0.1", expect="First scan: the list of all open ports. Second scan: the same port with a version string (for example OpenSSH 9.x) and script output such as host keys.",
          why="The CTF default: find all ports quickly, then spend time only on the open ones.", read="`-sV` replaces the guessed service name with a detected version; scripts add facts such as SSH host key fingerprints or web page titles."),
     dict(title="Save results", cmd="nmap -oA scan1 127.0.0.1 && ls scan1.*", expect="scan1.gnmap scan1.nmap scan1.xml",
          why="`-oA` writes three formats at once. `.gnmap` is grep-friendly, `.xml` feeds other tools.", read="Never scan without saving: you will want to compare scans later."),
     dict(title="Run one script", cmd="nmap --script http-title -p 80,8080 127.0.0.1", expect="For an open web port: a http-title line with the page title; for closed ports, nothing.",
          why="NSE scripts target one service. Read `--script-help` before running unfamiliar ones.", read="Scripts in categories such as `vuln` or `brute` can be intrusive: only use them where you are allowed.")],
    gotchas=["Scan only what you are authorised to scan, including at the venue.", "`filtered` means a firewall dropped the probe, not that the port is closed.",
             "`-sS` and `-O` need root; without it Nmap falls back to `-sT`.", "UDP scans are slow: limit with `--top-ports`.", "A host that blocks ping looks down: add `-Pn`."],
    related=["masscan", "rustscan", "nc", "tcpdump", "wireshark", "ffuf"],
    practice=["Scan your own VM with the two-step method and write the open-ports table.", "Start `python3 -m http.server 8000` and watch the port appear.", "Compare `-sS` and `-sT` in Wireshark."],
    cards=["What does `-Pn` do?", "What is the difference between closed and filtered?", "Why scan all ports first?", "What does `-oA` save?"]))

TOOLS2.append(dict(
    name="tcpdump", needs="tcpdump", version="tcpdump --version 2>&1 | head -1",
    one_line="Capture and print network packets from the command line, or save them for Wireshark.",
    when=["See whether traffic really leaves or reaches a machine.", "Record a capture of an attack on your defence-challenge service.", "Quick filters when Wireshark is not available."],
    anatomy="""sudo tcpdump  -i lo  -n  -nn  -c 10  -w cap.pcap  'tcp port 8080 and host 127.0.0.1'
                |      |    |       |         |           '--- BPF filter (quote it)
                |      |    |       |         '--- write packets to a file for Wireshark
                |      |    |       '--- stop after 10 packets
                |      |    '--- no name or port-name resolution
                |      '--- interface (`-i any` for all)
                '--- needs root to capture""",
    flags=[("-i IFACE", "Interface to listen on", "`lo` for local lab traffic, `eth0`, `any`"),
           ("-n / -nn", "No DNS / no port names", "Faster, shows numbers"),
           ("-c N", "Stop after N packets", "Short captures"),
           ("-w FILE / -r FILE", "Write / read a capture file", "Hand off to Wireshark"),
           ("-A / -X", "Show payload as ASCII / hex+ASCII", "Read cleartext protocols"),
           ("-v / -vv", "More protocol detail", "Check TTL, flags"),
           ("host / port / net / tcp / udp", "BPF filter words", "Narrow what you capture"),
           ("and / or / not", "Combine filter words", "`tcp and not port 22`")],
    recipes=[
     dict(title="Watch local web traffic", cmd="sudo tcpdump -i lo -nn -c 6 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/ > /dev/null; wait", expect="Lines like: IP 127.0.0.1.PORT > 127.0.0.1.8099: Flags [S], seq ... showing the SYN, SYN-ACK, ACK handshake and the HTTP request.",
          why="Capture on the loopback interface while making one request.", read="`[S]` is SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` data push, `[F.]` finish. Seeing the handshake proves a connection happened."),
     dict(title="See the payload in ASCII", cmd="sudo tcpdump -i lo -nn -A -c 8 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/hello > /dev/null; wait", expect="The packet containing 'GET /hello HTTP/1.1' and headers printed as readable text.",
          why="`-A` prints the payload as ASCII: cleartext HTTP, FTP and Telnet credentials are visible.", read="This is why encryption matters: on the wire everything is readable."),
     dict(title="Save a capture for Wireshark", cmd="sudo tcpdump -i lo -nn -c 20 -w cap.pcap 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/ > /dev/null; wait; tcpdump -nn -r cap.pcap | head -5", expect="A few packet lines read back from cap.pcap.",
          why="`-w` stores raw packets; `-r` reads them back.", read="Open `cap.pcap` in Wireshark and use Follow TCP Stream to read the conversation.")],
    gotchas=["Needs root (`sudo`) or the capture capability.", "Quote the filter so the shell does not eat `&` or parentheses.", "Capturing on `any` hides which interface a packet used.", "Only capture traffic you are allowed to see."],
    related=["wireshark / tshark", "nmap", "ss", "nc", "ngrep"],
    practice=["Capture a DNS lookup (`udp port 53`) and read the query and answer.", "Capture an SSH login and find the packet sizes.", "Filter for one host and one port."],
    cards=["What does `-w` do?", "What do the flags `[S]` and `[S.]` mean?", "Why quote a BPF filter?", "How do you show packet payload as text?"]))

TOOLS2.append(dict(
    name="gdb", needs="gdb", version="gdb --version | head -1",
    one_line="Run a program under a debugger: stop it, look at registers and memory, step instruction by instruction.",
    when=["Binary exploitation: find the offset that overwrites the return address.", "Reverse engineering: watch what a check compares.", "See what a crashed program was doing."],
    anatomy="""gdb  -q  --args ./hello open-sesame
 |    |       '--- everything after --args is the program and its arguments
 |    '--- quiet: no banner
 '--- the debugger

inside gdb:   break main    run    next / step    info registers    x/20wx $esp    bt    continue    quit""",
    flags=[("break FUNC / b *ADDR", "Set a breakpoint", "Stop where something interesting happens"),
           ("run [args] / r", "Start the program", "Begin"),
           ("next / step / nexti / stepi", "Step over / into a call; by source line or instruction", "Follow the logic"),
           ("continue / c", "Resume", "Run to the next breakpoint"),
           ("info registers / p $rip", "Show registers", "Where is the program, what are the values"),
           ("x/20wx $esp / x/s ADDR / x/10i $rip", "Examine memory: words, string, instructions", "Look at the stack, strings or code"),
           ("disassemble main / set disassembly-flavor intel", "Show code; Intel syntax", "Read assembly"),
           ("bt", "Backtrace: the call stack", "After a crash"),
           ("pattern create N / pattern offset X", "Cyclic pattern helpers (pwndbg/GEF)", "Find an overflow offset"),
           ("-ex 'cmd' -batch", "Run commands non-interactively", "Scripts")],
    recipes=[
     dict(title="Break at main and look at registers", cmd="gdb -q -batch -ex 'break main' -ex 'run' -ex 'info registers rip' ./hello", expect="Breakpoint 1, 0x... in main () followed by a line like rip 0x55555555513d showing the instruction pointer.",
          why="`-batch -ex` runs gdb commands without the interactive prompt.", read="`rip` (64-bit instruction pointer) is where the program stopped."),
     dict(title="Disassemble main in Intel syntax", cmd="gdb -q -batch -ex 'set disassembly-flavor intel' -ex 'disassemble main' ./hello", expect="Assembly of main with addresses, including a call to strcmp and a conditional jump.",
          why="The same view as `objdump -d` but inside the debugger.", read="Find the `cmp`/`test` and the following jump: that is the decision."),
     dict(title="Crash it and read the registers", cmd="gdb -q -batch -ex 'run $(python3 -c \"print(chr(65)*200)\")' -ex 'info registers rip' ./hello", expect="Possibly no crash for this program; for a vulnerable one: Program received signal SIGSEGV and rip showing the overwritten value (such as 0x4141414141414141).",
          why="This is the Narnia method: send a long input and see which bytes reach the instruction pointer.", read="If `rip` holds your pattern, you control execution: compute the offset with a cyclic pattern."),
     dict(title="Print a string from memory", cmd="gdb -q -batch -ex 'break main' -ex 'run' -ex 'x/s $rip' ./hello", expect="A line starting with the address and the bytes at it interpreted as text or instructions.",
          why="`x/s` examines memory as a string; use `x/10i` for instructions and `x/20wx` for words.", read="Learn the three formats: `s` string, `i` instruction, `x` hex.")],
    gotchas=["Stack addresses in gdb differ from the real run (environment size and path): sweep or leak the real address.", "gdb disables ASLR by default; the real program may randomise.", "Set-uid programs lose privileges under gdb.", "Install pwndbg or GEF for a readable display."],
    related=["pwndbg / GEF", "objdump", "ltrace / strace", "ghidra", "pwntools"],
    practice=["Find which instruction of `hello` compares your argument.", "Change `argv[1]` in memory so the check passes.", "Use `x/20wx $rsp` to dump the stack at `main`."],
    cards=["What does `break main` do?", "What do `x/s`, `x/i` and `x/x` print?", "Why do addresses differ inside gdb?", "How do you run gdb commands from a script?"]))

TOOLS2.append(dict(
    name="sqlite3", needs="sqlite3", version="sqlite3 --version",
    one_line="Open a SQLite database file and run SQL on it: list tables, read rows, search, count.",
    when=["Browser history, app data and many forensics challenges ship as `.db`/`.sqlite` files.", "Practice basic SQL offline.", "Check what an application stores."],
    anatomy="""sqlite3  -readonly  evidence.db  '.tables'
   |        |            |             '--- a dot-command or SQL statement to run, then exit
   |        |            '--- the database file
   |        '--- never modify evidence
   '--- the program""",
    flags=[(".tables", "List tables", "First step"),
           (".schema [table]", "Show table definitions", "Column names and types"),
           (".headers on / .mode column", "Nicer output", "Readable tables"),
           (".mode csv / .output FILE", "Export", "Hand off data"),
           ("-readonly", "Open without write access", "Evidence"),
           ("SELECT ... WHERE ... LIKE '%x%'", "Search rows", "Find a user, URL or message"),
           ("ORDER BY / LIMIT / GROUP BY / COUNT(*)", "Sort, cut, summarise", "Top N, counts per value"),
           (".dump", "Print the whole database as SQL", "Search it with grep")],
    recipes=[
     dict(title="Create a small database", cmd="rm -f t.db; sqlite3 t.db \"CREATE TABLE users(id INTEGER, name TEXT, role TEXT); INSERT INTO users VALUES (1,'alice','user'),(2,'bob','admin'),(3,'carol','user');\" && sqlite3 t.db '.tables'", expect="users",
          why="One command creates the file, the table and rows; then `.tables` lists it.", read="A database is just a file. Evidence files are opened the same way."),
     dict(title="Read it nicely", cmd="sqlite3 -header -column t.db 'SELECT * FROM users;'", expect="A header row id name role, a dashed line, then three rows.",
          why="`-header -column` formats output as a table.", read="Same result as `SELECT * FROM users;` in MySQL."),
     dict(title="Filter and count", cmd="sqlite3 -header -column t.db \"SELECT role, COUNT(*) AS n FROM users GROUP BY role;\"", expect="admin 1 and user 2.",
          why="`GROUP BY` counts rows per value.", read="Summaries are how you find the odd one out in thousands of rows."),
     dict(title="Look at the structure", cmd="sqlite3 t.db '.schema users'", expect="CREATE TABLE users(id INTEGER, name TEXT, role TEXT);",
          why="`.schema` prints the SQL that created the table.", read="MySQL's `DESCRIBE` equivalent.")],
    gotchas=["Dot-commands (`.tables`) are sqlite3 features, not SQL; they take no semicolon.", "Open evidence with `-readonly` or a copy.", "SQLite types are loose: text may hide in number columns.", "Browser databases may be locked while the browser runs: copy the file first."],
    related=["MySQL client", "DB Browser for SQLite", "python sqlite3 module", "strings", "grep"],
    practice=["List the tables of a browser history database copy.", "Find the most visited domain with `GROUP BY`.", "Export a table to CSV."],
    cards=["How do you list tables in sqlite3?", "How do you see a table's columns?", "Why use `-readonly` on evidence?", "What does `GROUP BY` do?"]))
