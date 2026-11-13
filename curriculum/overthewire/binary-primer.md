# Binary exploitation primer (for Narnia, Behemoth, Utumno, Maze)

Read this once before Narnia. These games use 32-bit x86 Linux programs that run with the next level's privileges (setuid). You break the program, get a shell as that user, and read the next password. This is also the CyberSci "beginner binary exploitation" skill.

Status: concept reference, safe to publish. Use only on OverTheWire or your own lab.

## 1. The stack in one picture

```
high addresses
+----------------------+
| argv / environment   |   <- environment variables live up here
+----------------------+
| return address       |   <- where the function goes back to when it finishes
| saved base pointer   |
| local variables      |   <- e.g. char buf[128]
| ... buffer grows up  |
+----------------------+
low addresses           writes go UPWARD toward the return address
```

An overflow is writing past the end of `buf` until you reach something important: a nearby variable (Narnia 0), a function pointer, or the return address.

## 2. The standard workflow

1. Read the C source (given in `/narnia/` and `/behemoth/`): find the unsafe call (`strcpy`, `gets`, `scanf("%s")`, `printf(user_input)`, `system`).
2. `file` and `checksec` (or `readelf -l`): is the stack executable? is there a stack canary? is ASLR on (`cat /proc/sys/kernel/randomize_va_space`)?
3. Find the offset: send a cyclic pattern in `gdb`, read the crashed `eip` value, compute where it sits.
4. Decide the target: change a variable, jump to existing code, or jump to your own shellcode.
5. Build the payload in Python; test in `gdb` with the same environment (stack addresses shift with env size and program name).
6. Run it for real, outside gdb.

```
payload = [ padding up to the return address ][ new return address ][ shellcode or arguments ]
```

## 3. Tools

| Tool | Use |
|---|---|
| `gdb` + `pwndbg`/`gef`/PEDA | step, inspect registers and stack, `x/32wx $esp`, `info registers` |
| `pwn cyclic` (pwntools) or `msf-pattern_create` | find the exact offset |
| `objdump -d`, `readelf`, `nm` | find function and symbol addresses |
| `ltrace`/`strace` | see library and system calls |
| `python3 -c 'print(...)'` or pwntools | build payloads |

## 4. Four ideas, one line each

- **Variable overwrite:** change a nearby variable to the value the program wants (Narnia 0).
- **Shellcode:** put machine code that runs `/bin/sh` into a buffer or environment variable, then redirect `eip` to it.
- **Format string:** `printf(user_input)` lets `%x` read memory and `%n` write memory.
- **ret2libc:** instead of shellcode, return into `system()` with `"/bin/sh"` as its argument (works when the stack is not executable).

## 5. Format strings in one picture

```
printf(buf)   with buf = "AAAA%x.%x.%x.%x"
   prints your own stack words:  41414141 shows up -> you can find YOUR input on the stack
   then "%N$n" writes the number of characters printed so far to the address at stack word N
```
So you place a target address in your input, find its position `N` with `%N$x`, print exactly the value you need, then write with `%N$n`. Use `%hn` to write 2 bytes at a time.

## 6. SUID gotcha

If the shell you get runs with your own user, `bash` dropped privileges. Use `/bin/sh -p`, or shellcode that calls `setreuid(geteuid(), geteuid())` first. Check with `id`.

## 7. Tidy habits

- Work in `mktemp -d`, never in the level folder. Don't leave payload files lying around.
- Note offsets, addresses and the command that worked: you will reuse them.
- ASLR may be off on these servers but verify; if addresses move, use a NOP sled or leak an address first.
