# Command Atlas coverage plan

Goal: every tool and platform you use for CyberSci has an `atlas-NAME` man page in Kali and the VM, with real captured output. Status: **captured** = recipes run for real; **written** = page exists, outputs marked *expected* until you run the generator where the tool is installed (Kali); **planned** = not started.

## Done (14 pages)

| Page | Status |
|---|---|
| grep, find, sed, awk, file + xxd + strings, curl, nc, openssl, python-oneliners, readelf + objdump | captured |
| nmap, tcpdump, gdb, sqlite3 | written (capture on Kali) |

## Batch 2: Linux and text toolbox (small, high use)

cut, sort, uniq, tr, tee, xargs, head/tail, wc, diff, cmp, dd, base64, jq, ripgrep, tmux, ssh + scp, socat, ss/ip, chmod/chown/umask, ps/lsof/strace/ltrace, git, systemd/journalctl, cron.

## Batch 3: forensics and reverse engineering

tshark (+ Wireshark display filters), exiftool, binwalk, foremost, steghide, zsteg, volatility3 (`vol`), sleuthkit (mmls/fls/icat), photorec, strings variants, ghidra (shortcuts + headless), radare2/rizin cheat page, checksec, pwntools, ROPgadget, ltrace/strace, objdump recipes.

## Batch 4: web, crypto, cracking

ffuf, gobuster, sqlmap, nikto, whatweb, Burp (keys and workflow), CyberChef (operations that matter), jwt_tool, hashcat, john, hydra, RsaCtfTool, openssl (more), gpg.

## Batch 5: network and Active Directory

netcat variants, ncat, proxychains, chisel, ssh tunnels (-L/-R/-D), impacket examples, NetExec, smbclient, enum4linux, ldapsearch, dig/nslookup/whois, traceroute, arp-scan.

## Batch 6: platform pages (`man atlas-overthewire`, etc.)

| Page | Contents |
|---|---|
| atlas-overthewire | ssh ports per game, the shared-connection helper, level workflow, tools by game, no-spoilers rules |
| atlas-tryhackme | AttackBox vs OpenVPN, room workflow, free-tier limits, the P1 list |
| atlas-picoctf | account, Challenge Library, categories and tool set per category |
| atlas-ctfd | submitting flags, team, scoreboard, how a CyberSci-style CTFd works |
| atlas-vulnhub | VMware import, host-only network, find the IP, snapshots |
| atlas-docker | compose commands used by the defence workshop and Juice Shop |
| atlas-defence | the 7-step defence loop as a man page |

## How to finish a page (each takes about 30 minutes)

1. Add a definition to `scripts/atlas_tools2.py` (or a new `atlas_tools3.py`).
2. In Kali: `python3 scripts/atlas_build.py --tool NAME` to capture real output.
3. Read the output against your explanation; fix anything that does not match.
4. `bash curriculum/atlas/install-man.sh` and test with `man atlas-NAME`.
5. Commit; the offline pack picks it up from `curriculum/atlas/`.
