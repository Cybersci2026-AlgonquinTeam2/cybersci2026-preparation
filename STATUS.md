# Status

## Current state

Repository scaffolded on 2026-10-06. No infrastructure has been claimed as built or runtime-tested.

## Next actions

- [x] Verify qualifier date, event shape, eligibility, team size, registration path, and current CTFtime classification with primary/current sources.
- [ ] Verify AI policy, internet access, and laptop policy with the organizers.
- [ ] Register through the school instructor or computer club if team participation is confirmed.
- [ ] Create a FortID no-AI run record before the event.
- [ ] Decide laptop OS/sandbox implementation and snapshot/restore procedure.
- [ ] Define the local router interface and fallback telemetry.
- [ ] Define the notes/RAG corpus boundary and citation format.
- [ ] Define shell MCP allowlist and threat model before implementation.

## Decisions

- Machine B is training-time capacity, not a competition dependency.
- Laptop-local execution is the default; remote execution is a fallback.
- Remote MCP servers must bind to Tailscale only and require authentication.
- Agents must not mount credential-factory directories.
- Human approval is required before traffic touches scoring infrastructure.

## Open risks

- Event dates and rules may change.
- Machine B reachability is intermittent.
- Six GB VRAM constrains model size and concurrency.
- A cross-event score comparison is confounded by event difficulty and team composition.
