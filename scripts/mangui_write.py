#!/usr/bin/env python3
"""Write explained-example guides (no capture) to mangui/guides/*.json.

    python scripts/mangui_write.py            # every module listed in MODULES
    python scripts/mangui_write.py batch4
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
OUT = Path(__file__).resolve().parent.parent / "mangui" / "guides"
MODULES = ["mangui_batch4", "mangui_batch5", "mangui_batch6", "mangui_batch7"]


def main():
    want = [("mangui_" + a) if not a.startswith("mangui_") else a for a in sys.argv[1:]] or MODULES
    OUT.mkdir(parents=True, exist_ok=True)
    for m in want:
        for g in __import__(m).GUIDES:
            doc = dict(name=g["name"], section=g.get("section", "1"), one_line=g["one_line"], plain=g["plain"], when=g["when"],
                       examples=[dict(title=t, cmd=c, explain=e) for t, c, e in g["examples"]],
                       options=[dict(flag=f, plain=p, use=u) for f, p, u in g["options"]], mistakes=g["mistakes"], **{"try": g["try_"]},
                       see_also=g["see_also"], captured_with="Examples are written to explain a technique; they are not captured output.")
            (OUT / f"{g['name']}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            print(f"{g['name']:8s} {len(g['examples'])} examples, {len(g['options'])} options")


if __name__ == "__main__":
    main()
