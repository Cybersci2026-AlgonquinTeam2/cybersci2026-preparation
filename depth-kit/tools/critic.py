#!/usr/bin/env python3
"""Cross-model review (standards section 9). A Critic model reads a topic against the rules and returns findings.

    python tools/critic.py TOPIC_DIR --out findings.json [--model M] [--url U] [--pack PACK.txt] [--probe]
Every finding must quote the page text it concerns (verbatim, whitespace-insensitive); findings without a valid quote are discarded and counted.
--probe runs the review twice and marks findings that do not recur as low confidence. The output is advisory: it never edits the page and never promotes it.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gatelib as L  # noqa: E402
import kitconfig  # noqa: E402
import retrieve  # noqa: E402
from gen import chat  # noqa: E402

CRITERIA = """Review the CHUNK of a study page. Report only real problems, each tied to an exact quote from the chunk.
Look for: (1) a statement that is factually wrong or contradicts the SOURCE PASSAGES; (2) a claim whose quote does not state the claim; (3) a command described incorrectly or a lab that answers a different question than the text says;
(4) a quiz option whose verdict (right or wrong) contradicts its explanation; (5) a missing or incomplete four-tier hint ladder; (6) text unrelated to the topic; (7) a step skipped without explanation or a skip-word (simply, just, obviously, trivially, clearly, of course);
(8) an unlabelled assumption or an unsupported certainty.
Answer ONLY with a JSON array. Each item: {"quote": "exact text from the chunk (under 200 characters)", "rule_or_source": "the rule or source it conflicts with", "severity": "high|medium|low", "why": "one sentence"}. If there are no problems answer []."""


def chunks(text, words=700):
    out, cur, n = [], [], 0
    for blk in re.split(r"(?m)^(?=#{1,3} )", text):
        w = len(blk.split())
        if cur and n + w > words:
            out.append("".join(cur))
            cur, n = [], 0
        cur.append(blk)
        n += w
    if cur:
        out.append("".join(cur))
    return out


def parse_json_array(s):
    m = re.search(r"\[.*\]", s, re.S)
    if not m:
        return []
    try:
        return [x for x in json.loads(m.group(0)) if isinstance(x, dict)]
    except Exception:
        return []


def review(text, label, cfg, model, url, pack):
    found, dropped = [], 0
    ntext = L.norm(text)
    for ch in chunks(text):
        passages = "\n---\n".join(retrieve.top_passages(pack, ch[:600], 4, cfg["sources"]["passage_words"])) if pack else "(none supplied)"
        user = f"SOURCE PASSAGES:\n{passages}\n\nCHUNK ({label}):\n{ch}\n\n{CRITERIA}"
        raw, _ = chat(url, model, "You are a careful reviewer. Be specific and quote exactly.", user, cfg["models"]["num_ctx"], 0.2, 900, 7)
        for f in parse_json_array(raw):
            q = str(f.get("quote", "")).strip()
            if len(q) >= 12 and L.norm(q) in ntext:
                f["file"] = label
                found.append(f)
            else:
                dropped += 1
    return found, dropped


def main():
    cfg = kitconfig.load()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model")
    ap.add_argument("--url")
    ap.add_argument("--pack")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--config")
    a = ap.parse_args()
    model, url = a.model or cfg["models"]["critic"], a.url or cfg["models"]["ollama_url"]
    pack = Path(a.pack).read_text(encoding="utf-8", errors="ignore") if a.pack else ""
    allf, dropped = [], 0
    for p in sorted(Path(a.topic).glob("[1-9]-*.md")):
        text = p.read_text(encoding="utf-8")
        f, d = review(text, p.name, cfg, model, url, pack)
        allf += f
        dropped += d
        if a.probe:
            f2, _ = review(text, p.name, cfg, model, url, pack)
            q2 = {L.norm(x["quote"]) for x in f2}
            for x in f:
                x["confidence"] = "recurred" if L.norm(x["quote"]) in q2 else "low (did not recur)"
    Path(a.out).write_text(json.dumps({"critic_model": model, "advisory": True, "findings": allf, "discarded_without_valid_quote": dropped}, indent=1), encoding="utf-8")
    print(f"{len(allf)} findings with valid quotes, {dropped} discarded -> {a.out}")


if __name__ == "__main__":
    main()
