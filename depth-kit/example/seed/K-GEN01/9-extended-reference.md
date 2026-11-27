# Extension D: extended reference

## Extended glossary `{A44}` `{A56}`

| Term | Meaning |
|---|---|
| anchor (regex) | `^` or `$`: ties a pattern to the start or end of a line |
| character class | `[abc]` or `[0-9]`: one character from a set |
| quantifier | `*`, `+`, `?`, `{n}`: how many times the previous item repeats |
| alternation | `a\|b`: either pattern |
| capture group | `( )` that remembers the matched text for a back-reference such as `\1` |
| back-reference | `\1`, `\2`: reuse a captured group in a replacement |
| address (sed) | which lines a command applies to, such as `2,4` or `/re/` |
| pattern (awk) | the test before `{action}` that selects lines |
| action (awk) | the code in `{ }` run on selected lines |
| built-in variable | a variable awk sets for you, such as `NR` and `NF` |
| associative array | a table keyed by text, used to group values |
| stable sort | a sort that keeps the original order of equal keys |
| key (sort) | the part of a line the sort compares |
| process substitution | `<( ... )`: lets a command's output act like a file |
| back-pressure | a slow reader makes a fast writer wait because the pipe buffer is full |
| broken pipe | the writer finds the reader has gone away |
| redirect | `>` or `<`: connects a stream to a file |
| idempotent | running it twice gives the same result as once |
| reproducible | the same input always gives the same output |
| independent method | a second way to compute the same number, used to check the first |

## Cheat sheet 3: the small languages `{P12}`

```
 regex                               awk                                   sed
   ^ $  start/end                      -F,  separator                        s/a/b/    first match
   .    any char                       NR>1  skip header                     s/a/b/g   every match
   [0-9] a digit                       $1..$NF  fields                       -n '2,4p' print lines
   * + ?  repeats                      a[$1]+=$2  group and total            /re/d     delete matching
   (a|b)  alternation                  END {print ...}  after last line      -E 's/(x)(y)/\2\1/'
   grep -E  extended                   printf "%s %.2f\n", k, v              -i.bak    edit with backup
 sort                                 helpers
   -t, -k2,2 -s  stable by field 2      tr 'a-z' 'A-Z'   paste - -   column -t
   -n numbers  -r reverse  -u unique    nl -ba   tac   rev   comm   join
```

## Frequently asked questions

**Why not do everything in a spreadsheet?** Spreadsheets are fine for small one-off data. Pipelines run on files too large to open, repeat unchanged tomorrow, and fit inside scripts and tests.

**Why does the order of ties change?** Equal keys are ordered by the rest of the line unless the sort is stable or the locale is fixed. Use `LC_ALL=C` and `-s` when repeatability matters.

**When should I leave the shell tools?** When fields contain quoted separators, when records span lines, when the data is nested (JSON, XML) or when the logic needs more than a few lines.

**How do I know a number is right?** Compute it a second, independent way, and change the input slightly to see that the answer follows.

## Extended claims register `{A42}` `{A58}`

| Id | Claim | Quote or VERIFY | Status | Note |
|---|---|---|---|---|
| C13 | a loose `grep` count can exceed an exact awk field test on the same log | VERIFY | Run | extension A1 lab matched |
| C14 | `awk` treats a run of spaces as one separator by default | VERIFY | Run | extension A2 lab matched |
| C15 | `sed -n '2,4p'` prints lines 2 to 4 | VERIFY | Run | extension A3 lab matched |
| C16 | `sort -k2,2 -s` and `sort -k2` can order ties differently | VERIFY | Run | extension A4 lab matched |
| C17 | `comm -12` prints the lines two sorted inputs share | VERIFY | Run | extension A5 lab matched |
| C18 | the hour can be taken from the log timestamp with `substr` | VERIFY | Run | case study 1 matched |
| C19 | an empty quantity counts as zero in awk arithmetic | VERIFY | Run | failure case 6 matched |
| C20 | the two grand totals in case study 2 agree | VERIFY | Run | case study 2 matched |
| C21 | `head` ends a pipeline early and the earlier stage may report a broken pipe | VERIFY | Not run | message text not captured |
| C22 | `sed -i` edits in place and `-i.bak` keeps a backup | VERIFY | Not run | stated from knowledge |
| C23 | `set -o pipefail` makes a pipeline fail if any stage fails | VERIFY | Not run | script lab not run |
| C24 | a script header check protects later stages | VERIFY | Not run | script lab not run |

## Sources still to capture (so VERIFY claims can become Read)

The manual pages of `grep`, `awk` (gawk), `sed`, `sort`, `uniq`, `cut`, `tr`, `comm` and `column` for the version used; the POSIX description of `sort -k` and of regular expressions; the bash manual's section on pipelines and `pipefail`. None is captured yet, so every behaviour not run in the labs stays `VERIFY`.

## Export and reuse `{P18}`

Cards: one Anki note per `- [type][difficulty]` line (Front and Back as written; the difficulty becomes a tag). Labs: the `lab` blocks are runnable shell lines; copy them into a script or run them in the sandbox gate. Cheat sheets: the figures are plain text and paste into a note or a printed page.
