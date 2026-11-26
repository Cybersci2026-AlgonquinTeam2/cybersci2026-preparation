# Extension A: the small languages inside the tools

The five parts taught the pipeline. This extension teaches the three small languages hidden in the tools, because most wrong answers come from not knowing them: patterns (regular expressions), the awk language, and the sed editor. It also covers `sort` keys and seven small helpers. Each section is structured the same way: the idea, a picture, a labelled example, a lab, a mistake to avoid `{A53}` `{A56}`.

## Extension A1: regular expressions, the pattern language

**Idea.** A regular expression (regex) describes a set of strings. `grep` shows the lines that contain a match. **Picture** `{V19}` `{fig:tree}`:

```
 regex pieces (arrows: "builds")
   literal characters ──► anchors ^ $ ──► character classes [abc] [0-9] . ──► repeats * + ? {n}
                                   │                                              │
                                   └────────► groups ( ) and alternation a|b ◄────┘
```

| Piece | Means | Example | Matches | Does not match |
|---|---|---|---|---|
| `^` | start of line | `^2026` | `2026-11-01,...` | `x2026` |
| `$` | end of line | `5$` | a line ending in 5 | `5 ` (trailing space) |
| `.` | any one character | `a.c` | `abc`, `a-c` | `ac` |
| `[abc]` | one of these | `[nsew]orth` | `north` | `forth` |
| `[0-9]` | one digit | `[0-9][0-9]` | `42` | `4` |
| `*` | zero or more of the previous | `ab*` | `a`, `abbb` | `b` |
| `+` | one or more (extended regex, `grep -E`) | `ab+` | `ab` | `a` |
| `?` | zero or one | `colou?r` | `color`, `colour` | `colouur` |
| `\|` | either (extended: `a\|b` in basic, `a|b` with `-E`) | `404\|500` | either code | `405` |
| `( )` | a group | `(ab)+` | `abab` | `aabb` |

**Labelled example** `{A10}`: lines whose status is exactly 500 in the web log. The status code is the ninth whitespace field, so a regex on the whole line risks matching the byte-size field. An anchored regex or a field test avoids it.

```lab
$ grep -c ' 500 ' access.log
24
$ awk '$9==500' access.log | wc -l
24
```

*Compare:* the second is exact by construction (a numeric test on field 9); the first depends on spaces around the number. When the two numbers differ, the regex is matching somewhere it should not. In this data the loose count is one higher than the exact one (**observed**): one line has the digits 500 in another field. *Evidence label* `{A42}`: **observed** in the lab data; the exact counts are in the filled blocks above.

**Lab: loose versus anchored** `{P7}`:

```lab
$ grep -c 500 access.log
25
$ grep -c ' 500 ' access.log
24
$ awk '$9==500' access.log | wc -l
24
```

- Hint 1: the first pattern has no spaces around the number.
- Hint 2: digits can appear in the size field and in the path.
- Hint 3: compare the three numbers; the largest is the loose one.
- Hint 4: loose regexes over-count; use a field test or anchor with delimiters.

**Mistake to avoid** `{A14}` (error class *logical*): trusting a regex count without a second method.

**Extended regex.** `grep -E` (or `egrep`) turns on `+`, `?`, `|` and `( )` without backslashes. Use it for alternation:

```lab
$ grep -E -c ' (401|403) ' access.log
129
$ grep -E -o '"(GET|POST) [^ ]+' access.log | head -3
"GET /products/42
"GET /static/app.js
"GET /
```

`-o` prints only the matching part; `[^ ]+` means "one or more characters that are not a space".

## Extension A2: the awk language, one piece at a time

**Idea.** An awk program is a list of `pattern {action}` pairs run on every line. **Picture** `{V20}` `{fig:flow}`:

```
 awk program flow
   BEGIN {...} ──once, before any input──► for each line: [pattern true?]──yes──► {action} ──► next line
                                                              │no                                   │
                                                              └─────────────────────────────────────┘
   END {...}   ──once, after the last line──► done
```

| Element | Meaning | Example |
|---|---|---|
| `$0`, `$1`...`$NF` | the whole line, field 1 to the last field | `print $1, $NF` |
| `NR`, `NF` | line number, number of fields | `NR>1`, `NF!=5` |
| `FS` and `-F` | input field separator | `-F,` |
| `OFS` | output field separator | `BEGIN {OFS=","}` |
| pattern | a test that selects lines | `$4>=10`, `/west/`, `$2=="west"` |
| `BEGIN`, `END` | run before the first and after the last line | `END {print s}` |
| variables | start empty (0 or empty string) | `s+=$4` |
| arrays | tables keyed by text | `c[$2]++` |
| functions | `length`, `substr`, `tolower`, `index` | `tolower($2)` |
| `printf` | formatted output | `printf "%s %.2f\n", k, v` |

**Worked examples with the languages' pieces** `{A9}` `{A10}`:

```lab
$ awk -F, 'NR>1 {n++; s+=$4} END {print n, s, s/n}' sales.csv
60 416 6.93333
$ awk -F, 'NR>1 {c[tolower($2)]++} END {for (k in c) print k, c[k]}' sales.csv | sort
east 9
north 18
south 15
west 18
$ awk -F, 'NR>1 && $3=="date" {print $1, $4*$5}' sales.csv | head -3
2026-11-01 6.5
2026-11-08 65
2026-11-24 65
$ awk 'NR>1 {print $5}' procs.txt | sort | uniq -c | sort -rn | head -3
      5 sshd
      3 python3
      3 node
```

- Hint 1: you need a total, a count and an average from one pass.
- Hint 2: awk variables start at zero, so `n++` and `s+=$4` work without setup.
- Hint 3: do the arithmetic in the `END` block.
- Hint 4: the first command above: `n++; s+=$4` per line, then `print n, s, s/n`.

*Walk the second line:* `tolower($2)` makes `North` and `north` one key; `c[...]++` adds one to that key's counter; the `for (k in c)` loop prints each key; `sort` orders the keys because awk loops over an array in no guaranteed order.

**Whitespace data.** `procs.txt` is aligned with runs of spaces. `cut -d' '` would split each space and make empty fields; awk's default separator treats a run of spaces as one:

```lab
$ cut -d' ' -f2 procs.txt | head -3 | cat -A
$
$
$
$ awk '{print $2}' procs.txt | head -3
PID
1000
1037
```

**Mistakes to avoid:** (1) `-F` after the program text is ignored (error class *procedural*). (2) Forgetting that awk's `for (k in a)` order is not sorted (*conceptual*). (3) Using `==` on text with trailing spaces (*assumption*).

## Extension A3: sed, the stream editor

**Idea.** `sed` applies editing commands to each line. The core command is `s/old/new/flags`; the core options are `-n` (print only on request) and `-E` (extended regex). **Picture** `{V19}` `{fig:blackbox}`:

```
 sed model
   line in ──► [ address? ] ──► [ command ] ──► line out (or nothing)
              (which lines)     s/x/y/  d  p
```

| Command | Meaning | Example |
|---|---|---|
| `s/a/b/` | replace the first `a` on each line | `s/north/N/` |
| `s/a/b/g` | replace every `a` on each line | `s/,/;/g` |
| `5p`, `-n '2,4p'` | print line 5; print lines 2 to 4 | `sed -n '2,4p'` |
| `/re/d` | delete lines that match | `/^$/d` removes blank lines |
| `-E 's/(a)(b)/\2\1/'` | groups and back-references | swap two parts |

```lab
$ sed -n '2,4p' sales.csv
2026-11-01,west,date,1,6.5
2026-11-02,north,elderberry,5,9.0
2026-11-03,south,cherry,11,4.0
$ sed 's/,/ | /g' sales.csv | head -2
date | region | item | qty | price
2026-11-01 | west | date | 1 | 6.5
$ sed '/^$/d' messy.csv | wc -l
9
$ sed -E 's/^([0-9-]+),([a-z]+),.*/\2 on \1/' sales.csv | head -3
date,region,item,qty,price
west on 2026-11-01
north on 2026-11-02
```

- Hint 1: the replacement is built from pieces of the line, so you need groups.
- Hint 2: wrap the date and the region in parentheses.
- Hint 3: `` is the first group and `` the second in the replacement.
- Hint 4: the last command above, using `-E` for extended groups.

*Walk the last line:* `([0-9-]+)` captures the date, `([a-z]+)` captures the region, `.*` swallows the rest, and `\2 on \1` rewrites the line from the two captures.

**Mistake to avoid** `{A14}`: assuming `sed -i` is safe: it edits the file in place; in the sandbox it is not allowed, and in real use keep a backup (`-i.bak`).

## Extension A4: `sort` keys, in detail

| Option | Meaning | Use |
|---|---|---|
| `-k N` | sort by field N to the end of line | `-k2` |
| `-k N,N` | sort by field N only | `-k2,2` |
| `-t X` | field separator | `-t,` |
| `-n` | numeric | `-n` |
| `-r` | reverse | `-rn` |
| `-u` | keep one of equal keys | `-u` |
| `-s` | stable: keep input order for ties | `-s` |
| `-f` | ignore case | `-f` |
| `-h` | human-readable sizes (`2K`, `1G`) | `-h` |

**Subtle point** `{A4}`: `-k2` means "from field 2 to the end of the line", so the later fields still break ties. `-k2,2` means "field 2 only"; add `-s` for stable ties.

```lab
$ tail -n +2 sales.csv | sort -t, -k2,2 -s | head -4
2026-11-07,east,cherry,4,4.0
2026-11-11,east,elderberry,5,9.0
2026-11-26,east,apple,5,0.5
2026-11-08,east,elderberry,3,9.0
$ tail -n +2 sales.csv | sort -t, -k2 | head -4
2026-11-23,east,apple,11,0.5
2026-11-25,east,apple,2,0.5
2026-11-26,east,apple,5,0.5
2026-11-11,east,banana,10,0.25
$ cut -d, -f2 sales.csv | tail -n +2 | sort -f | uniq -ic
      9 east
     18 north
     15 south
     18 west
```

- Hint 1: ties are lines with the same key.
- Hint 2: `-k2` runs to the end of the line; `-k2,2` stops at field 2.
- Hint 3: add `-s` to keep the original order inside equal keys.
- Hint 4: compare the first two commands above; they differ only in the key and the stability flag.

*Reading the result:* the first keeps the original order inside each region (stable); the second breaks ties on later fields. `uniq -ic` counts ignoring case, which merges `North` and `north` in `messy.csv`.

## Extension A5: seven small helpers

| Tool | Does | One-line example |
|---|---|---|
| `tr` | swap or delete characters | `tr 'a-z' 'A-Z'` |
| `paste` | join lines side by side | `paste - -` pairs consecutive lines |
| `column -t` | align into columns | `column -t -s,` |
| `nl` | number lines | `nl -ba` |
| `tac` | print lines in reverse order | `tac` |
| `rev` | reverse each line's characters | `rev` |
| `comm` | compare two sorted lists | `comm -12 a b` shows common lines |
| `join` | join two sorted files on a key | `join a b` |

```lab
$ printf 'a\nb\nc\nd\n' | paste - -
a	b
c	d
$ head -4 sales.csv | column -t -s,
date        region  item        qty  price
2026-11-01  west    date        1    6.5
2026-11-02  north   elderberry  5    9.0
2026-11-03  south   cherry      11   4.0
$ head -3 sales.csv | nl -ba
     1	date,region,item,qty,price
     2	2026-11-01,west,date,1,6.5
     3	2026-11-02,north,elderberry,5,9.0
$ head -3 sales.csv | tac
2026-11-02,north,elderberry,5,9.0
2026-11-01,west,date,1,6.5
date,region,item,qty,price
$ comm -12 <(printf 'a\nb\nc\n') <(printf 'b\nc\nd\n')
b
c
$ cut -d, -f3 sales.csv | tail -n +2 | tr 'a-z' 'A-Z' | sort -u
APPLE
BANANA
CHERRY
DATE
ELDERBERRY
```

**Which to reach for** `{A16}`: `comm` and `join` need sorted input (same lesson as `uniq`); `column -t` is for reading, not for further processing; `tr` handles single characters, so use `sed` for words.

## Extension A6: the language tools side by side `{V15}`

```
 comparison matrix                  grep        cut         awk            sed           tr
   selects lines by pattern         yes         no          yes (pattern)  yes (address) no
   selects columns                  no          yes         yes            with groups   no
   does arithmetic                  no          no          yes            no            no
   edits text                       no          no          yes (printf)   yes           chars only
   speed on huge files              fast        fast        medium         fast          fast
   learning cost                    low         low         medium         medium        low
   decision rule: pick the weakest tool that does the job; move up (cut ► awk) only when it cannot.
```
