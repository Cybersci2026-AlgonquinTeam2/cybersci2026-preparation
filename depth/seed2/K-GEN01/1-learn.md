---
id: K-GEN01
title: "Linux shell fluency: turning files into answers with pipes, cut, sort, uniq, grep and awk"
category: GEN
level: L1
status: proposed
lab_run: "Run 2026-11-26 in WSL Ubuntu (GNU coreutils, GNU Awk 5.2.1), LC_ALL=C: every lab block was executed by depth/tools/gate_v2.py against depth/data/make_sample.py output. Other shells, awk variants and quoted-CSV parsers: not run."
lane: frontier seed v2 (the example the local model is shown)
---

# Linux shell fluency: turning files into answers

> **Status:** proposed. Part 1 of 5. The labs in part 2 were executed; nothing here has been independently reviewed. Tags such as `{A13}` name the learning rule an element applies; `{V9}` names a visual rule; `{P7}` names a practice aid. They are explained in `depth/SPEC-v2.md`.

## 1. Orient

**Outcomes** `{A3}`. After the five parts you can:

1. **Explain** how a pipe connects two programs and what flows through it.
2. **Build** a pipeline that counts, groups and ranks the values in one column of a text file.
3. **Choose** between `grep`, `cut`, `sort`, `uniq`, `awk` and `sed` for a stated question, and defend the choice.
4. **Predict** the output of a pipeline from its text and a sample of the input.
5. **Diagnose** a pipeline that gives a wrong answer by finding the first stage that goes wrong.
6. **Compare** two pipelines for the same job on speed, clarity and risk.
7. **Design** a three-to-five stage report for an unfamiliar file and write the test that proves it right.

**Prerequisites** `{V13}` `{fig:tree}`. You can open a terminal, run `ls` and `cat`, and know a file is a list of lines.

```
 prerequisite tree (arrows: "is needed for")
   a file is lines ──────────► a line has fields ──────────► cut / awk pick fields
        │                              │
        └──► a program reads input ────┴──► a pipe joins output to input ──► pipelines
                 and writes output                                              │
                                                                                ▼
                                                              sort ► uniq -c ► sort -rn  (rank values)
```

**Short answer.** Each text tool does one small job on lines. A pipe sends one tool's output to the next tool's input, so a large question becomes a chain of small steps, each checkable on its own.

**Concept map** `{A8}` `{fig:map}`.

```
                           ┌──────────────────────────┐
                           │  PIPELINE  a | b | c     │
                           └─────────────┬────────────┘
        choose lines                 choose columns               order and count
   ┌───────────────────┐       ┌────────────────────┐       ┌────────────────────────┐
   │ grep  (by pattern)│       │ cut  (by position) │       │ sort    (order)        │
   │ head/tail (by     │       │ awk  (by field,    │       │ uniq -c (count runs)   │
   │ position)         │       │  test, arithmetic) │       │ wc -l   (count lines)  │
   └───────────────────┘       └────────────────────┘       └────────────────────────┘
```

**How the figures work** `{V1}` `{V2}` `{V3}` `{V4}` `{V5}`. Each idea shows its picture before or beside the words (draw first, narrate second). The picture type is chosen to fit the idea: a map for structure, a tree for choices, a sequence for exchanges over time, a trace table for step-by-step values, a states figure for a life cycle, layers for a stack, zones for boundaries. Figures are plain text so they survive any viewer; none has more than nine boxes, every arrow is labelled with what crosses it, and boundaries are drawn.

```
 legend {V5}
   ──►  flow or sequence      ◄──►  two-way       - - ►  optional or later
   [Box] a component or state     <Decision> a branch      [!] bottleneck, failure point or trust boundary
```

**Knowledge-graph relations** `{A8}`: `uniq -c` **requires** sorted input to group; `sort -rn` **orders** what `uniq -c` produced; `awk` **replaces** `cut` when a condition or arithmetic is needed; `grep` **narrows** the lines every later stage sees; a wrong delimiter **causes** whole-line fields; `LC_ALL=C` **makes** ordering repeatable.

**Reading plan.** Part 1 learn (about 90 minutes), part 2 labs (about 2 hours), part 3 retrieval (about 45 minutes, then again after 1, 3, 7, 14 and 30 days), part 4 transfer and capstone (about 2 hours), part 5 reference (a lookup page). Learner time for the topic: about 6 hours.

## 2. Prime: predict before you read

Cover the answer lines. For each item write a guess first `{A13}` `{A11}`. The form is scenario, prediction, result, and what a wrong guess tells you about your model.

| # | Scenario | Your prediction | Result (check after reading) | What a wrong guess means |
|---|---|---|---|---|
| 1 | The lines `west north west south` run through `uniq -c` | ? | `1 west`, `1 north`, `1 west`, `1 south`: nothing merges | you think `uniq` removes duplicates anywhere; it only joins neighbours |
| 2 | `cut -d, -f2` on `2026-11-01,west,date,1,6.5` | ? | `west` | you counted fields from zero or ignored the delimiter |
| 3 | `sort` on the lines `10` and `9` | ? | `10` first | you think sort reads numbers; it compares characters unless told otherwise |
| 4 | `a \| b` where `a` prints 1,000,000 lines and `b` is `head -1` | ? | `b` prints one line quickly; `a` is stopped early | you think the first program must finish before the second starts |
| 5 | `grep -c north` on a file where the word appears in two fields of one line | ? | the line is counted once | you think `-c` counts matches; it counts matching lines |

**Entry diagnostic** `{A50}`: score yourself 0 to 5 on the table above. 4 or 5: skim sections 3 and 4, then start at section 5. 2 or 3: read everything. 0 or 1: also read the prerequisite tree first and do the cards below.

**Concept cards to cover and reveal** `{P6}`: *What is a pipe?* (a one-way tube from one program's output to another's input). *What does `grep -c` print?* (a count of matching lines). *What is a field?* (a piece of a line between separators). *Why does `10` sort before `9`?* (characters are compared). *What does `uniq -c` need to group equal lines?* (sorted input).

## 3. Intuition

**Concrete example first** `{A7}`. You hold a file of 60 sales lines and want to know which region has the most orders. Reading by eye works for 60 lines and fails for 60,000.

**First principles** `{A5}`. Walk the chain:

| Step | Statement |
|---|---|
| Problem | turn a long text file into a short answer |
| Naive solution | read it and tally on paper |
| Why it fails | it is slow, error-prone and cannot be repeated tomorrow on a new file |
| Constraints | the data is lines; the answer needs one column; equal values must be grouped; the result must be ranked |
| The concept | do each mechanical step with a small program and pass the data along without saving temporary files: a pipe |
| Trade-offs | gain: speed, repeatability, streaming; lose: you must know the tools, and one wrong stage silently ruins the answer |

**Two analogies** `{A18}`.

- *A kitchen line.* One cook washes, the next chops, the next cooks; the plate moves along the counter. **Gets right:** each station does one job and order matters. **Breaks:** a cook can stop and ask a question; a pipeline runs straight through, so a wrong first station spoils every later one.
- *A post-sorting office.* Letters pass through a machine that reads the postcode, then one that groups equal postcodes, then one that counts the bundles. **Gets right:** grouping needs neighbours (equal items must be together before they are counted). **Breaks:** the post office can hold items for later; a pipe has a small buffer and a fast producer waits for a slow consumer.

```
 black box view {V18} {fig:blackbox}
   file ──► [ pick the column ] ──► [ group equal values ] ──► [ count ] ──► [ rank ] ──► answer
            cut -d, -f2             sort                        uniq -c       sort -rn
   Simplified: "tools in a row"   Accurate: processes joined by kernel buffers   Expert: see section 5
```

## 4. Foundations

| Term | Plain English | Precise | Example | Why it matters |
|---|---|---|---|---|
| Standard output (stdout) | where a program prints results | file descriptor 1 | `ls` prints names | pipes read this |
| Standard input (stdin) | where a program reads when no file is named | file descriptor 0 | `sort` with no file reads the pipe | lets tools be chained |
| Standard error (stderr) | where a program prints complaints | file descriptor 2 | `grep: file: No such file` | not carried by a pipe by default |
| Pipe `\|` | a one-way tube between two programs | connects stdout of the left to stdin of the right | `cat f \| sort` | builds pipelines |
| Field | a piece of a line between separators | text between delimiters | `west` in `a,west,b` | `cut` and `awk` select fields |
| Delimiter | the character separating fields | `-d,` for cut, `-F,` for awk | the comma in a CSV | the wrong one gives the whole line as field 1 |
| Regular expression | a pattern describing text | the language `grep` and `awk` use | `^2026` matches lines starting with 2026 | selects lines |
| Exit status | a number saying whether a command succeeded | 0 means success | `grep` returns 1 when nothing matches | scripts branch on it |
| Locale | the rules for ordering and comparing text | set by `LC_ALL` | `LC_ALL=C` compares bytes | changes sort order |
| Stream | data read in order, in chunks | not held whole in memory | a log read line by line | why pipelines scale |
| Stage | one program in a pipeline | a process with its own input and output | `sort` in `a \| sort \| b` | the unit you check |
| Header | the first line naming the columns | not data | `date,region,item,qty,price` | must be removed before counting |

**Relations** `{A8}`: a stage **needs** an input stream; a delimiter **defines** fields; a locale **changes** sorting; a header **pollutes** counts if left in.

**The same idea in five representations** `{A17}`. *Words:* count each region's orders and rank them. *Diagram:* the black-box figure above. *Example:* `18 west`, `18 north`, `15 south`, `9 east`. *Table:* region and count columns. *Code:*

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | sort | uniq -c | sort -rn
     18 west
     18 north
     15 south
      9 east
```

**Cloze cards** `{P6}`: To group equal lines before `uniq`, run `____` first (`sort`). awk splits on a comma with `-F____` (`,`). `tail -n ____` drops a header line (`+2`).

## 5. Mechanics

**What happens when you type `a | b | c`** `{A4}`. The shell starts all three programs at once and connects a's stdout to b's stdin and b's stdout to c's stdin. Data moves in chunks, so c can print before a has finished reading a large file.

| Step | Input | Trigger | State change | Output | Assumption | Failure |
|---|---|---|---|---|---|---|
| 1 shell parses the line | the typed text | Enter | creates a plan of 3 stages | none | quotes are balanced | unbalanced quote: the shell waits for more |
| 2 shell makes the pipes | the plan | before starting programs | two kernel buffers exist | none | the system has free descriptors | "too many open files" |
| 3 shell starts the stages | the pipes | fork and exec | three processes run | none | each program exists on `PATH` | "command not found" for one stage |
| 4 a produces lines | files or a source | start | a writes into pipe 1 | lines | a can read its input | permission denied |
| 5 b transforms | pipe 1 | data present | b writes into pipe 2 | changed lines | input format as b expects | wrong delimiter gives odd output |
| 6 c prints | pipe 2 | data present | none | to the terminal | the terminal is the last stdout | a full disk or closed terminal |

```
 sequence {V9} {fig:sequence}
   shell        a              b              c           terminal
     │ start all three, wire the pipes │              │
     ├────────►│              │              │              │
     │         │ lines ─────► │ (pipe 1)     │              │
     │         │              │ lines ─────► │ (pipe 2)     │
     │         │              │              │ result ────► │
     │         │ closes output│ sees end ──► │ sees end     │
```

```
 flow {V6} {fig:flow}   (happy path and error path)
   start ─► file readable? ──yes─► stage 1 ─► stage 2 ─► stage 3 ─► answer
                 │no                  │ wrong delimiter / wrong pattern
                 ▼                    ▼
        error on stderr          [!] silent wrong answer (the dangerous path)
```

```
 data shape after each stage {V11} {fig:layout}   (input: the sales file)
   sales.csv        61 lines, 5 fields
   cut -f2          61 lines, 1 field   (header + 60 regions)
   tail -n +2       60 lines, 1 field   (header removed)
   sort             60 lines, grouped
   uniq -c          4 lines: count + value
   sort -rn         4 lines, ranked
```

```
 states of one stage {V10} {fig:states}   (state, trigger, next state)
   [waiting for input] ──data arrives──► [processing a line] ──line done──► [writing output]
          ▲                                      │                                │
          └────────────more input────────────────┘                                │
   [writing output] ──downstream is full──► [blocked]  ──downstream reads──► [writing output]
   [waiting for input] ──end of input──► [finished] (closes its output; the next stage sees the end)
```

```
 layers {V14} {fig:layers}   (what sits on what)
   you type        a | b | c
   ─────────────────────────────────────────
   the shell       parses, creates pipes, starts the programs
   the programs    cut, sort, uniq: each reads stdin, writes stdout
   the kernel      holds the pipe buffers, schedules the processes
   the files       sales.csv on disk, read in order
```

```
 file descriptors of one stage {V12} {fig:layout}
   number  name    default      in "a | b | c" for stage b
     0     stdin   keyboard     ◄── pipe from a
     1     stdout  terminal     ──► pipe to c
     2     stderr  terminal     ──► the terminal (a pipe does not carry it)
```

**The seven lenses** `{A6}`:

| Lens | Answer |
|---|---|
| What | chain small tools so each does one job |
| Why | each step is easy to check and the chain is repeatable |
| How | stdout of one stage becomes stdin of the next |
| When | any text with structure: logs, CSV, command output |
| Where | a shell on Linux, macOS or WSL |
| What if | the data is nested (JSON): use a structure-aware tool such as `jq` |
| Why not a spreadsheet | a pipeline runs on huge files, runs again unchanged and can live inside a script |

**Textbook versus production** `{V23}`: the textbook diagram shows three boxes and two arrows. Production adds buffers that can fill, a first stage that can fail without stopping the rest, a locale that changes ordering, and input that does not match the assumed format.

**Three models** `{A7}` `{A18}`. **Simplified:** "each tool reads text and writes text." **Accurate:** each tool reads a byte stream split at newlines; sorting, field splitting and comparison depend on the locale unless it is fixed. **Expert (VERIFY):** output is buffered differently on a terminal and on a pipe, a fast producer blocks when the pipe buffer is full, and a failing first stage does not stop the later stages unless `pipefail` is set.

**The tools, one sentence and one question each** `{A57}` (no step is skipped):

- `grep PATTERN file`: which lines contain this? (`-c` counts lines, `-n` numbers them, `-v` inverts, `-w` matches whole words, `-i` ignores case.)
- `cut -d, -f2 file`: what is in this column? (single-character delimiter only.)
- `sort`: put lines in order (`-n` numeric, `-r` reverse, `-k2` by field 2, `-t,` separator, `-u` drop repeats).
- `uniq -c`: how many times did this line repeat in a row?
- `awk -F, 'test {action}' file`: for each line where the test holds, do something with its fields (`$1` first field, `NR` line number, `NF` number of fields).
- `sed 's/old/new/' file`: change text on each line.
- `head -n N` and `tail -n N`: the first or last N lines (`tail -n +2` means from line 2).
- `wc -l`: count lines. `tr`: swap or delete characters.

## 6. Worked examples

Three examples, each with known, needed, principle, why it applies, solution and verification `{A10}`. Look before you transform; the data first.

```lab
$ head -3 sales.csv
date,region,item,qty,price
2026-11-01,west,date,1,6.5
2026-11-02,north,elderberry,5,9.0
```

### Example A: orders per region, ranked

*Known:* the region is field 2; the first line is a header. *Needed:* a ranked count. *Principle:* select, group, count, rank. *Why it applies:* grouping needs equal values to be neighbours, so sorting comes first.

*Socratic questions* `{A12}`: What do we know about the file? (comma-separated, header first.) What are we assuming? (every line has all five fields.) Which stage would you test first if the answer looked wrong? (the cut, by printing its first lines.) What would distinguish "the delimiter is wrong" from "the data is unsorted"? (the first shows whole lines, the second shows counts of 1.)

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | sort | uniq -c | sort -rn
     18 west
     18 north
     15 south
      9 east
```

*Verification:* the four counts add up to 60 (`wc -l` on the data minus the header).

```lab
$ tail -n +2 sales.csv | wc -l
60
```

**Trace table** `{A31}` `{V16}` `{fig:trace}` on the tiny input `west north west south west`:

| Stage | Command | Output |
|---|---|---|
| 1 | `cut -d, -f2` | `west north west south west` |
| 2 | `sort` | `north south west west west` |
| 3 | `uniq -c` | `1 north`, `1 south`, `3 west` |
| 4 | `sort -rn` | `3 west`, `1 north`, `1 south` |

**Faded copy 1** `{A9}`: *orders per item.* The item is field `__`. `cut -d, -f__ sales.csv | tail -n +2 | ____ | uniq -c | sort -rn`. Answer: field 3 and the missing stage is `sort`.

### Example B: total value per item

*Known:* quantity is field 4, price field 5. *Needed:* total of quantity times price per item. *Principle:* an associative array keeps one running total per key. *Why `awk`:* neither `cut` nor `sort` can multiply or add.

```lab
$ awk -F, 'NR>1 {t[$3]+=$4*$5} END {for (k in t) printf "%s %.2f\n", k, t[k]}' sales.csv | sort -k2 -rn
elderberry 684.00
cherry 476.00
date 357.50
apple 42.00
banana 20.50
```

*Walk it:* `NR>1` skips the header; `t[$3]` is a slot named by the item; `+=$4*$5` adds this order's value; `END` runs once after the last line and prints each slot. *Verification:* the grand total should match a second method.

```lab
$ awk -F, 'NR>1 {s+=$4*$5} END {printf "%.2f\n", s}' sales.csv
1580.00
```

**Faded copy 2:** *total quantity per region.* `awk -F, 'NR>1 {t[$__]+=$__} END {for (k in t) print k, t[k]}' sales.csv`. Answer: `$2` and `$4`.

### Example C: the same job in another representation

*Needed:* orders per region again, now as a plain-language recipe, a table and code `{A17}`. *Recipe:* take column 2, drop the header, sort, count neighbours, rank. *Table:* region and count. *Code:* one line.

```lab
$ awk -F, 'NR>1 {c[$2]++} END {for (k in c) print c[k], k}' sales.csv | sort -rn
18 west
18 north
15 south
9 east
```

*Compare to Example A:* same answer, different mechanism (no `sort` before counting, because the array groups). *Why both exist:* the first streams without holding keys; the second holds one slot per distinct value, which is fine for a few values and costly for millions.

## 7. Compare and decide

| Need | Use | Why not the others |
|---|---|---|
| Lines containing a word | `grep` | `awk` works but is longer |
| One column, no maths | `cut` | `awk` is heavier; `cut` needs a one-character delimiter |
| A numeric condition on a column | `awk` | `grep` cannot compare numbers |
| Group and count | `sort \| uniq -c` | `uniq` alone needs sorted input |
| Sum or average a column | `awk` | `cut` and `sort` cannot add |
| Replace text | `sed` | `tr` handles single characters only |

**Decision rule** `{A16}` `{V15}`: arithmetic or a numeric test means `awk`; selecting lines means `grep`; selecting columns means `cut`; grouping means `sort | uniq -c`.

```
 decision tree {V7} {fig:tree}
                  what do you need?
        ┌─────────────┼───────────────────┬──────────────────┐
   some lines     some columns      a number computed     replaced text
        │              │                   │                   │
      grep       cut -d X -f N          awk (sum, test)       sed
        │              │
   then count?    then group and count?
     grep -c       sort | uniq -c
```

**Trade-offs** `{A24}` `{A40}`:

| Option | Gain | Lose | Worth it when |
|---|---|---|---|
| `sort \| uniq -c` | streams, simple, familiar | sorts everything first | many distinct values |
| `awk` array | one pass, no sort | holds every key in memory | few distinct values |
| a spreadsheet | visual, friendly | does not scale, not repeatable | one-off small data |
| a scripting language | full power, tests | more to write | the job will be reused |

**Stand on the shoulders of giants** `{A39}`: for CSV with quoted commas use `csvkit` or Python's `csv` module; for JSON use `jq`; for big structured data use a database. The shell tools here are for line-oriented text.

**Labels** `{A27}`: "look at the head of the file first" is a **best practice**; "set `LC_ALL=C` in scripts for repeatable order" is a **rule of thumb**; "quote a delimiter that the shell treats specially" is a **requirement**; "use `awk` for everything" is a **preference**; "use `grep -c` when the file is huge" is **context-dependent**.

**Assumptions** `{A41}`: the examples assume one record per line, no quoted commas, and a single header line. If the data has quoted commas (see the adversarial lab), field numbers shift and the answer changes: the conclusion holds only while the assumptions hold.
