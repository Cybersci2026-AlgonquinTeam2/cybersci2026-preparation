# Installing depth-kit into the credential content factory

Written from the factory's `AGENTS.md`, `COMPREHENSIVE-STUDY-STANDARD.md`, `DEPTH-AND-RIGOR-STANDARD.md`, `CURRICULUM-BLUEPRINT.md` and `ADAPTIVE-MASTERY-METHODS.md`. I did not open the rest of the factory (batch manifests, schemas, the worker), so section 3 lists what you must check on your side.

## 1. Copy

From the folder that contains `depth-kit/`, into the factory repository root (keep the kit's relative layout so `config/` and `tools/` stay siblings):

| From | To in the factory | Note |
|---|---|---|
| `depth-kit/tools/` | `tools/depth/` | the kit finds its config relative to the folder that holds `config/` and `tools/`, so copy `config/` next to it |
| `depth-kit/config/` | `tools/depth/config/` | use `credential-factory.project.json` as `project.json` (copy it over, or pass `--config`) |
| `depth-kit/standards/PORTABLE-LEARNING-CONTENT-STANDARD.md` | `standards/` | it is an umbrella reference; the narrower factory standards win for their own detail |
| `depth-kit/standards/TOPIC-PACKAGE-SPEC.md` | `standards/` | the nine-file package and minimum counts |
| `depth-kit/templates/` | `tools/depth/templates/` | spec, backlog and capture templates |
| `depth-kit/example/` and `tests/` | `tools/depth/example/`, `tools/depth/tests/` | the reference topic and the self-test; the example is a CTF topic, keep it as the format example until the factory has its own |
| `depth-kit/MANIFEST.sha256` | `tools/depth/` | to bind tool hashes in plans |

Then run `bash tools/depth/tests/selftest.sh` from `tools/depth/` to prove the copy works.

## 2. Map the factory onto the kit's eight replaceable items

| Kit item | Factory value |
|---|---|
| Domain and categories | one topic per top-level exam domain, from the exam's job file; level and tier from `DEPTH-AND-RIGOR-STANDARD` section 5 (Deep, Standard, Source-limited). Put the list in `config/factory-topics.csv` |
| Rule catalog | `config/rule-catalog.json` already uses the ids of `ADAPTIVE-MASTERY-METHODS.md` (A = Part A, V = Part B, P = Part E). If the factory edits the catalog, edit this file in the same commit |
| Source pack builder and retriever | captured official sources as `{"type": "file", "path": "...", "label": "<document>, retrieved <date>"}` entries in each topic spec; the retriever hands the drafter only the relevant passages. No blueprint text goes into a pack without an owner decision (AGENTS.md) |
| Sample data, sandbox, allow-list | free local labs only (Linux or WSL, containers, simulators). Paid-cloud or credential labs are written as procedures marked `Not run`. Extend `labs.allow` per credential and set `labs.min_commands` to 0 for concept-only domains |
| Topic keyword lists | `keywords` and `must_not_contain` in each topic spec |
| Thresholds | `credential-factory.project.json` starts lower than the CTF pilot (9,000 / 11,000 / 13,000 words per topic folder); tune on the first three topics |
| Forbidden facts | the profile's `forbidden_facts.patterns` encode the factory rule (prices, passing scores, exam codes, version numbers, years, durations): a match is allowed only when the same text sits in a claims-register row |
| Models | Machine B: `qwen3:8b` at about 23 tokens/s (measured in `batches/B002/batch-plan.md` section 19). The 32 GB server runs `qwen3:32b` at about 25 tokens/s. Provenance records the real model, settings, prompt hash and pack hash for every unit |

## 3. Things to verify inside the factory (not done here)

1. **Path rule:** `Test-Factory.ps1` forbids personal absolute paths in committed files. The kit contains none (checked with a search before packaging); run the factory's check after copying.
2. **Plan binding:** executable plans bind prompts, source packs and templates by SHA-256 and name deterministic generators by id and hash. `gate.py`, `gatelib.py` and the config are deterministic tools; register them as such using `MANIFEST.sha256`. `gen.py` is a local-model job: its prompt is assembled at run time from the spec, the retrieved passages and the format example, so a plan must bind the spec, pack and seed hashes and the kit version, not a single prompt file. Decide whether the worker should call `gen.py` per unit or the factory's own job runner should replace its model call; the kit does not implement leases, outbox paths or the worker's fail-closed checks.
3. **Status words:** the factory ladder is `proposed`, `local-reviewed`, `polished`, `accepted`. The kit adds `cross-reviewed` between `local-reviewed` and `accepted` (an independent local Critic with a passed planted-defect control). Either adopt the new word or map it onto `polished` with the Critic recorded as the pass; the standard, `standards/COMPREHENSIVE-STUDY-STANDARD.md` section 10 and `AGENTS.md` must agree in one commit.
4. **Lane rules:** the factory standard section 11 reserves domain-page prose and claims for a frontier lane. This kit's standard removes that dependency. That is an owner decision for the factory: record it in `AGENTS.md` and `docs/02-MODEL-TIER-POLICY.md`, because the current text says the local lane produced no accepted lesson.
5. **Review independence:** the Critic must be a different model from the drafter and must not read another reviewer's output first; log any exposure as the factory already requires.
6. **Delegated approvals:** the continuous-production pilot lets a model approve plan hashes under an owner delegation and keeps outputs `proposed`. The kit keeps that boundary: nothing it produces is promoted past `local-reviewed` by itself.
7. **Forbidden-fact patterns:** the profile's regexes are broad (any year, any version-like number). Expect false positives on legitimate prose; either narrow them per credential or require the claims-register row, as designed.
8. **Pilot order** (from `DEPTH-AND-RIGOR-STANDARD` section 7): one Deep topic (a Linux Essentials or LPIC-1 domain), one Standard topic (an AZ-104 domain), one concept topic (a Security+ domain). Measure words, figures, labs run, gate results and what the sources could not support, then calibrate thresholds.

## 4. AGENTS.md addition (suggested text)

> **Depth kit.** For study-material generation also read `standards/PORTABLE-LEARNING-CONTENT-STANDARD.md` and `standards/TOPIC-PACKAGE-SPEC.md`. Generate topics with `tools/depth/tools/gen.py`, never let a model write lab output (use `gate.py --fill`), and run `gate.py` before any status change. A gate pass is `local-reviewed` at most. A Critic run is advisory and counts only after `critic_control.py` passes for that Critic model and prompt. Record model, settings, prompt hash and pack hash for every generated unit (`provenance.json`).

## 5. First run in the factory

```bash
cd tools/depth
cp config/credential-factory.project.json config/project.json
bash tests/selftest.sh
python3 tools/new_topic.py --spec specs/LPIC1-103.json --out topics/LPIC1-103            # skeleton
python3 tools/make_pack.py specs/LPIC1-103.json > runs/LPIC1-103/pack.txt                 # from captured sources
bash tools/trial.sh specs/LPIC1-103.json example/seed/K-GEN01 qwen3:8b http://127.0.0.1:11434 10 runs/LPIC1-103
```

Read two candidates yourself before changing any threshold or prompt (Appendix B of the standard: the pass rate alone hid copying, mismatched claims and a likely logic error).
