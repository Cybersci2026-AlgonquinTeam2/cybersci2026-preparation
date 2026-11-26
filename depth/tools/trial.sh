#!/usr/bin/env bash
# Trial runner: generate N candidates, fill + gate each, print the acceptance table. Run on the server or in WSL.
# usage: depth/tools/trial.sh SPEC SEED MODEL URL N OUTDIR
set -u
SPEC=$1; SEED=$2; MODEL=$3; URL=$4; N=$5; OUT=$6
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT" && DATA="$OUT/data" && python3 "$HERE/../data/make_sample.py" "$DATA" >/dev/null
python3 "$HERE/make_pack.py" "$SPEC" > "$OUT/pack.txt"
python3 "$HERE/gen.py" --spec "$SPEC" --seed "$SEED" --pack "$OUT/pack.txt" --model "$MODEL" --url "$URL" --n "$N" --out "$OUT" | tee "$OUT/gen.log"
for f in "$OUT"/cand-*.md; do
  python3 "$HERE/gate.py" "$f" --fill --data "$DATA" --pack "$OUT/pack.txt" --json > "${f%.md}.gate.json"
done
python3 "$HERE/summary.py" "$OUT"
