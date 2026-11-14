# 27. Nmap and networking: the deep book

Status: written from the Nmap reference and standard networking practice; **commands not run on your machine yet**. The CyberSci skills list puts "networking and Nmap, including outside the local subnet" first. Only scan machines you own or that a challenge/lab explicitly allows. Nmap's own test host `scanme.nmap.org` allows light scanning; do not hammer it.

## 1. What Nmap does (layman)

Imagine a large building (a network). Nmap walks the corridors and tries every door handle:
1. **Which rooms are occupied?** (host discovery)
2. **Which doors are unlocked?** (port scan)
3. **What is behind each open door?** (service and version detection)
4. **Is there anything obviously wrong inside?** (scripts)

The result is a map you attack or defend from.

## 2. Networking basics you must own

```
 Your machine 192.168.1.20/24         Router 192.168.1.1        Internet / other subnets
        |                                   |                          |
   same subnet: talk directly         different subnet: send to the router (gateway)
```
- **IP address + subnet mask (CIDR):** `192.168.1.20/24` means the first 24 bits are the network, so `192.168.1.0`-`192.168.1.255` is "local". Anything outside goes through the gateway.
- **Ports:** a number (0-65535) naming a service on a host. TCP = reliable, connection-based (handshake SYN, SYN/ACK, ACK). UDP = fire-and-forget.
- **Common ports:** 21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 139/445 SMB, 143 IMAP, 443 HTTPS, 3306 MySQL, 3389 RDP, 5432 Postgres, 5900 VNC, 6379 Redis, 8080 alt-HTTP.

| CIDR | Hosts | Mask |
|---|---|---|
| /32 | 1 | 255.255.255.255 |
| /30 | 2 usable | 255.255.255.252 |
| /24 | 254 usable | 255.255.255.0 |
| /16 | 65,534 | 255.255.0.0 |
| /8 | 16.7 M | 255.0.0.0 |

Private ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.

## 3. Reading port states (the most-tested skill)

| State | Meaning |
|---|---|
| open | a service answered |
| closed | host answered "nothing here" (reachable but no service) |
| filtered | no answer: a firewall is dropping packets, or the host is down |
| open\|filtered | UDP and some scans: could not tell |

`filtered` is not "closed": it means you are being stopped by something. That is information.

## 4. The core commands, explained

```bash
nmap 192.168.1.10                         # top 1000 TCP ports, host discovery first
nmap -sn 192.168.1.0/24                   # ping sweep only: which hosts are up (no port scan)
nmap -Pn 192.168.1.10                     # skip host discovery: treat it as up (needed when ICMP is blocked)
nmap -p- 192.168.1.10                     # all 65,535 TCP ports
nmap -p 22,80,443 192.168.1.10            # chosen ports; -p 1-1024 for a range
nmap --top-ports 100 192.168.1.10         # the 100 most common
nmap -sV 192.168.1.10                     # probe open ports for service name and version
nmap -sC 192.168.1.10                     # run the default NSE scripts
nmap -O 192.168.1.10                      # guess the operating system (needs root)
nmap -A 192.168.1.10                      # aggressive: -sV -sC -O --traceroute
nmap -sU --top-ports 50 192.168.1.10      # UDP scan (slow; needs root)
nmap -sS 192.168.1.10                     # SYN ("half-open") scan: default when root
nmap -sT 192.168.1.10                     # full TCP connect scan: works without root and through proxies
nmap -T4 192.168.1.10                     # timing template 0-5 (T4 is a good lab default; T5 can miss ports)
nmap -v / -vv 192.168.1.10                # show progress and open ports as found
nmap -oA scan1 192.168.1.10               # save in all three formats: scan1.nmap / .xml / .gnmap
```
Piece by piece, the CTF default: **`nmap -p- -T4 TARGET`** to find every open port, then **`nmap -sV -sC -p <those ports> TARGET`** to look closely. Doing the full-port sweep first stops you missing a service on an odd port, and the targeted second pass is much faster than `-A` on 65k ports.

Targets can be an IP, a name, a CIDR (`192.168.1.0/24`), a range (`192.168.1.1-50`), a list, or a file (`-iL hosts.txt`); exclude with `--exclude`.

## 5. Scanning outside the local subnet (the CyberSci line)

When the target is on another network, packets route through a gateway, and extra devices (firewalls, NAT) sit in between.

1. **Check the route:** `ip route` (Linux) / `route print` (Windows). Is there a path to that subnet? `traceroute TARGET` or `nmap --traceroute TARGET` shows hops.
2. **ICMP is often blocked** across networks, so host discovery says "down" for hosts that are up: use `-Pn`.
3. **Discovery without ICMP:** `nmap -PS22,80,443 -PA80 TARGET` (TCP SYN/ACK probes to ports likely open).
4. **Firewalls change results:** many `filtered` ports means a firewall; try other source behaviour (`--source-port 53` or `-f` fragmenting) only where you are authorised.
5. **Pivoting (conceptually):** if you can only reach the second network *through* a compromised or provided host, you tunnel your scan through it (for example SSH dynamic forwarding `ssh -D 1080 user@jump` plus `proxychains nmap -sT -Pn TARGET`; use `-sT` and `-Pn` because SYN and ICMP do not pass through a SOCKS proxy).
6. **Slow networks:** raise `--host-timeout`, lower speed with `-T2`, or scan a short list of ports first.

Quick drill: draw two subnets and a router, then decide which of `-sn`, `-Pn`, `-sT` or `-sS` you would use for a target one hop away and why.

## 6. NSE: the Nmap Scripting Engine

```bash
nmap -sC TARGET                           # default, safe scripts
nmap --script vuln TARGET                 # known-vulnerability checks (can be noisy)
nmap --script http-enum -p80 TARGET       # find common web paths
nmap --script smb-enum-shares -p445 TARGET
nmap --script "ftp-anon,ssh-auth-methods" -p21,22 TARGET
nmap --script-help http-enum              # read what a script does before running it
ls /usr/share/nmap/scripts | grep smb     # find scripts by service
```
Categories: `default`, `safe`, `discovery`, `version`, `vuln`, `auth`, `brute`, `exploit` (the intrusive ones need explicit permission). Read `--script-help` first.

## 7. Turning output into next steps

| You see | Do next |
|---|---|
| 80/443 open | browse; `gobuster`/`ffuf`; Module 3 web attacks |
| 21 ftp (anonymous allowed) | `ftp TARGET`, login `anonymous` |
| 22 ssh | note the version; try credentials you found elsewhere |
| 139/445 smb | `smbclient -L //TARGET -N`, `enum4linux` |
| 3306/5432 DB | try default or leaked credentials |
| 6379 redis | check unauthenticated access |
| 8080/8443 | other web apps or admin panels |
| odd high port | `nc TARGET PORT` and read the banner |

Banner grabbing by hand: `nc -nv TARGET PORT` (type nothing, or `HEAD / HTTP/1.0` then Enter twice for web).

## 8. Saving and searching results

```bash
nmap -oA recon/target -p- -T4 TARGET      # always save
grep -E "open" recon/target.gnmap          # quick filter
xsltproc recon/target.xml -o recon/target.html   # readable report
```
Notes habit: paste the open-ports table into your notes with the date and the exact command.

## 9. Other network tools to pair with Nmap

`masscan` (very fast port sweep), `rustscan` (fast wrapper), `tcpdump -i eth0 -n host TARGET` (watch packets), Wireshark (display filters `tcp.port==80`, `ip.addr==10.0.0.5`, `tcp.flags.syn==1`), `dig`/`nslookup` (DNS), `curl -v` (HTTP detail), `arp-scan -l` (local hosts), `ip neigh`.

## 10. Learn by doing

1. **Own network first:** `nmap -sn YOUR_LAN/24`, then scan one lab VM with the section 4 two-step. Write down what each port is.
2. **Make states appear:** on a lab VM, start a service (`python3 -m http.server 8000`), block another port with the firewall, rescan, and watch `open` vs `filtered` change.
3. **Another subnet:** on VMware, create a second host-only network, route between two VMs, and scan across it with and without `-Pn`.
4. **Platform rooms:** the TryHackMe Nmap and network-services rooms and Hack The Box starting-point machines apply this on safe targets.
5. **The loop:** attempt (30 min) → check against `-oA` output → reread sections 3 and 5 → attempt again with a different target.

## 11. Flashcard prompts

- What is the difference between `filtered` and `closed`?
- What does `-Pn` do and when do you need it?
- Why scan all ports first, then `-sV -sC` on the open ones?
- Why does `-sS` need root and `-sT` not?
- How do you scan through an SSH SOCKS proxy, and what must you change?
- How many hosts are in a /24? A /16?
- Name five default ports and their services.

## 12. Cheat sheet

```
nmap -p- -T4 -oA recon/t TARGET
nmap -sV -sC -p P1,P2,P3 -oA recon/t2 TARGET
nmap -sn CIDR                    # who is up
nmap -Pn TARGET                  # ICMP blocked
nmap -sU --top-ports 50 TARGET   # UDP
nmap --script vuln -p P TARGET   # only if allowed
```
