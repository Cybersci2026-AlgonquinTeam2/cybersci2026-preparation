# 25. CyberSci past challenges: the activity book

The organizers publish every past challenge after each event: **`github.com/CyberSCI/PastChallenges`** (licence: AGPL-3.0; "released to the public for education purposes"). It's the single best preparation for the Nov 21 regionals because it shows the *actual* style, difficulty and themes. A local copy is at `external/PastChallenges/challenges/`.

> **Safety first.** Treat the repo as untrusted data. **Read** READMEs and source; **don't run** anything on your main machine. Run vulnerable services only in a lab VM or Docker with ports bound to `127.0.0.1`, after reading the compose file. I read descriptions and walkthrough text only; **I have not run any challenge** from the repo.

> **Spoilers.** Each challenge folder has a README with the flag and a walkthrough behind `<details>` blocks. Don't open them until after Attempt 1. This chapter keeps flags out and puts approach summaries in a clearly marked section at the end.

## 1. What the past regionals tell you

| Year | Theme | Categories in the repo | Flavour |
|---|---|---|---|
| 2024/25 | "Val Verde" election story | cloud, crypto, defence, forensics, pwn, RE, web | web apps, crypto misuse, three pwn, implant hunting, defence services |
| 2025/26 | post-apocalyptic "great reset": old tech | **AI**, crypto, defence, forensics, RE, web, warmups, pwn | Enigma, punched cards, a 16-bit DOS program, a BASIC web app, gopher/FTP, an AI prompt-injection challenge |

**Patterns worth planning around**

1. **Crypto is heavy and varied** (Enigma, AES-PCBC block swaps, piecewise RSA, RC2, vanity codes, Morse/Base32 layers). Know classical codes and common modes' weaknesses.
2. **Retro/odd formats** (punched cards, DOS, BASIC, gopher): the skill is *researching an unfamiliar format fast*.
3. **A defence challenge** every year (patch a vulnerable service).
4. **Web chains** (file upload → webshell → read file; JWT bypass → SQLi).
5. **An AI challenge** appeared in 2025/26 (prompt injection against a vision-language model).
6. **Warmups** exist; clear them first.

## 2. How to use this book

Use the workflow from chapter 23: **Read → Attempt 1 → Review → Reinforce → Attempt 2 → Review 2.**

| Step | For a past challenge |
|---|---|
| Read | the "Reading first" links below (10-15 min) |
| Attempt 1 | read only the challenge description + release files; time box 45-60 min |
| Review | open the README walkthrough; write the first thing you missed |
| Reinforce | re-read the linked sections; 5 flashcards |
| Attempt 2 | a *related* challenge from the "Attempt 2" column, with less time |
| Review 2 | note whether you recognised the pattern faster |

## 3. Start here: files-only challenges (no server needed)

These ship as files, so they're safe to analyse by reading and scripting.

| ID | Challenge | Year / category | Files | Reading first | Attempt 2 |
|---|---|---|---|---|---|
| PC-01 | **CySpace.com** | 25/26 crypto (warmup-style) | `cyspace.html` + images | Module 12 §12.6 (odd encodings); Module 4 §4.1 | **PC-04** |
| PC-02 | **Feed Me!** | 25/26 crypto | user-manual PDF + GIF | Module 4 §4.1, §4.5; read the PDF closely | PC-03 |
| PC-03 | **TRC** | 25/26 crypto (needs the hosted service; `sample.txt` shows the format) | sample output | Module 4 §4.1, Module 11 §11.5 | PC-02 |
| PC-04 | **Punched cards** | 25/26 forensics | three PNG images | Module 12 §12.6; find a punched-card encoding chart yourself | PC-01 |
| PC-05 | **parts** | 24/25 crypto | `parts.zip` (scripts + ciphertext) | Module 4 §4.6 (RSA misuse) | PC-07 |
| PC-06 | **Encrypted MFA** | 24/25 crypto | PDF + walkthrough doc | Module 4 §4.5-4.7 | PC-08 |
| PC-07 | **Leaked and Loaded** | 24/25 crypto | `password.txt` | Module 4 §4.4 (hashes) | PC-05 |
| PC-08 | **enigma** | 25/26 crypto (hard) | `encrypt.py`, `output.txt` | Module 4 §4.3; learn how Enigma works (rotors, plugboard) | PC-09 |
| PC-09 | **enigmail** | 25/26 crypto (harder) | `enigmail.zip` | same + known-plaintext attacks | PC-08 |
| PC-10 | **WhatWasThis** | 25/26 AI | `sample.txt`; hosted service | field map §8.8 (AI security); prompt injection | PC-11 |

**Suggested first three:** PC-01, PC-02, PC-04 (about 30-45 minutes each).

## 4. Web and RE challenges (need a lab)

| ID | Challenge | Skills | Reading first | Notes |
|---|---|---|---|---|
| PC-11 | **corporate complexity** (`web/corpo`) | file upload, predictable file names, command execution, multi-container chain | Module 3 §3.7 | files: `corporate_complexity.zip`; run in Docker only |
| PC-12 | **Rabbit Holes** (`web/rabbit-holes`) | non-HTTP protocol (gopher + FTP), input filtering, URL schemes | Module 3 §3.8 (SSRF) | files: `server.py` |
| PC-13 | **Secret Rally** (`web/secret_rally`) | JWT/auth bypass, then SQL injection | Module 3 §3.3, §3.5 | `secret_rally.zip` |
| PC-14 | **Ballot Scanner** (`web/BallotScanner`) | web app with a walkthrough doc | Module 3 | read `README.md`/`WALKTHROUGH.md` |
| PC-15 | **Water treatment** (`re/water-treatment`) | 16-bit DOS executable | Module 5 §5.2 | `wt.exe`: **analyse in an isolated VM only** (DOSBox/32-bit Windows) |
| PC-16 | **fishing-game** (`re/fishing-game`) | unpacking a packaged game, reading Lua, finding a logic bug | Module 5 §5.6, Module 11 | `dist.zip`; VNC-based service |
| PC-17 | **Spyware** (`re/spyware`) | finding an implant among system files | Module 13/6; Module 2 §2.4 | the task is on a machine image |
| PC-18 | **Vector Veil** (`re/vecveil`) | reverse engineering | Module 5 | walkthrough in `docs/WALKTHROUGH.md` |
| PC-19 | **Call Centre / Polling Station / Registration Oriented Programming** | beginner binary exploitation | Module 5 §5.7 | each has `src`, `hosted`, `solve` |
| PC-20 | **Voter Emailer** (`cloud`) | cloud misconfiguration | Module 14 | read the README |
| PC-21 | **Data is the new currency / Tricky Communications** | forensics, stego | Module 2 | read the READMEs |

## 5. Defence challenges

| ID | Service | Reading first |
|---|---|---|
| DEF-01 | **Defence CTF 101 workshop** (Candidate Registry) | chapter 24 §8 |
| DEF-02 | **Inventory** (25/26): BASIC web app | chapter 24 §5-6 |
| DEF-03 | **Chatbot** and **Voter Registry** (24/25) | chapter 24 §5-6; Module 3 |
| DEF-04 | Nationals services (Candidate Registry full patch notes, ElectoMap, Vote Tabulation) | after the regionals |

## 6. The activity cards (use the workflow)

```text
ACTIVITY: PC-01 CySpace.com           PLATFORM: CyberSci PastChallenges   TIME BOX: 30 min
READ:       Module 12 §12.6, Module 4 §4.1
DO:         open the page; find what looks out of place; decode it
ATTEMPT 1:  date __ grade __ minutes __
REVIEW:     first miss: __
REINFORCE:  flashcards "OSINT and misc"; re-read §12.6
ATTEMPT 2:  PC-04 Punched cards (same skill: decode an unusual writing system)
DONE WHEN:  you solved Attempt 2 faster, with fewer hints
```

Copy the card for each PC-* item. Track them in `tracker/activities.csv`.

---

# SPOILERS: approach summaries (read after Attempt 1)

These are concept-level summaries of the published walkthroughs, in my words, with no flags.

## 2025/26 regionals

| Challenge | Approach in one paragraph |
|---|---|
| **CySpace.com** | A comment in the page holds a number written as digit groups (`222-999-22-33-777 …`). That's **phone-keypad multi-tap ("vanity") code**: the digit is a key and the repeat count selects the letter. Decode by hand or with a decoder; the result is the flag. Lesson: odd-looking numbers are often an old input method. |
| **Feed Me!** | Re-read the manual carefully: it hides which cipher (**RC2**), that there is **no IV**, that input is **hex**, and when to start counting button presses. The key comes from the GIF (the sequence of button presses), converted to hex, then CyberChef decrypts. Lesson: documentation inside a challenge is the hints. |
| **TRC** | The service answers every message with **Morse code**; decoding it gives **Base32**, which decodes to more data. A CyberChef recipe works, but a **script** is better because the later steps repeat. Lesson: layered encodings; script what repeats. |
| **Punched cards** | Hand-decode IBM punched cards using a published chart (hole positions map to characters). Lesson: research the format; this is pure lookup and patience. |
| **enigma** | Known-plaintext (**crib**) attack on **Enigma**: the crib is a likely phrase; use a **Bombe simulation** to recover rotor order/positions and part of the plugboard, then refine ring settings and plugboard pairs and decrypt. The statement even gives SHA-1 checksums of acceptable answers. Lesson: cryptanalysis history; verify with hashes. |
| **enigmail** | Same idea plus a custom **Base-16** encoding and an **unknown crib location** (found from a flaw in Enigma: a letter never encrypts to itself). Decrypt the parts before and after the crib. |
| **WhatWasThis (AI)** | A **vision-language model** has a hidden "favourite" in its system prompt. **Prompt injection through an uploaded image** (text in the image) makes it reveal or assert that favourite. Lesson: treat model input as untrusted; this is an emerging category. |
| **Water treatment** | A **16-bit DOS** program. You need a DOS environment (DOSBox/dosbox-x or 32-bit Windows) to run it; the goal is to display a program name in ASCII art. Lesson: run legacy software in an emulator. |
| **fishing-game** | **Unpack** the packaged executable to find the **Lua source**, read it (or have a tool summarise it) and find a **logic bug**: a negative-strength condition duplicates an item, which can be sold repeatedly to earn the money for the flag. Lesson: read game logic for item/currency duplication. |
| **corporate complexity** | A multi-container chain: **upload a PHP file** through an order service, **predict the URL** of the stored file (derived from the MD5 of the file plus the extension), then use the uploaded code to read a file on the server. Lesson: upload bugs plus predictable names equal code execution. |
| **Rabbit Holes** | A **gopher** server's search feature fetches resources with **cURL**. It blocks `file` and `ftp` schemes but only in **lowercase**, so a **mixed-case scheme** bypasses the filter and reads a file from the FTP server. Lesson: case-sensitivity bugs in blocklists; blocklists lose to allow-lists. |
| **Inventory (defence)** | A BASIC app that calls **`EVAL$`** on user-controlled input, leaking data such as an admin password. The fix removes the dangerous call. Lesson: eval-style functions on user input are injection. |

## 2024/25 regionals

| Challenge | Approach in one paragraph |
|---|---|
| **candidate_registry (crypto)** | The server uses **AES in PCBC mode**. PCBC lets you **swap adjacent ciphertext blocks** and only disturb two plaintext blocks, so you can reshape the encrypted JSON so that it still parses and contains the right token. Lesson: unusual block-cipher modes break assumptions about integrity. |
| **parts** | A message encrypted with **RSA piece by piece** (4-byte chunks). Each chunk can be **brute-forced** by encrypting every candidate and comparing, with optimisations to be fast. Lesson: textbook RSA of small pieces is deterministic and guessable. |
| **Secret Rally (web)** | An **authentication bypass** lets you forge **JWTs** (the token only needs to name a valid user, and a default admin account exists), then a **SQL injection** reachable only when logged in. Lesson: token checks must verify identity properly; chain two bugs. |
| **Spyware** | Hunt for an implant on a server: list running programs and compare against what the OS ships. A program placed under `systemd` that **masquerades as a standard utility** (`cat`) turned out to be the malicious one, and it talks on the network. Lesson: compare against the known-good baseline; check what talks to the network. |
| **Vector Veil**, **Call Centre**, **Polling Station**, **Registration Oriented Programming**, **Ballot Scanner**, **Encrypted MFA**, **Leaked and Loaded**, **Voter Emailer**, **Data is the new currency**, **Tricky Communications**, **Chatbot**, **Voter Registry** | Read the folder README/WALKTHROUGH after your attempt. The pwn challenges include `src`, `hosted` and `solve` directories; the web, crypto and forensics ones include their own walkthrough documents. |

## 7. What these challenges teach as a set

| Skill | Seen in |
|---|---|
| Recognise an unfamiliar encoding and research it | vanity code, punched cards, Morse + Base32 |
| Crypto misuse over crypto breaking | PCBC, piecewise RSA, RC2 with a leaked key |
| Chain small bugs | file upload → webshell → read file; JWT bypass → SQLi |
| Read unfamiliar source | BASIC, Lua, DOS |
| Filters fail | mixed-case URL scheme, blocklists |
| Defend by patching | Inventory, Chatbot, Voter Registry, Candidate Registry |
| AI is now in scope | prompt injection via an image |

## 8. Check yourself

1. Which two 2025/26 challenges are solved by decoding an unusual notation, and what skill do they share?
2. Why does a blocklist for URL schemes fail when it is case-sensitive?
3. What property of AES-PCBC makes block swapping dangerous?
4. In the file-upload chain, why does a predictable file name matter?
5. Explain prompt injection in two sentences.
