# readelf-objdump: the expanded manual

> Captured 2026-11-23 on Ubuntu 24.04 (WSL): `GNU readelf (GNU Binutils for Ubuntu) 2.42`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox).

**In one line:** Read a Linux program without running it: headers, symbols, sections, protections and disassembly.

## When you reach for it (in a CTF or defence task)

- First look at a binary challenge: architecture, symbols, protections.
- Find the function that checks the password and read its assembly.
- See which strings and constants are stored in the file.

## Anatomy of a command

```text
readelf  -h  hello           # ELF header: class (32/64-bit), machine, entry point
readelf  -s  hello           # symbol table: function and variable names
readelf  -lW hello           # program headers: look for GNU_STACK (executable stack?)
objdump  -d -M intel hello   # disassemble code, Intel syntax
objdump  -s -j .rodata hello # hex dump of one section
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `readelf -h` | ELF header | 32-bit or 64-bit? which CPU? |
| `readelf -S / -lW` | Section headers / program headers (wide) | Stack flags, section layout |
| `readelf -s` | Symbols | Function names in a non-stripped binary |
| `readelf -p .rodata` | Print a section as strings | Constants and messages |
| `objdump -d` | Disassemble executable sections | Read the logic |
| `-M intel` | Intel syntax instead of AT&T | Easier to read, matches most tutorials |
| `--no-show-raw-insn` | Hide the machine-code bytes | Shorter output |
| `objdump -s -j SECTION` | Hex dump of a section | Data tables, embedded text |
| `nm / file / strings` | Related quick checks | Symbols, type, text |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. What kind of program is it?

The ELF header tells you the word size, CPU, and whether the program is position independent.

```bash
$ readelf -h hello | grep -E 'Class|Machine|Type|Entry'
```

```text
  Class:                             ELF64
  Type:                              DYN (Position-Independent Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Entry point address:               0x1080
```

64-bit x86-64 and a position-independent executable (type `DYN`). This decides which debugger setup and which addresses to expect.

### 2. Which functions does it have or use?

Symbols list what the program defines (`main`) and imports from libc (`puts`, `strcmp`).

```bash
$ readelf -s hello | grep -E ' main$| puts| strcmp'
```

```text
     3: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.2.5 (3)
    21: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.2.5
    25: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strcmp@GLIBC_2.2.5
    32: 0000000000001169   110 FUNC    GLOBAL DEFAULT   16 main
```

Seeing `strcmp` hints at a password comparison. A stripped binary has no names, so this shows less.

### 3. Is the stack executable?

`GNU_STACK` flags `RW` mean a non-executable stack (NX). `RWE` would allow shellcode on the stack, as in Narnia.

```bash
$ readelf -lW hello | grep -E 'GNU_STACK|GNU_RELRO'
```

```text
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x10
  GNU_RELRO      0x002db0 0x0000000000003db0 0x0000000000003db0 0x000250 0x000250 R   0x1
```

The stack segment is read-write only, which is the modern default. Narnia's binaries differ.

### 4. Read the strings the program stores

`.rodata` holds constants such as string literals.

```bash
$ readelf -p .rodata hello
```

```text

String dump of section '.rodata':
  [     4]  flag{demo_not_a_real_flag}
  [    1f]  open-sesame
  [    2b]  access denied
```

The secret passphrase, the denied message and the flag text, all visible without running anything.

### 5. Disassemble main

`-d` disassembles; `sed -n '/start/,/end/p'` prints just one function.

```bash
$ objdump -d -M intel --no-show-raw-insn hello | sed -n '/<main>:/,/ret/p'
```

```text
0000000000001169 <main>:
    1169:	endbr64
    116d:	push   rbp
    116e:	mov    rbp,rsp
    1171:	sub    rsp,0x20
    1175:	mov    DWORD PTR [rbp-0x14],edi
    1178:	mov    QWORD PTR [rbp-0x20],rsi
    117c:	lea    rax,[rip+0xe81]        # 2004 <_IO_stdin_used+0x4>
    1183:	mov    QWORD PTR [rbp-0x8],rax
    1187:	cmp    DWORD PTR [rbp-0x14],0x1
    118b:	jle    11c1 <main+0x58>
    118d:	mov    rax,QWORD PTR [rbp-0x20]
    1191:	add    rax,0x8
    1195:	mov    rax,QWORD PTR [rax]
    1198:	lea    rdx,[rip+0xe80]        # 201f <_IO_stdin_used+0x1f>
    119f:	mov    rsi,rdx
    11a2:	mov    rdi,rax
    11a5:	call   1070 <strcmp@plt>
    11aa:	test   eax,eax
    11ac:	jne    11c1 <main+0x58>
    11ae:	mov    rax,QWORD PTR [rbp-0x8]
    11b2:	mov    rdi,rax
    11b5:	call   1060 <puts@plt>
    11ba:	mov    eax,0x0
    11bf:	jmp    11d5 <main+0x6c>
    11c1:	lea    rax,[rip+0xe63]        # 202b <_IO_stdin_used+0x2b>
    11c8:	mov    rdi,rax
    11cb:	call   1060 <puts@plt>
    11d0:	mov    eax,0x1
    11d5:	leave
```

Look for `cmp`/`call strcmp` followed by a conditional jump (`je`/`jne`): that branch decides whether you get the secret. The `lea` instructions load the string addresses you saw in `.rodata`.

### 6. Hex dump of a section

`-s` prints a section as hex and ASCII, so you can check offsets and hidden bytes.

```bash
$ objdump -s -j .rodata hello
```

```text

hello:     file format elf64-x86-64

Contents of section .rodata:
 2000 01000200 666c6167 7b64656d 6f5f6e6f  ....flag{demo_no
 2010 745f615f 7265616c 5f666c61 677d006f  t_a_real_flag}.o
 2020 70656e2d 73657361 6d650061 63636573  pen-sesame.acces
 2030 73206465 6e696564 00                 s denied.       
```

The same constants in hex form with their addresses.

## Mistakes people make

- Stripped binaries have no function names: you will see `sub_...` in decompilers and unnamed code here.
- AT&T syntax (the default) puts source before destination; add `-M intel` for the order most books use.
- PIE binaries show small addresses until loaded; the real addresses change each run unless ASLR is off.
- `objdump` shows what is in the file, not what a packed or obfuscated program does after it unpacks itself.

## Related tools

ghidra, gdb, radare2 / cutter, ltrace, strace, checksec, nm, strings

## Practice

1. Find the address of the string `access denied` and the instruction that loads it.
2. Compile `hello.c` with `-no-pie -fno-stack-protector -z execstack` and compare the `GNU_STACK` line.
3. Work out which register holds `argv[1]` at the `strcmp` call.

## Flashcard prompts

- What does `readelf -h` tell you?
- What does `GNU_STACK RWE` mean?
- What does `-M intel` change?
- Where are string literals stored in an ELF file?

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
