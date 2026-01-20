#!/bin/bash

# verify_gemini.sh - Verify Gemini capsule generation
#
# Validates that gemini content was generated correctly:
# - Checks directory structure
# - Counts posts, tags, year archives
# - Validates gemtext syntax
# - Checks required files
#
# Usage:
#   bash tests/verify_gemini.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    FAILED=$((FAILED + 1))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

info() {
    echo -e "  $1"
}

# Configuration
GEMINI_DIR="_gemini"
EXPECTED_POSTS=30
EXPECTED_TAGS=63
EXPECTED_YEARS=8

echo "=== Gemini Capsule Verification ==="
echo

# Check if _gemini directory exists
echo "Checking directory structure..."
if [ -d "$GEMINI_DIR" ]; then
    pass "Directory $_GEMINI_DIR exists"
else
    fail "Directory $_GEMINI_DIR not found"
    exit 1
fi

# Check required subdirectories
for dir in blog tags; do
    if [ -d "$GEMINI_DIR/$dir" ]; then
        pass "Directory $_GEMINI_DIR/$dir exists"
    else
        fail "Directory $_GEMINI_DIR/$dir not found"
    fi
done

echo

# Check required root files
echo "Checking required files..."
for file in index.gmi about.gmi contact.gmi; do
    if [ -f "$GEMINI_DIR/$file" ]; then
        pass "File $file exists"
    else
        fail "File $file not found"
    fi
done

# Check blog index
if [ -f "$GEMINI_DIR/blog/index.gmi" ]; then
    pass "File blog/index.gmi exists"
else
    fail "File blog/index.gmi not found"
fi

# Check tags index
if [ -f "$GEMINI_DIR/tags/index.gmi" ]; then
    pass "File tags/index.gmi exists"
else
    fail "File tags/index.gmi not found"
fi

echo

# Count posts
echo "Counting posts..."
POST_COUNT=$(find "$GEMINI_DIR/blog" -name "*.gmi" -type f ! -name "index.gmi" | wc -l)
if [ "$POST_COUNT" -eq "$EXPECTED_POSTS" ]; then
    pass "Found $POST_COUNT posts (expected $EXPECTED_POSTS)"
else
    warn "Found $POST_COUNT posts (expected $EXPECTED_POSTS)"
fi

echo

# Count tag pages
echo "Counting tag pages..."
TAG_COUNT=$(find "$GEMINI_DIR/tags" -name "*.gmi" -type f ! -name "index.gmi" | wc -l)
if [ "$TAG_COUNT" -eq "$EXPECTED_TAGS" ]; then
    pass "Found $TAG_COUNT tag pages (expected $EXPECTED_TAGS)"
else
    warn "Found $TAG_COUNT tag pages (expected $EXPECTED_TAGS)"
fi

echo

# Count year archives
echo "Counting year archives..."
YEAR_COUNT=$(find "$GEMINI_DIR/blog" -type d -name "[0-9][0-9][0-9][0-9]" | wc -l)
if [ "$YEAR_COUNT" -eq "$EXPECTED_YEARS" ]; then
    pass "Found $YEAR_COUNT year directories (expected $EXPECTED_YEARS)"
else
    warn "Found $YEAR_COUNT year directories (expected $EXPECTED_YEARS)"
fi

# Check year index files
YEAR_INDEX_COUNT=$(find "$GEMINI_DIR/blog" -path "*/[0-9][0-9][0-9][0-9]/index.gmi" -type f | wc -l)
if [ "$YEAR_INDEX_COUNT" -eq "$EXPECTED_YEARS" ]; then
    pass "Found $YEAR_INDEX_COUNT year index files (expected $EXPECTED_YEARS)"
else
    warn "Found $YEAR_INDEX_COUNT year index files (expected $EXPECTED_YEARS)"
fi

echo

# Validate gemtext syntax
echo "Validating gemtext syntax..."

# Check for valid gemtext link syntax (=> URL [text])
INVALID_LINKS=$(grep -r "^\[" "$GEMINI_DIR" --include="*.gmi" | wc -l)
if [ "$INVALID_LINKS" -eq 0 ]; then
    pass "No markdown link syntax found (all converted to gemtext)"
else
    warn "Found $INVALID_LINKS lines with markdown link syntax"
fi

# Check for HTML tags
HTML_TAGS=$(grep -r "<[^>]*>" "$GEMINI_DIR" --include="*.gmi" | grep -v "^.*:\`\`\`" | wc -l)
if [ "$HTML_TAGS" -eq 0 ]; then
    pass "No HTML tags found"
else
    warn "Found $HTML_TAGS lines with HTML tags"
fi

# Check that gemtext links start with =>
GEMTEXT_LINKS=$(grep -r "^=> " "$GEMINI_DIR" --include="*.gmi" | wc -l)
if [ "$GEMTEXT_LINKS" -gt 0 ]; then
    pass "Found $GEMTEXT_LINKS gemtext links"
else
    fail "No gemtext links found (expected many)"
fi

# Check that headings use # syntax
HEADINGS=$(grep -r "^#" "$GEMINI_DIR" --include="*.gmi" | wc -l)
if [ "$HEADINGS" -gt 0 ]; then
    pass "Found $HEADINGS headings"
else
    warn "No headings found (expected many)"
fi

# Check that lists use * syntax
LISTS=$(grep -r "^\* " "$GEMINI_DIR" --include="*.gmi" | wc -l)
if [ "$LISTS" -gt 0 ]; then
    pass "Found $LISTS list items"
else
    warn "No list items found"
fi

# Check for code blocks
CODE_BLOCKS=$(grep -rE "^\`\`\`" "$GEMINI_DIR" --include="*.gmi" | wc -l)
if [ "$CODE_BLOCKS" -gt 0 ]; then
    pass "Found $CODE_BLOCKS code block markers"
else
    info "No code blocks found (acceptable)"
fi

echo

# Check specific year directories
echo "Checking expected year directories..."
for year in 2011 2015 2017 2021 2022 2023 2024 2025; do
    if [ -d "$GEMINI_DIR/blog/$year" ]; then
        if [ -f "$GEMINI_DIR/blog/$year/index.gmi" ]; then
            pass "Year $year has directory and index"
        else
            fail "Year $year missing index.gmi"
        fi
    else
        fail "Year $year directory not found"
    fi
done

echo

# Summary
echo "=== Verification Summary ==="
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
fi
if [ "$FAILED" -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
fi

echo

# Exit with appropriate code
if [ "$FAILED" -gt 0 ]; then
    echo -e "${RED}Verification FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}Verification PASSED${NC}"
    exit 0
fi
