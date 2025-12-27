#!/bin/bash
#
# Verification Script for Exercise 2: Integration
#
# This script verifies that Exercise 2 was completed successfully.
#

set -e

echo "🔍 Verifying Exercise 2: Integration"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Check if directory exists
check_directory_exists() {
    local dir=$1
    echo -n "✓ Checking if directory $dir exists... "
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Directory not found: $dir"
        ((FAILED++))
        return 1
    fi
}

# Check if file exists and is executable
check_executable_exists() {
    local file=$1
    echo -n "✓ Checking if $file exists and is executable... "
    
    if [ -f "$file" ]; then
        if [ -x "$file" ]; then
            echo -e "${GREEN}PASS${NC}"
            ((PASSED++))
            return 0
        else
            echo -e "${YELLOW}WARN${NC}"
            echo "  → File exists but is not executable"
            echo "  → Run: chmod +x $file"
            ((PASSED++))
            return 0
        fi
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found: $file"
        ((FAILED++))
        return 1
    fi
}

# Check if script has required content
check_script_content() {
    local file=$1
    local pattern=$2
    local description=$3
    echo -n "✓ Checking if $file contains $description... "
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → File not found"
        ((FAILED++))
        return 1
    fi
    
    if grep -q "$pattern" "$file"; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Pattern not found: $pattern"
        ((FAILED++))
        return 1
    fi
}

# Check if pre-commit hook is installed
check_precommit_hook() {
    local hook_file=".git/hooks/pre-commit"
    echo -n "✓ Checking if pre-commit hook is installed... "
    
    if [ -f "$hook_file" ]; then
        if [ -x "$hook_file" ]; then
            echo -e "${GREEN}PASS${NC}"
            ((PASSED++))
            return 0
        else
            echo -e "${YELLOW}WARN${NC}"
            echo "  → Hook exists but is not executable"
            echo "  → Run: chmod +x $hook_file"
            ((PASSED++))
            return 0
        fi
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Pre-commit hook not found: $hook_file"
        ((FAILED++))
        return 1
    fi
}

# Check if spec files exist
check_spec_files() {
    local spec_dir=$1
    local min_files=$2
    echo -n "✓ Checking if spec files exist (min $min_files files)... "
    
    if [ ! -d "$spec_dir" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → Directory not found: $spec_dir"
        ((FAILED++))
        return 1
    fi
    
    local file_count=$(find "$spec_dir" -name "*.md" -type f | wc -l)
    
    if [ "$file_count" -ge "$min_files" ]; then
        echo -e "${GREEN}PASS${NC} ($file_count files found)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Found only $file_count files, expected at least $min_files"
        ((FAILED++))
        return 1
    fi
}

# Test validation script
test_validation_script() {
    local script=$1
    echo -n "✓ Testing validation script... "
    
    if [ ! -f "$script" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  → Script not found: $script"
        ((FAILED++))
        return 1
    fi
    
    if [ ! -x "$script" ]; then
        echo -e "${YELLOW}WARN${NC}"
        echo "  → Script not executable, making it executable..."
        chmod +x "$script"
    fi
    
    # Try to run script (dry run)
    if bash -n "$script" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  → Script has syntax errors"
        ((FAILED++))
        return 1
    fi
}

# Main verification
main() {
    local project_dir="${1:-my-project}"
    
    echo "Target directory: $project_dir"
    echo ""
    
    # Check directory structure
    check_directory_exists "$project_dir"
    check_directory_exists "$project_dir/.spec"
    check_directory_exists "$project_dir/.spec/requirements"
    
    # Check scripts
    check_executable_exists "$project_dir/validate-all.sh"
    check_script_content "$project_dir/validate-all.sh" "validate_spec_from_prompt.py" "validator call"
    
    # Check pre-commit hook
    if [ -d "$project_dir/.git" ]; then
        cd "$project_dir"
        check_precommit_hook
        cd - > /dev/null
    else
        echo -e "${YELLOW}⚠ Git repository not initialized, skipping pre-commit hook check${NC}"
    fi
    
    # Check spec files
    check_spec_files "$project_dir/.spec" 2
    
    # Test validation script
    test_validation_script "$project_dir/validate-all.sh"
    
    # Summary
    echo ""
    echo "====================================="
    echo "Summary:"
    echo "  Passed: $PASSED"
    echo "  Failed: $FAILED"
    echo ""
    
    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✅ All checks passed! Exercise 2 completed successfully!${NC}"
        echo ""
        echo "🎉 Congratulations! You've completed Exercise 2!"
        echo ""
        echo "Your validation pipeline is ready to use:"
        echo "  1. Run: cd $project_dir && ./validate-all.sh"
        echo "  2. Try committing a spec file to test pre-commit hook"
        echo "  3. Move on to Exercise 3 (Advanced)"
        return 0
    else
        echo -e "${RED}❌ Some checks failed. Please review and fix the issues.${NC}"
        echo ""
        echo "Tips:"
        echo "  - Create directory structure: mkdir -p $project_dir/.spec/requirements"
        echo "  - Create validation script: $project_dir/validate-all.sh"
        echo "  - Install pre-commit hook: .git/hooks/pre-commit"
        echo "  - Create at least 2 spec files in .spec directory"
        return 1
    fi
}

# Run main function
main "$@"
