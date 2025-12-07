#!/usr/bin/env bash
# SmartSpec Multi-Platform Installer (Project-Local)
# Version: 5.2
# Supports: Kilo Code, Roo Code, Claude Code, Google Antigravity, Gemini CLI
#
# Master source of workflows: .smartspec/workflows/
# This installer downloads/updates the SmartSpec framework into .smartspec/
# then copies workflows to each platform-specific command directory
# located in THIS repository (not $HOME).

set -euo pipefail

# =============================
# Colors
# =============================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =============================
# Configuration
# =============================
SMARTSPEC_REPO="https://github.com/naibarn/SmartSpec.git"
SMARTSPEC_REPO_ZIP="https://github.com/naibarn/SmartSpec/archive/refs/heads/main.zip"
SMARTSPEC_VERSION="v5.2"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Project-local platform directories
KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"
ANTIGRAVITY_DIR=".agent/workflows"
GEMINI_CLI_DIR=".gemini/commands"

# =============================
# Helpers
# =============================
log() { echo -e "$1"; }

have_cmd() { command -v "$1" >/dev/null 2>&1; }

mktemp_dir() {
  if have_cmd mktemp; then
    mktemp -d 2>/dev/null || mktemp -d -t smartspec
  else
    # Fallback
    local d=".smartspec-tmp-$(date +%s)"
    mkdir -p "$d"
    echo "$d"
  fi
}

extract_zip() {
  local zipfile="$1"
  local dest="$2"

  mkdir -p "$dest"

  if have_cmd unzip; then
    unzip -q "$zipfile" -d "$dest"
    return 0
  fi

  if have_cmd python3; then
    python3 - <<PY
import sys, zipfile, os
zip_path = sys.argv[1]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(out_dir)
PY
    "$zipfile" "$dest"
    return 0
  fi

  if have_cmd python; then
    python - <<PY
import sys, zipfile, os
zip_path = sys.argv[1]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(out_dir)
PY
    "$zipfile" "$dest"
    return 0
  fi

  if have_cmd busybox; then
    busybox unzip -q "$zipfile" -d "$dest"
    return 0
  fi

  log "${RED}❌ Error: Cannot extract zip. Please install 'unzip' or 'python3'.${NC}"
  exit 1
}

backup_dir_if_exists() {
  local path="$1"
  if [ -d "$path" ]; then
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    cp -r "$path" "${path}.backup.${ts}"
  fi
}

# =============================
# UI
# =============================
log "${BLUE}🚀 SmartSpec Multi-Platform Installer${NC}"
log "${BLUE}======================================${NC}"
log ""

# =============================
# Step 0: Update mode detection
# =============================
UPDATE_MODE=false
if [ -d "$SMARTSPEC_DIR" ]; then
  UPDATE_MODE=true
  log "${BLUE}🔄 Existing SmartSpec detected — will update in-place${NC}"
  # Backup only workflows (where users might customize)
  backup_dir_if_exists "$WORKFLOWS_DIR"
fi

# =============================
# Step 1: Download SmartSpec framework into .smartspec/
# =============================
log "📥 Downloading SmartSpec framework (.smartspec)..."

TMP_DIR=$(mktemp_dir)
cleanup() { rm -rf "$TMP_DIR" 2>/dev/null || true; }
trap cleanup EXIT

if have_cmd git; then
  log "  ${BLUE}• Using git${NC}"
  git clone --depth 1 "$SMARTSPEC_REPO" "$TMP_DIR/repo" -q
  if [ ! -d "$TMP_DIR/repo/.smartspec" ]; then
    log "${RED}❌ Error: .smartspec folder not found in repository.${NC}"
    exit 1
  fi
  mkdir -p "$SMARTSPEC_DIR"
  # Preserve user edits by replacing everything EXCEPT workflows when update mode
  if [ "$UPDATE_MODE" = true ] && [ -d "$WORKFLOWS_DIR" ]; then
    # Copy non-workflow assets
    rsync -a --delete --exclude "workflows/" "$TMP_DIR/repo/.smartspec/" "$SMARTSPEC_DIR/" 2>/dev/null \
      || (rm -rf "$SMARTSPEC_DIR"/* && cp -r "$TMP_DIR/repo/.smartspec/"* "$SMARTSPEC_DIR/")
  else
    rm -rf "$SMARTSPEC_DIR"
    cp -r "$TMP_DIR/repo/.smartspec" "$SMARTSPEC_DIR"
  fi
else
  log "  ${BLUE}• Using zip download${NC}"
  if have_cmd curl; then
    curl -fsSL "$SMARTSPEC_REPO_ZIP" -o "$TMP_DIR/smartspec.zip"
  elif have_cmd wget; then
    wget -q "$SMARTSPEC_REPO_ZIP" -O "$TMP_DIR/smartspec.zip"
  else
    log "${RED}❌ Error: Neither git, curl, nor wget is available.${NC}"
    exit 1
  fi

  extract_zip "$TMP_DIR/smartspec.zip" "$TMP_DIR/unzipped"

  local_repo_dir=""
  if [ -d "$TMP_DIR/unzipped/SmartSpec-main" ]; then
    local_repo_dir="$TMP_DIR/unzipped/SmartSpec-main"
  else
    # Handle unexpected zip root
    local_repo_dir=$(find "$TMP_DIR/unzipped" -maxdepth 2 -type d -name "SmartSpec-*" | head -n 1 || true)
  fi

  if [ -z "$local_repo_dir" ] || [ ! -d "$local_repo_dir/.smartspec" ]; then
    log "${RED}❌ Error: .smartspec folder not found in the downloaded archive.${NC}"
    exit 1
  fi

  mkdir -p "$SMARTSPEC_DIR"
  if [ "$UPDATE_MODE" = true ] && [ -d "$WORKFLOWS_DIR" ]; then
    rsync -a --delete --exclude "workflows/" "$local_repo_dir/.smartspec/" "$SMARTSPEC_DIR/" 2>/dev/null \
      || (rm -rf "$SMARTSPEC_DIR"/* && cp -r "$local_repo_dir/.smartspec/"* "$SMARTSPEC_DIR/")
  else
    rm -rf "$SMARTSPEC_DIR"
    cp -r "$local_repo_dir/.smartspec" "$SMARTSPEC_DIR"
  fi
fi

# If update mode: restore backed-up workflows if repo copy is missing
if [ "$UPDATE_MODE" = true ]; then
  if [ ! -d "$WORKFLOWS_DIR" ]; then
    # Try to restore latest backup
    latest_backup=$(ls -td "${WORKFLOWS_DIR}.backup."* 2>/dev/null | head -n 1 || true)
    if [ -n "$latest_backup" ]; then
      mkdir -p "$WORKFLOWS_DIR"
      cp -r "$latest_backup"/* "$WORKFLOWS_DIR/" 2>/dev/null || true
    fi
  fi
fi

if [ ! -d "$WORKFLOWS_DIR" ]; then
  log "${RED}❌ Error: Master workflows directory not found: $WORKFLOWS_DIR${NC}"
  log "This installer expects workflows to live under .smartspec/workflows/."
  exit 1
fi

log "  ${GREEN}✅ SmartSpec framework ready${NC}"
log ""

# =============================
# Step 2: Detect platforms (project-local)
# =============================
log "🔍 Detecting project-local platforms..."

DETECTED=()

[ -d ".kilocode" ] && DETECTED+=("kilocode")
[ -d ".roo" ] && DETECTED+=("roo")
[ -d ".claude" ] && DETECTED+=("claude")
[ -d ".agent" ] && DETECTED+=("antigravity")
[ -d ".gemini" ] && DETECTED+=("gemini-cli")

if [ ${#DETECTED[@]} -eq 0 ]; then
  log "  ${YELLOW}⚠️  No platform folders detected in this repo yet.${NC}"
  log "  The installer will still create target folders for selected platforms."
fi

# =============================
# Step 3: Choose platforms
# =============================
log ""
log "Which platforms do you want to install/update in this repo?"
log "  1) Kilo Code (.kilocode)"
log "  2) Roo Code (.roo)"
log "  3) Claude Code (.claude)"
log "  4) Google Antigravity (.agent)"
log "  5) Gemini CLI (.gemini)"
log "  6) All of the above"
log ""

choice=""
if [ -t 0 ]; then
  read -p "Enter choice [1-6] (default: 6): " choice
else
  read -p "Enter choice [1-6] (default: 6): " choice < /dev/tty 2>/dev/null || choice=""
fi

[ -z "$choice" ] && choice="6"

PLATFORMS=()
case "$choice" in
  1) PLATFORMS=("kilocode") ;;
  2) PLATFORMS=("roo") ;;
  3) PLATFORMS=("claude") ;;
  4) PLATFORMS=("antigravity") ;;
  5) PLATFORMS=("gemini-cli") ;;
  6) PLATFORMS=("kilocode" "roo" "claude" "antigravity" "gemini-cli") ;;
  *) PLATFORMS=("kilocode" "roo" "claude" "antigravity" "gemini-cli") ;;
 esac

# =============================
# Step 4: Write config.json
# =============================
mkdir -p "$SMARTSPEC_DIR"
cat > "$SMARTSPEC_DIR/config.json" <<EOF
{
  "version": "$SMARTSPEC_VERSION",
  "platforms": [$(printf '"%s",' "${PLATFORMS[@]}" | sed 's/,$//')],
  "use_symlinks": false,
  "install_scope": "project-local"
}
EOF

log "${GREEN}✅ Config written: $SMARTSPEC_DIR/config.json${NC}"

# =============================
# Step 5: Create/update sync.sh (project-local)
# =============================
cat > "$SMARTSPEC_DIR/sync.sh" <<'SYNCEOF'
#!/usr/bin/env bash
# SmartSpec Sync Script (Project-Local)
# Copies master workflows from .smartspec/workflows/ to tool folders in this repo.

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"
CONFIG="$SMARTSPEC_DIR/config.json"

KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"
ANTIGRAVITY_DIR=".agent/workflows"
GEMINI_CLI_DIR=".gemini/commands"

have_cmd() { command -v "$1" >/dev/null 2>&1; }

log() { echo -e "$1"; }

if [ ! -d "$SMARTSPEC_DIR" ]; then
  log "${RED}❌ Error: .smartspec not found. Run install.sh first.${NC}"
  exit 1
fi

if [ ! -f "$CONFIG" ]; then
  log "${RED}❌ Error: $CONFIG not found.${NC}"
  exit 1
fi

if [ ! -d "$WORKFLOWS_DIR" ]; then
  log "${RED}❌ Error: Master workflows directory not found: $WORKFLOWS_DIR${NC}"
  exit 1
fi

# Extract platforms without requiring jq
PLATFORMS=$(grep -o '"platforms"\s*:\s*\[[^]]*\]' "$CONFIG" | grep -o '"[^"]*"' | grep -v platforms | tr -d '"' || true)

if [ -z "$PLATFORMS" ]; then
  log "${YELLOW}⚠️  No platforms listed in config. Defaulting to kilocode roo claude antigravity gemini-cli.${NC}"
  PLATFORMS="kilocode roo claude antigravity gemini-cli"
fi

log "${BLUE}🔄 SmartSpec Sync (project-local)${NC}"
log "=============================="
log ""

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
      TARGET_DIR="$GEMINI_CLI_DIR"
      PLATFORM_NAME="Gemini CLI"
      ;;
    *)
      log "  ${YELLOW}⚠️  Unknown platform '$platform' - skipping${NC}"
      continue
      ;;
  esac

  mkdir -p "$TARGET_DIR"

  if [ "$platform" = "gemini-cli" ]; then
    # Convert Markdown workflows to TOML
    CONVERTED=0
    for md_file in "$WORKFLOWS_DIR"/smartspec_*.md; do
      [ -f "$md_file" ] || continue
      filename=$(basename "$md_file" .md)
      toml_file="$TARGET_DIR/${filename}.toml"

      # Prefer YAML frontmatter description if present
      description=$(grep -m 1 '^description:' "$md_file" | sed 's/^description: *//')
      if [ -z "$description" ]; then
        description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //')
      fi
      [ -z "$description" ] && description="SmartSpec workflow: ${filename//_/ }"

      # Find second --- as end of frontmatter
      frontmatter_end=$(grep -n '^---$' "$md_file" | sed -n '2p' | cut -d: -f1 || true)
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

    log "  ${GREEN}✅ $PLATFORM_NAME synced ($CONVERTED TOML files generated)${NC}"
    continue
  fi

  # Markdown platforms
  cp "$WORKFLOWS_DIR"/smartspec_*.md "$TARGET_DIR/" 2>/dev/null || true
  log "  ${GREEN}✅ $PLATFORM_NAME synced${NC}"
 done

log ""
log "${GREEN}✅ Sync complete${NC}"
SYNCEOF

chmod +x "$SMARTSPEC_DIR/sync.sh"
log "${GREEN}✅ Sync script ready: $SMARTSPEC_DIR/sync.sh${NC}"

# =============================
# Step 6: Run initial sync
# =============================
log ""
log "${BLUE}🔄 Syncing workflows to project tool folders...${NC}"
"$SMARTSPEC_DIR/sync.sh"

# =============================
# Step 7: Optional git hook (project-local)
# =============================
if [ -d ".git" ]; then
  mkdir -p ".git/hooks"
  cat > ".git/hooks/post-merge" <<'HOOKEOF'
#!/usr/bin/env bash
# Auto-sync SmartSpec after git pull/merge (project-local)

if [ -f ".smartspec/sync.sh" ]; then
  echo "🔄 Auto-syncing SmartSpec workflows..."
  .smartspec/sync.sh
fi
HOOKEOF
  chmod +x ".git/hooks/post-merge"
  log "${GREEN}✅ Git hook installed (auto-sync on pull)${NC}"
fi

# =============================
# Done
# =============================
log ""
log "${GREEN}╔════════════════════════════════════════╗${NC}"
log "${GREEN}║  ✅ SmartSpec installed successfully!  ║${NC}"
log "${GREEN}╚════════════════════════════════════════╝${NC}"
log ""
log "📍 Installation details:"
log "  - Version: $SMARTSPEC_VERSION"
log "  - Scope: project-local"
log "  - Location: $SMARTSPEC_DIR"
log "  - Platforms: ${PLATFORMS[*]}"
log ""
log "📝 Notes:"
log "  - Always edit master workflows in $WORKFLOWS_DIR"
log "  - Run '$SMARTSPEC_DIR/sync.sh' to re-sync platforms anytime"
log ""
log "🎉 You can now use commands like /smartspec_generate_spec in supported tools."
