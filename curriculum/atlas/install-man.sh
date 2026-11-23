#!/usr/bin/env bash
# Install the CyberSci Command Atlas man pages for the current user (Kali, Ubuntu, WSL, any Linux with man-db).
#   bash install-man.sh        then open a new shell:  man atlas   |   man atlas-grep   |   gm grep
set -e
here="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.local/share/atlas/man"
mkdir -p "$dest/man1"
cp "$here"/man/man1/*.1 "$dest/man1/"
line='export MANPATH="$HOME/.local/share/atlas/man:${MANPATH:-}:"'
fn='gm() { man "atlas-$1" 2>/dev/null || man "$1"; }'
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  [ -f "$rc" ] || continue
  grep -q 'atlas/man' "$rc" || printf '\n# CyberSci Command Atlas man pages\n%s\n%s\n' "$line" "$fn" >> "$rc"
done
echo "Installed $(ls "$dest/man1" | wc -l) pages to $dest"
echo "Open a new terminal, then try:  man atlas   or   gm grep"
