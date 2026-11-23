# python-oneliners: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `Python 3.12.3`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Use `python3 -c` for the small decode, convert and brute-force jobs that come up in every CTF.

## When you reach for it (in a CTF or defence task)

- Decode or encode base64, hex, URL or binary text.
- Convert between number bases and byte orders.
- XOR, hash, brute-force a short secret, or work out tiny RSA.
- Parse a log with Counter instead of building a long shell pipeline.

## Anatomy of a command

```text
python3  -c  "import base64; print(base64.b64decode('aGk=').decode())"
   |      |        |
   |      |        '--- a program in one string: statements separated by ;
   |      '--- -c = run the string as code (use -m for a module, - to read a script from stdin)
   '--- the interpreter
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `-c 'code'` | Run code given on the command line | Quick transforms |
| `-m http.server 8000` | Run a module: a quick web server for transfers | Serve files in a lab |
| `-i` | Stay interactive afterwards | Explore the data you loaded |
| `-` | Read the script from stdin | Here-documents with `<<'PY'` |
| `-I` | Isolated mode: ignore the current folder and user site | Safe use inside an untrusted folder |
| `-u` | Unbuffered output | Network scripts and pipes |
| `bytes.fromhex(s) / b.hex()` | Hex string to bytes and back | Decode hex |
| `int(x, base) / bin() / hex() / oct()` | Convert between bases | Binary, hex, octal puzzles |
| `struct.pack('<I', n)` | Pack a number as little-endian bytes (`>` = big-endian) | Build payloads; read binary fields |
| `pow(a, -1, m)` | Modular inverse | RSA private exponent |
| `itertools.product` | Every combination of a character set | Short brute force |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Decode base64

Base64 turns bytes into text with `A-Z a-z 0-9 + /` and `=` padding. `b64decode` returns bytes; `.decode()` makes text.

```bash
$ python3 -c "import base64; print(base64.b64decode('aGVsbG8gd29ybGQ=').decode())"
```

```text
hello world
```

You get `hello world`. If decoding fails, check for missing `=` padding, newlines or URL-safe `-_` characters.

### 2. Hex and bytes

Two directions: hex text to bytes, and text to hex.

```bash
$ python3 -c "print(bytes.fromhex('666c61677b6865787d')); print('flag'.encode().hex())"
```

```text
b'flag{hex}'
666c6167
```

The first line is a `bytes` object (note the `b'...'`), the second the hex of the word `flag`.

### 3. XOR with a repeating key

`i % len(k)` repeats the key. XOR is its own inverse, so the same code encrypts and decrypts.

```bash
$ python3 -c "d=bytes.fromhex('0b0d080c'); k=b'AB'; print(bytes(b ^ k[i % len(k)] for i, b in enumerate(d)))"
```

```text
b'JOIN'
```

The result is readable text. In Natas 11 you recover the key the same way: key = ciphertext XOR known plaintext.

### 4. Number bases

`int(text, base)` parses; `bin`, `oct`, `hex` format.

```bash
$ python3 -c "n=0xdeadbeef; print(n); print(bin(10), oct(64), hex(255)); print(int('777', 8), int('1010', 2), int('ff', 16))"
```

```text
3735928559
0b1010 0o100 0xff
511 10 255
```

Decimal for the hex value, then conversions both ways. Handy for the picoCTF 'convertme' style tasks.

### 5. Byte order (endianness)

`<` = little-endian (x86), `>` = big-endian (network). `I` = 4-byte unsigned.

```bash
$ python3 -c "import struct; print(struct.pack('<I', 0xdeadbeef).hex(), struct.pack('>I', 0xdeadbeef).hex()); print(hex(struct.unpack('<I', bytes.fromhex('efbeadde'))[0]))"
```

```text
efbeadde deadbeef
0xdeadbeef
```

The same number gives two byte orders. This is the `ef be ad de` you typed in Narnia 0.

### 6. Brute-force a short secret from its hash

Only 10,000 four-digit PINs exist, so trying them all is instant. Cost grows as alphabet^length.

```bash
$ python3 -c "import hashlib, itertools; t = hashlib.md5(b'4821').hexdigest(); print(t); print(next(''.join(c) for c in itertools.product('0123456789', repeat=4) if hashlib.md5(''.join(c).encode()).hexdigest() == t))"
```

```text
85267d349a5e647ff0a9edcb5ffd1e02
4821
```

It prints the hash and then recovers `4821`. Real password cracking uses hashcat or john, but the idea is the same.

### 7. Count things in a log

`Counter` is awk's associative array with sorting built in.

```bash
$ python3 -c "import collections; print(collections.Counter(l.split()[0] for l in open('access.log')).most_common(2))"
```

```text
[('10.0.0.9', 5), ('10.0.0.5', 2)]
```

The two busiest IPs with their counts.

### 8. Tiny RSA

With the factors p and q you can compute the private exponent d. `pow(c, d, n)` decrypts.

```bash
$ python3 -c "p, q, e = 61, 53, 17; n = p * q; d = pow(e, -1, (p - 1) * (q - 1)); m = 65; c = pow(m, e, n); print(n, d, c, pow(c, d, n))"
```

```text
3233 2753 2790 65
```

`n=3233`, `d=2753`, a ciphertext, and the original message 65 again. CTF RSA tasks give you weak numbers where you must find p and q.

## Mistakes people make

- Quote carefully: wrap the program in double quotes in bash and use single quotes inside (or the other way round).
- `print(bytes)` shows `b'...'`: call `.decode()` for text.
- Python 2 is gone: `print` needs parentheses.
- Integer division is `//`; `/` gives a float, which breaks big-number maths.
- For anything longer than three lines, write a file and add comments.

## Related tools

CyberChef, xxd, base64, pwntools, pycryptodome, sympy, z3

## Practice

1. Decode a base64 string, then hex-decode the result.
2. XOR two hex strings of equal length.
3. Find the PIN whose sha1 equals a hash of your choice.

## Flashcard prompts

- What does `python3 -c` do?
- What does `<I` mean in struct?
- How do you invert a number modulo m in Python?
- Why is XOR with a repeating key breakable?

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
