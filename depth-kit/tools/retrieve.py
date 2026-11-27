#!/usr/bin/env python3
"""Passage retrieval over a source pack (BM25, standard library only). The drafter sees only the passages relevant to the move it is writing.

    python tools/retrieve.py PACK.txt "query words" [-k 6] [--words 160]
As a library: top_passages(pack_text, query, k, passage_words) -> list of passage strings (verbatim slices of the pack).
"""
import math
import re
import sys
from collections import Counter

STOP = set("the a an and or of to in on for with is are was be as at by it this that from can you your if not do does how what when".split())


def tok(s):
    return [w for w in re.findall(r"[a-z0-9_\-\.]+", s.lower()) if w not in STOP and len(w) > 1]


def passages(pack_text, passage_words=160):
    """Split into passages at blank lines, then cap each at about passage_words words (verbatim, so quotes stay valid)."""
    out = []
    for block in re.split(r"\n\s*\n", pack_text):
        words = block.split()
        if not words:
            continue
        if len(words) <= passage_words * 1.5:
            out.append(block.strip())
        else:
            lines, cur, n = block.splitlines(), [], 0
            for ln in lines:
                cur.append(ln)
                n += len(ln.split())
                if n >= passage_words:
                    out.append("\n".join(cur).strip())
                    cur, n = [], 0
            if cur:
                out.append("\n".join(cur).strip())
    return out


def top_passages(pack_text, query, k=6, passage_words=160):
    ps = passages(pack_text, passage_words)
    docs = [Counter(tok(p)) for p in ps]
    N = len(docs)
    df = Counter(t for d in docs for t in d)
    avg = sum(sum(d.values()) for d in docs) / max(N, 1)
    q = tok(query)
    k1, b = 1.5, 0.75
    scored = []
    for i, d in enumerate(docs):
        ln = sum(d.values())
        s = 0.0
        for t in q:
            if t in d:
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * d[t] * (k1 + 1) / (d[t] + k1 * (1 - b + b * ln / max(avg, 1)))
        scored.append((s, i))
    best = sorted((x for x in scored if x[0] > 0), reverse=True)[:k]
    return [ps[i] for _, i in sorted(best, key=lambda x: x[1])]   # keep original order for readability


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=6)
    ap.add_argument("--words", type=int, default=160)
    a = ap.parse_args()
    from pathlib import Path
    for p in top_passages(Path(a.pack).read_text(encoding="utf-8", errors="ignore"), a.query, a.k, a.words):
        print(p, "\n---")
