#!/bin/bash
# SmartSpec Markdown to TOML Converter
# Converts SmartSpec Markdown workflows to Gemini CLI TOML format
# Version: 1.1

# Note: Removed 'set -e' to allow script to continue even if some commands return non-zero
# (e.g., grep -q when pattern not found)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to escape special characters for TOML
escape_toml_string() {
    local input="$1"
    # Escape backslashes first
    input="${input//\\/\\\\}"
    # Escape double quotes
    input="${input//\"/\\\"}"
    # Escape newlines (keep as actual newlines in multi-line strings)
    echo "$input"
}

# Function to extract description from markdown
extract_description() {
    local md_file="$1"
    local description=""
    
    # Try to find description in various formats
    # 1. Look for first # title (works even with frontmatter)
    description=$(grep -m 1 '^# ' "$md_file" 2>/dev/null | sed 's/^# //' || true)
    
    # 2. If not found, look for "# Description" or "## Description" section
    if [ -z "$description" ]; then
        if grep -q "^#\+ Description" "$md_file" 2>/dev/null || true; then
            description=$(sed -n '/^#\+ Description/,/^#/p' "$md_file" | sed '1d;$d' | head -n 1 | sed 's/^[[:space:]]*//' || true)
        fi
    fi
    
    # 3. If still not found, use filename
    if [ -z "$description" ]; then
        local filename=$(basename "$md_file" .md)
        description="SmartSpec workflow: ${filename//_/ }"
    fi
    
    # Limit to 100 characters
    if [ ${#description} -gt 100 ]; then
        description="${description:0:97}..."
    fi
    
    echo "$description"
}

# Function to extract prompt content from markdown
extract_prompt() {
    local md_file="$1"
    local prompt=""
    
    # Remove the first title line and extract the rest
    # Note: No escaping here - printf handles it correctly
    prompt=$(tail -n +2 "$md_file")
    
    echo "$prompt"
}

# Function to convert a single markdown file to TOML
convert_workflow() {
    local md_file="$1"
    local toml_file="$2"
    
    if [ ! -f "$md_file" ]; then
        echo -e "${RED}❌ Error: Source file not found: $md_file${NC}"
        return 1
    fi
    
    # Extract description and prompt
    local description=$(extract_description "$md_file")
    local prompt=$(extract_prompt "$md_file")
    
    # Escape description for TOML
    description=$(escape_toml_string "$description")
    
    # Create TOML file using printf to avoid heredoc issues with special characters
    printf '%s\n\n%s\n%s\n%s\n' \
        "description = \"$description\"" \
        'prompt = """' \
        "$prompt" \
        '"""' > "$toml_file"
    
    return 0
}

# Main conversion function
convert_all_workflows() {
    local source_dir="$1"
    local target_dir="$2"
    
    if [ ! -d "$source_dir" ]; then
        echo -e "${RED}❌ Error: Source directory not found: $source_dir${NC}"
        return 1
    fi
    
    # Create target directory
    mkdir -p "$target_dir"
    
    local count=0
    local failed=0
    
    # Convert all smartspec_*.md files
    for md_file in "$source_dir"/smartspec_*.md; do
        if [ ! -f "$md_file" ]; then
            continue
        fi
        
        local filename=$(basename "$md_file" .md)
        local toml_file="$target_dir/${filename}.toml"
        
        if convert_workflow "$md_file" "$toml_file"; then
            echo -e "  ${GREEN}✅ Converted: $filename${NC}"
            ((count++))
        else
            echo -e "  ${RED}❌ Failed: $filename${NC}"
            ((failed++))
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ Conversion complete: $count workflows converted${NC}"
    if [ $failed -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $failed workflows failed${NC}"
    fi
    
    return 0
}

# Usage information
usage() {
    echo "Usage: $0 <source_dir> <target_dir>"
    echo ""
    echo "Convert SmartSpec Markdown workflows to Gemini CLI TOML format"
    echo ""
    echo "Arguments:"
    echo "  source_dir  Directory containing Markdown workflows (*.md)"
    echo "  target_dir  Directory where TOML files will be created"
    echo ""
    echo "Example:"
    echo "  $0 .smartspec/workflows .gemini/commands"
}

# Main script
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
    exit 0
fi

if [ $# -ne 2 ]; then
    echo -e "${RED}Error: Invalid number of arguments${NC}"
    echo ""
    usage
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

echo "🔄 Converting SmartSpec workflows to TOML format..."
echo "  Source: $SOURCE_DIR"
echo "  Target: $TARGET_DIR"
echo ""

convert_all_workflows "$SOURCE_DIR" "$TARGET_DIR"

exit $?
