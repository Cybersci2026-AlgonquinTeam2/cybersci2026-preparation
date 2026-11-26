# Depth page spec v2: comprehensive, rule-tagged, five parts

Replaces the single-page shape of v1. Reason: v1 applied each learning rule once, in one place. v2 applies the catalog in `standards/ADAPTIVE-MASTERY-METHODS.md` (60 learning rules `A`, 32 visual rules `V`, 18 practice-aid rules `P`) and the 15-move cycle in `standards/CURRICULUM-BLUEPRINT.md` at the depth `standards/DEPTH-AND-RIGOR-STANDARD.md` describes, and makes the coverage measurable. A topic is a folder of five parts. The gate is `depth/tools/gate_v2.py`.

## 1. The five parts (one folder per topic)

| File | Moves | Holds |
|---|---|---|
| `1-learn.md` | 1 to 7 | orient, prime, intuition, foundations, mechanics, three worked examples, compare and decide |
| `2-do.md` | 8 to 10 | four labs (guided, prompted, unassisted, adversarial), command explanations, mistakes, failure cases, two break-fix labs |
| `3-retrieve.md` | 12 | 10 micro-drills, 5 trace drills, 3 spot-the-bug items, a 10-question quiz, 30 flashcards, an interleaved set, the spaced-review schedule, the error-to-aid template |
| `4-transfer.md` | 11, 13, 14 | zoom out (systems, trust, performance, security, expert view), four transfer levels, critique, reconstruction, design kata, capstone, teach-back, the 11-level mastery ladder with a task per level |
| `5-reference.md` | 15 | two cheat sheets, glossary, claims register, gap list, rule-coverage matrix, completion report, next steps |

Headings are `## N. Title` with N the move number, so the move order is checked across the folder. Part 1 carries the front matter (`id`, `title`, `category`, `level`, `status: proposed`, `lab_run`, `lane`).

## 2. Rule tags (how coverage is measured)

Every element that implements a rule carries its tag in curly braces: `{A13}` learning rule 13 (prediction), `{V9}` visual rule 9 (sequence diagram), `{P7}` practice aid 7 (guided lab). Figures also carry a kind tag, `{fig:flow}`. The gate counts distinct tags; the coverage matrix in part 5 lists where each rule is applied, and the gate checks that every tag listed there appears in the parts. Tags are visible to the learner as small labels: they say which learning method an element is.

Minimum coverage per topic: **40 distinct A tags, 24 V tags, 15 P tags, 10 figures of at least 7 different kinds** (`flow`, `sequence`, `tree`, `map`, `layers`, `trace`, `diff`, `states`, `layout`, `zones`, `matrix`, `blackbox`, `failure`).

## 3. What each move must contain (with the rules it carries)

| Move | Required elements (minimum counts) | Rules |
|---|---|---|
| 1 Orient | 5 to 7 outcomes with Bloom verbs; prerequisite tree; concept map; knowledge-graph relations list (requires, causes, contrasts, implements); reading plan with time per part | A3, A8, A54, V13 |
| 2 Prime | 5 predict-then-check items in the form scenario, prediction, result, what a wrong guess means; entry diagnostic; 5 concept cards | A11, A13, A50, P6 |
| 3 Intuition | concrete example first; first-principles chain (problem, naive solution, why it fails, constraints, concept, trade-offs); 2 analogies each with gets-right and breaks; black-box figure; labels Simplified, Accurate, Expert | A4, A5, A7, A18, V18 |
| 4 Foundations | 10 or more terms (plain, precise, example, why it matters); relations; same idea in five representations (words, diagram, example, table, code); cloze cards | A4, A8, A17, V19 |
| 5 Mechanics | step table with input, trigger, state change, output, assumption, failure per step; seven-lens table; a sequence figure, a flow figure and a data-shape figure; trace; three models (simplified, accurate, expert) | A4, A6, A31, A57, V9, V11, V16, V20 |
| 6 Worked examples | 3 examples, each with known, needed, principle, why it applies, solution, verification; Socratic questions; trace table; 2 faded copies; one example redone in another representation | A9, A10, A12, A17, A31, V21 |
| 7 Compare and decide | comparison matrix with a decision rule; why-not for each rival; trade-offs (gain, lose, when); alternatives and cost-benefit; what mature tools already solve it; labelled advice; assumptions line; decision tree | A16, A24, A27, A39, A40, A41, V7, V15 |
| 8 Do it | 4 labs (guided, prompted, unassisted, adversarial) each with objective, environment, numbered tasks with the reason, expected output or check, four-tier hints, cleanup, stretch; every command explained (arguments, flags, side effects, risks) | A4.4, A29, A33, P3, P4, P7, P16 |
| 9 Repair | mistakes table of 8 or more rows with an error class (factual, conceptual, procedural, logical, assumption, strategy); 3 misconceptions each with why reasonable, where it breaks, test; before/after figure | A14, A15, V30 |
| 10 Break it | 3 failure cases with symptom, hypotheses table, informative test, cause, fix, prevention; 2 break-fix labs showing only the symptom; debugging checklist; diagnostic decision tree; failure map | A22, A25, A32, V25, P8 |
| 11 Zoom out | ecosystem to function ladder; systems figure with a bottleneck and a trust boundary marked; performance loop; security notes; novice versus expert table; tacit-knowledge labels; evidence tags (fact, observed, inference, assumption, estimate) | A23, A26, A28, A34, A35, A42, V22, V27, V28 |
| 12 Retrieve | 10 micro-drills; 5 trace drills; 3 spot-the-bug items; 10 quiz questions (4 options, every option explained, distractors from misconceptions); 30 flashcards (concept, cloze, scenario, contrast, trace, at least 5 each, tagged easy, medium, trap); interleaved set of 12 unlabelled items; spaced schedule (1, 3, 7, 14, 30 days); error-to-aid template; fill-in-the-node item | A11, A14, A19, A20, P5, P6, P9, P10, P11, P17, V31 |
| 13 Transfer and design | near, representation, context and far transfer; critique of a flawed example; reconstruction; design kata with a constraint shift; capstone (spec, non-goals, 3 to 5 milestones, acceptance tests, rubric) | A21, A46, A47, A48, P13, P14 |
| 14 Teach back | explain to beginner, practitioner, expert with a model answer and a rubric; metacognition ladder; the 11 mastery checks each with a concrete task; independence checklist | A49, A50, A51, A59, P15 |
| 15 Close | 2 cheat sheets (decision tree, top patterns, pitfalls); glossary of 15 or more terms; claims register (10 or more rows, 5 cells, statuses Read, Listing read, Run, Not run); gap list; rule-coverage matrix; visual completion report; next steps | A42, A44, A58, A60, V29, V32, P12, P18 |

## 4. Size

Topic total at least 9,000 words (L1), 11,000 (L2), 13,000 (L3), counted outside code blocks. At about 1.35 tokens a word with tables and figures, a topic is roughly 18,000 to 25,000 output tokens, which is 3 to 4 times the v1 page.

## 5. Grounding, copying and honesty (unchanged from the standard)

Facts come from a captured source pack or are `VERIFY`; at most 15 percent of the text may repeat the seed page in 8-word runs; no word skips a step (`simply`, `just`, `obviously`, `trivially`, `clearly`, `of course` are banned); every lab command is run by the gate and the page carries "Run" only for what was run; status is `proposed`; the gate is evidence of structure, never a review.
