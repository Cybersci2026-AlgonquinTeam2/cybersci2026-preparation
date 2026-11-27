#!/usr/bin/env python3
"""Cold-start stage 1 (standards section 11): create a headed skeleton for a new topic with every required element as an empty slot.

    python tools/new_topic.py --spec SPEC.json --out TOPIC_DIR
The owner (or the drafter, slot by slot) fills the slots; `tools/gate.py` then measures what is still missing.
The slot text is the same instruction the generator uses, so a hand-written seed and a generated candidate are held to one definition.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kitconfig  # noqa: E402
from gen import CORE, EXT  # noqa: E402

FILES = {"1-learn.md": [1, 2, 3, 4, 5, 6, 7], "2-do.md": [8, 9, 10], "3-retrieve.md": [12], "4-transfer.md": [11, 13, 14], "5-reference.md": [15]}


def main():
    cfg = kitconfig.load()
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fm = (f"---\nid: {spec['id']}\ntitle: \"{spec['title']}\"\ncategory: {spec['category']}\nlevel: {spec['level']}\nstatus: proposed\n"
          f"lab_run: \"Not run yet\"\nlane: skeleton, to be filled\n---\n\n# {spec['title']}\n\n")
    for fn, moves in FILES.items():
        body = []
        for m in moves:
            title, words, how, checks = CORE[m]
            body.append(f"## {m}. {title}\n\n<!-- SLOT {m}: about {words} words. REQUIRED: {how} -->\n\n[SLOT {m}]\n")
        (out / fn).write_text((fm if fn == "1-learn.md" else "") + "\n".join(body), encoding="utf-8")
    for n, (fname, title, words, how, checks) in EXT.items():
        (out / fname).write_text(f"# {title}\n\n<!-- SLOT ext{n}: about {words} words. REQUIRED: {how} -->\n\n[SLOT ext{n}]\n", encoding="utf-8")
    (out / "SLOTS.md").write_text("# Slots to fill\n\n" + "\n".join(f"- move {m}: {CORE[m][0]}" for ms in FILES.values() for m in ms) + "\n" + "\n".join(f"- extension {n}: {EXT[n][1]}" for n in EXT) + "\n", encoding="utf-8")
    print(f"skeleton for {spec['id']} written to {out}: {sum(len(v) for v in FILES.values())} moves and {len(EXT)} extension units")


if __name__ == "__main__":
    main()
