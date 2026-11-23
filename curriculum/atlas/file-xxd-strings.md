# file-xxd-strings: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `file-5.45`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** The first three commands for any unknown file: what is it (`file`), what are its bytes (`xxd`), what text is inside (`strings`).

## When you reach for it (in a CTF or defence task)

- Triage every supplied file before you open or run it.
- The extension and the contents disagree (a `.txt` that is really a PNG).
- Find hidden or appended data, magic bytes, embedded paths and flags.

## Anatomy of a command

```text
file   -k  holiday.txt          # what do the first bytes say it is?
xxd    -l 32  pic.png          # show the first 32 bytes in hex + ASCII
strings -n 8 -t x  hello       # printable runs of 8+ characters, with their hex offset
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `file -k` | Keep going: show all matches, not just the first | Polyglots and odd formats |
| `file -i` | MIME type output | Scripts and quick filters |
| `xxd -l N / -s OFFSET` | Read N bytes / start at an offset (negative = from the end) | Look at a header or a trailer |
| `xxd -c N / -g N` | Bytes per line / group size | Make the layout fit your screen |
| `xxd -p` | Plain hex without offsets | Copy bytes into a script |
| `xxd -r -p` | Reverse: hex text back into bytes | Decode a hex string |
| `strings -n N` | Minimum length of a string (default 4) | Cut noise |
| `strings -a` | Scan the whole file (not only data sections) | Be sure you did not skip anything |
| `strings -t x` | Print the offset of each string (hex) | Jump to the spot in `xxd` |
| `strings -e l` | UTF-16 little-endian strings | Windows text, memory images |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. What is this file really?

`file` reads the first bytes (magic numbers), not the name. `holiday.txt` is a copy of the PNG.

```bash
$ file hello pic.png holiday.txt notes.txt.gz access.log
```

```text
hello:        ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2f3fb8ed1f8be6
pic.png:      PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
holiday.txt:  PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
notes.txt.gz: gzip compressed data, was "notes.txt", last modified: Mon Nov 23 19:12:15 2026, from Unix, original size modulo 2^32 174
access.log:   ASCII text
```

The `.txt` file is identified as a PNG, the gzip as gzip, the binary as an ELF executable. Never trust an extension.

### 2. Look at a header

`-l 32` limits to 32 bytes. Left: offset. Middle: hex bytes. Right: printable ASCII.

```bash
$ xxd -l 32 pic.png
```

```text
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0001 0000 0001 0802 0000 0090 7753  ..............wS
```

`89 50 4e 47` is the PNG signature (`.PNG`). Every format has one; learn the common ones (PK zip, `%PDF`, ELF `7f 45 4c 46`).

### 3. Look at the end of a file

A negative `-s` counts from the end. Data after the format's end marker is a classic hiding place.

```bash
$ xxd -s -40 pic.png
```

```text
0000003f: 4e44 ae42 6082 6869 6464 656e 3a20 666c  ND.B`.hidden: fl
0000004f: 6167 7b64 656d 6f5f 6e6f 745f 615f 7265  ag{demo_not_a_re
0000005f: 616c 5f66 6c61 677d                      al_flag}
```

After the PNG end chunk (`IEND`) there is readable text that the picture viewer never shows.

### 4. Readable strings with offsets

`-t x` prints each string's offset in hex. The pipe keeps the interesting lines.

```bash
$ strings -n 8 -t x hello | grep -E 'flag|sesame|denied'
```

```text
   2004 flag{demo_not_a_real_flag}
   201f open-sesame
   202b access denied
```

The secret text sits in the binary. Note that the passphrase `open-sesame` is visible as a string too: strings often reveals comparison values.

### 5. Convert hex text back to bytes

`-r -p` reverses plain hex into bytes. The extra `echo` adds a newline.

```bash
$ echo '666c61677b6865787d' | xxd -r -p; echo
```

```text
flag{hex}
```

Hex that looks random is often just ASCII. This one decodes to a flag-shaped string.

### 6. UTF-16 text hides from plain strings

Windows stores text as 16-bit characters, so there are NUL bytes between letters and plain `strings` finds nothing.

```bash
$ printf 'p\0a\0s\0s\0w\0o\0r\0d\0' > wide.bin; strings wide.bin; echo '--- with -e l:'; strings -e l wide.bin
```

```text
--- with -e l:
password
```

The first command prints nothing; the second recovers `password`. Use `-e l` on memory dumps and Windows artefacts.

## Mistakes people make

- `file` can be wrong for polyglots (one file valid as two formats): use `file -k` and a format-specific parser.
- `strings` shows only runs of printable characters; encoded or compressed data will not appear.
- Hex dumps show bytes in file order; multi-byte numbers in x86 files are little-endian (`ef be ad de` = `0xdeadbeef`).
- Do not execute an unknown file to see what it does: analyse it first.

## Related tools

binwalk, exiftool, hexdump -C, od, readelf, objdump

## Practice

1. Work out the real type of `holiday.txt` and extract the hidden text from its end.
2. Find the byte offset of `flag{` in `hello` and view the bytes around it with `xxd -s`.
3. Decode `aGVsbG8gd29ybGQ=` using only commands from this page.

## Flashcard prompts

- What does `file` read to decide a type?
- What does the PNG signature look like in hex?
- Why does `strings` miss Windows text?
- How do you view the last 40 bytes of a file in hex?

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
