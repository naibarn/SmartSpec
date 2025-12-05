#!/bin/bash

# SmartSpec Gemini CLI TOML Fix Script v2
# This script will regenerate all TOML files with correct descriptions
# Run this in your SmartSpec project directory

echo "🔧 SmartSpec Gemini CLI TOML Fix Script v2"
echo "==========================================="
echo ""

# Check if we're in SmartSpec directory
if [ ! -d ".smartspec/workflows" ]; then
    echo "❌ Error: .smartspec/workflows directory not found"
    echo "Please run this script from your SmartSpec project root directory"
    exit 1
fi

# Create target directory
TARGET_DIR=".gemini/commands"
SOURCE_DIR=".smartspec/workflows"

echo "📁 Creating directory: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Backup existing files if any
if ls "$TARGET_DIR"/*.toml >/dev/null 2>&1; then
    BACKUP_DIR=".gemini/commands.backup.$(date +%Y%m%d_%H%M%S)"
    echo "💾 Backing up existing files to: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
    cp "$TARGET_DIR"/*.toml "$BACKUP_DIR/" 2>/dev/null || true
fi

echo ""
echo "🔄 Converting workflows to TOML format..."
echo ""

CONVERTED=0
for md_file in "$SOURCE_DIR"/smartspec_*.md; do
    if [ ! -f "$md_file" ]; then
        continue
    fi
    
    filename=$(basename "$md_file" .md)
    toml_file="$TARGET_DIR/${filename}.toml"
    
    # Extract description from first # title
    description=$(grep -m 1 '^# ' "$md_file" 2>/dev/null | sed 's/^# //' || echo "")
    
    # Fallback to filename if description is empty
    if [ -z "$description" ]; then
        description="SmartSpec workflow: ${filename//_/ }"
    fi
    
    # Extract prompt content (skip frontmatter if exists)
    frontmatter_end=$(grep -n '^---$' "$md_file" 2>/dev/null | sed -n '2p' | cut -d: -f1 || echo "")
    if [ -n "$frontmatter_end" ]; then
        # Skip frontmatter
        prompt=$(tail -n +$((frontmatter_end + 1)) "$md_file" || echo "")
    else
        # No frontmatter, use entire file
        prompt=$(cat "$md_file" || echo "")
    fi
    
    # Create TOML file using cat with heredoc
    # Note: Using cat instead of printf to avoid escaping issues
    cat > "$toml_file" <<TOMLEOF
description = "$description"

prompt = """
$prompt
"""
TOMLEOF
    
    if [ -f "$toml_file" ]; then
        ((CONVERTED++)) || true
        echo "  ✅ $filename"
    else
        echo "  ❌ Failed: $filename"
    fi
done

echo ""
echo "✅ Conversion complete: $CONVERTED workflows converted"
echo ""

if [ $CONVERTED -gt 0 ]; then
    echo "📊 Generated files:"
    for toml_file in "$TARGET_DIR"/*.toml; do
        if [ -f "$toml_file" ]; then
            desc=$(head -1 "$toml_file" 2>/dev/null | sed 's/description = //' | sed 's/"//g' || echo "N/A")
            echo "  - $(basename "$toml_file"): $desc"
        fi
    done
    
    echo ""
    echo "🎉 Done! All TOML files have been regenerated with correct descriptions."
    echo ""
    echo "You can now use Gemini CLI workflows:"
    echo "  gemini chat --workflow .gemini/commands/smartspec_fix_errors.toml"
else
    echo "❌ No workflows were converted. Please check if .smartspec/workflows/ contains markdown files."
fi
