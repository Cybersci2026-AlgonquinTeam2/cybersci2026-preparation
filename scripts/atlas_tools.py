"""Definitions for the Command Atlas (see atlas_build.py). Prose is written by hand; every recipe's output is captured by really running it."""

LAB_SETUP = r"""
rm -rf /tmp/atlas; mkdir -p /tmp/atlas && cd /tmp/atlas
cat > access.log <<'L'
10.0.0.5 - - [14/Nov/2026:10:01:12 +0000] "GET /index.html HTTP/1.1" 200 1043
10.0.0.5 - - [14/Nov/2026:10:01:15 +0000] "GET /login HTTP/1.1" 200 512
10.0.0.9 - - [14/Nov/2026:10:02:01 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:03 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:05 +0000] "POST /login HTTP/1.1" 401 87
10.0.0.9 - - [14/Nov/2026:10:02:09 +0000] "POST /login HTTP/1.1" 302 0
10.0.0.9 - - [14/Nov/2026:10:02:15 +0000] "GET /admin HTTP/1.1" 200 2210
10.0.0.7 - - [14/Nov/2026:10:03:40 +0000] "GET /../../etc/passwd HTTP/1.1" 400 0
10.0.0.7 - - [14/Nov/2026:10:03:44 +0000] "GET /backup.zip HTTP/1.1" 404 196
L
cat > users.txt <<'L'
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice Lee:/home/alice:/bin/bash
bob:x:1002:1002:Bob Ray:/home/bob:/bin/sh
svc-backup:x:998:998::/var/backups:/usr/sbin/nologin
L
cat > notes.txt <<'L'
Meeting at 3pm
Password reset for bob: Summer2026!
TODO: rotate keys
password policy: 12 characters
The flag format is flag{...}
Remember: PASSWORD files are case sensitive?
L
mkdir -p site/css site/js site/uploads
echo '<h1>Demo site</h1>' > site/index.html
echo 'Disallow: /admin' > site/robots.txt
echo 'body{}' > site/css/main.css
echo 'alert(1)' > site/js/app.js
echo 'x' > site/uploads/report.pdf
echo 'secret=1' > site/.env
chmod 600 site/.env
touch -d '2026-11-10 10:00' site/index.html site/robots.txt
printf '#!/bin/sh\necho hi\n' > run.sh; chmod +x run.sh
cat > hello.c <<'C'
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
    const char *secret = "flag{demo_not_a_real_flag}";
    if (argc > 1 && strcmp(argv[1], "open-sesame") == 0) { puts(secret); return 0; }
    puts("access denied");
    return 1;
}
C
gcc -o hello hello.c 2>/dev/null
python3 - <<'PY'
import zlib, struct
def ch(t, d): c = struct.pack('>I', len(d)) + t + d; return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(b'\x00\xff\x00\x00')) + ch(b'IEND', b'')
open('pic.png', 'wb').write(png + b'hidden: flag{demo_not_a_real_flag}')
PY
cp pic.png holiday.txt
gzip -k notes.txt
printf 'aGVsbG8gd29ybGQ=\n' > data.b64
cat > echo.py <<'PY'
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def _go(self):
        if self.path == '/old':
            self.send_response(301); self.send_header('Location', '/new'); self.end_headers(); return
        if self.path in ('/admin', '/missing'):
            self.send_response(403 if self.path == '/admin' else 404); self.end_headers(); return
        n = int(self.headers.get('Content-Length') or 0); body = self.rfile.read(n).decode()
        out = f"{self.command} {self.path}\n" + "".join(f"{k}: {v}\n" for k, v in self.headers.items() if k.lower() not in ('host', 'accept-encoding', 'connection')) + ("\n" + body if body else "")
        self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.send_header('X-Demo', 'echo'); self.end_headers(); self.wfile.write(out.encode())
    do_GET = do_POST = do_PUT = do_HEAD = _go
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', 8099), H).serve_forever()
PY
"""

START_ECHO = "cd /tmp/atlas; python3 echo.py > /dev/null 2>&1 & echo $! > /tmp/atlas/echo.pid; sleep 1"
STOP_ECHO = "kill $(cat /tmp/atlas/echo.pid) 2>/dev/null"

TOOLS = []

# ------------------------------------------------------------------ grep
TOOLS.append(dict(
    name="grep", version="grep --version",
    one_line="Search text (or binary data) for lines that match a pattern, and print them.",
    when=["Find a flag, password or username inside a log, dump, memory image or whole folder.",
          "Count or list evidence: failed logins, an IP, a path, a user agent.",
          "Filter the output of another command (`cmd | grep ...`)."],
    anatomy="""grep  -i  -n  -E  'pattern'  file1 file2
 |    |   |   |     |         '--- files to search (or a folder with -r; or stdin if omitted)
 |    |   |   |     '------------- the pattern (quote it so the shell leaves it alone)
 |    |   |   '------------------- -E = extended regular expressions (+ ? | () work)
 |    |   '----------------------- -n = print line numbers
 |    '--------------------------- -i = ignore upper/lower case
 '-------------------------------- the program""",
    flags=[("-i", "Ignore case", "You do not know if it is `Password` or `PASSWORD`"),
           ("-v", "Invert: show lines that do NOT match", "Remove the noise to see what is left"),
           ("-n", "Prefix lines with their line number", "You need to open the file at that spot later"),
           ("-c", "Count matching lines instead of printing them", "How many failures? how many hits?"),
           ("-o", "Print only the matching part", "Pull out IPs, emails, flags"),
           ("-E", "Extended regex (`+ ? | ( )` need no backslash)", "Anything beyond a plain word"),
           ("-F", "Fixed string: treat the pattern as plain text", "The pattern has `{ } . * [` characters you want literally"),
           ("-w / -x", "Match whole words / whole lines only", "`root` should not match `rootkit`"),
           ("-r / -R", "Recurse into folders (-R follows symlinks)", "Search a whole project or extracted archive"),
           ("-l / -L", "List only file names that do / do not match", "Which files contain it?"),
           ("-A N / -B N / -C N", "Show N lines After / Before / around the match", "Read the context of a hit"),
           ("-a", "Treat binary files as text", "Search images, binaries, memory dumps"),
           ("-b", "Print the byte offset of each match", "Locate data inside a binary for `xxd`/`dd`"),
           ("--include='*.py' / --exclude-dir=.git", "Limit which files a recursive search reads", "Large trees with noise"),
           ("-P", "Perl-style regex (lookahead, `\\d`)", "Complex patterns; not available on every system"),
           ("-m N", "Stop after N matches", "Huge files; you only need the first hit"),
           ("-q", "Quiet: no output, just the exit status", "Use in `if grep -q ...; then`")],
    recipes=[
     dict(title="Find a word, ignoring case, with line numbers", cmd="grep -in password notes.txt",
          why="Notes mix `Password` and `PASSWORD`. `-i` catches both; `-n` tells you where.",
          read="Three lines match even though the capitalisation differs. Without `-i` you would miss two of them."),
     dict(title="Count failed logins", cmd="grep -c ' 401 ' access.log",
          why="`-c` prints a number instead of the lines. The spaces around `401` avoid matching `4010` or a byte count.",
          read="The number is how many lines contain the HTTP status 401 (unauthorised)."),
     dict(title="Everything except the boring lines", cmd="grep -v ' 200 ' access.log",
          why="`-v` inverts the match. Drop the normal successes and read what is left.",
          read="Failed logins, a redirect, a path traversal attempt and a 404 remain. This is how you triage a log."),
     dict(title="Ranked list of source IPs (pipeline)", cmd="grep -oE '^[0-9]+(\\.[0-9]+){3}' access.log | sort | uniq -c | sort -rn",
          show="grep -oE '^[0-9]+(\\.[0-9]+){3}' access.log | sort | uniq -c | sort -rn",
          why="`-o` prints only the matched IP, `sort | uniq -c` counts duplicates, `sort -rn` ranks them.",
          read="The first line is the noisiest client. The same pattern (match, sort, count, rank) works on usernames, paths and user agents."),
     dict(title="Context around a hit", cmd="grep -n -C1 ' 302 ' access.log",
          why="`-C1` shows one line before and after. A 302 after several 401s means the login finally worked.",
          read="Three failures, then the redirect, then the admin page: a brute-force that succeeded."),
     dict(title="Search a whole folder", cmd="grep -rn 'secret' site",
          why="`-r` descends into folders, `-n` adds line numbers. Hidden files (names starting with a dot) are included.",
          read="The `.env` file shows up with its file name and line number."),
     dict(title="Find text inside a binary file", cmd="grep -a -o 'flag{[^}]*}' pic.png",
          why="`-a` makes grep read binary as text. This is the fastest check for data appended to an image.",
          read="A flag-shaped string was hidden after the end of the picture. (The flag here is a demo value.)"),
     dict(title="Why -F matters", cmd="printf 'flag{1x3}\\nflag{1.3}\\n' > t.txt; echo '--- regex:'; grep 'flag{1.3}' t.txt; echo '--- fixed string:'; grep -F 'flag{1.3}' t.txt",
          why="In a regex the dot means 'any single character', so it matches the `x` too. `-F` matches the characters exactly as typed.",
          read="The regex version prints both lines; the `-F` version prints only the one with a real dot. Use `-F` for anything copied from a log, an IP or a flag.")],
    gotchas=["Quote the pattern: unquoted `*` and `$` are expanded by the shell before grep sees them.",
             "`grep pattern *` skips hidden files; use `-r` on the folder.",
             "A dot `.` in a regex means any character; escape it (`\\.`) or use `-F` for an IP such as `10.0.0.5`.",
             "On binary files without `-a`, grep says `Binary file matches` and prints nothing useful.",
             "`-P` is not in every grep (macOS, BusyBox): `-E` is the portable choice."],
    related=["rg (ripgrep: faster, respects .gitignore)", "awk", "sed", "find", "strings", "zgrep (search .gz without extracting)"],
    practice=["Count how many distinct IPs hit `/login` in `access.log`.", "List every file under `site` that contains the letter `x`, with line numbers.",
              "Find the byte offset of the flag text in `pic.png`, then print the bytes there with `xxd -s`."],
    cards=["What does `grep -c` print?", "Difference between `-F` and `-E`?", "How do you search binary files for text?", "How do you list only file names that match?", "What exit status means 'not found'?"]))

# ------------------------------------------------------------------ find
TOOLS.append(dict(
    name="find", version="find --version",
    one_line="Walk a folder tree and list (or act on) files that match conditions such as name, size, type, time or permissions.",
    when=["Locate a file when you only know part of its name, its type or when it changed.",
          "Privilege escalation checks: world-writable files, SUID binaries, files owned by a user.",
          "Run a command on every matching file (`-exec`)."],
    anatomy="""find  site  -type f  -name '*.js'  -size -1k  -exec wc -c {} \\;
 |     |      |         |            |           '--- run a command; {} is the file; \\; ends it
 |     |      |         |            '--- tests are ANDed together in order
 |     |      |         '--- match the name against a glob (quote it)
 |     |      '--- f = regular file, d = directory, l = symlink
 |     '--- where to start looking
 '--- the program""",
    flags=[("-name / -iname", "Match the file name with a glob (`-iname` ignores case)", "You remember part of the name"),
           ("-type f|d|l", "Regular file, directory or symlink", "Skip folders or find links"),
           ("-maxdepth N / -mindepth N", "Limit how deep to look", "Avoid huge trees"),
           ("-size +1M / -1k", "Bigger / smaller than a size (`c` bytes, `k`, `M`)", "Find big dumps or tiny stubs"),
           ("-mtime N / -mmin N", "Modified N days / minutes ago (`-1` = less than, `+1` = more than)", "What changed during the incident?"),
           ("-newer FILE", "Newer than another file", "What changed after the first alert?"),
           ("-perm -4000 / -perm /111", "Has all of these bits / any of these bits", "SUID files, executable files"),
           ("-user NAME / -group NAME", "Owned by", "Files an attacker or service user created"),
           ("-empty", "Empty files and folders", "Clean-up or odd leftovers"),
           ("-exec CMD {} \\; / -exec CMD {} +", "Run CMD per file / on batches of files", "Search or hash every match"),
           ("-print0 | xargs -0", "Null-separated output for safe piping", "File names with spaces"),
           ("-delete", "Delete matches (dangerous: test first with `-print`)", "Clean-up only"),
           ("! / -not / -o", "NOT / OR combinators (group with `\\( \\)`)", "More complex conditions")],
    recipes=[
     dict(title="List everything below a folder", cmd="find site | sort",
          why="With no tests, find prints every path. `sort` makes the order stable (find prints in disk order).",
          read="Folders and files, including the hidden `.env`."),
     dict(title="By name, any depth", cmd="find . -name '*.js' | sort",
          why="`-name` takes a glob. Quote it so the shell does not expand it first.",
          read="One JavaScript file. `-iname` would also catch `APP.JS`."),
     dict(title="Hidden files only", cmd="find site -name '.*' -type f",
          why="Names starting with a dot are hidden from plain `ls`. Config files and secrets often live there.",
          read="The `.env` file appears."),
     dict(title="Executable files", cmd="find . -maxdepth 1 -type f -perm /111 | sort",
          why="`/111` means any execute bit is set. `-maxdepth 1` stays in this folder.",
          read="The compiled `hello` and the script `run.sh`. In a real privilege-escalation check you search `-perm -4000` for SUID."),
     dict(title="By age", cmd="find site -type f -newer site/robots.txt | sort",
          why="`-newer` compares modification times with a reference file. I set two files to an older date on purpose.",
          read="Files modified after `robots.txt`: everything except the two aged files. Use this to find what changed after an alert."),
     dict(title="Run a command on each match", cmd="find site -type f -exec grep -l 'x' {} \\; | sort",
          why="`-exec` replaces `{}` with each file name. `\\;` runs the command once per file; `+` batches many files into one run.",
          read="The names of files that contain the letter x."),
     dict(title="Safe piping with spaces in names", cmd="touch 'a file.txt'; find . -name '*.txt' -print0 | xargs -0 wc -c | tail -3",
          why="Without `-print0`/`-0`, a name with a space splits into two arguments and breaks the next command.",
          read="`wc` reports on `a file.txt` correctly because the names were separated by NUL bytes.")],
    gotchas=["Quote globs: `find . -name *.js` can be expanded by the shell and fail.",
             "Order matters for performance, not logic: put cheap tests (`-type`, `-name`) before `-exec`.",
             "`-mtime -1` means less than 24 hours ago, `-mtime 1` means exactly 1 day: easy to mix up.",
             "`-delete` placed before the tests deletes everything: always run with `-print` first.",
             "`find /` as a normal user prints many `Permission denied` lines; add `2>/dev/null`."],
    related=["locate", "fd", "ls -la", "xargs", "stat", "du"],
    practice=["Find every file in `site` larger than 5 bytes.", "List only directories two levels deep.", "Find files owned by your user that are not readable by others."],
    cards=["What does `-perm -4000` find?", "Why use `-print0 | xargs -0`?", "`-exec ... \\;` versus `-exec ... +`?", "How do you find files changed in the last 30 minutes?"]))

# ------------------------------------------------------------------ sed
TOOLS.append(dict(
    name="sed", version="sed --version",
    one_line="A stream editor: read lines, change them with rules (mostly search-and-replace), print the result.",
    when=["Clean up or transform text in a pipeline: strip prefixes, replace separators, mask secrets.",
          "Print a range of lines from a big file.", "Edit a file in place (with a backup)."],
    anatomy="""sed  -E  's/(alice|bob)/[\\1]/g'  users.txt
 |    |        |     |       |  |
 |    |        |     |       |  '--- g = replace every match on the line (default is the first only)
 |    |        |     |       '--- replacement; \\1 is the first group; & is the whole match
 |    |        |     '--- pattern
 |    |        '--- s = substitute command
 |    '--- -E = extended regex
 '--- the program""",
    flags=[("s/old/new/", "Substitute: the core command", "Replace text"),
           ("g / I", "Flags on `s`: all matches / ignore case", "Replace everything, any case"),
           ("-n and p", "Quiet mode plus print", "Print only chosen lines"),
           ("-E", "Extended regex", "Groups and alternation without backslashes"),
           ("-i[SUFFIX]", "Edit the file in place (`-i.bak` keeps a backup)", "Change a file; use a backup suffix"),
           ("N,Md / Np", "Delete / print lines N to M", "Cut a section out"),
           ("/regex/d", "Delete lines that match", "Remove noise"),
           ("-e A -e B", "Several commands", "Several edits in one pass"),
           ("y/abc/xyz/", "Transliterate characters one-to-one", "ROT13-style swaps")],
    recipes=[
     dict(title="Replace a separator", cmd="sed 's/:/ | /g' users.txt | head -2",
          why="`s/old/new/g` replaces every colon on each line. Without `g` only the first per line changes.",
          read="Fields are now separated by ` | `. The original file is untouched: sed prints to the screen."),
     dict(title="Print only chosen lines", cmd="sed -n '2,3p' users.txt",
          why="`-n` turns off automatic printing; `2,3p` prints lines 2 to 3.",
          read="Just alice and bob. Same idea: `sed -n '/ 401 /p'` prints matching lines like grep."),
     dict(title="Delete lines", cmd="sed '/nologin/d' users.txt",
          why="`/regex/d` removes lines that match. The rest are printed.",
          read="The service account with the nologin shell disappears."),
     dict(title="Use a captured group", cmd="sed -E 's/^([a-z-]+):x:([0-9]+):.*/user=\\1 uid=\\2/' users.txt",
          why="`(..)` captures; `\\1`, `\\2` insert the captures; `.*` swallows the rest of the line.",
          read="A compact table of user and uid. Capture groups are the main reason to learn sed."),
     dict(title="Mask secrets", cmd="sed -E 's/(Password reset for [a-z]+: ).*/\\1[REDACTED]/' notes.txt | head -3",
          why="Keep the label in group 1 and replace the secret. Useful before sharing a log.",
          read="The password text is replaced while the rest of the line stays."),
     dict(title="Edit a file in place, with a backup", cmd="cp users.txt copy.txt; sed -i.bak 's/bash/zsh/' copy.txt; diff copy.txt.bak copy.txt",
          why="`-i.bak` rewrites `copy.txt` and saves the original as `copy.txt.bak`. `diff` shows what changed.",
          read="Two lines changed from bash to zsh and the backup holds the original. Never use bare `-i` on something you cannot recover."),
     dict(title="ROT13 with y///", cmd="echo 'synt{ebg13}' | sed 'y/abcdefghijklmnopqrstuvwxyz/nopqrstuvwxyzabcdefghijklm/'",
          why="`y/from/to/` maps characters one for one.",
          read="`synt{ebg13}` becomes `flag{rot13}`. The same shift decodes and encodes.")],
    gotchas=["On macOS `sed -i` needs an argument (`sed -i ''`): scripts differ between GNU and BSD sed.",
             "Use a different delimiter for paths: `s#/usr/bin#/opt#`.",
             "`&` in the replacement means the whole match; escape it (`\\&`) for a literal ampersand.",
             "sed works line by line; to edit across lines use `-z` or switch to Python."],
    related=["awk", "tr", "perl -pe", "ed", "python -c"],
    practice=["Turn `users.txt` into `name -> shell` lines.", "Print only line 4 of `access.log`.", "Replace every IP in `access.log` with `x.x.x.x`."],
    cards=["What does `s/a/b/g` do?", "What does `sed -n '5,9p'` do?", "How do you keep a backup when editing in place?", "What do `\\1` and `&` mean in a replacement?"]))

# ------------------------------------------------------------------ awk
TOOLS.append(dict(
    name="awk", version="awk -W version 2>&1 | head -1; awk --version 2>&1 | head -1",
    one_line="Treat each line as fields and run a tiny program: print columns, filter, count, add up.",
    when=["Pull a column out of a log, `/etc/passwd`, `ps` or a CSV.", "Count events per IP or user (a one-line report).", "Sum or average numbers; reformat output."],
    anatomy="""awk  -F:  '$3 >= 1000 { print $1, $6 }'  users.txt
 |     |    |   |           |            '--- input file
 |     |    |   |           '--- action: print field 1 and field 6
 |     |    |   '--- condition (pattern): field 3 is at least 1000
 |     |    '--- the program is in single quotes
 |     '--- -F sets the field separator (default: whitespace)
 '--- the program""",
    flags=[("-F SEP", "Field separator (`-F:`, `-F,`, `-F'\\t'`)", "Colon, comma or tab separated data"),
           ("$1 $2 ... $NF", "Field 1, 2 ... the last field", "Pick columns"),
           ("$0", "The whole line", "Print or test everything"),
           ("NR / NF", "Line number / number of fields", "Skip headers (`NR>1`), check shape"),
           ("BEGIN { } / END { }", "Run once before / after all lines", "Totals and reports"),
           ("arr[key]++", "Associative arrays", "Counting per key"),
           ("printf", "Formatted output", "Aligned columns"),
           ("-v var=value", "Pass a shell value into awk", "Parameterise a filter"),
           ("~ / !~", "Regex match / no match", "Test a field against a pattern")],
    recipes=[
     dict(title="Print columns", cmd="awk '{print $1, $7, $9}' access.log | head -4",
          why="Fields are split on whitespace: 1 = IP, 7 = path, 9 = status in this log format.",
          read="IP, path, status for each request. Counting fields on one line first (`awk '{print NF}' | head -1`) avoids off-by-one mistakes."),
     dict(title="Filter on a field", cmd="awk '$9 == 401 {print $1, $7}' access.log",
          why="The part before `{...}` is a condition. Only matching lines run the action.",
          read="Only the three failed logins appear."),
     dict(title="Count per IP (associative array)", cmd="awk '{c[$1]++} END {for (ip in c) print c[ip], ip}' access.log | sort -rn",
          why="`c[$1]++` counts per IP. `END` prints the table after all lines are read.",
          read="Requests per IP, busiest first. Same shape as the grep pipeline but you can add conditions."),
     dict(title="Sum a column", cmd="awk '{s += $NF} END {print s, \"bytes in\", NR, \"requests\"}' access.log",
          why="`$NF` is the last field (the byte count). `NR` at the end is the number of lines read.",
          read="Total bytes served and the request count."),
     dict(title="Use another separator", cmd="awk -F: '$3 >= 1000 {print $1, \"->\", $6}' users.txt",
          why="`-F:` splits on colons, as in `/etc/passwd`. Field 3 is the UID, field 6 the home directory.",
          read="Normal users (UID 1000 and up) with their home folders. `svc-backup` (UID 998) is skipped."),
     dict(title="Format a small report", cmd="awk -F: 'BEGIN {printf \"%-12s %-6s\\n\", \"USER\", \"UID\"} {printf \"%-12s %-6s\\n\", $1, $3}' users.txt",
          why="`BEGIN` runs before the first line; `printf` pads columns.",
          read="A neat two-column table. Handy for screenshots in a writeup.")],
    gotchas=["Single-quote the program; double quotes let the shell expand `$1` first.",
             "Fields are 1-based; `$0` is the whole line.",
             "Quoted strings inside awk use double quotes; escape them inside `bash -c`.",
             "awk is not one program: gawk (used for these examples), mawk (the default on some Ubuntu installs) and BSD awk differ in features such as `asort`, `--version` and regex intervals."],
    related=["cut", "sort", "uniq", "sed", "column -t", "python -c"],
    practice=["Print the unique status codes in `access.log` with counts.", "Print lines where the byte count is greater than 1000.", "Print each username in `users.txt` in upper case (`toupper`)."],
    cards=["What is `$NF`?", "What does `NR>1` do?", "How do you count occurrences per key in awk?", "Why single-quote an awk program?"]))

# ------------------------------------------------------------------ inspect trio
TOOLS.append(dict(
    name="file-xxd-strings", version="file --version | head -1; xxd -v 2>&1 | head -1; strings --version | head -1",
    one_line="The first three commands for any unknown file: what is it (`file`), what are its bytes (`xxd`), what text is inside (`strings`).",
    when=["Triage every supplied file before you open or run it.", "The extension and the contents disagree (a `.txt` that is really a PNG).",
          "Find hidden or appended data, magic bytes, embedded paths and flags."],
    anatomy="""file   -k  holiday.txt          # what do the first bytes say it is?
xxd    -l 32  pic.png          # show the first 32 bytes in hex + ASCII
strings -n 8 -t x  hello       # printable runs of 8+ characters, with their hex offset""",
    flags=[("file -k", "Keep going: show all matches, not just the first", "Polyglots and odd formats"),
           ("file -i", "MIME type output", "Scripts and quick filters"),
           ("xxd -l N / -s OFFSET", "Read N bytes / start at an offset (negative = from the end)", "Look at a header or a trailer"),
           ("xxd -c N / -g N", "Bytes per line / group size", "Make the layout fit your screen"),
           ("xxd -p", "Plain hex without offsets", "Copy bytes into a script"),
           ("xxd -r -p", "Reverse: hex text back into bytes", "Decode a hex string"),
           ("strings -n N", "Minimum length of a string (default 4)", "Cut noise"),
           ("strings -a", "Scan the whole file (not only data sections)", "Be sure you did not skip anything"),
           ("strings -t x", "Print the offset of each string (hex)", "Jump to the spot in `xxd`"),
           ("strings -e l", "UTF-16 little-endian strings", "Windows text, memory images")],
    recipes=[
     dict(title="What is this file really?", cmd="file hello pic.png holiday.txt notes.txt.gz access.log",
          why="`file` reads the first bytes (magic numbers), not the name. `holiday.txt` is a copy of the PNG.",
          read="The `.txt` file is identified as a PNG, the gzip as gzip, the binary as an ELF executable. Never trust an extension."),
     dict(title="Look at a header", cmd="xxd -l 32 pic.png",
          why="`-l 32` limits to 32 bytes. Left: offset. Middle: hex bytes. Right: printable ASCII.",
          read="`89 50 4e 47` is the PNG signature (`.PNG`). Every format has one; learn the common ones (PK zip, `%PDF`, ELF `7f 45 4c 46`)."),
     dict(title="Look at the end of a file", cmd="xxd -s -40 pic.png",
          why="A negative `-s` counts from the end. Data after the format's end marker is a classic hiding place.",
          read="After the PNG end chunk (`IEND`) there is readable text that the picture viewer never shows."),
     dict(title="Readable strings with offsets", cmd="strings -n 8 -t x hello | grep -E 'flag|sesame|denied'",
          why="`-t x` prints each string's offset in hex. The pipe keeps the interesting lines.",
          read="The secret text sits in the binary. Note that the passphrase `open-sesame` is visible as a string too: strings often reveals comparison values."),
     dict(title="Convert hex text back to bytes", cmd="echo '666c61677b6865787d' | xxd -r -p; echo",
          why="`-r -p` reverses plain hex into bytes. The extra `echo` adds a newline.",
          read="Hex that looks random is often just ASCII. This one decodes to a flag-shaped string."),
     dict(title="UTF-16 text hides from plain strings", cmd="printf 'p\\0a\\0s\\0s\\0w\\0o\\0r\\0d\\0' > wide.bin; strings wide.bin; echo '--- with -e l:'; strings -e l wide.bin",
          why="Windows stores text as 16-bit characters, so there are NUL bytes between letters and plain `strings` finds nothing.",
          read="The first command prints nothing; the second recovers `password`. Use `-e l` on memory dumps and Windows artefacts.")],
    gotchas=["`file` can be wrong for polyglots (one file valid as two formats): use `file -k` and a format-specific parser.",
             "`strings` shows only runs of printable characters; encoded or compressed data will not appear.",
             "Hex dumps show bytes in file order; multi-byte numbers in x86 files are little-endian (`ef be ad de` = `0xdeadbeef`).",
             "Do not execute an unknown file to see what it does: analyse it first."],
    related=["binwalk", "exiftool", "hexdump -C", "od", "readelf", "objdump"],
    practice=["Work out the real type of `holiday.txt` and extract the hidden text from its end.", "Find the byte offset of `flag{` in `hello` and view the bytes around it with `xxd -s`.", "Decode `aGVsbG8gd29ybGQ=` using only commands from this page."],
    cards=["What does `file` read to decide a type?", "What does the PNG signature look like in hex?", "Why does `strings` miss Windows text?", "How do you view the last 40 bytes of a file in hex?"]))

# ------------------------------------------------------------------ curl
TOOLS.append(dict(
    name="curl", version="curl --version", setup=START_ECHO, teardown=STOP_ECHO,
    one_line="Send exactly the HTTP request you describe and show exactly what comes back.",
    when=["Test a web challenge without a browser: change a header, cookie, method or body and see the response.",
          "Download a file, follow a redirect, check a status code in a script.",
          "Reproduce what Burp or the browser sent, as a copy-paste command."],
    anatomy="""curl -s -i -X POST -H 'X-Role: admin' -b 'session=abc' -d 'user=alice' http://127.0.0.1:8099/login
 |    |  |  |       |                 |                 |                |             '--- URL
 |    |  |  |       |                 |                 |                '--- request body
 |    |  |  |       |                 |                 '--- cookie header
 |    |  |  |       |                 '--- add or replace a header
 |    |  |  |       '--- method (curl picks POST for -d by itself)
 |    |  |  '--- -i = show response headers too
 |    |  '--- -s = silent: no progress bar
 '--- the program""",
    flags=[("-s / -S", "Silent / show errors even when silent", "Scripts and clean output"),
           ("-i / -I", "Include response headers / HEAD request only", "See status line, cookies, redirects"),
           ("-v", "Verbose: show the request and response headers", "See exactly what is sent"),
           ("-X METHOD", "Set the method (GET, POST, PUT, DELETE)", "Test method handling"),
           ("-H 'Name: value'", "Add or replace a header", "User-Agent, Referer, Authorization, X-Forwarded-For"),
           ("-A / -e", "User-Agent / Referer shortcuts", "Natas-style Referer checks"),
           ("-b 'k=v' / -c file", "Send cookies / save cookies", "Session and cookie tampering"),
           ("-d / --data-urlencode", "Request body (form data) / URL-encode a value", "Forms and logins"),
           ("--json '{...}'", "Send JSON with the right headers (recent curl)", "APIs"),
           ("-u user:pass", "HTTP Basic authentication", "Basic-auth pages (note: it is only base64)"),
           ("-L", "Follow redirects", "Reach the final page"),
           ("-o FILE / -O", "Save the body to a file / use the remote name", "Download"),
           ("-w '%{http_code}'", "Print a field after the transfer", "Status codes in loops"),
           ("-k", "Ignore TLS certificate errors", "Lab self-signed certificates only"),
           ("--path-as-is", "Do not squash `/../` in the URL", "Path traversal tests"),
           ("--max-time N", "Give up after N seconds", "Scripts")],
    recipes=[
     dict(title="A plain GET", cmd="curl -s 'http://127.0.0.1:8099/hello?x=1'",
          why="This lab server echoes back what it received, so you can see the request as the server saw it.",
          read="The first line is method and path; the rest are headers curl sent by default (`User-Agent`, `Accept`)."),
     dict(title="See the response headers", cmd="curl -si http://127.0.0.1:8099/ | head -8",
          why="`-i` includes the status line and headers. `-s` hides the progress meter.",
          read="Status `200 OK`, a `Content-Type`, and the custom `X-Demo` header. Always read headers in web challenges: cookies and hints live there."),
     dict(title="Change headers and send a cookie", cmd="curl -s -H 'X-Role: admin' -A 'MyAgent/1.0' -e 'http://natas5.example' -b 'loggedin=1' http://127.0.0.1:8099/",
          why="Headers and cookies are client-controlled; a server must never trust them for access control.",
          read="The echo shows each of your values arriving: User-Agent, Referer, Cookie and X-Role."),
     dict(title="POST a form and JSON", cmd="curl -s -d 'user=alice&pass=1' http://127.0.0.1:8099/login; echo; echo ----; curl -s -H 'Content-Type: application/json' -d '{\"a\":1}' http://127.0.0.1:8099/api",
          why="`-d` switches to POST and sets a form content type; for JSON you set the header yourself.",
          read="The body appears after a blank line, with different `Content-Type` values for the two requests."),
     dict(title="Basic auth is just base64", cmd="curl -s -u alice:secret http://127.0.0.1:8099/ | grep Authorization; echo 'YWxpY2U6c2VjcmV0' | base64 -d; echo",
          why="`-u` sends `Authorization: Basic <base64(user:pass)>`. Anyone who sees the request can decode it.",
          read="The header carries the encoded credentials and `base64 -d` recovers them. This is why Basic auth needs HTTPS."),
     dict(title="Redirects", cmd="curl -si http://127.0.0.1:8099/old | head -3; echo ---; curl -sL -o /dev/null -w 'final=%{url_effective} code=%{http_code}\\n' http://127.0.0.1:8099/old",
          why="Without `-L` you see the 301 and its `Location` header; with `-L` curl follows to the final page. `-w` prints a summary.",
          read="Seeing the redirect response itself matters: sometimes the useful content is in the redirect, not the destination (Natas 22)."),
     dict(title="Status code only, for scripting", cmd="for p in / /admin /missing; do curl -s -o /dev/null -w \"$p %{http_code}\\n\" http://127.0.0.1:8099$p; done",
          why="`-o /dev/null` discards the body; `-w` prints the status. Loop over paths to build a tiny scanner.",
          read="200 for the home page, 403 (forbidden: it exists but you may not read it) for `/admin` and 404 (not found) for `/missing`. The difference between 403 and 404 tells you what exists. A real scanner (ffuf, gobuster) does this faster."),
     dict(title="Show the raw request curl sends", cmd="curl -sv http://127.0.0.1:8099/ 2>&1 >/dev/null | grep -E '^(>|<)'",
          why="`-v` prints lines starting with `>` (request) and `<` (response). Redirecting stdout hides the body.",
          read="This is the exact text on the wire. If a challenge says the server checks a header, this is where you confirm it was sent.")],
    gotchas=["Quote URLs that contain `&` or `?`: the shell treats `&` as 'run in background'.",
             "`-d` implies POST and `application/x-www-form-urlencoded`; use `-G` to put data in the URL instead.",
             "Use `--data-urlencode` for values with spaces or symbols, or they are sent raw.",
             "curl may normalise `/../` in the URL; add `--path-as-is` to send it unchanged.",
             "`-k` disables certificate checks: fine for your own lab, never for real credentials."],
    related=["wget", "httpie", "Burp Repeater", "ffuf", "nc (raw HTTP)", "python requests"],
    practice=["Send the request that makes the lab echo header `X-Forwarded-For: 127.0.0.1`.", "Write a loop that prints the status for 10 paths from a list in a file.", "Reproduce a browser request from DevTools: right-click, Copy as cURL."],
    cards=["What does `curl -i` show?", "How do you send a cookie?", "Why can you decode a Basic auth header?", "How do you see a redirect without following it?", "What does `-w '%{http_code}'` do?"]))

# ------------------------------------------------------------------ nc
TOOLS.append(dict(
    name="nc", version="dpkg -l netcat-openbsd 2>/dev/null | tail -1 | awk '{print $2, $3}'", setup=START_ECHO, teardown=STOP_ECHO,
    one_line="Open a plain TCP (or UDP) connection and pipe text or files through it: the Swiss army knife for talking to services.",
    when=["Connect to a CTF service and read its prompt (`nc host port`).", "Check whether a port is open; grab a banner; send a hand-written HTTP request.",
          "Move a file between two machines in a lab."],
    anatomy="""nc  -zv  -w 2  127.0.0.1  8099
 |   |    |     |         '--- port (or a range 8000-8100)
 |   |    |     '--- host
 |   |    '--- -w = give up after 2 seconds
 |   '--- -z = just check the port is open (send no data), -v = say so
 '--- the program (this guide uses the OpenBSD netcat that Ubuntu installs)""",
    flags=[("-v", "Verbose: report connection results", "See `succeeded`/`refused`"),
           ("-z", "Scan mode: connect and close", "Quick port check"),
           ("-w N", "Timeout in seconds", "Do not hang"),
           ("-l", "Listen for an incoming connection (OpenBSD: `nc -l HOST PORT`)", "Receive a file, catch a connection in a lab"),
           ("-N", "Shut down the network socket on end of input (OpenBSD)", "Make a file transfer finish"),
           ("-u", "UDP instead of TCP", "DNS-like services, games"),
           ("-n", "No DNS lookups", "Faster, avoids leaking names"),
           ("-k", "Keep listening after one connection", "Serve repeatedly")],
    recipes=[
     dict(title="Check whether a port is open", cmd="nc -zv -w2 127.0.0.1 8099; nc -zv -w2 127.0.0.1 9",
          why="`-z` connects without sending data. The first port has the lab server; the second has nothing.",
          read="One `succeeded` and one `refused`. Same idea as an Nmap TCP connect scan for a single port."),
     dict(title="Hand-write an HTTP request", cmd="printf 'GET /raw HTTP/1.0\\r\\nX-A: 1\\r\\n\\r\\n' | nc -w2 127.0.0.1 8099 | head -8",
          why="HTTP is plain text over TCP. `\\r\\n` line endings and a blank line end the request.",
          read="The server replies with a status line, headers and the echoed body: you spoke HTTP with no browser."),
     dict(title="Send a message to a listener", cmd="(nc -l 127.0.0.1 9099 > got.txt &) ; sleep 0.5; echo 'hello from the client' | nc -N 127.0.0.1 9099; sleep 0.5; cat got.txt",
          why="One side listens (`-l`) and writes what it receives to a file; the other connects and sends a line.",
          read="The file contains the message. Two terminals, one connection: the basis of every `nc host port` challenge."),
     dict(title="Transfer a file and verify it", cmd="(nc -l 127.0.0.1 9100 > recv.bin &) ; sleep 0.5; nc -N 127.0.0.1 9100 < hello; sleep 0.5; cmp hello recv.bin && echo identical; sha256sum hello recv.bin",
          why="Redirects (`<`, `>`) feed a file into and out of the socket. Compare hashes to prove nothing changed.",
          read="`identical` and two matching hashes. Always verify transfers in forensics work.")],
    gotchas=["There are several netcats: OpenBSD (`nc -l host port`), traditional (`nc -l -p port`, has `-e`), and `ncat` from Nmap. Check `nc -h`.",
             "A connection that hangs often means you did not send the newline the service waits for.",
             "Without `-N`/`-q`, a transfer may never exit; add a timeout (`-w`).",
             "Only connect to hosts you are allowed to test."],
    related=["ncat", "socat", "telnet", "curl", "nmap", "pwntools remote()"],
    practice=["Connect to the lab server and send a PUT with a body using only `nc`.", "Send `hello` over UDP between two terminals (`-u`).", "Check which of ports 8095-8100 are open with `nc -zv`."],
    cards=["What does `nc -zv host port` do?", "Why do different netcat versions matter?", "How do you listen and save to a file?", "How do you hand-write an HTTP request?"]))

# ------------------------------------------------------------------ openssl
TOOLS.append(dict(
    name="openssl", version="openssl version",
    one_line="A crypto toolbox: hashes, encoding, symmetric encryption, certificates and keys, from one command.",
    when=["Hash a string or file; compare with a checksum.", "Encode/decode base64; try AES with a known key.", "Read a certificate or CSR (picoCTF 'ReadMyCert').", "Check RSA keys in a challenge."],
    anatomy="""openssl  dgst  -sha256  file
   |       |      |        '--- input (stdin if omitted)
   |       |      '--- algorithm option
   |       '--- sub-command (dgst, enc, x509, req, rsa, base64, rand ...)
   '--- the program""",
    flags=[("dgst -sha256 / -md5", "Hash input", "Checksums, flag verification"),
           ("base64 [-d]", "Base64 encode / decode", "Quick encoding"),
           ("enc -aes-256-cbc -pbkdf2 -k PASS", "Encrypt with a password (adds a random salt)", "Lab encryption"),
           ("enc -aes-128-ecb -K HEX -nosalt", "Raw AES with a hex key and no salt", "Study modes such as ECB"),
           ("-d", "Decrypt (with `enc`)", "Reverse the above"),
           ("x509 -in cert -noout -subject -dates", "Show certificate fields", "Read a certificate"),
           ("req -x509 -newkey rsa:2048 -nodes", "Make a self-signed certificate", "Lab TLS"),
           ("rsa -in key -text -noout", "Show RSA key parameters", "RSA challenges (n, e)"),
           ("rand -hex N", "N random bytes as hex", "Keys and test data"),
           ("s_client -connect host:443", "Talk TLS to a server", "Check a certificate chain")],
    recipes=[
     dict(title="Hash a string (and avoid the newline trap)", cmd="echo -n hello | openssl dgst -sha256; echo hello | openssl dgst -sha256",
          why="`echo` adds a newline unless you use `-n`. A different input gives a completely different hash.",
          read="Two different hashes for what looks like the same word. This is a common source of 'wrong hash' errors in CTFs."),
     dict(title="Base64 both ways", cmd="printf 'hello world' | openssl base64; echo ---; cat data.b64 | openssl base64 -d; echo",
          why="Base64 is an encoding (anyone can reverse it), not encryption.",
          read="Encoding the text gives a string ending in `=`; decoding `data.b64` returns `hello world`."),
     dict(title="Encrypt with a password and look at the file", cmd="printf 'secret message' | openssl enc -aes-256-cbc -pbkdf2 -k letmein -out enc.bin; head -c 16 enc.bin | xxd; openssl enc -d -aes-256-cbc -pbkdf2 -k letmein -in enc.bin; echo",
          why="With a password, OpenSSL writes the header `Salted__` and 8 salt bytes, then the ciphertext.",
          read="The first bytes spell `Salted__`; decryption with the same password returns the message. A random salt means two runs give different files."),
     dict(title="ECB mode leaks patterns", cmd="printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | openssl enc -aes-128-ecb -K 000102030405060708090a0b0c0d0e0f -nosalt | xxd -c 16",
          why="ECB encrypts each 16-byte block independently, so equal plaintext blocks give equal ciphertext blocks.",
          read="The first two ciphertext lines are identical because the plaintext had two identical blocks (the third line is padding). This is exactly the weakness behind Natas 28 and the CyberSci block-swapping challenge."),
     dict(title="Read a certificate", cmd="openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -subj '/CN=demo.local/O=Lab' -days 1 2>/dev/null; openssl x509 -in c.pem -noout -subject -issuer",
          why="First we create a throw-away self-signed certificate, then read its fields with `x509 -noout`.",
          read="Subject and issuer are the same because it is self-signed. Add `-dates` or `-text` to see validity and the key.")],
    gotchas=["`echo` without `-n` hashes a trailing newline.", "`-pbkdf2` and `-md sha256` differ across OpenSSL versions: decrypting old files may need the original options.",
             "`openssl enc` is for study: never design real encryption with raw `enc`.", "CSR vs certificate vs key are different PEM types: check the header line (`-----BEGIN ...`)."],
    related=["sha256sum / md5sum", "base64", "gpg", "hashcat", "RsaCtfTool", "python pycryptodome"],
    practice=["Encrypt a 48-byte message of repeating blocks with ECB and with CBC and compare the dumps.", "Hash the contents of `hello.c` and verify with `sha256sum`.", "Create a certificate with a different CN and read it back."],
    cards=["Why do `echo hello` and `echo -n hello` hash differently?", "What does the `Salted__` header mean?", "Why is ECB insecure?", "How do you read a certificate's subject?"]))


from atlas_tools2 import TOOLS2  # noqa: E402
TOOLS.extend(TOOLS2)
