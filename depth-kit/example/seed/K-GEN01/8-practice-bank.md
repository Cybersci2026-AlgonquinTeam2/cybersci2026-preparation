# Extension C: the practice bank

More retrieval for the same topic: the items in part 3 are the first pass, these are the second and third. Use them on the days in the spaced schedule `{A20}`. Match the aid to the goal `{P1}`:

| Goal | Aid to use | Where |
|---|---|---|
| remember a flag or definition | flashcards | cards below and part 3 |
| build fluency with commands | micro-drills, timed | drills below |
| predict what a command does | trace drills | trace drills below |
| test judgment | quiz, spot the bug | quiz and spot-the-bug below |
| build the skill end to end | labs, case studies | parts 2 and 7 |
| transfer to a new file | interleaved set, kata | below and part 4 |
| fast lookup under pressure | cheat sheets | parts 5 and 9 |

Each item tests one fact, mechanism or decision, and each lab step targets one skill before skills are combined `{P2}`.

## C1: twenty more micro-drills `{P9}`

11. **Drill** Print the first field of space-separated lines. *Answer:* `awk '{print $1}'`.
12. **Drill** Print lines longer than 80 characters. *Answer:* `awk 'length($0)>80'`.
13. **Drill** Count lines that do not contain `debug`. *Answer:* `grep -vc debug file`.
14. **Drill** Show the number of distinct values in field 1 of a space-separated file. *Answer:* `awk '{print $1}' f | sort -u | wc -l`.
15. **Drill** Replace every comma with a semicolon. *Answer:* `sed 's/,/;/g'`.
16. **Drill** Print only lines 5 to 8. *Answer:* `sed -n '5,8p' f`.
17. **Drill** Show every line that starts with a digit. *Answer:* `grep '^[0-9]' f`.
18. **Drill** Show lines ending in `.log`. *Answer:* `grep '\.log$' f`.
19. **Drill** Upper-case all text. *Answer:* `tr 'a-z' 'A-Z'`.
20. **Drill** Delete blank lines. *Answer:* `sed '/^$/d'` or `grep -v '^$'`.
21. **Drill** Number the lines. *Answer:* `nl -ba` or `cat -n`.
22. **Drill** Show the last 3 lines. *Answer:* `tail -n 3`.
23. **Drill** Show all lines except the first. *Answer:* `tail -n +2`.
24. **Drill** The most common word in `words.txt` (one word per line). *Answer:* `sort words.txt | uniq -c | sort -rn | head -1`.
25. **Drill** The average of column 3 (space-separated, no header). *Answer:* `awk '{s+=$3} END {print s/NR}'`.
26. **Drill** Lines where field 2 equals `west` and field 4 is above 5. *Answer:* `awk -F, '$2=="west" && $4>5'`.
27. **Drill** The longest line. *Answer:* `awk '{ if (length($0)>m) {m=length($0); l=$0} } END {print l}'`.
28. **Drill** The line count of lines containing `error`, ignoring case. *Answer:* `grep -ci error file`.
29. **Drill** Print fields 1 and 3 separated by a tab. *Answer:* `awk '{print $1 "\t" $3}'`.
30. **Drill** Join two consecutive lines into one. *Answer:* `paste - -`.

## C2: ten more trace drills `{P10}`

6. **Trace** `printf 'x y\nz w\n' | awk '{print $2}'`. *Answer:* `y` then `w`.
7. **Trace** `printf 'a\na\nb\n' | uniq -c`. *Answer:* `2 a` then `1 b`.
8. **Trace** `printf '3\n1\n2\n' | sort -rn | head -2`. *Answer:* `3` then `2`.
9. **Trace** `printf 'a,b,c\n' | cut -d, -f2,3`. *Answer:* `b,c`.
10. **Trace** `printf 'a b  c\n' | awk '{print NF}'`. *Answer:* `3` (a run of spaces is one separator).
11. **Trace** `printf 'a b  c\n' | cut -d' ' -f3`. *Answer:* an empty line (field 3 sits between the two spaces).
12. **Trace** `printf 'one\ntwo\n' | sed 's/o/0/'`. *Answer:* `0ne` then `tw0`.
13. **Trace** `printf 'one\ntwo\n' | sed 's/o/0/g'`. *Answer:* `0ne` then `tw0`: each word has one `o`, so `g` changes nothing here; try `foo` to see the difference.
14. **Trace** `printf 'a\nb\n' | tac`. *Answer:* `b` then `a`.
15. **Trace** `printf 'b\nA\n' | sort -f`. *Answer:* `A` then `b` (case ignored in the comparison).

## C3: six more spot-the-bug items `{V31}`

4. **Spot the bug** `sort -n file | uniq -c` to rank by frequency. *Answer:* the ranking needs `sort -rn` after `uniq -c`; the first sort only groups.
5. **Spot the bug** `awk -F, 'NR>1 {print $3}' f | sort | uniq -c | head` to find the most common item. *Answer:* `head` shows the first lines of a count-ordered-by-name list; add `sort -rn` before `head`.
6. **Spot the bug** `cut -d, -f2 f | grep -c west` to count orders in the west region. *Answer:* it counts lines whose second field contains `west`, including `westeast`; use an exact test.
7. **Spot the bug** `cat f | sort > f` to sort a file in place. *Answer:* the redirect truncates `f` before `sort` reads it; the file ends up empty.
8. **Spot the bug** `grep error log | grep -v warning | wc -l` for "errors that are not warnings". *Answer:* a line containing both words is dropped; decide whether that is intended.
9. **Spot the bug** `awk '{print $NF}' f` to get the last column of lines with a trailing space. *Answer:* the last field may be empty; trim first.

## C4: ten more quiz questions (11 to 20) `{P11}`

**Q11.** You need the five busiest client addresses in a web log. Which is correct?
  - (A) `awk '{print $1}' log | sort | uniq -c | sort -rn | head -5` — right: select the field, group, count, rank, keep five.
  - (B) `awk '{print $1}' log | uniq -c | head -5` — wrong: without sorting, repeats are not adjacent.
  - (C) `sort log | head -5` — wrong: it sorts whole lines and shows five requests, not counts.
  - (D) `grep -c 1 log` — wrong: it counts lines containing a digit.

**Q12.** `sed 's/a/b/'` on the line `banana` gives:
  - (A) `bbnbnb` — wrong: that needs the `g` flag and also the first letter is `b` already.
  - (B) `bbnana` — right: without `g` only the first `a` on the line changes.
  - (C) `banana` — wrong: a match exists, so a change happens.
  - (D) `bbnbnb` for every line — wrong: the same reason as (A).

**Q13.** What does `sort -k2,2 -s` add compared with `sort -k2`?
  - (A) It sorts numerically — wrong: that needs `-n`.
  - (B) It uses only field 2 and keeps the original order for ties — right: `,2` ends the key, `-s` makes it stable.
  - (C) It removes duplicates — wrong: that is `-u`.
  - (D) It reverses the order — wrong: that is `-r`.

**Q14.** A lab shows a count of 5 for `grep -c 500 log` and 2 for `awk '$9==500' log | wc -l`. What does that tell you?
  - (A) awk is broken — wrong: the field test is exact.
  - (B) The grep pattern matches in other fields too — right: digits can appear in sizes and paths, so the loose count is higher.
  - (C) The file changed between runs — wrong: nothing suggests it.
  - (D) The log has no 500 statuses — wrong: the exact test found 2.

**Q15.** Why can `cut -d' ' -f2` fail on aligned columns?
  - (A) `cut` cannot read spaces — wrong: it can use a space delimiter.
  - (B) Runs of spaces create empty fields — right: each space is a separator, so field numbers shift.
  - (C) `cut` needs a header — wrong: it never reads one.
  - (D) The columns are sorted — wrong: order is irrelevant to splitting.

**Q16.** Which stage in `cut | sort | uniq -c | sort -rn | head` is the bottleneck on a huge file?
  - (A) the first `sort` — right: it must hold all input before output starts.
  - (B) `cut` — wrong: it works line by line and streams its output at once.
  - (C) `head` — wrong: it exits after a few lines.
  - (D) the second `sort` — wrong: its input is small, one line per distinct value.

**Q17.** What is the safest first move on an unfamiliar file?
  - (A) Run the full pipeline — wrong: a wrong delimiter would hide behind a plausible-looking answer.
  - (B) Print the first lines and the field count — right: it reveals the format before anything depends on it.
  - (C) Sort the file — wrong: it can scramble a header.
  - (D) Delete blank lines — wrong: you do not yet know what is in the file.

**Q18.** Why is `cat f | sort > f` dangerous?
  - (A) `cat` is slow — wrong: speed is not the issue.
  - (B) The shell opens `f` for writing first and empties it — right: `sort` then reads an empty file.
  - (C) `sort` cannot read from a pipe — wrong: reading standard input is its default when no file is named.
  - (D) The output is sorted twice — wrong: it is sorted once.

**Q19.** A teammate says "the totals agree, so the method is right." The best reply is:
  - (A) Agreed — wrong: agreement can be luck.
  - (B) Change the data slightly and check that the totals still agree for the right reason — right: a method is tested by what it does under change.
  - (C) Add more stages — wrong: that adds risk, not evidence.
  - (D) Use a spreadsheet instead — wrong: the tool is not the issue.

**Q20.** Which is a trust-boundary mistake?
  - (A) Printing a field — wrong: output is safe.
  - (B) Building a command line from a field of the file and running it — right: data becomes code.
  - (C) Sorting the file — wrong: sorting does not execute anything.
  - (D) Counting lines — wrong: nothing is interpreted.

## C5: sixty more flashcards (twelve of each type) `{P6}` `{P18}`

Concept:

- [concept][easy] Front: What does `tr` do? Back: swaps or deletes single characters.
- [concept][easy] Front: What does `tac` print? Back: lines in reverse order.
- [concept][medium] Front: What does `sort -u` do? Back: sorts and keeps one line of each equal group.
- [concept][medium] Front: What does `NF` hold in awk? Back: the number of fields on the current line.
- [concept][medium] Front: What does `sed -n '2,4p'` do? Back: prints only lines 2 to 4.
- [concept][easy] Front: What is a regular expression? Back: a pattern describing a set of strings.
- [concept][medium] Front: What does `grep -E` change? Back: it turns on extended regex (`+`, `?`, `|`, groups).
- [concept][medium] Front: What does `grep -o` print? Back: only the matching part of each line.
- [concept][easy] Front: What does `head -n 3` print? Back: the first three lines.
- [concept][medium] Front: What is the trust boundary in a pipeline? Back: file content is data and must never be run as a command.
- [concept][medium] Front: What does `column -t` do? Back: aligns whitespace-separated fields into columns for reading.
- [concept][easy] Front: What does `nl -ba` do? Back: numbers every line.

Cloze:

- [cloze][easy] Front: `grep ____` ignores case. Back: `-i`.
- [cloze][medium] Front: `uniq ____` counts repeats. Back: `-c`.
- [cloze][medium] Front: `sort -t____ -k2` sorts a comma file by field 2. Back: `,`.
- [cloze][medium] Front: awk's `____` block runs after the last line. Back: `END`.
- [cloze][medium] Front: `sed 's/a/b/____'` replaces every match on a line. Back: `g`.
- [cloze][easy] Front: `^` anchors the start and `____` anchors the end of a line. Back: `$`.
- [cloze][medium] Front: `awk -F, 'NR____1'` skips the header. Back: `>`.
- [cloze][trap] Front: `sort ____` sorts by field 2 only (end the key). Back: `-k2,2`.
- [cloze][medium] Front: `cut -d, -f____` selects fields 2 and 3. Back: `2,3`.
- [cloze][easy] Front: `wc ____` counts lines. Back: `-l`.
- [cloze][medium] Front: `LC_ALL=____` gives byte-order sorting. Back: `C`.
- [cloze][medium] Front: `tail -n ____` starts at line 2. Back: `+2`.

Scenario or decision:

- [scenario][medium] Front: Which stage is the bottleneck on a huge file? Back: `sort`, because it must see all input first.
- [scenario][trap] Front: A grep count is larger than a field test. Why? Back: the pattern matched in other fields.
- [scenario][medium] Front: How do you count requests per hour in a log? Back: take the hour from the timestamp field (`substr`), then `sort | uniq -c`.
- [scenario][easy] Front: You need to join two consecutive lines. Tool? Back: `paste - -`.
- [scenario][medium] Front: Data has quoted commas. Tool? Back: a CSV-aware tool (Python `csv`, csvkit).
- [scenario][trap] Front: A total is right once. What next? Back: change the data a little and check it follows.
- [scenario][medium] Front: You need to remove blank lines. Tool? Back: `grep -v '^$'` or `sed '/^$/d'`.
- [scenario][easy] Front: You want lines 5 to 8. Tool? Back: `sed -n '5,8p'`.
- [scenario][medium] Front: A script must stop if the header changed. How? Back: compare `head -1` with the expected text and exit if different.
- [scenario][trap] Front: Why should file content never be used as a command? Back: it crosses the trust boundary: data would become code.
- [scenario][medium] Front: You must sort by a numeric column in a comma file. Back: `sort -t, -kN -n`.
- [scenario][medium] Front: How do you see hidden characters? Back: `cat -A`.

Contrast:

- [contrast][medium] Front: `sed` versus `tr`? Back: `sed` replaces text and patterns; `tr` swaps single characters.
- [contrast][medium] Front: `head -n 5` versus `tail -n +5`? Back: first five lines versus everything from line 5.
- [contrast][trap] Front: `-k2` versus `-k2,2`? Back: from field 2 to the end of the line versus field 2 only.
- [contrast][medium] Front: `grep` versus `awk` pattern? Back: `grep` matches text; `awk` can also compare numbers and test fields.
- [contrast][medium] Front: `sort -u` versus `uniq`? Back: `sort -u` works on unsorted input; `uniq` needs sorted input.
- [contrast][trap] Front: `>` versus `|`? Back: `>` writes a file; `|` feeds another program.
- [contrast][medium] Front: stdout versus stderr? Back: results versus complaints; a pipe carries only stdout.
- [contrast][medium] Front: `cut` versus `awk` on aligned columns? Back: `cut` treats each space as a separator; `awk` treats a run as one.
- [contrast][easy] Front: `wc -l` versus `grep -c`? Back: total lines versus matching lines.
- [contrast][medium] Front: awk array versus `sort | uniq -c`? Back: one pass holding all keys versus streaming with a sort.
- [contrast][trap] Front: a correct answer versus a correct method? Back: the answer can be right by luck; only the method survives changed data.
- [contrast][medium] Front: `grep -E` versus basic `grep`? Back: extended supports `+ ? |` without backslashes.

Trace:

- [trace][medium] Front: `printf 'a b  c\n' | awk '{print NF}'` Back: `3`.
- [trace][trap] Front: `printf 'a b  c\n' | cut -d' ' -f3` Back: an empty line.
- [trace][medium] Front: `printf 'one\n' | sed 's/o/0/'` Back: `0ne`.
- [trace][easy] Front: `printf 'a\nb\n' | tac` Back: `b` then `a`.
- [trace][medium] Front: `printf 'b\nA\n' | sort -f` Back: `A` then `b`.
- [trace][medium] Front: `printf '3\n1\n2\n' | sort -rn | head -2` Back: `3` then `2`.
- [trace][trap] Front: `printf '1\n1\n2\n' | uniq -c` Back: `2 1` then `1 2`.
- [trace][medium] Front: `printf 'a,b\n' | awk -F, '{print $2,$1}'` Back: `b a`.
- [trace][easy] Front: `printf 'abc\n' | rev` Back: `cba`.
- [trace][medium] Front: `printf 'x\ny\nz\n' | tail -n +2` Back: `y` then `z`.
- [trace][trap] Front: `printf 'x\n\ny\n' | grep -vc '^$'` Back: `2`.
- [trace][medium] Front: `printf 'a\nb\n' | nl -ba` Back: numbered lines `1 a`, `2 b`.

## C6: twelve more interleaved items (13 to 24) `{A19}`

13. Count lines. *Answer:* `wc -l`.
14. Search a directory tree for the word `token`. *Answer:* `grep -r token dir`.
15. Show who owns a file and its permissions. *Answer:* `ls -l`.
16. Count how many times each request path appears in a log. *Answer:* `awk '{print $7}' log | sort | uniq -c | sort -rn`.
17. Make a file readable by everyone and writable by the owner only. *Answer:* `chmod 644 file`.
18. Show lines containing `GET` or `POST`. *Answer:* `grep -E 'GET|POST'`.
19. Find files bigger than 1 MB. *Answer:* `find . -size +1M`.
20. Print the second-to-last field of each line. *Answer:* `awk '{print $(NF-1)}'`.
21. Show the type of a file regardless of its name. *Answer:* `file`.
22. Sum the sizes (field 10) in a web log. *Answer:* `awk '{s+=$10} END {print s}' log`.
23. Remove the header and sort the rest by field 1. *Answer:* `tail -n +2 f | sort -t, -k1,1`.
24. Show the unique client addresses (field 1). *Answer:* `awk '{print $1}' log | sort -u`.

## C7: explain it in one sentence, and the error log `{A49}` `{A14}`

Say each in one sentence, then compare with a classmate or your notes: (1) why `uniq` needs sorting; (2) why a quote matters in `awk '...'`; (3) why `LC_ALL=C` helps; (4) what a trust boundary is; (5) how you would check a total.

**Error log.** Keep a running table (item, what went wrong, error class, corrected model, new card). After a week, count the classes: the most frequent class shows what to rehearse. This is the error-to-aid loop `{P5}` closing on your own data.
