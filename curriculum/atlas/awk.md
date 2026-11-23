# awk: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `GNU Awk 5.2.1, API 3.2, PMA Avon 8-g1, (GNU MPFR 4.2.1, GNU MP 6.3.0)`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Treat each line as fields and run a tiny program: print columns, filter, count, add up.

## When you reach for it (in a CTF or defence task)

- Pull a column out of a log, `/etc/passwd`, `ps` or a CSV.
- Count events per IP or user (a one-line report).
- Sum or average numbers; reformat output.

## Anatomy of a command

```text
awk  -F:  '$3 >= 1000 { print $1, $6 }'  users.txt
 |     |    |   |           |            '--- input file
 |     |    |   |           '--- action: print field 1 and field 6
 |     |    |   '--- condition (pattern): field 3 is at least 1000
 |     |    '--- the program is in single quotes
 |     '--- -F sets the field separator (default: whitespace)
 '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-F SEP` | Field separator (`-F:`, `-F,`, `-F'\t'`) | Colon, comma or tab separated data |
| `$1 $2 ... $NF` | Field 1, 2 ... the last field | Pick columns |
| `$0` | The whole line | Print or test everything |
| `NR / NF` | Line number / number of fields | Skip headers (`NR>1`), check shape |
| `BEGIN { } / END { }` | Run once before / after all lines | Totals and reports |
| `arr[key]++` | Associative arrays | Counting per key |
| `printf` | Formatted output | Aligned columns |
| `-v var=value` | Pass a shell value into awk | Parameterise a filter |
| `~ / !~` | Regex match / no match | Test a field against a pattern |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Print columns

Fields are split on whitespace: 1 = IP, 7 = path, 9 = status in this log format.

```bash
$ awk '{print $1, $7, $9}' access.log | head -4
```

```text
10.0.0.5 /index.html 200
10.0.0.5 /login 200
10.0.0.9 /login 401
10.0.0.9 /login 401
```

IP, path, status for each request. Counting fields on one line first (`awk '{print NF}' | head -1`) avoids off-by-one mistakes.

### 2. Filter on a field

The part before `{...}` is a condition. Only matching lines run the action.

```bash
$ awk '$9 == 401 {print $1, $7}' access.log
```

```text
10.0.0.9 /login
10.0.0.9 /login
10.0.0.9 /login
```

Only the three failed logins appear.

### 3. Count per IP (associative array)

`c[$1]++` counts per IP. `END` prints the table after all lines are read.

```bash
$ awk '{c[$1]++} END {for (ip in c) print c[ip], ip}' access.log | sort -rn
```

```text
5 10.0.0.9
2 10.0.0.7
2 10.0.0.5
```

Requests per IP, busiest first. Same shape as the grep pipeline but you can add conditions.

### 4. Sum a column

`$NF` is the last field (the byte count). `NR` at the end is the number of lines read.

```bash
$ awk '{s += $NF} END {print s, "bytes in", NR, "requests"}' access.log
```

```text
4222 bytes in 9 requests
```

Total bytes served and the request count.

### 5. Use another separator

`-F:` splits on colons, as in `/etc/passwd`. Field 3 is the UID, field 6 the home directory.

```bash
$ awk -F: '$3 >= 1000 {print $1, "->", $6}' users.txt
```

```text
alice -> /home/alice
bob -> /home/bob
```

Normal users (UID 1000 and up) with their home folders. `svc-backup` (UID 998) is skipped.

### 6. Format a small report

`BEGIN` runs before the first line; `printf` pads columns.

```bash
$ awk -F: 'BEGIN {printf "%-12s %-6s\n", "USER", "UID"} {printf "%-12s %-6s\n", $1, $3}' users.txt
```

```text
USER         UID   
root         0     
alice        1001  
bob          1002  
svc-backup   998   
```

A neat two-column table. Handy for screenshots in a writeup.

## Mistakes people make

- Single-quote the program; double quotes let the shell expand `$1` first.
- Fields are 1-based; `$0` is the whole line.
- Quoted strings inside awk use double quotes; escape them inside `bash -c`.
- awk is not one program: gawk (used for these examples), mawk (the default on some Ubuntu installs) and BSD awk differ in features such as `asort`, `--version` and regex intervals.

## Related tools

cut, sort, uniq, sed, column -t, python -c

## Practice

1. Print the unique status codes in `access.log` with counts.
2. Print lines where the byte count is greater than 1000.
3. Print each username in `users.txt` in upper case (`toupper`).

## Flashcard prompts

- What is `$NF`?
- What does `NR>1` do?
- How do you count occurrences per key in awk?
- Why single-quote an awk program?

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
