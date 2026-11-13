#!/usr/bin/env python3
"""Mirror public CTF reference repositories into a local folder (shallow clones).

    python scripts/fetch_offline_refs.py --dest D:/ctf-refs --only payloads gtfobins lolbas
    python scripts/fetch_offline_refs.py --list

Needs git and internet. NOT run automatically: review the list, check sizes, and confirm the
event rules allow reference material before bringing any of this to a competition.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPOS = {
    "payloads": ("https://github.com/swisskyrepo/PayloadsAllTheThings.git", "PayloadsAllTheThings"),
    "hacktricks": ("https://github.com/HackTricks-wiki/hacktricks.git", "hacktricks"),
    "gtfobins": ("https://github.com/GTFOBins/GTFOBins.github.io.git", "GTFOBins"),
    "lolbas": ("https://github.com/LOLBAS-Project/LOLBAS.git", "LOLBAS"),
    "cyberchef": ("https://github.com/gchq/CyberChef.git", "CyberChef-source"),
    "rsactftool": ("https://github.com/RsaCtfTool/RsaCtfTool.git", "RsaCtfTool"),
    "seclists": ("https://github.com/danielmiessler/SecLists.git", "SecLists"),
    "ctf-wiki": ("https://github.com/ctf-wiki/ctf-wiki.git", "ctf-wiki"),
}


def dir_size(p):
    return sum(f.stat().st_size for f in Path(p).rglob("*") if f.is_file())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest")
    ap.add_argument("--only", nargs="*", choices=REPOS)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.dest:
        for k, (url, d) in REPOS.items():
            print(f"{k:12s} {url}")
        return
    if not shutil.which("git"):
        sys.exit("git not found")
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    for key in (a.only or REPOS):
        url, name = REPOS[key]
        target = dest / name
        if target.exists():
            print("skip (exists):", target)
            continue
        print("cloning", key, "...")
        r = subprocess.run(["git", "clone", "--depth", "1", url, str(target)])
        if r.returncode != 0:
            print("  failed:", key)
            continue
        shutil.rmtree(target / ".git", ignore_errors=True)   # drop history to save space
        print(f"  {name}: {dir_size(target) / 1_048_576:.0f} MB")


if __name__ == "__main__":
    main()
