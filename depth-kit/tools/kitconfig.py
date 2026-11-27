"""Config loader shared by every kit tool. Resolution order: --config argument, $DEPTHKIT_CONFIG, <kit>/config/project.json.
Relative paths inside the config are relative to the kit root (the folder that holds config/ and tools/)."""
import json
import os
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def config_path(argv=None):
    argv = sys.argv if argv is None else argv
    for i, a in enumerate(argv):
        if a == "--config" and i + 1 < len(argv):
            return Path(argv[i + 1])
        if a.startswith("--config="):
            return Path(a.split("=", 1)[1])
    return Path(os.environ.get("DEPTHKIT_CONFIG", KIT / "config" / "project.json"))


def load(argv=None):
    p = config_path(argv)
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["_path"] = str(p)
    cfg["_root"] = str(KIT)
    return cfg


def resolve(cfg, rel):
    p = Path(rel)
    return p if p.is_absolute() else Path(cfg["_root"]) / p


def rule_catalog(cfg):
    return json.loads(resolve(cfg, cfg["rules"]["catalog"]).read_text(encoding="utf-8"))


def applicable_rules(cfg):
    """Return {'A': set of ids that apply to page content, 'V': ..., 'P': ...}."""
    cat = rule_catalog(cfg)
    return {k: {int(i) for i, (_, page) in cat[k].items() if page} for k in "AVP"}


def strip_argv(argv, flag):
    """Remove `--config PATH` style flags before a tool's own argparse sees them."""
    out, skip = [], False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == flag:
            skip = True
            continue
        if a.startswith(flag + "="):
            continue
        out.append(a)
    return out
