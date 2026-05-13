#!/usr/bin/env bash
# Re-render markdown for batches touched by Gemini backfill.
# Reads /tmp/backfill-gemini-summary.json (written by scripts/backfill_gemini.py).
# Each batch is re-rendered via lib.render_compare_feed (idempotent).

set -euo pipefail
cd "$(dirname "$0")/.."

SUMMARY=/tmp/backfill-gemini-summary.json
if [ ! -f "$SUMMARY" ]; then
  echo "[rerender] no $SUMMARY — run scripts/backfill_gemini.py first"
  exit 1
fi

BATCHES=$(uv run python -c "
import json
with open('$SUMMARY') as f:
    s = json.load(f)
for b in s['batches_to_rerender']:
    print(b)
")

if [ -z "$BATCHES" ]; then
  echo "[rerender] no batches to re-render (all skipped/failed)"
  exit 0
fi

echo "[rerender] batches:"
echo "$BATCHES" | sed 's/^/  /'
echo ""

while IFS= read -r batch; do
  echo "[rerender] $batch"
  uv run python -m lib.render_compare_feed "$batch" --output-dir output/compare-feed 2>&1 | tail -3
  echo ""
done <<< "$BATCHES"

echo "[rerender] done"
