# Part 5 of 5: Reference and close

## 15. Close

### Cheat sheet 1: choosing and building `{P12}`

```
 decision tree                           top patterns
   lines?    ── grep                      count lines matching     grep -c PATTERN file
   columns?  ── cut                       one column               cut -d, -f2 file
   maths?    ── awk                       group and count          ... | sort | uniq -c | sort -rn
   replace?  ── sed                       sum a column             awk -F, '{s+=$4} END {print s}'
                                          top N                    ... | head -N
 pitfalls (symptom ► fix)                 drop a header            tail -n +2
   counts all 1   ► sort first            distinct values          sort -u
   10 before 9    ► sort -n               lines from N on          tail -n +N
   extra matches  ► anchor the pattern    line numbers shown       grep -n PATTERN file
   header counted ► tail -n +2 or NR>1    repeatable order         LC_ALL=C sort
```

### Cheat sheet 2: when the pipeline is wrong `{P12}`

```
 checklist                                   quick tests
   1 print the first 10 lines                 head -10 file
   2 print after stage 1, then stage 2 ...    run the pipeline with a stage removed
   3 count lines in and out                   wc -l before and after a stage
   4 fields per line                          awk -F, '{print NF}' f | sort | uniq -c
   5 hidden characters                        cat -A file
   6 compare with a second method             awk total versus a manual sum
```

### Glossary `{A44}` (terms link back to part 1)

| Term | Meaning |
|---|---|
| pipe | a one-way connection from one program's output to another's input |
| stdin, stdout, stderr | the three standard streams: input, results, complaints |
| field | a piece of a line between delimiters |
| delimiter | the character that separates fields |
| header | the first line naming the columns |
| stage | one program in a pipeline |
| stream | data read in order, in chunks |
| locale | the rules for ordering and comparing text |
| regular expression | a pattern describing text |
| exit status | a number saying whether a command succeeded |
| bottleneck | the stage that limits total speed |
| trust boundary | the line between data you control and data you do not |
| reconcile | confirm a result with a second, independent method |
| anchor (a pattern) | make it match only where intended, such as between commas |
| associative array | an awk table keyed by a value, used to group |
| adjacent | next to each other: what `uniq` needs |

### Claims register `{A42}` `{A58}`

| Id | Claim | Quote or VERIFY | Status | Note |
|---|---|---|---|---|
| C1 | `sort`, then `uniq -c`, then `sort -rn` counts and ranks values in a column | VERIFY | Run | lab block in example A matched |
| C2 | `uniq -c` without `sort` leaves scattered repeats uncounted | VERIFY | Run | failure case 1 matched |
| C3 | `awk` can total quantity times price per item | VERIFY | Run | example B matched |
| C4 | `grep -c` counts matching lines | VERIFY | Run | lab A1 matched |
| C5 | a numeric condition is an awk pattern | VERIFY | Run | lab A3 matched |
| C6 | `sort -t, -k4 -rn` orders by a numeric column | VERIFY | Run | lab A4 matched |
| C7 | plain `sort` orders `10` before `9` | VERIFY | Run | trace drill 3 follows this behaviour |
| C8 | the awk array groups in one pass | VERIFY | Run | example C matched |
| C9 | the messy file has a blank line, a repeated header and a quoted comma | VERIFY | Run | lab D matched |
| C10 | the output of the last stage is buffered differently on a pipe than on a terminal | VERIFY | Not run | expert-view claim; no source captured |
| C11 | ties sort differently under different locales | VERIFY | Not run | observed on some systems; not run here |
| C12 | `pipefail` stops a pipeline on the first failing stage | VERIFY | Not run | bash behaviour, stated from knowledge |

### Gap list

Not covered by the captured source: no manual-page text was captured for `grep`, `awk`, `cut`, `sort`, `uniq` or `sed`, so option behaviour beyond the labs is unverified. Not run: other awk variants (mawk, busybox), other shells, quoted CSV parsing, Windows line endings, locale ordering, large-file timing, buffering. The expert-view claims are marked VERIFY. **Lab run status:** run (front matter).

### Rule-coverage matrix `{A60}`

Where each family of rules is applied (a tag in the parts is the evidence):

| Rules | Applied in |
|---|---|
| A3 A8 A54 V13 (outcomes, graph, structure, trees) | part 1, move 1 |
| A5 A7 A18 V18 (first principles, concrete first, analogies, black box) | part 1, move 3 |
| A4 A6 A17 A31 A57 V9 V11 V16 V20 (levels, lenses, representations, traces, sequence, data shape) | part 1, moves 4 and 5 |
| A9 A10 A12 A17 V21 (scaffolding, worked examples, Socratic) | part 1, move 6 |
| A16 A24 A27 A39 A40 A41 V7 V15 (compare, trade-offs, labels, giants, assumptions) | part 1, move 7 |
| A29 A33 P3 P4 P7 P16 (commands, verification, labs, hints) | part 2, move 8 |
| A14 A15 V30 (errors, misconceptions, before/after) | part 2, move 9 |
| A22 A25 A32 V25 P8 (failure, hypotheses, debugging, break-fix) | part 2, move 10 |
| A11 A13 A19 A20 P5 P6 P9 P10 P11 P17 V31 (retrieval, drills, quiz, cards, interleaving, schedule) | parts 1 and 3, moves 2 and 12 |
| A23 A26 A28 A34 A35 A42 V22 V27 V28 V32 (systems, expert, security, performance, evidence) | part 4, move 11 |
| A21 A46 A47 A48 A44 P13 P14 P15 (transfer, critique, reconstruction, design, capstone) | part 4, move 13 |
| A49 A50 A51 A59 A60 (teach back, metacognition, mastery, independence) | part 4, move 14 |
| A44 A58 P12 P18 V29 (documentation, honesty, cheat sheets, export, completion report) | part 5, move 15 |

### Visual completion report `{V29}`

```
 what this topic contains                     how it works now                       verification
   1-learn    moves 1-7, 3 examples             learn ► do ► retrieve ► transfer ►     labs run:  yes (see front matter)
   2-do       4 labs, 3 failures, 2 break-fix   reference; each part feeds the next    gate:      structure, rules, copy limit
   3-retrieve 10 drills, 10 quiz, 30 cards      error-to-aid loop closes the circle    review:    not done (status proposed)
   4-transfer systems, transfer, capstone       one-sentence model to keep:            run:       other shells, locales, big files
   5-reference cheat sheets, glossary, claims   "small tools, text streams, checked    not run
                                                 one stage at a time"
```

### Next steps

`K-LOG01` (apply these tools to web logs), `K-GEN02` (file types and magic bytes), then `jq` for JSON. Export `3-retrieve.md` cards to Anki `{P18}`: one card per `- [type][difficulty]` line, Front and Back as written, difficulty as a tag.
