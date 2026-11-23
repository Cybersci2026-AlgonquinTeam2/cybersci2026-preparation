"""Turn Command Atlas tool definitions into real roff man pages (man atlas-grep, man atlas) plus an installer.

Called by atlas_build.py. Output: curriculum/atlas/man/man1/atlas-<tool>.1, atlas.1 and curriculum/atlas/install-man.sh
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "curriculum" / "atlas" / "man" / "man1"


def esc(t):
    t = t.replace("\\", "\\e").replace("-", "\\-")
    return re.sub(r"`([^`]+)`", r"\\fB\1\\fR", t)


def block(text):
    """Escape a verbatim block: backslashes, hyphens and lines that start with a roff control character."""
    out = []
    for ln in text.split("\n"):
        ln = ln.replace("\\", "\\e").replace("-", "\\-")
        if ln[:1] in (".", "'"):
            ln = "\\&" + ln
        out.append(ln)
    return "\n".join(out)


def prose(text):
    lines = []
    for ln in esc(text).split("\n"):
        if ln[:1] in (".", "'"):
            ln = "\\&" + ln
        lines.append(ln)
    return "\n".join(lines)


def end(t):
    t = t.rstrip()
    return t if t[-1:] in ".?!" else t + "."


def write(tool, outs, ver):
    MAN.mkdir(parents=True, exist_ok=True)
    n = tool["name"]
    cap = outs is not None
    o = [f'.TH ATLAS-{n.upper().replace("_", "-")} 1 "{date.today().isoformat()}" "CyberSci Command Atlas" "Command Atlas"',
         ".SH NAME", "atlas\\-" + esc(n) + " \\- " + prose(tool["one_line"]),
         ".SH SYNOPSIS", ".nf", block(tool["anatomy"].rstrip()), ".fi",
         ".SH WHEN TO USE"]
    for w in tool["when"]:
        o += [".IP \\(bu 2", prose(w)]
    o += [".SH FLAGS"]
    for f, d, w in tool["flags"]:
        o += [".TP", "\\fB" + block(f) + "\\fR", end(prose(d)), ".br", "Use it when: " + end(prose(w))]
    o += [".SH RECIPES"]
    for i, r in enumerate(tool["recipes"], 1):
        o += [f'.SS "{i}. {esc(r["title"])}"', prose(r["why"]), ".PP", ".nf", "$ " + block(r.get("show") or r["cmd"]), ".fi", ".PP"]
        out = (outs.get(i - 1, "") if cap else "(expected, not captured) " + r.get("expect", "see the explanation")) or "(no output: that is the result)"
        o += [".nf", block(out), ".fi", ".PP", prose(r["read"])]
    o += [".SH COMMON MISTAKES"]
    for g in tool["gotchas"]:
        o += [".IP \\(bu 2", prose(g)]
    o += [".SH PRACTICE"]
    for k, p in enumerate(tool["practice"], 1):
        o += [f".IP {k}. 3", prose(p)]
    o += [".SH SEE ALSO", prose(", ".join(tool["related"])) + ".",
          ".SH CAPTURE", prose(("Output captured " + date.today().isoformat() + " with: " + ver) if cap else "Not captured yet: " + ver + ". Re-run atlas_build.py where the tool is installed (Kali) to replace the expected output with real output.")]
    (MAN / f"atlas-{n}.1").write_text("\n".join(o) + "\n", encoding="utf-8", newline="\n")


def write_index(tools):
    MAN.mkdir(parents=True, exist_ok=True)
    o = [f'.TH ATLAS 1 "{date.today().isoformat()}" "CyberSci Command Atlas" "Command Atlas"', ".SH NAME",
         "atlas \\- expanded manuals for the tools used in CyberSci preparation",
         ".SH DESCRIPTION", "Each tool has a page named atlas\\-TOOL with a purpose line, when to use it, an annotated command, "
         "a flag table that says when each flag helps, recipes with real captured output, common mistakes and practice tasks.",
         ".SH USAGE", ".nf", "man atlas\\-grep", "gm grep        # atlas page if present, else the normal man page", ".fi", ".SH PAGES"]
    for t in tools:
        o += [".TP", f"\\fBatlas\\-{esc(t['name'])}\\fR", prose(t["one_line"])]
    (MAN / "atlas.1").write_text("\n".join(o) + "\n", encoding="utf-8", newline="\n")
    inst = ROOT / "curriculum" / "atlas" / "install-man.sh"
    inst.write_text('''#!/usr/bin/env bash
# Install the CyberSci Command Atlas man pages for the current user (Kali, Ubuntu, WSL, any Linux with man-db).
#   bash install-man.sh        then open a new shell:  man atlas   |   man atlas-grep   |   gm grep
set -e
here="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.local/share/atlas/man"
mkdir -p "$dest/man1"
cp "$here"/man/man1/*.1 "$dest/man1/"
line='export MANPATH="$HOME/.local/share/atlas/man:${MANPATH:-}:"'
fn='gm() { man "atlas-$1" 2>/dev/null || man "$1"; }'
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  [ -f "$rc" ] || continue
  grep -q 'atlas/man' "$rc" || printf '\\n# CyberSci Command Atlas man pages\\n%s\\n%s\\n' "$line" "$fn" >> "$rc"
done
echo "Installed $(ls "$dest/man1" | wc -l) pages to $dest"
echo "Open a new terminal, then try:  man atlas   or   gm grep"
''', encoding="utf-8", newline="\n")
