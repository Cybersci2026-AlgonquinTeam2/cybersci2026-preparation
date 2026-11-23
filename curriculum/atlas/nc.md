# nc: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `netcat-openbsd 1.226-1ubuntu2`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Open a plain TCP (or UDP) connection and pipe text or files through it: the Swiss army knife for talking to services.

## When you reach for it (in a CTF or defence task)

- Connect to a CTF service and read its prompt (`nc host port`).
- Check whether a port is open; grab a banner; send a hand-written HTTP request.
- Move a file between two machines in a lab.

## Anatomy of a command

```text
nc  -zv  -w 2  127.0.0.1  8099
 |   |    |     |         '--- port (or a range 8000-8100)
 |   |    |     '--- host
 |   |    '--- -w = give up after 2 seconds
 |   '--- -z = just check the port is open (send no data), -v = say so
 '--- the program (this guide uses the OpenBSD netcat that Ubuntu installs)
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-v` | Verbose: report connection results | See `succeeded`/`refused` |
| `-z` | Scan mode: connect and close | Quick port check |
| `-w N` | Timeout in seconds | Do not hang |
| `-l` | Listen for an incoming connection (OpenBSD: `nc -l HOST PORT`) | Receive a file, catch a connection in a lab |
| `-N` | Shut down the network socket on end of input (OpenBSD) | Make a file transfer finish |
| `-u` | UDP instead of TCP | DNS-like services, games |
| `-n` | No DNS lookups | Faster, avoids leaking names |
| `-k` | Keep listening after one connection | Serve repeatedly |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Check whether a port is open

`-z` connects without sending data. The first port has the lab server; the second has nothing.

```bash
$ nc -zv -w2 127.0.0.1 8099; nc -zv -w2 127.0.0.1 9
```

```text
Connection to 127.0.0.1 8099 port [tcp/*] succeeded!
nc: connect to 127.0.0.1 port 9 (tcp) failed: Connection refused
```

One `succeeded` and one `refused`. Same idea as an Nmap TCP connect scan for a single port.

### 2. Hand-write an HTTP request

HTTP is plain text over TCP. `\r\n` line endings and a blank line end the request.

```bash
$ printf 'GET /raw HTTP/1.0\r\nX-A: 1\r\n\r\n' | nc -w2 127.0.0.1 8099 | head -8
```

```text
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.3
Date: Mon, 23 Nov 2026 18:22:33 GMT
Content-Type: text/plain
X-Demo: echo

GET /raw
X-A: 1
```

The server replies with a status line, headers and the echoed body: you spoke HTTP with no browser.

### 3. Send a message to a listener

One side listens (`-l`) and writes what it receives to a file; the other connects and sends a line.

```bash
$ (nc -l 127.0.0.1 9099 > got.txt &) ; sleep 0.5; echo 'hello from the client' | nc -N 127.0.0.1 9099; sleep 0.5; cat got.txt
```

```text
hello from the client
```

The file contains the message. Two terminals, one connection: the basis of every `nc host port` challenge.

### 4. Transfer a file and verify it

Redirects (`<`, `>`) feed a file into and out of the socket. Compare hashes to prove nothing changed.

```bash
$ (nc -l 127.0.0.1 9100 > recv.bin &) ; sleep 0.5; nc -N 127.0.0.1 9100 < hello; sleep 0.5; cmp hello recv.bin && echo identical; sha256sum hello recv.bin
```

```text
identical
8feb47265ff2233ef1420033f46617e67605c3234209fbd69d62e9468e3eb228  hello
8feb47265ff2233ef1420033f46617e67605c3234209fbd69d62e9468e3eb228  recv.bin
```

`identical` and two matching hashes. Always verify transfers in forensics work.

## Mistakes people make

- There are several netcats: OpenBSD (`nc -l host port`), traditional (`nc -l -p port`, has `-e`), and `ncat` from Nmap. Check `nc -h`.
- A connection that hangs often means you did not send the newline the service waits for.
- Without `-N`/`-q`, a transfer may never exit; add a timeout (`-w`).
- Only connect to hosts you are allowed to test.

## Related tools

ncat, socat, telnet, curl, nmap, pwntools remote()

## Practice

1. Connect to the lab server and send a PUT with a body using only `nc`.
2. Send `hello` over UDP between two terminals (`-u`).
3. Check which of ports 8095-8100 are open with `nc -zv`.

## Flashcard prompts

- What does `nc -zv host port` do?
- Why do different netcat versions matter?
- How do you listen and save to a file?
- How do you hand-write an HTTP request?

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
