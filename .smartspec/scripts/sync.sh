#!/bin/bash
# SmartSpec Sync Script (Project-first)

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

WORKFLOWS_DIR=".smartspec/workflows"

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo -e "${RED}❌ Master workflows not found at $WORKFLOWS_DIR${NC}"
  exit 1
fi

sync_dir() {
  local name="$1"
  local target="$2"

  mkdir -p "$target"
  rm -rf "$target"/*
  cp -r "$WORKFLOWS_DIR"/* "$target"/

  echo -e "  ${GREEN}✅ $name synced → $target${NC}"
}

# Project-first targets (what your screenshots show)
PROJECT_TARGETS=(
  "Antigravity:.agent/workflows"
  "Claude:.claude/commands"
  "Gemini:.gemini/commands"
)

# Optional global targets (only used if project targets absent)
GLOBAL_TARGETS=(
  "Kilo:$HOME/.kilocode/workflows"
  "Roo:$HOME/.roo/commands"
  "Claude:$HOME/.claude/commands"
  "Antigravity:$HOME/.agent/workflows"
  "Gemini:$HOME/.gemini/commands"
)

echo -e "${BLUE}🔄 Syncing SmartSpec workflows (project-first)...${NC}"

project_synced=0
for item in "${PROJECT_TARGETS[@]}"; do
  IFS=":" read -r name target <<< "$item"
  # Sync only if the folder exists OR we choose to create it
  # Here we create it because your old behavior appears to expect per-project
  sync_dir "$name" "$target"
  project_synced=$((project_synced + 1))
done

# If you want to ALSO sync global, uncomment:
# echo -e "${BLUE}🔄 Also syncing global targets...${NC}"
# for item in "${GLOBAL_TARGETS[@]}"; do
#   IFS=":" read -r name target <<< "$item"
#   sync_dir "$name" "$target"
# done

echo -e "${GREEN}✅ Sync complete (${project_synced} project target(s))${NC}"
