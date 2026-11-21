# Files, archives, logs and timelines

Evidence work turns an artifact into a defensible finding. A filename, signature match and embedded comment answer different questions. Establish what bytes you received, what their structure permits a parser to say, and what independent observation distinguishes one interpretation from another. Work in a scratch directory using copies. Hash results and keep notes outside the input directory. The following commands assume GNU tools on Kali and files supplied for analysis.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Does the hash match the supplied reference"} -- Yes --> Y0["Record that exact bytes were received"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Do name, signature and structural parser agree"} -- Yes --> Y1["Choose the relevant format parser"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Is it an archive"} -- Yes --> Y2["List entries and assess paths and sizes before opening a member"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Is the question about a sequence of events"} -- Yes --> Y3["Preserve the original clock and derive a normalized timeline"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can two observations corroborate the result"} -- Yes --> Y4["Record commands, timestamps and identifiers"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Does the hash match the supplied reference** If yes, Record that exact bytes were received. If no, verify source, transfer and expected reference before proceeding.
2. **Do name, signature and structural parser agree** If yes, Choose the relevant format parser. If no, inspect headers and tail and compare another parser.
3. **Is it an archive** If yes, List entries and assess paths and sizes before opening a member. If no, identify whether it is structured text, binary or media.
4. **Is the question about a sequence of events** If yes, Preserve the original clock and derive a normalized timeline. If no, find the smallest artifact that can support the claim.
5. **Can two observations corroborate the result** If yes, Record commands, timestamps and identifiers. If no, report it as a lead and explain what evidence is missing.

## Command recipes

### Intake and file identification

Start with a hash and format evidence before transforming any data. Digest the original, then the working copy. Matching hashes mean the copies contain matching bytes to practical SHA-256 confidence.

~~~bash
sha256sum -- artifact.bin
stat -c '%s bytes' -- artifact.bin
file -k -- artifact.bin
xxd -g 1 -l 64 artifact.bin
strings -a -n 8 -t x -- artifact.bin | head -n 25
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `--` | Stop option parsing for GNU sha256sum, stat, file and strings. |
| `stat -c` | Use a custom result format. `%s` is byte length. |
| `file -k` | Keep going after the first match. Secondary matches can be heuristic. |
| `xxd -g 1 -l 64` | Print one-byte groups and cap the input at 64 bytes. Offsets are hexadecimal. |
| `strings -a -n 8 -t x` | Search across input, require eight printable characters, and print hexadecimal offsets. |
| `head -n 25` | Limit displayed lines. An intentionally shortened listing is not evidence that no further string exists. |

Check a string's location with `xxd -s 0x100 -l 32 artifact.bin`, replacing the offset with the reported location. `-s` starts at the specified byte and `-l` limits the number read. The same bytes can have multiple reasonable interpretations, so use structure as corroboration.

### Archive inspection without extraction

Unknown archives can have surprising member paths, links, encrypted entries and huge expanded sizes. Use listings before opening individual files.

~~~bash
unzip -l bundle.zip
zipinfo -l bundle.zip
tar -tvf bundle.tar
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `unzip -l` | List members and their reported uncompressed size without extracting. |
| `zipinfo -l` | Long listing with entry attributes and sizes. Inspect types as well as names. |
| `tar -tvf` | List (`-t`) with details (`-v`) from the archive named after `-f`. |

Check for absolute paths, parent components, links and a large compressed-to-expanded ratio. A declared size can be wrong. For unfamiliar containers, find a safe format-specific viewer in the VM. Keep the original intact. Do not run files from an evidence bundle.

### Preserve original time and count results

The first pass checks shape and frequency, not the truth of the events. The example reads newline-delimited JSON with one object per line.

~~~bash
jq -r '[.timestamp, .event, .source] | @tsv' events.jsonl
jq -r '.event // "<missing>"' events.jsonl | LC_ALL=C sort | uniq -c
rg -n -F -- 'evt-42' events.jsonl
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `jq -r` | Emit string values directly instead of JSON-quoting each line. |
| `@tsv` | Serialize a row of fields with tab separators and escaped control characters. |
| `//` | Use a fallback for null, missing, or false. Review whether false is valid for your schema. |
| `LC_ALL=C sort` | Use a stable byte-oriented collation for this command, independent of host locale. |
| `uniq -c` | Count adjacent identical lines. Sort first to group all matches. |
| `rg -n -F --` | Show line number, match a literal string and end options. A regex would interpret punctuation differently. |

Confirm jq parsed all records without errors before trusting a downstream total. In a Bash pipeline use `set -o pipefail` in your analysis shell, then check the exit status. Preserve timezone and offsets. Sorting ISO-like timestamps with unlike offsets lexicographically can reverse their actual order.

## Worked walkthrough

1. Create a harmless ZIP containing a text note using `python3 -m zipfile -c demo.zip note.txt`, where `-m zipfile` runs the standard-library CLI and `-c` creates an archive from named files. Use a new destination in scratch.
2. Copy it under the name `report.jpg`. Predict what the filename suggests and what `file`, `xxd` and `unzip -l` will say independently. Compare hashes of both names. If the hashes agree, the name change did not change file bytes.
3. Check for ZIP-style header bytes and a valid member listing. If the header looks plausible but the central directory is missing, the content might be a truncated or composite file. Keep that uncertainty. A valid listing says you can parse part of the format, not that each entry is trustworthy.
4. Create a short paper timeline: 09:30−05:00 and 14:25Z. The first is 14:30Z, five minutes later. A compiler, archive creator and log collector may report different clocks, so annotate source and offset rather than replacing the original time.
5. Write a verification note with observed signature, member name and hash. Repeat with a plain text file merely named ZIP. A good triage procedure should classify the control differently from the renamed real archive.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| Only filename implies a type | Mislabeled or misleading extension | Compare header and format parser output. |
| Parser fails halfway | Truncation, corrupt record, unexpected type or password protection | Record the first failing offset or record and test with a known-good file. |
| No useful printable text | Binary encoding, compression, encryption, or UTF-16 | Look at byte patterns and use a format-aware parser; keep guesses labeled. |
| Same event appears twice | Forwarding, retries, merging sources or real repetition | Compare original record IDs, sources and timing before deduplicating. |
| Timeline order changes after normalization | Mixed offsets, clock drift, timestamp precision or naive sorting | Show raw and normalized time side by side and state assumptions. |
| Hashes disagree | Files differ or hash algorithms differ | Confirm command, exact path, bytes and comparison reference. |
| Archive contains a suspicious link or huge file | Malicious or incidental packaging | Keep the listing, use bounded read-only inspection and avoid bulk extraction. |

## Glossary

| Term | Meaning and use |
|---|---|
| Hash | Digest of exact bytes. Useful for preservation and deduplication, insufficient for authorship. |
| Magic bytes | Format-indicative bytes at a known offset. A signature can occur in unintended places. |
| Provenance | Who or what supplied an artifact and how it was handled. |
| Container | Format holding other streams or entries. Its structure is distinct from the content of any member. |
| UTC offset | Difference between a local time representation and UTC. |
| Clock skew | Difference between clocks of observers at a given moment. |
| Control sample | Known input expected to produce or lack a feature. |
| Evidence pointer | Stable locator such as a filename, byte offset, line number or source ID. |
| Observation | Direct parser output or measured feature. Interpretation connects the observation to the question. |

## Practice, transfer and handoff

- Produce a five-record JSONL fixture with a missing event, a repeated event and a broken line. Predict what the counters show before and after you fix the broken line.
- Ask a teammate to identify an archive format without revealing its extension. Compare whether they have one clue or independent corroboration.
- Handoff with exact artifact hash, paths, byte offsets, relevant lines, clock assumptions and the shortest safe reproduction.

[GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html) · [jq manual](https://jqlang.org/manual/)

[Chapter index](README.md)
