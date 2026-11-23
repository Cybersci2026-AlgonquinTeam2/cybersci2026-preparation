# 25. Memory forensics: the deep book

Status: written from the Volatility 3 documentation conventions and standard DFIR practice, **not run on your machine yet**. Plugin names and flags are marked where you must confirm them with `vol -h` and `vol <plugin> -h` on your installed version. The CyberSci skills list names memory forensics explicitly, so this book exists to make it a first-hour skill.

## 1. What memory forensics is (layman)

A computer's **RAM** is its short-term memory: whatever is running right now. When you "freeze" it and copy it to a file, you get a **memory image**. Unlike a disk, RAM holds things that were never saved: the password someone just typed, the command a hacker just ran, a program that only exists in memory.

Think of it as photographing a desk mid-task. You can see which papers are open (processes), who is on the phone (network connections), what notes are lying around (strings, clipboard) and sometimes the keys in the lock (passwords, encryption keys).

```
        RAM image (one big file)
 +---------------------------------------------+
 |  kernel structures  | process list | sockets |
 |  loaded programs    | command lines | files  |
 |  passwords/hashes   | registry      | text   |
 +---------------------------------------------+
        Volatility reads the OS's own bookkeeping
        out of that file and prints it as tables.
```

## 2. How it works (technical)

An OS keeps linked structures in memory: on Windows an `EPROCESS` per process, a socket table, loaded modules, registry hives. **Volatility 3** needs the right **symbol tables** (ISF files) for the OS build so it can find and decode those structures. Windows symbols download automatically the first time you have internet access (then cache); Linux and macOS images need matching symbol files (Volatility publishes some; otherwise you build one from the kernel's debug symbols).

Two views of "what is running":
- **List-walking** (`pslist`): follows the OS's own linked list. Fast, but malware can unlink itself.
- **Pool scanning** (`psscan`): scans raw memory for process-shaped structures. Finds hidden and already-terminated processes.
Compare both: a process present in `psscan` but not `pslist` is suspicious (hidden) or simply exited.

## 3. Get set up

```bash
python3 -m venv ~/vol3 && source ~/vol3/bin/activate
pip install volatility3          # provides the `vol` command (or `volatility3`)
vol -h                            # list plugins
vol -f mem.raw windows.info       # first command on any Windows image: confirms it parses
```
Handy global options (confirm with `vol -h`): `-f FILE` image, `-o DIR` folder for dumps, `-r pretty|csv|json` output format, `-q` quiet. Redirect output to files, then `grep`.
Without internet, copy the symbol cache folder from a machine that has it: do this before the event.

## 4. The standard first pass (the 10-minute triage)

| Step | Command | Looking for |
|---|---|---|
| 1 | `windows.info` | OS version/build, system time, confirms the image is usable |
| 2 | `windows.pstree` | Parent/child shape: Word launching PowerShell, `cmd` under a browser |
| 3 | `windows.pslist` and `windows.psscan` | Hidden or exited processes (diff the two) |
| 4 | `windows.cmdline` | Full command lines; flags and file names hide here |
| 5 | `windows.netscan` (and `windows.netstat`) | Outbound connections, odd ports, which process owns them |
| 6 | `windows.malfind` | Executable memory regions with no file behind them (injection) |
| 7 | `windows.filescan` then `grep` | Files that were open in memory (`flag`, `.txt`, `.zip`, `.docx`) |
| 8 | `windows.envars` | Environment variables (secrets and paths) |
| 9 | `windows.registry.hivelist`, `windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"` | Persistence |
| 10 | `windows.hashdump` | NTLM hashes for crack-or-pass-the-hash questions (needs the right hives in memory) |

Method: write one line after each step ("PID 3180 powershell, parent winword, started 14:02") so your timeline builds as you go.

## 5. The plugin toolbox, explained

| Plugin | What it shows | Notes |
|---|---|---|
| `windows.pslist` | Processes via the active list | PID, PPID, threads, start/exit time |
| `windows.pstree` | Same, as a parent/child tree | Best for spotting odd parentage |
| `windows.psscan` | Scans memory for process objects | Finds hidden/exited |
| `windows.cmdline` | Process command lines | Use `--pid N` to focus |
| `windows.dlllist` | DLLs loaded in a process | Odd DLL paths = injection or sideloading |
| `windows.handles` | Open files, keys, mutexes | Large; filter with `--pid` and grep |
| `windows.netscan` | Sockets and connections (pool scan) | Includes closed ones |
| `windows.malfind` | Injected or unbacked executable memory | Shows hex preview; look for `MZ` or shellcode |
| `windows.filescan` | File objects in memory | Gives offsets for `dumpfiles` |
| `windows.dumpfiles` | Extract a file | `--virtaddr` or `--physaddr`, `-o outdir` (confirm flags with `-h`) |
| `windows.memmap --pid N --dump` | Dump a process's memory pages | Then run `strings` on the dump |
| `windows.hashdump` | Local account hashes | Crack with `hashcat -m 1000` |
| `windows.registry.hivelist` / `printkey` | Registry hives and keys | Run keys, installed software, recent docs |
| `windows.svcscan` | Services | Persistence via services |
| `windows.cmdscan` / `windows.consoles` | Typed console commands | Present in newer releases; check `vol -h` |

Linux images (needs symbols): `linux.pslist`, `linux.pstree`, `linux.psaux`, `linux.bash` (shell history), `linux.lsof`, `linux.sockstat`, `linux.lsmod`.

## 6. Strings: the fastest trick when plugins fail

```bash
strings -a mem.raw | grep -i "flag{"           # ASCII strings
strings -a -e l mem.raw | grep -i "flag{"      # UTF-16 little-endian (most Windows text!)
strings -a -t d -e l mem.raw | grep -i password   # -t d prints byte offsets
```
Why `-e l`: Windows stores most text as 16-bit characters, so plain `strings` misses it. Then use the offset (or a plugin) to learn which process owned it. `grep -a` treats binary as text; `-b` prints offsets.

## 7. Common CTF patterns

1. **"What is the PID/name of the malicious process?"** pstree, parentage, path outside `System32`.
2. **"What is the attacker's IP/port?"** netscan, match to the suspicious PID.
3. **"What file was opened/downloaded?"** filescan then dumpfiles; or cmdline.
4. **"What did the user type?"** cmdline/consoles; clipboard strings; browser process strings.
5. **"What is the password?"** hashdump then crack, or strings near `password=`, or LSA/secrets plugins.
6. **"Is anything hidden?"** psscan vs pslist; malfind.
7. **Chained:** a flag split across a dumped file, a registry value and a command line.

## 8. Red flags table (copy to your notes)

| Observation | Meaning |
|---|---|
| Office app spawns `powershell.exe` or `cmd.exe` | macro or exploit execution |
| `svchost.exe` whose parent is not `services.exe` | masquerading |
| Process running from `\Users\...\AppData` or `\Temp` | likely malware |
| Same name misspelled (`svch0st`, `lsasss`) | typosquat process |
| In `psscan` but not `pslist` | hidden or exited |
| `malfind` hits with `MZ` header in non-image memory | reflective loading |
| Outbound connection from `notepad.exe`/`calc.exe` | injected process |

## 9. Learn by doing: make your OWN memory image (ground truth)

You already run VMs, so you can create an image where *you* know the answers.

1. In VMware, start a lab VM (use a throwaway Windows VM, not your real one). Open `notepad` with a typed secret, open `cmd` and run `ping 127.0.0.1 -t`, start a harmless listener or `ncat` connection between two lab VMs.
2. **Suspend** or **snapshot** the VM. The memory image is the `.vmem` file next to the `.vmx` (with a `.vmss`/`.vmsn` for state).
3. Copy the `.vmem` to your analysis box and run the whole table in section 4.
4. Check your answers: did `pstree` show `notepad`? `cmdline` show the ping? `netscan` show your connection? Did `strings -e l` find your typed secret?

This is the "do the exercise first" step; the reading above is the review.

## 10. Practice sources (verify they are still up)

| Source | What it gives |
|---|---|
| TryHackMe Volatility / memory forensics rooms | Guided, free-tier friendly |
| MemLabs (GitHub: stuxnet999/MemLabs) | Six CTF-style memory labs, graded difficulty |
| CyberDefenders memory labs | Blue-team scenarios with questions |
| Volatility Foundation sample images | Real images with known malware |
| 13Cubed (YouTube) | Clear walkthroughs of the workflow |

## 11. The attempt loop

1. **Attempt 1 (time-box 45 min):** your own VM image, the section 4 table, written answers.
2. **Review:** compare to what you did in the VM; note every plugin that surprised you.
3. **Reinforce:** re-read sections 2 and 8; make 5 flashcards.
4. **Attempt 2 (45 min):** a MemLabs lab with no hints; write the timeline.
5. **Review 2:** which step took longest? Add it to your cheat sheet.

## 12. Flashcard prompts

- Why do `pslist` and `psscan` disagree sometimes?
- What does `malfind` look for?
- Why does `strings` miss most Windows text, and how do you fix it?
- Where do persistence entries hide in the registry?
- Which plugin turns a file in memory into a file on disk?
- What does a process starting from `AppData` tell you?

## 13. Cheat sheet (one screen)

```
vol -f IMG windows.info
vol -f IMG windows.pstree        vol -f IMG windows.psscan
vol -f IMG windows.cmdline       vol -f IMG windows.netscan
vol -f IMG windows.malfind       vol -f IMG windows.filescan | grep -i NAME
vol -f IMG -o out windows.dumpfiles --virtaddr 0xADDR
strings -a -e l IMG | grep -i KEYWORD
```
Rule: **timeline first, flags second**. The flag is usually the answer to a question the evidence can prove.

## 14. Correlation traps (check these before you claim an answer)

- **PID reuse:** the same process id can belong to different processes at different times. Before linking a socket to a process, compare the process start time and the capture time.
- **Absence is not proof:** a process missing from `pslist` may have exited or been hidden; confirm with `psscan` and the timeline.
- **Different views, one story:** a process name alone is weak evidence. Match PID, parent, start time, command line and a second artifact (a file, a registry key, a network record).
- **State your limits:** if the capture does not contain the interval you need, write that down instead of guessing.

