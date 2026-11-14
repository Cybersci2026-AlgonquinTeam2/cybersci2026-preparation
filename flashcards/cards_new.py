"""Decks for the newer books: memory forensics, defence runbook, Nmap, basic SQL, OverTheWire games.
Written from the books in curriculum/activities and curriculum/overthewire (no image refs)."""


def register(add):
    add("Memory forensics", [
        ("What is a memory image?", "A file copy of RAM: running processes, connections, command lines, keys and files that never hit disk."),
        ("First Volatility 3 command on a Windows image?", "<code>vol -f mem.raw windows.info</code> (confirms it parses; shows OS build and time)."),
        ("pslist vs psscan?", "pslist walks the OS's active list; psscan scans memory for process objects and finds hidden or exited ones."),
        ("A process in psscan but not pslist means?", "Hidden (unlinked) or already exited."),
        ("Plugin to see parent/child process shape?", "<code>windows.pstree</code>"),
        ("Plugin for full command lines?", "<code>windows.cmdline</code> (use <code>--pid N</code> to focus)."),
        ("Plugin for network connections?", "<code>windows.netscan</code> (also <code>windows.netstat</code>)."),
        ("What does malfind look for?", "Executable memory regions with no file behind them, which suggests injected code."),
        ("List files open in memory, then extract one?", "<code>windows.filescan</code> to find the offset, then <code>windows.dumpfiles --virtaddr ...</code> with <code>-o outdir</code>."),
        ("Why does plain strings miss most Windows text?", "Windows stores text as UTF-16; use <code>strings -a -e l</code>."),
        ("Plugin for NTLM hashes, and the hashcat mode?", "<code>windows.hashdump</code>; hashcat mode 1000."),
        ("Where to look for persistence in a memory image?", "Registry Run keys (<code>windows.registry.printkey</code>), services (<code>windows.svcscan</code>)."),
        ("Red flag: Office app spawning powershell.exe?", "Macro or exploit execution."),
        ("Red flag: svchost.exe whose parent is not services.exe?", "Masquerading malware."),
        ("Red flag: a process running from AppData or Temp?", "Likely malware."),
        ("Do Linux images need anything extra in Volatility 3?", "Matching symbol (ISF) files for the kernel."),
        ("How can you make your own memory image in VMware?", "Suspend or snapshot the VM; the <code>.vmem</code> file is the RAM image."),
        ("Memory forensics triage rule?", "Timeline first, flags second: write one line per finding as you go."),
    ])

    add("Defence challenge", [
        ("Four levers of a defence challenge?", "Observe (logs/traffic), read (source), patch (minimal fix), verify (rerun attack and test features)."),
        ("Why git init before changing anything?", "A baseline and an undo button: you can diff and revert."),
        ("What is the patch hint ladder?", "Observe, reproduce, classify, find in source, patch minimally, verify twice, revert if it breaks."),
        ("Fix for SQL injection?", "Parameterized queries / prepared statements."),
        ("Fix for path traversal?", "Resolve to an absolute path and verify it stays under the allowed folder."),
        ("Fix for command injection?", "Do not use a shell; pass arguments as a list; allowlist inputs."),
        ("Fix for broken access control?", "Check on the server that the logged-in user owns the object, on every request."),
        ("Fix for unsafe upload?", "Allowlist type, random names, store outside the web root, never executable."),
        ("Blocklist or allowlist?", "Allowlist: blocklists miss variants."),
        ("Why verify a patch twice?", "The attack must now fail and the normal feature must still work."),
        ("Strongest sign of a remote shell on a Linux server?", "A web/app process that has a shell as its child, plus an outbound connection to an unknown IP."),
        ("Command to map connections to processes on Linux?", "<code>ss -tnp</code> (or <code>lsof -i -n -P</code>)."),
        ("Why capture evidence before killing a malicious process?", "You lose the command line, connections and parent if you kill and restart blindly."),
        ("Why block outbound traffic as a defence?", "Reverse shells and data theft need outbound connections; default-deny egress breaks them."),
        ("Where do attackers hide persistence on Linux?", "cron, authorized_keys, systemd services, startup scripts, modified binaries."),
        ("Defence challenge timeline for the first 15 minutes?", "Baseline in git, backups, logs, packet capture, map the service."),
    ])

    add("Nmap and networking", [
        ("What does <code>-sn</code> do?", "Ping sweep: host discovery only, no port scan."),
        ("What does <code>-Pn</code> do and when?", "Skips host discovery and treats the host as up; use when ICMP is blocked."),
        ("CTF default two-step scan?", "<code>nmap -p- -T4 TARGET</code> to find all open ports, then <code>nmap -sV -sC -p PORTS TARGET</code>."),
        ("Port state: filtered?", "No answer: a firewall is dropping packets (or the host is down). It is not 'closed'."),
        ("Port state: closed?", "Host answered that nothing listens there."),
        ("-sS vs -sT?", "-sS is SYN (half-open) and needs root; -sT is a full connect and works without root and through proxies."),
        ("Scan UDP?", "<code>nmap -sU --top-ports 50 TARGET</code> (slow, needs root)."),
        ("What does <code>-sV</code> do?", "Probes open ports to identify the service and version."),
        ("What does <code>-sC</code> do?", "Runs the default NSE scripts."),
        ("What does <code>-A</code> do?", "Aggressive: -sV -sC -O --traceroute."),
        ("Save all output formats?", "<code>-oA name</code> (.nmap, .xml, .gnmap)."),
        ("How many usable hosts in a /24? /16?", "254; 65,534."),
        ("Private IP ranges?", "10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16."),
        ("Scan through an SSH SOCKS proxy?", "<code>proxychains nmap -sT -Pn TARGET</code> (SYN and ICMP do not pass through SOCKS)."),
        ("How to check the route to another subnet?", "<code>ip route</code> / <code>route print</code>, and <code>traceroute</code> or <code>--traceroute</code>."),
        ("Read what an NSE script does?", "<code>nmap --script-help NAME</code>"),
        ("Default port for SSH, SMB, RDP, MySQL?", "22, 445 (and 139), 3389, 3306."),
        ("Banner-grab by hand?", "<code>nc -nv TARGET PORT</code>"),
    ])

    add("Basic SQL", [
        ("List databases in MySQL?", "<code>SHOW DATABASES;</code>"),
        ("Pick a database?", "<code>USE name;</code>"),
        ("List tables?", "<code>SHOW TABLES;</code>"),
        ("Show a table's columns?", "<code>DESCRIBE table;</code> (or <code>SHOW COLUMNS FROM table;</code>)."),
        ("Select every row?", "<code>SELECT * FROM table;</code>"),
        ("Filter rows?", "<code>WHERE column = 'value'</code>"),
        ("SQL wildcard for any number of characters? One character?", "<code>%</code>; <code>_</code> (used with LIKE)."),
        ("Match names starting with 'ad'?", "<code>WHERE name LIKE 'ad%'</code>"),
        ("Sort and limit results?", "<code>ORDER BY col DESC LIMIT 5</code>"),
        ("Combine two SELECTs with the same column count?", "<code>UNION SELECT ...</code>"),
        ("SQL comment markers?", "<code>-- </code> (note the space) and <code>#</code> in MySQL; <code>/* ... */</code>."),
        ("Where do MySQL table and column names live?", "<code>information_schema.tables</code> and <code>information_schema.columns</code>."),
        ("Why does <code>' OR '1'='1</code> work in a vulnerable login?", "It makes the WHERE condition always true; the query was built by string concatenation."),
        ("The proper fix for SQL injection?", "Parameterized queries (prepared statements), not quote filtering."),
        ("Boolean blind injection in one line?", "Ask yes/no questions about hidden data, one character at a time, from a true/false page difference."),
        ("Time-based blind injection?", "Make the DB sleep conditionally and measure the response time."),
    ])
