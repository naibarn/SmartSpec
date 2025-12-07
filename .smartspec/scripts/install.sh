#!/bin/bash
# SmartSpec Multi-Platform Installer
# Version: 5.2
# Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI
#
# Master source of workflows: .smartspec/workflows/
# This installer downloads the SmartSpec framework into .smartspec/
# then copies workflows to each platform-specific command directory.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SMARTSPEC_REPO="https://github.com/naibarn/SmartSpec.git"
SMARTSPEC_VERSION="v5.2"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories (default to home-based tool folders)
KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_CLI_DIR="$HOME/.gemini/commands"

echo -e "${BLUE}🚀 SmartSpec Multi-Platform Installer${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if already installed
UPDATE_MODE=false
if [ -d "$SMARTSPEC_DIR" ]; then
    UPDATE_MODE=true
    echo -e "${BLUE}🔄 SmartSpec is already installed${NC}"
    echo -e "${BLUE}📦 Updating to latest version...${NC}"
    echo ""

    # Backup custom workflows (if any)
    if [ -d "$WORKFLOWS_DIR" ]; then
        echo "💾 Backing up existing workflows..."
        cp -r "$WORKFLOWS_DIR" "${WORKFLOWS_DIR}.backup"
        echo -e "  ${GREEN}✅ Backup created${NC}"
    fi

    # Remove old installation (but keep backup)
    echo "🗑️  Removing old installation..."
    rm -rf "$SMARTSPEC_DIR"
    echo -e "  ${GREEN}✅ Old installation removed${NC}"
    echo ""
fi

# Step 1: Download SmartSpec framework (.smartspec/*)
echo "📥 Downloading SmartSpec workflows and knowledge base..."
if command -v git &> /dev/null; then
    # Use git sparse checkout to pull only .smartspec from the SmartSpec repository.
    mkdir -p "$SMARTSPEC_DIR"
    cd "$SMARTSPEC_DIR"

    git init -q
    git remote add origin "$SMARTSPEC_REPO"
    git config core.sparseCheckout true
    echo ".smartspec/" >> .git/info/sparse-checkout

    git pull -q origin main

    # Flatten nested .smartspec directory created by sparse checkout
    if [ -d ".smartspec" ]; then
        find .smartspec -mindepth 1 -maxdepth 1 -exec mv {} . \;
    fi

    # Cleanup git metadata + nested folder
    rm -rf .smartspec .git

    cd ..

    echo -e "${GREEN}✅ Downloaded SmartSpec via git${NC}"
else
    # Download as zip
    if command -v curl &> /dev/null; then
        curl -sL "$SMARTSPEC_REPO/archive/refs/heads/main.zip" -o smartspec.zip
    elif command -v wget &> /dev/null; then
        wget -q "$SMARTSPEC_REPO/archive/refs/heads/main.zip" -O smartspec.zip
    else
        echo -e "${RED}❌ Error: Neither git, curl, nor wget is available${NC}"
        exit 1
    fi

    unzip -q smartspec.zip

    mkdir -p "$SMARTSPEC_DIR"
    if [ -d "SmartSpec-main/.smartspec" ]; then
        cp -r SmartSpec-main/.smartspec/* "$SMARTSPEC_DIR/"
    else
        echo -e "${RED}❌ Error: .smartspec folder not found in the downloaded archive${NC}"
        rm -rf SmartSpec-main smartspec.zip
        exit 1
    fi

    rm -rf SmartSpec-main smartspec.zip

    echo -e "${GREEN}✅ Downloaded SmartSpec via zip${NC}"
fi

# Validate that master workflows exist
if [ ! -d "$WORKFLOWS_DIR" ]; then
    echo -e "${RED}❌ Error: Master workflows directory not found: $WORKFLOWS_DIR${NC}"
    echo "This version expects workflows to live under .smartspec/workflows in the SmartSpec repository."
    exit 1
fi

# Step 2: Detect platforms
echo ""
echo "🔍 Detecting platforms (home-based)..."

DETECTED_PLATFORMS=()

if [ -d "$HOME/.kilocode" ]; then
    DETECTED_PLATFORMS+=("kilocode")
    echo -e "  ${GREEN}✅ Kilo Code detected${NC}"
fi

if [ -d "$HOME/.roo" ]; then
    DETECTED_PLATFORMS+=("roo")
    echo -e "  ${GREEN}✅ Roo Code detected${NC}"
fi

if [ -d "$HOME/.claude" ]; then
    DETECTED_PLATFORMS+=("claude")
    echo -e "  ${GREEN}✅ Claude Code detected${NC}"
fi

if [ -d "$HOME/.agent" ]; then
    DETECTED_PLATFORMS+=("antigravity")
    echo -e "  ${GREEN}✅ Google Antigravity detected${NC}"
fi

if [ -d "$HOME/.gemini" ]; then
    DETECTED_PLATFORMS+=("gemini-cli")
    echo -e "  ${GREEN}✅ Gemini CLI detected${NC}"
fi

if [ ${#DETECTED_PLATFORMS[@]} -eq 0 ]; then
    echo -e "  ${YELLOW}⚠️  No supported platforms detected in your home directory${NC}"
fi

# Always ask user which platforms to install
echo ""
echo "Which platforms do you want to install/update?"
echo "  1) Kilo Code"
echo "  2) Roo Code"
echo "  3) Claude Code"
echo "  4) Google Antigravity"
echo "  5) Gemini CLI"
echo "  6) All of the above"

# Read input robustly
if [ -t 0 ]; then
    read -p "Enter choice [1-6] (default: 1): " choice
else
    read choice 2>/dev/null || choice=""
    if [ -z "$choice" ]; then
        read -p "Enter choice [1-6] (default: 1): " choice < /dev/tty 2>/dev/null || choice=""
    fi
fi

if [ -z "$choice" ]; then
    choice=1
    echo "Using default: $choice"
fi

case $choice in
    1) PLATFORMS=("kilocode") ;;
    2) PLATFORMS=("roo") ;;
    3) PLATFORMS=("claude") ;;
    4) PLATFORMS=("antigravity") ;;
    5) PLATFORMS=("gemini-cli") ;;
    6) PLATFORMS=("kilocode" "roo" "claude" "antigravity" "gemini-cli") ;;
    *) echo -e "${RED}Invalid choice: $choice${NC}"; exit 1 ;;
esac

# Step 3/4: Install workflows for each platform
echo ""
echo "📦 Installing SmartSpec workflows..."

for platform in "${PLATFORMS[@]}"; do
    REQUIRES_TOML_CONVERSION=false

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
            REQUIRES_TOML_CONVERSION=true
            ;;
    esac

    # If the tool parent folder doesn't exist, create it only when user explicitly selected it.
    mkdir -p "$(dirname "$TARGET_DIR")"
    mkdir -p "$TARGET_DIR"

    # Gemini CLI: convert Markdown workflows to TOML
    if [ "$REQUIRES_TOML_CONVERSION" = true ]; then
        echo -e "  ${BLUE}🔄 $PLATFORM_NAME: Converting Markdown workflows to TOML...${NC}"

        EXISTING_TOML=()
        if ls "$TARGET_DIR"/smartspec_*.toml >/dev/null 2>&1; then
            while IFS= read -r file; do
                EXISTING_TOML+=("$(basename "$file")")
            done < <(ls "$TARGET_DIR"/smartspec_*.toml 2>/dev/null)
        fi

        if [ ${#EXISTING_TOML[@]} -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Found ${#EXISTING_TOML[@]} existing SmartSpec TOML workflow(s)${NC}"
            echo ""
            echo "  How do you want to proceed?"
            echo "    1) Overwrite all (recommended for updates)"
            echo "    2) Skip all (keep existing versions)"
            echo "    3) Cancel installation"

            if [ -t 0 ]; then
                read -p "  Enter choice [1-3] (default: 1): " overwrite_choice
            else
                read -p "  Enter choice [1-3] (default: 1): " overwrite_choice < /dev/tty 2>/dev/null || overwrite_choice=""
            fi

            [ -z "$overwrite_choice" ] && overwrite_choice=1

            case $overwrite_choice in
                1)
                    BACKUP_DIR="${TARGET_DIR}.smartspec.backup.$(date +%Y%m%d_%H%M%S)"
                    mkdir -p "$BACKUP_DIR"
                    for file in "${EXISTING_TOML[@]}"; do
                        cp "$TARGET_DIR/$file" "$BACKUP_DIR/" 2>/dev/null || true
                    done
                    echo -e "  ${GREEN}💾 Backed up existing SmartSpec TOML workflows to $(basename "$BACKUP_DIR")${NC}"
                    ;;
                2)
                    echo -e "  ${BLUE}⏭️  Skipping $PLATFORM_NAME (keeping existing versions)${NC}"
                    continue
                    ;;
                3)
                    echo -e "${RED}❌ Installation cancelled${NC}"
                    exit 0
                    ;;
                *)
                    echo -e "  ${RED}Invalid choice. Skipping $PLATFORM_NAME${NC}"
                    continue
                    ;;
            esac
        fi

        CONVERTED=0
        for md_file in "$WORKFLOWS_DIR"/smartspec_*.md; do
            [ -f "$md_file" ] || continue

            filename=$(basename "$md_file" .md)
            toml_file="$TARGET_DIR/${filename}.toml"

            # Try to extract description from frontmatter first, then from # title
            description=$(grep -m 1 '^description:' "$md_file" | sed 's/^description: *//')
            if [ -z "$description" ]; then
                description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //')
            fi
            [ -z "$description" ] && description="SmartSpec workflow: ${filename//_/ }"

            # Extract content after frontmatter as prompt
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

        echo -e "  ${GREEN}✅ $PLATFORM_NAME: $CONVERTED workflows converted and installed${NC}"
        continue
    fi

    # Markdown platforms: merge logic (safe overwrite options)
    EXISTING_SMARTSPEC=()
    if ls "$TARGET_DIR"/smartspec_*.md >/dev/null 2>&1; then
        while IFS= read -r file; do
            EXISTING_SMARTSPEC+=("$(basename "$file")")
        done < <(ls "$TARGET_DIR"/smartspec_*.md 2>/dev/null)
    fi

    if [ ${#EXISTING_SMARTSPEC[@]} -gt 0 ]; then
        echo -e "  ${YELLOW}⚠️  Found ${#EXISTING_SMARTSPEC[@]} existing SmartSpec workflow(s) for $PLATFORM_NAME${NC}"
        echo ""
        echo "  How do you want to proceed?"
        echo "    1) Overwrite all (recommended for updates)"
        echo "    2) Skip existing, copy only new"
        echo "    3) Cancel this platform"

        if [ -t 0 ]; then
            read -p "  Enter choice [1-3] (default: 1): " overwrite_choice
        else
            read -p "  Enter choice [1-3] (default: 1): " overwrite_choice < /dev/tty 2>/dev/null || overwrite_choice=""
        fi

        [ -z "$overwrite_choice" ] && overwrite_choice=1

        case $overwrite_choice in
            1)
                BACKUP_DIR="${TARGET_DIR}.smartspec.backup.$(date +%Y%m%d_%H%M%S)"
                mkdir -p "$BACKUP_DIR"
                for file in "${EXISTING_SMARTSPEC[@]}"; do
                    cp "$TARGET_DIR/$file" "$BACKUP_DIR/" 2>/dev/null || true
                done
                echo -e "  ${GREEN}💾 Backed up existing SmartSpec workflows to $(basename "$BACKUP_DIR")${NC}"

                cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
                echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows updated${NC}"
                ;;
            2)
                COPIED=0
                for file in "$WORKFLOWS_DIR"/smartspec_*.md; do
                    filename=$(basename "$file")
                    if [ ! -f "$TARGET_DIR/$filename" ]; then
                        cp "$file" "$TARGET_DIR/"
                        COPIED=$((COPIED + 1))
                    fi
                done
                echo -e "  ${GREEN}✅ $PLATFORM_NAME: $COPIED new workflow(s) added${NC}"
                ;;
            3)
                echo -e "  ${YELLOW}❌ Installation cancelled for $PLATFORM_NAME${NC}"
                continue
                ;;
            *)
                echo -e "  ${RED}Invalid choice, skipping $PLATFORM_NAME${NC}"
                continue
                ;;
        esac
    else
        cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows installed${NC}"
    fi
done

# Step 5: Save configuration
echo ""
echo "💾 Saving configuration..."

cat > "$SMARTSPEC_DIR/config.json" <<EOF
{
  "version": "$SMARTSPEC_VERSION",
  "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "platforms": [$(printf '"%s"' "${PLATFORMS[@]}" | paste -sd ',' -)],
  "use_symlinks": false,
  "repo": "$SMARTSPEC_REPO"
}
EOF

echo "$SMARTSPEC_VERSION" > "$SMARTSPEC_DIR/version.txt"
echo -e "${GREEN}✅ Configuration saved${NC}"

# Step 6: Create sync script (project-local helper)
cat > "$SMARTSPEC_DIR/sync.sh" <<'SYNCEOF'
#!/bin/bash
# SmartSpec Sync Script (Project Helper)
# Syncs .smartspec/workflows to all configured platforms.

set -e

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_CLI_DIR="$HOME/.gemini/commands"

if [ ! -f "$SMARTSPEC_DIR/config.json" ]; then
    echo -e "${RED}Error: SmartSpec not installed${NC}"
    exit 1
fi

PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')

echo -e "${BLUE}🔄 Syncing SmartSpec workflows...${NC}"

for platform in $PLATFORMS; do
    case $platform in
        kilocode) TARGET_DIR="$KILOCODE_DIR" ;;
        roo) TARGET_DIR="$ROO_DIR" ;;
        claude) TARGET_DIR="$CLAUDE_DIR" ;;
        antigravity) TARGET_DIR="$ANTIGRAVITY_DIR" ;;
        gemini-cli)
            TARGET_DIR="$GEMINI_CLI_DIR"
            mkdir -p "$(dirname "$TARGET_DIR")"
            mkdir -p "$TARGET_DIR"

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

            echo -e "  ${GREEN}✅ gemini-cli synced ($CONVERTED workflows converted to TOML)${NC}"
            continue
            ;;
        *)
            echo -e "  ${YELLOW}⚠️  Unknown platform: $platform - skipping${NC}"
            continue
            ;;
    esac

    mkdir -p "$(dirname "$TARGET_DIR")"
    mkdir -p "$TARGET_DIR"
    cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
    echo -e "  ${GREEN}✅ $platform synced${NC}"
done

echo -e "${GREEN}✅ Sync complete${NC}"
SYNCEOF

chmod +x "$SMARTSPEC_DIR/sync.sh"
echo -e "${GREEN}✅ Sync script created${NC}"

# Step 7: Initial sync
echo ""
echo -e "${BLUE}🔄 Syncing workflows to platform directories...${NC}"
"$SMARTSPEC_DIR/sync.sh"

# Step 8: Create git hook (optional)
if [ -d ".git" ]; then
    mkdir -p ".git/hooks"
    cat > ".git/hooks/post-merge" <<'HOOKEOF'
#!/bin/bash
# Auto-sync SmartSpec after git pull

if [ -f ".smartspec/sync.sh" ]; then
    echo "🔄 Auto-syncing SmartSpec..."
    .smartspec/sync.sh
fi
HOOKEOF
    chmod +x ".git/hooks/post-merge"
    echo -e "${GREEN}✅ Git hook installed (auto-sync on pull)${NC}"
fi

# Success message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ SmartSpec installed successfully!  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "📍 Installation details:"
echo "  - Version: $SMARTSPEC_VERSION"
echo "  - Location: $SMARTSPEC_DIR"
echo "  - Platforms: ${PLATFORMS[*]}"
echo ""
echo -e "${YELLOW}📝 Note:${NC} Always edit master workflows in ${SMARTSPEC_DIR}/workflows/"
echo "   Run '.smartspec/sync.sh' to manually update platform copies."
echo ""
