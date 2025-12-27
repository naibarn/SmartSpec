#!/bin/bash
#
# Install SmartSpec Git hooks
#
# Usage:
#   bash .smartspec/scripts/install_hooks.sh
#

set -e

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

echo "📦 Installing SmartSpec Git hooks..."
echo "   Repo: $REPO_ROOT"
echo ""

# Check if .git directory exists
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "❌ Error: Not a Git repository"
    echo "   No .git directory found in $REPO_ROOT"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$REPO_ROOT/.git/hooks"

# Install pre-commit hook
HOOK_SOURCE="$REPO_ROOT/.smartspec/hooks/pre-commit-naming-convention"
HOOK_TARGET="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$HOOK_SOURCE" ]; then
    echo "❌ Error: Hook source not found"
    echo "   Expected: $HOOK_SOURCE"
    exit 1
fi

# Check if pre-commit hook already exists
if [ -f "$HOOK_TARGET" ] || [ -L "$HOOK_TARGET" ]; then
    echo "⚠️  Pre-commit hook already exists: $HOOK_TARGET"
    echo ""
    read -p "   Overwrite? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled"
        exit 1
    fi
    rm -f "$HOOK_TARGET"
fi

# Create symlink
ln -sf "../../.smartspec/hooks/pre-commit-naming-convention" "$HOOK_TARGET"
chmod +x "$HOOK_TARGET"

echo "✅ Pre-commit hook installed: $HOOK_TARGET"
echo ""

# Test hook
echo "🧪 Testing hook..."
if [ -x "$HOOK_TARGET" ]; then
    echo "✅ Hook is executable"
else
    echo "❌ Hook is not executable"
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "The pre-commit hook will now validate naming convention"
echo "for all staged TypeScript/JavaScript files before commit."
echo ""
echo "To bypass (not recommended):"
echo "  git commit --no-verify"
echo ""
echo "To uninstall:"
echo "  rm $HOOK_TARGET"
echo ""
