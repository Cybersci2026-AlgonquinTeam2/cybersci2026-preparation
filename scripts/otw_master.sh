#!/usr/bin/env bash
# Open a shared (multiplexed) SSH connection to an OverTheWire game, run it in WSL.
#   bash otw_master.sh narnia            # level 0, public default password (narnia0)
#   OTW_PASS='...' bash otw_master.sh narnia 3   # a later level, password from the environment
# Leave the window open: other commands reuse the connection through /tmp/cm-<game>.
# Only the public starter password (same as the user name) is built in; never put real
# credentials in this file.
set -eu
game="${1:?usage: otw_master.sh <game> [level]}"
level="${2:-0}"
case "$game" in
  bandit) port=2220;; natas) echo "natas is web-only, no SSH"; exit 1;;
  krypton) port=2231;; leviathan) port=2223;; narnia) port=2226;;
  behemoth) port=2221;; utumno) port=2227;; maze) port=2225;;
  manpage) port=2224;; vortex) port=2228;; formulaone) port=2232;;
  drifter) port=2230;;
  *) echo "unknown game: $game"; exit 1;;
esac
user="${game}${level}"
pass="${OTW_PASS:-}"
if [ -z "$pass" ]; then
  if [ "$level" = "0" ]; then pass="$user"; else read -r -s -p "password for $user: " pass; echo; fi
fi
sock="/tmp/cm-${game}"
rm -f "$sock"
askpass="$(mktemp)"
printf '#!/bin/sh\necho "$OTW_ASKPASS_VALUE"\n' > "$askpass"; chmod 700 "$askpass"
trap 'rm -f "$askpass" "$sock"' EXIT
echo "Connecting as $user to $game.labs.overthewire.org:$port ... leave this window open."
OTW_ASKPASS_VALUE="$pass" SSH_ASKPASS="$askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh -M -N -S "$sock" -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 \
      -p "$port" "$user@$game.labs.overthewire.org"
