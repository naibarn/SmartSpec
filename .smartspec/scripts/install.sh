#!/bin/bash
# SmartSpec Multi-Platform Installer
# Version: 5.0
# Supports: Kilo Code, Roo Code, Claude Code

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SMARTSPEC_REPO="https://github.com/naibarn/SmartSpec.git"
SMARTSPEC_VERSION="v5.0"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories
KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"

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

# Step 1: Clone or download workflows and knowledge base
echo "📥 Downloading SmartSpec workflows and knowledge base..."
if command -v git &> /dev/null; then
    # Use git sparse checkout (workflows + knowledge base)
    mkdir -p "$SMARTSPEC_DIR"
    cd "$SMARTSPEC_DIR"
    git init -q
    git remote add origin "$SMARTSPEC_REPO"
    git config core.sparseCheckout true
    echo ".smartspec/" >> .git/info/sparse-checkout
    git pull -q origin main
    # Move all files and directories from .smartspec/ to current directory
    if [ -d ".smartspec" ]; then
        # Use find to move both files and directories, including hidden files
        find .smartspec -mindepth 1 -maxdepth 1 -exec mv {} . \;
    fi
    rm -rf .smartspec .git
    cd ..
    echo -e "${GREEN}✅ Downloaded workflows and knowledge base via git${NC}"
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
    mkdir -p "$WORKFLOWS_DIR"
    mv SmartSpec-main/.kilocode/workflows/* "$WORKFLOWS_DIR/"
    # Copy knowledge base files (examples only, not user files)
    if [ -d "SmartSpec-main/.smartspec" ]; then
        cp -r SmartSpec-main/.smartspec/* "$SMARTSPEC_DIR/"
    fi
    rm -rf SmartSpec-main smartspec.zip
    echo -e "${GREEN}✅ Downloaded workflows and knowledge base via zip${NC}"
fi

# Step 2: Detect platforms
echo ""
echo "🔍 Detecting platforms..."
PLATFORMS=()

if [ -d ".kilocode" ]; then
    PLATFORMS+=("kilocode")
    echo -e "  ${GREEN}✅ Kilo Code detected${NC}"
fi

if [ -d ".roo" ]; then
    PLATFORMS+=("roo")
    echo -e "  ${GREEN}✅ Roo Code detected${NC}"
fi

if [ -d ".claude" ]; then
    PLATFORMS+=("claude")
    echo -e "  ${GREEN}✅ Claude Code detected${NC}"
fi

if [ ${#PLATFORMS[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No platforms detected${NC}"
    echo ""
    echo "Which platforms do you want to install?"
    echo "  1) Kilo Code"
    echo "  2) Roo Code"
    echo "  3) Claude Code"
    echo "  4) All of the above"
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) PLATFORMS=("kilocode") ;;
        2) PLATFORMS=("roo") ;;
        3) PLATFORMS=("claude") ;;
        4) PLATFORMS=("kilocode" "roo" "claude") ;;
        *) echo -e "${RED}Invalid choice${NC}"; exit 1 ;;
    esac
fi

# Step 3: Try symlinks first
echo ""
echo "🔗 Setting up platform integrations..."

USE_SYMLINKS=true

# Test if symlinks work
test_symlink() {
    local test_dir=".smartspec_test"
    mkdir -p "$test_dir"
    if ln -s "$test_dir" "$test_dir/link" 2>/dev/null; then
        rm -rf "$test_dir"
        return 0
    else
        rm -rf "$test_dir"
        return 1
    fi
}

if test_symlink; then
    echo -e "  ${GREEN}✅ Symlinks supported - using symlinks${NC}"
    USE_SYMLINKS=true
else
    echo -e "  ${YELLOW}⚠️  Symlinks not supported - using copies${NC}"
    USE_SYMLINKS=false
fi

# Step 4: Install for each platform
for platform in "${PLATFORMS[@]}"; do
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
    esac
    
    # Create parent directory
    mkdir -p "$(dirname "$TARGET_DIR")"
    
    # Remove existing
    if [ -e "$TARGET_DIR" ]; then
        rm -rf "$TARGET_DIR"
    fi
    
    # Install
    if [ "$USE_SYMLINKS" = true ]; then
        # Create symlink (relative path for portability)
        ln -s "../../$WORKFLOWS_DIR" "$TARGET_DIR"
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: Symlink created${NC}"
    else
        # Copy files
        cp -r "$WORKFLOWS_DIR" "$TARGET_DIR"
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: Files copied${NC}"
    fi
done

# Step 5: Save configuration
echo ""
echo "💾 Saving configuration..."

# Create config.json
cat > "$SMARTSPEC_DIR/config.json" <<EOF
{
  "version": "$SMARTSPEC_VERSION",
  "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "platforms": [$(printf '"%s"' "${PLATFORMS[@]}" | paste -sd ',' -)],
  "use_symlinks": $USE_SYMLINKS,
  "repo": "$SMARTSPEC_REPO"
}
EOF

echo "$SMARTSPEC_VERSION" > "$SMARTSPEC_DIR/version.txt"

echo -e "${GREEN}✅ Configuration saved${NC}"

# Step 6: Create sync script (if using copies)
if [ "$USE_SYMLINKS" = false ]; then
    cat > "$SMARTSPEC_DIR/sync.sh" <<'SYNCEOF'
#!/bin/bash
# SmartSpec Sync Script

set -e

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Read config
if [ ! -f "$SMARTSPEC_DIR/config.json" ]; then
    echo "Error: SmartSpec not installed"
    exit 1
fi

# Extract platforms (simple grep since jq might not be available)
PLATFORMS=$(grep -o '"platforms":\s*\[[^]]*\]' "$SMARTSPEC_DIR/config.json" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"')

echo -e "${BLUE}🔄 Syncing SmartSpec workflows...${NC}"

for platform in $PLATFORMS; do
    case $platform in
        kilocode) TARGET_DIR=".kilocode/workflows" ;;
        roo) TARGET_DIR=".roo/commands" ;;
        claude) TARGET_DIR=".claude/commands" ;;
    esac
    
    # Sync
    if [ -d "$TARGET_DIR" ]; then
        rsync -a --delete "$WORKFLOWS_DIR/" "$TARGET_DIR/"
        echo -e "  ${GREEN}✅ $platform synced${NC}"
    fi
done

echo -e "${GREEN}✅ Sync complete${NC}"
SYNCEOF
    
    chmod +x "$SMARTSPEC_DIR/sync.sh"
    echo -e "${GREEN}✅ Sync script created${NC}"
    
    # Create git hook
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
fi

# Step 7: Success message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ SmartSpec installed successfully!  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "📍 Installation details:"
echo "  - Version: $SMARTSPEC_VERSION"
echo "  - Location: $SMARTSPEC_DIR"
echo "  - Method: $([ "$USE_SYMLINKS" = true ] && echo "Symlinks (auto-sync)" || echo "Copies (manual sync)")"
echo "  - Platforms: ${PLATFORMS[*]}"
echo ""

if [ "$USE_SYMLINKS" = false ]; then
    echo -e "${YELLOW}📝 Note: You're using copies (not symlinks)${NC}"
    echo "   Run '.smartspec/sync.sh' after updating workflows"
    echo ""
fi

echo "🎉 You can now use SmartSpec workflows in:"
for platform in "${PLATFORMS[@]}"; do
    case $platform in
        kilocode) echo "  - Kilo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        roo) echo "  - Roo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        claude) echo "  - Claude Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
    esac
done

echo ""
echo "📚 Documentation: https://github.com/naibarn/SmartSpec"
echo "💡 Quick start: /smartspec_generate_spec <your-spec-file>"
