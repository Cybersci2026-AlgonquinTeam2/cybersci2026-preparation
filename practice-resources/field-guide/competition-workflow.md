# Offline triage, command mechanics and team handoff

Use this page as the entry point when several tasks arrive together. The domain manuals explain the commands. This page explains how to decide which one to run, how to interpret the result and how to leave evidence another person can use. Confirm current event rules before bringing prepared materials. The existing repository records a no-AI competition instruction.

## Pick the next action

~~~mermaid
flowchart TD
    A["Read question, scope and expected submission format"] --> B{"Artifact supplied?"}
    B -- Yes --> C["Preserve original and inventory its type"]
    B -- No --> D{"Code or scenario supplied?"}
    D -- Yes --> E["Map inputs and relevant decision in source"]
    D -- No --> F["Confirm instructions and what evidence is available"]
    C --> G{"Format and question agree?"}
    G -- Yes --> H["Choose the relevant manual and a narrow observation"]
    G -- No --> I["Compare signature and second parser before transforming"]
    E --> J["Predict a result and choose a benign control"]
    H --> J
    I --> J
    F --> J
    J --> K{"Distinguishes the top two explanations?"}
    K -- No --> L["Design a better observation or record evidence missing"]
    K -- Yes --> M["Run, record exact command and status, compare control"]
    M --> N{"Can another person reproduce the conclusion?"}
    N -- Yes --> O["Record result and hand off for verification or submission"]
    N -- No --> L
~~~

**Offline route.** Read scope and output format. Preserve the supplied artifact and classify it before selecting the manual. For code, trace input to the decision before judging the output. Write down two plausible explanations and choose a test that treats them differently. If it succeeds, record enough detail to replay it. If it fails, find which premise was wrong and decide whether to hand off.

| When you see | Ask | Use |
|---|---|---|
| File extension and parser disagree | What bytes and structure support each proposed type? | [File evidence](chapters/evidence.md) |
| Capture shows a request but no reply | Was the return path visible in the same time window? | [Networking and PCAP](chapters/network.md) |
| Process identifier repeats | Which instance was alive at the event time? | [Memory](chapters/memory.md) |
| App response is surprising | Which request, policy and data interpretation produced it? | [Web and SQL](chapters/application.md) |
| ELF strings seem to give an answer | Which executed branch could reference that string? | [Static analysis](chapters/binary.md) |
| Text appears encoded | What syntax and output justify the transform? | [Crypto and scripting](chapters/crypto.md) |
| Sound has structure or an image appears blank | Does it live in time, frequency, channel or metadata? | [Media analysis](chapters/media-analysis.md) |
| Instruction-like text comes from a report | Which component authorizes any resulting action? | [Prompt boundaries](chapters/prompt-boundaries.md) |
| Several records could describe the same object | Which independent fields corroborate timing and identity? | [OSINT and cloud records](chapters/osint-cloud.md) |

## Read Bash command examples accurately

Run examples from a scratch directory in the Kali VM. Check the filename and tools first. Commands with `<<'EOF'` create sample files. Commands with `>` can overwrite the named output. When a tool offers a no-overwrite option, its spelling belongs to that tool. For example, FFmpeg's `-n` refuses to overwrite, TShark's `-n` disables resolution, and `rg -n` shows line numbers. Read options by command, not from a universal list.

~~~bash
pwd
command -v python3
python3 --version
ls -l -- 'sample with spaces.txt'
sha256sum -- 'sample with spaces.txt'
~~~

`pwd` prints the working directory. `command -v` shows how Bash resolves a command. `--version` here asks Python for its version. `ls -l` shows details. The `--` marker ends option parsing for these GNU tools, and single quotes keep spaces in the filename within one argument. The source file must exist before these commands run.

`|` passes standard output from one command to standard input on the next. It does not automatically pass errors. `>` writes standard output to a file, while `2>` writes standard error. If a tool fails but still creates a partial file, a downstream parser may return a plausible-looking count. In Bash, `set -o pipefail` makes a failed stage visible in the pipeline status. Capture `$?` immediately after the command you care about. An exit status of zero records successful completion according to the tool, not proof that your inference is correct.

When an option is unfamiliar, read `COMMAND --help` or `man COMMAND` if available offline. Check that the tool version supports the option. If the short form is ambiguous, prefer the documented long form when there is one. For derived files, record whether you resampled, filtered, truncated, reordered or changed data types. A later analyst should know which parts of the original can no longer be recovered.

## Worked handoff

You receive a stereo WAV and a short log. The log says a message begins around 5 seconds. The WAV sounds quiet in mono. Two hypotheses fit. The content may be very low amplitude in both channels, or opposite components may cancel when summed. Measure or listen to the left and right derivatives at low volume. If both contain a clear tone but sum is quiet and difference is strong at the same time, cancellation is the better explanation. Preserve the timestamp from the original file rather than a derivative that starts at zero.

Now apply the same lesson to a DNS capture. A filter showing only query packets can make an interval look unanswered. Clear the filter and inspect both directions. If the capture point did not see the reply at all, the missing response cannot be recovered from the saved trace. In both examples, verify what was removed by the representation before attributing absence to the underlying system.

Write the handoff on one screen:

```text
Question and expected answer:
Owner and check-in time:
Artifact, SHA-256, source and time range:
Observation and exact command or GUI settings:
Expected result, actual result and exit status:
Best interpretation and one alternative:
Control result:
Next discriminating test and who owns it:
```

If another person cannot repeat the command or locate the source frame, byte or time interval, the evidence note is incomplete. If the test result depends on a missing tool, state that explicitly and hand off with the input and what the next test is expected to show. Keep live event evidence and flags in approved private storage.
