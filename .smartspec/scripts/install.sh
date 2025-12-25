#!/bin/bash
# SmartSpec Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash

set -e

echo "🚀 Installing SmartSpec..."

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📦 Detected OS: $MACHINE"

# Check prerequisites
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed. Please install git first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Determine installation directories
REPO_DIR="${HOME}/.smartspec-repo"
SMARTSPEC_HOME="${HOME}/.smartspec"

# Clone or update repository
if [ -d "$REPO_DIR" ]; then
    echo "📥 Updating existing SmartSpec installation..."
    cd "$REPO_DIR"
    git pull origin main
else
    echo "📥 Cloning SmartSpec repository..."
    git clone https://github.com/naibarn/SmartSpec.git "$REPO_DIR"
    cd "$REPO_DIR"
fi

# Verify .smartspec directory exists in repo
if [ ! -d "$REPO_DIR/.smartspec" ]; then
    echo "❌ Error: .smartspec directory not found in repository."
    exit 1
fi

# Verify workflows directory exists
if [ ! -d "$REPO_DIR/.smartspec/workflows" ]; then
    echo "❌ Error: Workflows directory not found after clone."
    exit 1
fi

# Verify scripts directory exists
if [ ! -d "$REPO_DIR/.smartspec/scripts" ]; then
    echo "❌ Error: Scripts directory not found after clone."
    exit 1
fi

# Create symlink to .smartspec directory
if [ -L "$SMARTSPEC_HOME" ]; then
    # Symlink exists, update it
    rm "$SMARTSPEC_HOME"
    ln -s "$REPO_DIR/.smartspec" "$SMARTSPEC_HOME"
elif [ -d "$SMARTSPEC_HOME" ]; then
    # Directory exists, backup and create symlink
    mv "$SMARTSPEC_HOME" "${SMARTSPEC_HOME}.backup.$(date +%Y%m%d_%H%M%S)"
    ln -s "$REPO_DIR/.smartspec" "$SMARTSPEC_HOME"
else
    # Create new symlink
    ln -s "$REPO_DIR/.smartspec" "$SMARTSPEC_HOME"
fi

# Install Python dependencies if requirements.txt exists
if [ -f "$REPO_DIR/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    python3 -m pip install --user -r "$REPO_DIR/requirements.txt"
fi

# Add to PATH
SHELL_RC=""
if [ -f "${HOME}/.bashrc" ]; then
    SHELL_RC="${HOME}/.bashrc"
elif [ -f "${HOME}/.zshrc" ]; then
    SHELL_RC="${HOME}/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "SMARTSPEC_HOME" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# SmartSpec" >> "$SHELL_RC"
        echo "export SMARTSPEC_HOME=\"$SMARTSPEC_HOME\"" >> "$SHELL_RC"
        echo "export PATH=\"\$SMARTSPEC_HOME/scripts:\$PATH\"" >> "$SHELL_RC"
        echo "✅ Added SmartSpec to PATH in $SHELL_RC"
    fi
fi

echo ""
echo "✅ SmartSpec installed successfully!"
echo ""
echo "📍 Repository: $REPO_DIR"
echo "📍 SmartSpec Home: $SMARTSPEC_HOME (symlink)"
echo "📁 Workflows: $SMARTSPEC_HOME/workflows/"
echo "📁 Scripts: $SMARTSPEC_HOME/scripts/"
echo ""
echo "🎯 Next steps:"
echo "   1. Reload your shell: source $SHELL_RC"
echo "   2. Verify installation: python3 \$SMARTSPEC_HOME/scripts/verify_evidence_strict.py --help"
echo "   3. Check workflows: ls \$SMARTSPEC_HOME/workflows/"
echo ""
