#!/usr/bin/env bash
# Trial runner (standards section 11): generate N candidate topics, fill lab outputs, gate each, print the pass table.
# usage: tools/trial.sh SPEC SEED_TOPIC_DIR MODEL URL N OUTDIR [BEST_OF]
# The spec names a "data_script" (a Python file that writes the sample data into the directory given as its first argument).
set -u
SPEC=$1; SEED=$2; MODEL=$3; URL=$4; N=$5; OUT=$6; BO=${7:-3}
HERE="$(cd "$(dirname "$0")" && pwd)"; KIT="$(dirname "$HERE")"
mkdir -p "$OUT"
DATA_SCRIPT=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('data_script',''))" "$SPEC")
DATA="$OUT/data"; python3 "$KIT/$DATA_SCRIPT" "$DATA" >/dev/null
python3 "$HERE/make_pack.py" "$SPEC" > "$OUT/pack.txt"
python3 "$HERE/gen.py" --spec "$SPEC" --seed "$SEED" --pack "$OUT/pack.txt" --out "$OUT" --n "$N" --model "$MODEL" --url "$URL" --best-of "$BO" | tee "$OUT/gen.log"
for d in "$OUT"/cand-*/; do
  b=$(basename "$d")
  python3 "$HERE/gate.py" "$d" --fill --data "$DATA" --pack "$OUT/pack.txt" --seed "$SEED" --spec "$SPEC" --json > "$OUT/$b.gate.json"
done
python3 "$HERE/summary.py" "$OUT"
