# picoCTF / picoGym: the full-depth guide

Status: **names marked S were seen in sources fetched on 2026-11-14; names marked M are recalled from memory and must be verified in the Challenge Library** (which the assistant could not open: `play.picoctf.org` did not resolve from here). The platform has been renamed: picoCTF's practice area is now called the **Challenge Library** on CMU's CyLab Security Academy; older logins from before May 2026 still work (see status.picoctf.org). The skill and nudge columns are written from memory of how such challenges usually work and may not match the current version of a challenge. Challenge pools change every year, so the archive is larger than any list here. This book gives you the method, a curated set of well-known beginner and intermediate challenges, and a hint ladder; it does **not** include flags or step-by-step solutions.

picoCTF rewards learning in the open: after you solve a challenge, read other people's writeups to compare methods (public repos such as Cajac/picoCTF-Writeups index writeups by event year).

## How to work a challenge

1. **Read** the description and any hints; note the file types and the category. 2. **Attempt (20 min):** do the obvious thing. 3. **Nudge:** the one-line nudge in the tables below. 4. **Hint:** the platform's own hint if you are still stuck. 5. **Review:** write down what the trick was. 6. **Reinforce:** reread the category method. 7. **Attempt 2:** retry a similar challenge a day later.

## Suggested order (matches CyberSci's list)

1. General Skills (all Easy) → 2. Cryptography (Easy) → 3. Forensics (Easy) → 4. Web Exploitation (Easy) → 5. Reverse Engineering (Easy) → 6. Binary Exploitation (Easy), then the Mediums.

The manifest `curriculum/picoctf/manifest.csv` lists 110 curated challenges (category, difficulty, confidence, skill, nudge, status).

## General Skills

Learn the command line, simple scripting and decoding. These are the warm-ups you should be able to do in minutes.

**Tools and ideas:**

- `cat`, `less`, `grep -r`, `find`, `strings`, `file`, `unzip`, `tar`
- `nc host port` for services; `ssh -p PORT user@host`
- Python for bases (`int(x, 2)`, `hex()`, `bytes.fromhex`) and hashing (`hashlib`)
- CyberChef for encodings

**Rule:** Run the thing, read the error, read the script. If a program prints something odd, look at its source.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| Obedient Cat | Easy | S | Using cat and files | Download the file and read it with the simplest command. |
| Python Wrangling | Easy | S | Running a Python script with arguments | Read the script's usage; the flag file is decrypted by running it correctly. |
| Wave a flag | Easy | S | Executable permissions and --help | Make the file executable, then ask it for help. |
| Nice netcat | Easy | S | Talking to a remote service | Connect with nc and read what it sends; the data needs a conversion. |
| Static aint always noise | Easy | S | strings and grep | Search a binary for readable text. |
| Tab Tab Attack | Easy | S | Shell tab completion and paths | Unzip, then follow the nested folders with tab completion. |
| Magikarp Ground Mission | Easy | S | SSH and the filesystem | Log in over SSH and read the instructions file, then explore. |
| Codebook | Easy | S | Running Python with the right directory | Run the script from the folder that contains its data. |
| convertme | Easy | S | Base conversion | Convert the number between decimal and binary by hand or with Python. |
| fixme1 | Easy | S | Fixing a Python syntax error | Run it, read the error, fix one line at a time. |
| fixme2 | Easy | S | Fixing a Python logic error | Compare the operators in the comparison. |
| Glitch Cat | Easy | S | Python escapes in output | Evaluate what the program prints with Python's repr/eval. |
| HashingJobApp | Easy | S | Computing md5 of text | Connect, receive text, hash it, answer. |
| PW Crack 1 | Easy | S | Reading a checker script | The password is in the script. |
| PW Crack 2 | Easy | S | Reading a checker script | The check uses character codes; convert them. |
| PW Crack 3 | Easy | S | Brute-forcing a short list | Try each candidate from the given list programmatically. |
| PW Crack 4 | Easy | S | Brute-forcing a longer list | Same idea; automate it. |
| PW Crack 5 | Easy | S | Brute-forcing with a dictionary file | Read the dictionary file in your own loop. |
| runme | Easy | S | Running a downloaded program | Make it executable and run it. |
| Serpentine | Easy | S | Reading Python code for hidden functions | Find the function that prints the flag and make the program call it. |
| First Find | Easy | S | find and grep over a directory tree | Search the tree by file name or contents. |
| Big Zip | Easy | S | Searching inside a large archive | Extract it and grep recursively. |
| strings it | Easy | S | strings | Pull readable text out of the program. |
| Bases | Easy | S | Base64 and other encodings | Identify the encoding from the alphabet. |
| First Grep | Easy | S | grep | Search the file for the flag format. |
| what's a net cat? | Easy | S | netcat basics | Connect to the host and port and read. |
| plumbing | Easy | S | Pipes and redirection | Connect and pipe the output through grep. |
| Based | Medium | S | Converting between binary, octal and hex | Answer each round by converting the numbers it gives. |
| Mod 26 | Easy | S | ROT13 | Shift letters by 13. |
| fixme1.py | Easy | S | Fixing a Python syntax error | Run it and fix what the error says. |
| 2Warm | Easy | S | Number bases | Convert 42 to binary. |
| Warmed Up | Easy | S | Hex to decimal | Convert the hexadecimal number. |
| Lets Warm Up | Easy | S | ASCII and hex | Look up the ASCII character for a hex byte. |
| flag-shop | Medium | S | Integer overflow logic in a program | Look at how the purchase total is computed with numbers. |
| mus1c | Medium | S | Esoteric language (Rockstar) | Identify the language from the lyrics, then find an interpreter. |
| I-wanna-b3-a-r0ck5tar | Medium | S | Esoteric language | Search for the language that looks like song lyrics. |

## Cryptography

Classical ciphers, modular arithmetic and RSA basics; the lesson is that weak parameters break strong algorithms.

**Tools and ideas:**

- Frequency analysis, Caesar/Vigenere solvers (write your own)
- RSA: n = p*q, phi = (p-1)(q-1), d = e^-1 mod phi; know small-e and factorable-n attacks
- `openssl` for certificates; `python-gmpy2`/`pycryptodome`; factordb.com
- CyberChef for quick decodes

**Rule:** Identify the primitive first (cipher name, key size, what is public), then ask what is weak.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| rotation | Easy | M | Caesar/ROT shifts | Try all 25 shifts and look for a flag format. |
| interencdec | Easy | M | Chained encodings | Decode in layers (base64, then another), checking each result. |
| ReadMyCert | Easy | M | Reading a certificate request | Decode the PEM/CSR with openssl. |
| C3 | Medium | M | Reading a custom cipher script | Understand the encryption function, then write its inverse. |
| Dachshund Attacks | Medium | M | RSA with a small private exponent (Wiener's attack) | A very large e hints at a very small d; look for the attack by name. |
| Easy1 | Easy | M | Vigenere / one-time-pad table | Use the table with the key given. |
| Caesar | Easy | M | Caesar cipher | Shift back by the right amount. |
| The Numbers | Easy | M | Number-to-letter cipher | Map each number to its position in the alphabet. |
| Vigenere | Easy | M | Vigenere with a given key | Decrypt with the key; use a tool you wrote or an online decoder. |
| miniRSA | Medium | M | RSA with a tiny exponent | When e is small and the message is small, take an integer root. |
| Easy Peasy | Medium | M | One-time pad key reuse | Observe how the key stream repeats. |
| basic-mod1 | Easy | M | Modular arithmetic and a character table | Take each number mod 37 and map to a character set. |
| basic-mod2 | Easy | M | Modular inverse | Compute each modular inverse, then map. |
| Mind your Ps and Qs | Medium | M | Factoring a weak RSA modulus | Small n can be factored with a database or tool. |
| Sum-O-Primes | Medium | M | RSA from the sum and product of primes | Use the relation between p+q and p*q to recover p and q. |
| Pixelated | Medium | M | Combining images | Overlay the images pixel by pixel. |
| Hashcrack | Easy | M | Identifying and cracking hashes | Identify the hash type, then use a wordlist. |

## Forensics

Files, images, captures and disk images: find hidden data and reconstruct what happened.

**Tools and ideas:**

- `file`, `exiftool`, `strings`, `binwalk`, `foremost`, `xxd`
- Steganography: `steghide`, `zsteg`, `stegsolve`, `outguess`
- Wireshark/`tshark` for captures; follow TCP streams; export objects
- Disk images: `mmls`, `fls`, `icat` (Sleuth Kit) or mount read-only; Autopsy

**Rule:** Never trust the file extension; check the type and the headers; extract everything before reading anything.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| Secret of the Polyglot | Medium | M | Polyglot files (PDF + PNG) | One file is valid as two formats; open it as each. |
| Redaction gone wrong | Easy | M | Hidden text under redaction | Select or extract the text from the document. |
| Disk, disk, sleuth! | Easy | M | Searching a disk image | Use strings and grep on the image. |
| Mob psycho | Medium | M | Android APK as a zip | Unpack the archive and search its files. |
| Wireshark doo dooo do doo... | Easy | M | Following a TCP stream | Open the capture and follow the stream. |
| information | Easy | M | File metadata | Read the metadata with exiftool. |
| Matryoshka doll | Medium | M | Nested files | Look for archives hidden inside the image. |
| Enhance! | Easy | M | SVG text | Open the SVG as text. |
| extensions | Easy | M | File signatures | The extension lies; check the real type with file. |
| Lookey here | Easy | M | Searching a large text file | grep for the flag format. |
| St3g0 | Medium | M | Image steganography | Try common stego tools on the image. |
| tunn3l v1s10n | Medium | M | Repairing a corrupted file header | Compare the bytes with a valid file of the same type. |
| Trivial Flag Transfer Protocol | Medium | M | TFTP in a packet capture | Extract the transferred files from the capture. |
| MacroHard WeakEdge | Medium | M | Macros in an Office file | Unzip the document and look through its parts. |
| Packets Primer | Easy | M | Reading a capture | Look at the payload of the packets. |
| Operation Oni | Medium | M | SSH key recovery from a disk image | Mount the image and find the key. |

## Web Exploitation

Browser, HTTP and server behaviour: find what the server trusts that you control.

**Tools and ideas:**

- Browser dev tools: Elements, Network, Application (cookies), Console
- `curl -v`, Burp/ZAP repeater
- Wordlists and `ffuf` for hidden paths
- SQL injection basics, JWT inspection (`jwt.io` concepts), PHP deserialization basics

**Rule:** View source first; then cookies and headers; then the inputs; then the server's files.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| where are the robots | Easy | M | robots.txt | Check the file the site publishes for crawlers. |
| dont-use-client-side | Easy | M | Client-side checks | Read the JavaScript and reassemble the secret. |
| More Cookies | Medium | M | Cookie tampering with encrypted values | Change a byte in the cookie and observe the effect. |
| Who are you? | Medium | M | HTTP headers | Change request headers to match the demands the page makes. |
| Super Serial | Medium | M | PHP deserialization | Find the source and the file the code reads. |
| Cookies | Easy | M | Cookie values | Change the cookie and watch the page change. |
| Insp3ct0r | Easy | M | View source | Read HTML, CSS and JavaScript. |
| Scavenger Hunt | Easy | M | Finding hidden files | Check robots.txt, .htaccess and other standard files. |
| logon | Easy | M | Cookie-based login | Look at which cookie decides who you are. |
| picobrowser | Easy | M | User-Agent header | Change the header your client sends. |
| Client-side-again | Medium | M | Obfuscated JavaScript | Deobfuscate the checker by reading it carefully. |
| Power Cookie | Easy | M | Cookie flags | Look for a flag-like cookie value. |
| Irish-Name-Repo 1 | Medium | M | SQL injection in a login | Try classic injection on the login form. |
| caas | Medium | M | Command injection through a web form | The input reaches a shell command. |
| JaWT Scratchpad | Medium | M | JWT weaknesses | Inspect the token and the algorithm. |
| SQLiLite | Medium | M | Basic SQL injection | Break out of the string in the query. |
| login | Medium | M | Client-side password check | Read how the page checks the password. |

## Reverse Engineering

Read what a program does without its source: strings, disassembly, decompilation and debugging.

**Tools and ideas:**

- `strings`, `file`, `ltrace`, `strace`, `objdump -d`
- Ghidra or `radare2`/`cutter` for decompilation
- `gdb` with a helper (pwndbg/gef) for dynamic analysis
- UPX for packed binaries; `uncompyle6`/`pycdc` for Python bytecode

**Rule:** Find the check, work out what input satisfies it, then reproduce it with a script.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| patchme.py | Easy | M | Reading a Python checker | Understand the check and the key it expects. |
| Safe Opener | Easy | M | Decoding in a Java source | Read the source and decode what it compares. |
| vault-door-training | Easy | M | Reading Java source | The password check is readable in the source. |
| packer | Medium | M | UPX-packed binary | Unpack with the standard packer tool, then read strings. |
| keygenme-py | Medium | M | Python license check | Work out the key format from the source. |
| vault-door-1 | Easy | M | Reading a character-by-character check | Reorder the characters as the code compares them. |
| ARMssembly 0 | Medium | M | Reading ARM assembly | Trace the function by hand. |
| Transformation | Easy | M | Python encoding scheme | Reverse the encoding function. |
| speeds and feeds | Easy | M | G-code | Render the commands as a toolpath. |
| crackme-py | Easy | M | Reading a Python script | Find the function that decrypts the flag and call it. |
| asm1 | Medium | M | x86 assembly | Trace the function with the argument. |
| Bbbbloat | Medium | M | Binary with a hard-coded check | Use a decompiler or ltrace. |
| GDB Test Drive | Easy | M | First steps in gdb | Follow the instructions in gdb. |

## Binary Exploitation

Memory corruption: change a program's behaviour with input it did not expect.

**Tools and ideas:**

- `gdb` + pwndbg/gef, `checksec`, `cyclic` patterns (pwntools)
- Stack layout, return addresses, calling conventions
- Format strings (`%x`, `%n`), ret2libc, simple heap ideas
- Your Narnia notes are the best preparation

**Rule:** Find the overflow, find the offset, decide what to jump to, test locally before the remote service.

| Challenge | Difficulty | Src | What it teaches | Nudge |
|---|---|---|---|---|
| Cache Me Outside | Hard | M | Heap/tcache behaviour | Study how the allocator reuses chunks. |
| Here's a LIBC | Medium | M | ret2libc with a leak | Leak a libc address, compute the base, call system. |
| buffer overflow 0 | Easy | M | Overflow to trigger a handler | Send more input than the buffer holds. |
| buffer overflow 1 | Medium | M | Overwrite the return address | Find the offset, then jump to the win function. |
| buffer overflow 2 | Medium | M | Return with arguments | Place the function arguments on the stack as the ABI needs. |
| format string 0 | Easy | M | Format string leak | Use format specifiers in the input. |
| format string 1 | Medium | M | Reading the stack with %x | Convert what you leak back to text. |
| Stonks | Medium | M | Format string in a menu program | Find the input that is passed straight to printf. |
| basic-file-exploit | Easy | M | Logic bug in a menu | Try unexpected menu inputs. |
| two-sum | Medium | M | Integer overflow | Find inputs whose sum wraps. |
| Local Target | Easy | M | Variable overwrite by overflow | Overflow a buffer to change a neighbouring variable. |

## How picoGym maps to the CyberSci skills list

| CyberSci skill | picoCTF category |
|---|---|
| Crypto algorithms and weaknesses | Cryptography |
| Memory forensics, packets, files | Forensics |
| Web exploits, basic SQL | Web Exploitation |
| Reverse engineering | Reverse Engineering |
| Beginner binary exploitation | Binary Exploitation (Easy first) |
| Basic programming | General Skills |

## Time budget

About 15 minutes per Easy challenge and 30-45 per Medium. Finish all Easy challenges in one category (about 2 hours) before the next. After CyberSci, do the Medium and Hard ones.
