@echo off
REM Build script for Downloads Editions Standalone Application (Windows)
REM This script automates the building process for Windows

echo ==========================================
echo Downloads Editions - Build Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.6 or higher.
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Step 1: Install dependencies
echo [STEP 1] Installing dependencies...
pip install -e . >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install package dependencies
    exit /b 1
)

pip install pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Step 2: Clean previous builds
echo [STEP 2] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo [OK] Cleaned build directories
echo.

REM Step 3: Build the application
echo [STEP 3] Building standalone application...
pyinstaller downloads_editions.spec
if errorlevel 1 (
    echo [ERROR] Build failed
    exit /b 1
)

echo [OK] Build completed!
echo.

REM Step 4: Report results
echo ==========================================
echo Build Summary
echo ==========================================

if exist "dist\DownloadsEditions.exe" (
    echo [OK] Application built successfully!
    echo   Location: dist\DownloadsEditions.exe
    echo.
    echo To run the application:
    echo   dist\DownloadsEditions.exe
    echo.
    echo To create a distributable ZIP:
    echo   powershell Compress-Archive -Path dist\DownloadsEditions.exe -DestinationPath DownloadsEditions-Windows.zip
) else (
    echo [ERROR] Executable not found
    exit /b 1
)

echo.
echo [OK] Build process completed!
echo.

pause
