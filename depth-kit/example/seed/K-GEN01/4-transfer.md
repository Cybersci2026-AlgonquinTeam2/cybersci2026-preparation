# Part 4 of 5: Zoom out, transfer and teach back

## 11. Zoom out

**The ecosystem-to-function ladder** `{A4}` `{V22}`. Zoom from the biggest view to the smallest:

| Level | In this topic |
|---|---|
| Ecosystem | the Unix toolbox: small programs, text as the shared format, the shell as the glue |
| System | a shell session running a pipeline of processes connected by kernel buffers |
| Subsystem | one stage and the two streams it reads and writes |
| Component | the program's option parser and its line-reading loop |
| Function | one comparison: "is this line equal to the previous one?" (`uniq`) |

```
 systems figure {V8} {V22} {V27} {fig:zones}   (zones, protocol on each link, [!] = bottleneck or trust boundary)
   ┌────────────── your shell (trusted: you typed it) ───────────────┐
   │   file ──bytes──► [cut] ──lines──► [sort] [!] ──lines──► [uniq -c] ──► [head] ──► terminal │
   └─────────────────────────────────────────────────────────────────┘
        ▲
        ┊  - - - trust boundary - - -  the file's CONTENT is untrusted data
        ┊  (never paste it into a command line or run bash on it)
```

**Feedback and bottlenecks** `{A23}`. If `cut` gets faster, does the system? Only until `sort` dominates: `sort` must hold the input before printing, so it is the bottleneck. Improving a non-bottleneck stage barely changes the total.

**Performance loop** `{A35}` `{V28}`: make it correct first; make it observable (`time`, `wc -l` between stages); take a baseline; find the bottleneck; change one thing (filter earlier, fix the locale, avoid sorting twice); measure again.

**Security notes** `{A34}`: treat file content as data, never as code; quote every variable; avoid `eval` and `bash -c` on text from outside; do not put secrets on a command line (other users can see process lists); run destructive commands only in a throwaway directory.

**Architecture view** `{A28}`: *purpose* turn text into answers; *components* programs and pipes; *interfaces* text lines and exit codes; *data flow* left to right; *control flow* the shell starts all stages; *state* none between runs; *trust boundary* file content versus command text; *failure* silent wrong answers; *scaling* streaming until a sort; *operations* put proven pipelines in scripts with tests.

**Novice versus expert** `{A26}`:

| Situation | Novice | Expert |
|---|---|---|
| wrong count | rewrites the whole line | prints each stage's output and finds the first bad one |
| big file | waits | filters early and measures |
| awkward data | forces `cut` to work | switches to a CSV-aware tool |
| a number looks right | accepts it | reconciles with a second method |

**Tacit knowledge** `{A27}`: *rule of thumb:* read the first 10 lines before anything else; *preference:* many people write `awk` for counts; *context-dependent:* `LC_ALL=C` helps repeatability but changes how accented text sorts.

**Evidence tags** `{A42}` `{V32}`: *fact* (run in the labs): `sort | uniq -c` groups; *observed:* ties order differently across locales; *inference:* the sort stage dominates on large input; *assumption:* one record per line; *estimate:* none given for speed; *VERIFY:* buffering behaviour differs on terminals.

## 13. Transfer and design

### Four levels of transfer `{A21}`

| Level | Problem | Answer to check against |
|---|---|---|
| Near | count orders per day in `sales.csv` | change only the field number (field 1) |
| Representation | present the item totals as a table in a spreadsheet; say what a pivot does for you that the pipeline did by hand | the pivot groups and sums; the pipeline did it with `awk` and `sort` |
| Context | a web log has the status code in field 9: list the codes by frequency | `awk '{print $9}' access.log \| sort \| uniq -c \| sort -rn` |
| Far | rank the words in a book, and the processes using the most memory | same pattern: select, group, count, rank |

```lab
$ awk '{print $9}' access.log | sort | uniq -c | sort -rn
     77 200
     72 401
     57 403
     27 301
     25 404
     24 500
     18 304
```

### Critique `{A46}` `{P15}`

Review this teammate's line like a senior engineer: `cat sales.csv | grep west | cut -d, -f4 | sort | uniq`. *Findings to reach:* a needless `cat`; the pattern can match other fields; `uniq` without `-c` hides how often each quantity appears; the header goes through the first stage; the intent is not stated. *Corrected:* anchor the pattern, count with `-c`, name the goal in a comment.

### Reconstruction `{A47}`

Given only "which item is ordered with the largest single quantity?", derive the pipeline from first principles: the quantity is field 4, so sort by field 4 numerically in reverse, take the first line, print the item field.

```lab
$ tail -n +2 sales.csv | sort -t, -k4 -rn | head -1 | cut -d, -f3
date
```

### Design kata with a constraint shift `{A48}` `{P13}`

*Design* a one-line report of orders per region. *Shift 1:* the file is 100 times bigger: which stage is the bottleneck and what do you change (filter early, fix the locale, avoid sorting twice)? *Shift 2:* the file is still being written: what breaks (you read a snapshot; a partial last line can mislead). *Shift 3:* the data now contains quoted commas: what changes (the field-based approach is wrong; use a CSV-aware tool). *Write down* which assumptions each shift breaks `{A41}`. Then choose between two candidate designs with a trade-off matrix `{V26}` `{fig:matrix}`:

```
 trade-off matrix {V26}        sort|uniq -c      awk array        scripting language
   speed on 100x data          medium [!] sort   fast, needs RAM  fast
   memory                      low (streams)     high if many keys medium
   handles quoted commas       no                no               yes (csv module)
   effort to write             low               low              medium
   chosen when                 many distinct     few distinct     the report will be reused
```

### Capstone project `{P14}`

**Spec.** Build a small report script `report.sh` that, given `sales.csv`, prints (1) orders per region ranked, (2) value per item ranked, (3) the three largest orders, and (4) a reconciliation line showing the grand total computed two ways.

**Non-goals.** Handling quoted commas; reading from a network; a graphical interface.

**Milestones.** (1) each of the four outputs as a separate pipeline; (2) one script that prints them with headings; (3) a header check that stops with a message if the first line is not the expected header; (4) a test that compares the output with saved expected output; (5) a note listing assumptions.

**Acceptance tests.** The four sections appear in order; the two totals match; running on `messy.csv` stops at the header check or reports the problem; the script prints nothing to stderr on good data.

**Self-review rubric** `{A44}`:

| Criterion | Question |
|---|---|
| Correctness | does each number match an independent method? |
| Edge cases | what happens on `messy.csv`? |
| Security | is any file content used as code? |
| Readability | could a teammate follow it without you? |
| Documentation | are the assumptions written down? |

## 14. Teach back and check yourself

### Explain to three audiences `{A49}` `{P15}`

Each in under a minute, then compare with the model answer and score yourself with the rubric.

| Audience | Model answer |
|---|---|
| Beginner | "One program hands its output to the next, like plates along a counter. We pick the column, group equal values, count them and rank them." |
| Practitioner | "Stages are processes joined by pipes. Filter early, sort late, set `LC_ALL=C` for repeatable order, and reconcile the result with a second method." |
| Expert | "Each stage buffers; `sort` needs all input; a failing stage does not stop the others unless `pipefail` is set; field-based tools mis-parse quoted CSV, so choose the right parser." |

*Rubric:* uses the right term without jargon for the beginner (2 points); names one trade-off for the practitioner (2); states one failure mode for the expert (2); gives an example for each (2); 8 of 8 means ready to teach.

### Metacognition ladder `{A50}`

Seen is not recognised, recognised is not remembered, remembered is not understood, understood is not applied. For this topic, mark each as seen, recognised, recalled, understood or applied: the pipe; `uniq` needing sorted input; `awk` arrays; the header trap; locale; the bottleneck.

### The eleven mastery checks, each with a task `{A51}`

| Level | Task |
|---|---|
| 1 Define | write one sentence defining a pipe and one defining a field |
| 2 Explain | explain why `uniq -c` needs sorted input, with the `printf` example |
| 3 Demonstrate | run the region-count pipeline and read each stage's output |
| 4 Apply | count orders per item with a pipeline of your own |
| 5 Distinguish | for five given questions, name the right tool and say why not the others |
| 6 Analyse | take a pipeline that gives all 1s and say which stage is wrong and why |
| 7 Troubleshoot | fix break-fix lab 1 with a written hypothesis table |
| 8 Evaluate | compare the `awk` array and `sort \| uniq -c` for a file with a million distinct keys |
| 9 Design | design the capstone report and name the assumptions |
| 10 Transfer | apply the pattern to `access.log` without help |
| 11 Teach | teach the pipeline to a beginner and answer one question from them |

```lab
$ awk '{print $9}' access.log | sort | uniq -c | sort -rn | head -3
     77 200
     72 401
     57 403
```

### Independence checklist `{A59}` `{A60}`

On an unfamiliar file, can you: (1) look at the first 10 lines; (2) state the format and delimiter; (3) state the question in one sentence; (4) pick the stage list; (5) build it one stage at a time; (6) read every stage's output; (7) anchor any pattern; (8) handle the header; (9) fix the locale; (10) reconcile with a second method; (11) note the assumptions; (12) write a test; (13) say when the shell tools are the wrong tool; (14) explain the result to someone else. The goal of the topic is that you need this page less over time: the capstone on a new file, done unaided, is the proof.
