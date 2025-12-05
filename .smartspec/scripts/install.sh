#!/bin/bash
# SmartSpec Multi-Platform Installer
# Version: 5.2
# Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SMARTSPEC_REPO="https://github.com/naibarn/SmartSpec.git"
SMARTSPEC_VERSION="v5.2"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories
KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"
ANTIGRAVITY_DIR=".agent/workflows"
GEMINI_CLI_DIR=".gemini/commands"

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

# Step 2: Detect platforms and ask user
echo ""
echo "🔍 Detecting platforms..."

DETECTED_PLATFORMS=()
if [ -d ".kilocode" ]; then
    DETECTED_PLATFORMS+=("kilocode")
    echo -e "  ${GREEN}✅ Kilo Code detected${NC}"
fi

if [ -d ".roo" ]; then
    DETECTED_PLATFORMS+=("roo")
    echo -e "  ${GREEN}✅ Roo Code detected${NC}"
fi

if [ -d ".claude" ]; then
    DETECTED_PLATFORMS+=("claude")
    echo -e "  ${GREEN}✅ Claude Code detected${NC}"
fi

if [ -d ".agent" ]; then
    DETECTED_PLATFORMS+=("antigravity")
    echo -e "  ${GREEN}✅ Google Antigravity detected${NC}"
fi

if [ -d ".gemini" ]; then
    DETECTED_PLATFORMS+=("gemini-cli")
    echo -e "  ${GREEN}✅ Gemini CLI detected${NC}"
fi

if [ ${#DETECTED_PLATFORMS[@]} -eq 0 ]; then
    echo -e "  ${YELLOW}⚠️  No platforms detected${NC}"
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

# Try to read user input
if [ -t 0 ]; then
    # stdin is a terminal, read normally
    read -p "Enter choice [1-6] (default: 1): " choice
else
    # stdin is piped, try to read from /dev/tty
    read -p "Enter choice [1-6] (default: 1): " choice < /dev/tty 2>/dev/null || choice=""
fi

# Default to 1 if empty
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

# Step 3: Install workflows
echo ""
echo "📦 Installing SmartSpec workflows..."

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
    
    # Create parent directory
    mkdir -p "$(dirname "$TARGET_DIR")"
    
    # Verify source directory exists
    if [ ! -d "$WORKFLOWS_DIR" ]; then
        echo -e "  ${RED}❌ Error: Workflows directory not found: $WORKFLOWS_DIR${NC}"
        exit 1
    fi
    
    # Handle Gemini CLI TOML conversion
    if [ "$platform" = "gemini-cli" ]; then
        echo -e "  ${BLUE}🔄 Converting Markdown workflows to TOML format...${NC}"
        
        # Create target directory
        mkdir -p "$TARGET_DIR"
        
        # Convert each workflow
        CONVERTED=0
        for md_file in "$WORKFLOWS_DIR"/smartspec_*.md; do
            if [ ! -f "$md_file" ]; then
                continue
            fi
            
            filename=$(basename "$md_file" .md)
            toml_file="$TARGET_DIR/${filename}.toml"
            
            # Simple inline conversion
            # Skip frontmatter (---...---) and extract first # title as description
            description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //' | sed 's/"/\\"/g')
            if [ -z "$description" ]; then
                description="SmartSpec workflow: ${filename//_/ }"
            fi
            
            # Extract content after frontmatter as prompt
            # Find line number of second --- (end of frontmatter)
            frontmatter_end=$(grep -n '^---$' "$md_file" | sed -n '2p' | cut -d: -f1)
            if [ -n "$frontmatter_end" ]; then
                # Skip frontmatter and extract rest
                prompt=$(tail -n +$((frontmatter_end + 1)) "$md_file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            else
                # No frontmatter, extract from line 2
                prompt=$(tail -n +2 "$md_file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            fi
            
            # Create TOML file
            cat > "$toml_file" <<EOF
description = "$description"

prompt = """
$prompt
"""
EOF
            
            ((CONVERTED++))
        done
        
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: $CONVERTED workflows converted and installed${NC}"
        continue
    fi
    
    # Handle existing workflows directory
    if [ -L "$TARGET_DIR" ]; then
        # Remove old symlink and convert to directory
        echo -e "  ${BLUE}🔗 Converting symlink to directory${NC}"
        rm -f "$TARGET_DIR"
        mkdir -p "$TARGET_DIR"
        cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows installed${NC}"
    elif [ -d "$TARGET_DIR" ]; then
        # Directory exists - merge workflows
        echo -e "  ${BLUE}🔍 Checking for existing SmartSpec workflows...${NC}"
        
        # Find existing SmartSpec workflows
        EXISTING_SMARTSPEC=()
        if ls "$TARGET_DIR"/smartspec_*.md >/dev/null 2>&1; then
            while IFS= read -r file; do
                EXISTING_SMARTSPEC+=("$(basename "$file")")
            done < <(ls "$TARGET_DIR"/smartspec_*.md 2>/dev/null)
        fi
        
        if [ ${#EXISTING_SMARTSPEC[@]} -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Found ${#EXISTING_SMARTSPEC[@]} existing SmartSpec workflow(s)${NC}"
            echo ""
            echo "  How do you want to proceed?"
            echo "    1) Overwrite all (recommended for updates)"
            echo "    2) Skip all (keep existing versions)"
            echo "    3) Cancel installation"
            
            # Try to read user input
            if [ -t 0 ]; then
                read -p "  Enter choice [1-3] (default: 1): " overwrite_choice
            else
                read -p "  Enter choice [1-3] (default: 1): " overwrite_choice < /dev/tty 2>/dev/null || overwrite_choice=""
            fi
            
            # Default to 1 if empty
            if [ -z "$overwrite_choice" ]; then
                overwrite_choice=1
                echo "  Using default: $overwrite_choice"
            fi
            
            case $overwrite_choice in
                1)
                    # Backup existing SmartSpec workflows
                    BACKUP_DIR="${TARGET_DIR}.smartspec.backup.$(date +%Y%m%d_%H%M%S)"
                    mkdir -p "$BACKUP_DIR"
                    for file in "${EXISTING_SMARTSPEC[@]}"; do
                        cp "$TARGET_DIR/$file" "$BACKUP_DIR/" 2>/dev/null || true
                    done
                    echo -e "  ${GREEN}💾 Backed up existing SmartSpec workflows to $(basename "$BACKUP_DIR")${NC}"
                    
                    # Copy new workflows
                    cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
                    echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows merged (${#EXISTING_SMARTSPEC[@]} updated)${NC}"
                    ;;
                2)
                    # Copy only new workflows (skip existing)
                    COPIED=0
                    for file in "$WORKFLOWS_DIR"/smartspec_*.md; do
                        filename=$(basename "$file")
                        if [ ! -f "$TARGET_DIR/$filename" ]; then
                            cp "$file" "$TARGET_DIR/"
                            ((COPIED++))
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
            # No existing SmartSpec workflows, just copy
            cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
            echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows installed${NC}"
        fi
    else
        # Directory doesn't exist - create and copy
        mkdir -p "$TARGET_DIR"
        cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
        echo -e "  ${GREEN}✅ $PLATFORM_NAME: Workflows installed${NC}"
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
  "use_symlinks": false,
  "repo": "$SMARTSPEC_REPO"
}
EOF

echo "$SMARTSPEC_VERSION" > "$SMARTSPEC_DIR/version.txt"

echo -e "${GREEN}✅ Configuration saved${NC}"

# Step 6: Create sync script
# Always create sync script for manual updates
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
        antigravity) TARGET_DIR=".agent/workflows" ;;
        gemini-cli) 
            TARGET_DIR=".gemini/commands"
            # Convert to TOML for Gemini CLI
            if [ -d "$TARGET_DIR" ]; then
                for md_file in "$WORKFLOWS_DIR"/smartspec_*.md; do
                    if [ ! -f "$md_file" ]; then continue; fi
                    filename=$(basename "$md_file" .md)
                    toml_file="$TARGET_DIR/${filename}.toml"
                    # Skip frontmatter and extract first # title
                    description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //' | sed 's/"/\\"/g')
                    [ -z "$description" ] && description="SmartSpec workflow: ${filename//_/ }"
                    # Extract content after frontmatter
                    frontmatter_end=$(grep -n '^---$' "$md_file" | sed -n '2p' | cut -d: -f1)
                    if [ -n "$frontmatter_end" ]; then
                        prompt=$(tail -n +$((frontmatter_end + 1)) "$md_file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
                    else
                        prompt=$(tail -n +2 "$md_file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
                    fi
                    cat > "$toml_file" <<EOF
description = "$description"

prompt = """
$prompt
"""
EOF
                done
                echo -e "  ${GREEN}✅ $platform synced (converted to TOML)${NC}"
                continue
            fi
            ;;
    esac
    
    # Sync only SmartSpec workflows (Markdown platforms)
    if [ -d "$TARGET_DIR" ]; then
        cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
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

# Step 7: Success message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ SmartSpec installed successfully!  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "📍 Installation details:"
echo "  - Version: $SMARTSPEC_VERSION"
echo "  - Location: $SMARTSPEC_DIR"
echo "  - Method: Merged installation (preserves existing workflows)"
echo "  - Platforms: ${PLATFORMS[*]}"
echo ""

echo -e "${YELLOW}📝 Note: SmartSpec workflows are merged with your existing workflows${NC}"
echo "   Run '.smartspec/sync.sh' to update SmartSpec workflows from repository"
echo ""

echo "🎉 You can now use SmartSpec workflows in:"
for platform in "${PLATFORMS[@]}"; do
    case $platform in
        kilocode) echo "  - Kilo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        roo) echo "  - Roo Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        claude) echo "  - Claude Code: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        antigravity) echo "  - Google Antigravity: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
        gemini-cli) echo "  - Gemini CLI: /smartspec_generate_spec, /smartspec_generate_tasks, etc." ;;
    esac
done

echo ""
echo "📚 Documentation: https://github.com/naibarn/SmartSpec"
echo "💡 Quick start: /smartspec_generate_spec <your-spec-file>"
