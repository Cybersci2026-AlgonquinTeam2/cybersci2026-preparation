# Bandit command encyclopedia

Every command used in Bandit, explained the same way: **what it is → anatomy → popular flags → examples → real use cases → alternatives → gotchas**. Use it as the reference while you do the levels, and as the seed for your own cheat sheet.

How to read an entry:

```text
command  [OPTIONS]  [ARGUMENTS]
   │          │            └── what it works on (files, hosts, patterns)
   │          └── flags that change behaviour (short -x, long --word)
   └── the program name; found via $PATH (`which cmd` shows where)
```

> Tip: every command has `man cmd` (full manual, `q` to quit, `/word` to search) and `cmd --help` (short summary).

**Contents:** [Shell basics](#1-shell-basics-streams-pipes-quoting-globbing) · [Navigating](#2-navigating-and-listing) · [Reading and identifying files](#3-reading-and-identifying-files) · [Searching](#4-searching-find-and-grep) · [Text tools](#5-text-tools) · [Decoding and compression](#6-decoding-and-compression) · [Files and permissions](#7-files-permissions-and-temp-space) · [Networking](#8-networking-ssh-nc-openssl-nmap) · [Compare, hash, cron](#9-compare-hash-and-schedule) · [Git](#10-git) · [Editors and pagers](#11-pagers-and-editors-more-less-vim)

---

## 1. Shell basics: streams, pipes, quoting, globbing

The shell (bash) reads a line, **expands** it (variables, globs, quotes, `$(...)`), then runs programs. Most Bandit confusion is a misunderstanding of *what the shell did before the program ran*.

### 1.1 The three streams

| Stream | Number | Default | Redirect with |
|---|---|---|---|
| stdin | 0 | keyboard | `< file` |
| stdout | 1 | terminal | `> file` (overwrite), `>> file` (append) |
| stderr | 2 | terminal | `2> file`, `2>/dev/null`, `2>&1` |

```text
        ┌────────────┐
 stdin ─▶  program   ├─▶ stdout (1)
 (0)    │            ├─▶ stderr (2)
        └────────────┘
```

| Syntax | Meaning | Example |
|---|---|---|
| `cmd > f` | stdout to file (truncates) | `ls > list.txt` |
| `cmd >> f` | append | `echo hi >> log` |
| `cmd < f` | feed file as stdin | `tr a-z A-Z < in.txt` |
| `cmd 2>/dev/null` | discard errors | `find / -name x 2>/dev/null` |
| `cmd > f 2>&1` / `&> f` | both streams to file | |
| `a \| b` | stdout of a becomes stdin of b | `sort f \| uniq -u` |

`/dev/null` is a special file that accepts and discards all writes.

### 1.2 Combining commands

| Operator | Meaning |
|---|---|
| `a ; b` | run a, then b regardless |
| `a && b` | run b only if a succeeded (`$?` = 0) |
| `a \|\| b` | run b only if a failed |
| `a &` | run a in the background (`jobs`, `fg`) |
| `$(cmd)` | command substitution: replace with cmd's stdout |
| `$?` | exit status of the last command |

### 1.3 Quoting (why `cat spaces in this filename` fails)

| Form | Effect | Example |
|---|---|---|
| `\x` | escape one character | `cat spaces\ in\ name` |
| `'...'` | literal; nothing expands | `echo '$HOME'` → `$HOME` |
| `"..."` | group words; `$var` and `$(...)` still expand | `cat "spaces in name"` |
| none | split on whitespace, glob expanded | `cat *` |

### 1.4 Globbing and brace expansion

| Pattern | Expands to |
|---|---|
| `*` | any characters (not leading dot) |
| `?` | exactly one character |
| `[abc]` / `[0-9]` | one of those |
| `{a,b}` | `a` and `b` |
| `{0000..9999}` | 0000, 0001, … 9999 (zero padded) |

The **program** never sees the `*`: the shell replaces `./-file*` with `./-file00 ./-file01 …` first.

### 1.5 The leading-dash trap and `--`

Programs treat arguments starting with `-` as options. Fixes:
`./-file` (a path), or `--` which means "end of options": `cat -- -file`.

### 1.6 Useful variables

| Variable | Meaning |
|---|---|
| `$HOME`, `~` | home folder |
| `$USER`, `$(whoami)` | current user |
| `$PATH` | where commands are searched |
| `$0` | name of the current shell/script |
| `$$` | PID of the current shell |

---

## 2. Navigating and listing

### `pwd`, `cd`, `whoami`, `id`

| Command | Purpose | Notes |
|---|---|---|
| `pwd` | print working directory | "where am I?" |
| `cd DIR` | change directory | `cd` alone = home; `cd -` = previous; `cd ..` = parent |
| `whoami` | current username | |
| `id` | uid, gid, groups | shows which groups you have (needed for group permissions) |

### `ls`: list directory contents

```text
ls  -la  /path
│   │    └── directory (default: .)
│   └── flags (combined short flags)
└── command
```

| Flag | Meaning |
|---|---|
| `-l` | long listing: permissions, owner, group, size, mtime |
| `-a` | include hidden (dot) files |
| `-A` | like `-a` but without `.` and `..` |
| `-h` | human sizes (K, M) with `-l` |
| `-t` / `-r` | sort by time / reverse |
| `-S` | sort by size |
| `-R` | recurse into subfolders |
| `-d` | list the directory itself, not its contents |
| `-1` | one per line |
| `-F` | append `/` to dirs, `*` to executables |

Reading `ls -l`:

```text
-rwsr-x---  1  bandit20  bandit19   7296  May  7 20:14  bandit20-do
│└┬┘└┬┘└┬┘  │     │         │         │       │            └ name
│ │  │  │   │     │         │         │       └ modification time
│ │  │  │   │     │         │         └ size in bytes
│ │  │  │   │     │         └ group
│ │  │  │   │     └ owner
│ │  │  │   └ hard link count
│ │  │  └ other: r-x? here "---"
│ │  └ group: r-x
│ └ owner: rws  (s = setuid + execute)
└ type: - file, d directory, l symlink
```

**Use cases:** first command on every box: `ls -la`. Spot hidden files, odd owners, setuid bits.
**Alternatives:** `tree` (tree view), `find .`, `stat file` (full metadata).
**Gotcha:** `ls` without `-a` hides dotfiles; "hidden" is only a display convention.

---

## 3. Reading and identifying files

### `cat`: concatenate and print

| Flag | Meaning |
|---|---|
| `-n` | number all lines |
| `-A` | show non-printing characters (`^I` tab, `$` line end): great for odd whitespace |
| `-s` | squeeze repeated blank lines |

```bash
cat readme            # one file
cat a b > both        # concatenate
cat < file            # stdin form (works for a file named "-")
cat -A weird.txt      # reveal tabs and trailing spaces
```

**Alternatives:** `less` (paged), `head`/`tail`, `more`, `xxd` (hex), `strings`.
**Gotcha:** `cat` on a binary can garble the terminal; run `reset` to fix it. Use `file` first.

### `file`: identify type by content (magic bytes)

| Flag | Meaning |
|---|---|
| `-b` | brief (no filename) |
| `-i` | MIME type |
| `-z` | look inside compressed files |
| `-L` | follow symlinks |

```bash
file ./-file*          # many files at once
file -b data           # "gzip compressed data, was "data2.bin", ..."
```

Typical outputs: `ASCII text`, `data` (unknown binary), `gzip compressed data`, `bzip2 compressed data`, `POSIX tar archive`, `ELF 64-bit LSB executable`, `PNG image data`.

**Use cases:** always the first step on an unknown download or extracted layer. A wrong extension can lie; the bytes can't.

### `head`, `tail`, `wc`

| Command | Purpose | Flags |
|---|---|---|
| `head file` | first 10 lines | `-n 5`, `-c 100` (bytes) |
| `tail file` | last 10 lines | `-n 5`, `-f` follow as it grows |
| `wc file` | line/word/byte counts | `-l`, `-w`, `-c` |

### `strings`: printable text from binary

| Flag | Meaning |
|---|---|
| `-n N` | minimum length (default 4) |
| `-a` | scan the whole file |
| `-t x` | print file offset in hex (also `d`, `o`) |
| `-e l` | 16-bit little-endian text (Windows/UTF-16: use `-e l`) |

```bash
strings data.txt | grep '=='      # level 9
strings -n 8 binary | less
```

**Use cases:** quick triage of binaries, memory dumps, firmware; hunting flags and passwords.

---

## 4. Searching: find and grep

### `find`: search the file tree by properties

```text
find  START  TESTS...  ACTION
      │      │         └── default -print; or -exec, -delete
      │      └── ANDed together; ! negates; -o is OR
      └── where to begin (. , /, /etc ...)
```

| Test | Meaning |
|---|---|
| `-name 'pat'` / `-iname` | file name glob (case-insensitive) |
| `-type f` / `d` / `l` | file / directory / symlink |
| `-size 33c` | exactly 33 bytes (`c` bytes, `k` KiB, `M` MiB) |
| `-size +1M` / `-size -100k` | larger than / smaller than |
| `-user U` / `-group G` | owner / group |
| `-perm 4000` / `-perm -4000` / `-perm /u+s` | exact / has at least / has any |
| `-executable` `-readable` `-writable` | permission for *you* |
| `-mtime -1` / `-mmin -30` | modified in last day / 30 minutes |
| `-newer FILE` | newer than FILE |
| `-maxdepth N` | limit recursion |
| `-empty` | zero length |

| Action | Meaning |
|---|---|
| `-print` (default) | print each match |
| `-exec CMD {} \;` | run CMD per match (`{}` = path) |
| `-exec CMD {} +` | run CMD once with many paths |
| `-delete` | remove matches (dangerous) |
| `-print0` + `xargs -0` | safe with spaces in names |

```bash
find . -type f -size 1033c ! -executable        # level 5
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null   # level 6
find / -perm -4000 -type f 2>/dev/null          # all setuid files (privesc recon)
find / -writable -type d 2>/dev/null            # where can I write?
find . -name '*.conf' -exec grep -l password {} +
```

**Why `2>/dev/null`:** searching `/` hits directories you can't enter; each prints "Permission denied" on **stderr**. Redirecting fd 2 hides them without hiding results (stdout).
**Alternatives:** `locate` (database, fast but stale), `fd` (modern), `ls -R | grep`.
**Gotchas:** `-size 33` means 33 *blocks* of 512 bytes, not bytes; always add `c`. Quote globs in `-name` so the shell doesn't expand them first.

### `grep`: filter lines by pattern

| Flag | Meaning |
|---|---|
| `-i` | ignore case |
| `-v` | invert (lines that do NOT match) |
| `-n` | show line numbers |
| `-c` | count matching lines |
| `-r` / `-R` | recurse through directories |
| `-l` | list only filenames with matches |
| `-o` | print only the matching part |
| `-E` | extended regex (`+`, `?`, `\|`, `()`) |
| `-F` | fixed string, no regex |
| `-w` | whole word |
| `-A N` `-B N` `-C N` | context lines after / before / around |
| `-a` | treat binary as text |
| `-P` | Perl regex (lookaheads, `\d`) |

```bash
grep millionth data.txt                 # level 7
grep -rn "password" /etc 2>/dev/null    # search a tree
grep -v '^#' config                     # skip comments
grep -oE '[A-Za-z0-9]{32}' file         # extract 32-char tokens
grep -c ERROR app.log                   # count
```

**Use cases:** log triage, finding credentials, filtering output of other commands.
**Alternatives:** `awk '/pat/'`, `sed -n '/pat/p'`, `rg` (ripgrep, much faster; installed on your own machines).

---

## 5. Text tools

### `sort` and `uniq`

| `sort` flag | Meaning |
|---|---|
| `-n` | numeric sort |
| `-r` | reverse |
| `-u` | unique (drop duplicates) |
| `-k N` | sort by field N |
| `-t C` | field delimiter C |
| `-f` | ignore case |
| `-h` | human numbers (1K, 2M) |

| `uniq` flag | Meaning |
|---|---|
| `-u` | print ONLY lines that appear once |
| `-d` | print only duplicated lines (one each) |
| `-c` | prefix count |
| `-i` | ignore case |

```bash
sort data.txt | uniq -u                 # level 8: the unique line
sort data.txt | uniq -c | sort -rn      # frequency table, most common first
```

**Key fact:** `uniq` compares only *adjacent* lines. Sorted input is what makes "all duplicates adjacent". `sort -u` removes duplicates but keeps one copy, which is different from `uniq -u`.

### `cut`, `awk`, `tr`, `sed`

| Tool | Purpose | Example |
|---|---|---|
| `cut -d' ' -f1` | pick delimited fields | `md5sum \| cut -d ' ' -f 1` |
| `cut -c1-8` | pick character columns | |
| `awk '{print $2}'` | field 2 of each line (whitespace split) | `grep millionth f \| awk '{print $2}'` |
| `tr 'a-z' 'A-Z'` | translate characters | ROT13 below |
| `tr -d '\r'` | delete characters | strip Windows line endings |
| `tr -s ' '` | squeeze repeats | |
| `sed 's/a/b/g'` | substitute | |

**ROT13 with tr:**

```text
input range : A B C ... M | N O P ... Z | a ... m | n ... z
output range: N O P ... Z | A B C ... M | n ... z | a ... m
tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

---

## 6. Decoding and compression

### `base64`

| Flag | Meaning |
|---|---|
| `-d` / `--decode` | decode |
| `-w 0` | do not wrap encoded lines |
| `-i` | ignore garbage characters when decoding |

```bash
echo 'aGVsbG8=' | base64 -d      # hello
echo -n hello | base64          # aGVsbG8=
```

Recognise Base64: alphabet `A-Za-z0-9+/`, length multiple of 4, often ends in `=` or `==`. **It is encoding, not encryption.**

### `xxd`: hex dump and reverse

| Flag | Meaning |
|---|---|
| (none) | hex + ASCII dump |
| `-r` | **reverse** a hex dump back to bytes |
| `-p` | plain hex (no offsets) |
| `-l N` | only N bytes |
| `-s N` | start at offset N |
| `-c N` | N bytes per line |

```bash
xxd file | head                 # inspect magic numbers (1f8b = gzip, 425a = bzip2)
xxd -r data.txt > data.bin      # level 12
xxd -r -p hex.txt > out.bin     # plain hex without offsets
```

Magic numbers to remember: `1f 8b` gzip · `42 5a 68` ("BZh") bzip2 · `50 4b 03 04` zip · `7f 45 4c 46` ELF · `89 50 4e 47` PNG.

### Compression and archives

| Tool | Decompress | Create | Key point |
|---|---|---|---|
| `gzip` | `gzip -d f.gz` / `gunzip f.gz` | `gzip f` | needs `.gz` suffix; `-k` keep original; `-c` to stdout |
| `bzip2` | `bzip2 -d f.bz2` | `bzip2 f` | needs `.bz2` suffix |
| `xz` | `xz -d f.xz` | `xz f` | |
| `tar` | `tar xf a.tar` | `tar cf a.tar dir` | archive only; add `z`/`j`/`J` to (de)compress |
| `zip` | `unzip a.zip` | `zip a.zip files` | |

`tar` flags: `x` extract · `c` create · `t` list · `f FILE` archive name · `v` verbose · `z` gzip · `j` bzip2 · `C DIR` change dir first. GNU tar auto-detects compression on extraction (`tar xf`).

Level 12 loop (always `file` first):

```text
file X → "gzip"  → mv X X.gz  → gzip -d X.gz
file X → "bzip2" → mv X X.bz2 → bzip2 -d X.bz2
file X → "POSIX tar" → tar xf X
file X → "ASCII text" → cat X
```

---

## 7. Files, permissions and temp space

### `mkdir`, `mktemp`, `cp`, `mv`, `rm`, `touch`

| Command | Purpose | Flags |
|---|---|---|
| `mkdir -p a/b` | create dirs (and parents) | `-p`, `-m 700` |
| `mktemp -d` | make a unique private temp dir | `-d` dir, `-p DIR` base, template `XXXXXX` |
| `cp SRC DST` | copy | `-r` recursive, `-a` preserve |
| `mv SRC DST` | move/rename | |
| `rm f` | remove | `-r`, `-f` (careful) |
| `touch f` | create empty / update mtime | |

On Bandit your home is read-only for most work; **`/tmp` is writable**. Use `mktemp -d` so your files don't collide with other players.

### Permissions: `chmod`

```text
  u = user (owner)   g = group   o = others   a = all
  r = read (4)       w = write (2)   x = execute (1)
```

| Form | Example | Result |
|---|---|---|
| numeric | `chmod 600 key` | `-rw-------` owner read/write only |
| numeric | `chmod 755 script` | `-rwxr-xr-x` |
| numeric | `chmod 777 dir` | everyone everything (use sparingly) |
| symbolic | `chmod +x script` | add execute for all |
| symbolic | `chmod go-rwx key` | remove group/other perms |

Special bits (leading digit): **4** setuid, **2** setgid, **1** sticky. `chmod 4755 f` sets setuid. Directory needs `x` to enter, `r` to list.

Why SSH insists on `600` for private keys: if others can read your key, the key is compromised in principle; `ssh` refuses with "UNPROTECTED PRIVATE KEY FILE".

---

## 8. Networking: ssh, nc, openssl, nmap

### `ssh`

```text
ssh  -i KEY  -p PORT  user@host  [COMMAND]
     │       │        │          └── run this instead of an interactive shell
     │       │        └── account@machine
     │       └── port (default 22; Bandit uses 2220)
     └── identity file (private key)
```

| Flag | Meaning |
|---|---|
| `-p PORT` | port |
| `-i FILE` | private key |
| `-t` | force a pseudo-terminal (needed for interactive commands) |
| `-v` | verbose (debugging) |
| `-L l:host:r` | local port forward |
| `-D PORT` | SOCKS proxy |
| `-o Opt=val` | any config option, e.g. `-o StrictHostKeyChecking=no` |
| `-N` | no remote command (tunnels only) |

First connection prints a host-key fingerprint prompt; answering `yes` stores it in `~/.ssh/known_hosts`. Auth order: key → password.

**Use cases:** remote administration; running one command (`ssh h cmd`); tunnels (`-L`/`-D`); `scp`/`sftp` ride the same protocol.

### `nc` (netcat)

| Flag | Meaning |
|---|---|
| `host port` | connect (client) |
| `-l` | listen (server) |
| `-p PORT` | local port (older netcat: with `-l`; OpenBSD netcat: `nc -l PORT`) |
| `-v` | verbose |
| `-n` | no DNS lookup |
| `-z` | scan without sending data (`nc -zv host 1-1000`) |
| `-u` | UDP |
| `-w SEC` | timeout |
| `-k` | keep listening for more connections |

```bash
nc localhost 30000                   # level 14: client
nc -l 4444                           # server: print what arrives
echo 'hello' | nc host 9000          # send a line, print reply
nc -zv localhost 31000-31010         # poor man's port scan
```

**Use cases:** testing services by hand, quick file transfer, reverse/bind shell listeners, debugging protocols.
**Gotcha:** different `nc` builds have different flags. If `-p` with `-l` errors, drop `-p`.

### `openssl s_client`

| Flag | Meaning |
|---|---|
| `-connect host:port` | where to connect |
| `-quiet` | suppress certificate output and session info |
| `-ign_eof` | keep the connection open after stdin ends |
| `-servername NAME` | SNI (virtual-host TLS) |
| `-showcerts` | print the certificate chain |
| `-starttls smtp` | upgrade a plain protocol to TLS |
| `-tls1_2` | force a version |

```bash
openssl s_client -quiet -connect localhost:30001
echo "$(cat /etc/bandit_pass/bandit15)" | openssl s_client -quiet -ign_eof -connect localhost:30001
```

**Gotcha:** without `-quiet`, a line starting with `R` or `k` is a *command* to s_client (renegotiate / key update). **Use cases:** inspect certificates, talk to HTTPS/SMTPS by hand.
**Alternatives:** `ncat --ssl`, `socat - OPENSSL:host:port`, `curl -v https://...`.

### `nmap`

| Flag | Meaning |
|---|---|
| `-p 80,443` / `-p 1-1000` / `-p-` | ports / range / all 65535 |
| `-sT` | TCP connect scan (works without root) |
| `-sS` | SYN scan (needs root, stealthier) |
| `-sV` | probe service/version |
| `-sC` | default NSE scripts |
| `-A` | OS, version, scripts, traceroute |
| `-Pn` | skip host discovery (treat as up) |
| `-T0..-T5` | timing: 0 paranoid .. 5 insane |
| `-oN file` / `-oA base` | save results |
| `--open` | only show open ports |
| `-n` | no DNS |
| `--top-ports N` | most common N ports |

```bash
nmap -p 31000-32000 localhost         # level 16
nmap -sV -p 31000-32000 localhost     # + identify services
nmap -sC -sV -oN scan.txt TARGET      # standard first scan
```

Port states: **open** (something answers), **closed** (reachable but nothing listening), **filtered** (firewall drops).
**Alternatives:** `masscan` (huge ranges), `rustscan`, `nc -zv`, a bash `/dev/tcp` loop.

---

## 9. Compare, hash and schedule

### `diff`

| Flag | Meaning |
|---|---|
| (none) | normal diff: `<` first file, `>` second |
| `-u` | unified format (what git uses) |
| `-y` | side-by-side |
| `-q` | only say whether they differ |
| `-r` | compare directories |
| `-i` `-w` | ignore case / whitespace |

`cmp` compares bytes; `comm` compares sorted files; `sdiff` side-by-side.

### `md5sum` and friends

```bash
echo I am user bandit23 | md5sum             # 32 hex chars + "  -"
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
echo -n 'text' | md5sum                      # -n: no trailing newline!
```

**Newline matters:** `echo` adds `\n`, which changes the hash. The Bandit cron script used plain `echo`, so you must too. Siblings: `sha1sum`, `sha256sum`.

### cron

A cron entry: `minute hour day-of-month month day-of-week [user] command`.

```text
* * * * *   user   /path/script.sh        every minute
*/5 * * * * user   cmd                    every 5 minutes
0 3 * * 1   user   cmd                    Mondays 03:00
@reboot     user   cmd                    at boot
```

| Location | Notes |
|---|---|
| `/etc/crontab` | system file; has a `user` column |
| `/etc/cron.d/*` | drop-in files; `user` column |
| `crontab -e` / `-l` | per-user crontab |
| `/etc/cron.hourly` etc. | scripts run by run-parts |

**Use cases:** you read cron to find scripts that run as another user, and you check whether *you* can write to those scripts or to what they execute (privesc).

---

## 10. Git

```text
 working tree ──git add──▶ index (staging) ──git commit──▶ local repo ──git push──▶ remote
```

| Command | Purpose | Popular flags |
|---|---|---|
| `git clone URL [dir]` | copy a remote repo | `-b branch`, `--depth 1` |
| `git status` | state of working tree/index | `-s` |
| `git log` | history | `--oneline`, `--graph`, `--all`, `-p` (patches), `-n 5`, `--stat` |
| `git show REF` | show a commit/tag/file | `REF:path` for a file at that commit |
| `git diff A B` | compare commits/branches | `--stat` |
| `git branch` | list branches | `-a` (all incl. remote), `-r` (remote only) |
| `git checkout BR` | switch branch | `-b new` create |
| `git tag` | list tags | `-a` annotated, `-l` pattern |
| `git add f` | stage | `-f` force (override .gitignore), `-A` all |
| `git commit -m msg` | record | `-a` stage tracked files |
| `git push REMOTE BR` | upload commits | `-u` set upstream |
| `git remote -v` | list remotes | |

Concepts: a **commit** is a snapshot with a parent pointer; a **branch** is a movable pointer to a commit; a **tag** is a fixed pointer; **HEAD** is "where you are". History keeps everything: deleting a secret in the newest commit does not remove it from older commits.

`.gitignore` hides files from `git add`/`git status`; `git check-ignore -v file` tells you which rule matches; `git add -f` overrides it.

---

## 11. Pagers and editors: more, less, vim

### `more` / `less`

| Key | Action |
|---|---|
| space / `f` | next page |
| `b` (less) | previous page |
| `q` | quit |
| `/text` | search forward |
| `v` | open the file in `$EDITOR` (vi/vim) |
| `!cmd` | run a shell command (in `more` and `less`) |

`more` only pauses if the content is taller than the terminal: this is why shrinking the window matters in level 25.

### vim survival kit

| Key / command | Meaning |
|---|---|
| `i` | insert mode; `Esc` returns to normal mode |
| `:w` / `:q` / `:wq` / `:q!` | save / quit / save+quit / quit without saving |
| `:r FILE` | insert file contents at the cursor |
| `:e FILE` | open another file |
| `:!cmd` | run a shell command |
| `:set shell=/bin/bash` | choose the shell used by `:shell` and `:!` |
| `:shell` | drop into that shell |
| `/text`, `n` | search, next |
| `dd`, `u`, `yy`, `p` | delete line, undo, copy line, paste |

**Why this matters in security:** pagers, editors, `man`, `find -exec`, `git`, `awk`, `tar` and many more can spawn a shell, which is how restricted environments are escaped. GTFOBins catalogues them.

---

## Quick decision table: which tool for which problem?

| Situation | Reach for | Why |
|---|---|---|
| Unknown file | `file`, `strings`, `xxd \| head` | identify before acting |
| Need one line out of a huge file | `grep` | pattern match |
| Need the odd one out | `sort \| uniq -u` / `-c` | duplicates logic |
| Need a file by attribute | `find` | size, owner, perms, time |
| Text looks like gibberish | decode: `base64 -d`, `tr`, `xxd -r` | recognise encoding |
| A service on a port | `nc`, `openssl s_client`, `nmap` | talk to it manually |
| Two similar files | `diff` | spot the change |
| Something runs on a schedule | `/etc/cron.d`, `crontab -l` | privesc surface |
| Locked-down shell | pagers, editors, `$0` | spawn a new shell |
