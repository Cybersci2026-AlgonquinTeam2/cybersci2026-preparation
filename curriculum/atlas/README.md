# Command Atlas: expanded manuals with real output

**What this is:** one page per tool that goes beyond `man`. Each page has a one-line purpose, when you reach for it, an annotated command, a flag table that says *when* to use each flag, recipes with output **captured by really running the command**, common mistakes, practice tasks and flashcard prompts.

**Why the output is real:** `scripts/atlas_build.py` runs every recipe inside a throw-away lab folder in WSL (Ubuntu 24.04) and pastes what the tool printed. Web and netcat examples talk only to a tiny echo server on `127.0.0.1`. When you rebuild, the output refreshes, so the examples cannot drift from the tool.

**Pages so far (8):** grep, find, sed, awk, file + xxd + strings, curl, nc (netcat), openssl.

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
