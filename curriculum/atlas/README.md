# Command Atlas: expanded manuals with real output

**What this is:** one page per tool that goes beyond `man`. Each page has a one-line purpose, when you reach for it, an annotated command, a flag table that says *when* to use each flag, recipes with output **captured by really running the command**, common mistakes, practice tasks and flashcard prompts.

**Why the output is real:** `scripts/atlas_build.py` runs every recipe inside a throw-away lab folder in WSL (Ubuntu 24.04) and pastes what the tool printed. Web and netcat examples talk only to a tiny echo server on `127.0.0.1`. When you rebuild, the output refreshes, so the examples cannot drift from the tool.

**Pages so far (14):** grep, find, sed, awk, file + xxd + strings, curl, nc (netcat), openssl, python one-liners, readelf + objdump (all captured with real output), and nmap, tcpdump, gdb, sqlite3 (written; marked *not captured* until you run the generator where those tools are installed, for example in Kali).

**Read a page in this order:** one-line purpose, anatomy, the three or four flags you actually use, the recipes (read the output *before* the explanation and predict it), then the mistakes.

**Add a tool:** write a definition in `scripts/atlas_tools.py` (purpose, when, anatomy, flags, recipes with commands and explanations, gotchas, practice, cards) and run `python scripts/atlas_build.py --tool NAME`. Tools that are not installed in WSL cannot be captured: install them first.

**Tools to add next, and what they need:**

| Tool | Needs install? | Why it matters for CyberSci |
|---|---|---|
| nmap | yes | scanning and service detection |
| tcpdump / tshark | yes | packet capture and analysis |
| gdb | yes | debugging, buffer overflows |
| exiftool, binwalk | yes | file and image forensics |
| sqlite3 | yes | basic SQL, database evidence |
| hashcat, john | yes | cracking hashes |
| ssh, scp, socat | partly | tunnels and transfers |
| ltrace, strace | yes | what a program does when it runs |
| readelf, objdump | already installed | reading binaries |
| python3 one-liners | already installed | quick decoding and scripting |

Install line for WSL (run it yourself in a WSL terminal, it needs your sudo password):

```bash
sudo apt update && sudo apt install -y nmap tcpdump tshark gdb ltrace strace sqlite3 binwalk libimage-exiftool-perl hashcat john socat
```

## Use these as real man pages in Kali or any Linux VM

The same pages are generated as roff man pages in `man/man1/` (`atlas-grep.1`, `atlas-nmap.1`, and an index `atlas.1`).

```bash
bash install-man.sh        # copies pages to ~/.local/share/atlas/man and adds MANPATH + a gm helper to ~/.bashrc and ~/.zshrc
man atlas                  # list every page
man atlas-grep             # one page
gm grep                    # atlas page if there is one, otherwise the normal man page
```

Get the files into the VM: `git clone` the repository and run the script from `curriculum/atlas/`, or unzip `Atlas-Man.zip` from the offline pack (OneDrive `CyberSci-Offline`) and run `bash install-man.sh`.

**Refresh with real output from Kali:** run `python3 scripts/atlas_build.py` inside the repository on Kali. On Linux it runs every recipe natively, so nmap, tcpdump, gdb and sqlite3 get captured output instead of *expected* output, and the man pages are rebuilt.
