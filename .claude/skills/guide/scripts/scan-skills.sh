#!/bin/bash
# Scan .claude/skills/ and generate skills-guide.md
# Output: docs/wiki/skills-guide.md

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../../../.."
WIKI_DIR="$ROOT_DIR/docs/wiki"
OUTPUT="$WIKI_DIR/skills-guide.md"

mkdir -p "$WIKI_DIR"

echo "# Skills Guide" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "Auto-generated from \`.claude/skills/\`. Run \`bash .claude/skills/guide/scripts/scan-all.sh\` to refresh." >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Skill | Description |" >> "$OUTPUT"
echo "|-------|-------------|" >> "$OUTPUT"

total=0

for dir in "$ROOT_DIR"/.claude/skills/*/; do
  [ ! -d "$dir" ] && continue
  skill_file="$dir/SKILL.md"
  [ ! -f "$skill_file" ] && continue
  total=$((total + 1))

  # Extract name and description from YAML frontmatter (between --- lines)
  name=""
  desc=""
  in_frontmatter=false
  while IFS= read -r line; do
    if [ "$line" = "---" ]; then
      if [ "$in_frontmatter" = true ]; then
        break
      fi
      in_frontmatter=true
      continue
    fi
    if [ "$in_frontmatter" = true ]; then
      case "$line" in
        name:*) name=$(echo "$line" | sed 's/^name:[[:space:]]*//');;
        description:*) desc=$(echo "$line" | sed 's/^description:[[:space:]]*//');;
      esac
    fi
  done < "$skill_file"

  # Truncate description to first sentence, max 120 chars
  desc_short=$(echo "$desc" | sed 's/\. .*/\./' | cut -c1-120)

  [ -z "$name" ] && name=$(basename "$dir")
  [ -z "$desc_short" ] && desc_short="-"

  echo "| \`$name\` | $desc_short |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "**Total**: $total skills" >> "$OUTPUT"

echo "Generated: $OUTPUT"
