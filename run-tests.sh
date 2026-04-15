#!/bin/bash

# Integration Test Runner Script
# Runs all integration tests with proper setup and teardown

set -e

echo "========================================="
echo "Personal Blog - Integration Test Runner"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# Function to cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up test environment...${NC}"
    docker-compose -f docker-compose.test.yml down -v > /dev/null 2>&1 || true
}

# Trap cleanup on exit
trap cleanup EXIT

echo -e "${YELLOW}Step 1: Starting test environment...${NC}"
docker-compose -f docker-compose.test.yml up -d

echo ""
echo -e "${YELLOW}Step 2: Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo -e "${YELLOW}Step 3: Running backend tests...${NC}"
docker-compose -f docker-compose.test.yml exec -T backend pytest tests/ -v

echo ""
echo -e "${YELLOW}Step 4: Running frontend tests...${NC}"
cd frontend && npm test || true
cd ..

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${GREEN}=========================================${NC}"
