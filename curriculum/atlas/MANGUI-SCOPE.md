# Enhanced man pages: scope and decisions (built; status in COVERAGE.md)

**Status 2026-11-24:** built and shipped (84 guides, `mangui/`). The proposal below is kept for the reasoning. **Decisions taken:** (1) a short pointer at the top of each page plus the guide at the end; (2) every option is explained (focused guides only for gcc, git, docker and bash); (3) tier 3 standalone pages for GUI tools: yes (burpsuite, ghidra, cyberchef, bloodhound, wireshark, pwntools); (4) the atlas pages were merged and the `atlas-` naming dropped; (5) examples are explained, not captured (captured output only where it already existed). See `COVERAGE.md` for what remains.


**Goal:** typing `man file` (or `man grep`, `man nmap` ...) in Kali or any Linux VM shows the **original manual page unchanged**, followed by a **LAYMAN GUIDE** section: plain-language purpose, when you use it, examples with real captured output, every option you are likely to meet explained in plain English, common mistakes, practice tasks, related tools.

## How it works (decided after testing)

1. An installer finds the system's real page (`man -w NAME`), reads it, and writes a merged copy: original text + guide, into `~/.local/share/mangui/man1/`.
2. A small `man` wrapper (in `~/.local/bin`, ahead of `/usr/bin` on PATH) shows the merged copy when one exists and otherwise runs the real `man`. So `man file`, `man 1 file`, `/search`, the pager and `q` all behave normally.
3. Two page dialects are handled: classic `man(7)` (most tools) and BSD `mdoc(7)` (file, nc, ssh).
4. When the system updates a page, run `mangui-refresh` to rebuild the merged copies from the new originals. The original text is never edited, only appended to.

Why a wrapper: I tested putting a merged page earlier in `MANPATH`, and man-db still prefers the system page (even after indexing with mandb). The wrapper is the reliable way.

## What the data says (scan of the 1,000+ commands in your material)

| Group | Count | Notes |
|---|---:|---|
| Commands in the material that already have a system man page here | 55 | cat, grep, file, find, sort, nc, ssh, curl, openssl, xxd, strings, readelf, objdump, tar, gzip, gcc, ip, ss, git, docker, python3 and others |
| ...of those in BSD mdoc format | 3 | file, nc, ssh |
| Real security/forensics tools used in the material but not installed here | ~30 | nmap, tshark, capinfos, vol (Volatility 3), exiftool, binwalk, zsteg, steghide, john, zip2john, hashcat, hashid, checksec, ltrace, strace, gdb, ffuf, chisel, proxychains, dig, whois, ffmpeg, ffprobe, sox, jq, rg, sqlite3, unzip, zipinfo, xsltproc, zbarimg |
| Tools in `toolkit.csv` | 41 | includes GUI tools with no man page (Ghidra, Burp, CyberChef, BloodHound): see tier 3 |
| Distinct flags the material actually uses, for the 55 commands | 116 | every one gets a plain-English line |
| Options documented in those 55 original pages | 4,282 | dominated by gcc (2,650 warning/optimisation flags); without gcc, git and bash about 1,300 |

## Proposed tiers

**Tier 1: the 55 commands that already have man pages (in WSL now, in Kali too).** Real captured output in my environment; the installer merges with Kali's own original page.

**Tier 2: ~30 security tools** (nmap, tshark, exiftool, ...). I write the guide now; the installer merges it with Kali's original page. Output is captured the first time you run `python3 scripts/atlas_build.py` in Kali (until then the examples are labelled "expected").

**Tier 3: tools with no man page (GUI or scripts).** Ghidra, Burp, CyberChef, BloodHound, Wireshark GUI, pwntools functions, Volatility plugin names. They would get a standalone page `man ghidra` (new, not a merge). Optional.

## Depth per page (proposal)

- 1 to 3 screens of guide text added to the end of the original page (a typical `man file` is 12 screens already).
- **Options:** every flag your material uses, plus the roughly 10 most useful flags in the original page, each with: what it does in plain English, when you reach for it, one example. A line at the end points to the rest of the original options list.
- **Examples:** 5 to 8 recipes per tool, each with real output captured from a lab folder.
- **Sections:** In plain words / When you would use it / Examples with real output / Options in plain English / Mistakes people make / Try this / See also / About these examples.
- Large pages (gcc, bash, git) get a focused guide, not an option-by-option rewrite.

## Order of work

1. Build the merger, wrapper, installer and refresh script; test on `file` (done as a sample), `grep` (man format) and `nc` (mdoc).
2. Tier 1 batches of 8 to 10 commands, in order of use in your material: cat, grep, file, python3, git, echo, xxd, head, strings, find, sort, nc, base64, ls, ssh, printf, sha256sum, uniq, curl, tr, md5sum, openssl, readelf, docker, cut, gcc, ip, gzip, chmod, awk, ss, objdump, date, and the rest.
3. Tier 2 batches by CyberSci skill: networking (nmap, dig, whois, proxychains, chisel), forensics (tshark, exiftool, binwalk, vol, steghide, zsteg), cracking (john, hashcat, hashid), reverse/pwn (gdb, ltrace, strace, checksec), media (ffmpeg, sox).
4. Tier 3 if you want it.

## Decisions needed before generating

1. Guide placement: **end of the page** (original stays first), or a short **pointer at the top** too?
2. Option depth: **material flags + the top ~10 per page** (recommended), or every option in the page (the big pages would be huge)?
3. Tier 3 standalone pages for GUI tools: yes or no?
4. Existing `atlas-*` pages: keep both styles, or fold them into the merged pages and drop the `atlas-` names?
