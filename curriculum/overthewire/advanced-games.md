# OverTheWire advanced games: Utumno, Maze, Vortex, FormulaOne, Drifter

Status: **research outline, not a walkthrough.** The official level pages are intentionally empty, and the public indexes I could read give one-line themes only. This file records what is known (with sources), a study order, and what to collect as you play. It does not invent per-level solutions. Prerequisites: finish Narnia and read [binary-primer.md](binary-primer.md). Strongly recommended: pwntools, gdb with pwndbg/gef, a disassembler (Ghidra or radare2).

None of this is needed for CyberSci regionals. It is the "advanced eventually" track.

## Utumno (10 levels per the site, rating 4/10, port 2227)

Host `utumno.labs.overthewire.org`, user `utumno0` / `utumno0`, data in `/utumno/`. Harder than Leviathan, a bit harder than Behemoth. One third-party index ([nguendung](https://nguendung.github.io/posts/overTheWire-Utumno-Full-Levels-Tutorial)) lists these themes, and shows only levels 0-8 (verify level 9 yourself):

| Level | Theme (per that index) |
|---|---|
| 0 | warm-up buffer overflow |
| 0→1 | classic stack overflow |
| 1→2 | control flow by overwriting a buffer |
| 2→3 | function pointer overwrite |
| 3→4 | off-by-one |
| 4→5 | format string with `%n` |
| 5→6 | shellcode injection |
| 6→7 | return-to-libc (NX stack) |
| 7→8 | multi-step chain |

## Maze (9 levels, 0-8, rating 5/10, port 2225)

Host `maze.labs.overthewire.org`, user `maze0` / `maze0`, data in `/maze/`. The author says some levels are "strange" and to expect gdb. Writeups ([Avishai](https://avishaigonen123.github.io/CTF_writeups/overthewire/maze), [7rocky](https://7rocky.github.io/en/ctf/overthewire/maze), [vkkkv](https://vkkkv.github.io/wp/OverTheWire/OverTheWire-Maze/)) mention: a TOCTOU race with a symlink swapped in a loop (maze0), shellcode injection, passing a magic value in `argv[1]` (maze3), library hooking, self-modifying code, custom ELF parsing, ptrace anti-debugging, and a TCP server with a format-string bug (maze8, listens on 1337 by default). Treat as leads, not confirmed. (The ptrace anti-debug and self-modifying code themes also match CyberSci's own reverse-engineering past challenges, which makes Maze relevant later.)

## Vortex (27 levels per the site, port to confirm)

Host `vortex.labs.overthewire.org`. Files mostly in `/vortex/`. Level 0 is a network program: one writeup says it listens on port 5842, sends four unsigned integers, and expects their sum back to get the next credentials ([l3ouu4n9](https://l3ouu4n9.github.io/post/wargames/overthewire/2019-12-02-overthewire-vortex)). Other levels are reported as a mix of network, web and exploitation. Confirm the SSH port and level numbering on the site before relying on them.

Skills to prepare for level 0: Python `socket` + `struct.unpack("<IIII")` / `struct.pack("<I", total)` (mind endianness and 32-bit wraparound).

## FormulaOne (7 levels, 0-6 per an index, port 2232)

Host `formulaone.labs.overthewire.org`, user `formulaone0`, data in `/formulaone/`. The site hints that the source for level 0 is viewable from another wargame on the same server and that finding which one is part of the challenge. One index ([nguendung](https://nguendung.github.io/posts/overTheWire-FormulaOne-Full-Levels-Tutorial)) lists the arc: simple overflow to control `eip`, offset finding with a cyclic pattern, getting past a weak input check, a small ROP chain, then ret2libc with an address leak, then a combined final exploit.

## Drifter (about 16 levels, one source says 19; port 2230 unconfirmed)

Host `drifter.labs.overthewire.org`. Described on the site as "along the lines of Vortex". One writeup ([Avishai](https://avishaigonen123.github.io/CTF_writeups/overthewire/drifter)) says level 0 listens on port 1111 with source in `/drifter/drifter0_src/`; another uses a different port, so check the page. WeChall lists the box as having [16-19 levels](https://wc2.wechall.net/19-levels-on-Drifter.html); the count grows as players solve levels.

## Suggested order and prerequisites

1. FormulaOne (7 levels, a good ROP/ret2libc ladder) after Narnia and Behemoth.
2. Utumno, then Maze.
3. Vortex and Drifter: expect network programming and mixed skills.

| Skill to have first | Source in this repo |
|---|---|
| gdb, stack, shellcode, format strings | binary-primer.md |
| ROP and ret2libc basics | add a primer when you reach FormulaOne |
| sockets and struct packing in Python | modules 11 (scripting) |
| reverse engineering with Ghidra | module 5 |

## What to record per level as you play (fills this file in)

Port/host, files provided, the bug in one line, the technique, the exact tool commands, the fix, and one flashcard question. Paste me the source or behaviour and I will turn it into a full walkthrough with diagrams.
