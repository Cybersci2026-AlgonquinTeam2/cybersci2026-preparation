#!/usr/bin/env python3
"""Add the remaining options (the ones the atlas flag tables did not cover) to converted mangui guides.

    python scripts/mangui_more.py        # merges MORE into mangui/guides/<name>.json (idempotent), then run: python3 mangui/mangui.py coverage
"""
import json
import re
from pathlib import Path

GUIDES = Path(__file__).resolve().parent.parent / "mangui" / "guides"
TOK = re.compile(r"(?<![\w-])(--?[A-Za-z0-9][\w-]*)")

MORE = {}

MORE["find"] = [
    ("-H, -L, -P", "How to treat symbolic links: -P never follows them (default), -L always follows them, -H follows only those named on the command line.", "You must decide whether a link counts as itself or as its target."),
    ("-D debugopts", "Print debugging information (tree, stat, opt, rates, exec, help) about how find works.", "Finding out why a search is slow or not matching."),
    ("-O, -Olevel", "Set the query optimisation level (0 to 3) that reorders cheap tests before expensive ones.", "Rarely: speeding up a huge search."),
    ("-d, -depth", "Process the contents of a directory before the directory itself.", "You are deleting a tree from the bottom up."),
    ("-daystart", "Measure -mtime, -atime and -ctime from the start of today instead of 24 hours ago.", "You mean 'since midnight', not 'in the last 24 hours'."),
    ("-amin n, -atime n", "Match files last read n minutes / n days ago.", "Which files were opened recently?"),
    ("-cmin n, -ctime n", "Match files whose metadata (permissions, owner, name) changed n minutes / days ago.", "Spotting files an attacker touched, since content time can be faked."),
    ("-anewer file, -cnewer file", "Match files read / changed more recently than a reference file.", "What was accessed after the first alert?"),
    ("-newerXY file", "Compare any two timestamps: X and Y are a (access), B (birth), c (change), m (modify) or t (a time string), for example -newermt '2026-11-10'.", "Selecting files by an exact date."),
    ("-used n", "Match files accessed n days after their status last changed.", "Finding files that were used well after creation."),
    ("-context pattern", "Match files whose SELinux security label fits the pattern.", "SELinux systems only."),
    ("-execdir command {} ;, -ok command ;, -okdir command ;", "-execdir runs the command from the file's own folder; -ok and -okdir ask you to confirm each time.", "-execdir is safer than -exec; -ok is for deletions you want to approve."),
    ("-executable, -readable, -writable", "Match files you can execute / read / write with your current permissions.", "Finding what you can use during privilege escalation."),
    ("-true, -false", "Tests that are always true / always false.", "Building conditions in complex expressions."),
    ("-files0-from file", "Read the starting points from a file, separated by NUL bytes.", "A very long list of start folders."),
    ("-fls file, -fprint file, -fprint0 file, -fprintf file format", "Like -ls, -print, -print0 and -printf but write the results into a file.", "Saving evidence lists directly."),
    ("-ls", "Print each match in the long ls -dils style (size, owner, date).", "A quick detailed listing."),
    ("-print", "Print the path of each match, then a newline. This is the default.", "Making it explicit, or combining with -prune."),
    ("-printf format", "Print each match with your own layout, such as %p (path) %s (size) %u (owner) %m (permissions) %t (time).", "Building a custom report."),
    ("-follow", "Old name for -L: follow symbolic links.", "Old scripts."),
    ("-fstype type", "Match files on a given file system type (ext4, tmpfs, nfs).", "Skipping network or virtual drives."),
    ("-mount, -xdev", "Do not descend into other file systems.", "Searching only the disk you are on, not mounted drives."),
    ("-gid n, -uid n", "Match files owned by a numeric group / user id.", "The owner has no name on this system."),
    ("-nogroup, -nouser", "Match files whose group / owner id does not exist in the system.", "Leftovers from deleted users, or files copied from elsewhere."),
    ("-ignore_readdir_race, -noignore_readdir_race", "Do not complain (or do complain) when a file vanishes between listing and checking.", "Searching busy folders such as /tmp or logs."),
    ("-ilname pattern, -lname pattern", "Match symbolic links whose target text matches the pattern (-ilname ignores case).", "Finding links that point somewhere suspicious."),
    ("-path pattern, -ipath pattern, -wholename pattern, -iwholename pattern", "Match against the whole path, not just the file name (the i versions ignore case).", "-name cannot see folders: use -path '*/site/*'."),
    ("-regex pattern, -iregex pattern, -regextype type", "Match the whole path with a regular expression; -regextype chooses the dialect (posix-extended, emacs...).", "Name rules that globs cannot express."),
    ("-inum n, -samefile name", "Match by inode number / match files that are the same file as name (hard links).", "Finding other names for one file."),
    ("-links n", "Match files with n hard links.", "Spotting hard-link tricks."),
    ("-mode", "Not a separate test: it appears in the -perm explanation as the permission mode (octal or symbolic) to compare with.", "Reading the -perm section of the original page."),
    ("-n", "Appears in the original page only as part of an example (for example -newer).", "Ignore as a stand-alone option."),
    ("-noleaf", "Do not use the trick that a folder's link count equals its sub-folders plus 2.", "Searching file systems that break that rule (CD-ROMs, some network drives)."),
    ("-nowarn, -warn", "Turn warnings off / on.", "Quiet scripts."),
    ("-prune", "Do not go into the directory that was just matched.", "Skipping .git or node_modules: find . -name .git -prune -o -print."),
    ("-quit", "Stop searching after the first match.", "You only need to know whether something exists."),
    ("-xtype c", "Like -type, but checks the target of a symbolic link.", "Finding broken links (-xtype l)."),
    ("--help, -help, --version, -version", "Print a usage summary / the version and exit.", "A quick reminder or version check."),
]

MORE["sed"] = [
    ("-e script, --expression=script", "Add the commands in script. Use it several times to run several edits.", "More than one edit in a single run."),
    ("-f script-file, --file=script-file", "Read the editing commands from a file.", "A long set of edits you want to keep and reuse."),
    ("-E, -r, --regexp-extended", "Use extended regular expressions, so + ? | ( ) need no backslash. -E is the portable spelling.", "Anything beyond a simple pattern."),
    ("-i[SUFFIX], --in-place[=SUFFIX]", "Edit the file itself; with a suffix, keep a backup copy.", "Changing a file for real (always give a suffix first)."),
    ("-n, --quiet, --silent", "Do not print every line automatically; print only what the p command selects.", "Printing a few chosen lines."),
    ("-s, --separate", "Treat each input file separately, so line numbers and ranges restart for every file.", "Running the same line-range edit on many files."),
    ("-u, --unbuffered", "Read and write in small pieces instead of large blocks.", "Live output from tail -f piped into sed."),
    ("-z, --null-data", "Use NUL bytes instead of newlines to separate lines.", "Editing text across lines, or output from find -print0."),
    ("-l N, --line-length=N", "Set how many characters the l command (show unprintables) puts on a line.", "Making hidden-character dumps fit the screen."),
    ("--follow-symlinks", "When editing in place, follow symbolic links and edit the real file.", "In-place edits on a path that is a link."),
    ("--posix", "Switch off GNU extensions so sed behaves strictly like the standard.", "Checking that a script will also work on other systems."),
    ("--sandbox", "Refuse commands that read or write files or run programs (r, w, e).", "Running a sed script you did not write."),
    ("--debug", "Print the program in canonical form and show each step as it runs.", "Working out why a script does not behave."),
    ("--help, --version", "Print a usage summary / the version and exit.", "A quick reminder or version check."),
]

MORE["awk"] = [
    ("-f program-file, --file program-file", "Read the awk program from a file instead of the command line.", "A program too long for one line."),
    ("-e program-text, --source program-text", "Give awk program text on the command line; may be used with -f to mix files and snippets.", "Combining library files with a one-liner."),
    ("-E file, --exec file", "Read the program from a file and stop option processing: the file name is the last gawk option.", "Safe scripts such as #! lines in CGI programs."),
    ("-i file, --include file", "Load an awk source library before running.", "Reusing a function library."),
    ("-l lib, --load lib", "Load a compiled gawk extension (a shared library).", "Advanced: file functions, regular-expression helpers."),
    ("-v var=value, --assign var=value", "Set an awk variable before the program starts. -F fs and --field-separator fs set the field separator the same way.", "Passing shell values into awk."),
    ("--field-separator fs", "Long form of -F: the character or regular expression that splits fields.", "Reading colon- or comma-separated data."),
    ("-b, --characters-as-bytes", "Treat every byte as one character, ignoring UTF-8 multi-byte letters.", "Binary data, or exact byte counts."),
    ("-c, --traditional", "Run in compatibility mode: GNU extensions are switched off.", "Matching the behaviour of the original awk."),
    ("-P, --posix", "Run in strict POSIX mode.", "Checking portability."),
    ("-C, --copyright", "Print the copyright notice and exit.", "Rarely needed."),
    ("-d[file], --dump-variables[=file]", "Write all global variables and their final values to a file (default awkvars.out).", "Debugging a program's state."),
    ("-D[file], --debug[=file]", "Run the program under the gawk debugger.", "Stepping through a misbehaving script."),
    ("-g, --gen-pot", "Extract translatable strings from the program into a template.", "Making awk programs available in several languages."),
    ("-h, --help", "Print a usage summary and exit.", "A quick reminder."),
    ("-L[value], --lint[=value]", "Warn about doubtful constructs; use fatal to make warnings stop the program.", "Checking a new script."),
    ("--lint-old", "Warn about things that are not allowed in the original Unix awk.", "Writing scripts that must run everywhere."),
    ("-M, --bignum", "Use arbitrary-precision numbers (needs GMP and MPFR).", "Calculations with huge integers, such as RSA numbers."),
    ("-n, --non-decimal-data", "Treat input numbers with a leading 0 or 0x as octal or hexadecimal.", "Reading hex values from a dump."),
    ("-N, --use-lc-numeric", "Use the number format of your locale (comma as decimal point, for example).", "Locale-specific input."),
    ("-o[file], --pretty-print[=file]", "Write a neatly indented copy of the program to a file instead of running it.", "Reading someone else's compact awk."),
    ("-O, --optimize, --no-optimize", "Turn program optimisation on or off.", "Rarely; for speed or debugging."),
    ("-p[file], --profile[=file]", "Write a profile showing how often each line ran (default awkprof.out).", "Finding the slow part of a script."),
    ("-r, --re-interval", "Allow interval expressions such as {2,3} in regular expressions (on by default in current versions).", "Old scripts."),
    ("-S, --sandbox", "Disable system(), file redirection and extensions.", "Running an awk program you do not trust."),
    ("-t", "Same as --lint-old in current gawk (warn about non-traditional features).", "Writing portable scripts."),
    ("-V, --version", "Print the version and exit.", "Checking which awk (gawk, mawk) you have."),
    ("--trace", "Print the internal instructions as the program runs.", "Debugging gawk itself."),
    ("--profile, --pretty-print", "Aliases for -p and -o listed above.", "Reading output files such as awkprof.out."),
]

MORE["nc"] = [
    ("-4, -6", "Use only IPv4 / only IPv6.", "Names resolve to both and you need to choose."),
    ("-b", "Allow sending to a broadcast address.", "Rare: broadcast tests on a lab network."),
    ("-C", "Send CRLF (carriage return plus line feed) as the line ending.", "Protocols that require CRLF, such as SMTP, HTTP and many text services."),
    ("-D", "Turn on socket debugging.", "Low-level troubleshooting."),
    ("-d", "Do not read from standard input.", "You only want to listen or watch, not send."),
    ("-F", "Pass the socket's file descriptor to another program over a Unix socket (needs -U).", "Advanced scripting."),
    ("-h", "Print a help message.", "A quick reminder."),
    ("-I length, -O length", "Set the TCP receive / send buffer size.", "Tuning file transfers."),
    ("-i interval", "Wait interval seconds between lines of text sent or between ports probed.", "Slowing a scan or a script."),
    ("-M ttl, -m minttl", "Set the outgoing IP time-to-live / require at least this TTL on incoming packets.", "Network experiments."),
    ("-P proxy_username", "Username for proxy authentication.", "Going through an authenticated proxy."),
    ("-p source_port", "Use this local source port.", "Testing rules that depend on the source port."),
    ("-q seconds", "After end of input, wait this many seconds and then quit.", "Making a transfer finish."),
    ("-r", "Choose source and destination ports at random instead of in order.", "Evading simple patterns when scanning in a lab."),
    ("-S", "Enable the TCP MD5 signature option.", "Router-to-router links; rare."),
    ("-s source", "Use this local IP address as the source.", "Machines with several addresses."),
    ("-T keyword", "Set the IP type-of-service or TLS options (for example lowdelay, throughput, reliability).", "Network quality-of-service tests."),
    ("-t", "Answer telnet negotiation requests automatically.", "Talking to telnet-style services."),
    ("-U", "Use Unix-domain sockets (files) instead of the network.", "Local sockets such as /var/run/docker.sock."),
    ("-V rtable", "Use a specific routing table (OpenBSD).", "Not used on Linux."),
    ("-W recvlimit", "Stop after receiving this many packets.", "Limited tests."),
    ("-X proxy_protocol, -x proxy_address[:port]", "Connect through a proxy (4, 5 for SOCKS, connect for HTTP) at the given address.", "Tunnelling nc through a proxy."),
    ("-Z", "Use the DCCP protocol instead of TCP.", "Rare."),
]

MORE["openssl"] = [
    ("-help", "Print a summary of the options for the chosen sub-command.", "A quick reminder inside openssl s_client or openssl enc."),
    ("-key", "Give a key (in hex) directly to a cipher command.", "ECB and CBC experiments with a known key."),
    ("-engine id, -provider name, -provider-path path, -propquery query", "Choose a crypto engine or provider (modules that supply algorithms), where to find them, and a property query to pick implementations.", "Advanced: legacy algorithms, hardware tokens."),
    ("-rand file, -writerand file", "Read random seed data from a file / write the seed state to a file.", "Rare; mostly for reproducing old behaviour."),
    ("-ssl3, -tls1, -tls1_1, -tls1_2, -tls1_3, -dtls, -dtls1, -dtls1_2", "Use only this protocol version when testing a connection (DTLS is the UDP variant).", "Checking whether a server still accepts weak old protocols."),
    ("-no_ssl3, -no_tls1, -no_tls1_1, -no_tls1_2, -no_tls1_3", "Refuse this protocol version.", "Forcing a negotiation to a particular version."),
]


def merge():
    try:
        from mangui_more2 import MORE2
        MORE.update(MORE2)
    except ImportError:
        pass
    for name, more in MORE.items():
        p = GUIDES / f"{name}.json"
        g = json.loads(p.read_text(encoding="utf-8"))
        have = set()
        for o in g["options"]:
            have |= set(TOK.findall(o["flag"]))
        added = 0
        for flag, plain, use in more:
            toks = set(TOK.findall(flag))
            if toks and toks <= have:
                continue
            g["options"].append(dict(flag=flag, plain=plain, use=use))
            have |= toks
            added += 1
        p.write_text(json.dumps(g, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(f"{name}: +{added} options (now {len(g['options'])})")


if __name__ == "__main__":
    merge()
