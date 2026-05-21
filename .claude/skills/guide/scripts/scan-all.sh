#!/bin/bash
# Master script: run all scan scripts and update _meta.json
# Usage: bash .claude/skills/guide/scripts/scan-all.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../../../.."
WIKI_DIR="$ROOT_DIR/docs/wiki"

echo "Scanning codebase..."

bash "$SCRIPT_DIR/scan-skills.sh"
bash "$SCRIPT_DIR/scan-features.sh"

# Update _meta.json with timestamps
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$WIKI_DIR/_meta.json" << EOF
{
  "last_scan": "$NOW",
  "files": {
    "skills-guide.md": "$NOW",
    "features-map.md": "$NOW"
  }
}
EOF

echo ""
echo "All scans complete. Wiki updated at $NOW"
echo "Generated files:"
ls -la "$WIKI_DIR"/*.md "$WIKI_DIR/_meta.json" 2>/dev/null
