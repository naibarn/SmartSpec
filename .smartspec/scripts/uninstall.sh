#!/bin/bash
# SmartSpec Uninstaller

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"

echo -e "${YELLOW}🗑️  SmartSpec Uninstaller${NC}"
echo "========================"
echo ""

# Check if installed
if [ ! -d "$SMARTSPEC_DIR" ]; then
    echo -e "${RED}❌ SmartSpec is not installed${NC}"
    exit 1
fi

# Read config
if [ -f "$SMARTSPEC_DIR/config.json" ]; then
    PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')
    USE_SYMLINKS=$(grep -o '"use_symlinks":\s*[^,}]*' "$SMARTSPEC_DIR/config.json" | grep -o '[^:]*$' | tr -d ' ')
else
    PLATFORMS="kilocode roo claude"
    USE_SYMLINKS="false"
fi

echo "This will remove SmartSpec from:"
echo "  - .smartspec/ directory"
for platform in $PLATFORMS; do
    case $platform in
        kilocode) echo "  - .kilocode/workflows/" ;;
        roo) echo "  - .roo/commands/" ;;
        claude) echo "  - .claude/commands/" ;;
    esac
done
echo ""

read -p "Are you sure? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing SmartSpec..."

# Remove from platforms
for platform in $PLATFORMS; do
    case $platform in
        kilocode) TARGET_DIR=".kilocode/workflows" ;;
        roo) TARGET_DIR=".roo/commands" ;;
        claude) TARGET_DIR=".claude/commands" ;;
    esac
    
    if [ -e "$TARGET_DIR" ]; then
        rm -rf "$TARGET_DIR"
        echo -e "  ${GREEN}✅ Removed from $platform${NC}"
    fi
done

# Remove .smartspec directory
if [ -d "$SMARTSPEC_DIR" ]; then
    rm -rf "$SMARTSPEC_DIR"
    echo -e "  ${GREEN}✅ Removed $SMARTSPEC_DIR${NC}"
fi

# Remove git hook
if [ -f ".git/hooks/post-merge" ]; then
    if grep -q "smartspec" ".git/hooks/post-merge"; then
        rm -f ".git/hooks/post-merge"
        echo -e "  ${GREEN}✅ Removed git hook${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ SmartSpec uninstalled successfully${NC}"
