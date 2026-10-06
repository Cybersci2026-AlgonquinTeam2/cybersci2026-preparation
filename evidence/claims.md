# Evidence and Claims Ledger

This file separates what is currently recorded from what still needs verification. `observed` means directly checked in the current environment; `source-claim` means supplied or linked material that still needs a current primary-source check; `inference` is reasoning from available information; `plan` is intentional future work.

| ID | Status | Claim | Source or basis | Verification needed |
|---|---|---|---|---|
| C-001 | source-claim | Regional Qualifiers are Saturday Nov 21, 2026 | User-provided CTFtime link: https://ctftime.org/event/3436 | Re-open current event page |
| C-002 | source-claim | Qualifier is on-site and jeopardy-style in a realistic IT environment | User-provided plan | Organizer rules/event page |
| C-003 | source-claim | Team limit is up to 4, or 5 with a woman or Indigenous member; max 2 teams per school | https://cybersci.ca/students/ | Current student/team rules |
| C-004 | source-claim | Registration goes through school instructor or computer club | https://cybersci.ca/students/ | Current registration instructions |
| C-005 | unresolved | AI, MCP tools, and agents are permitted | No current rule located in supplied material | Ask organizers and record response |
| C-006 | unresolved | Venue has usable internet and permits personal laptops | No current rule located in supplied material | Ask organizers |
| C-007 | observed | Target directory existed and was empty when repository creation began | Local filesystem inspection on 2026-10-06 | None |
| C-008 | source-claim | Laptop and Machine B each have six GB VRAM and Ollama/qwen models | User-provided notes | Verify hardware/model inventory locally |
| C-009 | source-claim | Machine B is Windows Server 2022, Docker was not installed, and WSL2 failed | User-provided notes | Re-check before implementation |
| C-010 | plan | Competition bundle must run offline on the laptop | Reliability requirement | Test in disconnected mode |

## Evidence rule

Do not promote a plan or source claim to observed behavior until the relevant check has been performed and recorded. A green schema check or a file inventory proves structure only; it does not prove runtime behavior, network reachability, model quality, or competition compliance.

