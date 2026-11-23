# find: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `find (GNU findutils) 4.9.0`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Walk a folder tree and list (or act on) files that match conditions such as name, size, type, time or permissions.

## When you reach for it (in a CTF or defence task)

- Locate a file when you only know part of its name, its type or when it changed.
- Privilege escalation checks: world-writable files, SUID binaries, files owned by a user.
- Run a command on every matching file (`-exec`).

## Anatomy of a command

```text
find  site  -type f  -name '*.js'  -size -1k  -exec wc -c {} \;
 |     |      |         |            |           '--- run a command; {} is the file; \; ends it
 |     |      |         |            '--- tests are ANDed together in order
 |     |      |         '--- match the name against a glob (quote it)
 |     |      '--- f = regular file, d = directory, l = symlink
 |     '--- where to start looking
 '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-name / -iname` | Match the file name with a glob (`-iname` ignores case) | You remember part of the name |
| `-type f|d|l` | Regular file, directory or symlink | Skip folders or find links |
| `-maxdepth N / -mindepth N` | Limit how deep to look | Avoid huge trees |
| `-size +1M / -1k` | Bigger / smaller than a size (`c` bytes, `k`, `M`) | Find big dumps or tiny stubs |
| `-mtime N / -mmin N` | Modified N days / minutes ago (`-1` = less than, `+1` = more than) | What changed during the incident? |
| `-newer FILE` | Newer than another file | What changed after the first alert? |
| `-perm -4000 / -perm /111` | Has all of these bits / any of these bits | SUID files, executable files |
| `-user NAME / -group NAME` | Owned by | Files an attacker or service user created |
| `-empty` | Empty files and folders | Clean-up or odd leftovers |
| `-exec CMD {} \; / -exec CMD {} +` | Run CMD per file / on batches of files | Search or hash every match |
| `-print0 | xargs -0` | Null-separated output for safe piping | File names with spaces |
| `-delete` | Delete matches (dangerous: test first with `-print`) | Clean-up only |
| `! / -not / -o` | NOT / OR combinators (group with `\( \)`) | More complex conditions |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. List everything below a folder

With no tests, find prints every path. `sort` makes the order stable (find prints in disk order).

```bash
$ find site | sort
```

```text
site
site/.env
site/css
site/css/main.css
site/index.html
site/js
site/js/app.js
site/robots.txt
site/uploads
site/uploads/report.pdf
```

Folders and files, including the hidden `.env`.

### 2. By name, any depth

`-name` takes a glob. Quote it so the shell does not expand it first.

```bash
$ find . -name '*.js' | sort
```

```text
./site/js/app.js
```

One JavaScript file. `-iname` would also catch `APP.JS`.

### 3. Hidden files only

Names starting with a dot are hidden from plain `ls`. Config files and secrets often live there.

```bash
$ find site -name '.*' -type f
```

```text
site/.env
```

The `.env` file appears.

### 4. Executable files

`/111` means any execute bit is set. `-maxdepth 1` stays in this folder.

```bash
$ find . -maxdepth 1 -type f -perm /111 | sort
```

```text
./hello
./run.sh
```

The compiled `hello` and the script `run.sh`. In a real privilege-escalation check you search `-perm -4000` for SUID.

### 5. By age

`-newer` compares modification times with a reference file. I set two files to an older date on purpose.

```bash
$ find site -type f -newer site/robots.txt | sort
```

```text
site/.env
site/css/main.css
site/js/app.js
site/uploads/report.pdf
```

Files modified after `robots.txt`: everything except the two aged files. Use this to find what changed after an alert.

### 6. Run a command on each match

`-exec` replaces `{}` with each file name. `\;` runs the command once per file; `+` batches many files into one run.

```bash
$ find site -type f -exec grep -l 'x' {} \; | sort
```

```text
site/uploads/report.pdf
```

The names of files that contain the letter x.

### 7. Safe piping with spaces in names

Without `-print0`/`-0`, a name with a space splits into two arguments and breaks the next command.

```bash
$ touch 'a file.txt'; find . -name '*.txt' -print0 | xargs -0 wc -c | tail -3
```

```text
  0 ./a file.txt
103 ./holiday.txt
471 total
```

`wc` reports on `a file.txt` correctly because the names were separated by NUL bytes.

## Mistakes people make

- Quote globs: `find . -name *.js` can be expanded by the shell and fail.
- Order matters for performance, not logic: put cheap tests (`-type`, `-name`) before `-exec`.
- `-mtime -1` means less than 24 hours ago, `-mtime 1` means exactly 1 day: easy to mix up.
- `-delete` placed before the tests deletes everything: always run with `-print` first.
- `find /` as a normal user prints many `Permission denied` lines; add `2>/dev/null`.

## Related tools

locate, fd, ls -la, xargs, stat, du

## Practice

1. Find every file in `site` larger than 5 bytes.
2. List only directories two levels deep.
3. Find files owned by your user that are not readable by others.

## Flashcard prompts

- What does `-perm -4000` find?
- Why use `-print0 | xargs -0`?
- `-exec ... \;` versus `-exec ... +`?
- How do you find files changed in the last 30 minutes?

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
