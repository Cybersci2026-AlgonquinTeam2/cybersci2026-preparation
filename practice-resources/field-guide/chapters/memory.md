# Memory forensics and process attribution

A memory image preserves an observer's view of RAM around one capture time. Process lists and network objects are interpretations of structures found in that image. Good attribution needs identity, time and agreement between multiple views. A PID match alone is insufficient because an operating system can reuse a PID. Prepare the tool and needed symbols before disconnecting. Use only a permitted memory image and keep memory output private because it can contain sensitive data.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Do acquisition notes identify OS and architecture"} -- Yes --> Y0["Choose the matching parser family and preserve the acquisition details"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Can the parser satisfy kernel layer and symbol requirements"} -- Yes --> Y1["Run a minimal information plugin before asking detailed questions"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Does a normal process view contain the candidate"} -- Yes --> Y2["Check process identity, parent, start time and path"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Do connection and process times agree"} -- Yes --> Y3["Correlate identifiers, source and timeline"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can a second source support the conclusion"} -- Yes --> Y4["Report attribution with evidence references"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Do acquisition notes identify OS and architecture** If yes, Choose the matching parser family and preserve the acquisition details. If no, inspect format and get the missing details before assuming a plugin family.
2. **Can the parser satisfy kernel layer and symbol requirements** If yes, Run a minimal information plugin before asking detailed questions. If no, check installation, symbols and image completeness using a known-good control.
3. **Does a normal process view contain the candidate** If yes, Check process identity, parent, start time and path. If no, compare another available process view and consider terminated objects.
4. **Do connection and process times agree** If yes, Correlate identifiers, source and timeline. If no, look for PID reuse, stale structures and clock differences.
5. **Can a second source support the conclusion** If yes, Report attribution with evidence references. If no, report the observed record and narrow the claim.

## Command recipes

### Prepare and check the local Volatility installation

Examples assume the Volatility 3 launcher is installed as `vol` and an authorized Windows image is staged. Launchers can differ. Read local help for the installed version and copy required symbols into the VM before event use.

~~~bash
vol --help
vol -f memory.raw windows.info
vol -f memory.raw windows.pslist --help
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `--help` | List installed options and plugin names. Plugin help shows its own arguments. |
| `-f memory.raw` | Supply the image. Place global arguments before the plugin name. |
| `windows.info` | Windows-specific information plugin. Use it to check the image and available context before branching further. |

If symbols are unavailable, do not treat the failure as evidence that the image lacks processes. Establish that a known-good sample works with the same installation and symbol cache while disconnected. Linux images can require matching kernel symbols which are not interchangeable with a Windows image.

### Compare Windows process views and network records

Start with the process list, then compare other views when the question warrants it. Output files below are fresh work products. Bash redirection overwrites them if they already exist.

~~~bash
vol -f memory.raw -r csv windows.pslist > processes.csv
vol -f memory.raw -r csv windows.pstree > process-tree.csv
vol -f memory.raw -r csv windows.psscan > process-scan.csv
vol -f memory.raw -r csv windows.netscan > connections.csv
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-r csv` | Select CSV output for machine-readable review. Verify headers for the installed version before parsing. |
| `windows.pslist` | Walk the list of processes exposed by supported Windows kernel structures. |
| `windows.pstree` | Show process hierarchy and parent-child relationships as reconstructed by the plugin. |
| `windows.psscan` | Use a scanning view to find process structures, which can include remnants. Treat scan-only entries as leads. |
| `windows.netscan` | Inspect network structures supported for the target image. Records can be stale or incomplete. |

Keep diagnostic output and check command status before comparing results. A CSV file can exist even when its command failed. Compare PID, process start and exit time, image name, parent and the fields available for the socket. Check how a plugin defines a timestamp before treating it as an exact observation time.

## Worked walkthrough

1. Consider three observations. A process named collector with PID 42 started at 08:00 UTC and exited at 08:15. A different process named reporter with PID 42 started at 08:20. A socket record refers to PID 42 at 08:24. Which process can plausibly own it if the times use the same clock and refer to creation?
2. Build the candidate intervals. Collector was no longer active at 08:24 and reporter had started. Reporter is the stronger candidate. That conclusion changes if 08:24 refers to when the investigator exported the record or a different source clock. Document those alternatives.
3. Add a parent PID and command-line observation from the same run if the source provides them. Explain which observation corroborates identity and which provides timeline evidence. A parent ID can also be reused, so compare both lifetimes.
4. Check a negative control by moving reporter's start time to 08:25. Now neither candidate fits. Report the observed socket record and the unresolved ownership. Avoid forcing a match just because one process has a familiar name.
5. On a permitted saved image, compare a process found in both pslist and the scan view to one found only in the scan view. Document exit time or missing evidence. If both views rely on related memory structures, treat the agreement as corroborating rather than completely independent.
6. Record artifact hash, plugin names and versions, relevant columns, timestamps, provenance and confidence. If comfortable sharing the learning outcome, use a synthetic record instead of publishing real memory content.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| Unsatisfied symbol requirement | Missing or mismatched OS/kernel symbols or incorrect parsing layer | Check image origin, target build and local cache. Test a matching known-good fixture before treating plugin output as evidence. |
| Rows but no useful process names | Wrong field, parser failure, incomplete pages or damaged structures | Use a second process view and inspect diagnostic output. |
| PID exists in two histories | PID reuse | Join on PID plus lifetime and source, and check whether clocks can be aligned. |
| Parent process absent | Parent exited, incomplete capture, or reused parent PID | Check start/exit evidence and report uncertainty rather than assigning the current occupant. |
| CSV has only header | Plugin succeeded without rows or output is partial | Check status and compare a known-good image. Empty results only constrain what was parsed. |
| Volatility works only online | On-demand symbol download or dependency missing on VM | Cache appropriate symbols and repeat the exact command offline before the event. |

## Glossary

| Term | Meaning and use |
|---|---|
| PID | Process identifier allocated by the OS and reusable after termination. |
| PPID | Parent PID as recorded by a source. Parent identity must be compared with lifetimes. |
| Kernel symbols | Metadata describing kernel types, fields and addresses needed to interpret structures. |
| Acquisition | The method that collected the memory image, with time and source metadata. |
| Plugin | Analysis routine that reads specific structures and reports an interpreted view. |
| Process list | OS-organized set of process structures traversed by a plugin. |
| Scan view | Search-driven view that can detect structures outside the normal list and can find remnants. |
| Corroboration | Support for one interpretation from a distinct observation. |
| Lifetime | Start-to-exit interval when available, with the source clock and uncertainty noted. |

## Practice, transfer and handoff

- Shift the socket time by ten minutes. Explain how missing clock provenance can change the most likely owner.
- Compare a successful known-good plugin invocation with a failed one that still creates its output file. Tell a teammate how to distinguish the two.
- Handoff using row identifiers, source plugin, timestamps and what must still be confirmed.

[Volatility 3 documentation](https://volatility3.readthedocs.io/en/latest/)

[Chapter index](README.md)
