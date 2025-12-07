#!/bin/bash
# SmartSpec Sync Script (Standalone)
# Version: 5.2 (centralization-compatible)
# Master source of workflows: .smartspec/workflows/
#
# This script syncs SmartSpec workflows to platform-specific folders
# in your home directory.

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"
CONFIG_PATH="$SMARTSPEC_DIR/config.json"

echo -e "${BLUE}🔄 SmartSpec Sync Tool${NC}"
echo "====================="
echo ""

if [ ! -d "$SMARTSPEC_DIR" ]; then
  echo -e "${RED}❌ SmartSpec is not installed in this project.${NC}"
  echo "Run install.sh first."
  exit 1
fi

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo -e "${RED}❌ Master workflows directory not found:${NC} $WORKFLOWS_DIR"
  exit 1
fi

if [ ! -f "$CONFIG_PATH" ]; then
  echo -e "${RED}❌ SmartSpec configuration not found:${NC} $CONFIG_PATH"
  echo "Run install.sh to create config.json."
  exit 1
fi

# Parse platforms from config.json without requiring jq
PLATFORMS_RAW=$(grep -o '"platforms"[[:space:]]*:[[:space:]]*\[[^]]*\]' "$CONFIG_PATH" | head -n1 || true)
PLATFORMS=$(echo "$PLATFORMS_RAW" | sed -E 's/.*\[(.*)\].*/\1/' | tr -d '" ' | tr ',' ' ')
USE_SYMLINKS=$(grep -o '"use_symlinks"[[:space:]]*:[[:space:]]*[a-zA-Z]*' "$CONFIG_PATH" | head -n1 | sed -E 's/.*:[[:space:]]*//')

if [ "$USE_SYMLINKS" = "true" ]; then
  echo "You're using symlinks - manual sync is not required."
  exit 0
fi

if [ -z "$PLATFORMS" ]; then
  echo -e "${YELLOW}⚠️  No platforms configured in config.json.${NC}"
  exit 0
fi

# Platform directories (home-based defaults)
KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_DIR="$HOME/.gemini/commands"

convert_md_to_toml() {
  local md="$1"
  local toml="$2"

  local desc=""
  desc=$(awk 'NR<=40 && $0 ~ /^description:[[:space:]]*/ {sub(/^description:[[:space:]]*/,""); print; exit}' "$md" 2>/dev/null || true)

  if [ -z "$desc" ]; then
    desc=$(grep -m1 '^# ' "$md" 2>/dev/null | sed 's/^# //' || true)
  fi

  if [ -z "$desc" ]; then
    local base
    base="$(basename "$md" .md)"
    desc="SmartSpec workflow: ${base//_/ }"
  fi

  {
    echo "description = \"${desc//\"/\\\"}\""
    echo ""
    echo 'prompt = """'
    # Strip YAML frontmatter if present
    awk '
      BEGIN{fm=0;dash=0}
      NR==1 && $0=="---" {fm=1;dash=1;next}
      fm==1 && $0=="---" {dash++; if(dash==2){fm=2; next}}
      fm==1 {next}
      {print}
    ' "$md"
    echo '"""'
  } > "$toml"
}

echo "Syncing workflows to platforms..."
echo ""

MD_FILES=()
while IFS= read -r -d '' f; do
  MD_FILES+=("$f")
done < <(find "$WORKFLOWS_DIR" -maxdepth 1 -type f -name "smartspec_*.md" -print0)

SYNCED=0

for platform in $PLATFORMS; do
  case "$platform" in
    kilocode)
      TARGET_DIR="$KILOCODE_DIR"
      PLATFORM_NAME="Kilo Code"
      ;;
    roo)
      TARGET_DIR="$ROO_DIR"
      PLATFORM_NAME="Roo Code"
      ;;
    claude)
      TARGET_DIR="$CLAUDE_DIR"
      PLATFORM_NAME="Claude Code"
      ;;
    antigravity)
      TARGET_DIR="$ANTIGRAVITY_DIR"
      PLATFORM_NAME="Google Antigravity"
      ;;
    gemini-cli)
      TARGET_DIR="$GEMINI_DIR"
      PLATFORM_NAME="Gemini CLI"
      ;;
    *)
      echo -e "  ${YELLOW}⚠️  Unknown platform: $platform - skipping${NC}"
      continue
      ;;
  esac

  mkdir -p "$TARGET_DIR"

  if [ "$platform" = "gemini-cli" ]; then
    echo -e "  ${BLUE}🔄 $PLATFORM_NAME: Converting Markdown workflows to TOML...${NC}"
    for md in "${MD_FILES[@]}"; do
      base="$(basename "$md" .md)"
      convert_md_to_toml "$md" "$TARGET_DIR/$base.toml"
    done
    echo -e "  ${GREEN}✅ $PLATFORM_NAME synced (TOML)${NC}"
    SYNCED=$((SYNCED + 1))
    continue
  fi

  # Replace only SmartSpec files to avoid deleting user files
  rm -f "$TARGET_DIR"/smartspec_*.md 2>/dev/null || true
  for md in "${MD_FILES[@]}"; do
    cp "$md" "$TARGET_DIR/"
  done

  echo -e "  ${GREEN}✅ $PLATFORM_NAME synced${NC}"
  SYNCED=$((SYNCED + 1))
done

echo ""
if [ "$SYNCED" -gt 0 ]; then
  echo -e "${GREEN}✅ Sync complete - $SYNCED platform(s) updated${NC}"
else
  echo -e "${YELLOW}⚠️  No platforms synced${NC}"
fi
