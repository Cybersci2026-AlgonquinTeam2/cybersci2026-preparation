# depth-kit: generate comprehensive learning content with local models

A copyable kit. It holds the standard, the topic package spec, a gate that measures what a page contains and runs its commands, a local-model generator, a cross-model critic with a planted-defect control, a skeleton builder for the cold start, and one complete reference topic. No hosted model is needed; none of the tools call the network except your own local model server.

## What is in the folder

| Path | What |
|---|---|
| `standards/PORTABLE-LEARNING-CONTENT-STANDARD.md` | the contract: principles, lanes, grounding, executable labs, gate, status ladder, local-model pipeline, adaptation steps |
| `standards/TOPIC-PACKAGE-SPEC.md` | the nine-file topic package and the minimum counts per move |
| `config/project.json` | **the one file you edit**: the eight replaceable items (domain, rule catalog, sources, lab sandbox, topic keywords, thresholds, forbidden facts, models) |
| `config/rule-catalog.json` | 60 learning, 32 visual and 18 practice-aid rules with stable ids; replace with your own |
| `config/credential-factory.project.json` | a ready profile for the credential content factory (forbidden facts, source captures, moderate thresholds) |
| `tools/gate.py` | the topic gate: structure, rule coverage, honesty, forbidden facts, grounding, copy limits, topic fit, and execution of every lab command (`--fill` writes the real outputs) |
| `tools/gen.py` | generates a candidate topic one unit at a time with retrieval, a structure-only format example, best-of-N and unit checks; writes `provenance.json` |
| `tools/new_topic.py` | creates a headed skeleton with every required element as a slot (cold start, stage 1) |
| `tools/make_pack.py`, `tools/retrieve.py` | build a source pack from local captures (command help, manual pages, text files) and retrieve the passages a unit needs |
| `tools/critic.py`, `tools/plant_defects.py`, `tools/critic_control.py` | cross-model review with quote-validated findings, and the control that proves a Critic can find planted defects |
| `tools/trial.sh`, `tools/summary.py` | generate N candidates, fill, gate, and print the pass table and the checks that fail most |
| `tools/gatelib.py`, `tools/kitconfig.py` | shared helpers: config loading, sandboxed lab execution, copy limits |
| `templates/` | topic spec, backlog, source-capture and forbidden-facts templates |
| `example/` | the reference topic `seed/K-GEN01` (nine files, 16,647 words), a topic spec for a trial topic, and a deterministic sample-data script |
| `tests/selftest.sh` | proves the install works (offline), and optionally one live generation and one critic control |
| `INSTALL-credential-factory.md` | step-by-step for dropping the kit into the credential content factory |
| `MANIFEST.sha256` | hashes of every kit file (for plans that bind tool hashes) |

## Requirements

Python 3.10 or newer (standard library only), bash, GNU coreutils and awk for the example labs, and for the live tools an Ollama-compatible server on a machine you control (`/api/chat`). Nothing else is installed.

## Five-minute check

```bash
bash tests/selftest.sh                                     # offline: gate, pack, retrieval, skeleton, defect planting
bash tests/selftest.sh http://127.0.0.1:11434 qwen3:8b     # adds one live unit and a critic control run
```

## Typical use

```bash
# 1. describe a topic (copy templates/topic-spec.template.json) and put its sources in a captures folder
# 2. skeleton for the cold start (the owner or the drafter fills the slots)
python3 tools/new_topic.py --spec specs/T-001.json --out topics/T-001
# 3. or generate candidates with the local drafter, fill labs by execution, gate, and see the pass table
bash tools/trial.sh specs/T-001.json example/seed/K-GEN01 qwen3:32b http://127.0.0.1:11434 10 runs/T-001
# 4. gate one topic by hand
python3 tools/gate.py topics/T-001 --spec specs/T-001.json --data data/T-001 --pack runs/T-001/pack.txt --seed example/seed/K-GEN01 --fill
# 5. cross-review a passing topic (and prove the Critic first)
python3 tools/critic_control.py topics/T-001 runs/critic --model qwen3:32b --url http://127.0.0.1:11434 --min-recall 0.5
python3 tools/critic.py topics/T-001 --out runs/T-001/findings.json --model qwen3:32b --probe
```

Every tool takes `--config PATH` (or the `DEPTHKIT_CONFIG` environment variable) to use another project file.

## What was tested, and what was not

**Tested** (offline self-test passes on Windows/WSL and on the Linux server): the gate passes the reference topic with 73 lab commands run; it rejects an empty skeleton; the pack builder, retrieval, skeleton builder, defect planting and the generator's helpers work; one live unit was generated with provenance recorded.

**Not proven yet:** (1) the model part of the Critic. Free-form review by an 8-billion-parameter model found 0 of 6 planted defects, so the Critic was rebuilt as narrow checks. Its mechanical checks are verified: they find 5 of the 6 planted defect types (recall 0.83) with 1 false alarm on the clean reference topic (since fixed). The per-sentence model check found none of the planted defects with either qwen3:8b (6 false alarms) or qwen3:32b (2 false alarms; run on CPU/RAM), so model findings are advisory only and never justify a status above `local-reviewed`. The one planted defect no check found was a negated sentence. Re-run `critic_control.py` on your own hardware before trusting any review. (2) One full candidate (qwen3:8b on CPU/RAM, best of 2 per unit, 3.7 hours) was generated and gated: 14,546 words, 22 gate checks failed (under the word target, short on labs, case studies, mastery checks and explained quiz options; three labs wrong; missing schedule, error-to-aid and completion-report sections). The generator builds the structure and the gate measures every shortfall, but a single 8B pass does not reach the standard: expect to repair or regenerate by unit, use a larger model, or both. (3) The credential-factory profile has not been run inside the factory repository; section 3 of `INSTALL-credential-factory.md` lists what to check. (4) The thresholds are the pilot's; tune them on your first three topics.

## Licence and provenance

Written for the owner's own projects. The reference topic was drafted with a hosted model and edited; under the standard it is a format example, not a dependency. Do not store secrets, private evidence or copyrighted full text in `captures/`.
