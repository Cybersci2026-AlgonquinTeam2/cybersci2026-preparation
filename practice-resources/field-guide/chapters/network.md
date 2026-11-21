# Networking and saved packet captures

A packet capture is an observation made at a particular interface during a time interval. A target packet can exist outside that interval or at a different capture point. Start by deciding whether the question asks what was visible, what the endpoints probably did, or why communication failed. The first is directly observable. The others require assumptions and often additional evidence.

The commands below read saved files or show the local Kali VM's state. Run them in Bash. Prepare the Kali toolkit before disconnecting. Use name resolution only when permitted and useful: it can add traffic or reinterpret historical addresses using present-day information.

## Triage and decision tree

~~~mermaid
flowchart TD
    A["Record the question and preserve input"] --> Q0
    Q0{"Is the question about VM connectivity"} -- Yes --> Y0["Inspect local interfaces, addresses, routes and listeners"]
    Q0 -- No --> Q1
    Y0 --> V["Verify against control and record evidence"]
    Q1{"Is there a readable saved capture"} -- Yes --> Y1["Record duration, packet count, capture limits and protocols"]
    Q1 -- No --> Q2
    Y1 --> V["Verify against control and record evidence"]
    Q2{"Does the question identify DNS or an endpoint"} -- Yes --> Y2["Apply an explicit display filter and find both directions"]
    Q2 -- No --> Q3
    Y2 --> V["Verify against control and record evidence"]
    Q3{"Can you pair request and reply with corroborating fields"} -- Yes --> Y3["Record both frame numbers and time delta"]
    Q3 -- No --> Q4
    Y3 --> V["Verify against control and record evidence"]
    Q4{"Can you see application data"} -- Yes --> Y4["Describe exactly what was decoded"]
    Q4 -- No --> N
    Y4 --> V["Verify against control and record evidence"]
    N["Check prerequisites, capture limitations and missing evidence"]
    N --> V
~~~

Offline text equivalent:

1. **Is the question about VM connectivity** If yes, Inspect local interfaces, addresses, routes and listeners. If no, continue to the capture inventory.
2. **Is there a readable saved capture** If yes, Record duration, packet count, capture limits and protocols. If no, test the file signature and get a second copy if incomplete.
3. **Does the question identify DNS or an endpoint** If yes, Apply an explicit display filter and find both directions. If no, survey protocol hierarchy and conversations.
4. **Can you pair request and reply with corroborating fields** If yes, Record both frame numbers and time delta. If no, check capture boundary, retransmissions and alternate transport.
5. **Can you see application data** If yes, Describe exactly what was decoded. If no, report transport and handshake evidence separately.

## Run the decision tree at the terminal

~~~mermaid
flowchart TD
    Entry["Enter at the first applicable node"] --> Step1
    Step1["1. ip -br addr"] --> Result1{"Isolate local VM connectivity"}
    Result1 -->|No usable address or route| End1_0["1. Follow the matching result below"]
    Result1 -->|missing listener| End1_1["1. Follow the matching result below"]
    Result1 -->|saved capture available| Step2
    Step2["2. capinfos capture.pcapng"] --> Result2{"Inventory the entire saved capture"}
    Result2 -->|DNS present| Step3
    Result2 -->|relevant TCP flow| Step4
    Result2 -->|file unreadable or interval absent| End2_2["2. Follow the matching result below"]
    Step3["3. tshark -n -2 -r capture.pcapng -Y dns -T fields \"] --> Result3{"Find request and reply without trusting IDs alone"}
    Result3 -->|Response reverses endpoints and matches time, port/stream and question| Step4
    Result3 -->|repeated IDs| End3_1["3. Follow the matching result below"]
    Result3 -->|missing response| Step2
    Step4["4. tshark -n -r capture.pcapng -Y 'frame.number == 42' -V"] --> Result4{"Verify frames and application visibility"}
    Result4 -->|Evidence matches| End4_0["4. Follow the matching result below"]
    Result4 -->|encrypted content| End4_1["4. Follow the matching result below"]
    Result4 -->|no rows| End4_2["4. Follow the matching result below"]
~~~


Start at **1**. Each node gives the exact check, the options that affect the result, and where to go for each outcome. Filenames are placeholders for your local working copies. **Record** means save the observation and its evidence locator. **Hand off** means keep the last confirmed result and state what is missing.

### 1 · Isolate local VM connectivity

~~~bash
ip -br addr
ip route show
ip -6 route show
ss -lnt
~~~

**Options and interpretation.** `-br` gives compact addresses, `-6` selects IPv6, and `ss -lnt` shows listening (`-l`) numeric (`-n`) TCP (`-t`) sockets on your VM.

- **No usable address or route.** check VM adapter and addressing
- **missing listener.** check service and bind address
- **saved capture available.** **2**.

### 2 · Inventory the entire saved capture

~~~bash
capinfos capture.pcapng
tshark -n -r capture.pcapng -q -z io,phs
tshark -n -r capture.pcapng -q -z conv,tcp
~~~

**Options and interpretation.** `-n` disables name resolution, `-r` reads a file, `-q` suppresses packet lines and `-z` requests statistics. `capinfos` reports capture boundaries.

- **DNS present.** **3**
- **relevant TCP flow.** **4**
- **file unreadable or interval absent.** verify input and hand off with missing coverage.

### 3 · Find request and reply without trusting IDs alone

~~~bash
tshark -n -2 -r capture.pcapng -Y dns -T fields \
  -E header=y -E separator=, -E quote=d \
  -e frame.number -e frame.time_epoch -e ip.src -e ipv6.src -e ip.dst -e ipv6.dst \
  -e udp.srcport -e udp.dstport -e tcp.stream -e dns.id -e dns.flags.response -e dns.qry.name
~~~

**Options and interpretation.** `-2` requests two passes, `-Y` selects decoded frames, `-T fields` emits named `-e` fields, and `-E` sets headers, separator and quoting.

- **Response reverses endpoints and matches time, port/stream and question.** **4**
- **repeated IDs.** require all fields
- **missing response.** check capture direction and duration at **2**.

### 4 · Verify frames and application visibility

~~~bash
tshark -n -r capture.pcapng -Y 'frame.number == 42' -V
tshark -n -r capture.pcapng -Y 'tcp.stream == 3'
~~~

**Options and interpretation.** Substitute known frame and stream numbers. `-V` expands fields for the matched frame; the stream identifier belongs to this trace.

- **Evidence matches.** record source frame numbers and observed fields
- **encrypted content.** report observable transport separately
- **no rows.** clear filter and recheck capture and identifier.

## Command recipes

### Local interface and route triage

These commands answer three different questions: which interfaces have addresses, which routes exist, and which local processes are listening.

~~~bash
ip -br addr
ip route show
ss -lnt
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `ip -br addr` | Brief output. Shows interface state and addresses without full per-interface detail. |
| `ip route show` | Displays IPv4 routes by default. For IPv6 use `ip -6 route show`. |
| `ss -lnt` | Limit to listening sockets (`-l`), keep numeric endpoints (`-n`), and show TCP (`-t`). Use `ss -lnu` for UDP. |

An interface marked UP can still lack a useful address or route. A local listener on 127.0.0.1 accepts loopback traffic only. A socket bound to all interfaces is not proof that firewall policy permits a peer to reach it.

### Capture inventory and conversation survey

Read the capture without opening a live interface. Inventory before narrowing.

~~~bash
capinfos capture.pcapng
tshark -n -r capture.pcapng -q -z io,phs
tshark -n -r capture.pcapng -q -z conv,tcp
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `capinfos` | Summarizes capture metadata, time span and packet counts where available. |
| `-n` | Disable address, port and other name resolution in TShark. |
| `-r` | Read the named saved capture. |
| `-q` | Suppress routine packet listings so statistics are easier to read. |
| `-z io,phs` | Protocol hierarchy statistics. |
| `-z conv,tcp` | TCP conversations with packet and byte totals by endpoint pair. |

A high byte total makes a conversation worth investigating if the question is about transfers. It is weak evidence of a particular payload. Compare the time range and traffic direction. Capture truncation may leave headers intact while cutting payloads.

### DNS extraction and detailed replay

Use one output row per matching record and preserve the original frame identifier.

~~~bash
tshark -n -2 -r capture.pcapng -Y 'dns' -T fields \
  -E header=y -E separator=, -E quote=d \
  -e frame.number -e frame.time_epoch -e ip.src -e ipv6.src \
  -e ip.dst -e ipv6.dst -e dns.id -e dns.flags.response -e dns.qry.name

tshark -n -r capture.pcapng -Y 'frame.number == 42' -V
~~~

| Flag, option or operand | What it does and why it matters |
|---|---|
| `-2` | Two-pass analysis on an offline file, useful when fields depend on later packets. |
| `-Y` | Apply Wireshark display-filter syntax to decoded fields. It does not modify the saved capture. |
| `-T fields` | Choose tabular field output. |
| `-E header=y`, `separator=,`, `quote=d` | Add headers, choose commas, and quote fields with double quotes. Use a CSV parser if automating. |
| `-e` | Request one field by its exact dissector name. Missing layers produce empty fields. |
| `-V` | Print full packet details. Apply to a small set of frames. |
| `frame.time_epoch` | Epoch timestamp suitable for comparisons when the underlying capture clock is sound. |

Start with `dns` rather than `udp.port == 53`. DNS can use TCP and port 53 can carry other traffic. Transaction IDs are short and can repeat. Match question, transport, endpoints and timing as well. The example frame 42 is a placeholder, so replace it with one from your output.

## Worked walkthrough

1. Start with a saved allowed capture. Build a scratch note with its hash, file size, capture start and end, and question. A question like “did the resolver answer?” requires a match in the return direction.
2. Use the inventory commands. Compare total packets and time span. Decide whether the relevant client, resolver and time are likely included. If the question refers to a port, check conversations without assuming that the port is the application.
3. Export the DNS fields. Select a query row with the response bit clear. Identify the resolver, transaction ID and query name. Find the candidate answer and check direction is reversed. If there are duplicate queries, check UDP ports or TCP stream identity in the detail pane.
4. For a paper control, consider frame 18, client A to resolver B, ID 0x0042, name alpha.test; frame 19, a distinct client C to B with the same ID and name; frame 24, resolver B to A with the matching client port. Frame 24 supports pairing with frame 18. ID and name alone would also match frame 19 and give a false conclusion.
5. Check response code and record count on the paired response. A DNS error is still a reply. A reply with no matching data can be caused by record type, a negative response, or a partial capture. Report the field values and what they support.
6. Clear the display filter and inspect surrounding frames. Save the source frame references and any limitations. Do not renumber by exporting only the filtered rows and then referencing row numbers as original frames.

## Troubleshooting and verification

| Symptom | Likely explanations | Discriminating test and action |
|---|---|---|
| No DNS rows | Wrong capture, filter or encrypted DNS | Run inventory and clear filters. Report encrypted application content as unavailable unless the artifact includes legitimate decode material. |
| Source and destination fields empty | ARP, different link layer, or IPv6 fields not selected | Inspect frame detail and include the correct address family. |
| A DNS question appears unanswered | Capture boundary, packet loss, selected interface, or no reply | Check similar flows, timestamp range and whether the dataset contains return traffic. |
| Repeated TCP packets | Retransmission, repeated capture or both | Compare sequence ranges and capture interface identifiers before counting events. |
| Flow is establishment-only | Capture started late or application traffic absent | Check SYN/SYN-ACK/ACK and subsequent frames. Keep conclusions within the observed interval. |
| Packet timestamps jump | Source clock drift or multiple merged captures | Sort only after evaluating capture provenance and clock offsets. Preserve original packet order. |

## Glossary

| Term | Meaning and use |
|---|---|
| Frame | One recorded link-layer packet with capture metadata and a stable number inside the original trace. |
| Five-tuple | Source and destination addresses, ports and transport protocol. Useful for separating flows. |
| Capture filter | Selects what is collected at capture time. Packets excluded then cannot be recovered from the saved file. |
| Display filter | Selects what you see from evidence already recorded. |
| Snap length | Maximum captured bytes per packet. A truncated frame may show only headers. |
| Stream | A reconstructed conversation. Stream numbers depend on the specific trace and dissector context. |
| Retransmission | A repeated attempt to deliver transport data. Repeated packets need careful counting. |
| TTL | Time-to-live field used in forwarding or DNS cache lifetimes depending on context. |
| Capture point | The observer's interface or tap. It determines which directions and segments can be seen. |

## Practice, transfer and handoff

- Try the duplicate-ID paper control with NAT between the client and capture point. Which endpoint labels change and which evidence remains useful?
- Give a teammate a clean trace and one answer frame. Ask them to find the query without using your stream filter.
- Handoff with source hash, interval, capture point if known, filter, source frame identifiers and one observation the trace cannot support.

[TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html)

[Chapter index](README.md)
