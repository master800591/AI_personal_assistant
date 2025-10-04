#!/usr/bin/env python3
"""
Cleanup Script for AI Personal Assistant
Moves old files to appropriate locations and organizes the project structure
"""

import os
import shutil
from pathlib import Path

def main():
    """Clean up and organize the project structure"""
    root = Path(".")
    
    print("🧹 Starting project cleanup...")
    
    # Create archive directory for old files
    archive_dir = root / "archive"
    archive_dir.mkdir(exist_ok=True)
    
    # Files to archive (old/experimental files)
    files_to_archive = [
        "autonomous_ollama_crew.py",
        "celebrate_discord_fix.py", 
        "continuous_evolution_engine.py",
        "create_initial_issue.py",
        "debug_discord_token.py",
        "demo_ai_corporation.py",
        "deploy_production.py",
        "real_ai_developer.py",
        "real_crewai_system.py",
        "real_discord_bot.py",
        "simple_autonomous_dev.py",
        "start_ai_corporation.bat",
        "quick_ollama_setup.py",
        "setup_ollama_toolkit.py",
        "ai_platform_enhanced.py",
        "test_context_extraction.py",
        "test_encoding_fix.py",
        "test_github.py",
        "test_tokens.py",
        "ollama_discover.py",
        "ollama_examples.py",
        "ollama_model_manager.py",
        "run_ollama_tools.bat",
        "run_ollama_tools_enhanced.bat"
    ]
    
    # Archive old files
    for filename in files_to_archive:
        file_path = root / filename
        if file_path.exists():
            print(f"📦 Archiving {filename}")
            shutil.move(str(file_path), str(archive_dir / filename))
    
    # Move test files to tests directory
    test_files = [
        "test_ollama_toolkit.py"
    ]
    
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    for filename in test_files:
        file_path = root / filename
        if file_path.exists():
            print(f"🧪 Moving test file {filename}")
            shutil.move(str(file_path), str(tests_dir / filename))
    
    # Move documentation files
    docs_dir = root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    doc_files = [
        "README_model_manager.md",
        "README_ollama_toolkit.md",
        "REMOVE_FUNCTIONALITY.md"
    ]
    
    for filename in doc_files:
        file_path = root / filename
        if file_path.exists():
            print(f"📚 Moving documentation {filename}")
            shutil.move(str(file_path), str(docs_dir / filename))
    
    # Clean up directories
    dirs_to_archive = [
        "__pycache__",
        "improvements",
        "replications"
    ]
    
    for dirname in dirs_to_archive:
        dir_path = root / dirname
        if dir_path.exists() and dir_path.is_dir():
            print(f"📂 Archiving directory {dirname}")
            if (archive_dir / dirname).exists():
                shutil.rmtree(str(archive_dir / dirname))
            shutil.move(str(dir_path), str(archive_dir / dirname))
    
    # Create proper package structure if needed
    src_dir = root / "src" / "ai_assistant"
    if not src_dir.exists():
        src_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy ollama_toolkit.py to proper location if not already there
    toolkit_src = root / "ollama_toolkit.py"
    toolkit_dst = src_dir / "ollama" / "toolkit.py"
    
    if toolkit_src.exists() and not toolkit_dst.exists():
        print("🔧 Moving ollama_toolkit.py to proper location")
        toolkit_dst.parent.mkdir(exist_ok=True)
        shutil.copy2(str(toolkit_src), str(toolkit_dst))
        # Archive the original
        shutil.move(str(toolkit_src), str(archive_dir / "ollama_toolkit.py"))
    
    # Create .gitignore if it doesn't exist
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        print("📝 Creating .gitignore")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# Data
data/
*.db
*.sqlite

# Archive
archive/

# OS
.DS_Store
Thumbs.db

# AI Assistant specific
config/local_*.yaml
backups/
temp/
"""
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
    
    print("✅ Cleanup completed!")
    print(f"📦 Archived files moved to: {archive_dir}")
    print("🚀 Project structure is now organized")
    print("\nNext steps:")
    print("1. Review archived files in archive/ directory")
    print("2. Run: pip install -e . (to install in development mode)")
    print("3. Copy .env.example to .env and configure")
    print("4. Start development with: ai-assistant --dev-mode")

if __name__ == "__main__":
    main()