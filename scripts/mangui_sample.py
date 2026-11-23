#!/usr/bin/env python3
"""SAMPLE of the 'enhanced man page' idea: take the system's real page for `file`, append a layman guide, render it.

    python scripts/mangui_sample.py

Writes the merged page into WSL (/tmp/mangui_sample/man1/file.1, nothing in your home), renders it with the normal `man`,
and saves the rendered result to curriculum/atlas/SAMPLE-man-file.txt so you can judge the idea before the full build.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_build as B  # noqa: E402
import atlas_tools as T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# examples whose output is captured for real
EX = [
    ("What is each file really?", "file hello pic.png holiday.txt access.log"),
    ("Just the answer, no file name  (-b)", "file -b holiday.txt"),
    ("Machine-readable type  (-i)", "file -i hello pic.png access.log"),
    ("Show every match, not only the first  (-k)", "file -k pic.png"),
    ("Look inside a compressed file  (-z)", "file notes.txt.gz; file -z notes.txt.gz"),
    ("Follow a symbolic link  (-L)", "ln -sf pic.png link.png; file link.png; file -L link.png"),
    ("Check many names from a list  (-f)", "printf 'hello\\nusers.txt\\n' > names.txt; file -f names.txt"),
    ("Change the separator  (-F)", "file -F '=>' users.txt notes.txt"),
]


def capture():
    parts = ["set +e", T.LAB_SETUP]
    for i, (_, cmd) in enumerate(EX):
        parts.append(f'echo "@@S{i}"; ( {cmd} ) </dev/null 2>&1 | cut -c1-150; echo "@@E{i}"')
    parts.append('echo "@@V"; file --version | head -1')
    raw = B.run_wsl("\n".join(parts))
    out = {}
    for i in range(len(EX)):
        m = re.search(rf"@@S{i}\n(.*?)\n?@@E{i}", raw, re.S)
        out[i] = m.group(1) if m else ""
    ver = re.search(r"@@V\n(.*)", raw).group(1).strip()
    return out, ver


def tx(s):
    """text line safe for mdoc: escape backslash and neutralise a leading macro or dot."""
    s = s.replace("\\", "\\e").replace("-", "\\-")
    s = re.sub(r"`([^`]+)`", r"\\fB\1\\fP", s)
    return "\\&" + s if s[:1] in (".", "'") or re.match(r"^[A-Z][a-z]\b", s) else s


def mdoc_section(out, ver):
    o = [".Sh LAYMAN GUIDE",
         "Added by the CyberSci Command Atlas. Everything above this line is the original manual page; nothing in it was changed.",
         '.Ss "In plain words"',
         "\\&" + tx("`file` looks at the first bytes inside a file (its \"magic number\") and tells you what the file really is."),
         tx("A name such as holiday.txt proves nothing: anyone can rename a picture to .txt."),
         tx("`file` ignores the name and reads the contents, so it is the first command to run on anything you did not create."),
         ".Ss When you would use it",
         ".Bl -bullet -compact",
         ".It", tx("A download, e-mail attachment or CTF file has no extension, or the wrong one."),
         ".It", tx("You must decide how to open something: image viewer, archive tool, disassembler or text editor."),
         ".It", tx("You want to know if a program is 32-bit or 64-bit before you debug it."),
         ".El",
         ".Ss Examples with real output"]
    for i, (title, cmd) in enumerate(EX):
        o += [".Pp", ".Sy " + '"' + title.replace('"', "'") + '"', ".Bd -literal -offset indent", tx("$ " + cmd)]
        o += [tx(l) for l in (out[i] or "(no output)").split("\n")] + [".Ed"]
    o += [".Ss The options in plain English",
          ".Bl -tag -width Ds",
          ".It Sy -b", tx("Brief. Print only the description, without the file name. Use it in scripts or when you only want the answer."),
          ".It Sy -i", tx("Print a MIME type (such as image/png or text/plain) instead of the long description. Best for scripts and for sorting files by kind."),
          ".It Sy -k", tx("Keep going after the first match. Some files are two things at once (a polyglot); this shows both."),
          ".It Sy -z", tx("Look inside a compressed file and describe what is in it, not just that it is compressed."),
          ".It Sy -L", tx("Follow symbolic links, so you describe the target, not the link."),
          ".It Sy -f", tx("Read the list of files to check from a text file, one per line."),
          ".It Sy -F", tx("Change the separator between the file name and the answer (the default is a colon)."),
          ".It Sy -s", tx("Also read special files such as disks and partitions (needs permission). Use it to identify a disk image on a block device."),
          ".It Sy -m", tx("Use your own magic database. Advanced: teach file to recognise a format you invented."),
          ".El",
          ".Ss Mistakes people make",
          ".Bl -bullet -compact",
          ".It", tx("Trusting the extension. Always run file first."),
          ".It", tx("Treating the answer as proof. file reads a few bytes and can be fooled by a crafted file; confirm with a format-specific tool."),
          ".It", tx("Forgetting -z for .gz files and then wondering what is inside."),
          ".El",
          ".Ss Try this",
          ".Bl -enum -compact",
          ".It", tx("Copy a picture to notes.txt and run file on both."),
          ".It", tx("Run file on /bin/ls, then on a shell script, then on a folder."),
          ".It", tx("Run file -k on a PDF and a ZIP, and compare."),
          ".El",
          ".Ss See also",
          tx("xxd(1) to see the bytes file is reading, strings(1) for the text inside, exiftool for metadata, binwalk for files hidden inside files."),
          ".Ss About these examples",
          tx("Outputs above were produced by running the commands on " + ver + ". The lab files are created by the Command Atlas (curriculum/atlas).")]
    return "\n".join(o) + "\n"


def main():
    out, ver = capture()
    # original page
    orig = B.run_wsl('zcat "$(man -w file)" 2>/dev/null || cat "$(man -w file)"')
    if not orig.strip():
        sys.exit("could not read the system page for file(1)")
    fmt = "mdoc" if re.search(r"^\.Dd", orig, re.M) else "man"
    print("original format:", fmt, "| lines:", len(orig.split("\n")))
    assert fmt == "mdoc", "this sample only handles mdoc pages; the full build also has a man(7) emitter"
    merged = orig.rstrip("\n") + "\n" + mdoc_section(out, ver)
    # write the merged page and render it with the ordinary man command in ONE WSL session (WSL may clear /tmp between sessions)
    script = ("mkdir -p /tmp/mangui_sample/man1\ncat > /tmp/mangui_sample/man1/file.1 <<'ROFF_EOF'\n" + merged
              + "ROFF_EOF\nMANWIDTH=78 man -l /tmp/mangui_sample/man1/file.1 2>&1 | col -bx\n")
    rendered = B.run_wsl(script)
    (ROOT / "curriculum" / "atlas" / "SAMPLE-man-file.txt").write_text(rendered, encoding="utf-8", newline="\n")
    i = max(rendered.find("LAYMAN GUIDE"), 0)
    print("rendered lines:", len(rendered.split("\n")), "| guide starts at line", rendered[:i].count("\n") + 1)
    print(rendered[i - 40:i + 4200])


if __name__ == "__main__":
    main()
