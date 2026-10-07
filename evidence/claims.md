# Evidence and Claims Ledger

This file separates what is currently recorded from what still needs verification. `observed` means directly checked in the current environment; `source-claim` means supplied or linked material that still needs a current primary-source check; `inference` is reasoning from available information; `plan` is intentional future work.

| ID | Status | Claim | Source or basis | Verification needed |
|---|---|---|---|---|
| C-001 | verified-source | Regional Qualifiers are Saturday Nov 21, 2026 | CyberSci home page: https://cybersci.ca/ ; CTFtime listing: https://ctftime.org/event/3436 | Re-check before event because schedules can change |
| C-002 | verified-source | CyberSci describes a one-day regional event with hacking in the morning and interviews in the afternoon | https://cybersci.ca/students/ | Confirm 2026/27 operational details when published |
| C-003 | verified-source | Regional participants must be full-time students at a Canadian university or college and eligible to work in Canada | https://cybersci.ca/students/ | Confirm whether any 2026/27 eligibility update exists |
| C-004 | verified-source | Team limit is up to 4, or 5 if the team includes a woman or Indigenous member; max 2 teams per school | https://cybersci.ca/students/ | Confirm current event-specific rules |
| C-005 | verified-source | Students cannot register directly; registration goes through the school, instructor, or official student club | https://cybersci.ca/students/ | Contact school representative |
| C-006 | verified-source | CTFtime currently lists the event as Jeopardy, onsite at six Canadian locations, academic teams only | https://ctftime.org/event/3436 | Confirm against organizer rules |
| C-007 | unresolved | AI, MCP tools, and agents are permitted | No current rule located in supplied material | Ask organizers and record response |
| C-008 | unresolved | Venue has usable internet and permits personal laptops | No current rule located in supplied material | Ask organizers |
| C-009 | observed | Target directory existed and was empty when repository creation began | Local filesystem inspection on 2026-10-06 | None |
| C-010 | source-claim | Laptop and Machine B each have six GB VRAM and Ollama/qwen models | User-provided notes | Verify hardware/model inventory locally |
| C-011 | source-claim | Machine B is Windows Server 2022, Docker was not installed, and WSL2 failed | User-provided notes | Re-check before implementation |
| C-012 | plan | Competition bundle must run offline on the laptop | Reliability requirement | Test in disconnected mode |

## Evidence rule

Do not promote a plan or source claim to observed behavior until the relevant check has been performed and recorded. A green schema check or a file inventory proves structure only; it does not prove runtime behavior, network reachability, model quality, or competition compliance.

## Current source findings

As of 2026-10-06, the official CyberSci site confirms the November 21, 2026 date, the regional one-day hacking/interview structure, eligibility, team size, and school-mediated registration. CTFtime independently lists the event as onsite, Jeopardy, and academic-only. The official pages inspected do not answer AI-tool permission, MCP/agent use, venue internet, or personal-laptop policy; those remain unresolved rather than assumed.
