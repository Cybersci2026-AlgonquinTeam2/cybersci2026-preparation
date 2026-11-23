# openssl: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** A crypto toolbox: hashes, encoding, symmetric encryption, certificates and keys, from one command.

## When you reach for it (in a CTF or defence task)

- Hash a string or file; compare with a checksum.
- Encode/decode base64; try AES with a known key.
- Read a certificate or CSR (picoCTF 'ReadMyCert').
- Check RSA keys in a challenge.

## Anatomy of a command

```text
openssl  dgst  -sha256  file
   |       |      |        '--- input (stdin if omitted)
   |       |      '--- algorithm option
   |       '--- sub-command (dgst, enc, x509, req, rsa, base64, rand ...)
   '--- the program
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `dgst -sha256 / -md5` | Hash input | Checksums, flag verification |
| `base64 [-d]` | Base64 encode / decode | Quick encoding |
| `enc -aes-256-cbc -pbkdf2 -k PASS` | Encrypt with a password (adds a random salt) | Lab encryption |
| `enc -aes-128-ecb -K HEX -nosalt` | Raw AES with a hex key and no salt | Study modes such as ECB |
| `-d` | Decrypt (with `enc`) | Reverse the above |
| `x509 -in cert -noout -subject -dates` | Show certificate fields | Read a certificate |
| `req -x509 -newkey rsa:2048 -nodes` | Make a self-signed certificate | Lab TLS |
| `rsa -in key -text -noout` | Show RSA key parameters | RSA challenges (n, e) |
| `rand -hex N` | N random bytes as hex | Keys and test data |
| `s_client -connect host:443` | Talk TLS to a server | Check a certificate chain |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Hash a string (and avoid the newline trap)

`echo` adds a newline unless you use `-n`. A different input gives a completely different hash.

```bash
$ echo -n hello | openssl dgst -sha256; echo hello | openssl dgst -sha256
```

```text
SHA2-256(stdin)= 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
SHA2-256(stdin)= 5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
```

Two different hashes for what looks like the same word. This is a common source of 'wrong hash' errors in CTFs.

### 2. Base64 both ways

Base64 is an encoding (anyone can reverse it), not encryption.

```bash
$ printf 'hello world' | openssl base64; echo ---; cat data.b64 | openssl base64 -d; echo
```

```text
aGVsbG8gd29ybGQ=
---
hello world
```

Encoding the text gives a string ending in `=`; decoding `data.b64` returns `hello world`.

### 3. Encrypt with a password and look at the file

With a password, OpenSSL writes the header `Salted__` and 8 salt bytes, then the ciphertext.

```bash
$ printf 'secret message' | openssl enc -aes-256-cbc -pbkdf2 -k letmein -out enc.bin; head -c 16 enc.bin | xxd; openssl enc -d -aes-256-cbc -pbkdf2 -k letmein -in enc.bin; echo
```

```text
00000000: 5361 6c74 6564 5f5f 2e72 ded1 4ff5 4056  Salted__.r..O.@V
secret message
```

The first bytes spell `Salted__`; decryption with the same password returns the message. A random salt means two runs give different files.

### 4. ECB mode leaks patterns

ECB encrypts each 16-byte block independently, so equal plaintext blocks give equal ciphertext blocks.

```bash
$ printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | openssl enc -aes-128-ecb -K 000102030405060708090a0b0c0d0e0f -nosalt | xxd -c 16
```

```text
00000000: dd4b 1a0b 47da a706 7d0b 59d9 5d58 a6ae  .K..G...}.Y.]X..
00000010: dd4b 1a0b 47da a706 7d0b 59d9 5d58 a6ae  .K..G...}.Y.]X..
00000020: 954f 64f2 e4e8 6e9e ee82 d202 1668 4899  .Od...n......hH.
```

The first two ciphertext lines are identical because the plaintext had two identical blocks (the third line is padding). This is exactly the weakness behind Natas 28 and the CyberSci block-swapping challenge.

### 5. Read a certificate

First we create a throw-away self-signed certificate, then read its fields with `x509 -noout`.

```bash
$ openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -subj '/CN=demo.local/O=Lab' -days 1 2>/dev/null; openssl x509 -in c.pem -noout -subject -issuer
```

```text
subject=CN = demo.local, O = Lab
issuer=CN = demo.local, O = Lab
```

Subject and issuer are the same because it is self-signed. Add `-dates` or `-text` to see validity and the key.

## Mistakes people make

- `echo` without `-n` hashes a trailing newline.
- `-pbkdf2` and `-md sha256` differ across OpenSSL versions: decrypting old files may need the original options.
- `openssl enc` is for study: never design real encryption with raw `enc`.
- CSR vs certificate vs key are different PEM types: check the header line (`-----BEGIN ...`).

## Related tools

sha256sum / md5sum, base64, gpg, hashcat, RsaCtfTool, python pycryptodome

## Practice

1. Encrypt a 48-byte message of repeating blocks with ECB and with CBC and compare the dumps.
2. Hash the contents of `hello.c` and verify with `sha256sum`.
3. Create a certificate with a different CN and read it back.

## Flashcard prompts

- Why do `echo hello` and `echo -n hello` hash differently?
- What does the `Salted__` header mean?
- Why is ECB insecure?
- How do you read a certificate's subject?

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
