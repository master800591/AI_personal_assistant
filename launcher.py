#!/usr/bin/env python3
"""
Launch the Working AI Assistant
Simple, reliable entry point
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

def main():
    """Main launcher"""
    print("🤖 AI Personal Assistant Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return 1
    
    # Try different entry points
    entry_points = [
        ("Working AI Assistant", "working_ai_assistant"),
        ("Simple Main", "src.ai_assistant.simple_main"),
        ("Original Main", "src.ai_assistant.main")
    ]
    
    for name, module_name in entry_points:
        try:
            print(f"🔄 Trying {name}...")
            
            if module_name == "working_ai_assistant":
                # Direct import and run
                from working_ai_assistant import main as run_main
                asyncio.run(run_main())
                return 0
            else:
                # Try importing and running
                module = __import__(module_name, fromlist=['main'])
                if hasattr(module, 'main'):
                    asyncio.run(module.main())
                    return 0
                    
        except ImportError as e:
            print(f"⚠️ {name} not available: {e}")
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    # Fallback: Basic functionality test
    print("\n🔧 Running basic functionality test...")
    try:
        # Test Ollama
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama: {len(models)} models available")
        else:
            print("⚠️ Ollama: Not responding")
    except:
        print("❌ Ollama: Not available")
    
    # Test file structure
    workspace_files = list(Path('.').glob('*.py'))
    print(f"📁 Workspace: {len(workspace_files)} Python files found")
    
    print("\n💡 To get started:")
    print("1. Ensure Ollama is running: ollama serve")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run: python launcher.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())