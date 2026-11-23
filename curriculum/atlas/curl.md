# curl: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Send exactly the HTTP request you describe and show exactly what comes back.

## When you reach for it (in a CTF or defence task)

- Test a web challenge without a browser: change a header, cookie, method or body and see the response.
- Download a file, follow a redirect, check a status code in a script.
- Reproduce what Burp or the browser sent, as a copy-paste command.

## Anatomy of a command

```text
curl -s -i -X POST -H 'X-Role: admin' -b 'session=abc' -d 'user=alice' http://127.0.0.1:8099/login
 |    |  |  |       |                 |                 |                |             '--- URL
 |    |  |  |       |                 |                 |                '--- request body
 |    |  |  |       |                 |                 '--- cookie header
 |    |  |  |       |                 '--- add or replace a header
 |    |  |  |       '--- method (curl picks POST for -d by itself)
 |    |  |  '--- -i = show response headers too
 |    |  '--- -s = silent: no progress bar
 '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-s / -S` | Silent / show errors even when silent | Scripts and clean output |
| `-i / -I` | Include response headers / HEAD request only | See status line, cookies, redirects |
| `-v` | Verbose: show the request and response headers | See exactly what is sent |
| `-X METHOD` | Set the method (GET, POST, PUT, DELETE) | Test method handling |
| `-H 'Name: value'` | Add or replace a header | User-Agent, Referer, Authorization, X-Forwarded-For |
| `-A / -e` | User-Agent / Referer shortcuts | Natas-style Referer checks |
| `-b 'k=v' / -c file` | Send cookies / save cookies | Session and cookie tampering |
| `-d / --data-urlencode` | Request body (form data) / URL-encode a value | Forms and logins |
| `--json '{...}'` | Send JSON with the right headers (recent curl) | APIs |
| `-u user:pass` | HTTP Basic authentication | Basic-auth pages (note: it is only base64) |
| `-L` | Follow redirects | Reach the final page |
| `-o FILE / -O` | Save the body to a file / use the remote name | Download |
| `-w '%{http_code}'` | Print a field after the transfer | Status codes in loops |
| `-k` | Ignore TLS certificate errors | Lab self-signed certificates only |
| `--path-as-is` | Do not squash `/../` in the URL | Path traversal tests |
| `--max-time N` | Give up after N seconds | Scripts |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. A plain GET

This lab server echoes back what it received, so you can see the request as the server saw it.

```bash
$ curl -s 'http://127.0.0.1:8099/hello?x=1'
```

```text
GET /hello?x=1
User-Agent: curl/8.5.0
Accept: */*
```

The first line is method and path; the rest are headers curl sent by default (`User-Agent`, `Accept`).

### 2. See the response headers

`-i` includes the status line and headers. `-s` hides the progress meter.

```bash
$ curl -si http://127.0.0.1:8099/ | head -8
```

```text
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.3
Date: Mon, 23 Nov 2026 17:11:42 GMT
Content-Type: text/plain
X-Demo: echo

GET /
User-Agent: curl/8.5.0
```

Status `200 OK`, a `Content-Type`, and the custom `X-Demo` header. Always read headers in web challenges: cookies and hints live there.

### 3. Change headers and send a cookie

Headers and cookies are client-controlled; a server must never trust them for access control.

```bash
$ curl -s -H 'X-Role: admin' -A 'MyAgent/1.0' -e 'http://natas5.example' -b 'loggedin=1' http://127.0.0.1:8099/
```

```text
GET /
User-Agent: MyAgent/1.0
Accept: */*
Referer: http://natas5.example
Cookie: loggedin=1
X-Role: admin
```

The echo shows each of your values arriving: User-Agent, Referer, Cookie and X-Role.

### 4. POST a form and JSON

`-d` switches to POST and sets a form content type; for JSON you set the header yourself.

```bash
$ curl -s -d 'user=alice&pass=1' http://127.0.0.1:8099/login; echo; echo ----; curl -s -H 'Content-Type: application/json' -d '{"a":1}' http://127.0.0.1:8099/api
```

```text
POST /login
User-Agent: curl/8.5.0
Accept: */*
Content-Length: 17
Content-Type: application/x-www-form-urlencoded

user=alice&pass=1
----
POST /api
User-Agent: curl/8.5.0
Accept: */*
Content-Type: application/json
Content-Length: 7

{"a":1}
```

The body appears after a blank line, with different `Content-Type` values for the two requests.

### 5. Basic auth is just base64

`-u` sends `Authorization: Basic <base64(user:pass)>`. Anyone who sees the request can decode it.

```bash
$ curl -s -u alice:secret http://127.0.0.1:8099/ | grep Authorization; echo 'YWxpY2U6c2VjcmV0' | base64 -d; echo
```

```text
Authorization: Basic YWxpY2U6c2VjcmV0
alice:secret
```

The header carries the encoded credentials and `base64 -d` recovers them. This is why Basic auth needs HTTPS.

### 6. Redirects

Without `-L` you see the 301 and its `Location` header; with `-L` curl follows to the final page. `-w` prints a summary.

```bash
$ curl -si http://127.0.0.1:8099/old | head -3; echo ---; curl -sL -o /dev/null -w 'final=%{url_effective} code=%{http_code}\n' http://127.0.0.1:8099/old
```

```text
HTTP/1.0 301 Moved Permanently
Server: BaseHTTP/0.6 Python/3.12.3
Date: Mon, 23 Nov 2026 17:11:42 GMT
---
final=http://127.0.0.1:8099/new code=200
```

Seeing the redirect response itself matters: sometimes the useful content is in the redirect, not the destination (Natas 22).

### 7. Status code only, for scripting

`-o /dev/null` discards the body; `-w` prints the status. Loop over paths to build a tiny scanner.

```bash
$ for p in / /admin /missing; do curl -s -o /dev/null -w "$p %{http_code}\n" http://127.0.0.1:8099$p; done
```

```text
/ 200
/admin 403
/missing 404
```

200 for the home page, 403 (forbidden: it exists but you may not read it) for `/admin` and 404 (not found) for `/missing`. The difference between 403 and 404 tells you what exists. A real scanner (ffuf, gobuster) does this faster.

### 8. Show the raw request curl sends

`-v` prints lines starting with `>` (request) and `<` (response). Redirecting stdout hides the body.

```bash
$ curl -sv http://127.0.0.1:8099/ 2>&1 >/dev/null | grep -E '^(>|<)'
```

```text
> GET / HTTP/1.1
> Host: 127.0.0.1:8099
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.12.3
< Date: Mon, 23 Nov 2026 17:11:42 GMT
< Content-Type: text/plain
< X-Demo: echo
< 
```

This is the exact text on the wire. If a challenge says the server checks a header, this is where you confirm it was sent.

## Mistakes people make

- Quote URLs that contain `&` or `?`: the shell treats `&` as 'run in background'.
- `-d` implies POST and `application/x-www-form-urlencoded`; use `-G` to put data in the URL instead.
- Use `--data-urlencode` for values with spaces or symbols, or they are sent raw.
- curl may normalise `/../` in the URL; add `--path-as-is` to send it unchanged.
- `-k` disables certificate checks: fine for your own lab, never for real credentials.

## Related tools

wget, httpie, Burp Repeater, ffuf, nc (raw HTTP), python requests

## Practice

1. Send the request that makes the lab echo header `X-Forwarded-For: 127.0.0.1`.
2. Write a loop that prints the status for 10 paths from a list in a file.
3. Reproduce a browser request from DevTools: right-click, Copy as cURL.

## Flashcard prompts

- What does `curl -i` show?
- How do you send a cookie?
- Why can you decode a Basic auth header?
- How do you see a redirect without following it?
- What does `-w '%{http_code}'` do?

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
