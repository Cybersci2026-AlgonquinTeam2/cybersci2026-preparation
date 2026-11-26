# Portable standard: generating comprehensive learning content with measured quality

Status: proposed, 2026-11-26. Version 1.0. A project-independent standard for any repository that generates study material (certification prep, CTF training, technical courses) with a mix of frontier models, local models and deterministic tools. It is distilled from two efforts: the credential content factory (grounding, lanes, status ladder, adaptive-mastery rules) and the cybersci-prep depth pilot (the five-part topic package, the executable gate, the local-model trial). Where a project already has a narrower standard, the narrower one wins for its own detail; this document supplies the contract and the mechanisms.

## 1. What this standard is for

Use it when you want learning content that is (1) comprehensive, meaning it applies many learning methods, not one; (2) measurable, meaning a program can say what it contains; (3) honest, meaning every claim and every "tested" has a record behind it; (4) cheap to scale, meaning most of the work can run on local models once a few reference pages exist.

It does not make content correct or well taught. It makes content inspectable, and it refuses to call anything reviewed that was only checked by a program.

## 2. Principles (non-negotiable)

1. **Grounded.** Every factual claim traces to a captured source (a quote of 8 or more words) or is marked `VERIFY`. A teaching scaffold (analogy, mental model, prompt) may be original and holds no source facts. A page never fills a gap with invention; it lists the gap.
2. **Executed, where it can be.** If a page says a command, query, script or calculation produces a result, a program runs it and records the real output. The page never carries a result a model wrote from memory.
3. **Visual first, active always.** Each idea has a picture before or beside the words. Every page makes the learner predict, retrieve, practise, break something, transfer and teach back.
4. **Levels without lowering the ceiling.** Intuition, foundations, mechanics, application, systems, expert reasoning. Scaffolding goes up for novices; the destination stays expert.
5. **Honest status.** A status word is a record, not a mood: `proposed` (generated), `local-reviewed` (deterministic gates passed), `polished` (a recorded frontier pass), `accepted` (an owner decision). A gate is never a review.
6. **Independence is the goal.** Each topic ends with transfer, design and teach-back; the learner needs the material less over time.
7. **Safe by default.** Content that is dual-use is framed for labs the learner owns or for authorised events, and where a platform's safeguards block a draft, the project does not retry the same content reworded: it changes the framing or the scope (see section 12).

## 3. Roles and generation lanes

| Lane | May produce | May not |
|---|---|---|
| Frontier model | reference (seed) pages, hard prose, claims with quotes, figures, reviews | anything without provenance recorded (model, setting, client, date, input hashes) |
| Local model, with or without a LoRA | first drafts of pages and derived blocks (cards, drills, quiz distractors and rationales, cheat-sheet tables, lab scaffolding, glossary), under the gate | new source facts, quotes, status promotion |
| Deterministic tools | filling lab outputs, validation, packaging, exports | free-text teaching |
| Human or independent reviewer | review findings, owner decisions, running labs not yet run | none |

Independence rule: a reviewer must be a different model or a person who did not author the page and did not read another reviewer's output first.

## 4. The topic package (the unit of content)

A topic is a folder, not a page. The core is five parts; extension parts add depth without bloating the core.

| File | Moves | Holds |
|---|---|---|
| `1-learn` | orient, prime, intuition, foundations, mechanics, worked examples, compare and decide | the explanation |
| `2-do` | do it, repair, break it | labs from guided to adversarial, command explanations, mistakes, failure cases, break-fix labs |
| `3-retrieve` | retrieve and discriminate | drills, trace drills, spot-the-bug items, quiz, cards, interleaved set, spaced schedule, error-to-aid template |
| `4-transfer` | zoom out, transfer and design, teach back | systems view, four transfer levels, critique, reconstruction, design kata, capstone, teach-back, mastery ladder |
| `5-reference` | close | cheat sheets, glossary, claims register, gap list, rule-coverage matrix, completion report |
| `6` to `9` (extensions) | language/tool primers, case studies and extra labs, a practice bank, extended reference | as needed, counted by the same gate |

Headings in the core parts are `## N. Title` with N the move number so move order is checkable across the folder. Part 1 carries front matter: `id`, `title`, `category`, `level`, `status`, `lab_run`, `lane`.

## 5. Rule tagging: making coverage measurable

Keep a catalog of the learning rules you apply (this project uses 60 learning rules `A`, 32 visual rules `V`, 18 practice-aid rules `P`; replace with your own catalog). Every element that implements a rule carries its tag in the text, for example `{A13}` (prediction), `{V9}` (sequence figure), `{P7}` (guided lab), and every figure carries a kind tag, `{fig:flow}`. The gate counts distinct tags and figure kinds. Tags are visible to the learner as labels of the method in use.

Rules that describe how an assistant behaves, not what a page contains, are excluded from the target (this project excluded 7 of 60). A coverage matrix in the reference part lists where each rule family is applied, and the gate checks the matrix exists.

Limit to remember: tags can be added without the element being good. They prove presence, not quality.

## 6. Grounding and the claims register

- Capture sources into a source pack before generating: official documentation, the tools' own `--help` and manual text, standards. Record version and retrieval date. Where the source is a program, capture its output from the version used.
- Every factual claim goes in a register with exactly five cells: `Id | Claim | Quote or VERIFY | Status | Note`. Status is one of **Read** (the cited text was read), **Listing read** (record or abstract only), **Run** (the command or lab was executed and recorded), **Not run**. A `Read` claim carries a quote of 8 or more consecutive words that appears in the source pack; otherwise the cell is `VERIFY`.
- Learner text must not repeat 8 or more consecutive source words outside the register (copy limit).
- Forbidden facts (per project): prices, passing scores, exam codes, version numbers and dates are not stated unless a source register records them.
- Tag advice (requirement, best practice, rule of thumb, preference, context-dependent) and certainty (fact, observed, inference, assumption, estimate) where it matters.

Known hole: a gate can check that a quote exists in the pack, not that it supports the claim. Keep a human or independent-model spot check on relevance.

## 7. Executable labs: execute and fill

For content with runnable commands, adopt the pattern proven in the pilot:

1. The author (human or model) writes only the command lines in a ```lab block, each starting `$ `.
2. A harness runs each command in a throw-away sandbox with fixed sample data, a fixed locale, a time limit, no network and an allow-list of programs, then writes the real output under the command.
3. The gate re-runs the blocks and fails the page if any command errors, returns nothing or does not match.
4. The page states "Run" only for what was run, with environment and date in front matter. Anything needing writes, network or accounts is written as a procedure marked "not run".

This removes invented outputs from model-written pages. It does not catch a command that runs and answers the wrong question (a loose pattern that over-counts, for example). Design at least one lab per topic whose data exposes that failure, and verify claims about outputs against the filled results.

For domains without runnable commands (concepts, policy), use the equivalent: an executable check where one exists (a calculation, a configuration linter, a simulator) and `Not run` where none does.

## 8. The gate

A deterministic program, versioned with the content, run on every candidate. Its checks, in order of importance:

1. **Structure:** all parts exist, front matter present, move headings 1 to 15 once each, status `proposed`.
2. **Size:** minimum words by level, counted outside code.
3. **Coverage:** distinct rule tags and figure kinds above the minimums; figure count; every counted element (drills, quiz questions with every option explained, cards by type and difficulty, hint ladders with four tiers, labs, failure cases, break-fix labs, misconceptions, mistake rows with an error class, case studies, katas, glossary, claims).
4. **Honesty:** banned skip-words (`simply`, `just`, `obviously`, `trivially`, `clearly`, `of course`), no review or acceptance claims in status fields, gap list and lab run status present.
5. **Grounding:** claims register shape and quote checks; copy limit against the source pack.
6. **Execution:** every lab command runs and matches.
7. **Originality:** a copy limit against the seed page (at most 15 percent of 8-word runs), so a model shown an example cannot pass by repeating it.

A gate is evidence of structure. It is reported as `GATE PASSED` or the list of failed checks and never as "reviewed". Raise thresholds in the spec and the gate together; record the version in each result.

## 9. Status ladder and record-keeping

| Status | Meaning | Required |
|---|---|---|
| `proposed` | generated, not gated | none |
| `local-reviewed` | deterministic gates passed | gate results saved with hashes of inputs |
| `polished` | a recorded frontier pass | model, setting, client, date, input hashes, findings |
| `accepted` | an owner decision | independent review of the unit end to end |

Record for every generated page: the lane, the model and its settings, the prompt and source-pack hashes, the gate version and result. Promotion needs the record; deleting the record revokes it.

## 10. Local-model pipeline

**Facts to measure first** on the hardware you will use: decode speed for the candidate models at the context you need, memory use (a larger model may fill the GPU and block other work), model load time.

**Generation.** Generate one move (section) at a time, not a whole topic: the context is bounded and failures localise. Give the model: the rules for that move, the topic spec, the source pack, the seed's section for that move as a **format** example. Tell it not to copy words. Disable hidden reasoning output if it pollutes the text. Fill lab outputs by execution, never by the model.

**Trial before scale.** Run a fixed small trial (10 candidates for one topic) and report: pass rate under the full gate, the checks that fail most, and a human reading of at least two passing candidates. The pilot's lesson: a weak gate gave 60 percent; adding the seed-copy and claims-table checks gave 0 percent; the model copied 32 to 44 percent of its words from the seed, reused claims that did not match its topic, and wrote a plausible lab with a likely logic error. Treat a first pass rate as an upper bound until the gate has been hardened against what you saw when you read the output.

**Reduce copying by design:** show the seed as structure with placeholders, vary the sampling, require topic-specific claims, and keep the seed-copy limit.

**Bootstrapping and LoRA.** A LoRA teaches format and voice; it does not add facts and does not stop invention. Train only on reviewed material, record the adapter and its training set, and evaluate on held-out topics with the same gate. Self-distillation (a local model's own filtered output as training data) is acceptable only with a strong filter and a human pass on the survivors; stop after 2 to 3 rounds because each round amplifies whatever the filter lets through. A seed set of 40 to 60 reviewed pages is the usual threshold before training is worth running; with a few seeds, use few-shot prompting instead.

**Larger model, same prompt.** Compare models on identical prompts and the same gate before changing the prompt, so differences come from the model.

## 11. Measures

Track per project and per topic: topics with a complete package, words, rule-tag and figure coverage, lab commands run, claim support rate (supported over total), thin-source gaps, first-pass gate failures by check, candidate pass rate by model, reviewer findings by severity, learner evidence (mastery level per topic). A count of pages is never presented as coverage of the subject.

## 12. Safety, policy and content scope

- Dual-use topics (security, chemistry, biology) are written for authorised labs, owned systems or sanctioned competitions, and say so. Offensive step-by-step material is not required for learning and may be blocked by a platform's safeguards; when a draft is stopped, do not rewrite and resend the same content. Change the framing to defence, detection and fixes, point the practice to existing labs, or ask the account owner about the platform's verification programmes for vetted professionals.
- Rules of events (for example competitions that ban AI tools) bind how the learner uses the material at the event, not how it is written; record event rules in the project's calendar and tag them (banned, allowed, split, check).
- Do not store secrets, private evidence or copyrighted full text. Credentials, accounts and spending are the owner's actions.
- Local servers: record who else uses them, keep work in your own account, do not change shared services without the owner.

## 13. Adapting this standard to a new project

Replace, do not rewrite:

| Item | Replace with |
|---|---|
| Domain and categories | your backlog of topics with levels, hours and which goals need each |
| Rule catalog | your learning rules, visual rules and practice aids with stable ids |
| Source pack builder | the right capture for your sources (docs, man pages, standards, datasets) |
| Sample data and sandbox | data the labs run on, an allow-list of programs |
| Thresholds | minimums by level, tuned on the first three topics |
| Forbidden facts | the facts your domain must never state without a register |
| Move names | keep the 15 moves unless your domain argues otherwise |

Adoption steps: (1) write your catalog and spec; (2) write one reference topic by hand, with the labs executed; (3) build or copy the gate and make the reference pass; (4) run a 10-candidate local trial and read two results; (5) harden the gate against what you saw; (6) scale by category with the trial numbers in hand; (7) independent review of one finished category before more are accepted.

## 14. Reference implementation

In this repository (`depth/`): `SPEC-v2.md` (the topic package and minimums), `tools/gate.py` and `tools/gate_v2.py` (the gates, with sandboxed lab execution and fill), `tools/gen.py` (one-move-at-a-time generation through a local model server), `tools/make_pack.py` (source pack from tool help), `tools/trial.sh` and `tools/summary.py` (trial and pass-rate report), `data/make_sample.py` (deterministic sample data), `seed2/K-GEN01/` (a nine-file reference topic: 16,647 words, 53 learning-rule tags, 32 visual, 18 practice, 22 figures, 73 lab commands run). The v1 trial results (10 candidates, 8B model) that motivated the originality and claims checks are described in section 10.

## 15. Change control

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
```

## Appendix B: lessons from the pilot (so they are not relearned)

1. A first gate that checked only structure passed 6 of 10 weak pages; every one failed once originality and claims-shape checks existed.
2. Showing a model a full seed page makes it copy; show structure and require topic-specific content.
3. Quotes that exist in the source pack can still fail to support the claim beside them.
4. A runnable lab can still answer the wrong question; design the data so the common mistake produces a visibly different number.
5. Shell scripts edited on Windows may gain CRLF line endings and fail on the server; normalise line endings for anything a Linux host runs.
6. Hand-edited string replacement scripts with escaped newlines corrupt files; prefer whole-file writes or editor tools for multi-line edits.
7. A server on a private route can disappear (reboot, VPN); keep a second route and make background jobs restartable and logged.
8. A platform safeguard can stop a draft mid-write: keep partial work out of commits, and keep the file list honest about what was and was not written.
