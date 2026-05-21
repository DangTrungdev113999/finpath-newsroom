#!/bin/bash
# Scan lib/, lib/stages/, worker/ and generate features-map.md
# Output: docs/wiki/features-map.md

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../../../.."
WIKI_DIR="$ROOT_DIR/docs/wiki"
OUTPUT="$WIKI_DIR/features-map.md"

mkdir -p "$WIKI_DIR"

echo "# Features Map" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "Auto-generated feature index. Run \`bash .claude/skills/guide/scripts/scan-all.sh\` to refresh." >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Scan lib/ modules
echo "## Lib Modules (\`lib/\`)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Module | Description |" >> "$OUTPUT"
echo "|--------|-------------|" >> "$OUTPUT"

for file in "$ROOT_DIR"/lib/*.py; do
  [ ! -f "$file" ] && continue
  [ "$(basename "$file")" = "__init__.py" ] && continue

  name=$(basename "$file" .py)
  # Extract first line of docstring if exists
  desc=$(grep -m1 '"""' "$file" | sed 's/"""//g' | cut -c1-80)
  [ -z "$desc" ] && desc="-"

  echo "| \`$name\` | $desc |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"

# Scan lib/stages/ modules
echo "## Pipeline Stages (\`lib/stages/\`)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Stage | Description |" >> "$OUTPUT"
echo "|-------|-------------|" >> "$OUTPUT"

if [ -d "$ROOT_DIR/lib/stages" ]; then
  for file in "$ROOT_DIR"/lib/stages/*.py; do
    [ ! -f "$file" ] && continue
    [ "$(basename "$file")" = "__init__.py" ] && continue

    name=$(basename "$file" .py)
    desc=$(grep -m1 '"""' "$file" | sed 's/"""//g' | cut -c1-80)
    [ -z "$desc" ] && desc="-"

    echo "| \`$name\` | $desc |" >> "$OUTPUT"
  done
fi

echo "" >> "$OUTPUT"

# Scan worker/
echo "## Workers (\`worker/\`)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Worker | Description |" >> "$OUTPUT"
echo "|--------|-------------|" >> "$OUTPUT"

if [ -d "$ROOT_DIR/worker" ]; then
  for file in "$ROOT_DIR"/worker/*.ts "$ROOT_DIR"/worker/*.js; do
    [ ! -f "$file" ] && continue

    name=$(basename "$file")
    # Try to extract first comment
    desc=$(grep -m1 '//' "$file" | sed 's|//||' | cut -c1-80)
    [ -z "$desc" ] && desc="-"

    echo "| \`$name\` | $desc |" >> "$OUTPUT"
  done
fi

echo "" >> "$OUTPUT"

# List KB domains
echo "## Knowledge Base Domains (\`kb/\`)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Domain | Files | Description |" >> "$OUTPUT"
echo "|--------|-------|-------------|" >> "$OUTPUT"

for dir in "$ROOT_DIR"/kb/*/; do
  [ ! -d "$dir" ] && continue

  domain=$(basename "$dir")
  count=$(find "$dir" -name "*.md" 2>/dev/null | wc -l)

  case "$domain" in
    bank) desc="27 mã ngân hàng (Big4 + tư nhân + hợp tác xã)" ;;
    ck) desc="30 mã chứng khoán (HOSE/HNX/UPCOM)" ;;
    bds) desc="BĐS dân cư (VHM/NVL/KDH/DXG)" ;;
    oil-gas) desc="10 mã dầu khí + phân bón" ;;
    *) desc="-" ;;
  esac

  echo "| \`$domain\` | $count files | $desc |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "Generated: $OUTPUT"
