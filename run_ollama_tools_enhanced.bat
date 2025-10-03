@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   OLLAMA MODEL MANAGEMENT TOOLS
echo ========================================
echo.
echo Choose your tool:
echo.
echo 1. Quick Setup (Interactive)
echo 2. Discovery CLI Help
echo 3. Discover Popular Models
echo 4. Search Models
echo 5. Pull Models
echo 6. Remove Models
echo 7. List Local Models
echo 8. Test Tools
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" (
    echo.
    echo Starting Quick Setup...
    python3.11 quick_ollama_setup.py
) else if "%choice%"=="2" (
    echo.
    echo Discovery CLI Help:
    python3.11 ollama_discover.py --help
) else if "%choice%"=="3" (
    echo.
    echo Discovering popular models...
    python3.11 ollama_discover.py discover --popular --limit 10
) else if "%choice%"=="4" (
    echo.
    set /p query="Enter search query: "
    if not "!query!"=="" (
        python3.11 ollama_discover.py search "!query!" --pull
    ) else (
        echo No query entered.
    )
) else if "%choice%"=="5" (
    echo.
    set /p models="Enter model names (space-separated): "
    if not "!models!"=="" (
        python3.11 ollama_discover.py pull --models !models! --yes
    ) else (
        echo No models specified.
    )
) else if "%choice%"=="6" (
    echo.
    echo Remove Models Menu:
    echo.
    echo 1. Remove specific models
    echo 2. Remove ALL models (WARNING!)
    echo 3. Interactive removal
    echo.
    set /p remove_choice="Choose removal option (1-3): "
    
    if "!remove_choice!"=="1" (
        set /p models="Enter model names to remove (space-separated): "
        if not "!models!"=="" (
            python3.11 ollama_discover.py remove --models !models!
        ) else (
            echo No models specified.
        )
    ) else if "!remove_choice!"=="2" (
        echo.
        echo ⚠️  WARNING: This will remove ALL models!
        echo This action cannot be undone.
        set /p confirm="Are you absolutely sure? Type 'YES' to confirm: "
        if "!confirm!"=="YES" (
            python3.11 ollama_discover.py remove --all --yes
        ) else (
            echo Operation cancelled.
        )
    ) else if "!remove_choice!"=="3" (
        python3.11 ollama_discover.py remove
    ) else (
        echo Invalid choice.
    )
) else if "%choice%"=="7" (
    echo.
    echo Listing local models:
    python3.11 ollama_discover.py list --details
) else if "%choice%"=="8" (
    echo.
    echo Running basic tests...
    python3.11 test_ollama_toolkit.py
) else if "%choice%"=="9" (
    echo.
    echo Goodbye! 🦙
    exit /b
) else (
    echo.
    echo Invalid choice. Please try again.
)

echo.
pause