#!/bin/bash
# Build and publish script for PDF Action Inspector

set -e

echo "=== PDF Action Inspector Build & Publish Script ==="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Install build dependencies
echo "Installing build dependencies..."
pip install --upgrade pip setuptools wheel build twine

# Build the package
echo "Building package..."
python -m build

# Check the package
echo "Checking package..."
python -m twine check dist/*

echo "Build completed successfully!"
echo "Built files:"
ls -la dist/

echo ""
echo "To publish to PyPI:"
echo "1. Test on TestPyPI first:"
echo "   python -m twine upload --repository testpypi dist/*"
echo ""
echo "2. Then upload to real PyPI:"
echo "   python -m twine upload dist/*"
echo ""
echo "Note: You'll need PyPI account credentials for uploading."
