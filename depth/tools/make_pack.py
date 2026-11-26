#!/usr/bin/env python3
"""Build a source pack from the installed tools' own --help text (official, versioned). Usage: make_pack.py SPEC.json > pack.txt"""
import json, subprocess, sys
spec = json.load(open(sys.argv[1], encoding="utf-8"))
print(f"SOURCE PACK for {spec['id']}: the installed tools' own help text, captured verbatim.\n")
for t in spec["pack_tools"]:
    for flag in ("--help", "-h"):
        p = subprocess.run([t, flag], capture_output=True, text=True, timeout=10)
        txt = (p.stdout or p.stderr).strip()
        if txt:
            break
    v = subprocess.run([t, "--version"], capture_output=True, text=True, timeout=10)
    ver = (v.stdout or v.stderr).splitlines()[0] if (v.stdout or v.stderr) else "version unknown"
    print(f"=== {t} ({ver}) ===\n{txt}\n")
