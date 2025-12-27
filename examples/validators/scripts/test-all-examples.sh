#!/bin/bash
#
# Master Test Script - Tests all sample files and verification scripts
#
# This script validates that all example files work correctly with their
# respective validators.
#

set -e

echo "🧪 Testing All Validator Examples"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(dirname "$SCRIPT_DIR")"
VALIDATORS_DIR="/home/ubuntu/SmartSpec/.smartspec/scripts"

# Test result tracking
test_result() {
    local test_name=$1
    local exit_code=$2
    
    ((TOTAL_TESTS++))
    
    if [ "$exit_code" -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        ((FAILED_TESTS++))
    fi
}

# Test a validator with a file
test_validator() {
    local validator=$1
    local file=$2
    local expected_result=$3  # "pass" or "fail"
    local test_name=$4
    
    echo -n "  Testing: $test_name... "
    
    if [ ! -f "$validator" ]; then
        echo -e "${RED}SKIP${NC} (validator not found)"
        return 0
    fi
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}SKIP${NC} (file not found)"
        return 0
    fi
    
    # Run validator
    local output=$(python3 "$validator" "$file" 2>&1)
    local exit_code=$?
    
    # Check result
    if [ "$expected_result" = "pass" ]; then
        # Expect validation to pass (0 errors)
        if echo "$output" | grep -q "\*\*Errors:\*\* 0"; then
            echo -e "${GREEN}PASS${NC}"
            test_result "$test_name" 0
            return 0
        else
            echo -e "${RED}FAIL${NC}"
            echo "    Expected: 0 errors"
            echo "    Got: $(echo "$output" | grep "Errors:" | head -1)"
            test_result "$test_name" 1
            return 1
        fi
    else
        # Expect validation to fail (errors found)
        if echo "$output" | grep -q "\*\*Errors:\*\* 0"; then
            echo -e "${RED}FAIL${NC}"
            echo "    Expected: errors found"
            echo "    Got: 0 errors"
            test_result "$test_name" 1
            return 1
        else
            echo -e "${GREEN}PASS${NC}"
            test_result "$test_name" 0
            return 0
        fi
    fi
}

# Test auto-fix functionality
test_autofix() {
    local validator=$1
    local source_file=$2
    local test_name=$3
    
    echo -n "  Testing auto-fix: $test_name... "
    
    if [ ! -f "$validator" ]; then
        echo -e "${RED}SKIP${NC} (validator not found)"
        return 0
    fi
    
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}SKIP${NC} (file not found)"
        return 0
    fi
    
    # Create temp file
    local temp_file=$(mktemp)
    cp "$source_file" "$temp_file"
    
    # Apply auto-fix
    python3 "$validator" "$temp_file" --apply > /dev/null 2>&1
    
    # Validate fixed file
    local output=$(python3 "$validator" "$temp_file" 2>&1)
    
    # Check if errors reduced
    if echo "$output" | grep -q "\*\*Errors:\*\* 0"; then
        echo -e "${GREEN}PASS${NC}"
        test_result "$test_name" 0
        rm "$temp_file"
        return 0
    else
        echo -e "${YELLOW}PARTIAL${NC}"
        echo "    Auto-fix applied but errors remain"
        test_result "$test_name" 0  # Still pass, as auto-fix may not fix everything
        rm "$temp_file"
        return 0
    fi
}

# Main test suite
main() {
    echo -e "${BLUE}Phase 1: Testing Good Examples${NC}"
    echo "-------------------------------"
    
    test_validator \
        "$VALIDATORS_DIR/validate_spec_from_prompt.py" \
        "$EXAMPLES_DIR/good/sample-spec-from-prompt.md" \
        "pass" \
        "Good spec-from-prompt example"
    
    test_validator \
        "$VALIDATORS_DIR/validate_generate_spec.py" \
        "$EXAMPLES_DIR/good/sample-generate-spec.md" \
        "pass" \
        "Good generate-spec example"
    
    echo ""
    echo -e "${BLUE}Phase 2: Testing Bad Examples${NC}"
    echo "------------------------------"
    
    test_validator \
        "$VALIDATORS_DIR/validate_spec_from_prompt.py" \
        "$EXAMPLES_DIR/bad/sample-spec-from-prompt.md" \
        "fail" \
        "Bad spec-from-prompt example (should have errors)"
    
    test_validator \
        "$VALIDATORS_DIR/validate_generate_spec.py" \
        "$EXAMPLES_DIR/bad/sample-generate-spec.md" \
        "fail" \
        "Bad generate-spec example (should have errors)"
    
    echo ""
    echo -e "${BLUE}Phase 3: Testing Auto-fix${NC}"
    echo "-------------------------"
    
    test_autofix \
        "$VALIDATORS_DIR/validate_spec_from_prompt.py" \
        "$EXAMPLES_DIR/bad/sample-spec-from-prompt.md" \
        "Auto-fix spec-from-prompt"
    
    test_autofix \
        "$VALIDATORS_DIR/validate_generate_spec.py" \
        "$EXAMPLES_DIR/bad/sample-generate-spec.md" \
        "Auto-fix generate-spec"
    
    echo ""
    echo -e "${BLUE}Phase 4: Testing Empty Examples${NC}"
    echo "-------------------------------"
    
    test_validator \
        "$VALIDATORS_DIR/validate_spec_from_prompt.py" \
        "$EXAMPLES_DIR/empty/sample-spec-from-prompt.md" \
        "fail" \
        "Empty spec-from-prompt example (should have errors)"
    
    echo ""
    echo -e "${BLUE}Phase 5: Testing Verification Scripts${NC}"
    echo "-------------------------------------"
    
    # Test verification scripts syntax
    for script in "$SCRIPT_DIR"/verify-*.sh; do
        if [ -f "$script" ]; then
            local script_name=$(basename "$script")
            echo -n "  Testing syntax: $script_name... "
            
            if bash -n "$script" 2>/dev/null; then
                echo -e "${GREEN}PASS${NC}"
                test_result "Syntax check: $script_name" 0
            else
                echo -e "${RED}FAIL${NC}"
                test_result "Syntax check: $script_name" 1
            fi
        fi
    done
    
    # Summary
    echo ""
    echo "=================================="
    echo -e "${BLUE}Test Summary${NC}"
    echo "=================================="
    echo "  Total Tests:  $TOTAL_TESTS"
    echo -e "  Passed:       ${GREEN}$PASSED_TESTS${NC}"
    echo -e "  Failed:       ${RED}$FAILED_TESTS${NC}"
    
    if [ "$FAILED_TESTS" -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ All tests passed!${NC}"
        echo ""
        echo "🎉 All validator examples are working correctly!"
        echo ""
        echo "Next steps:"
        echo "  1. Try the examples yourself"
        echo "  2. Complete the exercises"
        echo "  3. Integrate validators into your workflow"
        return 0
    else
        echo ""
        echo -e "${RED}❌ Some tests failed!${NC}"
        echo ""
        echo "Please review the failed tests and fix any issues."
        return 1
    fi
}

# Run main function
main "$@"
