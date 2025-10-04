"""Quick test for Discord tools fix"""

import asyncio
from src.ai_assistant.tools.discord_tools import DiscordListenerTool

async def test_discord_listener():
    try:
        # Test tool instantiation
        tool = DiscordListenerTool()
        
        # Check required attributes
        assert hasattr(tool, 'name')
        assert hasattr(tool, 'description')
        assert hasattr(tool, 'listening')
        assert hasattr(tool, '_run')
        
        print("✅ DiscordListenerTool instantiation successful")
        print(f"   Name: {tool.name}")
        print(f"   Description: {tool.description[:50]}...")
        print(f"   Listening: {tool.listening}")
        
        return True
        
    except Exception as e:
        print(f"❌ DiscordListenerTool test failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_discord_listener())
    print(f"\nTest result: {'PASSED' if result else 'FAILED'}")