#!/usr/bin/env python3
"""mangui: make `man NAME` show the original manual page PLUS a plain-language guide.

    python3 mangui.py install      merge every guide in ./guides into the system's real man page; install the `man` wrapper
    python3 mangui.py refresh      same (run again after the system updates a man page)
    python3 mangui.py list         which guides exist and how each one will be shown
    python3 mangui.py coverage     how many of the original page's options each guide explains
    python3 mangui.py uninstall    remove everything this script installed

Nothing in /usr is modified. Merged pages go to ~/.local/share/mangui/man<N>/ and a small wrapper goes to ~/.local/bin/man
(it opens the merged page when one exists and otherwise runs the real man). Set MANGUI=0 to bypass the wrapper once.
The original text of every page is kept exactly as shipped; the guide is appended and a short pointer is added near the top.
"""
import bz2
import gzip
import json
import lzma
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDES = HERE / "guides"
HOME = Path(os.environ.get("HOME", str(Path.home())))
OUT = HOME / ".local" / "share" / "mangui"
BIN = HOME / ".local" / "bin"
MARK = "# mangui"
POINTER = ("A plain-language guide to this command, with examples and every option explained, is at the end of this page. "
           "In the pager press G (or type /LAYMAN GUIDE and press Enter) to jump to it.")


# ---------------------------------------------------------------- finding the real page
def real_man():
    for p in os.environ.get("PATH", "").split(os.pathsep):
        f = Path(p) / "man"
        if f.exists() and os.access(f, os.X_OK) and BIN not in f.parents:
            return str(f)
    return "/usr/bin/man"


def find_page(name, section):
    for sec in dict.fromkeys([section, "1", "8", "5", "7", "6", "3"]):
        r = subprocess.run([real_man(), "-w", sec, name], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        p = r.stdout.strip().split("\n")[0].strip()
        if r.returncode == 0 and p and not p.startswith(str(OUT)):
            return p, sec
    return None, section


def read_page(path):
    op = {".gz": gzip.open, ".bz2": bz2.open, ".xz": lzma.open}.get(Path(path).suffix, open)
    with op(path, "rt", encoding="utf-8", errors="replace") as f:
        return f.read()


# ---------------------------------------------------------------- text helpers
def esc(t):
    t = t.replace("\\", "\\e").replace("-", "\\-")
    return re.sub(r"`([^`]+)`", r"\\fB\1\\fP", t)


def safe(t, mdoc=False):
    """escape one line of text; neutralise a leading control character or (mdoc) a leading macro name"""
    t = esc(t)
    if t[:1] in (".", "'") or (mdoc and re.match(r"^[A-Z][a-z]\b", t)):
        t = "\\&" + t
    return t


def block(text, mdoc=False):
    out = []
    for ln in text.split("\n"):
        ln = ln.replace("\\", "\\e").replace("-", "\\-")
        if ln[:1] in (".", "'"):
            ln = "\\&" + ln
        out.append(ln)
    return "\n".join(out)


# ---------------------------------------------------------------- guide -> roff
def intro_text(g, have_orig):
    return ("Added by mangui. Everything above this line is the original manual page, unchanged." if have_orig else
            "The system manual page for this command is not installed on this machine, so this page contains only the layman guide.")


def emit_man(g, have_orig):
    o = [".SH LAYMAN GUIDE", safe(intro_text(g, have_orig)), ".SS In plain words"]
    for i, p in enumerate(g["plain"]):
        o += ([".PP"] if i else []) + [safe(p)]
    o += [".SS When you would use it"] + sum([[".IP \\(bu 2", safe(w)] for w in g["when"]], [])
    o += [".SS Examples with real output"]
    for ex in g["examples"]:
        o += [".PP", ".B " + '"' + esc(ex["title"]).replace('"', "'") + '"', ".nf", "$ " + block(ex["cmd"]), block(ex.get("output", "") or "(no output: that is the result)"), ".fi"]
    o += [".SS Every option in plain English"]
    for op in g["options"]:
        o += [".TP", "\\fB" + block(op["flag"]) + "\\fP", safe(op["plain"])]
        if op.get("use"):
            o += [".br", safe("Use it when: " + op["use"])]
    o += [".SS Mistakes people make"] + sum([[".IP \\(bu 2", safe(m)] for m in g["mistakes"]], [])
    o += [".SS Try this"] + sum([[f".IP {i}. 3", safe(t)] for i, t in enumerate(g["try"], 1)], [])
    o += [".SS See also", safe(g["see_also"]), ".SS About these examples", safe(g.get("captured_with", ""))]
    return "\n".join(o) + "\n"


def emit_mdoc(g, have_orig):
    o = [".Sh LAYMAN GUIDE", safe(intro_text(g, have_orig), True), '.Ss "In plain words"']
    for i, p in enumerate(g["plain"]):
        o += ([".Pp"] if i else []) + [safe(p, True)]
    o += ['.Ss "When you would use it"', ".Bl -bullet -compact"] + sum([[".It", safe(w, True)] for w in g["when"]], []) + [".El"]
    o += ['.Ss "Examples with real output"']
    for ex in g["examples"]:
        o += [".Pp", ".Sy " + '"' + esc(ex["title"]).replace('"', "'") + '"', ".Bd -literal -offset indent", block("$ " + ex["cmd"]),
              block(ex.get("output", "") or "(no output: that is the result)"), ".Ed"]
    o += ['.Ss "Every option in plain English"', ".Bl -tag -width indent"]
    for op in g["options"]:
        o += [".It Sy " + '"' + block(op["flag"]).replace('"', "'") + '"', safe(op["plain"], True)]
        if op.get("use"):
            o += [".Pp", safe("Use it when: " + op["use"], True)]
    o += [".El", '.Ss "Mistakes people make"', ".Bl -bullet -compact"] + sum([[".It", safe(m, True)] for m in g["mistakes"]], []) + [".El"]
    o += ['.Ss "Try this"', ".Bl -enum -compact"] + sum([[".It", safe(t, True)] for t in g["try"]], []) + [".El"]
    o += ['.Ss "See also"', safe(g["see_also"], True), '.Ss "About these examples"', safe(g.get("captured_with", ""), True)]
    return "\n".join(o) + "\n"


def add_pointer(text, fmt):
    """insert a short pointer section right after NAME (so `whatis`/`apropos` still see NAME first)"""
    head = r"^\.Sh\s+" if fmt == "mdoc" else r"^\.SH\s+"
    m = re.search(head + r'"?NAME"?\s*$', text, re.M)
    if not m:
        return text
    nxt = re.compile(head + r"\S", re.M).search(text, m.end())
    if not nxt:
        return text
    sec = (f'.Sh "ABOUT THE LAYMAN GUIDE"\n{safe(POINTER, True)}\n' if fmt == "mdoc" else f'.SH "ABOUT THE LAYMAN GUIDE"\n{safe(POINTER)}\n')
    return text[:nxt.start()] + sec + text[nxt.start():]


def standalone(g):
    sec = g.get("section", "1")
    top = (f'.TH {g["name"].upper()} {sec} "{date.today().isoformat()}" "mangui" "Layman guide"\n.SH NAME\n'
           f'{esc(g["name"])} \\- {safe(g["one_line"])}\n.SH SYNOPSIS\n.nf\n{block(g.get("synopsis", g["name"] + " [options] [arguments]"))}\n.fi\n')
    return top + emit_man(g, False)


# ---------------------------------------------------------------- install
def load_guides():
    gs = []
    for p in sorted(GUIDES.glob("*.json")):
        gs.append(json.loads(p.read_text(encoding="utf-8")))
    return gs


def build_one(g):
    name, sec = g["name"], str(g.get("section", "1"))
    path, sec = find_page(name, sec)
    if g.get("standalone") or not path:
        text, how = standalone(g), ("standalone (no system page)" if not path else "standalone")
    else:
        orig = read_page(path)
        fmt = "mdoc" if re.search(r"^\.Dd", orig, re.M) else "man"
        text = add_pointer(orig.rstrip("\n"), fmt) + "\n" + (emit_mdoc(g, True) if fmt == "mdoc" else emit_man(g, True))
        how = f"merged with {path} ({fmt})"
    d = OUT / f"man{sec}"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.{sec}").write_text(text, encoding="utf-8", newline="\n")
    return how


WRAPPER = r'''#!/usr/bin/env bash
# man wrapper installed by mangui: shows the merged page (original + layman guide) when there is one.
REAL="__REAL__"
GUIDE="$HOME/.local/share/mangui"
if [ "${MANGUI:-1}" != "0" ]; then
  passthru=0; nonopt=()
  for a in "$@"; do case "$a" in -*) passthru=1;; *) nonopt+=("$a");; esac; done
  if [ "$passthru" = 0 ]; then
    name=""; secs="1 8 5 7 6 3 2 4"
    if [ "${#nonopt[@]}" -eq 1 ]; then name="${nonopt[0]}"
    elif [ "${#nonopt[@]}" -eq 2 ] && [[ "${nonopt[0]}" =~ ^[0-9]$ ]]; then secs="${nonopt[0]}"; name="${nonopt[1]}"; fi
    if [ -n "$name" ]; then
      for s in $secs; do f="$GUIDE/man$s/$name.$s"; if [ -f "$f" ]; then exec "$REAL" -l "$f"; fi; done
    fi
  fi
fi
exec "$REAL" "$@"
'''


def install(refresh=False):
    gs = load_guides()
    for g in gs:
        print(f"  {g['name']:<10} {build_one(g)}")
    BIN.mkdir(parents=True, exist_ok=True)
    w = BIN / "man"
    w.write_text(WRAPPER.replace("__REAL__", real_man()), encoding="utf-8", newline="\n")
    w.chmod(0o755)
    line = 'export PATH="$HOME/.local/bin:$PATH"'
    for rc in (HOME / ".bashrc", HOME / ".zshrc"):
        if rc.exists() and MARK not in rc.read_text(encoding="utf-8", errors="ignore"):
            with rc.open("a", encoding="utf-8", newline="\n") as f:
                f.write(f"\n{MARK}: enhanced man pages\n{line}\n")
    print(f"installed {len(gs)} pages in {OUT}; wrapper in {w}. Open a new terminal, then try: man {gs[0]['name'] if gs else 'file'}")


def uninstall():
    shutil.rmtree(OUT, ignore_errors=True)
    w = BIN / "man"
    if w.exists() and "mangui" in w.read_text(encoding="utf-8", errors="ignore"):
        w.unlink()
    for rc in (HOME / ".bashrc", HOME / ".zshrc"):
        if rc.exists():
            t = rc.read_text(encoding="utf-8", errors="ignore")
            t2 = re.sub(rf"\n{re.escape(MARK)}: enhanced man pages\nexport PATH=\"\$HOME/\.local/bin:\$PATH\"\n", "\n", t)
            if t2 != t:
                rc.write_text(t2, encoding="utf-8", newline="\n")
    print("removed")


def options_of(name, sec):
    r = subprocess.run(f'MANWIDTH=200 {real_man()} {sec} {name} 2>/dev/null </dev/null | col -bx', shell=True, capture_output=True, text=True)
    found = set()
    for ln in r.stdout.split("\n"):
        m = re.match(r"^\s{2,12}(-.*)$", ln)
        if m:
            found |= set(re.findall(r"(?<![\w-])(--?[A-Za-z0-9][\w-]*)", m.group(1).split("  ")[0]))
    return found


def coverage():
    tot_a = tot_b = 0
    for g in load_guides():
        have = set()
        for op in g["options"]:
            have |= set(re.findall(r"(?<![\w-])(--?[A-Za-z0-9][\w-]*)", op["flag"]))
        orig = options_of(g["name"], str(g.get("section", "1")))
        if not orig:
            print(f"  {g['name']:<10} (no system page here)  guide documents {len(have)} options")
            continue
        got = orig & have
        tot_a += len(got)
        tot_b += len(orig)
        miss = sorted(orig - have)
        print(f"  {g['name']:<10} {len(got):>3}/{len(orig):<3} options explained" + (f"   missing: {' '.join(miss[:12])}{' ...' if len(miss) > 12 else ''}" if miss else "   COMPLETE"))
    print(f"total {tot_a}/{tot_b}")


def listing():
    for g in load_guides():
        p, sec = find_page(g["name"], str(g.get("section", "1")))
        print(f"  {g['name']:<10} {'standalone' if g.get('standalone') else ('merge into ' + p if p else 'standalone (no system page)')}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd in ("install", "refresh"):
        install()
    elif cmd == "uninstall":
        uninstall()
    elif cmd == "coverage":
        coverage()
    elif cmd == "list":
        listing()
    else:
        print(__doc__)
