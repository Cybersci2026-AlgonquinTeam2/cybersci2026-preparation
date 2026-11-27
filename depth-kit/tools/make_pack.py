#!/usr/bin/env python3
"""Build a source pack from a topic spec. Works offline: every source is a local capture. Usage: make_pack.py SPEC.json > pack.txt

The spec lists sources under "pack_sources", each one of:
  {"type": "command_help", "tool": "grep"}          the installed program's own --help text and version
  {"type": "command_man",  "tool": "grep"}          its manual page rendered as text (needs man and col)
  {"type": "file", "path": "captures/doc.txt", "label": "Vendor guide, retrieved 2026-01-05"}   a text capture you saved
Add your own types in SOURCE_TYPES (for example a PDF-to-text capture or a dataset description). Record version and retrieval date in the label.
"""
import json
import subprocess
import sys
from pathlib import Path


def command_help(s):
    t = s["tool"]
    txt = ""
    for flag in ("--help", "-h"):
        p = subprocess.run([t, flag], capture_output=True, text=True, timeout=15)
        txt = (p.stdout or p.stderr).strip()
        if txt:
            break
    v = subprocess.run([t, "--version"], capture_output=True, text=True, timeout=15)
    ver = ((v.stdout or v.stderr).splitlines() or ["version unknown"])[0]
    return f"=== {t} ({ver}) --help ===\n{txt}\n"


def command_man(s):
    t = s["tool"]
    p = subprocess.run(f"man {t} | col -b", shell=True, capture_output=True, text=True, timeout=30)
    return f"=== {t} manual page ===\n{p.stdout.strip()}\n"


def file_capture(s):
    return f"=== {s.get('label', s['path'])} ===\n{Path(s['path']).read_text(encoding='utf-8', errors='ignore').strip()}\n"


SOURCE_TYPES = {"command_help": command_help, "command_man": command_man, "file": file_capture}

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    print(f"SOURCE PACK for {spec['id']}: local captures, verbatim.\n")
    for s in spec.get("pack_sources") or [{"type": "command_help", "tool": t} for t in spec.get("pack_tools", [])]:
        print(SOURCE_TYPES[s["type"]](s))
