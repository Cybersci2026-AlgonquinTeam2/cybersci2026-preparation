# mangui: enhanced man pages

`man file`, `man grep` ... show the original manual page, a short pointer near the top, and a LAYMAN GUIDE at the end (plain words, examples with real output, every option explained).

    python3 mangui/mangui.py install     # merge guides into the real pages; installs a `man` wrapper in ~/.local/bin
    python3 mangui/mangui.py coverage    # options explained vs options in each original page
    python3 mangui/mangui.py refresh     # after a system update; `uninstall` removes everything

Done: file and grep (every option). Converted but partial: awk, curl, find, nc, openssl, python3, sed (plus nmap, gdb, sqlite3, tcpdump written, not yet captured). Next: finish every option for those, then the remaining commands and the standalone pages for GUI tools. See curriculum/atlas/MANGUI-SCOPE.md.
