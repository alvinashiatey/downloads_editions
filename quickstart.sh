#!/bin/bash

# Quickstart script for Downloads Editions
# This script downloads the project, sets up a temporary environment, runs the app, and cleans up.
# Usage: curl -sL https://raw.githubusercontent.com/alvinashiatey/downloads_editions/main/quickstart.sh | bash

set -e

REPO_URL="https://github.com/alvinashiatey/downloads_editions.git"
BRANCH="main"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}Downloads Editions - Quick Start${NC}"
echo -e "${BLUE}==========================================${NC}"

# Check for git
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed."
    exit 1
fi

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
echo -e "${GREEN}✓ Created temporary workspace${NC}"

# Cleanup function
cleanup() {
    echo ""
    echo -e "${BLUE}Cleaning up...${NC}"
    rm -rf "$TEMP_DIR"
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}
trap cleanup EXIT

# Clone the repository
echo -e "${BLUE}Downloading Downloads Editions...${NC}"
git clone -b "$BRANCH" --depth 1 "$REPO_URL" "$TEMP_DIR/repo" > /dev/null 2>&1
echo -e "${GREEN}✓ Download complete${NC}"

# Navigate to repo
cd "$TEMP_DIR/repo"

# Create virtual environment
echo -e "${BLUE}Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install the package
echo -e "${BLUE}Installing dependencies...${NC}"
pip install . > /dev/null 2>&1
echo -e "${GREEN}✓ Installation complete${NC}"

# Run the application
echo ""
echo -e "${GREEN}Starting application...${NC}"
echo ""
downloads-editions-gui
