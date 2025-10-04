"""
Test Enhanced AI Personal Assistant Components
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

print("🔍 Testing AI Personal Assistant Components...")
print(f"📁 Current directory: {current_dir}")
print(f"📁 Src directory: {src_dir}")
print(f"🔄 Python path: {sys.path[:3]}...")

# Load environment
load_dotenv()
print("✅ Environment loaded")

# Test imports
try:
    print("🧠 Testing CrewAI import...")
    from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
    print("✅ CrewAI imported successfully")
except Exception as e:
    print(f"❌ CrewAI import failed: {e}")

try:
    print("🤖 Testing Discord bot import...")
    from ai_assistant.discord.enhanced_bot import AIAssistantDiscordBot
    print("✅ Discord bot imported successfully")
except Exception as e:
    print(f"❌ Discord bot import failed: {e}")

try:
    print("📚 Testing GitHub manager import...")
    from ai_assistant.github.manager import GitHubManager
    print("✅ GitHub manager imported successfully")
except Exception as e:
    print(f"❌ GitHub manager import failed: {e}")

# Test basic configuration
config = {
    'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
    'github_token': os.getenv('GITHUB_TOKEN'),
    'founder_name': 'Steve Cornell',
    'founder_github': 'master80059'
}

print(f"🔑 Discord token present: {bool(config['discord_token'])}")
print(f"🔑 GitHub token present: {bool(config['github_token'])}")

print("✅ Component test complete!")