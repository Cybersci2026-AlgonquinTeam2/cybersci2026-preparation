# gdb: the expanded manual

> **Not captured yet** (gdb not installed here). The outputs below are marked *expected*: they describe what you should see. Run `python3 scripts/atlas_build.py --tool gdb` on a machine that has the tool (Kali has it) to replace them with real captured output.

**In one line:** Run a program under a debugger: stop it, look at registers and memory, step instruction by instruction.

## When you reach for it (in a CTF or defence task)

- Binary exploitation: find the offset that overwrites the return address.
- Reverse engineering: watch what a check compares.
- See what a crashed program was doing.

## Anatomy of a command

```text
gdb  -q  --args ./hello open-sesame
 |    |       '--- everything after --args is the program and its arguments
 |    '--- quiet: no banner
 '--- the debugger

inside gdb:   break main    run    next / step    info registers    x/20wx $esp    bt    continue    quit
```

## The flags worth knowing

| Flag | What it does | Reach for it when |
|---|---|---|
| `break FUNC / b *ADDR` | Set a breakpoint | Stop where something interesting happens |
| `run [args] / r` | Start the program | Begin |
| `next / step / nexti / stepi` | Step over / into a call; by source line or instruction | Follow the logic |
| `continue / c` | Resume | Run to the next breakpoint |
| `info registers / p $rip` | Show registers | Where is the program, what are the values |
| `x/20wx $esp / x/s ADDR / x/10i $rip` | Examine memory: words, string, instructions | Look at the stack, strings or code |
| `disassemble main / set disassembly-flavor intel` | Show code; Intel syntax | Read assembly |
| `bt` | Backtrace: the call stack | After a crash |
| `pattern create N / pattern offset X` | Cyclic pattern helpers (pwndbg/GEF) | Find an overflow offset |
| `-ex 'cmd' -batch` | Run commands non-interactively | Scripts |

## Recipes with real output

The lab folder used for these examples is created fresh each build (see the bottom of this page).

### 1. Break at main and look at registers

`-batch -ex` runs gdb commands without the interactive prompt.

```bash
$ gdb -q -batch -ex 'break main' -ex 'run' -ex 'info registers rip' ./hello
```

```text
(expected, not captured) Breakpoint 1, 0x... in main () followed by a line like rip 0x55555555513d showing the instruction pointer.
```

`rip` (64-bit instruction pointer) is where the program stopped.

### 2. Disassemble main in Intel syntax

The same view as `objdump -d` but inside the debugger.

```bash
$ gdb -q -batch -ex 'set disassembly-flavor intel' -ex 'disassemble main' ./hello
```

```text
(expected, not captured) Assembly of main with addresses, including a call to strcmp and a conditional jump.
```

Find the `cmp`/`test` and the following jump: that is the decision.

### 3. Crash it and read the registers

This is the Narnia method: send a long input and see which bytes reach the instruction pointer.

```bash
$ gdb -q -batch -ex 'run $(python3 -c "print(chr(65)*200)")' -ex 'info registers rip' ./hello
```

```text
(expected, not captured) Possibly no crash for this program; for a vulnerable one: Program received signal SIGSEGV and rip showing the overwritten value (such as 0x4141414141414141).
```

If `rip` holds your pattern, you control execution: compute the offset with a cyclic pattern.

### 4. Print a string from memory

`x/s` examines memory as a string; use `x/10i` for instructions and `x/20wx` for words.

```bash
$ gdb -q -batch -ex 'break main' -ex 'run' -ex 'x/s $rip' ./hello
```

```text
(expected, not captured) A line starting with the address and the bytes at it interpreted as text or instructions.
```

Learn the three formats: `s` string, `i` instruction, `x` hex.

## Mistakes people make

- Stack addresses in gdb differ from the real run (environment size and path): sweep or leak the real address.
- gdb disables ASLR by default; the real program may randomise.
- Set-uid programs lose privileges under gdb.
- Install pwndbg or GEF for a readable display.

## Related tools

pwndbg / GEF, objdump, ltrace / strace, ghidra, pwntools

## Practice

1. Find which instruction of `hello` compares your argument.
2. Change `argv[1]` in memory so the check passes.
3. Use `x/20wx $rsp` to dump the stack at `main`.

## Flashcard prompts

- What does `break main` do?
- What do `x/s`, `x/i` and `x/x` print?
- Why do addresses differ inside gdb?
- How do you run gdb commands from a script?

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
