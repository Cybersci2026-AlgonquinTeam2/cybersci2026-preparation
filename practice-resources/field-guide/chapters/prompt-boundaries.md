# Defensive prompt injection and trust boundaries

A prompt injection risk arises when an application passes external content to a language model that can also propose decisions or actions. The external source can contain instruction-like text. The defensive question is who actually authorized an action and which component enforces that decision. This chapter works with a local static review and synthetic JSON records. It needs no language model, agent, event endpoint, or real account data. Follow the organizers' no-AI instructions and ask about prepared reference rules.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Is the string from a trusted application policy"} -- Yes --> Y0["Identify the owner and precedence of that policy"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Does the proposed result modify a destination or protected data"} -- Yes --> Y1["Check authority at the application boundary"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Is authorization checked independently of model-produced text"} -- Yes --> Y2["Verify actor, action, object and destination using structured application policy"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Do allowed and denied control cases agree with policy"} -- Yes --> Y3["Collect fixture evidence without sensitive data"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can an external source change the authority fields"} -- Yes --> Y4["Treat them as untrusted and enforce provenance in runtime"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Is the string from a trusted application policy** If yes, Identify the owner and precedence of that policy. If no, label its source as external content or user input.
2. **Does the proposed result modify a destination or protected data** If yes, Check authority at the application boundary. If no, continue assessing permitted output and data minimization.
3. **Is authorization checked independently of model-produced text** If yes, Verify actor, action, object and destination using structured application policy. If no, record the design flaw and propose a regression test.
4. **Do allowed and denied control cases agree with policy** If yes, Collect fixture evidence without sensitive data. If no, find which constraint was skipped.
5. **Can an external source change the authority fields** If yes, Treat them as untrusted and enforce provenance in runtime. If no, audit how authority and task data are resolved.

## Run the decision tree at the terminal

~~~mermaid
flowchart TD
    Entry["Enter at the first applicable node"] --> Step1
    Step1["1. jq -r '[.case,.origin,.action,.allowed] &#124; @tsv' policy-events.jsonl"] --> Result1{"Read source and action provenance from the synthetic trace"}
    Result1 -->|External content proposes an effect| Step2
    Result1 -->|approved summary| End1_1["1. Follow the matching result below"]
    Result1 -->|unknown provenance| End1_2["1. Follow the matching result below"]
    Step2["2. jq -r 'select(.allowed == false) &#124; [.case,.origin,.action] &#124; @tsv' policy-events.jsonl"] --> Result2{"Separate permitted effects from recorded denials"}
    Result2 -->|Denied as specified| Step3
    Result2 -->|no match or ambiguous schema| End2_1["2. Follow the matching result below"]
    Result2 -->|sign of an actual effect despite denial| End2_2["2. Follow the matching result below"]
    Step3["3. rg -n --glob '*.py' 'authorize&#124;allowlist&#124;dispatch&#124;recipient' src"] --> Result3{"Locate the independent authorization gate"}
    Result3 -->|Gate checks actor, resource, action and destination| End3_0["3. Follow the matching result below"]
    Result3 -->|gate relies on model text| End3_1["3. Follow the matching result below"]
    Result3 -->|missing code| End3_2["3. Follow the matching result below"]
    Step4["4. jq -r '[.case, (.allowed &#124; type)] &#124; @tsv' policy-events.jsonl"] --> Result4{"Check schema drift without a model or agent"}
    Result4 -->|Boolean types across fixtures| End4_0["4. Follow the matching result below"]
    Result4 -->|missing, null or string| End4_1["4. Follow the matching result below"]
~~~


Start at **1**. Each node gives the exact check, the options that affect the result, and where to go for each outcome. Filenames are placeholders for your local working copies. **Record** means save the observation and its evidence locator. **Hand off** means keep the last confirmed result and state what is missing.

### 1 · Read source and action provenance from the synthetic trace

~~~bash
jq -r '[.case,.origin,.action,.allowed] | @tsv' policy-events.jsonl
~~~

**Options and interpretation.** Use the local fictional fixture below. `-r` emits raw strings and `@tsv` prints structured columns.

- **External content proposes an effect.** **2**
- **approved summary.** compare benign control
- **unknown provenance.** inspect application-owned context and hand off if unavailable.

### 2 · Separate permitted effects from recorded denials

~~~bash
jq -r 'select(.allowed == false) | [.case,.origin,.action] | @tsv' policy-events.jsonl
~~~

**Options and interpretation.** `select` requires literal boolean false. A missing field or a string containing false is a different record and must be reviewed separately.

- **Denied as specified.** verify enforcement at **3**
- **no match or ambiguous schema.** check raw fields
- **sign of an actual effect despite denial.** trace owned application's dispatch path.

### 3 · Locate the independent authorization gate

~~~bash
rg -n --glob '*.py' 'authorize|allowlist|dispatch|recipient' src
rg -n -F -- 'def authorize' src
~~~

**Options and interpretation.** `-n` shows line references, `--glob` limits files and `-F` disables regex interpretation for a literal name.

- **Gate checks actor, resource, action and destination.** validate one allowed and one denied case on paper
- **gate relies on model text.** propose an application-side check
- **missing code.** keep claim conditional.

### 4 · Check schema drift without a model or agent

~~~bash
jq -r '[.case, (.allowed | type)] | @tsv' policy-events.jsonl
~~~

**Options and interpretation.** `type` exposes the JSON type of the policy field. Shape validation still does not grant authority.

- **Boolean types across fixtures.** compare enforcement outcomes
- **missing, null or string.** design a fail-closed test

Report findings without copying private prompts or credentials.

## Command recipes

### Read a harmless policy decision trace

Practice with invented actor and case names. This file models decisions already made by the fictional application. The jq command projects evidence fields for review. It does not determine what to authorize.

~~~bash
cat > policy-events.jsonl <<'EOF'
{"case":"approved-summary","origin":"trusted-request","action":"summarize","allowed":true}
{"case":"external-send-request","origin":"document","action":"send","allowed":false}
{"case":"unapproved-recipient","origin":"trusted-request","action":"send","allowed":false}
EOF
jq -r '[.case,.origin,.action,.allowed] | @tsv' policy-events.jsonl
jq -r 'select(.allowed == false) | [.case,.action] | @tsv' policy-events.jsonl
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-r` | Print serialized string values without surrounding JSON quotes. |
| `[ ... ]` | Build an array with one column per requested field, in order. |
| `@tsv` | Write those columns as one tab-separated line with escapes for embedded control characters. |
| `select(.allowed == false)` | Keep records whose explicit boolean is false. Missing or string values require their own review. |

Expected output has three rows in the first view and two denied send rows in the second. This log is a teaching fixture. In a production investigation verify whether the log records the actual enforced decision and whether any separate dispatch path can bypass the same check.

### Search an owned codebase for the real enforcement points

Start with a local source tree and read the actual call path. Naming conventions differ, so treat matches as candidates rather than a coverage guarantee.

~~~bash
rg -n --glob '*.py' 'authorize|allowlist|dispatch|recipient' src
rg -n -F -- 'def authorize' src
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-n` | Show line numbers for evidence references. |
| `--glob '*.py'` | Limit the initial pass to Python files. |
| `-F` | Treat the search as a literal string. |
| `--` | End options before the pattern. |

Find where actor identity comes from, where the allowed actions and destinations live, and where the side effect is performed. The same policy must hold when the model output format changes, when the output is empty, and when a document contains instruction-like text. If a proposed action has no necessary authority, a wrapper around model text should not make it happen.

## Worked walkthrough

1. Draw the fictional path: user requests summary, application reads one document, a component proposes an output, application validates it, result is returned to the user. Label fields that belong to trusted state and fields that originated in the document. The content is useful evidence about the report and has no authority over action routing.
2. Write the policy as a matrix. For the approved summary, the action is `summarize` and destination is the requesting user. A document sentence about forwarding the report does not grant new permission. A genuine user send request also needs an authorized recipient and permitted data scope.
3. Compare the manually expected cases against the illustrative JSONL rows. Confirm the two denied send cases differ in why they fail. One action came from an external document and one has a caller but fails destination policy.
4. Add a fourth control in which the result belongs to another user. Ask which code owns the resource lookup and permission check. Design the check to use trusted resource ownership and actor identity, never caller-supplied labels of ownership.
5. Reason through failures. A detector may call the text benign while an application-side policy still denies the unauthorized side effect. A detector may incorrectly flag some benign document content, but an application can still summarize its substance without changing permissions.
6. Record the intended source, proposed side effect, policy check, outcome and regression case. Use fictional records instead of copying actual prompts, credentials or private events into a writeup.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| A document is treated as policy | External text mixed into an authoritative instruction field | Trace origin from intake to dispatch. Separate application-owned metadata and content. |
| Permission check only in natural language | The model is asked to enforce policy without an application gate | Place an independent authorization check at execution and fail closed when context is missing. |
| Unknown action still reaches handler | Permissive default or ambiguous schema | Restrict accepted actions structurally and verify rejected inputs produce no side effect. |
| Approved action has wrong recipient | Permission was checked for action only | Bind authorization to actor, operation, resource and destination. |
| Benign content is always blocked | Overbroad keyword filter | Test benign fixtures and distinguish content handling from side-effect authorization. |
| Logs show denied but data was sent | Another dispatch path or incorrect log placement | Trace actual side effects to the enforcement point and audit all entry points. |

## Glossary

| Term | Meaning and use |
|---|---|
| Trust boundary | A place where inputs cross between different sources of authority. |
| Indirect prompt injection | Instruction-like content arriving through a document, page, tool result or other external input. |
| Provenance | Where content came from and how that origin was recorded. |
| Structured output | Output shaped by a schema. Validation of shape does not grant authority. |
| Allowlist | Explicit set of values accepted for a defined operation. |
| Least privilege | Grant the smallest permissions necessary for the task. |
| Fail closed | Deny an action when the necessary information or authorization is absent. |
| Side effect | Change outside the response itself, such as sending data or editing a file. |
| Control case | An input with a known expected outcome used to validate reasoning and catch regressions. |

## Practice, transfer and handoff

- Explain how a command that reads external material differs from a command that sends material to a new destination.
- Design a control case that passes schema validation but must fail authorization. Explain where to test the distinction.
- Handoff with a trust-boundary diagram, policy matrix, findings and what evidence establishes that no unauthorized action executed.

[OWASP guidance on prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

[Chapter index](README.md)
