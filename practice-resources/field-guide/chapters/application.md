# Web, HTTP and SQL review

Start with a request you can explain end to end: method, path, identity, input values, server decision, returned data. A response code describes how a request finished, while authorization is the server's decision about one actor and one resource. For practice, use an owned static local server and a scratch SQLite database. The application review portion uses source and test cases to reason about flaws and fixes.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Do you have a captured request or local fixture"} -- Yes --> Y0["Record method, URL, redirects, code, headers and content type"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Does the response contain the expected format"} -- Yes --> Y1["Inspect a small structured sample"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Is there a server side resource decision"} -- Yes --> Y2["Identify actor, action and object and inspect policy placement"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Does user input reach a query"} -- Yes --> Y3["Verify parameter binding and expected type"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Do normal and denied cases behave as specified"} -- Yes --> Y4["Record test conditions and observed result"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Do you have a captured request or local fixture** If yes, Record method, URL, redirects, code, headers and content type. If no, trace the request structure in source or reconstruct a benign local fixture.
2. **Does the response contain the expected format** If yes, Inspect a small structured sample. If no, check whether the body is a redirect page or an error page.
3. **Is there a server side resource decision** If yes, Identify actor, action and object and inspect policy placement. If no, map storage and distinguish parsing from authorization.
4. **Does user input reach a query** If yes, Verify parameter binding and expected type. If no, look at the output context and expected encoding.
5. **Do normal and denied cases behave as specified** If yes, Record test conditions and observed result. If no, identify which assumption fails first.

## Command recipes

### Owned HTTP fixture and response inspection

Create a scratch directory with a small index.html. In one terminal start the server below. In a second terminal request the fixture. Use a fresh header and body filename for each check. Stop the server with Ctrl+C.

~~~bash
python3 -m http.server 8000 --bind 127.0.0.1

# Run the following from a second terminal.
curl -sS --max-time 5 -D headers.txt -o body.html \
  -w 'status=%{http_code} type=%{content_type}\n' http://127.0.0.1:8000/
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-m http.server` | Run the standard-library development server for files in the current directory. |
| `8000 --bind 127.0.0.1` | Use port 8000 and bind only to loopback. Do not serve sensitive files. |
| `-sS` | Hide progress but retain errors. |
| `--max-time 5` | Bound total operation time in seconds. |
| `-D headers.txt` | Write received headers to a separate file. |
| `-o body.html` | Write body bytes to the named output. |
| `-w` | Print selected transfer fields after the request, even though body went to file. |

Compare `/` with a nonexistent local filename. Expect 200 for an existing index and 404 for the missing path. Both may have HTML bodies. By default curl can exit successfully after receiving an HTTP error response, so use the reported status and check transport errors separately. For API review in a browser, observe Network request method, response code and Initiator without sharing cookies or tokens.

### SQLite schema and read-only analysis

Use a scratch database you create, and inspect it through a new read-only connection. The source lines below are commands for Bash.

~~~bash
sqlite3 review.db "CREATE TABLE events(kind TEXT); INSERT INTO events VALUES ('ok'),('warn'),('warn'),(NULL);"
sqlite3 -readonly review.db '.schema events'
sqlite3 -readonly -header -column review.db \
  'SELECT kind, COUNT(*) AS rows, COUNT(kind) AS non_null FROM events GROUP BY kind ORDER BY kind;'
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-readonly` | Open the database in read-only mode. Database side files and acquisition circumstances can still affect which committed state is visible. |
| `-header -column` | Print headings and human-readable aligned columns. |
| `.schema events` | SQLite shell dot-command to display schema, not a SQL statement. |
| `COUNT(*)` | Counts result rows within a group. |
| `COUNT(kind)` | Counts non-NULL kind values. Compare the NULL group with the all-row count. |
| `GROUP BY` / `ORDER BY` | Group aggregates by kind and define deterministic display order. |

The NULL group has one row and zero non-NULL kinds. The warn group has two rows, and ok has one. A blank displayed field might be NULL or a zero-length string. Inspect `kind IS NULL` and length to distinguish them. Compare the sum of group sizes to the source row count.

### Safe static review of an owned source tree

Use a local search to find candidate areas for manual review. Names vary by framework, so use the application's actual abstractions once you find them.

~~~bash
rg -n --glob '*.py' 'execute\(|authorize\(|request\.' src
rg -n -F -- 'read_report' src
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-n` | Show line numbers for evidence references. |
| `--glob '*.py'` | Limit candidates to Python files in this search. |
| `-F` | Treat the search pattern as literal rather than a regex. |
| `--` | End option parsing before the pattern. |

Search results do not prove a vulnerable flow. Walk from entry point through parsing, identity, policy, data access and response. Find a legitimate case and a denied case in tests. Check how path normalization, escaping and bound parameters are handled at the relevant boundary.

## Worked walkthrough

1. Read the route contract for a fictional `GET /reports/{id}`. An authenticated owner may read a report. Another ordinary user may not. An invalid ID must follow the declared error policy. Give each rule a test case and a result you can distinguish.
2. Now review the pseudocode `read_report(actor, id) → load_report(id) → response`. The loaded object is never compared against actor permissions. Identity at the endpoint does not establish access to the requested object.
3. Design the server check using explicit actor, object and action. Make parsing reject malformed identifiers. Call an authoritative policy before serializing or returning protected fields. If a database query uses a placeholder, verify the ID arrives as a bound argument instead of text interpolation.
4. Repeat the owner case and denied case. Add a deleted object and an anonymous actor. Some policies intentionally use the same response for missing and denied objects. Evaluate actual policy before using status alone as proof.
5. Compare returned fields as well as status. A response can deny the primary action while still exposing a name in an error body or logs. Verify that the amount of returned data is consistent with policy.
6. Document the call path, observed code and test result. Avoid including live cookies, credentials or protected records in shared notes.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| Connection refused | Fixture server not running or wrong interface/port | Check the server console and local listener, then repeat with the known URL. |
| HTML where JSON expected | Error page, wrong route, or login redirect | Check status, Content-Type, and initial Location before following redirects. |
| Valid user sees wrong object | Object-level authorization absent or at wrong layer | Trace resource ID and actor into the same policy check and compare expected tests. |
| SQL count increases after join | One-to-many join duplicates base rows | Compare row counts before and after each join, and use stable IDs. |
| A NULL field looks blank | Formatting obscures a missing value | Select `column IS NULL` as a separate projection. |
| Search returns no matches | Wrong root, ignores or different framework naming | Inspect file inventory, then start from a known route declaration. |

## Glossary

| Term | Meaning and use |
|---|---|
| Method | HTTP operation supplied by a client. A name like GET does not enforce policy by itself. |
| Content-Type | Declared representation of a body, useful for choosing a parser. |
| Authentication | Establishing who the caller is. |
| Authorization | Checking whether that caller may perform an action on the specific resource. |
| Input validation | Ensuring an input conforms to defined types, lengths or allowed values. |
| Parameter binding | Passing SQL values separately from query structure. |
| Output encoding | Representing data safely for a particular rendering context such as HTML text. |
| NULL | SQL marker for absent or unknown value. It affects predicates and aggregates. |
| Object identifier | An address for a resource. Knowing the identifier does not grant access. |

## Practice, transfer and handoff

- Compare response metadata for the real index and missing-file control. Explain why a successful network transfer can carry an HTTP failure.
- Design an owner/non-owner/same-group matrix and justify which rows should succeed under two plausible policies.
- Handoff with request identity redacted, route, exact policy, returned fields and test outcome.

[SQLite command-line docs](https://www.sqlite.org/cli.html) · [curl manual](https://curl.se/docs/manpage.html)

[Chapter index](README.md)
