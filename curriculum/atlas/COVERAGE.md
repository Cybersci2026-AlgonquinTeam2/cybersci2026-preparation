# Man-page guides: coverage and what is left

The Command Atlas pages (`curriculum/atlas/*.md`) are the long-form study notes with captured output. The **man-page guides** (`mangui/guides/*.json`, installed with `python3 mangui/mangui.py install`) are what you read in the terminal: the original `man` page followed by a layman guide. The old `atlas-NAME.1` pages and `install-man.sh` are gone; their content was merged into the guides and the `atlas-` naming dropped.

Status as of 2026-11-24: **84 guides** (see `mangui/README.md` for the list by group).

## Done

| Group | Guides |
|---|---|
| Captured with real output | file, grep, and the early batch converted from the atlas pages (awk, curl, find, nc, openssl, python3, sed, xxd, strings, readelf, objdump, ssh, tar, cat, sort, ls) |
| Explained examples, every option | head, tail, wc, cut, tr, uniq, base64, gzip, bzip2, chmod, date, diff, cmp, less, nano, timeout, paste, fold, echo, printf, test, getcap, crontab, ip, ss, md5sum, sha256sum, cp, mv, mkdir, stat, id |
| Security tools | nmap, tshark, exiftool, binwalk, john, hashcat, gobuster, ffuf, hydra, sqlmap, steghide, nikto, wfuzz, dirb, smbclient, enum4linux, hashid, zsteg, searchsploit, msfconsole, vol, wireshark |
| Focused guides (most-used options) | gcc, git, docker, bash |
| Standalone pages for tools with no man page | burpsuite, ghidra, cyberchef, bloodhound, pwntools |

## Not finished

| Item | Why | What it needs |
|---|---|---|
| Complete option lists for **gdb, tcpdump, sqlite3** | those tools' real pages are not installed in the author's WSL | run `python3 mangui/mangui.py coverage` on Kali and send the `missing:` lists |
| **Check every security-tool guide** against Kali's real pages | option lists were written from knowledge | same coverage run |
| awk `-I`/`-s`, cut `-M` | not explained; not guessed | confirm against Kali's man page |
| Real captured output for nmap, tcpdump, gdb, sqlite3 | not installed in WSL | `python3 scripts/atlas_build.py` on Kali (updates the atlas `.md` pages) |
| Extra tools not yet written | not in the first scope | dig/whois, ltrace/strace, checksec, ffmpeg/sox, jq, tmux, socat, chisel, proxychains, radare2, foremost, impacket, ROPgadget |
| Platform pages (OverTheWire, TryHackMe, picoCTF, CTFd, VulnHub) | you asked for guides on tools and commands, not platforms | not planned; the platform books in the offline pack cover them |

## How to finish a guide

See "Writing or extending a guide" in `mangui/README.md`: add an entry to a `scripts/mangui_batchN.py`, run `python scripts/mangui_write.py batchN`, check with groff, rebuild with `python scripts/package_pack.py`.
