#!/bin/bash
# SmartSpec Uninstaller
# Removes the project-local .smartspec directory
# and removes SmartSpec workflows from installed platforms.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"

KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_CLI_DIR="$HOME/.gemini/commands"

echo -e "${YELLOW}🗑️  SmartSpec Uninstaller${NC}"
echo "========================"
echo ""

if [ ! -d "$SMARTSPEC_DIR" ]; then
    echo -e "${RED}❌ SmartSpec is not installed in this project${NC}"
    exit 1
fi

if [ -f "$SMARTSPEC_DIR/config.json" ]; then
    PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')
else
    PLATFORMS="kilocode roo claude antigravity gemini-cli"
fi

echo "This will remove:"
echo "  - $SMARTSPEC_DIR/ directory"
echo "  - SmartSpec workflows from configured platforms"
echo ""

read -p "Are you sure? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing SmartSpec..."

for platform in $PLATFORMS; do
    case $platform in
        kilocode) TARGET_DIR="$KILOCODE_DIR" ;;
        roo) TARGET_DIR="$ROO_DIR" ;;
        claude) TARGET_DIR="$CLAUDE_DIR" ;;
        antigravity) TARGET_DIR="$ANTIGRAVITY_DIR" ;;
        gemini-cli) TARGET_DIR="$GEMINI_CLI_DIR" ;;
        *) continue ;;
    esac

    if [ -d "$TARGET_DIR" ]; then
        rm -f "$TARGET_DIR"/smartspec_*.md 2>/dev/null || true
        rm -f "$TARGET_DIR"/smartspec_*.toml 2>/dev/null || true
        echo -e "  ${GREEN}✅ Removed SmartSpec workflows from $platform${NC}"
    fi
done

rm -rf "$SMARTSPEC_DIR"
echo -e "  ${GREEN}✅ Removed $SMARTSPEC_DIR${NC}"

if [ -f ".git/hooks/post-merge" ]; then
    if grep -q "Auto-sync SmartSpec" ".git/hooks/post-merge" 2>/dev/null; then
        rm -f ".git/hooks/post-merge"
        echo -e "  ${GREEN}✅ Removed git hook${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ SmartSpec uninstalled successfully${NC}"
