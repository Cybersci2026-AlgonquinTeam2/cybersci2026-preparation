# OverTheWire Behemoth: hints book (levels 0-8)

Behemoth builds on Narnia: buffer overflows, race conditions, environment handling and privilege escalation, difficulty 3/10, 9 levels, 32-bit x86. Connect: `ssh behemoth0@behemoth.labs.overthewire.org -p 2221`; level 0 is `behemoth0` / `behemoth0`. Programs are in `/behemoth/` (this game does not hand you source for every level: use `ltrace`, `strings`, `objdump -d` and `gdb`). Read [binary-primer.md](binary-primer.md) first.

Status: **outline only, researched-unverified, low detail.** Per-level information was not available from the official pages (they are intentionally empty) and the third-party index I found has only one-line taglines. The map below is what those taglines and general knowledge support. Treat it as a checklist of techniques to look for, and replace each row with your own findings as you play.

| Level | Likely theme | What to try first |
|---|---|---|
| 0 | warm-up: a password check | `ltrace` the binary and read the comparison |
| 1 | stack overflow | find the offset in gdb, jump to shellcode |
| 2 | input / PATH handling | look for a command run without an absolute path (PATH hijack) |
| 3 | format string | `%x` to read the stack, `%n` to write |
| 4 | file / `/tmp` handling | what file does it open? can a symlink redirect it? |
| 5 | network or I/O behaviour | `strace` for sockets, `netstat`/`ss` for ports |
| 6 | combined or file descriptor trick | `strace` and `ltrace` side by side |
| 7 | final exploit | chain the earlier techniques |
| 8 | end | congratulations |

## Method for any unknown binary

1. `file`, `strings`, `ltrace`, `strace`: what does it read, execute, compare, connect to?
2. `objdump -d` to find unsafe calls (`gets`, `strcpy`, `system`, `popen`, `printf` with a variable format).
3. Pick the matching idea from the primer.
4. Test in gdb, then outside gdb (stack addresses differ).
5. Write a note: the bug class, the exploit idea, one fix.

## Reinforce

- Flashcards: PATH hijack, TOCTOU, symlink attack, format string `%n`, setuid, `ltrace` vs `strace`.
- When you finish a level, add its real details here and to the private solutions file.
