#!/bin/bash
# verify_gopher.sh - Verify gopher content structure and counts

set -e

GOPHER_DIR="_gopher"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Gopher Content Verification ==="
echo ""

# Check if gopher directory exists
if [ ! -d "$GOPHER_DIR" ]; then
    echo -e "${RED}✗ Error: $GOPHER_DIR directory not found${NC}"
    echo "  Run: python3 _scripts/manage.py gopher"
    exit 1
fi

# Count markdown posts (2015-2026)
EXPECTED_POSTS=30
POST_COUNT=$(find "$GOPHER_DIR/blog" -name "*.txt" -type f | wc -l)

if [ "$POST_COUNT" -eq "$EXPECTED_POSTS" ]; then
    echo -e "${GREEN}✓ All $EXPECTED_POSTS markdown posts generated${NC}"
else
    echo -e "${YELLOW}⚠ Found $POST_COUNT posts, expected $EXPECTED_POSTS${NC}"
fi

# Count tag pages
TAG_COUNT=$(find "$GOPHER_DIR/tags" -mindepth 1 -maxdepth 1 -type d | wc -l)
echo -e "${GREEN}✓ $TAG_COUNT tag pages generated${NC}"

# Count year archives
YEAR_COUNT=$(find "$GOPHER_DIR/blog" -mindepth 1 -maxdepth 1 -type d | wc -l)
echo -e "${GREEN}✓ $YEAR_COUNT year archive directories${NC}"

# Check required files
REQUIRED_FILES=(
    "$GOPHER_DIR/gophermap"
    "$GOPHER_DIR/blog/gophermap"
    "$GOPHER_DIR/tags/gophermap"
    "$GOPHER_DIR/about.txt"
    "$GOPHER_DIR/contact.txt"
)

echo ""
echo "Checking required files:"
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}✗ Missing: $file${NC}"
    fi
done

# Validate gophermap syntax (basic check)
echo ""
echo "Validating gophermap syntax:"

validate_gophermap() {
    local file=$1
    local errors=0

    # Check for proper line format (type + title + tab + path + tab + host + tab + port)
    # Info lines (i) can omit host/port
    while IFS= read -r line; do
        # Skip empty lines
        [ -z "$line" ] && continue

        # Get first character (type code)
        type="${line:0:1}"

        # Info lines (i) are simple, just need type
        if [ "$type" = "i" ]; then
            continue
        fi

        # Other types need tabs
        if [[ ! "$line" =~ $'\t' ]]; then
            errors=$((errors + 1))
        fi
    done < "$file"

    if [ $errors -eq 0 ]; then
        echo -e "${GREEN}✓ $(basename $file)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ $(basename $file): $errors potential issues${NC}"
        return 1
    fi
}

validate_gophermap "$GOPHER_DIR/gophermap"
validate_gophermap "$GOPHER_DIR/blog/gophermap"
validate_gophermap "$GOPHER_DIR/tags/gophermap"

# Check a sample year gophermap
SAMPLE_YEAR="$GOPHER_DIR/blog/2025/gophermap"
if [ -f "$SAMPLE_YEAR" ]; then
    validate_gophermap "$SAMPLE_YEAR"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "Summary:"
echo "  Posts: $POST_COUNT"
echo "  Tags: $TAG_COUNT"
echo "  Years: $YEAR_COUNT"
echo ""
echo "To test with Docker:"
echo "  docker compose -f docker-compose.gopher.yml up -d"
echo "  curl gopher://localhost:70/"
echo ""
