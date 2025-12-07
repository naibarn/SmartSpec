#!/bin/bash
# SmartSpec Sync Script (Standalone)
# Use this to manually sync workflows to all platforms.

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories (home-based defaults)
KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_CLI_DIR="$HOME/.gemini/commands"

echo -e "${BLUE}🔄 SmartSpec Sync Tool${NC}"
echo "====================="
echo ""

if [ ! -d "$SMARTSPEC_DIR" ]; then
    echo -e "${RED}❌ Error: SmartSpec is not installed${NC}"
    echo "Run 'install.sh' first"
    exit 1
fi

if [ ! -f "$SMARTSPEC_DIR/config.json" ]; then
    echo -e "${RED}❌ Error: SmartSpec configuration not found${NC}"
    exit 1
fi

PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')
USE_SYMLINKS=$(grep -o '"use_symlinks":\s*[^,}]*' "$SMARTSPEC_DIR/config.json" | grep -o '[^:]*$' | tr -d ' ' | tr -d '\n')

if [ "$USE_SYMLINKS" = "true" ]; then
    echo -e "${YELLOW}⚠️  You're using symlinks - sync is automatic${NC}"
    echo "No manual sync needed!"
    exit 0
fi

if [ ! -d "$WORKFLOWS_DIR" ]; then
    echo -e "${RED}❌ Error: Master workflows directory not found: $WORKFLOWS_DIR${NC}"
    exit 1
fi

echo "Syncing workflows to platforms..."
echo ""

SYNCED=0

for platform in $PLATFORMS; do
    case $platform in
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
            TARGET_DIR="$GEMINI_CLI_DIR"
            PLATFORM_NAME="Gemini CLI"
            ;;
        *)
            echo -e "  ${YELLOW}⚠️  Unknown platform '$platform' - skipping${NC}"
            continue
            ;;
    esac

    PARENT_DIR="$(dirname "$TARGET_DIR")"
    if [ ! -d "$PARENT_DIR" ]; then
        echo -e "  ${YELLOW}⚠️  $PLATFORM_NAME not detected at $PARENT_DIR - skipping${NC}"
        continue
    fi

    mkdir -p "$TARGET_DIR"

    if [ "$platform" = "gemini-cli" ]; then
        CONVERTED=0
        for md_file in "$WORKFLOWS_DIR"/smartspec_*.md; do
            [ -f "$md_file" ] || continue
            filename=$(basename "$md_file" .md)
            toml_file="$TARGET_DIR/${filename}.toml"

            description=$(grep -m 1 '^description:' "$md_file" | sed 's/^description: *//')
            if [ -z "$description" ]; then
                description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //')
            fi
            [ -z "$description" ] && description="SmartSpec workflow: ${filename//_/ }"

            frontmatter_end=$(grep -n '^---$' "$md_file" | sed -n '2p' | cut -d: -f1)
            if [ -n "$frontmatter_end" ]; then
                prompt=$(tail -n +$((frontmatter_end + 1)) "$md_file")
            else
                prompt=$(tail -n +2 "$md_file")
            fi

            {
                echo "description = \"$description\""
                echo ""
                echo 'prompt = """'
                echo "$prompt"
                echo '"""'
            } > "$toml_file"

            CONVERTED=$((CONVERTED + 1))
        done

        echo -e "  ${GREEN}✅ $PLATFORM_NAME synced ($CONVERTED workflows converted)${NC}"
        SYNCED=$((SYNCED + 1))
        continue
    fi

    # Markdown platforms sync (avoid deleting non-SmartSpec commands)
    rm -f "$TARGET_DIR"/smartspec_*.md 2>/dev/null || true
    cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true

    echo -e "  ${GREEN}✅ $PLATFORM_NAME synced${NC}"
    SYNCED=$((SYNCED + 1))
done

echo ""
if [ $SYNCED -gt 0 ]; then
    echo -e "${GREEN}✅ Sync complete - $SYNCED platform(s) updated${NC}"
else
    echo -e "${YELLOW}⚠️  No platforms synced${NC}"
fi
