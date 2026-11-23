#!/usr/bin/env python3
"""Build the Command Atlas: expanded 'man pages' with REAL captured output.

    python scripts/atlas_build.py              # run every example in WSL, write curriculum/atlas/*.md
    python scripts/atlas_build.py --tool grep  # one tool

Each recipe's command is executed for real in a throw-away lab folder inside WSL (Ubuntu-24.04), and the
output that appears in the guide is what the tool actually printed on the build date. Nothing leaves your machine
(the web/netcat examples talk only to 127.0.0.1). Definitions live in scripts/atlas_tools.py.
"""
import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_tools as T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "curriculum" / "atlas"
DISTRO = "Ubuntu-24.04"


LOCAL = sys.platform.startswith("linux")      # on Kali/Linux run recipes natively; on Windows go through WSL


def run_wsl(script, timeout=180):
    cmd = ["bash", "-s"] if LOCAL else ["wsl.exe", "-d", DISTRO, "-e", "bash", "-s"]
    p = subprocess.run(cmd, input=script.encode("utf-8"), capture_output=True, timeout=timeout)
    return p.stdout.decode("utf-8", "replace").replace("\x00", "").replace("\r", "")


def capture(tool):
    """Run setup, every recipe, teardown in ONE bash session; return {recipe_index: output} and version string.
    If the tool binary is missing, nothing is run and the page is marked as not captured."""
    need = tool.get("needs")
    if need and "yes" not in run_wsl(f"command -v {need} >/dev/null 2>&1 && echo yes || echo no"):
        return None, f"{need} not installed here"
    parts = ["set +e", T.LAB_SETUP, tool.get("setup", "")]
    for i, r in enumerate(tool["recipes"]):
        cmd = r["cmd"]
        parts.append(f'echo "@@START {i}"')
        parts.append(f'( {cmd} ) </dev/null 2>&1 | head -n {r.get("lines", 30)} | cut -c1-{r.get("cols", 160)}')
        parts.append(f'echo "@@END {i}"')
    parts.append(tool.get("teardown", ""))
    parts.append(f'echo "@@VERSION"; ( {tool.get("version", tool["name"] + " --version")} ) 2>&1 | head -n 1')
    raw = run_wsl("\n".join(parts))
    outs, cur, ver = {}, None, ""
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("@@START "):
            cur = int(ln.split()[1]); outs[cur] = []
        elif ln.startswith("@@END "):
            cur = None
        elif ln.startswith("@@VERSION"):
            ver = lines[i + 1].strip() if i + 1 < len(lines) else ""
            break
        elif cur is not None:
            outs[cur].append(ln)
        i += 1
    return {k: "\n".join(v).rstrip("\n") for k, v in outs.items()}, ver


def render(tool, outs, ver):
    n = tool["name"]
    cap = outs is not None
    if not cap:
        outs = {}
    banner = (f"> Captured {date.today().isoformat()} on {'Linux' if LOCAL else 'Ubuntu 24.04 (WSL)'}: `{ver}`. Every output block below is what the command really printed in a lab folder; flags can differ on other versions or systems (Kali, macOS, BusyBox)."
              if cap else
              f"> **Not captured yet** ({ver}). The outputs below are marked *expected*: they describe what you should see. Run `python3 scripts/atlas_build.py --tool {n}` on a machine that has the tool (Kali has it) to replace them with real captured output.")
    md = [f"# {n}: the expanded manual", "", banner, "",
          f"**In one line:** {tool['one_line']}", "", "## When you reach for it (in a CTF or defence task)", ""]
    md += [f"- {w}" for w in tool["when"]]
    md += ["", "## Anatomy of a command", "", "```text", tool["anatomy"].rstrip(), "```", "", "## The flags worth knowing", "",
           "| Flag | What it does | Reach for it when |", "|---|---|---|"]
    md += [f"| `{f}` | {d} | {w} |" for f, d, w in tool["flags"]]
    md += ["", "## Recipes with real output", "", "The lab folder used for these examples is created fresh each build (see the bottom of this page).", ""]
    for i, r in enumerate(tool["recipes"]):
        md += [f"### {i + 1}. {r['title']}", "", r["why"], "", "```bash", "$ " + r["show"] if r.get("show") else "$ " + r["cmd"], "```", "", "```text",
               (outs.get(i, "(no output captured)") or "(no output: that is the result)") if cap else "(expected, not captured) " + r.get("expect", "see the explanation below"), "```", "", r["read"], ""]
    md += ["## Mistakes people make", ""] + [f"- {g}" for g in tool["gotchas"]]
    md += ["", "## Related tools", "", ", ".join(tool["related"]), "", "## Practice", ""] + [f"{k}. {p}" for k, p in enumerate(tool["practice"], 1)]
    md += ["", "## Flashcard prompts", ""] + [f"- {q}" for q in tool["cards"]]
    md += ["", "## The lab used for these examples", "", "```bash", T.LAB_SETUP.strip(), "```", ""]
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for tool in T.TOOLS:
        if a.tool and tool["name"] != a.tool:
            continue
        outs, ver = capture(tool)
        missing = [i for i in range(len(tool["recipes"]))] if outs is None else [i for i in range(len(tool["recipes"])) if i not in outs]
        (OUT / f"{tool['name']}.md").write_text(render(tool, outs, ver), encoding="utf-8")
        import atlas_man
        atlas_man.write(tool, outs, ver)
        print(f"{tool['name']:16s} {0 if outs is None else len(outs)}/{len(tool['recipes'])} recipes captured", "MISSING " + str(missing) if missing else "", "|", ver[:60])
    import atlas_man
    atlas_man.write_index(T.TOOLS)


if __name__ == "__main__":
    main()
