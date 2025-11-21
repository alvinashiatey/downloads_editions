#!/bin/bash

# Build script for Downloads Editions Standalone Application
# This script automates the building process for different platforms

set -e  # Exit on error

echo "=========================================="
echo "Downloads Editions - Build Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

print_success "Python found: $(python3 --version)"

# Step 1: Install dependencies
print_step "Installing dependencies..."
pip install -e . || {
    print_error "Failed to install package dependencies"
    exit 1
}

pip install pyinstaller || {
    print_error "Failed to install PyInstaller"
    exit 1
}

print_success "Dependencies installed"

# Step 2: Clean previous builds
print_step "Cleaning previous builds..."
rm -rf build dist *.spec 2>/dev/null || true
print_success "Cleaned build directories"

# Step 3: Build the application
print_step "Building standalone application..."
pyinstaller downloads_editions.spec || {
    print_error "Build failed"
    exit 1
}

print_success "Build completed!"

# Step 4: Report results
echo ""
echo "=========================================="
echo "Build Summary"
echo "=========================================="

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -d "dist/DownloadsEditions.app" ]; then
        APP_SIZE=$(du -sh dist/DownloadsEditions.app | cut -f1)
        print_success "Application built successfully!"
        echo "  Location: dist/DownloadsEditions.app"
        echo "  Size: $APP_SIZE"
        echo ""
        echo "To run the application:"
        echo "  open dist/DownloadsEditions.app"
        echo ""
        echo "To create a distributable ZIP:"
        echo "  cd dist && zip -r DownloadsEditions-macOS.zip DownloadsEditions.app"
    else
        print_error "App bundle not found"
        exit 1
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    if [ -f "dist/DownloadsEditions.exe" ]; then
        print_success "Application built successfully!"
        echo "  Location: dist/DownloadsEditions.exe"
        echo ""
        echo "To run the application:"
        echo "  dist\\DownloadsEditions.exe"
        echo ""
        echo "To create a distributable ZIP:"
        echo "  powershell Compress-Archive -Path dist/DownloadsEditions.exe -DestinationPath DownloadsEditions-Windows.zip"
    else
        print_error "Executable not found"
        exit 1
    fi
else
    # Linux
    if [ -f "dist/DownloadsEditions" ]; then
        APP_SIZE=$(du -sh dist/DownloadsEditions | cut -f1)
        print_success "Application built successfully!"
        echo "  Location: dist/DownloadsEditions"
        echo "  Size: $APP_SIZE"
        echo ""
        echo "To run the application:"
        echo "  ./dist/DownloadsEditions"
        echo ""
        echo "To create a distributable archive:"
        echo "  cd dist && tar -czf DownloadsEditions-Linux.tar.gz DownloadsEditions"
    else
        print_error "Executable not found"
        exit 1
    fi
fi

echo ""
print_success "Build process completed!"
echo ""
