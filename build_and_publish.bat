@echo off
REM Build and publish script for PDF Action Inspector (Windows)

echo === PDF Action Inspector Build ^& Publish Script ===

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo Error: pyproject.toml not found. Please run this script from the project root.
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Install build dependencies
echo Installing build dependencies...
pip install --upgrade pip setuptools wheel build twine

REM Build the package
echo Building package...
python -m build

REM Check the package
echo Checking package...
python -m twine check dist/*

echo Build completed successfully!
echo Built files:
dir dist\

echo.
echo To publish to PyPI:
echo 1. Test on TestPyPI first:
echo    python -m twine upload --repository testpypi dist/*
echo.
echo 2. Then upload to real PyPI:
echo    python -m twine upload dist/*
echo.
echo Note: You'll need PyPI account credentials for uploading.
