#!/usr/bin/env python3
"""Narrow-check Critic (standards section 9). Free-form "find anything wrong" review failed the planted-defect control (recall 0 of 6 with an
8B model), so this Critic asks narrow questions:

  mechanical (no model):  quiz verdicts (exactly one right option per question), hint ladders (tiers 1 to 4 in order), skip-words,
                          claim/quote relevance (lexical overlap), off-topic sentences (vocabulary novelty)
  model, one sentence at a time:  sentences that assert something (negations, "always", "only", "must", "never", ...) are checked against
                          their neighbouring lines and the retrieved source passages with a yes/no JSON answer

    python tools/critic.py TOPIC_DIR --out findings.json [--model M] [--url U] [--pack PACK] [--cpu] [--threads N] [--max-checks K] [--no-model]
--cpu runs the model on CPU and system RAM (Ollama num_gpu=0) so a busy or full GPU is not needed.
Every finding carries a valid verbatim quote, a method (mechanical or model) and a severity. The output is advisory: it never edits a page and never promotes it.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gatelib as L  # noqa: E402
import kitconfig  # noqa: E402
import retrieve  # noqa: E402
from gen import chat  # noqa: E402

STOP = set("the a an and or of to in on for with is are was be as at by it this that from can you your if not do does how what when which then than so but also each any all one two into out only just more most such use used using have has had will would should could may might its their there these those them they we our i".split())
ASSERT = re.compile(r"\b(is not|are not|isn't|aren't|cannot|can not|does not|do not|never|always|only|must|requires|needs|returns|means|prints|counts|sorts)\b", re.I)


def words(s):
    return [w for w in re.findall(r"[a-z][a-z0-9_\-]{2,}", s.lower()) if w not in STOP]


SKIP_CHECK = ("**Non-goals", "**Break-fix", "**Spot the bug")   # lines that list non-goals or describe a bug on purpose are not checked for truth or topic


def prose_lines(text, claims=False):
    """(line_index, line) for plain prose lines: not code, tables, headings, list markers of cards/hints, or html comments."""
    out, in_code, in_fm = [], False, text.startswith("---\n")
    for i, ln in enumerate(text.splitlines()):
        if in_fm:
            in_fm = not (i > 0 and ln.strip() == "---")
            continue
        if ln.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not ln.strip() or ln.lstrip().startswith(("|", "#", "<!--", "- [", "- Hint", "*Answer")):
            continue
        if claims and ln.lstrip().lstrip("0123456789. ").startswith(SKIP_CHECK):
            continue
        out.append((i, ln))
    return out


def sentences(line):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`*])", line) if len(s.split()) >= 6]


def m_quiz(text, name):
    f = []
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"\*\*Q\d+\.", ln):
            opts = []
            for j in range(i + 1, min(i + 9, len(lines))):
                if re.match(r"\*\*Q\d+\.", lines[j]):
                    break
                if re.match(r"\s*- \([A-D]\) ", lines[j]):
                    opts.append((j, lines[j]))
            right = [o for o in opts if "— right:" in o[1]]
            if opts and len(right) != 1:
                f.append({"file": name, "quote": opts[-1][1].strip()[:180], "rule_or_source": "a quiz question has exactly one right option", "severity": "high",
                          "why": f"{len(right)} options are marked right", "method": "mechanical"})
    return f


def m_hints(text, name):
    f, lines = [], text.splitlines()
    i = 0
    while i < len(lines):
        if re.match(r"\s*- Hint 1", lines[i]):
            seq, j = [1], i + 1
            while j < len(lines) and re.match(r"\s*- Hint (\d)", lines[j]):
                seq.append(int(re.match(r"\s*- Hint (\d)", lines[j]).group(1)))
                j += 1
            if seq != [1, 2, 3, 4]:
                f.append({"file": name, "quote": lines[j - 1].strip()[:180], "rule_or_source": "four-tier hint ladder (nudge, direction, partial, full answer)", "severity": "medium",
                          "why": f"the ladder has tiers {seq}", "method": "mechanical"})
            i = j
        else:
            i += 1
    return f


def m_skip(text, name, cfg):
    f = []
    for i, ln in prose_lines(text):
        for w in cfg["banned_words"]:
            if re.search(rf"\b{re.escape(w)}\b", ln, re.I):
                s = next((s for s in sentences(ln) if re.search(rf"\b{re.escape(w)}\b", s, re.I)), ln)
                f.append({"file": name, "quote": s[:180], "rule_or_source": "no skipped-step words", "severity": "medium", "why": f"contains '{w}'", "method": "mechanical"})
    return f


def m_claims(text, name):
    f = []
    for ln in text.splitlines():
        m = re.match(r"\| (C\d+) \| (.*?) \| (.*?) \| (Read|Listing read) \| (.*?) \|$", ln)
        if m:
            q = m.group(3).strip()
            if q.upper().startswith("VERIFY"):
                continue
            cw, qw = set(words(m.group(2))), set(words(q))
            overlap = len(cw & qw) / max(len(cw), 1)
            if overlap < 0.25:
                f.append({"file": name, "quote": ln[:180], "rule_or_source": "a Read claim's quote must state the claim", "severity": "high",
                          "why": f"only {int(overlap * 100)}% of the claim's words appear in its quote", "method": "mechanical"})
    return f


def m_offtopic(all_texts):
    vocab = Counter(w for t in all_texts.values() for _, ln in prose_lines(t) for w in words(ln))
    f = []
    for name, t in all_texts.items():
        for i, ln in prose_lines(t, True):
            for s in sentences(ln):
                ws = words(s)
                if len(ws) < 6:
                    continue
                rare = sum(1 for w in ws if vocab[w] <= 1) / len(ws)
                if rare >= 0.6:
                    f.append({"file": name, "quote": s[:180], "rule_or_source": "text must belong to the topic", "severity": "medium",
                              "why": f"{int(rare * 100)}% of its content words occur nowhere else in the topic", "method": "mechanical"})
    return f


def m_model(texts, cfg, model, url, pack, cpu, threads, max_checks):
    cands = []
    for name, t in texts.items():
        lines = t.splitlines()
        for i, ln in prose_lines(t, True):
            for s in sentences(ln):
                if ASSERT.search(s):
                    cands.append((name, i, s, " ".join(x.strip() for x in lines[max(i - 1, 0):i + 2])))
    neg = re.compile(r"\b(is not|are not|isn't|aren't|cannot|can not|does not|do not|never)\b", re.I)
    cands = sorted(cands, key=lambda c: 0 if neg.search(c[2]) else 1)[:max_checks]     # negations first: a flipped meaning is the likeliest error
    extra = {"num_gpu": 0, "num_thread": threads} if cpu else None
    out = []
    for name, i, s, ctx in cands:
        ps = "\n---\n".join(retrieve.top_passages(pack, s, 3, 120)) if pack else "(none supplied)"
        user = (f"SOURCE PASSAGES:\n{ps}\n\nNEARBY TEXT:\n{ctx[:900]}\n\nSTATEMENT:\n{s}\n\n"
                "Is the STATEMENT correct for this topic, consistent with the nearby text and the source passages? "
                'Answer ONLY JSON: {"correct": true or false, "reason": "one short sentence"}')
        raw, _ = chat(url, model, "You check one statement at a time. Be strict: mark false any statement that contradicts the nearby text or common technical knowledge.",
                      user, cfg["models"]["num_ctx"], 0.0, 80, 3, extra)
        m = re.search(r"\{.*?\}", raw, re.S)
        try:
            j = json.loads(m.group(0)) if m else {}
        except Exception:
            j = {}
        if j.get("correct") is False:
            out.append({"file": name, "quote": s[:180], "rule_or_source": "statement checked against nearby text and sources", "severity": "medium",
                        "why": str(j.get("reason", ""))[:160], "method": "model"})
    return out, len(cands)


def main():
    cfg = kitconfig.load()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model")
    ap.add_argument("--url")
    ap.add_argument("--pack")
    ap.add_argument("--cpu", action="store_true")
    ap.add_argument("--threads", type=int, default=32)
    ap.add_argument("--max-checks", type=int, default=150)
    ap.add_argument("--no-model", action="store_true")
    ap.add_argument("--config")
    a = ap.parse_args()
    model, url = a.model or cfg["models"]["critic"], a.url or cfg["models"]["ollama_url"]
    pack = Path(a.pack).read_text(encoding="utf-8", errors="ignore") if a.pack else ""
    texts = {p.name: p.read_text(encoding="utf-8") for p in sorted(Path(a.topic).glob("[1-9]-*.md"))}
    found = []
    for name, t in texts.items():
        found += m_quiz(t, name) + m_hints(t, name) + m_skip(t, name, cfg) + m_claims(t, name)
    found += m_offtopic(texts)
    mech = len(found)
    nchecks = 0
    if not a.no_model:
        mf, nchecks = m_model(texts, cfg, model, url, pack, a.cpu, a.threads, a.max_checks)
        found += mf
    allt = {n: L.norm(t) for n, t in texts.items()}
    valid = [f for f in found if L.norm(f["quote"]) in allt[f["file"]]]
    Path(a.out).write_text(json.dumps({"critic_model": None if a.no_model else model, "cpu": a.cpu, "advisory": True, "mechanical_findings": mech,
                                       "model_checks_run": nchecks, "findings": valid, "discarded_without_valid_quote": len(found) - len(valid)}, indent=1), encoding="utf-8")
    print(f"{len(valid)} findings ({mech} mechanical, {len(valid) - mech if len(valid) >= mech else 0} model; {nchecks} model checks run) -> {a.out}")


if __name__ == "__main__":
    main()
