# Part 2 of 5: Do it, repair it, break it

## 8. Do it: four labs, guided to adversarial

**Environment for all labs** `{P7}`. A Linux shell or WSL. Create the data with `python depth/data/make_sample.py DIR` and `cd DIR`; it writes `sales.csv` (60 orders), `access.log` and `messy.csv`. **Cleanup** (every lab): leave the directory and delete it; nothing else is changed. **Safety:** every command reads files and prints; none writes outside the directory. The progression is guided (exact steps), prompted (goals and hints), unassisted (specifications only) and adversarial (the data fights back) `{P3}`.

### Lab A: guided (every step given)

**Objective.** Answer four questions about `sales.csv`.

**Task A1: how many lines mention the north region?** *Why:* `grep -c` counts matching lines; commas around the word stop it matching inside other fields. *Expected:* a single number.

```lab
$ grep -c ,north, sales.csv
18
```

- Hint 1: you need a count, not the lines.
- Hint 2: look at the `-c` option of `grep`.
- Hint 3: `grep -c ____ sales.csv` with the pattern `,north,`.
- Hint 4: `grep -c ,north, sales.csv`; the commas keep it from matching other fields.

**Task A2: total value per item, biggest first.** *Why:* a total of quantity times price needs arithmetic, so `awk`; an array keeps one total per item.

```lab
$ awk -F, 'NR>1 {t[$3]+=$4*$5} END {for (k in t) printf "%s %.2f\n", k, t[k]}' sales.csv | sort -k2 -rn
elderberry 684.00
cherry 476.00
date 357.50
apple 42.00
banana 20.50
```

- Hint 1: you need to multiply two columns, so `cut` is not enough.
- Hint 2: awk can keep an array indexed by item name.
- Hint 3: `NR>1 {t[$3]+=$4*$5}` adds each line; an `END` block prints the array.
- Hint 4: pipe the awk output to `sort -k2 -rn` to rank by the second field as a number.

**Task A3: how many orders have a quantity of 10 or more?** *Why:* a numeric condition is an awk pattern; `wc -l` counts what survives.

```lab
$ awk -F, 'NR>1 && $4>=10' sales.csv | wc -l
16
```

- Hint 1: you need a numeric comparison on column 4.
- Hint 2: an awk pattern without an action prints the matching line.
- Hint 3: `NR>1 && $4>=10` skips the header and tests the quantity.
- Hint 4: pipe to `wc -l`.

**Task A4: the three biggest quantities.** *Why:* numeric reverse sort on column 4, keep three lines; with `LC_ALL=C` ties are ordered the same way every run.

```lab
$ tail -n +2 sales.csv | sort -t, -k4 -rn | head -3
2026-11-26,south,date,12,6.5
2026-11-19,west,apple,12,0.5
2026-11-13,west,apple,12,0.5
```

- Hint 1: you need numeric order on one column of a comma-separated file.
- Hint 2: `sort` needs the separator set with `-t`.
- Hint 3: `sort -t, -k4 -rn`.
- Hint 4: remove the header with `tail -n +2`, sort, then `head -3`.

**Verification.** Compare each output with the line under its block. **Stretch.** Total quantity per region (change the key and the sum in A2).

**Every command explained** `{A29}`:

| Command | Arguments and flags | Reads / writes | Privileges | Output | Side effects and risks |
|---|---|---|---|---|---|
| `grep -c ,north, sales.csv` | `-c` count; pattern `,north,`; file | reads the file | none | one number | none; an unquoted special character can be seen by the shell |
| `awk -F, '...' sales.csv` | `-F,` field separator; program in quotes | reads the file | none | the printed lines | none; the quotes keep `$` and `{}` away from the shell |
| `sort -t, -k4 -rn` | `-t,` separator; `-k4` key; `-r` reverse; `-n` numeric | reads stdin | none | ordered lines | uses memory for large input; locale changes ties |
| `tail -n +2` | start at line 2 | reads stdin | none | everything after line 1 | drops a data line if there is no header |

### Lab B: prompted (goals and hints, no commands)

Use `sales.csv`. For each goal write the pipeline, run it, and say how you checked it.

1. **Goal:** orders per item, ranked. *Hint:* the item is column 3; group before counting.
2. **Goal:** the most valuable single order (quantity times price). *Hint:* awk can compute per line; sort the computed value.
3. **Goal:** the number of distinct items. *Hint:* select a column, remove duplicates, count lines.

Reference answers (try first):

```lab
$ cut -d, -f3 sales.csv | tail -n +2 | sort | uniq -c | sort -rn
     18 cherry
     12 elderberry
     11 banana
     11 apple
      8 date
$ awk -F, 'NR>1 {print $4*$5, $0}' sales.csv | sort -rn | head -1
99 2026-11-07,north,elderberry,11,9.0
$ cut -d, -f3 sales.csv | tail -n +2 | sort -u | wc -l
5
```

- Hint 1 (all three): write the stages as English first, then pick one tool for each.
- Hint 2: a count of a grouped column is `sort | uniq -c`; a count of distinct values is `sort -u | wc -l`.
- Hint 3: the second goal needs the line printed beside the computed value so you can read the order.
- Hint 4: the reference answers above.

### Lab C: unassisted (specifications only)

Write, run and verify (no hints; the ladders below are closed on purpose, open one tier at a time only if you are stuck): (1) the average quantity per order; (2) orders per day, busiest first; (3) every order whose price is above 5, sorted by date. A correct solution states how it was verified: for example, a second method for the same number `{P4}`. First look at the data with a reconnaissance step `{V24}`: print the first lines and the field count before you write anything.

**Goal 1, ladder:**

- Hint 1: an average is a total divided by a count.
- Hint 2: awk can keep a total and use `NR` for the count.
- Hint 3: `NR>1 {s+=$4} END {print s/(NR-1)}`.
- Hint 4: `awk -F, 'NR>1 {s+=$4} END {print s/(NR-1)}' sales.csv`.

**Goal 2, ladder:**

- Hint 1: the date is field 1; group like orders per region.
- Hint 2: select, sort, count neighbours, rank.
- Hint 3: `cut -d, -f1 sales.csv | tail -n +2 | sort | ____ | sort -rn`.
- Hint 4: `cut -d, -f1 sales.csv | tail -n +2 | sort | uniq -c | sort -rn | head`.

**Goal 3, ladder:**

- Hint 1: a numeric condition on field 5 is an awk pattern.
- Hint 2: keep the header out with `NR>1`.
- Hint 3: `awk -F, 'NR>1 && $5>5' sales.csv | sort ...` ordered by field 1.
- Hint 4: `awk -F, 'NR>1 && $5>5' sales.csv | sort -t, -k1`.

### Lab D: adversarial (the data fights back)

`messy.csv` has a blank line, a repeated header, mixed case (`North`), a leading space (` south`), a quoted field containing a comma, and an empty quantity. **Objective:** find each problem with a command, then say what it would have done to a naive count.

```lab
$ cat messy.csv
date,region,item,qty,price
2026-11-01,north,apple,3,0.5
2026-11-01,North,apple,2,0.5
2026-11-02, south,banana,4,0.25

date,region,item,qty,price
2026-11-03,east,"cherry, dark",1,4.0
2026-11-03,west,date,5,6.5
2026-11-04,west,date,,6.5
2026-11-04,north,apple,10,0.5
$ grep -n '^$' messy.csv
5:
$ grep -c '^date' messy.csv
2
$ cut -d, -f2 messy.csv | sort | uniq -c
      1 
      1  south
      1 North
      1 east
      2 north
      2 region
      2 west
$ awk -F, 'NF!=5 {print NR": "$0}' messy.csv
5: 
7: 2026-11-03,east,"cherry, dark",1,4.0
$ awk -F, 'NR>1 && $4=="" {print NR": empty quantity"}' messy.csv
5: empty quantity
9: empty quantity
```

- Hint 1: a wrong count usually means some line does not look like the others.
- Hint 2: print the line number beside the oddity with `grep -n` or `awk` and `NR`.
- Hint 3: compare the number of fields per line with the expected 5 (`NF`).
- Hint 4: the six commands above find all six problems; the field-count test finds both the blank line and the quoted comma.

**Stretch:** clean the file in a pipeline (drop blank and repeated header lines, lower-case the region, trim the space) and count orders per region.

```lab
$ grep -v '^$' messy.csv | grep -v '^date' | tr 'A-Z' 'a-z' | sed 's/, */,/g' | cut -d, -f2 | sort | uniq -c
      1 east
      3 north
      1 south
      2 west
```

*Expected result and a caution:* the quoted comma row still has a shifted field, so a field-based count is wrong for that row; this is the assumption stated in section 7 failing, and the signal to reach for a CSV-aware tool.

## 9. Repair: common mistakes and wrong models

| Mistake | What breaks | Instead | Error class `{A14}` |
|---|---|---|---|
| `uniq -c` without `sort` | counts of 1 for scattered repeats | `sort \| uniq -c` | conceptual |
| `sort` on numbers without `-n` | `10` before `9` | `sort -n` | factual |
| `cut -d' '` on text with runs of spaces | empty fields | `awk '{print $2}'` splits on runs | procedural |
| forgetting the header | the word "region" is counted | `tail -n +2` or `NR>1` | procedural |
| `grep north` | also matches `northeast` | `,north,` or `-w` | logical |
| `cat file \| grep x` | works, with a needless process | `grep x file` | strategy |
| `awk -F ,` after the program | the delimiter is ignored | options before the program | procedural |
| trusting the first answer | a wrong stage hides | check each stage and one independent number | assumption |

**Misconception 1** `{A15}` `{V30}`: "`uniq` removes duplicates." *Why reasonable:* the name suggests it. *Where it breaks:* it only joins adjacent equal lines. *Test:* `printf 'b\na\nb\n' | uniq` still prints three lines.

```
 before / after {V30} {fig:diff}
   BEFORE (broken model)                       AFTER (accurate model)
   "uniq removes duplicates everywhere"        "uniq joins neighbouring equal lines"
   input  b a b  ─► uniq ─► b a b  [!]         input  a b b  ─► uniq -c ─► 1 a  2 b
          fault: the two b are not neighbours         fix: sort first so equal lines touch
```

**Misconception 2:** "A pipeline reads the whole file before it starts." *Why reasonable:* a spreadsheet does. *Where it breaks:* stages stream. *Test:* `yes | head -3` stops at once although `yes` never ends.

**Misconception 3:** "`grep -c` counts matches." *Why reasonable:* "count" suggests matches. *Where it breaks:* it counts lines. *Test:* a line containing the pattern twice is counted once.

## 10. Break it

### Failure case 1: every count is 1

*Symptom:* each line of the counted output starts with 1. *Hypotheses* `{A22}`:

| Hypothesis | Evidence for | Evidence against | Most informative test | Result |
|---|---|---|---|---|
| (a) input not sorted | the same value appears again later | none | add `sort` before `uniq -c` | counts become 18, 18, 15, 9 |
| (b) wrong delimiter | each line is a whole row | output shows one region name per line | look at the first lines after the cut | one column: not this |
| (c) carriage returns | `west` and `west^M` look alike | the output is clean | `cat -A` | not present |

*Symptom reproduced:*

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | uniq -c | head -4
      1 west
      1 north
      1 south
      1 north
```

*Root cause:* unsorted input. *Smallest fix:* insert `sort`. *Same cause elsewhere:* any `uniq` after a column cut. *Prevention* `{A32}`: build the pipeline one stage at a time and read each stage's output.

### Failure case 2: the total is too high

*Symptom:* a "north" total is larger than the count of north orders.

| Hypothesis | Evidence for | Evidence against | Test | Result |
|---|---|---|---|---|
| (a) pattern too loose | other fields contain the text | none | anchor the pattern with commas | totals match |
| (b) summing quantity not orders | the stage printed quantities | none | `wc -l` versus the sum | the sum differs by design |

### Failure case 3: the answer changes between machines

*Symptom:* the ranking of tied values differs. *Cause:* locale-dependent ordering. *Test:* run with `LC_ALL=C`. *Fix:* set the locale in scripts. *Evidence label:* this is an **observed** behaviour on some systems; the exact rule is **VERIFY**.

**Break-fix lab 1 (symptom only)** `{P8}`: a teammate's pipeline `grep north sales.csv | cut -d, -f4 | sort | uniq -c` prints counts that are higher than `grep -c ,north, sales.csv`. Find two causes before reading on. *Debrief:* the loose pattern can match inside other fields, and the pipeline counts quantity values, not orders. *Prevention:* anchor patterns and write down what each stage should produce.

**Break-fix lab 2 (symptom only):** `awk -F, '{s+=$4} END {print s}' sales.csv` prints a total, but it is not the same as `awk -F, 'NR>1 {s+=$4} END {print s}' sales.csv`. *Debrief:* the header's text counts as 0 in the first and is skipped in the second; here the sums agree, which hides the bug. Change the header to a number and the first becomes wrong: *a correct answer does not prove a correct method*.

**Debugging checklist** `{A32}`: (1) state the expected output; (2) read the actual output; (3) find the first stage whose output differs from what you expect; (4) form two or three hypotheses; (5) choose the test that separates them; (6) fix the smallest thing; (7) check the same cause elsewhere; (8) add a guard (a second method or a count check).

```
 diagnostic decision tree {V25} {fig:tree}
              wrong answer
        ┌────────┴───────────┐
   output has odd lines   output is clean but wrong
        │                      │
   inspect after stage 1   compare with an independent method
        │                      │
   delimiter? header?      pattern too loose? wrong column?
   blank line?              header counted? locale?
```

```
 failure map {fig:failure}
   normal:   pattern ─► fields ─► group ─► count ─► ranking correct
   fault:    pattern too loose                  [!] extra lines enter the pipeline
   symptom:  totals higher than expected
   blast:    every later stage is correct but the answer is wrong
   mitigate: anchor the pattern; reconcile with `grep -c`
```
