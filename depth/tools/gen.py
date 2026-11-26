#!/usr/bin/env python3
"""Generate candidate depth pages with a local model, one move (section) at a time. Standard library only.

    python depth/tools/gen.py --spec depth/spec/K-LOG01.json --seed depth/seed/K-GEN01-shell-pipelines.md \
        --pack pack.txt --model qwen3:8b --url http://127.0.0.1:11500 --n 10 --out runs/log01
Writes cand-NN.md (lab blocks hold commands only; run `gate.py --fill --data DIR --pack pack.txt cand-NN.md` next).
The seed page is shown to the model one move at a time as the FORMAT example (never as content). The model is told the standard's
rules for that move; facts must come from the source pack; every number printed by a command is filled in by running it.
"""
import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

MOVES = {
 1: ("Orient", 250, "Outcomes (3 to 7, one Bloom verb each), prerequisites, a short answer (two sentences), and ONE ASCII concept-map figure in a code block (at most 9 nodes, every link labelled)."),
 2: ("Prime", 200, "Three predict-then-check questions with short answers marked as answers to check after reading, then three concept cards to cover and reveal."),
 3: ("Intuition", 350, "The concrete problem, the naive solution, why it falls short, ONE analogy stating what it gets right and where it breaks, and a small black-box ASCII figure (input, box, output)."),
 4: ("Foundations", 300, "A table: Term | Plain English | Precise | Example | Why it matters (6 to 8 terms), then one line of relations (requires, causes, contrasts, replaces)."),
 5: ("Mechanics", 450, "Step-by-step what happens, the seven lenses (what, why, how, when, where, what if, why not) in one paragraph, a simplified model then an accurate model then an expert model marked VERIFY, and ONE ASCII flow or sequence figure."),
 6: ("Worked example", 450, "One worked example on the sample data: look at the data first, build the answer one stage at a time using ```lab blocks (write ONLY the `$ command` lines; the real output is added by the harness), a trace table on a tiny input, a faded copy with blanks and its answer, and a similar problem to try alone."),
 7: ("Compare and decide", 300, "A comparison table with 'why not the others', a one-line decision rule, ONE ASCII decision-tree figure, and three advice labels (requirement, best practice, rule of thumb)."),
 8: ("Do it: guided lab", 550, "Objective, environment, cleanup, then 4 numbered tasks each with: the question, why this approach, a ```lab block with ONLY the `$ command` line(s), and a four-tier hint ladder written as '- Hint 1:' to '- Hint 4:' (nudge, direction, partial with blanks, full answer). End with verification, a stretch, and the guided/prompted/unassisted/adversarial progression."),
 9: ("Repair: common mistakes", 300, "A table Mistake | What breaks | Instead (5 to 6 rows), one named misconception with why it is reasonable, where it breaks and a test, and ONE before/after ASCII figure with [!] on the fault."),
 10: ("Break it", 350, "A failure case: symptom, three hypotheses in a table (hypothesis, evidence for, evidence against, test, result), one ```lab block showing the symptom (commands only), a break-fix exercise showing only the symptom, prevention, and ONE ASCII failure-map figure."),
 11: ("Zoom out", 250, "Where this sits in the larger system, the trust boundary (data versus code), the bottleneck, and beginner / accurate / expert models with the expert one marked VERIFY."),
 12: ("Retrieve and discriminate", 900, "Exactly: 6 micro-drills written as '1. **Drill** question. *Answer:* ...'; one trace drill; 5 quiz questions written as '**Q1.** text' with four options '  - (A) option — why it is right or wrong' (every option explained, at least 20 characters of reason, distractors from real misconceptions); 16 flashcards written '- [type][difficulty] Front: ... Back: ...' with types concept, cloze, scenario, contrast, trace (at least 2 of each) and difficulty easy, medium or trap; a mixed set with earlier ideas."),
 13: ("Transfer and design", 300, "Near, representation, context and far transfer problems; one critique of a flawed example; one reconstruction; one design problem with a constraint shift."),
 14: ("Teach back and check yourself", 200, "Explain-to-three-audiences prompts (beginner, practitioner, expert) with a model answer for each, and the 11-level mastery ladder as a checklist."),
 15: ("Close", 450, "A cheat sheet in a code block (decision tree, top patterns, pitfalls), what to learn next, a claims register table '| Id | Claim | Quote or VERIFY | Status | Note |' with at least 6 rows (Status is exactly one of Read, Listing read, Run, Not run; a Read claim must quote 8 or more consecutive words from the source pack, otherwise write VERIFY and Not run), and a gap list that starts 'Not covered by the captured source:'."),
}

RULES = """You write one section of a study page for a visual learner moving from novice to expert. Rules:
- Draw first, narrate second: ASCII figures go in plain ``` code blocks, at most 9 nodes, every arrow labelled.
- Plain wording. NEVER use the words: simply, just, obviously, trivially, clearly, of course. Define each term before use.
- Facts about the tools come only from the SOURCE PACK. If you are unsure, write VERIFY. Never invent options, outputs or numbers.
- Never write command output yourself: in ```lab blocks write only lines starting with '$ ' and the command. The harness runs them on the sample data and adds the real output.
- In prose, do not state specific counts or results of commands (they are filled in only inside lab blocks).
- Only use these programs in lab commands, one pipeline per line, no redirects, no semicolons: {tools}.
- Start your answer with the exact heading line given and output only that section, in Markdown."""


def sections(md):
    m = re.search(r"^## 1\.", md, re.M)
    body = md[m.start():]
    parts = re.split(r"(?m)^(?=## \d+\.)", body)
    return {int(re.match(r"## (\d+)\.", p).group(1)): p.strip() for p in parts if p.strip()}


def chat(url, model, system, user, num_ctx, temp, num_predict, seed):
    body = json.dumps({"model": model, "stream": False, "think": False,
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                       "options": {"num_ctx": num_ctx, "temperature": temp, "num_predict": num_predict, "seed": seed}}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(url + "/api/chat", body, {"Content-Type": "application/json"}), timeout=1800))
    return r["message"]["content"].strip(), r.get("eval_count", 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--model", default="qwen3:8b")
    ap.add_argument("--url", default="http://127.0.0.1:11500")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--temp", type=float, default=0.8)
    ap.add_argument("--num-ctx", type=int, default=16384)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    seed = sections(Path(a.seed).read_text(encoding="utf-8"))
    pack = Path(a.pack).read_text(encoding="utf-8")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    system = RULES.format(tools=", ".join(spec["allowed_tools"]))
    for k in range(a.start, a.start + a.n):
        t0, toks, secs = time.time(), 0, []
        for n in range(1, 16):
            name, words, how = MOVES[n]
            head = f"## {n}. {name}"
            user = (f"TOPIC: {spec['title']} (level {spec['level']}); learner: {spec['audience']}.\nFOCUS: {spec['focus']}.\n"
                    f"SAMPLE DATA you may use in lab commands (files already in the working directory):\n"
                    + "\n".join(f"- {f}: {d}" for f, d in spec["data"].items())
                    + f"\nQUESTIONS the labs should answer: " + "; ".join(spec["lab_questions"])
                    + f"\nAVOID: {', '.join(spec['avoid'])}.\n\nSOURCE PACK (the only allowed source of tool facts):\n{pack}\n\n"
                    f"FORMAT EXAMPLE: this is the same section of a DIFFERENT page (topic: shell pipelines on a sales file). Copy its shape, tables, labels and figure style. Do NOT copy its words or its content.\n<example>\n{seed[n]}\n</example>\n\n"
                    f"NOW WRITE section {n} for the topic above. Required content: {how} Aim for about {words} words. Begin with the line: {head}")
            text, c = chat(a.url, a.model, system, user, a.num_ctx, a.temp, int(words * 3.2) + 400, 1000 * k + n)
            text = re.sub(r"^<think>.*?</think>\s*", "", text, flags=re.S)
            if not text.startswith("## "):
                text = head + "\n\n" + text
            secs.append(text)
            toks += c
        fm = (f"---\nid: {spec['id']}\ntitle: \"{spec['title']}\"\ncategory: {spec['category']}\nlevel: {spec['level']}\nstatus: proposed\n"
              f"lab_run: \"Not run yet: lab outputs are filled by running the commands in the sandbox (depth/tools/gate.py --fill)\"\n"
              f"lane: local model {a.model}, candidate {k}\n---\n\n# {spec['title']}\n\n")
        (out / f"cand-{k:02d}.md").write_text(fm + "\n\n".join(secs) + "\n", encoding="utf-8")
        print(f"cand-{k:02d}: {toks} tokens in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
