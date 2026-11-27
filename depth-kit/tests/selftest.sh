#!/usr/bin/env bash
# Self-test for the kit. Offline checks run without any model. Pass a model URL to also run the live checks.
#   bash tests/selftest.sh                         # offline checks (needs bash, python3, coreutils, awk)
#   bash tests/selftest.sh http://127.0.0.1:11434 qwen3:8b   # adds one generated unit and the critic planted-defect control
set -u
KIT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$KIT"
URL=${1:-}; MODEL=${2:-}
W=$(mktemp -d); fail=0
ok() { echo "[PASS] $1"; }
bad() { echo "[FAIL] $1"; fail=1; }

python3 example/data/make_sample.py "$W/data" >/dev/null && ok "sample data generated" || bad "sample data"
python3 tools/gate.py example/seed/K-GEN01 --data "$W/data" > "$W/gate.txt" 2>&1 && ok "gate passes the reference topic ($(grep -o 'stats:.*' "$W/gate.txt" | head -1))" || { bad "gate on the reference topic"; tail -5 "$W/gate.txt"; }

python3 tools/make_pack.py example/spec/K-LOG01.json > "$W/pack.txt" 2>/dev/null && [ -s "$W/pack.txt" ] && ok "source pack built ($(wc -w < "$W/pack.txt") words)" || bad "pack builder"
python3 tools/retrieve.py "$W/pack.txt" "count lines matching a pattern" -k 2 | grep -q . && ok "retrieval returns passages" || bad "retrieval"

python3 - <<'PY' && ok "generator helpers: skeleton keeps structure, drops prose; unit checks flag copying" || bad "generator helpers"
import sys
sys.path.insert(0, "tools")
import gen, kitconfig, gatelib as L
cfg = kitconfig.load()
core, ext = gen.seed_units("example/seed/K-GEN01")
assert set(core) == set(range(1, 16)) and set(ext) == {6, 7, 8, 9}, (sorted(core), sorted(ext))
sk = gen.skeleton(core[3])
assert len(sk) < len(core[3]) and sk.startswith("## 3."), "skeleton"
fails = gen.unit_checks(core[3], "## 3. Intuition", [], core[3], cfg)
assert any("copies" in f for f in fails), fails       # the seed copies itself: the originality check must fire
PY

mkdir -p "$W/new" && python3 tools/new_topic.py --spec example/spec/K-LOG01.json --out "$W/new" >/dev/null && [ "$(ls "$W/new"/*.md | wc -l)" -ge 10 ] && ok "skeleton created (nine files plus SLOTS.md)" || bad "skeleton"
python3 tools/gate.py "$W/new" --data "$W/data" > "$W/gate-skel.txt" 2>&1; grep -q "GATE FAILED" "$W/gate-skel.txt" && ok "gate rejects an empty skeleton" || bad "gate accepted a skeleton"
python3 tools/plant_defects.py example/seed/K-GEN01 "$W/planted" | grep -q "planted 6" && ok "six defects planted" || bad "defect planting"

if [ -n "$URL" ]; then
  python3 tools/gen.py --spec example/spec/K-LOG01.json --seed example/seed/K-GEN01 --pack "$W/pack.txt" --out "$W/live" --model "$MODEL" --url "$URL" --best-of 1 --only 3 >/dev/null 2>&1 && [ -s "$W/live/cand-01/provenance.json" ] && ok "live: one unit generated with provenance" || bad "live generation"
  python3 tools/critic_control.py example/seed/K-GEN01 "$W/ctl" --model "$MODEL" --url "$URL" --min-recall 0 >/dev/null 2>&1 && ok "live: critic control ran ($(python3 -c "import json;print('recall',json.load(open('$W/ctl/control.json'))['recall'])"))" || bad "live critic control"
fi
echo; [ $fail = 0 ] && echo "SELFTEST PASSED" || echo "SELFTEST FAILED"; exit $fail
