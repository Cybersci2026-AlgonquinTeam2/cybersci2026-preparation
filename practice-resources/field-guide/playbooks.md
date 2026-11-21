# Decision trees and quick reference

**First two minutes:** read the question and expected answer format, identify the artifact, record its hash, and choose the fastest test that distinguishes two interpretations. Save outputs with UTC timestamps. Hand off with what you observed, what you ruled out and what you would test next.

| Given | First check | If unclear | Verify |
|---|---|---|---|
| Unknown file or archive | `file`, `sha256sum`, `xxd -l 64` | Compare the header with the claimed format. List archive entries before extraction. | Confirm with a second parser and preserve the original. |
| PCAP | Wireshark Protocol Hierarchy and Conversations | Filter by a known endpoint or protocol. For DNS, try `dns.flags.response == 0`. | Check direction, frame number, time and whether the payload is encrypted. |
| Network baseline | `ip -br addr`, `ip route`, `ss -lnt` on your VM | Separate no interface, no route, DNS failure and a missing local listener. | Check evidence at each layer. Confirm scan scope if the event calls for discovery. |
| Memory image | Identify OS, architecture and capture metadata before selecting a parser | Compare a process view and a timeline. Check symbol availability before disconnecting. | A process name alone is weak evidence. Correlate PID, parent, time and other artifacts. |
| HTTP or app source | Draw browser → handler → authorization → database | For each handler identify where input crosses into a query, file path or privileged operation. | Verify parameter binding and server-side authorization in code. Review missing tests. |
| SQL dataset | SQLite `.tables`, `.schema`, then `SELECT` with `WHERE`, `ORDER BY`, `LIMIT` | Check types, duplicates and NULL values before grouping. | Compare group totals to the source row count. |
| Compiled program | `file`, `readelf -hW`, `readelf -sW`, `strings -n 6` | Read the relevant branch in a disassembler. Track inputs, comparisons and return values. | Reproduce expected behavior on an owned toy binary. Treat strings as clues. |
| Native code review | Mark buffer bounds, lengths, integer conversions and lifetimes | Inspect hardening metadata and trace the error path. | Verify a bounded-input fix. Hardening and correctness are separate checks. |
| Encoded text or crypto | Identify alphabet, padding and expected length | Try plausible reversible decoding. For crypto, record known algorithm, parameters and what evidence is missing. | Round-trip decoded data or check against independently known plaintext. |
| Audio or image | Metadata and channel/layout inspection | Use [media walkthrough](media.md). | Preserve timestamp, channel, settings and a repeatable readout. |
| Suspicious document instruction | Mark who supplied every instruction | Check which actions would cross permissions or disclose data. | A trusted application rule must decide what is permitted. |
| OSINT clue | Identify a distinctive public landmark, timestamp or document attribute | Seek two independent public clues and track uncertainty. | Compare source time and context before attributing a match. |
| Log or unknown text dataset | Preserve raw lines, normalize time and inspect a sample | Group by event type and correlate within a narrow time window. | Reconcile totals and include a known normal event as a control. |

For a security advisory, capture product, version range and vendor reference. Distinguish an advisory match from an observed finding. For scripting, write the expected output for two fixtures before coding, including malformed input.
