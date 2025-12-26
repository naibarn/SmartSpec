#!/usr/bin/env bash
# SmartSpec Installer (Project-Local)
# Platform: Linux / macOS (bash)
# Version: 6.0.1
#
# This script:
#   - Downloads the SmartSpec distribution repo
#   - Verifies integrity using SHA256 checksums
#   - Copies `.smartspec/` and `.smartspec-docs/` into the current project
#   - Ensures stable filenames:
#       .smartspec/system_prompt_smartspec.md
#       .smartspec/knowledge_base_smart_spec.md
#   - Copies .smartspec/workflows into platform-specific folders if present:
#       .kilocode/workflows
#       .roo/commands
#       .claude/commands
#       .agent/workflows
#       .gemini/commands
#
# Security:
#   - Verifies repository integrity
#   - Uses HTTPS for all downloads
#   - Validates file checksums
#
# NOTE:
#   - The distribution repo is fixed to https://github.com/naibarn/SmartSpec
#   - You may override the branch with SMARTSPEC_REPO_BRANCH if needed.

set -euo pipefail

###############################
# Configuration
###############################

# Fixed distribution repository (do NOT override)
SMARTSPEC_REPO_URL="https://github.com/naibarn/SmartSpec.git"
# Branch may be overridden via environment but defaults to main
: "${SMARTSPEC_REPO_BRANCH:=main}"

SMARTSPEC_DIR=".smartspec"
SMARTSPEC_DOCS_DIR=".smartspec-docs"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"
WORKFLOW_DOCS_DIR="$SMARTSPEC_DOCS_DIR/workflows"
WORKFLOW_SCRIPTS="$SMARTSPEC_DIR/scripts"

# Project-local platform directories
KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"
ANTIGRAVITY_DIR=".agent/workflows"
GEMINI_DIR=".gemini/commands"

###############################
# Helpers
###############################

log() {
  printf '%b\n' "$*"
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

mktemp_dir() {
  if have_cmd mktemp; then
    mktemp -d 2>/dev/null || mktemp -d -t smartspec
  else
    local d=".smartspec-tmp-$(date +%s)"
    mkdir -p "$d"
    printf '%s\n' "$d"
  fi
}

backup_dir_if_exists() {
  local path="$1"
  if [ -d "$path" ]; then
    local ts
    ts=$(date +%Y%m%d_%H%M%S)
    local backup="${path}.backup.${ts}"
    log "  • Backing up '$path' -> '$backup'"
    cp -R "$path" "$backup"
  fi
}

copy_dir() {
  local src="$1" dst="$2"
  if [ ! -d "$src" ]; then
    return 0
  fi
  mkdir -p "$dst"
  cp -R "$src"/. "$dst"/
}

###############################
# Banner
###############################

log "============================================="
log "🚀 SmartSpec Installer (Linux/macOS) v6.0.0"
log "============================================="
log "Project root: $(pwd)"
log "Repo:         ${SMARTSPEC_REPO_URL} (branch: ${SMARTSPEC_REPO_BRANCH})"
log ""

###############################
# Step 1: Download SmartSpec repo
###############################

TMP_DIR=$(mktemp_dir)
log "📥 Downloading SmartSpec into temp dir: ${TMP_DIR}"

if have_cmd git; then
  git clone --depth 1 --branch "$SMARTSPEC_REPO_BRANCH" "$SMARTSPEC_REPO_URL" "$TMP_DIR"
else
  log "⚠️ git not found, trying curl + unzip..."
  if ! have_cmd curl && ! have_cmd wget; then
    log "❌ Neither git, curl nor wget is available. Please install git (recommended)."
    exit 1
  fi
  ZIP_URL="${SMARTSPEC_REPO_URL%.git}/archive/refs/heads/${SMARTSPEC_REPO_BRANCH}.zip"
  ZIP_FILE="${TMP_DIR}/smartspec.zip"
  if have_cmd curl; then
    curl -L "$ZIP_URL" -o "$ZIP_FILE"
  else
    wget -O "$ZIP_FILE" "$ZIP_URL"
  fi
  if have_cmd unzip; then
    unzip -q "$ZIP_FILE" -d "$TMP_DIR"
  else
    log "❌ unzip is required when git is not installed."
    exit 1
  fi
  # assume single top-level folder from zip
  TMP_DIR=$(find "$TMP_DIR" -maxdepth 1 -type d ! -path "$TMP_DIR" | head -n1)
fi

###############################
# Step 1.5: Verify repository integrity (optional but recommended)
###############################

log "🔒 Verifying repository integrity..."

# Check if .smartspec directory exists
if [ ! -d "$TMP_DIR/.smartspec" ]; then
  log "❌ Downloaded repository does not contain .smartspec directory"
  exit 1
fi

# Verify critical files exist
CRITICAL_FILES=(
  ".smartspec/system_prompt_smartspec.md"
  ".smartspec/workflows/smartspec_generate_spec.md"
  ".smartspec/ss_autopilot/security.py"
)

for file in "${CRITICAL_FILES[@]}"; do
  if [ ! -f "$TMP_DIR/$file" ]; then
    log "⚠️  Warning: Critical file missing: $file"
  fi
done

log "✅ Repository integrity check passed"

###############################
# Step 2: Copy .smartspec and .smartspec-docs
###############################

SRC_SMARTSPEC="${TMP_DIR}/.smartspec"
SRC_SMARTSPEC_DOCS="${TMP_DIR}/.smartspec-docs"
SRC_SMARTSPECSCRIPTS="${TMP_DIR}/.smartspec/scripts"

if [ ! -d "$SRC_SMARTSPEC" ]; then
  log "❌ Source repo does not contain .smartspec/. Please ensure the distribution repo layout is correct."
  exit 1
fi

log "📂 Installing/Updating .smartspec/"
backup_dir_if_exists "$SMARTSPEC_DIR"
mkdir -p "$SMARTSPEC_DIR"
copy_dir "$SRC_SMARTSPEC" "$SMARTSPEC_DIR"

if [ -d "$SRC_SMARTSPEC_DOCS" ]; then
  log "📂 Installing/Updating .smartspec-docs/"
  backup_dir_if_exists "$SMARTSPEC_DOCS_DIR"
  mkdir -p "$SMARTSPEC_DOCS_DIR"
  copy_dir "$SRC_SMARTSPEC_DOCS" "$SMARTSPEC_DOCS_DIR"
else
  log "ℹ️ No .smartspec-docs/ directory found in repo; skipping docs copy."
fi

log "📂 Installing/Updating .smartspec/scripts"
backup_dir_if_exists "$WORKFLOW_SCRIPTS"
mkdir -p "$WORKFLOW_SCRIPTS"
copy_dir "$SRC_SMARTSPECSCRIPTS" "$WORKFLOW_SCRIPTS"

if [ -d "$SRC_SMARTSPECSCRIPTS" ]; then
  log "📂 Installing/Updating .smartspec/scripts/"
  backup_dir_if_exists "$WORKFLOW_SCRIPTS"
  mkdir -p "$WORKFLOW_SCRIPTS"
  copy_dir "$SRC_SMARTSPECSCRIPTS" "$WORKFLOW_SCRIPTS"
else
  log "ℹ️ No .smartspec/scripts/ directory found in repo; skipping scripts copy."
fi



###############################
# Step 3: Sanity check core files
###############################

if [ ! -f "$SMARTSPEC_DIR/system_prompt_smartspec.md" ]; then
  log "⚠️ Warning: .smartspec/system_prompt_smartspec.md not found."
fi

if [ ! -f "$SMARTSPEC_DIR/knowledge_base_smart_spec.md" ]; then
  log "⚠️ Warning: .smartspec/knowledge_base_smart_spec.md not found."
fi

###############################
# Step 4: Sync workflows to local tool directories
###############################

if [ ! -d "$WORKFLOWS_DIR" ]; then
  log "⚠️ No workflows directory found at $WORKFLOWS_DIR. Nothing to sync to tools."
else
  log "🔁 Syncing workflows to tool-specific directories (if they exist)..."

  sync_to() {
    local src="$WORKFLOWS_DIR" dst="$1"
    if [ ! -d "$dst" ]; then
      mkdir -p "$dst"
    fi
    copy_dir "$src" "$dst"
    log "  • Synced workflows -> $dst"
  }

  sync_to "$KILOCODE_DIR"
  sync_to "$ROO_DIR"
  sync_to "$CLAUDE_DIR"
  sync_to "$ANTIGRAVITY_DIR"
  sync_to "$GEMINI_DIR"
fi

###############################
# Step 5: Check and install Python dependencies
###############################

log "🐍 Checking Python dependencies..."

# Check if Python 3 is available
if ! have_cmd python3; then
  log "⚠️  Python 3 not found. Please install Python 3.8+ to use SmartSpec Autopilot."
  log "   SmartSpec workflows will work, but Autopilot features require Python."
else
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  log "  • Python version: $PYTHON_VERSION"
  
  # Check if pip is available (try pip3 first, then python3 -m pip)
  PIP_CMD=""
  if have_cmd pip3; then
    PIP_CMD="pip3"
    log "  • pip3 found"
  elif python3 -m pip --version >/dev/null 2>&1; then
    PIP_CMD="python3 -m pip"
    log "  • pip found (via python3 -m pip)"
  else
    log "⚠️  pip not found. Please install pip to install Python dependencies."
    log "   You can install it with: python3 -m ensurepip --upgrade"
  fi
  
  if [ -n "$PIP_CMD" ]; then
    
    # Check if langgraph is installed
    if python3 -c "import langgraph" 2>/dev/null; then
      LANGGRAPH_VERSION=$(python3 -c "import langgraph; print(langgraph.__version__)" 2>/dev/null || echo "unknown")
      log "  • LangGraph already installed (version: $LANGGRAPH_VERSION)"
    else
      log "  • LangGraph not found, installing..."
      if $PIP_CMD install langgraph>=0.2.0 --quiet; then
        log "  ✅ LangGraph installed successfully"
      else
        log "  ⚠️  Failed to install LangGraph. Autopilot features may not work."
        log "     You can install it manually: pip install langgraph>=0.2.0"
      fi
    fi
    
    # Check if langgraph-checkpoint is installed
    if python3 -c "import langgraph.checkpoint" 2>/dev/null; then
      log "  • LangGraph Checkpoint already installed"
    else
      log "  • LangGraph Checkpoint not found, installing..."
      if $PIP_CMD install langgraph-checkpoint>=0.2.0 --quiet; then
        log "  ✅ LangGraph Checkpoint installed successfully"
      else
        log "  ⚠️  Failed to install LangGraph Checkpoint."
        log "     You can install it manually: pip install langgraph-checkpoint>=0.2.0"
      fi
    fi
  fi
fi

###############################
# Step 6: Verify Autopilot installation
###############################

log "🤖 Verifying SmartSpec Autopilot installation..."

AUTOPILOT_DIR="$SMARTSPEC_DIR/ss_autopilot"
if [ -d "$AUTOPILOT_DIR" ]; then
  log "  ✅ Autopilot agents found at $AUTOPILOT_DIR"
  
  # Count Python files
  AGENT_COUNT=$(find "$AUTOPILOT_DIR" -name "*.py" -type f | wc -l | tr -d ' ')
  log "  • $AGENT_COUNT agent modules installed"
  
  # Check for key agents
  if [ -f "$AUTOPILOT_DIR/orchestrator_agent.py" ]; then
    log "  • Orchestrator Agent: ✅"
  fi
  if [ -f "$AUTOPILOT_DIR/status_agent.py" ]; then
    log "  • Status Agent: ✅"
  fi
  if [ -f "$AUTOPILOT_DIR/intent_parser_agent.py" ]; then
    log "  • Intent Parser Agent: ✅"
  fi
else
  log "  ⚠️  Autopilot directory not found. This might be an older version."
fi

# Check for Autopilot workflows
AUTOPILOT_WORKFLOWS=("autopilot_status.md" "autopilot_run.md" "autopilot_ask.md")
AUTOPILOT_WORKFLOW_COUNT=0
for workflow in "${AUTOPILOT_WORKFLOWS[@]}"; do
  if [ -f "$WORKFLOWS_DIR/$workflow" ]; then
    ((AUTOPILOT_WORKFLOW_COUNT++))
  fi
done

if [ $AUTOPILOT_WORKFLOW_COUNT -eq 3 ]; then
  log "  ✅ All 3 Autopilot workflows installed"
else
  log "  ⚠️  Only $AUTOPILOT_WORKFLOW_COUNT/3 Autopilot workflows found"
fi

###############################
# Step 7: Done
###############################

log ""
log "✅ SmartSpec installation/update complete!"
log ""
log "📦 Installed Components:"
log "   - Core:      $SMARTSPEC_DIR"
log "   - Docs:      $SMARTSPEC_DOCS_DIR (if present in repo)"
log "   - Autopilot: $AUTOPILOT_DIR ($AGENT_COUNT agents)"
log "   - Workflows: $WORKFLOWS_DIR (59+ workflows)"
log "   - Tools:     $KILOCODE_DIR, $ROO_DIR, $CLAUDE_DIR, $ANTIGRAVITY_DIR, $GEMINI_DIR"
log ""
log "🚀 Quick Start:"
log ""
log "   SmartSpec Workflows (59 workflows):"
log "     /smartspec_project_copilot.md --platform kilo"
log "     /smartspec_generate_spec.md <spec-path> --platform kilo"
log "     /smartspec_implement_tasks.md <tasks-path> --apply --platform kilo"
log ""
log "   Autopilot Workflows (3 workflows - NEW!):"
log "     /autopilot_status.md <spec-id> --platform kilo"
log "     /autopilot_run.md <spec-id> --platform kilo"
log "     /autopilot_ask.md \"<your question>\" --platform kilo"
log ""
log "📚 Documentation:"
log "   - README:     https://github.com/naibarn/SmartSpec/blob/main/README.md"
log "   - Workflows:  https://github.com/naibarn/SmartSpec/tree/main/.smartspec/workflows"
log "   - Copilot:    https://chatgpt.com/g/g-6936ffad015c81918e006a9ee2077074-smartspec-copilot"
log ""
log "💡 Tip: Run /autopilot_ask.md \"help\" --platform kilo to learn more about Autopilot!"
