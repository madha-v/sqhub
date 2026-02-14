@echo off
title Mini SQL Compiler
color 0A

echo ========================================
echo    Mini SQL Compiler
echo    Compiler Design Project
echo ========================================
echo.
echo Starting the SQL Compiler GUI...
echo.

python gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the compiler!
    echo.
    echo Please make sure:
    echo 1. Python is installed
    echo 2. All files are in the same folder
    echo 3. Python is added to PATH
    echo.
    pause
) else (
    echo.
    echo Compiler closed successfully.
)
