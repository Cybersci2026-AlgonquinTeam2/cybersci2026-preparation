#!/usr/bin/env python3
"""Generate a candidate topic package with a local model, one move (or extension unit) at a time. Standard library only.

    python tools/gen.py --spec SPEC.json --seed SEED_TOPIC_DIR --pack PACK.txt --out OUT_DIR [--n 1] [--start 1] [--model M] [--url U] [--best-of N]
For each unit the tool: retrieves the source passages relevant to the unit, shows the model the seed's section as a STRUCTURE-ONLY
format example (prose truncated, so there is nothing to copy), generates up to best-of-N candidates, runs unit-level checks
(heading, banned words, allowed lab commands, originality against the seed, required element counts), keeps the first clean candidate
or the one with the fewest failures, and records every attempt in provenance.json (model, settings, prompt and pack hashes).
Lab outputs are never written by the model: run `gate.py --fill --data DIR` on the result.
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gatelib as L  # noqa: E402
import kitconfig  # noqa: E402
import retrieve  # noqa: E402

# (title, target words, instruction, [(regex, minimum count), ...])  regexes are matched per line (re.M) on the candidate text
CORE = {
 1: ("Orient", 650, "5 to 7 outcomes with Bloom verbs {A3}; a prerequisite tree figure {V13}{fig:tree}; the short answer; a concept map figure {A8}{fig:map}; a legend figure {V5}; the knowledge-graph relations list (requires, causes, contrasts, replaces) {A8}; a reading plan with time per part.", [(r"\{fig:", 2)]),
 2: ("Prime", 450, "5 predict-then-check rows as a table: scenario, your prediction, result, what a wrong guess means {A13}; an entry diagnostic {A50}; 5 concept cards {P6}.", [(r"^\| \d", 5)]),
 3: ("Intuition", 700, "The concrete example first {A7}; a first-principles table: problem, naive solution, why it fails, constraints, the concept, trade-offs {A5}; TWO analogies each with 'gets right' and 'breaks' {A18}; a black-box figure {V18}{fig:blackbox}; label Simplified, Accurate, Expert.", [(r"Gets right|gets right", 2)]),
 4: ("Foundations", 650, "A table of 10 to 12 terms: Term | Plain English | Precise | Example | Why it matters; the relations line {A8}; the same idea in five representations: words, diagram, example, table, code {A17}; cloze cards {P6}.", [(r"^\| .+ \| .+ \| .+ \| .+ \| .+ \|$", 8)]),
 5: ("Mechanics", 1000, "A step table with columns input, trigger, state change, output, assumption, failure {A4}; a sequence figure {V9}{fig:sequence}; a flow figure with the error path {V6}{fig:flow}; a data-shape figure {V11}{fig:layout}; a states figure {V10}{fig:states}; a layers figure {V14}{fig:layers}; the seven-lens table {A6}; textbook versus production {V23}; three models Simplified, Accurate, Expert {A7}.", [(r"\{fig:", 4)]),
 6: ("Worked examples", 1200, "THREE worked examples, each with known, needed, principle, why it applies, solution, verification {A10}; Socratic questions {A12}; a trace table {A31}{V16}{fig:trace}; two faded copies {A9}; one example redone in another representation {A17}; a fade-the-figure figure {V21}. Lab blocks hold only `$ command` lines.", [(r"^### Example", 3), (r"```lab", 3)]),
 7: ("Compare and decide", 800, "A comparison matrix {V15}; a one-line decision rule {A16}; a decision tree figure {V7}{fig:tree}; a trade-offs table gain/lose/when {A24}{A40}; the mature tools that already solve it {A39}; labelled advice {A27}; an assumptions line {A41}; a trade-off matrix figure {V26}{fig:matrix}.", [(r"\{fig:", 2)]),
 8: ("Do it: four labs", 1500, "Four labs: A guided, B prompted, C unassisted, D adversarial, each a '### Lab X' heading {P3}{P7}; objective, environment, cleanup; numbered tasks with the reason for each; lab blocks with only `$ command` lines; a four-tier hint ladder '- Hint 1:' to '- Hint 4:' after every task {P16}; a table explaining every command: arguments, reads/writes, privileges, output, risks {A29}.", [(r"^### Lab [A-D]", 4), (r"^\s*- Hint 4", 6)]),
 9: ("Repair", 700, "A mistakes table of 8 rows Mistake | What breaks | Instead | Error class, the last cell one of factual, conceptual, procedural, logical, assumption, strategy {A14}; THREE misconceptions written '**Misconception N**' with why reasonable, where it breaks, a test {A15}; a before/after figure {V17}{V30}{fig:diff}.", [(r"^\*\*Misconception \d", 3), (r"\| (factual|conceptual|procedural|logical|assumption|strategy) \|$", 8)]),
 10: ("Break it", 1000, "THREE failure cases '### Failure case N' each with symptom, a hypotheses table (hypothesis, evidence for, evidence against, test, result), cause, fix, prevention {A22}{A25}; TWO '**Break-fix lab N**' showing only the symptom with a debrief {P8}; a debugging checklist {A32}; a diagnostic decision tree {V25}{fig:tree}; a failure map {fig:failure}.", [(r"^### Failure case", 3), (r"\*\*Break-fix lab \d", 2)]),
 11: ("Zoom out", 900, "The ecosystem-to-function ladder {A4}{V22}; a systems figure with zones, a bottleneck [!] and a trust boundary {V8}{V27}{fig:zones}; feedback and bottlenecks {A23}; the performance loop {A35}{V28}; security notes {A34}; architecture view {A28}; a novice versus expert table {A26}; tacit-knowledge labels {A27}; evidence tags fact/observed/inference/assumption/estimate {A42}{V32}.", [(r"\{fig:", 1)]),
 12: ("Retrieve and discriminate", 2200, "EXACTLY: 10 micro-drills '1. **Drill** ... *Answer:* ...' {P9}; 5 trace drills '1. **Trace** ...' {P10}; 3 '1. **Spot the bug** ...' {V31}; a fill-in-the-node figure; 10 quiz questions '**Q1.** text' each with four options '  - (A) option — why it is right or wrong (20+ characters)' with distractors from real misconceptions {P11}; 30 flashcards '- [type][difficulty] Front: ... Back: ...' types concept, cloze, scenario, contrast, trace (6 each), difficulty easy, medium or trap {P6}; 12 interleaved items numbered 1 to 12 under '### Interleaved set' {A19}; '### Spaced review schedule' with rows day 0, day 1, day 3, day 7, day 14, day 30 {A20}{P17}; the error-to-aid template with fields 'Error class' and 'New card' {P5}.", [(r"^\d+\. \*\*Drill\*\*", 10), (r"^\*\*Q\d+\.", 10), (r"^- \[\w+\]\[(easy|medium|trap)\]", 30), (r"^\d+\. \*\*Trace\*\*", 5)]),
 13: ("Transfer and design", 1000, "A table with rows Near, Representation, Context, Far {A21}; '### Reconstruction' {A47}; '### Design kata' with three constraint shifts and a trade-off matrix {A48}{P13}; '### Capstone project' with **Spec.**, **Non-goals.**, **Milestones.**, **Acceptance tests.** and a 'Self-review rubric' table {P14}; a critique section '### Critique' {A46}.", [(r"^### (Critique|Reconstruction|Design kata|Capstone project)", 4)]),
 14: ("Teach back and check yourself", 600, "A table with rows Beginner, Practitioner, Expert with a model answer and a rubric {A49}; the metacognition ladder {A50}; EXACTLY 11 mastery rows '| N Define | task |' through Teach, each with a concrete task {A51}; an '### Independence checklist' {A59}{A60}.", [(r"^\| \d+ (Define|Explain|Demonstrate|Apply|Distinguish|Analyse|Troubleshoot|Evaluate|Design|Transfer|Teach) \|", 11)]),
 15: ("Close", 1100, "'### Cheat sheet 1' and '### Cheat sheet 2' as figures {P12}; '### Glossary' with 16 terms; '### Claims register' with at least 12 rows '| C1 | claim | \"8+ word quote\" or VERIFY | Read, Listing read, Run or Not run | note |' (exactly 5 cells; Run for lab-verified claims; a Read claim quotes 8 or more consecutive words found in the SOURCE PASSAGES) {A42}{A58}; '### Gap list' starting 'Not covered by the captured source:'; '### Rule-coverage matrix' {A60}; '### Visual completion report' figure {V29}; '### Next steps' mentioning export {P18}.", [(r"^\| C\d+ \|", 12), (r"^### Cheat sheet", 2)]),
}
EXT = {
 6: ("6-language-primers.md", "Extension A: the small languages inside the tools", 2800, "For each language or tool family used in this topic, a section 'Extension A1', 'A2', ...: the idea, a labelled figure ({V19}{V20}), a reference table, a lab with a four-tier hint ladder, a mistake to avoid with its error class. {A53}{A56}", [(r"^## Extension A\d", 3)]),
 7: ("7-cases-and-projects.md", "Extension B: case studies, more labs, more failures, more design", 3600, "'### Case study 1..3' (scenario, questions, plan, lab block, interpretation, verification, expert additions) {A38}{A54}; '### Lab E', '### Lab F', '### Lab G' with ladders; code teaching from problem to script {A30}; '### Failure case 4..6'; '**Break-fix lab 3**' and '**Break-fix lab 4**'; '**Misconception 4..6**'; six more mistake rows with an error class; '**Critique 2**', '**Critique 3**'; '**Design kata 2**', '**Design kata 3**'; adaptive routing {A52}; a testing statement {A33}.", [(r"^### Case study", 3), (r"^### Lab [E-G]", 3)]),
 8: ("8-practice-bank.md", "Extension C: the practice bank", 3500, "An aid-selection table {P1}; atomic-item statement {P2}; drills 11 to 30; trace drills 6 to 15; spot-the-bug 4 to 9; quiz Q11 to Q20 with every option explained; 60 flashcards (12 per type); '## C6' with interleaved items 13 to 24; '## C7' one-sentence explanations and an error log.", [(r"^\d+\. \*\*Drill\*\*", 20), (r"^\*\*Q\d+\.", 10), (r"^- \[\w+\]\[(easy|medium|trap)\]", 60)]),
 9: ("9-extended-reference.md", "Extension D: extended reference", 1500, "'## Extended glossary' (20 terms); '## Cheat sheet 3'; a FAQ; claims C13 onward in the five-cell format; sources still to capture; export and reuse notes {P18}.", [(r"^\| C\d+ \|", 8)]),
}
RULES = """You write one unit of a study topic for a learner moving from novice to expert. Rules:
- Draw first, narrate second: ASCII figures in plain ``` blocks, at most 9 nodes, every arrow labelled. Tag rules like {{A13}} and figures like {{fig:flow}} where the element implements them.
- Plain wording. NEVER use: {banned}. Define each term before use.
- Facts about the subject come ONLY from the SOURCE PASSAGES. When unsure write VERIFY. Never invent options, outputs, numbers, versions or quotes.
- Never write command output: in ```lab blocks write only lines starting '$ ' with the command. The harness runs them on the sample data and adds the real output.
- In prose do not state specific counts or results of commands.
- Lab commands may use only these programs, one pipeline per line, no redirects or semicolons: {tools}.
- Do NOT copy wording from the format example; copy only its shape. Use the topic's own data and terms.
- Start with the exact heading line given and output only that unit, in Markdown."""


def skeleton(text):
    """Structure-only version of a seed unit: keep headings, table headers, tags, code fences and figures; shorten prose so there is nothing to copy."""
    out, in_code, seen_rows = [], False, 0
    for ln in text.splitlines():
        if ln.startswith("```"):
            in_code = not in_code
            out.append(ln)
            seen_rows = 0
            continue
        if in_code:
            out.append(ln if (not ln.startswith("$ ")) else "$ ...")
            continue
        if ln.startswith("#"):
            out.append(ln)
        elif ln.startswith("|"):
            seen_rows += 1
            out.append(ln if seen_rows <= 3 else "| ... |")
        elif ln.strip() == "":
            out.append(ln)
            seen_rows = 0
        else:
            w = ln.split()
            out.append(" ".join(w[:7]) + (" [...]" if len(w) > 7 else ""))
    return "\n".join(out)


def seed_units(seed_dir):
    parts = {p.name: p.read_text(encoding="utf-8") for p in sorted(Path(seed_dir).glob("*.md"))}
    core = {}
    for name, t in parts.items():
        if name[0] in "12345":
            for m in re.finditer(r"(?m)^## (\d+)\.", t):
                pass
            for chunk in re.split(r"(?m)^(?=## \d+\.)", t):
                mm = re.match(r"## (\d+)\.", chunk)
                if mm:
                    core[int(mm.group(1))] = chunk.strip()
    ext = {int(n[0]): t for n, t in parts.items() if n[0] in "6789"}
    return core, ext


def chat(url, model, system, user, num_ctx, temp, num_predict, seed):
    body = json.dumps({"model": model, "stream": False, "think": False,
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                       "options": {"num_ctx": num_ctx, "temperature": temp, "num_predict": num_predict, "seed": seed}}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(url + "/api/chat", body, {"Content-Type": "application/json"}), timeout=3600))
    return re.sub(r"^<think>.*?</think>\s*", "", r["message"]["content"].strip(), flags=re.S), r.get("eval_count", 0)


def unit_checks(text, heading, checks, example, cfg):
    fails = []
    if not text.startswith(heading.split("\n")[0][:12]):
        fails.append("heading")
    low = L.strip_code(text).lower()
    bad = [w for w in cfg["banned_words"] if re.search(rf"\b{re.escape(w)}\b", low)]
    if bad:
        fails.append(f"banned words {bad}")
    for b in L.lab_blocks(text):
        for cmd, _ in b:
            if not L.allowed(cmd, cfg):
                fails.append(f"lab command not allowed: {cmd[:40]}")
                break
    if L.copy_fraction(text, example) > cfg["thresholds"]["max_seed_copy"]:
        fails.append("copies the format example")
    for rx, mn in checks:
        if len(re.findall(rx, text, re.M)) < mn:
            fails.append(f"needs {mn}+ of /{rx[:30]}/")
    return fails


def main():
    cfg = kitconfig.load()
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--model")
    ap.add_argument("--url")
    ap.add_argument("--best-of", type=int)
    ap.add_argument("--only", help="comma list of units to generate, e.g. 1,2,6 (testing)")
    ap.add_argument("--config")
    a = ap.parse_args()
    M = cfg["models"]
    model, url, bo = a.model or M["drafter"], a.url or M["ollama_url"], a.best_of or M["best_of_n"]
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    core, ext = seed_units(a.seed)
    pack = Path(a.pack).read_text(encoding="utf-8", errors="ignore")
    pack_hash = hashlib.sha256(pack.encode()).hexdigest()[:16]
    system = RULES.format(banned=", ".join(cfg["banned_words"]), tools=", ".join(spec["allowed_tools"]))
    only = {int(x) for x in a.only.split(",")} if a.only else None
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    data_desc = "\n".join(f"- {f}: {d}" for f, d in spec["data"].items())
    for k in range(a.start, a.start + a.n):
        topic = out / f"cand-{k:02d}"
        topic.mkdir(exist_ok=True)
        prov, parts_text = [], {}
        t0 = time.time()
        units = [("core", n) for n in range(1, 16)] + [("ext", n) for n in range(6, 10)]
        for kind, n in units:
            if only and n not in only and not (kind == "core" and n in only):
                continue
            if kind == "core":
                title, words, how, checks = CORE[n]
                heading, example_full = f"## {n}. {title}", core.get(n, "")
            else:
                fname, title, words, how, checks = EXT[n]
                heading, example_full = f"# {title}", ext.get(n, "")
            example = skeleton(example_full)
            query = " ".join([title, spec["focus"], " ".join(spec.get("keywords", [])), " ".join(spec["lab_questions"][:2])])
            passages = retrieve.top_passages(pack, query, cfg["sources"]["retrieval_top_k"], cfg["sources"]["passage_words"])
            user = (f"TOPIC: {spec['title']} (level {spec['level']}); learner: {spec['audience']}.\nFOCUS: {spec['focus']}.\n"
                    f"SAMPLE DATA available in lab commands (files in the working directory):\n{data_desc}\n"
                    f"QUESTIONS the labs should answer: {'; '.join(spec['lab_questions'])}\nAVOID: {', '.join(spec['avoid'])}.\n\n"
                    f"SOURCE PASSAGES (the only allowed source of subject facts; quote 8+ consecutive words verbatim for Read claims):\n" + "\n---\n".join(passages) +
                    f"\n\nFORMAT EXAMPLE (structure only, from a different topic; copy the shape, not the words):\n<example>\n{example}\n</example>\n\n"
                    f"NOW WRITE the unit '{title}'. Required content: {how} Aim for about {words} words. Begin with the line: {heading}")
            phash = hashlib.sha256((system + user).encode()).hexdigest()[:16]
            best, attempts = None, []
            for i in range(bo):
                t1 = time.time()
                text, toks = chat(url, model, system, user, M["num_ctx"], M["temperature"], int(words * 3.2) + 600, 1000 * k + 10 * n + i)
                if not text.startswith("#"):
                    text = heading + "\n\n" + text
                fails = unit_checks(text, heading, checks, example_full, cfg)
                attempts.append({"attempt": i + 1, "tokens": toks, "seconds": round(time.time() - t1), "failures": fails})
                if best is None or len(fails) < len(best[1]):
                    best = (text, fails)
                if not fails:
                    break
            parts_text[(kind, n)] = best[0]
            prov.append({"unit": f"{kind}{n}", "title": title, "model": model, "temperature": M["temperature"], "num_ctx": M["num_ctx"],
                         "prompt_sha256_16": phash, "pack_sha256_16": pack_hash, "passages": len(passages), "attempts": attempts, "kept_failures": best[1]})
            print(f"cand-{k:02d} {kind}{n} {title}: {len(attempts)} attempt(s), kept failures: {best[1]}", flush=True)
        # assemble the nine files
        fm = (f"---\nid: {spec['id']}\ntitle: \"{spec['title']}\"\ncategory: {spec['category']}\nlevel: {spec['level']}\nstatus: proposed\n"
              f"lab_run: \"Not run yet: lab outputs are filled by running the commands in the sandbox (tools/gate.py --fill)\"\n"
              f"lane: local model {model}, candidate {k}\n---\n\n# {spec['title']}\n\n")
        files = {"1-learn.md": range(1, 8), "2-do.md": range(8, 11), "3-retrieve.md": [12], "4-transfer.md": [11, 13, 14], "5-reference.md": [15]}
        for fn, mv in files.items():
            body = "\n\n".join(parts_text[("core", m)] for m in mv if ("core", m) in parts_text)
            (topic / fn).write_text((fm if fn == "1-learn.md" else "") + body + "\n", encoding="utf-8")
        for n, (fname, *_r) in EXT.items():
            if ("ext", n) in parts_text:
                (topic / fname).write_text(parts_text[("ext", n)] + "\n", encoding="utf-8")
        (topic / "provenance.json").write_text(json.dumps({"spec": spec["id"], "model": model, "seconds": round(time.time() - t0), "units": prov}, indent=1), encoding="utf-8")
        print(f"cand-{k:02d} written to {topic} in {round(time.time() - t0)} s", flush=True)


if __name__ == "__main__":
    main()
