# Portable standard: generating comprehensive learning content entirely with local models

Status: proposed, 2026-11-26. Version 2.0 (v1.0 assumed a frontier model for reference pages; v2.0 removes that dependency). A project-independent standard for any repository that generates study material (certification prep, CTF training, technical courses) using only models that run on hardware you control, plus deterministic tools and a human owner. It is distilled from two efforts: the credential content factory (grounding, lanes, status ladder, adaptive-mastery rules) and the cybersci-prep depth pilot (the multi-part topic package, the executable gate, the local-model trial). Where a project has a narrower standard, the narrower one wins for its own detail; this document supplies the contract and the mechanisms.

**Frontier models are optional, never required.** A project may use one for any lane in section 3; if it does, it records provenance exactly as for a local model and the project's gates apply unchanged. Nothing in this standard depends on one.

## 1. What this standard is for

Use it when you want learning content that is (1) comprehensive: many learning methods applied, not one; (2) measurable: a program can say what a page contains and that its commands ran; (3) honest: every claim and every "tested" has a record behind it; (4) producible offline on your own machines.

It does not make content correct or well taught. It makes content inspectable, and it never calls anything reviewed that was only checked by a program.

**The local-only trade, stated plainly.** Local models are smaller and make more factual and reasoning mistakes than the strongest hosted models. This standard compensates with five mechanisms rather than hoping the model is right: source packs the model must quote (section 6), execution of everything runnable (section 7), a hardened gate (section 8), cross-model review (section 9) and a human owner who reads what gets promoted. If a project cannot supply those, its content stays `proposed`.

## 2. Principles (non-negotiable)

1. **Grounded.** Every factual claim traces to a captured source (a quote of 8 or more words) or is marked `VERIFY`. A teaching scaffold (analogy, mental model, prompt) may be original and holds no source facts. A page never fills a gap with invention; it lists the gap.
2. **Executed, where it can be.** If a page says a command, query, script or calculation produces a result, a program runs it and records the real output. The page never carries a result a model wrote from memory.
3. **Visual first, active always.** Each idea has a picture before or beside the words. Every page makes the learner predict, retrieve, practise, break something, transfer and teach back.
4. **Levels without lowering the ceiling.** Intuition, foundations, mechanics, application, systems, expert reasoning.
5. **Honest status.** A status word is a record: `proposed`, `local-reviewed`, `cross-reviewed`, `accepted` (section 10). A gate is never a review, and a model reviewing a model is not a human decision.
6. **Independence is the goal.** Each topic ends with transfer, design and teach-back.
7. **Safe by default.** Dual-use content is framed for labs the learner owns or for authorised events (section 13).
8. **No hidden dependency.** The workflow must run with the network off once the models and source packs are on disk.

## 3. Roles and lanes (local models only)

Roles are jobs, not model names. One model can hold several roles if the independence rules in section 9 hold.

| Role | Job | Typical local choice | May not |
|---|---|---|---|
| Drafter | writes candidate pages one move at a time from the rules, the topic spec, the source pack and a format example | the largest model that fits your hardware (the pilot's 32-billion-parameter model on a 32 GB GPU) for seeds and hard moves; a mid-size model for derived blocks | invent source facts, write command output, set status |
| Worker | high-volume derived blocks (cards, drills, quiz explanations, cheat sheets, glossary, lab scaffolding) | a small or LoRA-tuned model | quote, add facts, promote |
| Critic | reads a candidate against the rules and the source pack and returns findings that quote the text | a different model family from the drafter, or a different size | change the page, mark it reviewed |
| Verifier (deterministic) | runs the gate, fills lab outputs, checks quotes, measures coverage and copying | no model | free-text teaching |
| Owner | writes or edits the first seeds, reads promoted pages, makes accept decisions | you, or a person you name | none |

Record provenance for every model call that shaped a page: model name and version, quantisation, sampling settings, random seed, the prompt hash, the source-pack hash and the date.

## 4. The topic package (the unit of content)

A topic is a folder, not a page. The core is five parts; extension parts add depth without bloating the core.

| File | Moves | Holds |
|---|---|---|
| `1-learn` | orient, prime, intuition, foundations, mechanics, worked examples, compare and decide | the explanation |
| `2-do` | do it, repair, break it | labs from guided to adversarial, command explanations, mistakes, failure cases, break-fix labs |
| `3-retrieve` | retrieve and discriminate | drills, trace drills, spot-the-bug items, quiz, cards, interleaved set, spaced schedule, error-to-aid template |
| `4-transfer` | zoom out, transfer and design, teach back | systems view, four transfer levels, critique, reconstruction, design kata, capstone, teach-back, mastery ladder |
| `5-reference` | close | cheat sheets, glossary, claims register, gap list, rule-coverage matrix, completion report |
| `6` to `9` | extensions: tool/language primers, case studies and extra labs, a practice bank, extended reference | as needed, counted by the same gate |

Headings in the core parts are `## N. Title`, N the move number, so move order is checkable across the folder. Part 1 carries front matter: `id`, `title`, `category`, `level`, `status`, `lab_run`, `lane`.

## 5. Rule tagging: making coverage measurable

Keep a catalog of the learning rules you apply (this project uses 60 learning rules `A`, 32 visual rules `V` and 18 practice-aid rules `P`; replace with your own). Every element that implements a rule carries its tag, for example `{A13}` (prediction), `{V9}` (sequence figure), `{P7}` (guided lab), and every figure carries a kind tag, `{fig:flow}`. The gate counts distinct tags and figure kinds. Rules that describe how an assistant behaves, not what a page contains, are excluded from the target (7 of 60 here). A coverage matrix in the reference part lists where each rule family is applied.

Limit: tags prove presence, not quality, and a model can add them without the element being good.

## 6. Grounding and the claims register (the main defence against local-model errors)

- **Capture sources first** into a source pack: official documentation, the tools' own `--help` and manual text, standards, a textbook you own. Record version and retrieval date. Where the source is a program, capture its output from the version used.
- **Retrieval for the drafter.** The prompt for each move contains only the source passages relevant to that move (selected by keyword or by a small embedding index), not the whole pack, so the context stays small and the model has less room to drift.
- **Claims register.** Every factual claim sits in a register with exactly five cells: `Id | Claim | Quote or VERIFY | Status | Note`. Status is **Read** (the cited text was read), **Listing read** (record or abstract only), **Run** (the command or lab was executed), **Not run**. A `Read` claim carries a quote of 8 or more consecutive words found verbatim in the pack; otherwise `VERIFY`.
- **Relevance check for quotes.** A quote existing in the pack does not prove it supports the claim. Add a check: the Critic is asked, for each `Read` row, "does this quote state this claim? yes or no, and why", and the answers are stored. A `no` blocks promotion.
- **Copy limit.** Learner text must not repeat 8 or more consecutive source words outside the register.
- **Forbidden facts** (per project): prices, passing scores, exam codes, version numbers and dates are not stated unless a source register records them.
- Label advice (requirement, best practice, rule of thumb, preference, context-dependent) and certainty (fact, observed, inference, assumption, estimate).

## 7. Executable labs: execute and fill

For content with runnable commands:

1. The model writes only the command lines in a ```lab block, each starting `$ `.
2. A harness runs each command in a throw-away sandbox with fixed sample data, a fixed locale, a time limit, no network and an allow-list of programs, then writes the real output under the command.
3. The gate re-runs the blocks and fails the page if any command errors, returns nothing or does not match.
4. The page states "Run" only for what was run, with environment and date in front matter. Anything needing writes, network or accounts is a procedure marked "not run".

This removes invented outputs and is the strongest check a local model's output can have. It does not catch a command that runs and answers the wrong question (a loose pattern that over-counts). Design at least one lab per topic whose data exposes the common mistake with a visibly different number, and check prose claims about outputs against the filled results.

For domains without runnable commands, use the equivalent executable check (a calculation, a configuration linter, a simulator, a unit test) and `Not run` where none exists.

## 8. The gate

A deterministic program, versioned with the content, run on every candidate:

1. **Structure:** parts exist, front matter present, move headings 1 to 15 once each, status `proposed`.
2. **Size:** minimum words by level, counted outside code.
3. **Coverage:** distinct rule tags and figure kinds above the minimums; counts of drills, quiz questions with every option explained, cards by type and difficulty, four-tier hint ladders, labs, failure cases, break-fix labs, misconceptions, mistake rows with an error class, case studies, katas, glossary entries and claims.
4. **Honesty:** banned skip-words (`simply`, `just`, `obviously`, `trivially`, `clearly`, `of course`); no review or acceptance claims in status fields; gap list and lab run status present.
5. **Grounding:** claims-table shape, quote presence, copy limit against the pack.
6. **Execution:** every lab command runs and matches.
7. **Originality:** at most 15 percent of 8-word runs repeat the format example (the seed), so a model shown an example cannot pass by repeating it.
8. **Topic-fit:** the page's terms come from its own spec (a keyword list per topic); a candidate whose cheat sheet or claims describe a different topic fails.

A gate result is `GATE PASSED` or the failed checks, never "reviewed". Raise thresholds in the spec and the gate together and record the gate version in every result.

## 9. Cross-model review (replacing the frontier review pass)

A page may reach `cross-reviewed` only after a review that is independent in a defined sense:

- **Different model:** the Critic is a different model family or a different size from the Drafter, with its own prompt, and does not see the Drafter's prompts or sampling record.
- **Quote-or-it-did-not-happen:** every finding must quote the page text it concerns, state the rule or source it conflicts with, and give a severity. Findings without a quote are discarded.
- **Planted-defect control:** each Critic configuration is tested on a page with known planted defects (a wrong command description, a claim contradicting its quote, a missing four-tier hint). A Critic that misses most is not used for promotion. Re-run the control whenever the Critic model or prompt changes.
- **Self-consistency probe:** a second sampling of the same Critic on the same page; findings that do not recur are marked low confidence.
- **No reading of another reviewer's output** before finishing, and any exposure is recorded.

A cross-review is advisory. It never changes the page, never promotes it alone, and does not replace the owner.

## 10. Status ladder and record-keeping

| Status | Meaning | Required |
|---|---|---|
| `proposed` | generated, not gated | none |
| `local-reviewed` | deterministic gates passed | gate result saved with input hashes and gate version |
| `cross-reviewed` | an independent local Critic reviewed it | critic model and prompt hash, planted-defect control result, findings with quotes, each finding resolved or declined with a reason |
| `accepted` | an owner decision | the owner read the page (or an agreed sample of the category) and signed the decision |

Promotion needs the record; deleting the record revokes the status. A hosted-model review, if a project chooses to use one, is recorded as `cross-reviewed` with its provenance and gets no extra standing.

## 11. Local-model pipeline

**Measure first** on your hardware: decode speed for each candidate model at the context you need, memory use (a large model may fill the GPU and block other work), load time. The pilot's measurements are an example, not a promise: a 32-billion-parameter model at 4-bit decoded at about 25 tokens per second and filled 28 of 32 GB; an 8-billion model decoded at about 91 tokens per second in 6.4 GB. Tokens per topic are roughly words times 1.35 times 1.3 for tables and figures; divide by your speed for a time estimate and multiply by the retries you observe.

**Generation.** One move (section) at a time. Give the Drafter the rules for that move, the topic spec, the relevant source passages and a format example. Tell it not to copy words. Fill lab outputs by execution. Best-of-N at the move level (generate N candidates for a move, keep the one that passes the section-level checks) is cheaper than regenerating a whole topic.

**Cold start without a frontier model.** The first seed topic cannot be copied from another page, so it is built in stages:

1. **Skeleton by the owner or a small script:** the topic spec, a headed skeleton with each move's required elements as empty slots (the spec lists the minimum counts), the sample data and the source pack.
2. **Drafter fills slots:** the largest local model fills one slot at a time, with the source passages for that slot, using best-of-N and the move-level gate; labs are filled by execution.
3. **Owner pass:** the owner reads and edits the whole topic. This is the seed's quality gate and the one place human time is non-negotiable. Budget it: reading a 16,000-word topic is hours, not minutes.
4. **Critic pass and fixes:** a different local model reviews under section 9; findings are fixed or declined.
5. **Repeat for 3 to 5 seeds in different categories** so the format example is not a single topic's phrasing.

A seed written by any model, local or hosted, enters the project the same way: it passes the gate and is read by the owner. An existing hosted-model seed may be used as the stage-1 format example if one exists; its provenance is recorded and the pipeline never depends on it.

**Trial before scale.** Run a fixed small trial (10 candidates for one topic) and report: pass rate under the full gate, the checks that fail most, and a human reading of at least two passing candidates. In the pilot a structure-only gate passed 60 percent and a hardened gate (originality and claims-shape checks) passed 0 percent; the model copied 32 to 44 percent of its words from the example, reused claims that did not fit the topic and wrote a plausible lab with a likely logic error. Treat any first pass rate as an upper bound until the gate has been hardened against what you saw when you read the output.

**Reduce copying by design:** show the format example as structure with placeholders, vary sampling, require topic-specific claims, keep the originality limit.

**Bootstrapping and LoRA.** A LoRA teaches format and voice; it does not add facts or prevent invention. Train only on pages that reached at least `local-reviewed` and were read by the owner; record the adapter and its training set; evaluate on held-out topics with the same gate. Self-distillation (a local model's own filtered output as training data) is acceptable only with the gate and the owner's reading of the survivors; stop after 2 to 3 rounds because each round amplifies whatever the filter lets through. About 40 to 60 owner-read pages is the usual point where training pays; before that, few-shot prompting with 3 to 5 seeds is the method.

**Compare models fairly:** identical prompts and gate first; change the prompt only after.

## 12. Measures

Track per project and topic: topics with a complete package, words, rule-tag and figure coverage, lab commands run, claim support rate (supported over total, with Critic relevance answers), thin-source gaps, first-pass gate failures by check, candidate pass rate by model and by move, Critic findings by severity and by whether the owner upheld them, owner hours per accepted topic, learner evidence (mastery level per topic). A count of pages is never presented as coverage of the subject.

## 13. Safety, policy and scope

- Dual-use topics (security, chemistry, biology) are written for authorised labs, owned systems or sanctioned competitions, and say so. Offensive step-by-step material is not required to learn the defensive and analytical skills, and hosted platforms may block it. Local models have no such filter, so the project owns the policy: write dual-use material as lab exercises on systems the learner owns, state the authorisation boundary on the page, prefer detection and fix sections alongside every attack technique, and keep the practice on deliberately vulnerable local labs. Do not generate content intended for use against systems you are not authorised to test.
- Rules of events (for example competitions that ban AI tools) bind how the learner uses material at the event, not how it is written; record event rules in the project calendar and tag them (banned, allowed, split, check).
- Do not store secrets, private evidence or copyrighted full text. Credentials, accounts and spending are the owner's actions.
- Shared servers: record who else uses them, keep work in your own account, do not change shared services without the owner, and keep a second route and restartable, logged background jobs.

## 14. Adapting this standard to a new project

Replace, do not rewrite:

| Item | Replace with |
|---|---|
| Domain and categories | your backlog of topics with levels, hours and which goals need each |
| Rule catalog | your learning rules, visual rules and practice aids with stable ids |
| Source pack builder and retriever | the right capture for your sources (docs, manual pages, standards, datasets, books you own) |
| Sample data, sandbox, allow-list | what your labs run on and which programs they may use |
| Topic keyword lists | the terms each topic must contain (for the topic-fit check) |
| Thresholds | minimums by level, tuned on the first three topics |
| Forbidden facts | the facts your domain must never state without a register |
| Models | the models your hardware runs; record them in provenance |

Adoption steps: (1) write your catalog and spec; (2) build the skeleton, sample data and source pack for one topic; (3) fill it with the Drafter, execute the labs, read and edit it yourself; (4) build or copy the gate and make that topic pass; (5) run a 10-candidate trial and read two results; (6) harden the gate against what you saw; (7) repeat for 3 to 5 seeds; (8) scale by category with the trial numbers in hand; (9) cross-review one finished category and read a sample before more is accepted.

## 15. Reference implementation

In the cybersci-prep repository, `depth/`: `SPEC-v2.md` (the topic package and minimums), `tools/gate.py` and `tools/gate_v2.py` (the gates, with sandboxed lab execution and fill), `tools/gen.py` (one-move-at-a-time generation through a local model server), `tools/make_pack.py` (source pack from tool help), `tools/trial.sh` and `tools/summary.py` (trial and pass-rate report), `data/make_sample.py` (deterministic sample data), `seed2/K-GEN01/` (a nine-file reference topic: 16,647 words, 53 learning-rule tags, 32 visual, 18 practice, 22 figures, 73 lab commands run). The reference topic was written with a hosted model; under this standard it is a format example, not a dependency. **Not yet built here:** the move-level best-of-N generator, the topic-fit check, the Critic harness with planted-defect control, and the retrieval step; each is specified above and each is required before a project claims `cross-reviewed` content.

## 16. Change control

Version this document with the content. A change to a gate, a threshold or a status rule updates the standard in the same commit and says why. A conflict between this document and a narrower project standard is a defect to fix in one of them, not a rule to work around.

## Appendix A: formats the gate relies on

```
Front matter (part 1):  id, title, category, level, status: proposed, lab_run, lane
Claims row:             | C1 | claim | "8+ word quote" or VERIFY | Read | Listing read | Run | Not run | note |
Flashcard:              - [concept|cloze|scenario|contrast|trace][easy|medium|trap] Front: ... Back: ...
Drill / trace / bug:    1. **Drill** ...   1. **Trace** ...   1. **Spot the bug** ...
Quiz:                   **Q1.** text, then   - (A) option — why it is right or wrong (20+ characters)
Hint ladder:            - Hint 1: nudge   - Hint 2: direction   - Hint 3: partial   - Hint 4: full answer
Lab block:              ```lab  then lines  $ command   (output is filled by the harness)
Rule tag / figure kind: {A13} {V9} {P7}   {fig:flow}
Critic finding:         page quote | rule or source it conflicts with | severity | resolved / declined + reason
```

## Appendix B: lessons from the pilot (so they are not relearned)

1. A first gate that checked only structure passed 6 of 10 weak pages; every one failed once originality and claims-shape checks existed.
2. Showing a model a full example page makes it copy; show structure and require topic-specific content.
3. Quotes that exist in the source pack can still fail to support the claim beside them.
4. A runnable lab can still answer the wrong question; design the data so the common mistake produces a visibly different number.
5. Shell scripts edited on Windows may gain CRLF line endings and fail on a Linux host; normalise them.
6. Hand-written string-replacement scripts with escaped newlines corrupt files; prefer whole-file writes or editor tools for multi-line edits.
7. A server on a private route can disappear (reboot, VPN); keep a second route and make background jobs restartable and logged.
8. A hosted platform's safeguard can stop a draft mid-write; keep partial work out of commits. Local-only workflows remove that dependency but not the policy duty in section 13.
9. Reading the output is part of the method: the pass rate alone hid copying, mismatched claims and a likely logic error.
