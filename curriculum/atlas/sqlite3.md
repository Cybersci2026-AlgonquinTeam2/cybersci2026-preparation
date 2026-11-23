# sqlite3: the expanded manual

> **Not captured yet** (sqlite3 not installed here). The outputs below are marked *expected*: they describe what you should see. Run `python3 scripts/atlas_build.py --tool sqlite3` on a machine that has the tool (Kali has it) to replace them with real captured output.

**In one line:** Open a SQLite database file and run SQL on it: list tables, read rows, search, count.

## When you reach for it (in a CTF or defence task)

- Browser history, app data and many forensics challenges ship as `.db`/`.sqlite` files.
- Practice basic SQL offline.
- Check what an application stores.

## Anatomy of a command

```text
sqlite3  -readonly  evidence.db  '.tables'
   |        |            |             '--- a dot-command or SQL statement to run, then exit
   |        |            '--- the database file
   |        '--- never modify evidence
   '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `.tables` | List tables | First step |
| `.schema [table]` | Show table definitions | Column names and types |
| `.headers on / .mode column` | Nicer output | Readable tables |
| `.mode csv / .output FILE` | Export | Hand off data |
| `-readonly` | Open without write access | Evidence |
| `SELECT ... WHERE ... LIKE '%x%'` | Search rows | Find a user, URL or message |
| `ORDER BY / LIMIT / GROUP BY / COUNT(*)` | Sort, cut, summarise | Top N, counts per value |
| `.dump` | Print the whole database as SQL | Search it with grep |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Create a small database

One command creates the file, the table and rows; then `.tables` lists it.

```bash
$ rm -f t.db; sqlite3 t.db "CREATE TABLE users(id INTEGER, name TEXT, role TEXT); INSERT INTO users VALUES (1,'alice','user'),(2,'bob','admin'),(3,'carol','user');" && sqlite3 t.db '.tables'
```

```text
(expected, not captured) users
```

A database is just a file. Evidence files are opened the same way.

### 2. Read it nicely

`-header -column` formats output as a table.

```bash
$ sqlite3 -header -column t.db 'SELECT * FROM users;'
```

```text
(expected, not captured) A header row id name role, a dashed line, then three rows.
```

Same result as `SELECT * FROM users;` in MySQL.

### 3. Filter and count

`GROUP BY` counts rows per value.

```bash
$ sqlite3 -header -column t.db "SELECT role, COUNT(*) AS n FROM users GROUP BY role;"
```

```text
(expected, not captured) admin 1 and user 2.
```

Summaries are how you find the odd one out in thousands of rows.

### 4. Look at the structure

`.schema` prints the SQL that created the table.

```bash
$ sqlite3 t.db '.schema users'
```

```text
(expected, not captured) CREATE TABLE users(id INTEGER, name TEXT, role TEXT);
```

MySQL's `DESCRIBE` equivalent.

## Mistakes people make

- Dot-commands (`.tables`) are sqlite3 features, not SQL; they take no semicolon.
- Open evidence with `-readonly` or a copy.
- SQLite types are loose: text may hide in number columns.
- Browser databases may be locked while the browser runs: copy the file first.

## Related tools

MySQL client, DB Browser for SQLite, python sqlite3 module, strings, grep

## Practice

1. List the tables of a browser history database copy.
2. Find the most visited domain with `GROUP BY`.
3. Export a table to CSV.

## Flashcard prompts

- How do you list tables in sqlite3?
- How do you see a table's columns?
- Why use `-readonly` on evidence?
- What does `GROUP BY` do?

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
