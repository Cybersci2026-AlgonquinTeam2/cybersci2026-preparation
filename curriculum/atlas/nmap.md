# nmap: the expanded manual

> **Not captured yet** (nmap not installed here). The outputs below are marked *expected*: they describe what you should see. Run `python3 scripts/atlas_build.py --tool nmap` on a machine that has the tool (Kali has it) to replace them with real captured output.

**In one line:** Discover hosts, open ports, services and versions on a network, and run scripts against them.

## When you reach for it (in a CTF or defence task)

- The first command on any network challenge or lab machine.
- Find out which services run and which versions.
- Check what a firewall allows (open versus filtered).

## Anatomy of a command

```text
nmap  -sV  -sC  -p 22,80,443  -oA scan1  127.0.0.1
 |     |    |     |            |           '--- target: IP, name, CIDR (10.0.0.0/24), range, or -iL file
 |     |    |     |            '--- save in all formats (scan1.nmap/.xml/.gnmap)
 |     |    |     '--- ports (use -p- for all 65,535)
 |     |    '--- default NSE scripts
 |     '--- probe open ports for service and version
 '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-sn` | Host discovery only (ping sweep) | Who is up on this subnet? |
| `-Pn` | Skip discovery, treat host as up | ICMP blocked or crossing a firewall |
| `-p- / -p 1-1024 / --top-ports N` | Which ports to scan | All ports first, then focus |
| `-sS / -sT / -sU` | SYN scan (root) / TCP connect / UDP | Default, no-root or proxy use, UDP services |
| `-sV` | Service and version detection | After you know the open ports |
| `-sC / --script NAME` | Default scripts / a chosen script | Enumerate and check known issues |
| `-O / -A` | OS guess / aggressive (-sV -sC -O --traceroute) | Quick profile of a lab box |
| `-T0..T5` | Timing template | T4 in labs, slower on fragile or monitored networks |
| `-oA name / -oN / -oX` | Save output | Always save |
| `--open / -v` | Show only open ports / more detail | Cleaner output |
| `--script-help NAME` | Read what a script does | Before running unfamiliar scripts |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Is the host up?

`-sn` does discovery without scanning ports.

```bash
$ nmap -sn 127.0.0.1
```

```text
(expected, not captured) Starting Nmap ... Nmap scan report for localhost (127.0.0.1) / Host is up / Nmap done: 1 IP address (1 host up) scanned.
```

One host up. On a LAN you would pass a CIDR such as `192.168.1.0/24`.

### 2. Default scan of localhost

With no options Nmap scans the 1000 most common TCP ports.

```bash
$ nmap 127.0.0.1
```

```text
(expected, not captured) A PORT STATE SERVICE table listing the open TCP ports among the top 1000 (for example 22/tcp ssh if sshd runs), and the number of closed ports not shown.
```

Read the three columns: port/protocol, state (open, closed, filtered) and the service name guessed from the port number.

### 3. Every port, then look closely

The CTF default: find all ports quickly, then spend time only on the open ones.

```bash
$ nmap -p- -T4 127.0.0.1 && nmap -sV -sC -p 22 127.0.0.1
```

```text
(expected, not captured) First scan: the list of all open ports. Second scan: the same port with a version string (for example OpenSSH 9.x) and script output such as host keys.
```

`-sV` replaces the guessed service name with a detected version; scripts add facts such as SSH host key fingerprints or web page titles.

### 4. Save results

`-oA` writes three formats at once. `.gnmap` is grep-friendly, `.xml` feeds other tools.

```bash
$ nmap -oA scan1 127.0.0.1 && ls scan1.*
```

```text
(expected, not captured) scan1.gnmap scan1.nmap scan1.xml
```

Never scan without saving: you will want to compare scans later.

### 5. Run one script

NSE scripts target one service. Read `--script-help` before running unfamiliar ones.

```bash
$ nmap --script http-title -p 80,8080 127.0.0.1
```

```text
(expected, not captured) For an open web port: a http-title line with the page title; for closed ports, nothing.
```

Scripts in categories such as `vuln` or `brute` can be intrusive: only use them where you are allowed.

## Mistakes people make

- Scan only what you are authorised to scan, including at the venue.
- `filtered` means a firewall dropped the probe, not that the port is closed.
- `-sS` and `-O` need root; without it Nmap falls back to `-sT`.
- UDP scans are slow: limit with `--top-ports`.
- A host that blocks ping looks down: add `-Pn`.

## Related tools

masscan, rustscan, nc, tcpdump, wireshark, ffuf

## Practice

1. Scan your own VM with the two-step method and write the open-ports table.
2. Start `python3 -m http.server 8000` and watch the port appear.
3. Compare `-sS` and `-sT` in Wireshark.

## Flashcard prompts

- What does `-Pn` do?
- What is the difference between closed and filtered?
- Why scan all ports first?
- What does `-oA` save?

## The lab used for these examples

```bash
rm -rf /tmp/atlas; mkdir -p /tmp/atlas && cd /tmp/atlas
cat > access.log <<'L'
10.0.0.5 - - [14/Nov/2026:10:01:12 +0000] "GET /index.html HTTP/1.1" 200 1043
10.0.0.5 - - [14/Nov/2026:10:01:15 +0000] "GET /login HTTP/1.1" 200 512
10.0.0.9 - - [14/Nov/2026:10:02:01 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:03 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:05 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:09 +0000] "POST /login HTTP/1.1" 302 0
10.0.0.9 - - [14/Nov/2026:10:02:15 +0000] "GET /admin HTTP/1.1" 200 2210
10.0.0.7 - - [14/Nov/2026:10:03:40 +0000] "GET /../../etc/passwd HTTP/1.1" 400 0
10.0.0.7 - - [14/Nov/2026:10:03:44 +0000] "GET /backup.zip HTTP/1.1" 404 196
L
cat > users.txt <<'L'
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice Lee:/home/alice:/bin/bash
bob:x:1002:1002:Bob Ray:/home/bob:/bin/sh
svc-backup:x:998:998::/var/backups:/usr/sbin/nologin
L
cat > notes.txt <<'L'
Meeting at 3pm
Password reset for bob: Summer2026!
TODO: rotate keys
password policy: 12 characters
The flag format is flag{...}
Remember: PASSWORD files are case sensitive?
L
mkdir -p site/css site/js site/uploads
echo '<h1>Demo site</h1>' > site/index.html
echo 'Disallow: /admin' > site/robots.txt
echo 'body{}' > site/css/main.css
echo 'alert(1)' > site/js/app.js
echo 'x' > site/uploads/report.pdf
echo 'secret=1' > site/.env
chmod 600 site/.env
touch -d '2026-11-10 10:00' site/index.html site/robots.txt
printf '#!/bin/sh\necho hi\n' > run.sh; chmod +x run.sh
cat > hello.c <<'C'
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
    const char *secret = "flag{demo_not_a_real_flag}";
    if (argc > 1 && strcmp(argv[1], "open-sesame") == 0) { puts(secret); return 0; }
    puts("access denied");
    return 1;
}
C
gcc -o hello hello.c 2>/dev/null
python3 - <<'PY'
import zlib, struct
def ch(t, d): c = struct.pack('>I', len(d)) + t + d; return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(b'\x00\xff\x00\x00')) + ch(b'IEND', b'')
open('pic.png', 'wb').write(png + b'hidden: flag{demo_not_a_real_flag}')
PY
cp pic.png holiday.txt
gzip -k notes.txt
printf 'aGVsbG8gd29ybGQ=\n' > data.b64
cat > echo.py <<'PY'
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def _go(self):
        if self.path == '/old':
            self.send_response(301); self.send_header('Location', '/new'); self.end_headers(); return
        if self.path in ('/admin', '/missing'):
            self.send_response(403 if self.path == '/admin' else 404); self.end_headers(); return
        n = int(self.headers.get('Content-Length') or 0); body = self.rfile.read(n).decode()
        out = f"{self.command} {self.path}\n" + "".join(f"{k}: {v}\n" for k, v in self.headers.items() if k.lower() not in ('host', 'accept-encoding', 'connection')) + ("\n" + body if body else "")
        self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.send_header('X-Demo', 'echo'); self.end_headers(); self.wfile.write(out.encode())
    do_GET = do_POST = do_PUT = do_HEAD = _go
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', 8099), H).serve_forever()
PY
```
