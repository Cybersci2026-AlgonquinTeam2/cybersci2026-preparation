#!/usr/bin/env python3
"""Author and capture layman guides for mangui (mangui/guides/*.json).

    python scripts/mangui_build.py                # capture real output for every guide below, write the JSON
    python scripts/mangui_build.py --only file

Each example command is run for real in the Command Atlas lab (inside WSL, or natively on Linux/Kali); the output stored in
the guide is what the tool printed. Options are authored by hand: the goal is every option in the original page.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_build as B  # noqa: E402
import atlas_tools as T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "mangui" / "guides"

GUIDES = []

# ============================================================== file
GUIDES.append(dict(
    name="file", section="1", version_cmd="file --version | head -1",
    one_line="determine a file's real type by reading its contents",
    plain=["`file` looks at the first bytes inside a file (its \"magic number\") and tells you what the file really is.",
           "A name such as holiday.txt proves nothing: anyone can rename a picture to .txt. `file` ignores the name and reads the contents, so it is the first command to run on anything you did not create."],
    when=["A download, e-mail attachment or CTF file has no extension, or the wrong one.",
          "You must decide how to open something: image viewer, archive tool, disassembler or text editor.",
          "You want to know if a program is 32-bit or 64-bit, or whether it has been stripped, before you debug it."],
    examples=[
        ("What is each file really?", "file hello pic.png holiday.txt access.log"),
        ("Just the answer, no file name  (-b)", "file -b holiday.txt"),
        ("A MIME type for scripts  (-i)", "file -i hello pic.png access.log"),
        ("Only the type word  (--mime-type)", "file --mime-type pic.png access.log"),
        ("Only the character encoding  (--mime-encoding)", "file --mime-encoding pic.png access.log"),
        ("Show every match  (-k)", "file -k pic.png"),
        ("Look inside a compressed file  (-z)", "file notes.txt.gz; file -z notes.txt.gz"),
        ("Follow a symbolic link  (-L)", "ln -sf pic.png link.png; file link.png; file -L link.png"),
        ("Check many names from a list  (-f)", "printf 'hello\\nusers.txt\\n' > names.txt; file -f names.txt"),
        ("Change the separator  (-F)", "file -F '=>' users.txt notes.txt"),
        ("Separate answers with NUL bytes  (-0)", "file -0 users.txt notes.txt | od -c | head -3"),
        ("Likely file extensions  (--extension)", "file --extension pic.png access.log"),
    ],
    options=[
        ("-b, --brief", "Print only the description, without the file name in front.", "You are scripting or you only want the answer."),
        ("-i, --mime", "Print a MIME type and encoding (image/png; charset=binary) instead of the long description.", "Sorting or filtering files by kind in a script."),
        ("--mime-type", "Print only the MIME type, for example image/png.", "You want a short, stable word to compare against."),
        ("--mime-encoding", "Print only the character encoding: us-ascii, utf-8 or binary.", "Deciding whether a file is text or raw bytes."),
        ("--extension", "Print the file extensions that normally go with this type.", "A file has no extension and you want to name it properly."),
        ("--apple", "Print an old Apple (Mac) creator and type code instead of the usual description.", "Rarely: identifying legacy Mac files."),
        ("-k, --keep-going", "Do not stop at the first match; show every type that fits.", "A file may be two things at once (a polyglot) or hide a second format."),
        ("-z, --uncompress", "Look inside compressed files (gzip, bzip2, xz) and describe what is inside as well.", "You want to know what a .gz contains without extracting it."),
        ("-Z, --uncompress-noreport", "Look inside compressed files but report only the inside, not the fact that it is compressed.", "You only care about the content type."),
        ("-L, --dereference", "Follow symbolic links, so you describe the target, not the link.", "A path may be a shortcut to the real file."),
        ("-h, --no-dereference", "Do not follow symbolic links: describe the link itself. This is the default on most systems.", "You want to confirm that something is a link."),
        ("-f, --files-from namefile", "Read the names of the files to check from a text file, one per line.", "Checking hundreds of files without a huge command line."),
        ("-F, --separator separator", "Change the separator printed between the file name and the answer (default is a colon).", "Making output easy to cut or parse."),
        ("-0, --print0", "End each file name with a NUL byte instead of a newline, to pair with xargs -0 or cut.", "File names contain spaces or odd characters."),
        ("-N, --no-pad", "Do not line up the answers in a column.", "You want compact output."),
        ("-n, --no-buffer", "Flush the output after every file instead of in chunks.", "You feed file's output to another program and need results immediately."),
        ("-s, --special-files", "Also read special files such as disks (/dev/sda) and partitions, which are normally skipped.", "Identifying a disk image or partition on a block device (needs permission)."),
        ("-p, --preserve-date", "Try to leave the file's last-access time unchanged.", "Evidence handling, when you do not want to change timestamps."),
        ("-r, --raw", "Do not translate unprintable characters into \\ooo escape codes.", "You are going to process the exact bytes yourself."),
        ("-m, --magic-file magicfiles", "Use your own list of magic rules (colon-separated files) instead of the built-in database.", "You are teaching file a format it does not know."),
        ("-C, --compile", "Turn a text magic file into the fast binary form (magic.mgc).", "After writing your own magic rules."),
        ("-l, --list", "List the magic patterns in the order they are checked, with their strength.", "Debugging why file picked one answer over another."),
        ("-c, --checking-printout", "Print the parsed form of the magic file (used with -m to check your rules).", "Checking a hand-written magic file."),
        ("-e, --exclude testname", "Skip one kind of test (apptype, ascii, cdf, compress, csv, elf, encoding, json, soft, tar, text, tokens).", "A test gives wrong or slow answers."),
        ("--exclude-quiet", "Same as -e, but ignore an unknown test name instead of complaining.", "Scripts that must work with older versions of file."),
        ("-P, --parameter name=value", "Change a limit, such as how many bytes or how deep file looks (bytes, elf_notes, indir, name, regex).", "A big file is mis-identified because the check stops too early."),
        ("-E", "Report file system errors (such as a missing file) as errors with a non-zero exit status, not as normal output.", "Scripts that must notice a missing file."),
        ("-S, --no-sandbox", "Turn off the security sandbox that restricts what file may do while it works.", "Only if the sandbox breaks file on your system."),
        ("-d", "Print debugging information to standard error.", "You are developing magic rules and need to see how they match."),
        ("-v, --version", "Print the version and exit.", "Checking which release you have; options differ between versions."),
        ("--help", "Print a short usage message and exit.", "A quick reminder of the options without opening the manual."),
    ],
    mistakes=["Trusting the extension. Always run file first.",
              "Treating the answer as proof: file reads only a few bytes and can be fooled by a crafted file. Confirm with a format-specific tool.",
              "Forgetting -z for .gz files and wondering what is inside.",
              "Using -i and expecting a nice sentence: -i prints MIME types, not descriptions.",
              "Pointing file at a huge or unknown file from an untrusted source: it is safe, but do not execute the result."],
    try_=["Copy a picture to notes.txt and run file on both.",
          "Run file on /bin/ls, then on a shell script, then on a folder.",
          "Run file -k on a PDF and a ZIP, and compare with plain file.",
          "Make a list of ten files and check them all with -f and -b."],
    see_also="xxd(1) shows the bytes file is reading, strings(1) the text inside, exiftool(1) the metadata, binwalk(1) files hidden inside files, magic(5) the rule format.",
))

# ============================================================== grep
GUIDES.append(dict(
    name="grep", section="1", version_cmd="grep --version | head -1",
    one_line="print lines that match a pattern",
    plain=["`grep` reads text and prints only the lines that contain what you are looking for. It is how you find a flag, a password, an IP address or an error in a pile of text.",
           "You give it a pattern and one or more files (or pipe text into it). Patterns can be plain words or regular expressions, and many options change what counts as a match and what is printed."],
    when=["Find a flag, password or username inside a log, dump, memory image or whole folder.",
          "Count or list evidence: failed logins, an IP, a path, a user agent.",
          "Filter the output of another command (cmd | grep word)."],
    examples=[
        ("Find a word, ignoring case, with line numbers  (-i -n)", "grep -in password notes.txt"),
        ("Count matching lines  (-c)", "grep -c ' 401 ' access.log"),
        ("Everything except the boring lines  (-v)", "grep -v ' 200 ' access.log"),
        ("Only the matching part  (-o, -E)", "grep -oE '^[0-9]+(\\.[0-9]+){3}' access.log | sort | uniq -c | sort -rn"),
        ("Context around a hit  (-C)", "grep -n -C1 ' 302 ' access.log"),
        ("Search a whole folder  (-r)", "grep -rn 'secret' site"),
        ("Find text inside a binary  (-a, -o)", "grep -a -o 'flag{[^}]*}' pic.png"),
        ("Byte offset of a match  (-b -a -o)", "grep -abo 'flag{' pic.png"),
        ("Why -F matters", "printf 'flag{1x3}\\nflag{1.3}\\n' > t.txt; echo '--- regex:'; grep 'flag{1.3}' t.txt; echo '--- fixed string:'; grep -F 'flag{1.3}' t.txt"),
        ("Whole words only  (-w)", "printf 'root\\nrootkit\\n' > w.txt; grep root w.txt; echo ---; grep -w root w.txt"),
        ("List files that match  (-l)", "grep -rl 'x' site | sort"),
        ("Several patterns at once  (-e)", "grep -e ' 401 ' -e ' 404 ' access.log"),
        ("Just the exit status  (-q)", "grep -q admin access.log && echo found admin"),
        ("Stop after the first match  (-m)", "grep -m1 'login' access.log"),
    ],
    options=[
        ("-E, --extended-regexp", "Treat the pattern as an extended regular expression, where + ? | ( ) work without backslashes.", "Anything beyond a plain word."),
        ("-F, --fixed-strings", "Treat the pattern as plain text, not a regular expression.", "The pattern has characters like . { [ that you want literally (IPs, flags, copied log text)."),
        ("-G, --basic-regexp", "Treat the pattern as a basic regular expression. This is the default.", "You want to be explicit, or undo an earlier -E."),
        ("-P, --perl-regexp", "Treat the pattern as a Perl-style regular expression (lookahead, \\d).", "Complex patterns that -E cannot express; not available in every grep."),
        ("-e PATTERNS, --regexp=PATTERNS", "Give the pattern with an option, so you can use several -e and patterns that start with a dash.", "Searching for more than one thing, or for -x."),
        ("-f FILE, --file=FILE", "Read the patterns from a file, one per line.", "A long list of indicators (bad IPs, keywords)."),
        ("-i, --ignore-case", "Ignore upper and lower case.", "You do not know if it is Password or PASSWORD."),
        ("--no-ignore-case", "Turn off an earlier -i (for example from an alias).", "An alias adds -i and you want a case-sensitive search."),
        ("-v, --invert-match", "Show lines that do NOT match.", "Remove the noise to see what is left."),
        ("-w, --word-regexp", "Match whole words only.", "root should not match rootkit."),
        ("-x, --line-regexp", "Match only when the whole line matches.", "Exact-line checks, such as a specific entry in a list."),
        ("-c, --count", "Print the number of matching lines instead of the lines.", "How many failures? how many hits?"),
        ("--color[=WHEN], --colour[=WHEN]", "Highlight the matches in colour (WHEN is always, never or auto).", "Reading results on a terminal; use always when piping into less -R."),
        ("-L, --files-without-match", "List only the names of files that contain no match.", "Which files lack a required line?"),
        ("-l, --files-with-matches", "List only the names of files that contain a match.", "Which files mention this? Fast triage of a folder."),
        ("-m NUM, --max-count=NUM", "Stop after NUM matching lines.", "Huge files where the first hit is enough."),
        ("-o, --only-matching", "Print only the matched part of the line.", "Pull out IPs, e-mails, flags."),
        ("-q, --quiet, --silent", "Print nothing; just set the exit status (0 found, 1 not found).", "Inside if statements and scripts."),
        ("-s, --no-messages", "Hide error messages about files that do not exist or cannot be read.", "Recursive searches full of permission errors."),
        ("-b, --byte-offset", "Print the byte position of each match (with -o, of the match itself).", "Locating data in a binary so you can open it with xxd -s."),
        ("-H, --with-filename", "Always print the file name in front of each line.", "Searching one file but wanting the name in the output."),
        ("-h, --no-filename", "Never print file names, even for several files.", "You only want the lines."),
        ("--label=LABEL", "Use LABEL as the file name when reading from standard input.", "Piped input should show a name."),
        ("-n, --line-number", "Prefix each line with its line number.", "You need to open the file at that spot later."),
        ("-T, --initial-tab", "Align the prefixes (file name, line number) with a tab.", "Neat columns of output."),
        ("-Z, --null", "End file names with a NUL byte instead of a newline (with -l, -L or -H).", "Safe piping to xargs -0 when names contain spaces."),
        ("-A NUM, --after-context=NUM", "Also print NUM lines after each match.", "Read what happened right after the hit."),
        ("-B NUM, --before-context=NUM", "Also print NUM lines before each match.", "Read what led to the hit."),
        ("-C NUM, -NUM, --context=NUM", "Also print NUM lines before and after each match.", "Read the surroundings of a hit."),
        ("--group-separator=SEP", "Use SEP instead of -- between groups of context lines.", "Making context output easier to parse."),
        ("--no-group-separator", "Do not print a separator between groups of context lines.", "Clean output for further processing."),
        ("-a, --text", "Treat a binary file as if it were text.", "Searching images, binaries and memory dumps."),
        ("--binary-files=TYPE", "Say how binary files are handled: binary (default message), text, or without-match.", "Control the Binary file matches message."),
        ("-I", "Skip binary files as if they had no matches.", "Searching source trees without noise from compiled files."),
        ("-U, --binary", "Do not strip carriage returns; read files as raw bytes (matters on Windows).", "Exact byte matching on Windows files."),
        ("-z, --null-data", "Treat input as lines ended by NUL bytes instead of newlines.", "Working with find -print0 output or multi-line records."),
        ("-D ACTION, --devices=ACTION", "Say what to do with devices and sockets: read or skip.", "Avoid hanging on special files."),
        ("-d ACTION, --directories=ACTION", "Say what to do with directories: read, skip or recurse.", "Same as -r when set to recurse."),
        ("-r, --recursive", "Search every file under a folder, not following symbolic links.", "Search a whole project or extracted archive."),
        ("-R, --dereference-recursive", "Like -r, but follow symbolic links.", "A tree uses symlinks to other folders."),
        ("--include=GLOB", "Only search files whose names match GLOB.", "Limit a recursive search to *.py or *.log."),
        ("--exclude=GLOB", "Skip files whose names match GLOB.", "Ignore minified or binary files."),
        ("--exclude-from=FILE", "Skip files that match any pattern listed in FILE.", "A long ignore list."),
        ("--exclude-dir=GLOB", "Skip directories whose names match GLOB.", "Ignore .git or node_modules."),
        ("--line-buffered", "Flush output after every line.", "Watching a live log: tail -f log | grep --line-buffered x."),
        ("-V, --version", "Print the version and exit.", "Checking which grep you have."),
        ("--help", "Print a short usage message and exit.", "A quick reminder without opening the manual."),
    ],
    mistakes=["Quote the pattern: unquoted * and $ are expanded by the shell before grep sees them.",
              "grep pattern * skips hidden files: use -r on the folder.",
              "A dot in a regular expression means any character: escape it (\\.) or use -F for an IP such as 10.0.0.5.",
              "On binary files without -a, grep prints only Binary file matches.",
              "-P is not in every grep (macOS, BusyBox): -E is the portable choice."],
    try_=["Count how many distinct IPs hit /login in access.log.",
          "List every file under site that contains the letter x, with line numbers.",
          "Find the byte offset of the flag text in pic.png, then print the bytes there with xxd -s.",
          "Search a folder recursively but skip .git with --exclude-dir."],
    see_also="rg(1) (ripgrep, faster and respects .gitignore), awk(1), sed(1), find(1), strings(1), zgrep(1) to search compressed files.",
))


# further batches live in their own modules
for _m in ('mangui_batch2', 'mangui_batch3'):
    try:
        GUIDES.extend(__import__(_m).GUIDES)
    except ImportError:
        pass


def capture(g):
    parts = ["set +e", T.LAB_SETUP]
    for i, ex in enumerate(g["examples"]):
        parts.append(f'echo "@@S{i}"; ( {ex[1]} ) </dev/null 2>&1 | head -n 25 | cut -c1-140; echo "@@E{i}"')
    parts.append(f'echo "@@V"; ( {g["version_cmd"]} ) 2>&1 | head -1')
    raw = B.run_wsl("\n".join(parts))
    outs = {}
    for i in range(len(g["examples"])):
        m = re.search(rf"@@S{i}\n(.*?)\n?@@E{i}", raw, re.S)
        outs[i] = m.group(1) if m else ""
    ver = re.search(r"@@V\n(.*)", raw)
    return outs, (ver.group(1).strip() if ver else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for g in GUIDES:
        if a.only and g["name"] != a.only:
            continue
        outs, ver = capture(g)
        doc = dict(name=g["name"], section=g["section"], one_line=g["one_line"], plain=g["plain"], when=g["when"],
                   examples=[dict(title=e[0], cmd=e[1].replace("\\n", "\\n"), output=outs[i]) for i, e in enumerate(g["examples"])],
                   options=[dict(flag=o[0], plain=o[1], use=o[2]) for o in g["options"]], mistakes=g["mistakes"], **{"try": g["try_"]},
                   see_also=g["see_also"], captured_with=f"Example output captured {date.today().isoformat()} with {ver} on {'Linux' if B.LOCAL else 'Ubuntu 24.04 (WSL)'}. The lab files are created by scripts/atlas_tools.py.")
        (OUT / f"{g['name']}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        empty = [e[0] for i, e in enumerate(g["examples"]) if not outs[i]]
        print(f"{g['name']:6s} {len(g['examples'])} examples, {len(g['options'])} options |", ver, "| empty outputs:", empty or "none")


if __name__ == "__main__":
    main()
