"""Phone-first diagrams for the past-challenge writeups -> curriculum/pastchallenges/img/"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phone_svg import P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "curriculum" / "pastchallenges" / "img"


def chain(name, title, sub, steps, note=""):
    p = P(title, sub)
    cols = ["blue", "green", "amber", "purple", "teal", "red"]
    for i, s in enumerate(steps):
        p.box(s, cols[i % len(cols)], size=13)
        if i < len(steps) - 1:
            p.arrow()
    if note:
        p.note(note)
    p.save(OUT, name)


p = P("Where to start with the past challenges", "easiest wins first")
for t, c in [("1 Warmups: CySpace, Punched card 1, Feed Me, TRC, Leaked and Loaded", "green"),
             ("2 CyberChef-style: Encrypted MFA, Ballot Scanner 1-2", "teal"),
             ("3 Web chains: Secret Rally, corporate complexity", "blue"),
             ("4 Defence: Defence CTF 101 workshop, then Inventory", "amber"),
             ("5 Crypto misuse: parts, candidate_registry (PCBC)", "purple"),
             ("6 Forensics and implants: Data is the new currency, Spyware 1", "red"),
             ("7 RE: Water treatment, Spyware 2-3, fishing-game, Vector Veil", "gray"),
             ("8 Advanced: Enigma, pwn (heap/ROP)", "gray")]:
    p.box(t, c, size=12.5)
p.save(OUT, "pc-roadmap.svg")

chain("pc-corpo.svg", "corporate complexity: the chain", "three parts, each unlocks the next",
      ["Part 1: upload a PHP file through the order form",
       "Predict where it is stored (name derived from a hash of the file)",
       "Run code through it: read a file on the server",
       "Part 2: use it to reach a backend service; SQL injection in a quantity field",
       "Part 3: use the injection to plant a script a cron job runs; reach the HR database"],
      "Pattern: foothold, pivot, escalate. Each step needs the previous one.")

chain("pc-pcbc.svg", "AES-PCBC block swapping", "candidate_registry",
      ["Server decrypts a payload; must be valid JSON with the right token and a new username",
       "PCBC chains plaintext AND ciphertext into the next block",
       "Swapping two ciphertext blocks only damages two plaintext blocks",
       "Craft a swap so the JSON still parses and the token field survives",
       "Server accepts it and reveals the secret"],
      "Lesson: encryption without authentication is malleable.")

p = P("Piecewise RSA", "parts")
p.box("Message split into 4-byte pieces; each piece encrypted with the same public key", "blue", size=12.5)
p.arrow()
p.box("Same plaintext piece always gives the same ciphertext", "amber", size=12.5)
p.arrow()
p.box("Encrypt every printable 4-byte candidate (~100^4 = 2^27) and compare", "green", size=12.5)
p.arrow()
p.box("Matches reveal each piece; join them into the message", "red", size=12.5)
p.note("Lesson: textbook RSA on small inputs is a lookup table.")
p.save(OUT, "pc-rsa-pieces.svg")

chain("pc-trc.svg", "TRC: nested encodings", "crypto warmup that needs a script",
      ["Any message to the server gets a Morse-code reply",
       "Decode the Morse: you get Base32 text",
       "Decode the Base32: the first message",
       "Part 2: send an HTTP GET request, encoded the same way (Base32, then Morse)",
       "Script the encode/decode loop; the server answers"],
      "Lesson: when the same transform repeats, write the script early.")

chain("pc-enigma.svg", "Enigma: crib attack", "enigma and enigmail",
      ["Know or guess part of the plaintext (the crib)",
       "Enigma never maps a letter to itself: slide the crib to find valid positions",
       "Simulate a Bombe to find rotors, start positions and part of the plugboard",
       "Refine ring settings and remaining plugboard pairs",
       "Decrypt the whole message; verify with the given hashes"],
      "Lesson: history's attacks still work when the system is reproduced.")

chain("pc-jwt.svg", "JWT auth bypass then SQL injection", "Secret Rally",
      ["Read the code: default admin account named admin plus a random number",
       "Forge a token naming a valid user (the check only needs a real username)",
       "Try every possible username until the dashboard loads",
       "Use the SQL injection in the attendee form (logged-in only)",
       "Change what the query returns so the secret becomes visible"],
      "Lesson: a token is only as good as its verification.")

chain("pc-llm.svg", "LLMs as the attack surface", "AI and cloud challenges 2024-26",
      ["WhatWasThis: instructions hidden in an uploaded image reach the model",
       "Chatbot (defence): the agent's tools trust the model, not the session",
       "Voter Emailer: the model chooses OS commands via a tool-calling endpoint",
       "Chain: model output becomes code execution, then cloud credentials",
       "Fix: authorise in code, never in the prompt"],
      "Lesson: never let a model be the access-control decision.")

chain("pc-spyware.svg", "Hunting an implant", "Spyware parts 1-3",
      ["Part 1: list programs; compare with what the OS ships; spot the fake 'cat'",
       "It disguises itself and sends traffic that looks like cat-photo exchange",
       "Part 2: recover the key phrase it derives encryption from (decode or debug)",
       "Part 3: the kill keyword is checked in 3-byte pieces by hash: brute-force each",
       "Lesson: hash checks on tiny pieces are brute-forceable"])

p = P("Inventory (BASIC) defence bugs", "three exploits, three fixes")
p.box("1 EVAL$ on user input: leaks data such as the admin password → remove EVAL$", "red", size=12.5)
p.box("2 Global MODE reused as a local variable: scrolling backward turns you into an admin → declare it LOCAL or rename it", "amber", size=12.5)
p.box("3 (Part 3) see the repo; same method: read the code, find the shared state, patch", "gray", size=12.5)
p.note("Lesson: old languages share variables silently; trace where state is written.")
p.save(OUT, "pc-inventory.svg")

chain("pc-water.svg", "Water treatment: three RE steps", "16-bit DOS program",
      ["1 Get it running (DOSBox, real DOS, or 32-bit Windows) to see the program's name",
       "2 Reverse the password check: it compares an MD2 hash; test a common-password list",
       "3 Reverse the safety code: compares keyboard scan codes, not characters"],
      "Lesson: legacy tooling is part of the puzzle; hashing choices can be old.")

chain("pc-ballot.svg", "Ballot Scanner: web by barcode", "three small steps",
      ["1 Submit the sample ballot's barcode image: a test ballot returns a message",
       "2 Admin barcode format (PRECINCT-CODE): a count function returns a total",
       "3 Fuzz other codes: one is an admin code that opens a diagnostics page"],
      "Lesson: map the input format, then fuzz the neighbouring values.")

chain("pc-defence-fix.svg", "Defence services: the common fixes", "Voter Registry, Chatbot, Candidate Registry",
      ["Signatures: verify them properly (not just their length)",
       "JWT: never make signature verification optional",
       "Access control: check the user owns the record (and the tool call)",
       "Sessions: random tokens, not base64 of the username",
       "Test: re-run the attack and the health check"])

print(len(list(OUT.glob("*.svg"))), "past-challenge SVGs ->", OUT)
