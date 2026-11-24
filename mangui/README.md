# mangui: enhanced man pages

`man file`, `man grep`, `man nmap` ... show the **original manual page unchanged**, a short pointer near the top, and a **LAYMAN GUIDE** at the end: plain-language purpose, when you use it, explained examples, every option in plain English, common mistakes, practice tasks and related tools. In the pager press `G` to jump to the guide.

Tools that have no system page (Ghidra, Burp, CyberChef, BloodHound, pwntools ...) get a standalone page, so `man ghidra` works too.

## Install (Kali or any Linux VM)

```bash
python3 mangui/mangui.py install     # merge guides into the real pages; installs a `man` wrapper in ~/.local/bin
source ~/.bashrc                     # (or ~/.zshrc) once, to pick up the PATH line
python3 mangui/mangui.py list        # which guides merge into a real page and which are standalone
python3 mangui/mangui.py coverage    # options explained vs options in each original page (takes several minutes)
python3 mangui/mangui.py refresh     # run again after a system update rewrites a page
python3 mangui/mangui.py uninstall   # remove everything it installed
```

Nothing under `/usr` is touched. Merged pages go to `~/.local/share/mangui/man<N>/`. The wrapper opens a merged page when one exists and otherwise runs the real `man`; `MANGUI=0 man file` shows the original once. Two page dialects are handled: classic `man(7)` and BSD `mdoc(7)` (file, nc, ssh).

Get it into the VM: `git clone` the repository, or unzip `Mangui.zip` from the offline pack (OneDrive `CyberSci-Offline`). Step by step for Kali, including the apt line that installs the tools whose real pages should exist first: see **Kali steps** below.

## What is covered (102 guides)

| Group | Guides |
|---|---|
| Text and files | cat, head, tail, less, nano, wc, cut, sort, uniq, tr, paste, fold, diff, cmp, sed, awk, grep, find, file, strings, xxd, ls, cp, mv, mkdir, stat, id |
| Shell and system | jq, tmux, bash (focused), echo, printf, test, timeout, date, chmod, getcap, crontab, git (focused), docker (focused), ip, ss, ssh, tar, gzip, bzip2, base64, md5sum, sha256sum, curl, nc, openssl, python3 |
| Build and debug | gcc (focused), gdb, readelf, objdump, strace, ltrace, checksec, pwntools, radare2, ROPgadget |
| Network and web | nmap, tcpdump, tshark, wireshark, dig, whois, socat, chisel, proxychains4, ldapsearch, rpcclient, impacket, nikto, gobuster, ffuf, wfuzz, dirb, sqlmap, burpsuite, smbclient, enum4linux, hydra |
| Cracking | john, hashcat, hashid |
| Forensics and stego | exiftool, binwalk, foremost, steghide, zsteg, ffmpeg, sox, vol (Volatility 3), cyberchef |
| Exploitation and AD | searchsploit, msfconsole, ghidra, bloodhound |

"Focused" means the most-used options and cases rather than every option (marked `"partial": true` in the guide, so `coverage` does not count it against the original).

## How accurate is it?

- Guides explain techniques with **written, explained examples**. They are not captured output (file, grep and the guides converted from the atlas pages do contain captured output).
- Option lists for the tools not installed in the author's WSL (nmap, tshark, exiftool, binwalk, john, hashcat, gobuster, ffuf, hydra, sqlmap, steghide, nikto, wfuzz, dirb, smbclient, enum4linux, hashid, zsteg, searchsploit, msfconsole, vol) were written **from knowledge, not checked against Kali's pages**. Run `coverage` on Kali; it lists every option in the real page that a guide does not mention.
- Known gaps: awk `-I` and `-s`, cut `-M`; nmap, tcpdump, gdb and sqlite3 option lists are not complete until checked against Kali.

## Kali steps

1. Copy the files in (git clone, or `unzip Mangui.zip -d ~/mangui-pack`).
2. `python3 mangui.py install`, then `source ~/.bashrc`.
3. Install the tools so their real pages exist, then refresh:

```bash
sudo apt update
sudo apt install -y nmap tcpdump gdb sqlite3 tshark wireshark binwalk libimage-exiftool-perl \
  john hashcat gobuster ffuf hydra sqlmap steghide nikto wfuzz dirb smbclient enum4linux \
  hashid exploitdb metasploit-framework
python3 mangui.py refresh
```

(`zsteg` is a Ruby gem and `pwntools` a pip package: they stay standalone.)

4. `python3 mangui.py coverage | tee ~/coverage.txt` and send back the `missing:` lists so the option lists can be completed.

## Writing or extending a guide

Guides live in `guides/NAME.json` (keys: name, section, one_line, plain, when, examples[title, cmd, explain], options[flag, plain, use], mistakes, try, see_also; optional `partial`). They are generated from Python modules so they are easy to author:

1. Add a `GUIDES.append(dict(name=..., section="1", one_line=..., plain=[...], when=[...], examples=[(title, cmd, explain), ...], options=[(flag, plain, use), ...], mistakes=[...], try_=[...], see_also=...))` entry to `scripts/mangui_batchN.py` (copy any existing batch as a template; `partial=True` for focused guides).
2. Add the module to `MODULES` in `scripts/mangui_write.py` and run `python scripts/mangui_write.py batchN`.
3. Check it renders: install into a throw-away HOME and run `groff -man -ww -z ~/.local/share/mangui/man1/NAME.1` (warnings from the original page are not yours).
4. `python scripts/package_pack.py` rebuilds `Mangui.zip` for the offline pack.

`mangui_build.py` is the older route that captures real output from commands run in the Atlas lab (WSL); `file` and `grep` use it.

See also `curriculum/atlas/MANGUI-SCOPE.md` (design, decisions) and `curriculum/atlas/COVERAGE.md` (status and what remains).
