# Extension B: case studies, more labs, more failures, more design

Each case study follows one frame: scenario, questions, plan, run, interpretation, verification, assumptions, what an expert adds `{A54}` `{A38}`. The labs here are the harder half of the topic.

## Extension B1: three case studies

### Case study 1: triage of a web log

**Scenario.** A small web shop asks why the site felt slow and whether anything odd happened this morning. You have `access.log` (300 requests) and nothing else. **Questions:** who made the most requests; what statuses were returned; did any client keep failing; when did traffic peak.

**Plan** `{A38}`: one pipeline per question; reconnaissance first `{V24}`.

```lab
$ head -3 access.log
10.0.1.35 - - [26/Nov/2026:09:00:29 +0000] "GET /products/42 HTTP/1.1" 200 5557 "-" "python-requests/2.31"
10.0.1.21 - - [26/Nov/2026:09:01:41 +0000] "GET /static/app.js HTTP/1.1" 200 1455 "-" "Googlebot/2.1"
10.0.3.31 - - [26/Nov/2026:09:02:42 +0000] "GET / HTTP/1.1" 403 2927 "-" "Mozilla/5.0"
$ awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
    106 203.0.113.9
     42 10.0.1.21
     19 10.0.1.28
$ awk '{print $9}' access.log | sort | uniq -c | sort -rn
     77 200
     72 401
     57 403
     27 301
     25 404
     24 500
     18 304
$ awk '$9==401 || $9==403 {print $1}' access.log | sort | uniq -c | sort -rn | head -3
    106 203.0.113.9
      6 10.0.1.21
      3 10.0.3.31
$ awk '{print substr($4,2,14)}' access.log | sort | uniq -c
     60 26/Nov/2026:09
     60 26/Nov/2026:10
     60 26/Nov/2026:11
     60 26/Nov/2026:12
     60 26/Nov/2026:13
```

**Interpretation.** One client address makes far more requests than any other, and the same address accounts for most of the 401 and 403 answers: the failures and the volume come from one place. The per-hour counts show whether the load was steady. *Evidence labels* `{A42}`: the counts are **facts** from this file; "that client is misbehaving" is an **inference**; "it caused the slowness" is an **assumption** the log cannot prove (response times are not in this format).

**Verification** `{A33}`: the counts of statuses should add up to 300; check with `wc -l`. *Checks passed:* the labs above ran. *Not run:* anything involving response time, because the log format here has no such field.

```lab
$ wc -l access.log
300 access.log
$ awk '{s+=1} END {print s}' access.log
300
```

**What an expert adds.** A second source (the server's error log), time-of-day context, and a note of what the logs cannot show.

### Case study 2: a sales report you can trust

**Scenario.** The manager wants orders per region, value per item, the three biggest orders and a total, every week. **Plan:** four pipelines, then a reconciliation. **Design** `{A38}`: requirements (correct, repeatable, readable), constraints (text file, no quoted commas), candidates (pipelines versus a script language), decision (pipelines, wrapped in a script), failure modes (header changes, blank lines), tests (reconcile two totals).

```lab
$ cut -d, -f2 sales.csv | tail -n +2 | sort | uniq -c | sort -rn
     18 west
     18 north
     15 south
      9 east
$ awk -F, 'NR>1 {t[$3]+=$4*$5} END {for (k in t) printf "%s %.2f\n", k, t[k]}' sales.csv | sort -k2 -rn
elderberry 684.00
cherry 476.00
date 357.50
apple 42.00
banana 20.50
$ tail -n +2 sales.csv | sort -t, -k4 -rn | head -3
2026-11-26,south,date,12,6.5
2026-11-19,west,apple,12,0.5
2026-11-13,west,apple,12,0.5
$ awk -F, 'NR>1 {s+=$4*$5} END {printf "%.2f\n", s}' sales.csv
1580.00
$ awk -F, 'NR>1 {t[$3]+=$4*$5} END {for (k in t) s+=t[k]; printf "%.2f\n", s}' sales.csv
1580.00
```

*Reconciliation:* the last two commands compute the grand total two ways; equal numbers mean the grouping lost nothing. **Interpretation:** the report is only as trustworthy as that equality.

### Case study 3: reading a process listing

**Scenario.** A server feels loaded; `procs.txt` is a saved listing with aligned columns (user, process id, CPU, memory, command). **Questions:** which user holds the most memory; which commands are most common; which processes use more than half the CPU.

```lab
$ awk 'NR>1 {m[$1]+=$4} END {for (u in m) print m[u], u}' procs.txt | sort -rn
250 postgres
176 alice
133 bob
116 root
70 www
$ awk 'NR>1 {print $5}' procs.txt | sort | uniq -c | sort -rn | head -3
      5 sshd
      3 python3
      3 node
$ awk 'NR>1 && $3>50' procs.txt | column -t
root      1037  68  7   cron
postgres  1185  54  4   systemd
root      1259  73  38  node
postgres  1407  87  12  sshd
postgres  1444  73  41  nginx
bob       1555  87  35  node
alice     1592  59  38  java
postgres  1703  63  57  cron
root      1777  65  27  python3
```

**Assumptions** `{A41}`: percentages are one snapshot, not an average over time; a command name is not a program identity (two programs can share a name). **What an expert adds:** repeated snapshots and the time dimension.

## Extension B2: more labs

### Lab E: regex versus field (prompted)

Use `access.log`. Goal: a count of requests that returned status 500. Write it with `grep` and with `awk`, explain which can over-count and prove it with a number.

```lab
$ grep -c 500 access.log
25
$ grep -c ' 500 ' access.log
24
$ awk '$9==500' access.log | wc -l
24
```

- Hint 1: the first pattern has no anchors.
- Hint 2: the digits 500 can appear in other fields (size, path).
- Hint 3: compare the three numbers.
- Hint 4: the awk field test is exact; the loose grep over-counts when the three differ.

### Lab F: clean the messy file (unassisted, with a verification rule)

Goal: orders per region from `messy.csv`, correct despite the blank line, the repeated header, the case difference and the leading space. *Rule:* explain, in one sentence per problem, what you did about it, and say which problem you could not fix with these tools.

```lab
$ grep -v '^$' messy.csv | grep -v '^date' | cut -d, -f2 | tr 'A-Z' 'a-z' | sed 's/^ *//' | sort | uniq -c
      1 east
      3 north
      1 south
      2 west
```

*Expected caution:* the quoted-comma row shifts its fields, so a field-based pipeline mis-reads its region; that is the problem these tools cannot fix.

- Hint 1: list the problems before fixing any.
- Hint 2: remove, normalise, then count.
- Hint 3: `grep -v` removes lines; `tr` and `sed` normalise text.
- Hint 4: the command above; the quoted comma needs a CSV-aware tool.

### Lab G: turn a pipeline into a reusable script (procedure, not run)

*Status:* **not run in the sandbox** (it writes a file). Steps, with the reason for each `{A29}`:

1. State the question as a comment: scripts without a question rot.
2. Put the pipeline in `report.sh` with a first line `#!/usr/bin/env bash`: tells the system how to run it.
3. Add `set -o pipefail`: a failing stage fails the whole line.
4. Check the header before anything else and stop with a message if it is wrong: protects every later stage.
5. Quote file names (`"$1"`): protects against spaces and special characters.
6. Make it executable (`chmod u+x report.sh`) and run it on `sales.csv` and `messy.csv`.

- Hint 1: write the questions as comments first.
- Hint 2: the header check is one `head -1` compared with the expected text.
- Hint 3: use `[ "$(head -1 "$1")" = "date,region,item,qty,price" ] || exit 1`.
- Hint 4: the full script is in the next section.

## Extension B3: code teaching, from problem to script `{A30}`

| Step | Content |
|---|---|
| Problem | print a ranked order count per region, safely |
| Requirements | correct, repeatable, stops on a bad header, no output on error except the message |
| Logic | check the header; drop it; count per region; rank |
| Pseudocode | if first line is not the header then stop; otherwise cut, sort, count, rank |

```bash
#!/usr/bin/env bash
# question: how many orders per region, biggest first?
set -o pipefail
file="$1"
[ "$(head -1 "$file")" = "date,region,item,qty,price" ] || { echo "unexpected header" >&2; exit 1; }
tail -n +2 "$file" | cut -d, -f2 | sort | uniq -c | sort -rn
```

*Run:* **not run** here. *Test:* run on `sales.csv` and compare with the pipeline in part 1; run on `messy.csv` and expect the stop message only if the header differs. *Debug:* print with `bash -x report.sh sales.csv`. *Refactor:* put the header string in a variable; add a second function for the value report. *Architecture:* the script is one component with one input (a file path), one output (stdout) and one error channel (stderr); the trust boundary is the file content.

## Extension B4: more failure cases and break-fix labs

### Failure case 4: output stops after the first screen

*Symptom:* a pipeline ending in `head` finishes at once, and a message about a broken pipe may appear on the previous stage. *Cause:* `head` closes its input after enough lines; the earlier stage is told its output is gone. *Test:* run `yes | head -3`. *Fix:* none needed; it is normal, and shows that stages stream `{A25}`. *Label:* **observed**; the exact message is **VERIFY**.

### Failure case 5: a space or tab sorts in the wrong place

*Symptom:* `sort -k2` orders fields oddly when fields contain spaces. *Hypotheses:* (a) the separator is not what you think; (b) leading blanks count; (c) the locale ignores punctuation. *Test:* sort with `-t` set and with `LC_ALL=C`. *Fix:* set the separator explicitly and fix the locale.

### Failure case 6: an empty field turns into zero

*Symptom:* an average looks too low. *Cause:* an empty quantity is read as 0 by awk, so it counts as an order of 0 units. *Test:* find them with `awk -F, 'NR>1 && $4==""'`. *Fix:* skip them in the sum and decide how to count them. *Label:* the choice is a **preference** that must be written down.

```lab
$ awk -F, 'NR>1 && $4=="" {print NR": "$0}' messy.csv
5: 
9: 2026-11-04,west,date,,6.5
$ awk -F, 'NR>1 {n++; s+=$4} END {print n, s, s/n}' messy.csv
9 24 2.66667
$ awk -F, 'NR>1 && $4!="" {n++; s+=$4} END {print n, s, s/n}' messy.csv
7 24 3.42857
```

**Break-fix lab 3 (symptom only)** `{P8}`: a script counts requests per client, but one address appears twice in the output with different counts. Find the cause before reading on. *Debrief:* the two entries differ by a trailing character (a space or a carriage return); fix by normalising or by choosing the delimiter. *Prevention:* print `cat -A` of a few lines of unfamiliar data.

**Break-fix lab 4 (symptom only):** a total is off by exactly one order. *Debrief:* the header was counted, or the last line has no trailing newline and was skipped by a tool that reads whole lines. *Prevention:* count lines two ways.

## Extension B5: more misconceptions and mistakes

**Misconception 4** `{A15}`: "`sort` changes the file." *Why reasonable:* the name suggests editing. *Where it breaks:* it prints a sorted copy to stdout and leaves the file alone. *Test:* run `sort` on a file and read the file again.

**Misconception 5:** "`head` and `tail` need to read the whole file." *Where it breaks:* `head` stops early; `tail` has to reach the end but does not hold the whole file. *Test:* `yes | head -3`.

**Misconception 6:** "A count that matches my expectation is right." *Where it breaks:* a wrong method can give a right number by luck. *Test:* change the data slightly and see whether the answer still follows.

| Mistake | What breaks | Instead | Error class |
|---|---|---|---|
| trusting a loose regex count | over-counts | field test or anchored pattern | logical |
| `sed -i` without a backup | the file is changed for good | `-i.bak` or write a copy | strategy |
| unquoted variable in a script | splits on spaces | `"$var"` | procedural |
| sorting numbers with locale rules | surprising order | `LC_ALL=C sort -n` | conceptual |
| reading output without a header check | silent misalignment | assert the header | assumption |
| piping a huge file to a pager first | slow, pointless | filter first | strategy |

## Extension B6: more critique and design

**Critique 2** `{A46}`: review `grep north sales.csv | wc -l > count.txt`. *Findings:* the pattern is loose; the redirect writes a file (a side effect), so the command is no longer read-only; `grep -c` is shorter; no stated question.

**Critique 3:** review `awk '{s+=$4} END {print s}' sales.csv` as a "total quantity". *Findings:* the header is included; the delimiter is not set, so the whole line is one field and `$4` is empty; the answer is 0 and looks like data, not an error.

**Design kata 2** `{A48}`: the same report must now run unattended every night and email only on a problem. *Shifts:* the input sometimes does not arrive (what do you check first), the format changes (header assertion), the data grows 50 times (filter and sort cost), a teammate edits the script (tests). *Decide* what to log and what to keep silent.

**Design kata 3:** compare three designs for "top 10 clients in a log of 10 million lines": a sort-and-count pipeline, an awk array, and a database. State the memory, the speed, the effort and the maintenance for each, and when you would move to the database.

## Extension B7: adaptive routing and testing statements

**Adaptive difficulty** `{A52}`: if you scored 2 or fewer on the entry diagnostic, repeat parts 1 and 3 before the labs; if you struggled with Lab C, return to worked example B and the awk primer; if the adversarial lab passed first time, skip to the capstone and the case studies; if the case studies pass without hints, move to `K-LOG01`.

**Testing statement** `{A33}`: *passed:* every lab block in this topic ran and matched. *Failed:* none at the time of writing. *Not run:* the script lab, other shells and awk variants, locale differences, quoted CSV parsing, timing on large files.
