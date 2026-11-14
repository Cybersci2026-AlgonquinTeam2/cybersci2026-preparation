# 26. Defence challenge lab runbook (Defence CTF 101)

Status: a runbook for the organizers' own workshop (`external/Workshops/2026/defence-ctf-101`, read from the repo's README; not yet run on your machine). This book deliberately gives **hints, not the answer key**: the workshop is a discovery exercise, and reading the answers first would waste it. If you want the answer key later, ask for it after your first attempt.

## 1. What a defence challenge is (layman)

You are the security guard of a shop that is being robbed on a schedule. A tester ("the attacker") keeps attacking your website. Your job is to keep the shop open **and** fix the holes so the attacks stop working.

You score for uptime and for blocking attacks. You lose for taking the site down or breaking real features. So the skill is **safe, small, fast fixes**.

## 2. The cycle (technical)

```
 snapshot/backup  ->  watch an attack  ->  find the cause  ->  minimal patch  ->  rebuild  ->  retest  ->  keep or revert
        ^                                                                                              |
        +-----------------------------------------------------------------------------------------------+
```
Four levers: **observe** (logs, traffic captures, `docker compose logs -f`), **read** (source of the service), **patch** (smallest code or config change that closes the hole), **verify** (rerun the attack; confirm real features still work).

## 3. Run the lab (check these before you start)

From the workshop README (read it yourself; treat the repo as untrusted):
1. Docker with the Compose plugin and at least 4 GB of memory for Docker.
2. Free ports: 80, 67, 666, 2222 and 6767 (all published on 127.0.0.1 only: keep it that way, the app is vulnerable on purpose and the helper container is privileged).
3. `docker compose up -d` in `Workshops/2026/defence-ctf-101`, then open `http://localhost` and wait for three green lights.
4. Reset to a clean slate with `docker compose down -v`.
Run it on a lab machine or VM, not on a machine holding anything you care about.

Quick preflight: `docker version`, `docker compose version`, and check nothing else uses the ports (`netstat -ano | findstr :80` on Windows).

## 4. Setup before the first attack (10 minutes)

- [ ] Note the services and ports (the table in the README).
- [ ] SSH into the service VM (port 2222) and find where the app source lives.
- [ ] `git init` the source folder and commit it: your baseline and your undo button.
- [ ] Copy the folder to a backup path.
- [ ] Open a log tail: `docker compose logs -f` (inside the VM for the app).
- [ ] Start a Wireshark capture on the VM's interface (optional but powerful).
- [ ] Know the rebuild command and how long a rebuild takes.

## 5. Per-attack investigation drill (the hint ladder)

For each attack the portal launches:

**Rung 1: observe.** What did the log show at the moment of the attack? Which URL, method, parameters, which status code? Write one line.
**Rung 2: reproduce.** Can you repeat the request yourself with `curl`? Does it behave the same?
**Rung 3: classify.** Which class is it: injection, path traversal, broken access control, missing authentication, unsafe file upload, secrets in code, verbose errors?
**Rung 4: find it in the source.** Search the code for the handler of that URL; follow the input to where it is used (database query, file path, shell call, template).
**Rung 5: patch minimally.** Parameterize the query; validate and canonicalize the path; check authorization on the server; restrict upload types and locations; remove the secret; do **not** rewrite the app.
**Rung 6: verify twice.** Rerun the attack (it must now fail) and test the normal feature (it must still work). Commit the patch with a message.
**Rung 7: if the service breaks:** `git diff`, then revert.

Never skip rung 6: an unverified patch is a coin flip with your uptime.

## 6. Reading unknown source quickly (30-minute method)

1. Find the **entry points**: routes/handlers, file uploads, login.
2. Search for dangerous sinks: `exec`, `system`, `Command`, string-built SQL (`+`, `fmt.Sprintf` in queries), `os.Open`/`ReadFile` with user-influenced paths, `eval`, `unserialize`, template rendering of raw input.
3. Search for **missing checks**: handlers that never read the session/user, ids taken from the URL without ownership checks.
4. Search for **secrets**: hard-coded passwords, tokens, keys.
5. Read authentication code twice: small mistakes there break everything.
This is the CyberSci "application vulnerability analysis" skill, in practice.

## 7. Patching toolbox (what to reach for)

| Bug class | Fix |
|---|---|
| SQL injection | prepared statements / parameter binding |
| Path traversal / LFI | resolve to an absolute path, then verify it stays under the allowed folder |
| Command injection | no shell; pass arguments as a list; allowlist values |
| Broken access control | check the logged-in user owns the object on every request |
| Weak or missing auth | verify tokens/sessions server-side; no client-trusted flags |
| Unsafe upload | allowlist extension and content type, random file names, store outside the web root |
| XSS | output-encode in templates; do not render raw HTML |
| Info leaks | turn off debug and verbose errors |
| Secrets in code | move to environment/config; rotate |

Rules of thumb: patch the **cause**, not the exploit's exact string; prefer allowlists to blocklists; change as little as possible.

## 8. Timeline and roles (for the real event)

| Time | Action |
|---|---|
| 0-15 min | baseline, backups, logs, packet capture, map the service |
| ongoing | one person watches logs and traffic; one reads source; one patches and tests |
| after every attack | write a line in a shared log: attack, cause, patch, verified |
| last 15 min | stop risky changes; confirm the service is up and healthy |

## 9. The attempt loop (read, do, review, reinforce, repeat)

1. **Read** sections 1-7 (20 min).
2. **Attempt 1 (90 min):** run the workshop; for every attack use the hint ladder; keep a log.
3. **Review:** which attacks did you stop? which took too long? which patch broke something?
4. **Reinforce:** reread section 6 and the patching table; make 5 flashcards.
5. **Attempt 2 (60 min):** `docker compose down -v` for a clean slate; do it again, **source review and logging first**, faster.
6. **Review 2:** time per attack; write your own 1-page checklist.

## 10. Flashcard prompts

- What are the four levers of defence?
- Why initialise git before changing anything?
- Why parameterize SQL instead of filtering quotes?
- What is the difference between a blocklist and an allowlist?
- Why verify twice after a patch?
- What would you do if your patch took the service down?

## 11. Common mistakes

- Fixing the symptom (blocking one string) instead of the cause.
- Patching without a baseline, then not knowing what you changed.
- Changing many things at once, so you cannot tell which one broke the site.
- Forgetting to rebuild or restart after editing the source.
- Letting uptime slip while chasing a perfect fix.

## 12. Defender's view: spotting and cutting off a remote shell

The CyberSci skills list mentions hacker tools and reverse shells. In a defence challenge you meet them from the other side: an attacker who exploited the app wants a shell that "calls home". Your job is to notice it, identify how it got there, and close the hole. (How attackers build shells is practised in the guided rooms on TryHackMe; this section is the detection and response half.)

**Layman:** a reverse shell is a hidden phone line from your server to the attacker. You find it by checking *which processes are on the phone and who they are talking to*, then you hang up and fix whatever let the line in.

### 12.1 Signs on the server (Linux)

| Question | Command | Suspicious sign |
|---|---|---|
| Who is connected outward? | `ss -tnp` (or `ss -tnpa`) | an established connection from `bash`, `sh`, `python`, `nc` or the web server's user to an unknown IP and odd port |
| What opened it? | `lsof -i -n -P` | a shell process holding a network socket |
| What is the process family? | `ps -ef --forest` | a web server or app process that spawned `sh`/`bash` |
| Where did it run from? | `ls -l /proc/<PID>/exe /proc/<PID>/cwd` | binary or directory in `/tmp`, `/dev/shm` or the upload folder |
| What was it told to do? | `cat /proc/<PID>/cmdline \| tr '\0' ' '` | a command line mentioning an IP/port, `/dev/tcp`, `mkfifo` or an encoded blob |
| Did it add persistence? | `crontab -l`, `/etc/cron*`, `~/.ssh/authorized_keys`, `systemctl list-units --type=service --state=running`, `ls -la /etc/systemd/system` | new cron lines, unknown keys, unknown services |

Remember: **no legitimate web app needs to run a shell**. A server process with a shell as its child is the single strongest signal.

### 12.2 Signs in logs and traffic

- Web/app logs: a request just before the shell appears that contains command-like text (`;`, `|`, backticks, `$(`), a path to an uploaded script, or a file extension that should not run.
- Wireshark display filters: `tcp.flags.syn==1 && tcp.flags.ack==0` (new connections), `ip.dst == ATTACKER_IP`, and *Follow TCP Stream* on a suspicious connection: a shell session shows plain-text commands and their output.
- Long-lived TCP connection with small, interactive-looking packets in both directions, to a port the service never uses.

### 12.3 Windows (if a service runs there)

`netstat -ano` then `tasklist /fi "PID eq <PID>"` to map a connection to a process; PowerShell `Get-NetTCPConnection -State Established | Select RemoteAddress,RemotePort,OwningProcess`; Task Manager "details" tab for parent/child; Sysmon event 3 (network connection) and 1 (process create) if installed.

### 12.4 Response order (do it fast, then fix the cause)

1. **Capture evidence first** (10 seconds): save `ss -tnp`, `ps -ef --forest`, and the suspicious process's `/proc/<PID>/cmdline`; screenshot Wireshark.
2. **Cut the line:** `kill -9 <PID>` of the shell *and* its parent if it is the injected process; do not restart the whole service until you know the cause or you will lose the evidence.
3. **Block outbound:** a default-deny egress rule for the service's user or the container (for Docker, restrict the network or drop the route), allowing only what the app truly needs. Reverse shells die when outbound is blocked.
4. **Find the hole:** the request just before the process appeared (logs) leads to the vulnerable handler: injection into a command, an upload that executes, an unsafe deserialiser, an outdated component.
5. **Patch the cause** (section 7), rebuild, retest the attack, confirm the connection cannot be made again.
6. **Hunt persistence:** cron, startup scripts, new users, keys, modified binaries (`find / -mmin -60 -type f 2>/dev/null | head`), then remove them.
7. **Log it** in your attack/cause/patch/verified table.

### 12.5 Hardening that makes shells fail

Run the service as an unprivileged user; read-only filesystem and no write access to the code folder; no shell binary inside minimal containers; no `exec`/`system` on user input; egress allowlist; uploaded files stored outside the web root and never executable; alert on web processes spawning shells.

### 12.6 Flashcard prompts

- Why is a shell as the child of a web server a red flag?
- Which command maps a network connection to a process, and which maps it to a binary path?
- Why block outbound traffic as a defence?
- Why capture evidence before killing a process?
- Where do attackers hide persistence on Linux?
