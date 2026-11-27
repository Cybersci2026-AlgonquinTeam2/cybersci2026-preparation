"""Shared helpers for the topic gate, the generator and the critic. Config-driven (see kitconfig.py and config/project.json)."""
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

MOVE_NAMES = ["Orient", "Prime", "Intuition", "Foundations", "Mechanics", "Worked", "Compare", "Do it", "Repair", "Break", "Zoom", "Retrieve", "Transfer", "Teach", "Close"]


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def strip_code(t):
    return re.sub(r"```.*?```", " ", t, flags=re.S)


def parse(page):
    m = re.match(r"---\n(.*?)\n---\n", page, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    return fm, (page[m.end():] if m else page)


def lab_blocks(body):
    out = []
    for m in re.finditer(r"```lab\n(.*?)```", body, re.S):
        cmds, cur = [], None
        for line in m.group(1).splitlines():
            if line.startswith("$ "):
                cur = [line[2:], []]
                cmds.append(cur)
            elif cur is not None:
                cur[1].append(line)
        out.append([(c, "\n".join(e).rstrip()) for c, e in cmds])
    return out


def allowed(cmd, cfg):
    labs = cfg["labs"]
    s = re.sub(r"'[^']*'|\"[^\"]*\"", "''", cmd)           # ignore quoted text (programs contain > and ;)
    if re.search(labs["deny_regex"], s):
        return False
    for part in s.split("|"):
        w = part.strip().split()
        if not w or w[0] not in labs["allow"]:
            return False
    return True


def _run(cmd, cwd, cfg):
    return subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True, timeout=cfg["labs"]["timeout_seconds"], env=cfg["labs"]["env"])


def fill_lab(page, data, cfg):
    """Write the real output under every `$ cmd` in lab blocks. Returns (page, problems)."""
    problems = []
    with tempfile.TemporaryDirectory() as td:
        if data:
            for f in Path(data).iterdir():
                if f.is_file():
                    shutil.copy(f, td)

        def one(m):
            out_lines = []
            for line in m.group(1).splitlines():
                if line.startswith("$ "):
                    cmd = line[2:]
                    out_lines.append(line)
                    if not allowed(cmd, cfg):
                        problems.append((cmd, "command not allowed"))
                        continue
                    try:
                        p = _run(cmd, td, cfg)
                    except subprocess.TimeoutExpired:
                        problems.append((cmd, "timeout"))
                        continue
                    if p.returncode != 0 or not p.stdout.strip():
                        problems.append((cmd, f"exit {p.returncode}" + (", empty output" if not p.stdout.strip() else "")))
                    out_lines.extend(p.stdout.rstrip().splitlines())
            return "```lab\n" + "\n".join(out_lines) + "\n```"
        page = re.sub(r"```lab\n(.*?)```", one, page, flags=re.S)
    return page, problems


def run_lab(blocks, data, cfg):
    results = []
    with tempfile.TemporaryDirectory() as td:
        if data:
            for f in Path(data).iterdir():
                if f.is_file():
                    shutil.copy(f, td)
        for b in blocks:
            for cmd, want in b:
                if not allowed(cmd, cfg):
                    results.append((cmd, False, "command not allowed in the sandbox"))
                    continue
                try:
                    got = _run(cmd, td, cfg).stdout.rstrip()
                except subprocess.TimeoutExpired:
                    results.append((cmd, False, "timeout"))
                    continue
                g, w = [x.rstrip() for x in got.splitlines()], [x.rstrip() for x in want.splitlines()]
                results.append((cmd, g == w, "" if g == w else f"expected {w[:3]}... got {g[:3]}..."))
    return results


def shingles(text, n=8):
    w = norm(strip_code(text)).split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}, w


def copy_fraction(text, reference_text, n=8):
    ref, _ = shingles(reference_text, n)
    _, w = shingles(text, n)
    runs = max(len(w) - n + 1, 1)
    return sum(1 for i in range(len(w) - n + 1) if " ".join(w[i:i + n]) in ref) / runs
