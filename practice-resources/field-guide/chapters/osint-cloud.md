# Public-source evidence, cloud records and correlation

A public-source task asks for a claim that can be corroborated from public evidence. A cloud-log task asks which identity or service performed an operation, under which recorded conditions. Both reward more than one source and careful scope. For these exercises use provided evidence, public non-personal references and fictional local JSON. A source can be accurate today and still fail to support a statement about an earlier date.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Is the question about a location, time or an object in an image"} -- Yes --> Y0["Separate visible observations, metadata and candidate inference"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Does the image metadata contain location or time fields"} -- Yes --> Y1["Record values and seek independent corroboration"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Is there a structured cloud audit record"} -- Yes --> Y2["Project actor, action, resource, result and request ID"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Do the candidate records refer to the same request"} -- Yes --> Y3["Compare request IDs, intervals and aggregation source"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can you show an independent observation supporting the same claim"} -- Yes --> Y4["Record evidence with publication date and uncertainty"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Is the question about a location, time or an object in an image** If yes, Separate visible observations, metadata and candidate inference. If no, identify the event source and question type.
2. **Does the image metadata contain location or time fields** If yes, Record values and seek independent corroboration. If no, inspect stable non-personal features and do not infer missing precision.
3. **Is there a structured cloud audit record** If yes, Project actor, action, resource, result and request ID. If no, find provider log schema and inspect a small sample.
4. **Do the candidate records refer to the same request** If yes, Compare request IDs, intervals and aggregation source. If no, check ID namespace, retries and cross-service logging.
5. **Can you show an independent observation supporting the same claim** If yes, Record evidence with publication date and uncertainty. If no, report the candidate as unresolved.

## Command recipes

### Extract local image metadata without modifying it

Treat metadata as a hypothesis. Copy the original in a scratch directory and preserve its digest before opening with a viewer.

~~~bash
sha256sum -- photo.jpg
exiftool -a -G1 -s -time:all photo.jpg
exiftool -n -GPSLatitude -GPSLongitude photo.jpg
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-a` | Allow duplicate tags, useful for seeing competing timestamp fields. |
| `-G1` | Show the family-1 metadata group for each displayed field. |
| `-s` | Use short field names. |
| `-time:all` | Select time-related tags from metadata categories recognized by ExifTool. |
| `-n` | Disable print conversion to display underlying values in machine-oriented forms. |
| `-GPSLatitude -GPSLongitude` | Select those fields if present. Inspect reference or hemisphere fields when interpreting coordinates. |

Compare original capture metadata with edit or export times. Offset information can be missing, and the host file's modification time can reflect a download. Use a stable landmark or map corroboration for a fictional place rather than using clues to identify private people.

### Project synthetic audit records

The example creates three local JSON objects. Values are intentionally fictional and the schema is generic. A real provider can use different fields or timestamps.

~~~bash
cat > audit.jsonl <<'EOF'
{"time":"2026-01-05T17:05:00Z","id":"req-7","actor":"demo-reader","action":"read","resource":"demo:notes","outcome":"allowed"}
{"time":"2026-01-05T17:06:00Z","id":"req-8","actor":"demo-reader","action":"write","resource":"demo:notes","outcome":"denied"}
{"time":"2026-01-05T17:07:00Z","id":"req-9","actor":"demo-editor","action":"write","resource":"demo:notes","outcome":"allowed"}
EOF
jq -r '[.time,.id,.actor,.action,.resource,.outcome] | @tsv' audit.jsonl
jq -r --arg key req-8 'select(.id == $key) | [.actor,.action,.outcome] | @tsv' audit.jsonl
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-r` | Return TSV strings without surrounding JSON quotes. |
| `--arg key req-8` | Pass the request ID as a string variable rather than pasting it into filter code. |
| `select(.id == $key)` | Keep only exact matches. Multiple rows can share an ID across event stages or services. |
| `@tsv` | Escape control characters and display related fields together. |

Request 8 records a denied write by demo-reader. Request 9 is an allowed write by a different actor. A time filter alone might combine them and falsely attribute the write to the reader. In real logs, an allowed decision does not prove that a write actually committed. Use a completion event, state history or other authorized corroboration.

### Record exact text clues in local notes

Search a small directory of authorized references rather than trying to align two large exports by sight.

~~~bash
rg -n -F -- 'req-8' evidence/
rg -n -i -- 'observatory' references/
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-n` | Include line numbers in results. |
| `-F` | Search the exact text rather than interpreting pattern punctuation. |
| `-i` | Case-insensitive match. Check original spelling to verify the actual observation. |
| `--` | End option parsing. |

Keep the source file and line reference, the source timestamp and your retrieval date. Two reposts of the same source are not independent. Prefer directly observed reference material and explicitly note which facts each item corroborates.

## Worked walkthrough

1. For a fictional venue, an image shows the unique outline of a clock tower and a sign saying Observatory. The GPS tag points to a generic city center. Form two candidates based on visible geometry. Record what would disqualify each and compare another public view at a similar angle. Do not replace the image observation with its edited tag.
2. Separately read the three-record audit fixture. Predict the result of selecting req-8 before running the command. Compare the `actor`, `action` and `outcome` fields rather than attributing all writes in the same period to one actor.
3. Add a second fictional observer log reporting object version 4 after req-9. Explain why it strengthens the conclusion only if it references the same object and request. If the version number is alone, it proves a version exists but does not identify the writer.
4. Re-evaluate a mismatch. A local time with −05:00 offset might correspond to a UTC audit record five hours later. Preserve both original strings, map both to UTC and compare source precision before declaring either incorrect.
5. Write an evidence record that separates the question, sources, observation, inference and uncertainty. Ask a teammate to reconstruct the claim without seeing your proposed conclusion.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| No coordinates | Missing or stripped metadata | Use observable features and record reduced precision. |
| Several images show the same place | Mirrors or reused public photos | Identify the original source or use genuinely independent corroboration. |
| Nearby times imply same event | Clock offsets or separate requests | Use IDs, actors, objects and window boundaries. |
| Two events with the same ID disagree | Lifecycle stages, provider namespaces or replay | Compare stage, service and source rather than collapsing them. |
| Actor looks like a person but is a service role | Assumed identity based on display label | Check provider fields and delegated identity provenance. |
| Allowed appears in the log but object has not changed | Authorization and successful commit are distinct events | Look for completion evidence and check read consistency and time range. |

## Glossary

| Term | Meaning and use |
|---|---|
| OSINT | Analysis of publicly accessible information. This exercise emphasizes non-personal, corroborated facts. |
| Attribution | Linking an action to an actor using evidence and explicit assumptions. |
| Audit event | Log entry describing an attempted or completed action according to a provider's schema. |
| Principal | Identity that can request access, including a service or delegated role. |
| Request ID | Identifier for correlation within a defined system or propagation scope. |
| Provenance | Origin, collection and handling history of evidence. |
| EXIF | Metadata structure often used in images. Editable and commonly stripped. |
| Corroboration | Supporting the same interpretation through a distinct line of evidence. |

## Practice, transfer and handoff

- Compare two matching photos copied from one archive against a separate map survey. Which are independent?
- Extend the JSON fixture with a denied result followed by a success for the same resource and different request. Document how your filter avoids mixing them.
- Handoff with sources, version/date, observations, unmatched alternatives and confidence.

[ExifTool documentation](https://exiftool.org/exiftool_pod.html) · [jq manual](https://jqlang.org/manual/)

[Chapter index](README.md)
