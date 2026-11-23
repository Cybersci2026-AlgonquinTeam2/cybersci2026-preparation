"""Convert Command Atlas tool definitions into mangui guide JSON (mangui/guides/<command>.json).

Hand-authored guides (see mangui_build.py) are never overwritten. Converted guides start with the flags listed in the atlas
definition; `python3 mangui/mangui.py coverage` shows how many of the original page's options are still unexplained.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "mangui" / "guides"
HAND = {"file", "grep"}                      # authored fully in mangui_build.py
NAME_MAP = {"python-oneliners": "python3"}   # atlas page name -> command whose man page it extends
SKIP = {"file-xxd-strings", "readelf-objdump"}   # combined pages: to be split into one guide per command


def write(tool, outs, ver, local):
    n = NAME_MAP.get(tool["name"], tool["name"])
    if n in HAND or tool["name"] in SKIP:
        return None
    cap = outs is not None
    ex = []
    for i, r in enumerate(tool["recipes"]):
        out = (outs.get(i, "") if cap else "(expected, not captured) " + r.get("expect", "see the explanation"))
        ex.append(dict(title=r["title"], cmd=r.get("show") or r["cmd"], output=out))
    doc = dict(name=n, section="1", one_line=tool["one_line"],
               plain=[tool["one_line"].rstrip(".") + ".", "The sections below show when to use it, real examples, and the options explained in plain English."],
               when=tool["when"], examples=ex,
               options=[dict(flag=f, plain=d, use=w) for f, d, w in tool["flags"]],
               mistakes=tool["gotchas"], **{"try": tool["practice"]}, see_also=", ".join(tool["related"]) + ".",
               captured_with=(f"Example output captured {date.today().isoformat()} with {ver} on {'Linux' if local else 'Ubuntu 24.04 (WSL)'}."
                              if cap else f"Examples marked expected were not captured yet ({ver}); run scripts/atlas_build.py where the tool is installed (Kali) to capture real output."))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{n}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return n
