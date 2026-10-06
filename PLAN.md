# CyberSci Prep: Scope and Plan

## Target

Regional Qualifiers are planned here as an on-site, one-day jeopardy-style competition on **Saturday, November 21, 2026**. This date, format, team rules, AI rules, internet availability, and laptop policy are tracked as claims in [`evidence/claims.md`](evidence/claims.md) until verified with current organizer material.

## Dress rehearsals

The rehearsal sequence is intentional:

1. **FortID CTF, Oct 9–11** — no AI; baseline only.
2. **DEADFACE, Oct 17–19** — first team run with the AI stack.
3. **Hack.lu and HITCON, Oct 23–25** — difficult learning events; do not use score as the primary metric.
4. **CSCTF, PINK+, and HKCERT Quals, Nov 6–9** — volume and category comparison.
5. **Platypwn, Nov 13–14** — tiered difficulty practice.
6. **WolvCTF, Nov 13–15** — approachable university event.
7. **InIt CTF, Nov 14** — full-length dress rehearsal: team roles, offline laptop, setup, and chosen AI mode.

GlacierCTF, Nov 20–21, is intentionally skipped because it overlaps the final preparation window.

## Skill priorities

Prioritize web exploitation, forensics/network analysis, reverse engineering, pwn, crypto, Windows/AD/Linux, and blue-team/incident response. The existing networking and Windows lab experience should reduce the time needed for fundamentals there; web, reverse/pwn, and incident response under time pressure are current candidates for concentrated practice.

## AI architecture

Use a laptop-first router with this fallback order:

```text
laptop-local model
        ↓ unavailable or insufficient
Machine B over authenticated Tailscale endpoint
        ↓ unavailable or policy permits internet
hosted API
```

Every path must expose capability and provenance to the caller. A failed remote request must not erase the fact that the answer came from a fallback model.

Start with three useful components:

- offline-first model/router;
- notes and RAG search;
- shell-in-container MCP server with an allowlist, command log, and no factory-directory mounts.

Later components may include pcap/tshark, Ghidra headless, CTFd, and GDB/pwndbg integrations. Build pipelines before free-roaming agents.

## Measurement

Track points per hour, solve rate, false leads, time to first useful observation, and category-specific outcomes. Compare FortID and DEADFACE carefully: they are different events, so the comparison is directional evidence, not a controlled experiment. For stronger evidence, replay solved challenge sets with AI/no-AI conditions.

## Build order

1. Verify competition rules and event dates from primary sources.
2. Create the offline laptop sandbox and restore procedure.
3. Run and record the no-AI FortID baseline.
4. Add the router, notes search, and shell MCP with tests and logs.
5. Run DEADFACE with explicit AI attribution.
6. Add category tools one at a time and benchmark them on known solved material.
7. Run the InIt full rehearsal and freeze the competition-day bundle.

