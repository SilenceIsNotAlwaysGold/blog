#!/bin/bash

# API Testing Script for Personal Blog Backend
# Tests all API endpoints with actual requests

BASE_URL="http://localhost:8001"
API_PREFIX="/api/v1"

echo "========================================="
echo "Personal Blog API Testing"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test API endpoint
test_api() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local expected_status=$5

    echo -n "Testing: $description ... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$API_PREFIX$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL$API_PREFIX$endpoint")
    fi

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}PASS${NC} (Status: $status_code)"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        echo "Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "========================================="
echo "1. Articles API Tests"
echo "========================================="

test_api "GET" "/articles?board=tech&is_published=true&page=1&page_size=10" "Get tech articles (page 1)" "" "200"
test_api "GET" "/articles?board=tech&is_published=true&page=2&page_size=10" "Get tech articles (page 2)" "" "200"
test_api "GET" "/articles?board=tech&is_published=true&category_id=6977418e4ab66bba578b11a3&page=1&page_size=10" "Get articles by category" "" "200"

# Get first article ID for detail test
ARTICLE_ID=$(curl -s "$BASE_URL$API_PREFIX/articles?board=tech&is_published=true&page=1&page_size=1" | grep -o '"_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$ARTICLE_ID" ]; then
    test_api "GET" "/articles/$ARTICLE_ID" "Get article detail" "" "200"
else
    echo -e "${YELLOW}SKIP${NC}: Could not get article ID for detail test"
fi

echo ""
echo "========================================="
echo "2. Categories API Tests"
echo "========================================="

test_api "GET" "/categories?board=tech" "Get tech categories" "" "200"
test_api "GET" "/categories?board=life" "Get life categories" "" "200"

echo ""
echo "========================================="
echo "3. Likes API Tests"
echo "========================================="

if [ -n "$ARTICLE_ID" ]; then
    test_api "GET" "/likes/$ARTICLE_ID/status" "Check like status" "" "200"
    test_api "POST" "/likes/$ARTICLE_ID" "Toggle like" "" "200"
    test_api "GET" "/likes/$ARTICLE_ID/status" "Check like status after toggle" "" "200"
else
    echo -e "${YELLOW}SKIP${NC}: No article ID for like tests"
fi

echo ""
echo "========================================="
echo "4. Projects API Tests"
echo "========================================="

test_api "GET" "/projects" "Get all projects" "" "200"
test_api "GET" "/projects/featured" "Get featured projects" "" "200"
test_api "GET" "/projects/tech-stack" "Get tech stack" "" "200"

echo ""
echo "========================================="
echo "5. Skills API Tests"
echo "========================================="

test_api "GET" "/skills/grouped" "Get grouped skills" "" "200"

echo ""
echo "========================================="
echo "6. Search API Tests"
echo "========================================="

# Test search with keyword as query parameter
test_api "POST" "/articles/search?keyword=Python&page=1&page_size=10" "Search articles (with keyword)" "" "200"
test_api "POST" "/articles/search?keyword=&page=1&page_size=10" "Search articles (empty keyword)" "" "200"

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
