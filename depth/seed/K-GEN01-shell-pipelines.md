---
id: K-GEN01
title: "Linux shell fluency: turning files into answers with pipes, cut, sort, uniq, grep and awk"
category: GEN
level: L1
status: proposed
lab_run: "Run 2026-11-26 in WSL Ubuntu with GNU coreutils and awk, LC_ALL=C; every lab block was executed by depth/tools/gate.py against depth/data/make_sample.py output. Other shells and awk variants: not run."
lane: frontier seed page (the example the local model is shown)
---

# Linux shell fluency: turning files into answers

> **Status:** proposed. The lab commands in this page were executed and matched (see the front matter). Nothing here has been independently reviewed.

## 1. Orient

**Outcomes.** After this page you can: (1) explain how a pipe connects two programs; (2) count, group and rank the values in one column of a text file; (3) pick `grep`, `cut`, `sort`, `uniq` or `awk` for a given question and say why; (4) read a pipeline left to right and predict its output; (5) find the usual reason a pipeline gives the wrong answer; (6) write a three-stage pipeline from a plain-English question.

**Prerequisites.** You can open a terminal, run `ls` and `cat`, and know that a file is a list of lines. Next pages: `K-LOG01` (web logs with these tools) and `K-GEN04` (archives and compression).

**Short answer.** Each Linux text tool does one small job on lines of text. A pipe (`|`) feeds the output of one tool into the next, so a long question becomes a chain of small steps you can check one at a time.

```
 concept map
                         ┌─────────────────────────┐
                         │  PIPELINE: small tools  │
                         │  chained with  |        │
                         └────────────┬────────────┘
        pick lines              pick columns            order and count
   ┌────────────────┐     ┌────────────────────┐    ┌───────────────────────┐
   │ grep  (match)  │     │ cut  (by position) │    │ sort   (order)        │
   │ head / tail    │     │ awk  (by field,    │    │ uniq -c (count runs)  │
   │ (by position)  │     │      and maths)    │    │ wc -l  (count lines)  │
   └────────────────┘     └────────────────────┘    └───────────────────────┘
```

## 2. Prime: predict before you read

Cover the answers and write a guess for each.

1. A file has the regions `west north west south`, one per line. You run `uniq -c` on it. Do you get `2 west`? Why or why not?
2. `cut -d, -f2` is run on the line `2026-11-01,west,date,1,6.5`. What is printed?
3. `sort` puts `10` before `9`. Is the tool broken?

*Answers (check after reading):* 1 no, `uniq` only joins neighbours, so the two `west` lines stay separate until the input is sorted. 2 `west`, the second comma-separated field. 3 no, plain `sort` compares characters, so `1` comes before `9`; `-n` compares numbers.

Concept cards to cover and reveal: *What does a pipe pass along?* (standard output of the left program becomes standard input of the right one). *What does `grep -c` print?* (a count of matching lines, not the lines). *What is a field?* (a piece of a line between separators).

## 3. Intuition

**The problem.** You have a file of 60 sales lines and a question: which region sells the most orders? Reading the file by eye works for 60 lines and fails for 60,000.

**The naive solution.** Open the file in an editor, scan down, and tally on paper. It works once, it is slow, and it cannot be repeated on tomorrow's file.

**Why it falls short.** The tally is a mechanical procedure: pick one column, group equal values, count each group, rank the groups. A computer does each of those steps instantly. What it needs is a way to hand the file from one step to the next without saving temporary files, and that is the pipe.

**Analogy.** A kitchen line. One cook washes, the next chops, the next cooks, and the plate moves along the counter without anyone carrying it back to a storeroom. *What the analogy gets right:* each station does one thing, and the order of stations matters. *Where it breaks:* a cook can stop and ask a question; a pipeline runs straight through, so a wrong first step silently ruins every later one.

```
 black box view
   file ──► [ pick the column ] ──► [ group equal values ] ──► [ count ] ──► [ rank ] ──► answer
            cut -d, -f2             sort                        uniq -c       sort -rn
```

## 4. Foundations

| Term | Plain English | Precise | Example | Why it matters |
|---|---|---|---|---|
| Standard output (stdout) | where a program prints its results | file descriptor 1 | `ls` prints names | pipes read this |
| Standard input (stdin) | where a program reads when no file is named | file descriptor 0 | `sort` with no file reads the pipe | lets tools be chained |
| Pipe `\|` | a one-way tube between two programs | connects stdout of the left to stdin of the right | `cat f \| sort` | builds pipelines |
| Field | one piece of a line between separators | text between delimiters | `west` in `a,west,b` | `cut` and `awk` work on fields |
| Delimiter | the character that separates fields | set by `-d,` (cut) or `-F,` (awk) | the comma in a CSV | wrong delimiter gives the whole line |
| Regular expression | a pattern describing text | the language `grep` uses | `^2026` matches lines starting with 2026 | selects lines |
| Exit status | a number saying whether a command succeeded | 0 means success | `grep` returns 1 when nothing matches | scripts branch on it |

*Relations:* `uniq` **requires** sorted input to group; `sort -rn` **orders** what `uniq -c` produced; `awk` **replaces** `cut` when you need arithmetic or a condition on a field.

## 5. Mechanics

**What happens when you type `a | b | c`.** The shell starts the three programs at the same time. It connects a's stdout to b's stdin and b's stdout to c's stdin. Data flows in chunks, so c can print before a has finished reading a large file. If you do not redirect the last program, its output goes to the terminal.

```
 sequence: three programs, two pipes
   shell        a              b              c           terminal
     │ start a,b,c, wire pipes │              │              │
     ├────────►│              │              │              │
     │         │ lines ──►    │              │              │
     │         │   (pipe 1)   │ lines ──►    │              │
     │         │              │   (pipe 2)   │ result ───►  │
     │         │              │              │              │
```

**The five tools in one sentence each, with the question each answers.**

- `grep PATTERN file`: which lines contain this? (`-c` counts them, `-n` numbers them, `-v` inverts, `-i` ignores case.)
- `cut -d, -f2 file`: what is in this column? (works on a single-character delimiter.)
- `sort`: put the lines in order. (`-n` numbers, `-r` reverse, `-k2` by the second field, `-t,` set the separator, `-u` drop repeats.)
- `uniq -c`: how many times did this line repeat in a row?
- `awk -F, 'condition {action}' file`: for each line, if the condition holds, do something with its fields (`$1` is the first field, `NR` is the line number).

**The seven lenses.** *What:* chain small tools. *Why:* each step is easy to check, and the chain is repeatable. *How:* stdout to stdin. *When:* any text that has structure, such as logs, CSV and command output. *Where:* a shell on Linux, macOS or WSL. *What if:* the data is binary or deeply nested (JSON): use a tool made for it, such as `jq`. *Why not a spreadsheet:* a pipeline runs on huge files, runs again unchanged, and can sit inside a script.

**Simplified model, accurate model.** *Simplified:* "each tool reads text and writes text." *Accurate:* each tool reads a stream of bytes and splits it at newlines; sorting, field splitting and comparison depend on the locale unless it is fixed (the lab uses `LC_ALL=C`). *Expert model (VERIFY):* the programs buffer their output differently on a terminal and on a pipe, so a slow producer can look stuck until a buffer fills.

## 6. Worked example

The file `sales.csv` has the columns `date,region,item,qty,price`. Question: **how many orders per region, biggest first?**

First look at the data. Always look before you transform.

```lab
$ head -3 sales.csv
date,region,item,qty,price
2026-11-01,west,date,1,6.5
2026-11-02,north,elderberry,5,9.0
```

Now build the answer one stage at a time. Stage 1 removes the header and keeps column 2. Stage 2 sorts so equal regions are neighbours. Stage 3 counts the neighbours. Stage 4 ranks the counts.

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | sort | uniq -c | sort -rn
     18 west
     18 north
     15 south
      9 east
```

**Trace table** (the same pipeline on a tiny input, five lines `west north west south west`):

| Stage | Command | What it outputs |
|---|---|---|
| 1 | `cut -d, -f2` | `west north west south west` |
| 2 | `sort` | `north south west west west` |
| 3 | `uniq -c` | `1 north`, `1 south`, `3 west` |
| 4 | `sort -rn` | `3 west`, `1 south`, `1 north` |

**Faded copy** (fill the blanks, then check below): *How many orders per item?* Column 3 holds the item. `cut -d, -f__ sales.csv | tail -n +2 | ____ | uniq -c | sort -rn`. Answer: field `3`, and the missing stage is `sort`.

**A similar problem alone.** How many distinct items are there? (Hint: `sort -u`, then `tr` can put them on one line.)

```lab
$ cut -d, -f3 sales.csv | tail -n +2 | sort -u | tr '\n' ' '
apple banana cherry date elderberry 
```

## 7. Compare and decide

| Need | Use | Why not the others |
|---|---|---|
| Lines containing a word | `grep` | `awk` works but is longer |
| One column, no maths | `cut` | `awk` is heavier; `cut` needs a one-character separator |
| A condition on a number in a column | `awk` | `grep` cannot compare numbers |
| Group and count | `sort \| uniq -c` | `uniq` alone needs sorted input |
| Sum or average a column | `awk` | `cut` and `sort` cannot add |

**Decision rule:** if the answer needs arithmetic or a numeric condition, use `awk`; if it only selects lines, use `grep`; if it only selects columns, use `cut`.

```
 decision tree
              what do you need?
        ┌──────────────┼──────────────────┐
   some lines     some columns        a number computed
        │              │                   │
      grep          cut -d X -f N        awk (sum, test, average)
        │              │
   then count?    then group and count?
     grep -c       sort | uniq -c
```

*Labels on advice:* "always look at the head of the file first" is a **best practice**. "Use `LC_ALL=C` in scripts so sorting is repeatable" is a **rule of thumb**. "Put the delimiter in single quotes" is a **requirement** when the delimiter is a shell special character.

## 8. Do it: guided lab

**Objective.** Answer four questions about `sales.csv` with pipelines you build one stage at a time. **Environment.** Any Linux shell or WSL; create the data with `python depth/data/make_sample.py DIR` and `cd` into `DIR`. **Cleanup.** Delete the directory when you are done; nothing else is changed.

**Task 1: how many lines mention the north region?** Why: `grep -c` counts matching lines. The pattern has commas around it so it cannot match `north` inside another word.

```lab
$ grep -c ,north, sales.csv
18
```

- Hint 1: you want a count, not the lines themselves.
- Hint 2: look at the `-c` option of `grep`.
- Hint 3: `grep -c ____ sales.csv` with the pattern `,north,`.
- Hint 4: `grep -c ,north, sales.csv` prints 18; the commas stop it matching other fields.

**Task 2: what is the total value (qty times price) per item, biggest first?** Why: this needs multiplication and a running total per item, which is a job for `awk`. The array `t` keeps one total per item; the `END` block runs once after the last line.

```lab
$ awk -F, 'NR>1 {t[$3]+=$4*$5} END {for (k in t) printf "%s %.2f\n", k, t[k]}' sales.csv | sort -k2 -rn
elderberry 684.00
cherry 476.00
date 357.50
apple 42.00
banana 20.50
```

- Hint 1: you need arithmetic on two columns, so `cut` is not enough.
- Hint 2: `awk` can keep an array indexed by the item name.
- Hint 3: `NR>1 {t[$3]+=$4*$5}` adds up each line; an `END` block prints the array.
- Hint 4: pipe the awk output to `sort -k2 -rn` to rank by the second field as a number.

**Task 3: how many orders have a quantity of 10 or more?** Why: a condition on a number is an `awk` pattern; `wc -l` counts what survives.

```lab
$ awk -F, 'NR>1 && $4>=10' sales.csv | wc -l
16
```

- Hint 1: you need a numeric comparison on column 4.
- Hint 2: an awk pattern without an action prints the whole matching line.
- Hint 3: `NR>1` skips the header; add `&& $4>=10`.
- Hint 4: pipe to `wc -l` to count the matching lines.

**Task 4: the three biggest quantities.** Why: sort numerically on column 4, reversed, and keep three lines. With ties the order depends on the whole line, which is why the lab sets `LC_ALL=C`.

```lab
$ tail -n +2 sales.csv | sort -t, -k4 -rn | head -3
2026-11-26,south,date,12,6.5
2026-11-19,west,apple,12,0.5
2026-11-13,west,apple,12,0.5
```

- Hint 1: you need numeric order on one column of a comma-separated file.
- Hint 2: `sort` needs the separator set with `-t`.
- Hint 3: `sort -t, -k4 -rn` sorts by column 4, numeric, biggest first.
- Hint 4: add `head -3` and remove the header with `tail -n +2` first.

**Verification.** Compare each output with the block above it. **Stretch.** Total quantity per region: change the awk key from `$3` to `$2` and the sum to `$4`. **Progression:** guided (this lab), prompted (answer "orders per day" from a goal and the hints), unassisted (write the pipeline from a question only), adversarial (the data has a blank line and a header repeated in the middle: what breaks?).

## 9. Repair: common mistakes and wrong models

| Mistake | What breaks | Instead |
|---|---|---|
| `uniq -c` without `sort` | counts of 1 for scattered repeats | `sort \| uniq -c` |
| `sort` on numbers without `-n` | `10` sorts before `9` | `sort -n` |
| `cut -d' '` on text with several spaces | empty fields | use `awk '{print $2}'`, which splits on runs of spaces |
| forgetting the header line | the word "region" is counted as a region | `tail -n +2` or `NR>1` |
| `grep north` | also matches `northeast` | anchor it: `,north,` or `-w` |
| `cat file \| grep x` | works, but adds a pointless process | `grep x file` |

**Misconception.** "The shell reads the whole file into memory first." *Why it is reasonable:* that is how a spreadsheet works. *Where it breaks:* a pipeline streams, so the first output line can appear before the last input line is read. *Test:* run `yes | head -3`; it stops at once even though `yes` never ends.

```
 before / after
   BEFORE (broken)                          AFTER (fixed)
   cut -d, -f2 | uniq -c                    cut -d, -f2 | sort | uniq -c
   "1 west 1 north 1 south 1 north ..."     "18 north 15 south 18 west 9 east"
        [!] repeats are not neighbours           sorting makes equal lines neighbours
```

## 10. Break it

**Failure case: the counts look wrong.** *Symptom:* every count is 1. *Causes (hypotheses):* (a) the input is not sorted, (b) the delimiter is wrong so each whole line is unique, (c) hidden characters such as carriage returns make equal values differ. *Most informative test:* look at the first lines of the data after the cut. Here is the symptom for hypothesis (a):

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | uniq -c | head -4
      1 west
      1 north
      1 south
      1 north
```

| Hypothesis | Evidence for | Evidence against | Test | Result |
|---|---|---|---|---|
| (a) unsorted | the same region appears again later | none | add `sort` before `uniq` | counts become 18, 18, 15, 9 |
| (b) wrong delimiter | each count line is a whole row | the output shows only the region name | print `head -2` after the cut | the output is one column, so this is not it |
| (c) carriage returns | `west` and `west^M` look equal | the output was clean | `cat -A` shows `^M` | not present here |

**Break-fix lab (symptom only).** A teammate's pipeline `grep north sales.csv | cut -d, -f4 | sort | uniq -c` prints counts, but the totals are higher than `grep -c ,north, sales.csv` says. Find the two causes before reading on: the pattern `north` can match text in other fields, and the output counts quantities, not orders. Prevention: anchor the pattern, and write down what each stage is supposed to produce.

```
 failure map
   normal:  pattern ──► fields ──► group ──► count ──► ranking correct
   fault:   pattern too loose           [!] extra lines enter the pipeline
   symptom: totals higher than expected
   blast radius: every later stage is correct but the answer is wrong
   mitigation: anchor the pattern; compare against grep -c
```

## 11. Zoom out

**Where this sits.** Shell pipelines are the glue of CTF work, log triage and system administration. The same stages scale from a 60-line file to a 6 GB log, because the pipe streams.

**Trust boundary.** Text in a file is data. Pasting it into a command line, or running `bash -c` on it, turns data into code: never do that with content from a source you do not control. **Bottleneck:** `sort` is the stage that must see all input before it can print, so it limits memory and speed on large files.

**Beginner, accurate and expert model.** *Beginner:* "tools in a row." *Accurate:* each tool is a process, the pipe is a kernel buffer, and the order of stages changes both the answer and the cost: filter early, sort late. *Expert (VERIFY):* in production, fixed locales, `set -o pipefail` and explicit error handling matter, because a failing first stage does not stop the pipeline by default. *Textbook versus production:* the page shows one clean file; real files have blank lines, quoted commas and mixed line endings.

## 12. Retrieve and discriminate

**Micro-drills** (answers after each; try first).

1. **Drill** Print only the third field of `a:b:c` lines. *Answer:* `cut -d: -f3`.
2. **Drill** Count lines that contain `error` in `app.log`. *Answer:* `grep -c error app.log`.
3. **Drill** Sort the lines of `n.txt` as numbers, largest first. *Answer:* `sort -rn n.txt`.
4. **Drill** Show each distinct line of `names.txt` once. *Answer:* `sort -u names.txt`.
5. **Drill** Print the second field of lines whose first field is `GET`. *Answer:* `awk '$1=="GET" {print $2}'`.
6. **Drill** Add up the numbers in column 4 of a CSV. *Answer:* `awk -F, 'NR>1 {s+=$4} END {print s}'`.

**Trace drill.** Predict the output of `printf 'b\na\nb\n' | sort | uniq -c`. *Answer:* `1 a` then `2 b` (with the counts right-aligned).

**Diagnostic quiz** (choose, then read why each option is right or wrong).

**Q1.** A pipeline `cut -d, -f2 f | uniq -c` gives many lines with the count 1. What is the most likely fix?
  - (A) Add `sort` before `uniq` — right: `uniq` only merges neighbours, so scattered repeats stay separate until the input is sorted.
  - (B) Add `-r` to `cut` — wrong: `cut` has no such option for this, and it would not group anything.
  - (C) Replace `uniq -c` with `wc -l` — wrong: that counts all lines, not the repeats per value.
  - (D) Use `grep -c` — wrong: it counts matching lines in total and does not group values.

**Q2.** Which tool adds up the numbers in a column?
  - (A) `cut` — wrong: it extracts fields and cannot do arithmetic.
  - (B) `sort` — wrong: it orders lines and does not add them.
  - (C) `awk` — right: an action such as `s+=$4` accumulates a total across lines.
  - (D) `uniq` — wrong: it counts repeated lines and does not sum field values.

**Q3.** `sort` prints `10` before `9`. Why?
  - (A) The file is corrupted — wrong: the data is fine; the ordering rule is the cause.
  - (B) Plain `sort` compares characters — right: the character `1` comes before `9`, so `-n` is needed for numeric order.
  - (C) `sort` is reversed by default — wrong: the default is ascending, by character.
  - (D) The locale is broken — wrong: even a correct locale compares text unless told otherwise.

**Q4.** Why does `grep north sales.csv` sometimes return more lines than expected?
  - (A) It matches inside longer words such as `northeast` — right: without anchors the pattern matches any occurrence of the letters.
  - (B) It also searches other files — wrong: it reads only the file named.
  - (C) It ignores the header — wrong: it treats every line the same.
  - (D) It counts bytes — wrong: matching is by lines of text.

**Q5.** What does the pipe in `a | b` pass from `a` to `b`?
  - (A) The exit status — wrong: that is separate and is not data flowing through the pipe.
  - (B) The standard output of `a` as the standard input of `b` — right: that is the whole mechanism.
  - (C) The files `a` opened — wrong: open files are not handed over; only the byte stream is.
  - (D) The environment variables of `a` — wrong: a child process may inherit them, but the pipe does not carry them.

**Flashcards** (five types, tagged by difficulty).

- [concept][easy] Front: What does `|` do? Back: connects the stdout of the left program to the stdin of the right program.
- [concept][easy] Front: What does `cut -d, -f2` print? Back: the second comma-separated field of each line.
- [concept][medium] Front: What does `uniq -c` count? Back: how many times a line repeats consecutively.
- [concept][medium] Front: What does `grep -c` print? Back: the number of matching lines.
- [concept][easy] Front: What does `wc -l` count? Back: lines.
- [cloze][easy] Front: To group equal lines before `uniq`, run `____` first. Back: `sort`.
- [cloze][medium] Front: awk splits on a comma with `-F____`. Back: `-F,`.
- [cloze][easy] Front: `sort ____` orders numbers correctly. Back: `-n`.
- [cloze][medium] Front: `tail -n ____` prints from line 2 onward and drops a header. Back: `+2`.
- [scenario][medium] Front: A log has 100 000 lines and you want the five most frequent values in column 3. Which pipeline? Back: `cut -f3 file | sort | uniq -c | sort -rn | head -5`.
- [scenario][trap] Front: You get a count of 1 for every value. First check? Back: whether the input is sorted before `uniq`.
- [scenario][medium] Front: You need the total of column 4 where column 2 is `west`. Tool? Back: `awk -F, '$2=="west" {s+=$4} END {print s}'`.
- [contrast][medium] Front: `cut` versus `awk` for fields? Back: `cut` is simple and needs a one-character delimiter; `awk` handles runs of spaces, conditions and arithmetic.
- [contrast][trap] Front: `sort -u` versus `sort | uniq`? Back: both give distinct lines; only `uniq -c` also counts.
- [trace][medium] Front: Output of `printf 'b\na\nb\n' | sort | uniq -c`? Back: `1 a` then `2 b`.
- [trace][trap] Front: Output of `printf 'b\na\nb\n' | uniq -c`? Back: `1 b`, `1 a`, `1 b` (not sorted, so nothing merges).

**Mixed set with earlier ideas.** For each, name the tool before running anything: (1) the line count of a file; (2) the lines that do not contain `404`; (3) the average of a column; (4) the longest line. *Answers:* `wc -l`; `grep -v 404`; `awk` (sum divided by count); `awk '{ if (length($0)>m) {m=length($0); l=$0} } END {print l}'`.

## 13. Transfer and design

**Near transfer.** Count orders per day in `sales.csv`. The date is column 1, so only the field number changes. **Representation transfer.** Rewrite Task 2 as a table in a spreadsheet (a pivot of item by sum of qty times price) and say what the pivot does for you that the pipeline does by hand. **Context transfer.** A web log has the status code in field 9 of each line. Which pipeline lists status codes by frequency? (`awk '{print $9}' access.log | sort | uniq -c | sort -rn`; `K-LOG01` builds this out.) **Far transfer.** The same group, count, rank idea answers "which process uses the most memory?" and "which words occur most in this book?"

**Critique.** A teammate wrote `cat sales.csv | grep west | cut -d, -f4 | sort | uniq`. List the problems: a needless `cat`, the pattern can match other fields, `uniq` without `-c` hides how often each quantity appears, and the header is kept in the first stage. **Reconstruct.** Given only the question "which item is ordered with the largest single quantity?", derive the pipeline from first principles and say which stage is the key.

**Design with a constraint shift.** Design a one-line report of orders per region. Now the file is 100 times bigger: which stage is the bottleneck and what could you do (filter early, use `LC_ALL=C`, avoid sorting twice)? Now the file arrives while it is still being written: what changes?

## 14. Teach back and check yourself

Explain a pipeline to three audiences, each in under a minute. *A beginner:* "one program hands its output to the next, like plates along a counter." *A practitioner:* "stages are processes connected by pipes; filter early, sort late; use `LC_ALL=C` for repeatable order." *An expert:* "each stage buffers, `sort` must read all input, and a failing stage does not stop the pipeline unless `pipefail` is set."

**Mastery ladder** (mark each as recognised, recalled or applied): define a pipe; explain why `uniq` needs sorted input; demonstrate the region-count pipeline; apply it to the item column; distinguish `cut` from `awk`; analyse why a count of 1 appears everywhere; troubleshoot a pipeline that gives the wrong total; evaluate two pipelines for the same task; design a report with a constraint shift; transfer the idea to a log file; teach it to a beginner.

## 15. Close

**Cheat sheet.**

```
 decision tree                         top patterns
   lines? ── grep                       count lines matching     grep -c PATTERN file
   columns? ── cut                      one column               cut -d, -f2 file
   maths? ── awk                        group and count          ... | sort | uniq -c | sort -rn
                                        sum a column             awk -F, '{s+=$4} END {print s}'
 pitfalls                               top N                    ... | head -N
   counts all 1  ──► sort first         drop a header            tail -n +2
   10 before 9   ──► sort -n            distinct values          sort -u
   extra matches ──► anchor the pattern
```

**What to learn next.** `K-LOG01` (apply this to web logs), `K-GEN02` (file types and magic bytes), then `jq` for JSON.

**Claims register.**

| Id | Claim | Quote or VERIFY | Status | Note |
|---|---|---|---|---|
| C1 | `sort`, then `uniq -c`, then `sort -rn` counts and ranks values in a column | VERIFY | Run | lab block in section 6 matched |
| C2 | `uniq -c` without `sort` leaves scattered repeats uncounted | VERIFY | Run | lab block in section 10 matched |
| C3 | `awk` can total qty times price per item | VERIFY | Run | lab block in task 2 matched |
| C4 | `grep -c` counts matching lines | VERIFY | Run | lab block in task 1 matched |
| C5 | plain `sort` orders `10` before `9` | VERIFY | Not run | stated from knowledge; run it to confirm |
| C6 | the output of the last stage is buffered differently on a pipe than on a terminal | VERIFY | Not run | expert-view claim; no source captured |

**Gap list.** Not covered by the captured source: no manual-page text was captured for `grep`, `awk`, `cut`, `sort` or `uniq`, so option behaviour beyond the lab is unverified. Not run: other awk variants and shells, quoted CSV fields, Windows line endings. **Lab run status:** run (front matter).
