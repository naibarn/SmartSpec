#!/bin/bash
# SmartSpec Multi-Platform Installer
# Version: 5.2 (centralization-compatible)
# Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI
#
# Master source of workflows: .smartspec/workflows/
# This script installs/updates SmartSpec into the current project
# and syncs workflows to platform-specific command folders in your home directory.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_REPO_ZIP="https://github.com/naibarn/SmartSpec/archive/refs/heads/main.zip"
SMARTSPEC_VERSION="v5.2"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories (home-based defaults)
KILOCODE_DIR="$HOME/.kilocode/workflows"
ROO_DIR="$HOME/.roo/commands"
CLAUDE_DIR="$HOME/.claude/commands"
ANTIGRAVITY_DIR="$HOME/.agent/workflows"
GEMINI_DIR="$HOME/.gemini/commands"

echo -e "${BLUE}🚀 SmartSpec Multi-Platform Installer${NC}"
echo "===================================="
echo ""

# Backup & remove old install if exists
if [ -d "$SMARTSPEC_DIR" ]; then
  echo -e "${BLUE}🔄 SmartSpec is already installed. Updating...${NC}"

  if [ -d "$WORKFLOWS_DIR" ]; then
    echo "💾 Backing up existing workflows..."
    cp -r "$WORKFLOWS_DIR" "$WORKFLOWS_DIR.backup" 2>/dev/null || true
    echo -e "  ${GREEN}✅ Backup created${NC}"
  fi

  echo "🗑️  Removing old installation..."
  rm -rf "$SMARTSPEC_DIR"
  echo -e "  ${GREEN}✅ Old installation removed${NC}"
  echo ""
fi

# Step 1: Download SmartSpec zip
echo "📥 Downloading SmartSpec workflows and knowledge base..."
TMP_ROOT="$(mktemp -d 2>/dev/null || mktemp -d -t smartspec_install)"
ZIP_PATH="$TMP_ROOT/smartspec.zip"

if command -v curl >/dev/null 2>&1; then
  curl -L "$SMARTSPEC_REPO_ZIP" -o "$ZIP_PATH"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$ZIP_PATH" "$SMARTSPEC_REPO_ZIP"
else
  echo -e "${RED}❌ curl or wget is required to download SmartSpec.${NC}"
  exit 1
fi

unzip -q "$ZIP_PATH" -d "$TMP_ROOT"

REPO_EXTRACT="$TMP_ROOT/SmartSpec-main"
SOURCE_SPEC="$REPO_EXTRACT/.smartspec"

if [ ! -d "$SOURCE_SPEC" ]; then
  echo -e "${RED}❌ '.smartspec' folder not found in the downloaded archive.${NC}"
  exit 1
fi

mkdir -p "$SMARTSPEC_DIR"
cp -r "$SOURCE_SPEC/"* "$SMARTSPEC_DIR/"

rm -rf "$TMP_ROOT"

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo -e "${RED}❌ Master workflows directory not found:${NC} $WORKFLOWS_DIR"
  exit 1
fi

echo -e "  ${GREEN}✅ Downloaded SmartSpec${NC}"
echo ""

# Step 2: Select platforms
echo "Which platforms do you want to install/update?"
echo "  1) Kilo Code"
echo "  2) Roo Code"
echo "  3) Claude Code"
echo "  4) Google Antigravity"
echo "  5) Gemini CLI"
echo "  6) All of the above"

read -r -p "Enter choice [1-6] (default: 1): " CHOICE
CHOICE="${CHOICE:-1}"

case "$CHOICE" in
  1) PLATFORMS=("kilocode") ;;
  2) PLATFORMS=("roo") ;;
  3) PLATFORMS=("claude") ;;
  4) PLATFORMS=("antigravity") ;;
  5) PLATFORMS=("gemini-cli") ;;
  6) PLATFORMS=("kilocode" "roo" "claude" "antigravity" "gemini-cli") ;;
  *) echo -e "${RED}❌ Invalid choice.${NC}"; exit 1 ;;
esac

# Step 3: Save configuration
echo ""
echo "💾 Saving configuration..."

PLATFORMS_JSON=$(printf '"%s",' "${PLATFORMS[@]}" | sed 's/,$//')
INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "$SMARTSPEC_DIR/config.json" << EOF
{
  "version": "$SMARTSPEC_VERSION",
  "installed_at": "$INSTALLED_AT",
  "platforms": [ $PLATFORMS_JSON ],
  "use_symlinks": false,
  "repo": "https://github.com/naibarn/SmartSpec.git"
}
EOF

echo "$SMARTSPEC_VERSION" > "$SMARTSPEC_DIR/version.txt"

echo -e "  ${GREEN}✅ Configuration saved${NC}"

# Step 4: Create project helper sync script (wrapper)
cat > "$SMARTSPEC_DIR/sync.sh" << 'EOF'
#!/bin/bash
# SmartSpec Sync Script (Project Helper)
# Delegates to root-level sync.sh when available.

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROOT_DIR/sync.sh" ]; then
  bash "$ROOT_DIR/sync.sh" "$@"
  exit $?
fi

echo "❌ Root-level sync.sh not found."
echo "Please run the standalone sync.sh from your SmartSpec distribution."
exit 1
EOF
chmod +x "$SMARTSPEC_DIR/sync.sh"

echo -e "  ${GREEN}✅ Project sync helper created at .smartspec/sync.sh${NC}"

# Step 5: Initial sync using the standalone logic embedded here
echo ""
echo "📦 Installing SmartSpec workflows..."

MD_FILES=()
while IFS= read -r -d '' f; do
  MD_FILES+=("$f")
done < <(find "$WORKFLOWS_DIR" -maxdepth 1 -type f -name "smartspec_*.md" -print0)

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

for platform in "${PLATFORMS[@]}"; do
  case "$platform" in
    kilocode) TARGET_DIR="$KILOCODE_DIR"; PLATFORM_NAME="Kilo Code" ;;
    roo) TARGET_DIR="$ROO_DIR"; PLATFORM_NAME="Roo Code" ;;
    claude) TARGET_DIR="$CLAUDE_DIR"; PLATFORM_NAME="Claude Code" ;;
    antigravity) TARGET_DIR="$ANTIGRAVITY_DIR"; PLATFORM_NAME="Google Antigravity" ;;
    gemini-cli) TARGET_DIR="$GEMINI_DIR"; PLATFORM_NAME="Gemini CLI" ;;
    *) echo -e "${YELLOW}⚠️  Unknown platform: $platform - skipping${NC}"; continue ;;
  esac

  mkdir -p "$TARGET_DIR"

  if [ "$platform" = "gemini-cli" ]; then
    echo -e "  ${BLUE}🔄 $PLATFORM_NAME: Converting Markdown workflows to TOML...${NC}"
    for md in "${MD_FILES[@]}"; do
      base="$(basename "$md" .md)"
      convert_md_to_toml "$md" "$TARGET_DIR/$base.toml"
    done
    echo -e "  ${GREEN}✅ $PLATFORM_NAME installed (TOML)${NC}"
    continue
  fi

  rm -f "$TARGET_DIR"/smartspec_*.md 2>/dev/null || true
  for md in "${MD_FILES[@]}"; do
    cp "$md" "$TARGET_DIR/"
  done
  echo -e "  ${GREEN}✅ $PLATFORM_NAME installed${NC}"
done

echo ""
echo -e "${GREEN}✅ SmartSpec installed successfully!${NC}"
echo "Edit workflows in .smartspec/workflows/ and run:"
echo "  .smartspec/sync.sh"
