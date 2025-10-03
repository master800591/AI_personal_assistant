@echo off
echo 🦙 OLLAMA MODEL DISCOVERY TOOLS
echo ================================

echo.
echo Available tools:
echo.
echo 1. Quick Interactive Setup (Recommended for beginners)
echo    python3.11 quick_ollama_setup.py
echo.
echo 2. Command Line Interface (Advanced users)
echo    python3.11 ollama_discover.py discover --popular
echo    python3.11 ollama_discover.py search "embedding" --pull
echo    python3.11 ollama_discover.py recommend --category code
echo.
echo 3. Test Basic Functionality
echo    python3.11 test_ollama_toolkit.py
echo.

set /p choice="Which tool would you like to run? (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Starting Quick Interactive Setup...
    python3.11 quick_ollama_setup.py
) else if "%choice%"=="2" (
    echo.
    echo Command Line Interface Examples:
    echo.
    echo Discover popular models:
    echo python3.11 ollama_discover.py discover --popular --limit 10
    echo.
    echo Search for embedding models:
    echo python3.11 ollama_discover.py search "embedding" --pull
    echo.
    echo Get recommendations:
    echo python3.11 ollama_discover.py recommend --category code --pull
    echo.
    echo Pull specific models:
    echo python3.11 ollama_discover.py pull --models llama3.2 gemma2
    echo.
    set /p cmd="Enter command or press Enter to exit: "
    if not "%cmd%"=="" (
        %cmd%
    )
) else if "%choice%"=="3" (
    echo.
    echo Running basic tests...
    python3.11 test_ollama_toolkit.py
) else (
    echo Invalid choice. Exiting.
)

echo.
pause