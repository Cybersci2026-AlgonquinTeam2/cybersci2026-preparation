# Part 3 of 5: Retrieve and discriminate

## 12. Retrieve and discriminate

Retrieval comes within 24 hours of part 1 and again on the schedule at the end of this part. Answer from memory first, then check `{A11}` `{A20}`.

### Micro-drills (ten, easy to tricky) `{P9}`

Graded for correctness, safety and idiom. Answers follow each item.

1. **Drill** Print only the third field of colon-separated lines. *Answer:* `cut -d: -f3`.
2. **Drill** Count lines that contain `error` in `app.log`. *Answer:* `grep -c error app.log`.
3. **Drill** Sort the lines of `n.txt` as numbers, largest first. *Answer:* `sort -rn n.txt`.
4. **Drill** Show each distinct line of `names.txt` once. *Answer:* `sort -u names.txt`.
5. **Drill** Print the second field of lines whose first field is `GET`. *Answer:* `awk '$1=="GET" {print $2}'`.
6. **Drill** Add up the numbers in column 4 of a CSV that has a header. *Answer:* `awk -F, 'NR>1 {s+=$4} END {print s}'`.
7. **Drill** List the five most frequent values of column 2 (comma-separated, header present). *Answer:* `cut -d, -f2 f | tail -n +2 | sort | uniq -c | sort -rn | head -5`.
8. **Drill** Print lines 10 to 20 of a file. *Answer:* `sed -n '10,20p' file` (idiom) or `head -20 file | tail -11`.
9. **Drill** Count the distinct values of column 3. *Answer:* `cut -d, -f3 f | tail -n +2 | sort -u | wc -l`.
10. **Drill** Print each line of a CSV whose quantity (field 4) is at least 10, with the line number. *Answer:* `awk -F, 'NR>1 && $4>=10 {print NR": "$0}' f`. *Grading note:* a solution that forgets `NR>1` is correct on the data but wrong on the header.

### Trace drills (predict the output) `{P10}` `{V16}`

1. **Trace** `printf 'b\na\nb\n' | sort | uniq -c`. *Answer:* `1 a` then `2 b` (counts right-aligned).
2. **Trace** `printf 'b\na\nb\n' | uniq -c`. *Answer:* `1 b`, `1 a`, `1 b`.
3. **Trace** `printf '10\n9\n100\n' | sort`. *Answer:* `10`, `100`, `9`.
4. **Trace** `printf '10\n9\n100\n' | sort -n`. *Answer:* `9`, `10`, `100`.
5. **Trace** `printf 'a,1\nb,2\n' | awk -F, '{s+=$2} END {print s}'`. *Answer:* `3`.

### Spot the bug (three items) `{V31}`

1. **Spot the bug** `cut -d, -f2 sales.csv | uniq -c | sort -rn`: why are the counts all 1 and what is the fix? *Answer:* the input is not sorted; insert `sort` before `uniq -c`.
2. **Spot the bug** `awk -F, '{s+=$4*$5} END {print s}' sales.csv`: when is the answer misleading? *Answer:* the header line is included; with a text header it contributes 0 so the number looks right, but the method is wrong.
3. **Spot the bug** `grep -c north sales.csv` used to count north-region orders: what could go wrong? *Answer:* `north` can appear in other fields (an item named `northern`), so the count may be too high; anchor with commas.

**Fill in the node** `{V31}` `{fig:flow}`: complete the box.

```
   file ─► [ cut -d, -f2 ] ─► [ ??? ] ─► [ uniq -c ] ─► [ sort -rn ] ─► ranked counts
```

*Answer:* `sort`, because `uniq -c` needs equal lines to be neighbours.

### Diagnostic quiz (ten questions) `{P11}`

Choose, then read why each option is right or wrong.

**Q1.** A pipeline `cut -d, -f2 f | uniq -c` gives many lines with count 1. The most likely fix is:
  - (A) Add `sort` before `uniq` — right: `uniq` only merges neighbours, so scattered repeats stay separate until the input is sorted.
  - (B) Add `-r` to `cut` — wrong: `cut` has no option that groups values, so nothing changes.
  - (C) Replace `uniq -c` with `wc -l` — wrong: that counts all lines instead of repeats per value.
  - (D) Use `grep -c` instead — wrong: it counts matching lines in total and does not group values.

**Q2.** Which tool adds up a numeric column?
  - (A) `cut` — wrong: it extracts fields and cannot do arithmetic.
  - (B) `sort` — wrong: it orders lines and never adds them.
  - (C) `awk` — right: an action such as `s+=$4` accumulates a total across lines.
  - (D) `uniq` — wrong: it counts repeated lines and does not sum field values.

**Q3.** `sort` prints `10` before `9`. Why?
  - (A) The file is corrupted — wrong: the data is fine; the ordering rule is the cause.
  - (B) Plain `sort` compares characters — right: the character `1` comes before `9`, so `-n` is needed for numeric order.
  - (C) `sort` is reversed by default — wrong: the default is ascending, by character.
  - (D) The locale is broken — wrong: even a correct locale compares text unless told otherwise.

**Q4.** `grep north sales.csv` returns more lines than expected. Why?
  - (A) It matches inside longer words — right: without anchors it matches any occurrence of the letters.
  - (B) It also searches other files — wrong: it reads only the file named.
  - (C) It ignores the header — wrong: it treats every line the same.
  - (D) It counts bytes — wrong: matching is by lines of text.

**Q5.** What does the pipe in `a | b` pass from `a` to `b`?
  - (A) The exit status — wrong: that is separate and not data flowing through the pipe.
  - (B) The standard output of `a` as the standard input of `b` — right: that is the whole mechanism.
  - (C) The files `a` opened — wrong: open files are not handed over, only the byte stream.
  - (D) The environment variables of `a` — wrong: a child process may inherit them, but the pipe does not carry them.

**Q6.** You need the total of column 4 where column 2 is `west`. Which fits best?
  - (A) `grep west f | cut -f4` — wrong: it prints values and does not add them.
  - (B) `awk -F, '$2=="west" {s+=$4} END {print s}' f` — right: a test on one field and a running total are what awk is for.
  - (C) `sort f | uniq -c` — wrong: it counts repeated lines and ignores column 4.
  - (D) `wc -l f` — wrong: it counts lines, not a sum.

**Q7.** Why set `LC_ALL=C` in a script?
  - (A) It makes commands faster only — wrong: speed can change, but the point is repeatable ordering.
  - (B) It makes sorting and comparison depend on bytes, not the user's language settings — right: so the same input gives the same order on every machine.
  - (C) It hides error messages — wrong: it does not change what is printed to stderr.
  - (D) It turns on colour output — wrong: colour is a separate option.

**Q8.** Which stage is the bottleneck on a very large file?
  - (A) `cut` — wrong: it works line by line and streams.
  - (B) `sort` — right: it must see all input before it can print the first line.
  - (C) `head` — wrong: it stops early and often shortens the work.
  - (D) `tr` — wrong: it transforms characters as they arrive.

**Q9.** A count looks right but the method is `awk -F, '{s+=$4} END {print s}'` with a text header. What is the risk?
  - (A) None, the answer is correct — wrong: it is correct by luck, since text counts as 0.
  - (B) The method is unsound and fails if the header ever becomes numeric — right: a correct answer does not prove a correct method.
  - (C) awk crashes — wrong: it converts text to 0 and continues.
  - (D) The total doubles — wrong: nothing is counted twice.

**Q10.** `grep -c` on a line containing the pattern twice counts it:
  - (A) twice — wrong: `-c` counts lines, not matches.
  - (B) once — right: the line matches, so it adds 1.
  - (C) zero times — wrong: a matching line is counted.
  - (D) as an error — wrong: repeats are not an error.

### Flashcards (thirty, five types) `{P6}`

Concept (easy to medium):

- [concept][easy] Front: What does `|` do? Back: connects the stdout of the left program to the stdin of the right program.
- [concept][easy] Front: What does `cut -d, -f2` print? Back: the second comma-separated field of each line.
- [concept][medium] Front: What does `uniq -c` count? Back: how many times a line repeats consecutively.
- [concept][medium] Front: What does `grep -c` print? Back: the number of matching lines.
- [concept][easy] Front: What does `wc -l` count? Back: lines.
- [concept][medium] Front: What is a field? Back: a piece of a line between delimiters.
- [concept][medium] Front: What does `NR` hold in awk? Back: the current line number.

Cloze:

- [cloze][easy] Front: To group equal lines before `uniq`, run `____` first. Back: `sort`.
- [cloze][medium] Front: awk splits on a comma with `-F____`. Back: `-F,`.
- [cloze][easy] Front: `sort ____` orders numbers correctly. Back: `-n`.
- [cloze][medium] Front: `tail -n ____` prints from line 2 onward and drops a header. Back: `+2`.
- [cloze][medium] Front: `awk 'NR____1'` skips the header line. Back: `>`.
- [cloze][trap] Front: `grep ____` inverts the match and shows non-matching lines. Back: `-v`.

Scenario or decision:

- [scenario][medium] Front: A log has 100 000 lines; you want the five most frequent values in column 3. Pipeline? Back: `cut -f3 file | sort | uniq -c | sort -rn | head -5`.
- [scenario][trap] Front: You get a count of 1 for every value. First check? Back: whether the input is sorted before `uniq`.
- [scenario][medium] Front: You need the total of column 4 where column 2 is `west`. Tool? Back: `awk -F, '$2=="west" {s+=$4} END {print s}'`.
- [scenario][medium] Front: A CSV has quoted commas. What should you use? Back: a CSV-aware tool, since `cut` and `awk -F,` split inside the quotes.
- [scenario][trap] Front: A total matches by luck. What do you do? Back: verify with a second, independent method.
- [scenario][easy] Front: You want only the lines with `404`. Tool? Back: `grep`.

Contrast:

- [contrast][medium] Front: `cut` versus `awk` for fields? Back: `cut` is simple with a one-character delimiter; `awk` handles runs of spaces, conditions and arithmetic.
- [contrast][trap] Front: `sort -u` versus `sort | uniq`? Back: both give distinct lines; only `uniq -c` also counts.
- [contrast][medium] Front: `grep -c` versus `grep | wc -l`? Back: the same count for ordinary use; `-c` is shorter and runs one process.
- [contrast][medium] Front: awk array versus `sort | uniq -c`? Back: the array groups in one pass and holds all keys; sort streams but sorts everything.
- [contrast][trap] Front: `head -n 5` versus `tail -n +5`? Back: the first five lines versus everything from line 5 on.

Trace:

- [trace][medium] Front: Output of `printf 'b\na\nb\n' | sort | uniq -c`? Back: `1 a` then `2 b`.
- [trace][trap] Front: Output of `printf 'b\na\nb\n' | uniq -c`? Back: `1 b`, `1 a`, `1 b`.
- [trace][medium] Front: Output of `printf '10\n9\n' | sort`? Back: `10` then `9`.
- [trace][medium] Front: Output of `printf 'a,1\nb,2\n' | cut -d, -f2`? Back: `1` then `2`.
- [trace][trap] Front: Output of `printf 'x\nx\n' | uniq -c`? Back: `2 x`.
- [trace][easy] Front: Output of `printf 'a\nb\n' | wc -l`? Back: `2`.

### Interleaved set (twelve unlabelled items) `{A19}` `{P17}`

No labels say which topic each belongs to: decide which concept applies, and why not the others. Items mix this topic with earlier ones (files and paths, permissions, searching).

1. Count the lines in a file. *Answer:* `wc -l`; not `grep` (it needs a pattern).
2. List files whose name ends in `.log` below the current directory. *Answer:* `find . -name '*.log'`; not `ls` (it does not recurse by default).
3. Show lines that do not contain `404`. *Answer:* `grep -v 404`.
4. Make a script runnable by its owner. *Answer:* `chmod u+x script`.
5. The ten largest numbers in a column. *Answer:* `sort -rn | head -10` after selecting the column.
6. Replace `foo` with `bar` on every line. *Answer:* `sed 's/foo/bar/g'`.
7. Print the last line of a file. *Answer:* `tail -n 1`.
8. Find which value repeats most often in column 2. *Answer:* `cut -d, -f2 | sort | uniq -c | sort -rn | head -1`.
9. Show the type of an unknown file. *Answer:* `file name`.
10. Print the sum of column 3. *Answer:* `awk '{s+=$3} END {print s}'`.
11. Search for the word `root` in every file in a directory. *Answer:* `grep -r root dir`.
12. Print the line number of each match of `error`. *Answer:* `grep -n error file`.

### Spaced review schedule `{A20}` `{P17}`

| When | What | Evidence |
|---|---|---|
| day 0 (within 24 h) | this whole part, from memory first | quiz at 8 of 10 |
| day 1 | cards marked trap or medium; trace drills | cards correct |
| day 3 | micro-drills 5 to 10 without looking | all correct |
| day 7 | interleaved set plus one new pipeline from a fresh question | explained out loud |
| day 14 | Lab C goals again, no hints | verified by a second method |
| day 30 | adversarial lab again on a new messy file | problems found without notes |

The standard lists intervals of 1, 3, 7, 14 and 30 days while the aids catalog says 1, 3, 7 and 21; this table follows the standard until the tracker is rebuilt.

### Error-to-aid pipeline `{P5}` `{A14}`

When you miss an item, copy it into this template and add it to your deck:

| Field | Fill in |
|---|---|
| What I did | the command or answer I gave |
| What happened | the output I saw |
| Error class | factual, conceptual, procedural, logical, assumption or strategy |
| Why it seemed plausible | the belief behind it |
| Corrected model | one sentence |
| New card | a Front and Back that would have caught it |

*Example:* *I ran `cut -d, -f2 f | uniq -c` and got all 1s. Conceptual: I thought uniq removes duplicates. Plausible because the name says unique. Corrected: it joins adjacent equal lines. New card: Front "What must be true of the input for `uniq -c` to group?" Back "equal lines are adjacent (sorted)".*
