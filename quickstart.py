"""
Quick Start Guide for AI Personal Assistant
Founder: Steve Cornell (master80059)
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup the AI Personal Assistant environment"""
    print("🤖 AI Personal Assistant Quick Start")
    print("Founder: Steve Cornell (master80059)")
    print("=" * 50)
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            # Copy .env.example to .env
            env_file.write_text(env_example.read_text())
            print("✅ .env file created")
        else:
            print("❌ .env.example not found")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connected - {len(models)} models available")
            for model in models[:3]:  # Show first 3
                print(f"   📦 {model.get('name', 'Unknown')}")
        else:
            print("⚠️ Ollama not responding")
    except:
        print("❌ Ollama not available - install from https://ollama.ai")
    
    # Show configuration status
    print("\n📋 Configuration Status:")
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    github_token = os.getenv('GITHUB_TOKEN')
    
    print(f"   Discord Bot: {'✅' if discord_token else '❌'} {discord_token[:20] + '...' if discord_token else 'Not configured'}")
    print(f"   GitHub Token: {'✅' if github_token else '❌'} {github_token[:20] + '...' if github_token else 'Not configured'}")
    
    print("\n🚀 Ready to start AI Personal Assistant!")
    print("\nCommands:")
    print("   py main.py                 - Start full system")
    print("   py main.py --mode crew_only    - CrewAI only")
    print("   py main.py --mode discord_only - Discord bot only")
    
    return True

if __name__ == "__main__":
    setup_environment()