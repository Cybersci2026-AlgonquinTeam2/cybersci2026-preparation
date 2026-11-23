# grep: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `grep (GNU grep) 3.11`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Search text (or binary data) for lines that match a pattern, and print them.

## When you reach for it (in a CTF or defence task)

- Find a flag, password or username inside a log, dump, memory image or whole folder.
- Count or list evidence: failed logins, an IP, a path, a user agent.
- Filter the output of another command (`cmd | grep ...`).

## Anatomy of a command

```text
grep  -i  -n  -E  'pattern'  file1 file2
 |    |   |   |     |         '--- files to search (or a folder with -r; or stdin if omitted)
 |    |   |   |     '------------- the pattern (quote it so the shell leaves it alone)
 |    |   |   '------------------- -E = extended regular expressions (+ ? | () work)
 |    |   '----------------------- -n = print line numbers
 |    '--------------------------- -i = ignore upper/lower case
 '-------------------------------- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-i` | Ignore case | You do not know if it is `Password` or `PASSWORD` |
| `-v` | Invert: show lines that do NOT match | Remove the noise to see what is left |
| `-n` | Prefix lines with their line number | You need to open the file at that spot later |
| `-c` | Count matching lines instead of printing them | How many failures? how many hits? |
| `-o` | Print only the matching part | Pull out IPs, emails, flags |
| `-E` | Extended regex (`+ ? | ( )` need no backslash) | Anything beyond a plain word |
| `-F` | Fixed string: treat the pattern as plain text | The pattern has `{ } . * [` characters you want literally |
| `-w / -x` | Match whole words / whole lines only | `root` should not match `rootkit` |
| `-r / -R` | Recurse into folders (-R follows symlinks) | Search a whole project or extracted archive |
| `-l / -L` | List only file names that do / do not match | Which files contain it? |
| `-A N / -B N / -C N` | Show N lines After / Before / around the match | Read the context of a hit |
| `-a` | Treat binary files as text | Search images, binaries, memory dumps |
| `-b` | Print the byte offset of each match | Locate data inside a binary for `xxd`/`dd` |
| `--include='*.py' / --exclude-dir=.git` | Limit which files a recursive search reads | Large trees with noise |
| `-P` | Perl-style regex (lookahead, `\d`) | Complex patterns; not available on every system |
| `-m N` | Stop after N matches | Huge files; you only need the first hit |
| `-q` | Quiet: no output, just the exit status | Use in `if grep -q ...; then` |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Find a word, ignoring case, with line numbers

Notes mix `Password` and `PASSWORD`. `-i` catches both; `-n` tells you where.

```bash
$ grep -in password notes.txt
```

```text
2:Password reset for bob: Summer2026!
4:password policy: 12 characters
6:Remember: PASSWORD files are case sensitive?
```

Three lines match even though the capitalisation differs. Without `-i` you would miss two of them.

### 2. Count failed logins

`-c` prints a number instead of the lines. The spaces around `401` avoid matching `4010` or a byte count.

```bash
$ grep -c ' 401 ' access.log
```

```text
3
```

The number is how many lines contain the HTTP status 401 (unauthorised).

### 3. Everything except the boring lines

`-v` inverts the match. Drop the normal successes and read what is left.

```bash
$ grep -v ' 200 ' access.log
```

```text
10.0.0.9 - - [14/Nov/2026:10:02:01 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:03 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:05 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:09 +0000] "POST /login HTTP/1.1" 302 0
10.0.0.7 - - [14/Nov/2026:10:03:40 +0000] "GET /../../etc/passwd HTTP/1.1" 400 0
10.0.0.7 - - [14/Nov/2026:10:03:44 +0000] "GET /backup.zip HTTP/1.1" 404 196
```

Failed logins, a redirect, a path traversal attempt and a 404 remain. This is how you triage a log.

### 4. Ranked list of source IPs (pipeline)

`-o` prints only the matched IP, `sort | uniq -c` counts duplicates, `sort -rn` ranks them.

```bash
$ grep -oE '^[0-9]+(\.[0-9]+){3}' access.log | sort | uniq -c | sort -rn
```

```text
      5 10.0.0.9
      2 10.0.0.7
      2 10.0.0.5
```

The first line is the noisiest client. The same pattern (match, sort, count, rank) works on usernames, paths and user agents.

### 5. Context around a hit

`-C1` shows one line before and after. A 302 after several 401s means the login finally worked.

```bash
$ grep -n -C1 ' 302 ' access.log
```

```text
5-10.0.0.9 - - [14/Nov/2026:10:02:05 +0000] "POST /login HTTP/1.1" 401 87
6:10.0.0.9 - - [14/Nov/2026:10:02:09 +0000] "POST /login HTTP/1.1" 302 0
7-10.0.0.9 - - [14/Nov/2026:10:02:15 +0000] "GET /admin HTTP/1.1" 200 2210
```

Three failures, then the redirect, then the admin page: a brute-force that succeeded.

### 6. Search a whole folder

`-r` descends into folders, `-n` adds line numbers. Hidden files (names starting with a dot) are included.

```bash
$ grep -rn 'secret' site
```

```text
site/.env:1:secret=1
```

The `.env` file shows up with its file name and line number.

### 7. Find text inside a binary file

`-a` makes grep read binary as text. This is the fastest check for data appended to an image.

```bash
$ grep -a -o 'flag{[^}]*}' pic.png
```

```text
flag{demo_not_a_real_flag}
```

A flag-shaped string was hidden after the end of the picture. (The flag here is a demo value.)

### 8. Why -F matters

In a regex the dot means 'any single character', so it matches the `x` too. `-F` matches the characters exactly as typed.

```bash
$ printf 'flag{1x3}\nflag{1.3}\n' > t.txt; echo '--- regex:'; grep 'flag{1.3}' t.txt; echo '--- fixed string:'; grep -F 'flag{1.3}' t.txt
```

```text
--- regex:
flag{1x3}
flag{1.3}
--- fixed string:
flag{1.3}
```

The regex version prints both lines; the `-F` version prints only the one with a real dot. Use `-F` for anything copied from a log, an IP or a flag.

## Mistakes people make

- Quote the pattern: unquoted `*` and `$` are expanded by the shell before grep sees them.
- `grep pattern *` skips hidden files; use `-r` on the folder.
- A dot `.` in a regex means any character; escape it (`\.`) or use `-F` for an IP such as `10.0.0.5`.
- On binary files without `-a`, grep says `Binary file matches` and prints nothing useful.
- `-P` is not in every grep (macOS, BusyBox): `-E` is the portable choice.

## Related tools

rg (ripgrep: faster, respects .gitignore), awk, sed, find, strings, zgrep (search .gz without extracting)

## Practice

1. Count how many distinct IPs hit `/login` in `access.log`.
2. List every file under `site` that contains the letter `x`, with line numbers.
3. Find the byte offset of the flag text in `pic.png`, then print the bytes there with `xxd -s`.

## Flashcard prompts

- What does `grep -c` print?
- Difference between `-F` and `-E`?
- How do you search binary files for text?
- How do you list only file names that match?
- What exit status means 'not found'?

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
