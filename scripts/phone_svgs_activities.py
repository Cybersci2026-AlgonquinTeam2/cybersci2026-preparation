"""Phone-first diagrams for the learn-by-doing activity books -> curriculum/activities/img/"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phone_svg import P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "curriculum" / "activities" / "img"


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


chain("a-workflow.svg", "The learn-by-doing loop", "read first, do, review, reinforce, repeat",
      ["1 READ (10-15 min): only the section linked to the activity",
       "2 ATTEMPT 1 (time-boxed): do it, take notes, don't peek",
       "3 REVIEW: what failed? what was the first thing you missed?",
       "4 REINFORCE: re-read the exact sections + 5 flashcards",
       "5 ATTEMPT 2: a fresh variant, less help, less time",
       "6 REVIEW 2: faster? fewer hints? write the 5-line note"],
      "Done = Attempt 2 completed unaided, or you can explain why not.")

p = P("Attempt grades", "be honest: they drive the plan")
p.box("A  Unaided: no hints, no notes beyond your cheat sheet", "green", size=13)
p.box("B  Hint 1-2: used the first hints only", "teal", size=13)
p.box("C  Hint 3+ or a peek at the approach", "amber", size=13)
p.box("D  Needed the full solution: redo from scratch later", "red", size=13)
p.note("Target: Attempt 1 is B or C. Attempt 2 is A or B. If Attempt 2 is C or D, re-read and repeat in 2 days.")
p.save(OUT, "a-grades.svg")

chain("a-hints.svg", "The hint ladder", "never jump straight to the solution",
      ["H0: re-read the objective and your notes (2 min)",
       "H1: ask 'what is this category / what tool tests it?'",
       "H2: read the section's 'steps' table without the commands",
       "H3: read the commands, run them, predict the output first",
       "H4: read a public writeup AFTER you have an observation"],
      "Log which hint level you reached. It tells you which reading to repeat.")

p = P("One activity card", "every exercise gets the same card")
for t, c in [("READ  linked pack section + the platform's own guide", "blue"),
             ("DO  platform + activity + time box + target grade", "green"),
             ("REVIEW  checklist: first miss, tool I didn't know, mistake", "amber"),
             ("REINFORCE  sections to re-read, flashcard decks, mini drill", "purple"),
             ("ATTEMPT 2  variant or reset + 'done when'", "teal"),
             ("LOG  date, grade, minutes, 5-line note", "red")]:
    p.box(t, c, size=12.5)
p.save(OUT, "a-card.svg")

p = P("Which platform for which skill", "pick the right gym")
for a, b, c in [("TryHackMe", "guided rooms: Linux, web, Windows/AD, forensics", "blue"),
                ("OverTheWire", "Linux shell (Bandit), web (Natas), binaries (Narnia, Leviathan)", "green"),
                ("picoCTF / picoGym", "jeopardy skills across all categories", "amber"),
                ("VulnHub", "attack a whole machine: recon to root", "purple"),
                ("Parrot CTFs", "web, AD, crypto, forensics, micro labs", "teal"),
                ("Cybrary", "video courses and concepts; labs may be paid", "gray")]:
    p.box(f"{a}: {b}", c, size=12.5)
p.save(OUT, "a-platforms.svg")

chain("a-box.svg", "Attacking a whole machine", "VulnHub and boxes: the five phases",
      ["RECON: scan ports, identify services and versions",
       "ENUMERATE: each service by hand (web paths, shares, users)",
       "FOOTHOLD: a weakness that gives you a shell as a low user",
       "PRIVESC: sudo, SUID, cron, creds → root",
       "WRITEUP: timeline of commands, what worked, what failed"],
      "Take a VM snapshot before you start so Attempt 2 begins clean.")

chain("a-room.svg", "A TryHackMe room, done well", "don't just click through",
      ["Skim the room title and tasks; write the goal in one line",
       "Read the pack section first (10-15 min)",
       "Do the tasks; before each answer, predict it",
       "Stuck 10 minutes? use the hint ladder, not the answer",
       "Finish: write three things you couldn't have done before"],
      "Speed-running rooms teaches clicking, not skill.")

p = P("Natas and Bandit progression", "web and Linux ladders")
p.box("Bandit 0-12 shell basics → 13-20 keys, ports, setuid → 21-26 cron, escapes → 27-33 git", "blue", size=12.5)
p.box("Natas 0-10 HTTP basics → 11-20 crypto, uploads, SQLi → 21-34 sessions, advanced", "green", size=12.5)
p.box("Narnia / Leviathan: read source, setuid binaries, buffer overflows", "amber", size=12.5)
p.note("Do Bandit before Natas; do both before Narnia.")
p.save(OUT, "a-ladders.svg")

p = P("Defence CTF formats", "where each one appears")
p.box("JEOPARDY DEFENCE CHALLENGE: attacks run on demand; patch any time for full points. CyberSci Regionals", "blue", size=12.5)
p.box("DEFENCE COMPETITION: attacks every tick (e.g. 2 min); points gained or lost each tick. CyberSci Nationals", "amber", size=12.5)
p.box("ATTACK & DEFENCE: health checks (SLA) every tick; you also attack other teams. ICC, ECSC", "purple", size=12.5)
p.note("Source: CyberSci Defence CTF 101 workshop (CyberSCI/Workshops).")
p.save(OUT, "d-formats.svg")

chain("d-phases.svg", "Phases of a defence challenge", "from days before to the patch",
      ["BEFORE: learn the rules, scoring, tick length, infrastructure (Docker/VMs)",
       "PREP (first 30-60 min): git baseline, backup tarball, know how to stop/start the app",
       "INVESTIGATE: find the exploits that are actually being used",
       "PATCH: smallest change that stops the exploit; deploy; verify",
       "WATCH: confirm health checks stay green; revert if needed"],
      "You only score for vulnerabilities that are being actively exploited.")

chain("d-patch-loop.svg", "The patch loop", "repeat safely",
      ["Reproduce locally (or in the VM) and understand the attack",
       "Edit the code; commit with a clear message",
       "docker compose build, then docker compose up -d",
       "Re-run the attack and the health check",
       "Broken? git revert, rebuild, redeploy"],
      "Always keep a baseline commit and a backup tarball.")

p = P("Five ways to find the exploit", "from the workshop")
for t, c in [("1 Watch the network (Wireshark, ssh remote capture)", "blue"),
             ("2 Look for indicators on the live service (broken images, odd accounts)", "green"),
             ("3 Review the code (secrets, injection, OWASP Top 10)", "amber"),
             ("4 Add your own logging where it matters", "purple"),
             ("5 Go on offence: reproduce the attack yourself", "red")]:
    p.box(t, c, size=12.5)
p.note("Network is king until traffic is encrypted or the bug is pure logic.")
p.save(OUT, "d-signals.svg")

p = P("Official CyberSci regional skills", "from the organizers, mapped to this pack")
for a, b, c in [("Networking + Nmap beyond the local subnet", "modules 6, 2, 11", "blue"),
                ("Web: SQLi, file include, command injection, traversal", "module 3", "red"),
                ("Basic SQL: show/describe/select, wildcards", "module 3 + labs", "amber"),
                ("Memory analysis (forensics)", "module 2 §2.4, 13", "green"),
                ("Reverse engineering + beginner pwn", "module 5", "purple"),
                ("Crypto algorithms and weaknesses", "module 4", "teal"),
                ("App vulnerability analysis + defence", "module 3, defence guide", "blue"),
                ("Security news + known vulnerabilities", "defence guide §6", "gray"),
                ("Reverse shells and hacker tools", "module 6 §6.2", "red"),
                ("Basic programming", "module 11", "amber")]:
    p.box(f"{a}: {b}", c, size=12)
p.note("Not needed: routing protocols (RIP, BGP, OSPF). 'It's a hacker event: there will be surprises.'")
p.save(OUT, "os-map.svg")

print(len(list(OUT.glob("*.svg"))), "activity SVGs ->", OUT)
