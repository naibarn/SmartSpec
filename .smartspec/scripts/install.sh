#!/bin/bash
# SmartSpec Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/install.sh | bash

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

# Determine installation directory
INSTALL_DIR="${HOME}/.smartspec"

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo "📥 Updating existing SmartSpec installation..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📥 Cloning SmartSpec repository..."
    git clone https://github.com/naibarn/SmartSpec.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    python3 -m pip install --user -r requirements.txt
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
        echo "export SMARTSPEC_HOME=\"$INSTALL_DIR\"" >> "$SHELL_RC"
        echo "export PATH=\"\$SMARTSPEC_HOME/.smartspec/scripts:\$PATH\"" >> "$SHELL_RC"
        echo "✅ Added SmartSpec to PATH in $SHELL_RC"
    fi
fi

echo ""
echo "✅ SmartSpec installed successfully!"
echo ""
echo "📍 Installation directory: $INSTALL_DIR"
echo ""
echo "🎯 Next steps:"
echo "   1. Reload your shell: source $SHELL_RC"
echo "   2. Verify installation: python3 \$SMARTSPEC_HOME/.smartspec/scripts/verify_evidence_strict.py --help"
echo "   3. Read the docs: https://smartspec.docs/"
echo "   4. Thai manual: https://smartspec.docs/th/"
echo ""
