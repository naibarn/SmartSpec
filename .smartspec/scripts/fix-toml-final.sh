#!/usr/bin/env bash

echo "🔧 SmartSpec Gemini CLI TOML Fix Script (Final Version)"
echo "========================================================"
echo ""

# Check if .smartspec directory exists
if [ ! -d ".smartspec" ]; then
    echo "❌ Error: .smartspec directory not found"
    echo "   Please run this script from your SmartSpec project root"
    exit 1
fi

# Create .gemini/commands directory
COMMANDS_DIR=".gemini/commands"
mkdir -p "$COMMANDS_DIR"
echo "📁 Creating directory: $COMMANDS_DIR"

# Backup existing files if any
if [ -d "$COMMANDS_DIR" ] && [ "$(ls -A $COMMANDS_DIR 2>/dev/null)" ]; then
    BACKUP_DIR="${COMMANDS_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "💾 Backing up existing files to: $BACKUP_DIR"
    mv "$COMMANDS_DIR" "$BACKUP_DIR"
    mkdir -p "$COMMANDS_DIR"
fi

echo ""
echo "🔄 Converting workflows to TOML format..."
echo ""

CONVERTED=0

for md_file in .smartspec/workflows/smartspec_*.md; do
    if [ ! -f "$md_file" ]; then
        continue
    fi
    
    filename=$(basename "$md_file" .md)
    toml_file="$COMMANDS_DIR/${filename}.toml"
    
    # Extract description from first # heading (NO ESCAPING!)
    description=$(grep -m 1 '^# ' "$md_file" | sed 's/^# //')
    
    # Fallback to filename if no description found
    if [ -z "$description" ]; then
        description="SmartSpec workflow: ${filename//_/ }"
    fi
    
    # Extract content after frontmatter
    frontmatter_end=$(grep -n '^---$' "$md_file" | sed -n '2p' | cut -d: -f1)
    if [ -n "$frontmatter_end" ]; then
        # Has frontmatter, extract from after second ---
        prompt=$(tail -n +$((frontmatter_end + 1)) "$md_file")
    else
        # No frontmatter, extract from line 2
        prompt=$(tail -n +2 "$md_file")
    fi
    
    # Create TOML file using echo (NO ESCAPING!)
    {
        echo "description = \"$description\""
        echo ""
        echo 'prompt = """'
        echo "$prompt"
        echo '"""'
    } > "$toml_file"
    
    echo "  ✅ $filename"
    echo "     Description: $description"
    
    ((CONVERTED++))
done

echo ""
echo "✅ Conversion complete: $CONVERTED workflows converted"
echo ""
echo "📊 Generated files:"
for toml_file in "$COMMANDS_DIR"/*.toml; do
    if [ -f "$toml_file" ]; then
        desc=$(grep '^description = ' "$toml_file" | sed 's/description = "//' | sed 's/"$//')
        echo "  - $(basename "$toml_file"): $desc"
    fi
done

echo ""
echo "🎉 Done! All TOML files have been regenerated with correct descriptions."
echo ""
echo "You can now use Gemini CLI workflows:"
echo "  gemini chat --workflow .gemini/commands/smartspec_fix_errors.toml"
