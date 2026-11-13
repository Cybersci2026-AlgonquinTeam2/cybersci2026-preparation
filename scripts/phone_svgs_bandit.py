"""Phone-first versions of the Bandit diagrams -> curriculum/bandit/img-phone/"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phone_svg import P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "curriculum" / "bandit" / "img-phone"


def journey():
    p = P("Bandit journey map", "34 levels in 13 skill clusters")
    for lv, t, c in [("0-4", "Basics: ssh, cat, odd filenames", "blue"),
                     ("5-6", "find: filter by properties", "green"),
                     ("7-9", "grep, sort, uniq, strings", "amber"),
                     ("10-12", "base64, ROT13, hex + compression", "purple"),
                     ("13", "SSH keys", "red"),
                     ("14-16", "nc, TLS, nmap", "teal"),
                     ("17-19", "diff, remote commands, setuid", "blue"),
                     ("20", "sockets: be the server", "green"),
                     ("21-23", "cron jobs", "amber"),
                     ("24", "brute force a PIN", "purple"),
                     ("25-26", "restricted shell, vim escape", "red"),
                     ("27-31", "git: log, branch, tag, push", "teal"),
                     ("32-33", "uppercase shell, finish", "gray")]:
        p.box(f"Levels {lv}:  {t}", c, size=13.5)
    p.save(OUT, "00-journey.svg")


def ssh_connection():
    p = P("How you reach Bandit", "SSH on port 2220")
    p.box("Your PC\nWindows Terminal", "blue", weight="bold")
    p.arrow("ssh bandit0@bandit.labs\n.overthewire.org -p 2220")
    p.gap(14)
    p.box("bandit server\nsshd listening on 2220", "green", weight="bold")
    p.arrow("encrypted shell")
    p.box("You land in /home/banditN as that user", "gray")
    p.note("Password for level N = what you found in level N-1.\nLevel 0 password: bandit0")
    p.save(OUT, "01-ssh-connection.svg")


def filesystem():
    p = P("The Linux file system", "where Bandit hides things")
    p.box("/   (root)", "gray", mono=True, weight="bold")
    p.box("/home/banditN  =  ~\nyour starting folder", "blue")
    p.box("/etc/bandit_pass/\none file per user; only that user can read it", "red")
    p.box("/tmp\nanyone can write: your scratch space", "green")
    p.box("/var/spool, /var/log\nqueues and logs", "amber")
    p.box("/usr/bin\nprograms and scripts (cron jobs live here)", "purple")
    p.note(".  = this folder      ..  = parent folder\n~  = your home        /  = the root\nstarts with /  =  absolute path", mono=True)
    p.save(OUT, "02-filesystem.svg")


def filenames():
    p = P("Filenames that fight the shell", "levels 1-4")
    for a, b, c, col in [("-", "looks like stdin / an option", "cat ./-", "blue"),
                         ("spaces in this filename", "split into 4 arguments", 'cat "spaces in this filename"', "green"),
                         (".hidden", "ls skips dotfiles", "ls -a   then   cat ./.hidden", "amber"),
                         ("-file07", "starts with - so looks like a flag", "cat ./-file07", "purple")]:
        p.box(a, col, mono=True, weight="bold", gap=2)
        p.note("problem: " + b, size=12.5)
        p.box("fix:  " + c, "white", mono=True, size=12.5, gap=12)
    p.save(OUT, "03-filenames.svg")


def find_funnel():
    p = P("find is a funnel", "each test throws files away (levels 5-6)")
    steps = [("find /", "every file on disk", "gray"),
             ("-type f", "regular files only", "blue"),
             ("-size 33c", "exactly 33 bytes", "green"),
             ("-user bandit7", "owned by bandit7", "amber"),
             ("-group bandit6", "group is bandit6", "purple"),
             ("1 file left", "cat it", "red")]
    for i, (a, b, c) in enumerate(steps):
        w = 388 - i * 46
        p.box(a, c, mono=True, weight="bold", sub=b, x=(420 - w) / 2, w=w, gap=6)
    p.note("Add 2>/dev/null to hide 'Permission denied' noise (stderr to the trash).")
    p.save(OUT, "04-find-funnel.svg")


def pipes():
    p = P("Pipes", "each command's output feeds the next (levels 7-9)")
    p.box("cat data.txt", "blue", mono=True)
    p.arrow("|")
    p.box("sort\ngroups equal lines together", "green", mono=True)
    p.arrow("|")
    p.box("uniq -u\nkeeps lines that occur ONCE", "amber", mono=True)
    p.arrow()
    p.box("the answer", "red", weight="bold")
    p.note("uniq only compares NEIGHBOURING lines, so sort first.\ngrep PATTERN file: keep matching lines.\nstrings file | grep '==': readable text out of binary junk.")
    p.save(OUT, "05-pipes.svg")


def encodings():
    p = P("Decoding onions", "peel one layer at a time (levels 10-12)")
    p.box("Level 12 loop:  file → pick tool → peel → file …", "gray", weight="bold")
    p.row([("hex dump\nxxd -r", "gray"), ("gzip\ngzip -d", "blue")])
    p.row([("bzip2\nbzip2 -d", "green"), ("tar\ntar xf", "amber")])
    p.box("until file says ASCII text → cat it", "red")
    p.gap(6)
    p.box("Level 11: ROT13 shifts letters by 13\nA→N  B→O  C→P … M→Z  (twice = original)", "purple")
    p.box("tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt", "white", mono=True, size=12)
    p.box("Level 10: base64 -d data.txt", "white", mono=True, size=12.5)
    p.save(OUT, "06-encodings.svg")


def ssh_keys():
    p = P("SSH key login", "prove who you are without sending a password")
    p.row([("YOU hold the PRIVATE key\n(secret, chmod 600)", "red"), ("SERVER holds the PUBLIC key\n(authorized_keys)", "green")])
    p.arrow("1. I'm bandit14", "blue")
    p.arrow("2. sign this random challenge", "green")
    p.arrow("3. here is my signature", "blue")
    p.box("server verifies with the public key → you're in", "amber")
    p.box("ssh -i sshkey.private bandit14@localhost -p 2220", "white", mono=True, size=12)
    p.note("'UNPROTECTED PRIVATE KEY FILE' → chmod 600 keyfile")
    p.save(OUT, "07-ssh-keys.svg")


def ports():
    p = P("Ports: one machine, many doors", "levels 14-16")
    p.box("localhost  (the server you are on)", "gray", weight="bold")
    p.arrow()
    p.box("30000  plain TCP", "blue", weight="bold", sub="nc localhost 30000")
    p.box("30001  TLS / SSL", "green", weight="bold", sub="openssl s_client -quiet -connect localhost:30001")
    p.box("31000-32000  1000 ports", "amber", weight="bold",
          sub="most closed, some echo, ONE speaks TLS and returns a key.  nmap -p 31000-32000 localhost")
    p.note("Plain TCP: text goes as-is.  TLS: encrypted first, nc can't talk to it.\nIf s_client prints RENEGOTIATING / KEYUPDATE, add -quiet.")
    p.save(OUT, "08-ports.svg")


def setuid():
    p = P("setuid: borrow the owner's identity", "levels 19 and 26")
    p.box("Normal program\nyou (bandit19) run cat\n→ runs AS bandit19\n→ /etc/bandit_pass/bandit20: DENIED", "red")
    p.box("setuid program  -rwsr-x---\n./bandit20-do cat …\n→ runs AS bandit20 (owner)\n→ file readable: ALLOWED", "green")
    p.box("ls -l shows the s:\n-rwsr-x---  bandit20 bandit19  bandit20-do", "white", mono=True, size=12)
    p.note("Find all setuid files:  find / -perm -4000 2>/dev/null\nThey are prime privilege-escalation targets (GTFOBins).")
    p.save(OUT, "09-setuid.svg")


def cron():
    p = P("cron: scheduled robot", "levels 21-23")
    p.box("/etc/cron.d/cronjob_banditN\n* * * * *  banditN  script.sh", "blue", mono=True, size=12.5)
    p.arrow("every minute")
    p.box("script.sh runs AS banditN\nwrites the password to /tmp/<name>", "amber")
    p.arrow()
    p.box("YOU: cat /tmp/<name>", "green", mono=True)
    p.note("Method: ls /etc/cron.d → cat the job → cat the script → work out the output file → cat it.\nLevel 23 flips it: YOU write the script, cron (as bandit24) runs it.")
    p.save(OUT, "10-cron.svg")


def suconnect():
    p = P("Be the server (level 20)", "two terminals")
    p.box("Terminal 1\nnc -l -p 4444   (listen)", "blue", mono=True)
    p.box("Terminal 2\n./suconnect 4444", "green", mono=True)
    for n, t in enumerate(["T1 starts listening on port 4444",
                           "T2 runs suconnect: it dials localhost:4444",
                           "you send bandit20's password through T1",
                           "suconnect checks it; if right, SENDS the next password back"], 1):
        p.box(f"{n}.  {t}", "amber" if n % 2 else "white", size=13)
    p.note("One-shell version:\necho \"$(cat /etc/bandit_pass/bandit20)\" | nc -l -p 4444 &\n./suconnect 4444", mono=True)
    p.save(OUT, "11-suconnect.svg")


def git():
    p = P("Git in one picture", "levels 27-31")
    p.row([("working folder", "blue"), ("staging", "green")])
    p.arrow("git add")
    p.row([("local repo", "amber"), ("remote origin", "purple")])
    p.arrow("git commit → git push")
    p.gap(4)
    p.box("History = chain of commits\nc1 ← c2 ← c3 (SECRET added) ← c4 (removed) ← c5 HEAD", "red", size=12.5)
    p.note("Level 28: removed in the newest commit, still in c3 → git log -p")
    p.box("master / dev  = branches (level 29: git branch -a)", "green", size=12.5)
    p.box("secret  = a tag (level 30: git tag, git show secret)", "purple", size=12.5)
    p.box("level 31: git add -f key.txt → commit → git push origin master", "white", mono=True, size=11.5)
    p.save(OUT, "12-git.svg")


def bruteforce():
    p = P("Brute force a 4-digit PIN", "10,000 tries, one pipe (level 24)")
    p.box('for i in {0000..9999}\n  echo "PASS $i"', "blue", mono=True)
    p.arrow("one long stream, 10,000 lines")
    p.box("nc localhost 30002", "green", mono=True)
    p.arrow()
    p.box("daemon on :30002 replies line by line", "amber")
    p.arrow("| grep -v Wrong")
    p.box("the one reply that is not 'Wrong!'", "red")
    p.note("Zero padding matters: 0007, not 7.  Real systems add lockouts and rate limits.")
    p.save(OUT, "13-bruteforce.svg")


def restricted():
    p = P("Escape a restricted shell", "more → vim (level 25)")
    for i, (a, c) in enumerate([("ssh as bandit26: login shell is /usr/bin/showtext, not bash", "red"),
                                ("showtext runs more; text fits → prints and logs you out", "gray"),
                                ("shrink the terminal window → more PAUSES", "amber"),
                                ("press v → more opens vim", "green"),
                                (":set shell=/bin/bash  then  :shell", "blue")]):
        p.box(f"{i + 1}.  {a}", c, size=13)
        if i < 4:
            p.arrow()
    p.note("Or in vim:  :r /etc/bandit_pass/bandit26\nAny program that can launch another program (more, less, vim, man, find, git…) is an exit.")
    p.save(OUT, "14-restricted-shell.svg")


def uppercase():
    p = P("The uppercase shell", "level 32")
    p.box("you type:  ls", "blue", mono=True)
    p.arrow("shell uppercases")
    p.box("LS: command not found", "gray", mono=True)
    p.gap(10)
    p.box("you type:  $0", "blue", mono=True)
    p.arrow("$ and digits have no case")
    p.box("$0 expands to the shell's name (sh)", "green")
    p.arrow()
    p.box("a normal sh starts: lowercase works again", "amber")
    p.save(OUT, "15-uppercase.svg")


for f in (journey, ssh_connection, filesystem, filenames, find_funnel, pipes, encodings, ssh_keys,
          ports, setuid, cron, suconnect, git, bruteforce, restricted, uppercase):
    f()
print(len(list(OUT.glob("*.svg"))), "phone SVGs ->", OUT)
