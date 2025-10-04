#!/usr/bin/env python3
"""
AI Personal Assistant Test Suite
Quick validation of the cleaned up project structure
"""

import sys
import os
import importlib.util
from pathlib import Path

def test_project_structure():
    """Test that the project structure is correct"""
    print("🧪 Testing project structure...")
    
    expected_dirs = [
        "src/ai_assistant",
        "src/ai_assistant/autonomous",
        "src/ai_assistant/ollama", 
        "src/ai_assistant/discord",
        "src/ai_assistant/github",
        "src/ai_assistant/utils",
        "tests",
        "docs",
        "scripts", 
        "config",
        "logs"
    ]
    
    for dir_path in expected_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - Missing")
    
    expected_files = [
        "setup.py",
        "requirements.txt",
        "README.md",
        ".env.example",
        "src/ai_assistant/__init__.py",
        "src/ai_assistant/main.py",
        "src/ai_assistant/utils/config.py",
        "src/ai_assistant/utils/logging.py",
        "src/ai_assistant/utils/helpers.py"
    ]
    
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")

def test_imports():
    """Test that key modules can be imported"""
    print("\n🧪 Testing imports...")
    
    test_imports = [
        ("src.ai_assistant.utils.config", "Config"),
        ("src.ai_assistant.utils.logging", "setup_logging"),
        ("src.ai_assistant.utils.helpers", "ensure_directory")
    ]
    
    for module_name, class_name in test_imports:
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, 
                Path(module_name.replace('.', '/') + '.py')
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, class_name):
                print(f"✅ {module_name}.{class_name}")
            else:
                print(f"❌ {module_name}.{class_name} - Not found")
                
        except Exception as e:
            print(f"❌ {module_name} - Import failed: {e}")

def test_config():
    """Test configuration system"""
    print("\n🧪 Testing configuration...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path('src')))
        
        from ai_assistant.utils.config import Config
        
        config = Config()
        
        # Test basic functionality
        test_value = "test_value"
        config.set('test.key', test_value)
        retrieved = config.get('test.key')
        
        if retrieved == test_value:
            print("✅ Config set/get works")
        else:
            print(f"❌ Config set/get failed: expected {test_value}, got {retrieved}")
        
        # Test default values
        default_value = config.get('nonexistent.key', 'default')
        if default_value == 'default':
            print("✅ Config default values work")
        else:
            print("❌ Config default values failed")
            
        # Test has method
        if config.has('test.key'):
            print("✅ Config has method works")
        else:
            print("❌ Config has method failed")
            
    except Exception as e:
        print(f"❌ Config test failed: {e}")

def test_environment():
    """Test environment setup"""
    print("\n🧪 Testing environment...")
    
    # Check for .env.example
    if Path('.env.example').exists():
        print("✅ .env.example exists")
    else:
        print("❌ .env.example missing")
    
    # Check for Python version
    if sys.version_info >= (3, 8):
        print(f"✅ Python version: {sys.version}")
    else:
        print(f"❌ Python version too old: {sys.version}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️ Not in a virtual environment (recommended)")

def run_all_tests():
    """Run all tests"""
    print("🚀 AI Personal Assistant - Project Structure Test\n")
    
    try:
        test_project_structure()
        test_imports() 
        test_config()
        test_environment()
        
        print("\n🎉 Testing completed!")
        print("\n📋 Next steps:")
        print("1. Install package: pip install -e .")
        print("2. Copy .env.example to .env and configure")
        print("3. Start development: ai-assistant --dev-mode")
        print("4. Run tests: pytest tests/")
        
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)