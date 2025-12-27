#!/bin/bash
#
# Verification Script for Exercise 1: Basic Validation
#
# This script verifies that Exercise 1 was completed successfully.
#

set -e

echo "🔍 Verifying Exercise 1: Basic Validation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Check if file exists
check_file_exists() {
    local file=$1
    echo -n "✓ Checking if $file exists... "
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found: $file"
        ((FAILED++))
        return 1
    fi
}

# Check if file has content
check_file_content() {
    local file=$1
    local min_lines=$2
    echo -n "✓ Checking if $file has content (min $min_lines lines)... "
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found"
        ((FAILED++))
        return 1
    fi
    
    local lines=$(wc -l < "$file")
    
    if [ "$lines" -ge "$min_lines" ]; then
        echo -e "${GREEN}PASS${NC} ($lines lines)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → File has only $lines lines, expected at least $min_lines"
        ((FAILED++))
        return 1
    fi
}

# Check if validation passes
check_validation_passes() {
    local file=$1
    echo -n "✓ Checking if $file passes validation... "
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found"
        ((FAILED++))
        return 1
    fi
    
    # Run validator
    local validator="$HOME/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py"
    
    if [ ! -f "$validator" ]; then
        echo -e "${YELLOW}SKIP${NC}"
        echo "  → Validator not found: $validator"
        return 0
    fi
    
    # Capture output
    local output=$(python3 "$validator" "$file" 2>&1)
    local exit_code=$?
    
    # Check for errors
    if echo "$output" | grep -q "Errors: 0"; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Validation found errors:"
        echo "$output" | grep "Errors:" | head -1
        ((FAILED++))
        return 1
    fi
}

# Check if TODO placeholders are replaced
check_no_todos() {
    local file=$1
    local max_todos=$2
    echo -n "✓ Checking if TODO placeholders are replaced... "
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found"
        ((FAILED++))
        return 1
    fi
    
    local todo_count=$(grep -c "TODO:" "$file" || true)
    
    if [ "$todo_count" -le "$max_todos" ]; then
        echo -e "${GREEN}PASS${NC} ($todo_count TODOs remaining)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Found $todo_count TODO placeholders, expected max $max_todos"
        echo "  → Please replace TODO placeholders with real content"
        ((FAILED++))
        return 1
    fi
}

# Check if required sections exist
check_sections_exist() {
    local file=$1
    shift
    local sections=("$@")
    
    echo "✓ Checking if required sections exist..."
    
    if [ ! -f "$file" ]; then
        echo -e "  ${RED}FAIL${NC} - File not found"
        ((FAILED++))
        return 1
    fi
    
    local all_found=true
    
    for section in "${sections[@]}"; do
        echo -n "  - $section... "
        
        if grep -q "^## $section" "$file"; then
            echo -e "${GREEN}FOUND${NC}"
        else
            echo -e "${RED}MISSING${NC}"
            all_found=false
        fi
    done
    
    if [ "$all_found" = true ]; then
        ((PASSED++))
        return 0
    else
        ((FAILED++))
        return 1
    fi
}

# Main verification
main() {
    local exercise_file="${1:-todo-api-spec.md}"
    
    echo "Target file: $exercise_file"
    echo ""
    
    # Run checks
    check_file_exists "$exercise_file"
    check_file_content "$exercise_file" 50
    check_sections_exist "$exercise_file" "Problem" "Solution" "Requirements" "Architecture" "Implementation"
    check_no_todos "$exercise_file" 3
    check_validation_passes "$exercise_file"
    
    # Summary
    echo ""
    echo "=========================================="
    echo "Summary:"
    echo "  Passed: $PASSED"
    echo "  Failed: $FAILED"
    echo ""
    
    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✅ All checks passed! Exercise 1 completed successfully!${NC}"
        echo ""
        echo "🎉 Congratulations! You've completed Exercise 1!"
        echo ""
        echo "Next steps:"
        echo "  1. Review your spec file"
        echo "  2. Move on to Exercise 2"
        echo "  3. Try the intermediate learning path"
        return 0
    else
        echo -e "${RED}❌ Some checks failed. Please review and fix the issues.${NC}"
        echo ""
        echo "Tips:"
        echo "  - Make sure the file exists"
        echo "  - Run validation: python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py $exercise_file"
        echo "  - Apply auto-fix: python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py $exercise_file --apply"
        echo "  - Replace TODO placeholders with real content"
        return 1
    fi
}

# Run main function
main "$@"
