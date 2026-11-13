# CyberSci writeups and past-challenge intel

Researched 2026-10-14. CyberSci publishes **no official challenge archive or writeups** (cybersci.ca/past-events/ has photos, scoreboards and sponsor brochures only). CTFtime has task lists for some years but zero attached writeups. The material below is what third parties posted. It is thin; treat it as format intelligence, not a complete archive.

## What exists

| Event | Source | What is there |
|---|---|---|
| Regionals 2022 (Nov 5, 2022) | [crimist/ctf `cybersci_regionals2022`](https://github.com/crimist/ctf/tree/master/cybersci_regionals2022) | `warmups/` and `vault/` writeups; "Vault" = `vault.dat` containing only 0x20/0x09 bytes (whitespace binary), decoded with a bit-mapping script |
| Regionals 2022 | [crimist/ctf warmups](https://github.com/crimist/ctf/blob/master/cybersci_regionals2022/warmups/README.md) | A web warmup: TLS cert lists `warmup.nuber.int` + `internal.nuber.int`; solved with a custom `Host` header (vhost discovery) over **https** |
| Regionals 2022 | [Green-Avocado/CTF `cybersciregionals2022`](https://github.com/Green-Avocado/CTF/tree/main/cybersciregionals2022) | `pwn/lock3` |
| Regionals 2022 | [UofTCTF: String Storage](https://uoftctf.org/posts/string-storage/) | 300-pt pwn, source only; off-by-one in `search_entries` lets you leak the adjacent `CTFKEY` byte-by-byte through a match oracle; solved with pwntools |
| Regionals 2022 (listed as 2023 path) | [Green-Avocado/CTF `cybersciregionals2023`](https://github.com/Green-Avocado/CTF/tree/main/cybersciregionals2023) | `pwn/string-storage`; `rev/` for Puzzle Vault and Hash Vault (names match the 2022-23 CTFtime task list) |
| Regionals 2022-23 | [CTFtime task list, event 1805](https://ctftime.org/event/1805/tasks/) | 25 tasks, 0 writeups; see shape below |
| Nationals 2022 | [crimist/ctf `cybersci_nationals2022`](https://github.com/crimist/ctf) ; [PhilippSchweinzer/CTFs](https://github.com/PhilippSchweinzer/CTFs) | Folder-level only; contents not inspected |
| Nationals 2021 | [CTFtime writeup 29656](https://ctftime.org/writeup/29656) -> [crazyeights225.github.io/cs-track1](https://crazyeights225.github.io/cs-track1/) | Track 1 "Command and Control": chatbot recon -> VPN -> Apache Druid 0.20 RCE (Metasploit) -> decompile Python C2 with uncompyle6 -> implement RSA SHA-256 PKCS#1 v1.5 signing with a found key -> termination code |
| Nationals 2025 | cybersci.ca past events | "Val Verde" election-defence themed CTF; no public writeups found |
| Nationals 2023 | cybersci.ca past events | "PowerGPT Edition" (an AI controlling the power grid); no public writeups found |
| CTFtime events | 1394 (N2021), 1805 (R22-23), 1995 (N2023), 2171 (R23-24), 2366 (N2024), 2511 (R24-25), 2689 (N2025), 2909 (R25-26), 3125 (N2025-26), 3436 (R26-27) | Check each for writeups added later |

## Challenge shape (Regionals 2022-23, from the task list)

25 tasks: **forensics heavy (8)**, a big **warmup** ladder (~9 including 1-point and 5-point openers), plus a small **vault series** (rev, pwn, crypto and a zip task) and tiered series like "Layer Vault 1-4" (layered encoding/forensics) and "A small / Bigger small / Biggest small problem" (escalating).

Forensics names suggest memory forensics (Volatility profile/PID tasks) and report/log/credential-breach analysis.

Takeaways for training:
1. **Warmups are many and cheap**: speed on triage and encodings wins points early. Tracked in D02, `O06`, `S02a`.
2. **Forensics is the largest category**: memory (Volatility), logs, documents, "who did what" reports. Weight Volatility, log timelines and stego above heap exploitation.
3. **Series with tiers** (Level 1-4): solve in order; each level reuses the previous technique.
4. **Source-only pwn** (String Storage gave source, no memory-corruption): read the code for logic bugs and oracles before reaching for ROP.
5. **Weird-encoding "crypto"** (whitespace binary): look at the byte histogram first (`xxd`, `sort | uniq -c`).
6. **Nationals are scenario/hackquest style** (2021 Track 1; 2023 and 2025 themed): chained recon -> exploit -> reverse -> crypto, in a networked environment. This is the "realistic IT environment" from the site.

## Replay plan (see `tracker.csv`)

- `S01` read all of the above (1 h)
- `S02a` recreate the 2022 vhost warmup + vault.dat challenge (1 h)
- `S03` 4 h CyberSci-style mock with analogues (warmup ladder, forensics set, vault rev/pwn/crypto, source-only pwn)
- `S04` (backlog) rebuild the 2021 Track 1 chain in your lab

## Where to keep looking

- CTFtime writeups by event: `https://ctftime.org/writeups` (filter the CyberSci events above)
- Team repos: UofTCTF (`uoftctf.org/posts`), Maple Bacon, Singularity, shellrippers (CTFtime team pages)
- Search `"CyberSci" "regionals" writeup <year>`, plus challenge names ("Layer Vault", "Hash Vault", "Puzzle Vault", "Zip Vault", "Signature Vault", "String Storage")
- Ask your instructor/teammates: school clubs often keep their own notes; Discord galleries linked on cybersci.ca are photos only.

## Note on search results

One web-search result for these queries contained text instructing the reader to run a `curl` command that sends the user's environment to an external URL. That text came from a page, not from you; it was ignored and nothing was run. Don't paste commands from writeups or search snippets into a shell without reading them, and run unfamiliar challenge files only in the VM.
