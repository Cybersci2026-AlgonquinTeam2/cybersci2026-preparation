# OverTheWire Manpage: hints book (levels 0-6)

Manpage teaches common misconceptions in Linux C programming: auditing unfamiliar code is easier when you check the manual pages for pitfalls and unusual behaviour. 7 levels, Linux/x86, rating x/10. Connect: `ssh manpage0@manpage.labs.overthewire.org -p 2224`; level 0 is `manpage0` / `manpage0`. Level data is in `/manpage/`.

Status: **method stub only.** I could not retrieve per-level descriptions or reliable writeups (the third-party index I found is generic, and the official level pages are intentionally empty), so I am not going to invent level solutions. What follows is the study method the game is designed around.

## The game in one idea

```
see a C function  ->  read its man page (man 3 / man 2)  ->  find the NOTES / BUGS / CAVEATS
                  ->  ask: does the program rely on behaviour the page warns about?
```

## How to attack a level

1. Read the source (or disassemble). List every libc call.
2. For each call run `man 3 funcname` (or `man 2 funcname` for system calls) and read **RETURN VALUE**, **NOTES**, **BUGS** and **CAVEATS**.
3. Typical pitfalls to check: a function that doesn't null-terminate (`strncpy`), ignoring return values, signed/unsigned mix-ups, `atoi` with no error reporting, `gets`, `sprintf` size, `strcmp` vs `strncmp`, permissions of files created with default `umask`, `access()` then `open()` (race), `system()`/`popen()` with PATH.
4. Write a tiny test program to confirm the behaviour before you rely on it.
5. Then exploit using the primer's ideas.

## Tools

`man`, `man -k`/`apropos`, `man 2 syscalls`, `gcc -Wall -Wextra`, `gdb`, `ltrace`, `strace`.

## Next steps

- Play the game and fill each level here with: the man page that explains the bug, the pitfall in one sentence, and the fix.
- If you want me to draft level details, paste the source or the observed behaviour for a level and I will write the walkthrough.
