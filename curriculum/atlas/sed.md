# sed: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `sed (GNU sed) 4.9`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** A stream editor: read lines, change them with rules (mostly search-and-replace), print the result.

## When you reach for it (in a CTF or defence task)

- Clean up or transform text in a pipeline: strip prefixes, replace separators, mask secrets.
- Print a range of lines from a big file.
- Edit a file in place (with a backup).

## Anatomy of a command

```text
sed  -E  's/(alice|bob)/[\1]/g'  users.txt
 |    |        |     |       |  |
 |    |        |     |       |  '--- g = replace every match on the line (default is the first only)
 |    |        |     |       '--- replacement; \1 is the first group; & is the whole match
 |    |        |     '--- pattern
 |    |        '--- s = substitute command
 |    '--- -E = extended regex
 '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `s/old/new/` | Substitute: the core command | Replace text |
| `g / I` | Flags on `s`: all matches / ignore case | Replace everything, any case |
| `-n and p` | Quiet mode plus print | Print only chosen lines |
| `-E` | Extended regex | Groups and alternation without backslashes |
| `-i[SUFFIX]` | Edit the file in place (`-i.bak` keeps a backup) | Change a file; use a backup suffix |
| `N,Md / Np` | Delete / print lines N to M | Cut a section out |
| `/regex/d` | Delete lines that match | Remove noise |
| `-e A -e B` | Several commands | Several edits in one pass |
| `y/abc/xyz/` | Transliterate characters one-to-one | ROT13-style swaps |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Replace a separator

`s/old/new/g` replaces every colon on each line. Without `g` only the first per line changes.

```bash
$ sed 's/:/ | /g' users.txt | head -2
```

```text
root | x | 0 | 0 | root | /root | /bin/bash
alice | x | 1001 | 1001 | Alice Lee | /home/alice | /bin/bash
```

Fields are now separated by ` | `. The original file is untouched: sed prints to the screen.

### 2. Print only chosen lines

`-n` turns off automatic printing; `2,3p` prints lines 2 to 3.

```bash
$ sed -n '2,3p' users.txt
```

```text
alice:x:1001:1001:Alice Lee:/home/alice:/bin/bash
bob:x:1002:1002:Bob Ray:/home/bob:/bin/sh
```

Just alice and bob. Same idea: `sed -n '/ 401 /p'` prints matching lines like grep.

### 3. Delete lines

`/regex/d` removes lines that match. The rest are printed.

```bash
$ sed '/nologin/d' users.txt
```

```text
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice Lee:/home/alice:/bin/bash
bob:x:1002:1002:Bob Ray:/home/bob:/bin/sh
```

The service account with the nologin shell disappears.

### 4. Use a captured group

`(..)` captures; `\1`, `\2` insert the captures; `.*` swallows the rest of the line.

```bash
$ sed -E 's/^([a-z-]+):x:([0-9]+):.*/user=\1 uid=\2/' users.txt
```

```text
user=root uid=0
user=alice uid=1001
user=bob uid=1002
user=svc-backup uid=998
```

A compact table of user and uid. Capture groups are the main reason to learn sed.

### 5. Mask secrets

Keep the label in group 1 and replace the secret. Useful before sharing a log.

```bash
$ sed -E 's/(Password reset for [a-z]+: ).*/\1[REDACTED]/' notes.txt | head -3
```

```text
Meeting at 3pm
Password reset for bob: [REDACTED]
TODO: rotate keys
```

The password text is replaced while the rest of the line stays.

### 6. Edit a file in place, with a backup

`-i.bak` rewrites `copy.txt` and saves the original as `copy.txt.bak`. `diff` shows what changed.

```bash
$ cp users.txt copy.txt; sed -i.bak 's/bash/zsh/' copy.txt; diff copy.txt.bak copy.txt
```

```text
1,2c1,2
< root:x:0:0:root:/root:/bin/bash
< alice:x:1001:1001:Alice Lee:/home/alice:/bin/bash
---
> root:x:0:0:root:/root:/bin/zsh
> alice:x:1001:1001:Alice Lee:/home/alice:/bin/zsh
```

Two lines changed from bash to zsh and the backup holds the original. Never use bare `-i` on something you cannot recover.

### 7. ROT13 with y///

`y/from/to/` maps characters one for one.

```bash
$ echo 'synt{ebg13}' | sed 'y/abcdefghijklmnopqrstuvwxyz/nopqrstuvwxyzabcdefghijklm/'
```

```text
flag{rot13}
```

`synt{ebg13}` becomes `flag{rot13}`. The same shift decodes and encodes.

## Mistakes people make

- On macOS `sed -i` needs an argument (`sed -i ''`): scripts differ between GNU and BSD sed.
- Use a different delimiter for paths: `s#/usr/bin#/opt#`.
- `&` in the replacement means the whole match; escape it (`\&`) for a literal ampersand.
- sed works line by line; to edit across lines use `-z` or switch to Python.

## Related tools

awk, tr, perl -pe, ed, python -c

## Practice

1. Turn `users.txt` into `name -> shell` lines.
2. Print only line 4 of `access.log`.
3. Replace every IP in `access.log` with `x.x.x.x`.

## Flashcard prompts

- What does `s/a/b/g` do?
- What does `sed -n '5,9p'` do?
- How do you keep a backup when editing in place?
- What do `\1` and `&` mean in a replacement?

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
