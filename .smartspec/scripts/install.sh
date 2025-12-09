#!/usr/bin/env bash
# SmartSpec Installer (Project-Local)
# Platform: Linux / macOS (bash)
# Version: 5.6
#
# This script:
#   - Downloads the SmartSpec distribution repo
#   - Copies `.smartspec/` and `.smartspec-docs/` into the current project
#   - Ensures stable filenames:
#       .smartspec/system_prompt_smartspec.md
#       .smartspec/knowledge_base_smartspec.md
#   - Copies .smartspec/workflows into platform-specific folders if present:
#       .kilocode/workflows
#       .roo/commands
#       .claude/commands
#       .agent/workflows
#       .gemini/commands
#
# NOTE:
#   - Set SMARTSPEC_REPO_URL and SMARTSPEC_REPO_BRANCH as needed, or
#     edit defaults below.

set -euo pipefail

###############################
# Configuration
###############################

: "${SMARTSPEC_REPO_URL:=https://github.com/your-org/SmartSpec.git}"
: "${SMARTSPEC_REPO_BRANCH:=main}"

SMARTSPEC_DIR=".smartspec"
SMARTSPEC_DOCS_DIR=".smartspec-docs"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"
WORKFLOW_DOCS_DIR="$SMARTSPEC_DOCS_DIR/workflows"

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
  # Copy contents of src into dst
  # shellcheck disable=SC2115
  cp -R "$src"/. "$dst"/
}

###############################
# Banner
###############################

log "============================================="
log "🚀 SmartSpec Installer (Linux/macOS) v5.6"
log "============================================="
log "Project root: $(pwd)"
log "Repo:         ${SMARTSPEC_REPO_URL} (${SMARTSPEC_REPO_BRANCH})"
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
# Step 2: Copy .smartspec and .smartspec-docs
###############################

SRC_SMARTSPEC="${TMP_DIR}/.smartspec"
SRC_SMARTSPEC_DOCS="${TMP_DIR}/.smartspec-docs"

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

###############################
# Step 3: Sanity check core files
###############################

if [ ! -f "$SMARTSPEC_DIR/system_prompt_smartspec.md" ]; then
  log "⚠️ Warning: .smartspec/system_prompt_smartspec.md not found."
fi

if [ ! -f "$SMARTSPEC_DIR/knowledge_base_smartspec.md" ]; then
  log "⚠️ Warning: .smartspec/knowledge_base_smartspec.md not found."
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
      # create the directory so the user can start using it
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
# Step 5: Done
###############################

log ""
log "✅ SmartSpec installation/update complete."
log "   - Core:   $SMARTSPEC_DIR"
log "   - Docs:   $SMARTSPEC_DOCS_DIR (if present in repo)"
log "   - Tools:  $KILOCODE_DIR, $ROO_DIR, $CLAUDE_DIR, $ANTIGRAVITY_DIR, $GEMINI_DIR"
log ""
log "You can now run SmartSpec workflows (e.g. /smartspec_project_copilot) via"
log "your preferred tool (Kilo/Roo/Claude/Antigravity/Gemini) using the synced"
log "commands from .smartspec/workflows."
