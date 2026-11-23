# tcpdump: the expanded manual

> **Not captured yet** (tcpdump not installed here). The outputs below are marked *expected*: they describe what you should see. Run `python3 scripts/atlas_build.py --tool tcpdump` on a machine that has the tool (Kali has it) to replace them with real captured output.

**In one line:** Capture and print network packets from the command line, or save them for Wireshark.

## When you reach for it (in a CTF or defence task)

- See whether traffic really leaves or reaches a machine.
- Record a capture of an attack on your defence-challenge service.
- Quick filters when Wireshark is not available.

## Anatomy of a command

```text
sudo tcpdump  -i lo  -n  -nn  -c 10  -w cap.pcap  'tcp port 8080 and host 127.0.0.1'
                |      |    |       |         |           '--- BPF filter (quote it)
                |      |    |       |         '--- write packets to a file for Wireshark
                |      |    |       '--- stop after 10 packets
                |      |    '--- no name or port-name resolution
                |      '--- interface (`-i any` for all)
                '--- needs root to capture
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-i IFACE` | Interface to listen on | `lo` for local lab traffic, `eth0`, `any` |
| `-n / -nn` | No DNS / no port names | Faster, shows numbers |
| `-c N` | Stop after N packets | Short captures |
| `-w FILE / -r FILE` | Write / read a capture file | Hand off to Wireshark |
| `-A / -X` | Show payload as ASCII / hex+ASCII | Read cleartext protocols |
| `-v / -vv` | More protocol detail | Check TTL, flags |
| `host / port / net / tcp / udp` | BPF filter words | Narrow what you capture |
| `and / or / not` | Combine filter words | `tcp and not port 22` |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Watch local web traffic

Capture on the loopback interface while making one request.

```bash
$ sudo tcpdump -i lo -nn -c 6 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/ > /dev/null; wait
```

```text
(expected, not captured) Lines like: IP 127.0.0.1.PORT > 127.0.0.1.8099: Flags [S], seq ... showing the SYN, SYN-ACK, ACK handshake and the HTTP request.
```

`[S]` is SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` data push, `[F.]` finish. Seeing the handshake proves a connection happened.

### 2. See the payload in ASCII

`-A` prints the payload as ASCII: cleartext HTTP, FTP and Telnet credentials are visible.

```bash
$ sudo tcpdump -i lo -nn -A -c 8 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/hello > /dev/null; wait
```

```text
(expected, not captured) The packet containing 'GET /hello HTTP/1.1' and headers printed as readable text.
```

This is why encryption matters: on the wire everything is readable.

### 3. Save a capture for Wireshark

`-w` stores raw packets; `-r` reads them back.

```bash
$ sudo tcpdump -i lo -nn -c 20 -w cap.pcap 'tcp port 8099' & sleep 1; curl -s http://127.0.0.1:8099/ > /dev/null; wait; tcpdump -nn -r cap.pcap | head -5
```

```text
(expected, not captured) A few packet lines read back from cap.pcap.
```

Open `cap.pcap` in Wireshark and use Follow TCP Stream to read the conversation.

## Mistakes people make

- Needs root (`sudo`) or the capture capability.
- Quote the filter so the shell does not eat `&` or parentheses.
- Capturing on `any` hides which interface a packet used.
- Only capture traffic you are allowed to see.

## Related tools

wireshark / tshark, nmap, ss, nc, ngrep

## Practice

1. Capture a DNS lookup (`udp port 53`) and read the query and answer.
2. Capture an SSH login and find the packet sizes.
3. Filter for one host and one port.

## Flashcard prompts

- What does `-w` do?
- What do the flags `[S]` and `[S.]` mean?
- Why quote a BPF filter?
- How do you show packet payload as text?

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
