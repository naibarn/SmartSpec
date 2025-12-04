#!/bin/bash
# SmartSpec Sync Script (Standalone)
# Use this to manually sync workflows to all platforms

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

echo -e "${BLUE}🔄 SmartSpec Sync Tool${NC}"
echo "====================="
echo ""

# Check if SmartSpec is installed
if [ ! -d "$SMARTSPEC_DIR" ]; then
    echo -e "${RED}❌ Error: SmartSpec is not installed${NC}"
    echo "Run 'install.sh' first"
    exit 1
fi

# Check if config exists
if [ ! -f "$SMARTSPEC_DIR/config.json" ]; then
    echo -e "${RED}❌ Error: SmartSpec configuration not found${NC}"
    exit 1
fi

# Read config
PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')
USE_SYMLINKS=$(grep -o '"use_symlinks":\s*[^,}]*' "$SMARTSPEC_DIR/config.json" | grep -o '[^:]*$' | tr -d ' ' | tr -d '\n')

# Check if using symlinks
if [ "$USE_SYMLINKS" = "true" ]; then
    echo -e "${YELLOW}⚠️  You're using symlinks - sync is automatic${NC}"
    echo "No manual sync needed!"
    exit 0
fi

# Sync to each platform
echo "Syncing workflows to platforms..."
echo ""

SYNCED=0
FAILED=0

for platform in $PLATFORMS; do
    case $platform in
        kilocode) 
            TARGET_DIR=".kilocode/workflows"
            PLATFORM_NAME="Kilo Code"
            ;;
        roo) 
            TARGET_DIR=".roo/commands"
            PLATFORM_NAME="Roo Code"
            ;;
        claude) 
            TARGET_DIR=".claude/commands"
            PLATFORM_NAME="Claude Code"
            ;;
    esac
    
    # Check if target exists
    if [ ! -d "$(dirname "$TARGET_DIR")" ]; then
        echo -e "  ${YELLOW}⚠️  $PLATFORM_NAME directory not found - skipping${NC}"
        continue
    fi
    
    # Sync
    if command -v rsync &> /dev/null; then
        rsync -a --delete "$WORKFLOWS_DIR/" "$TARGET_DIR/"
    else
        rm -rf "$TARGET_DIR"
        cp -r "$WORKFLOWS_DIR" "$TARGET_DIR"
    fi
    
    echo -e "  ${GREEN}✅ $PLATFORM_NAME synced${NC}"
    SYNCED=$((SYNCED + 1))
done

echo ""
if [ $SYNCED -gt 0 ]; then
    echo -e "${GREEN}✅ Sync complete - $SYNCED platform(s) updated${NC}"
else
    echo -e "${YELLOW}⚠️  No platforms synced${NC}"
fi
