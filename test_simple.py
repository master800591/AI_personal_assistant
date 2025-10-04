"""
Simple Enhanced AI Personal Assistant Test
Testing multiprocessing Discord + CrewAI
"""

import os
import sys
import asyncio
import logging
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Load environment first
load_dotenv()

def test_discord_bot():
    """Test Discord bot in separate process"""
    print("🤖 Testing Discord bot process...")
    
    try:
        from ai_assistant.discord.enhanced_bot import AIAssistantDiscordBot
        
        config = {
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'founder_name': 'Steve Cornell',
            'founder_github': 'master80059'
        }
        
        # Create bot
        bot = AIAssistantDiscordBot(config, None)
        print("✅ Discord bot created successfully")
        
        # Test token
        if config['discord_token']:
            print("✅ Discord token found")
        else:
            print("❌ No Discord token")
            
        return True
        
    except Exception as e:
        print(f"❌ Discord bot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crewai_system():
    """Test CrewAI system in separate process"""
    print("🧠 Testing CrewAI system process...")
    
    try:
        from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
        
        config = {
            'founder_name': 'Steve Cornell',
            'founder_github': 'master80059',
            'ollama_host': 'localhost',
            'ollama_port': '11434'
        }
        
        # Create crew manager
        crew_manager = AutonomousCrewManager(config)
        print("✅ CrewAI manager created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewAI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_simple_test():
    """Run simple multiprocessing test"""
    print("🔧 Testing Enhanced AI Personal Assistant Components")
    print("=" * 50)
    
    # Test in main process first
    print("📊 Testing in main process...")
    discord_ok = test_discord_bot()
    crewai_ok = test_crewai_system()
    
    if not discord_ok or not crewai_ok:
        print("❌ Main process tests failed!")
        return False
    
    print("✅ Main process tests passed!")
    
    # Test multiprocessing capability
    print("\n🔄 Testing multiprocessing capability...")
    
    def worker_test(worker_name):
        """Simple worker process test"""
        print(f"👷 Worker {worker_name} started in process {os.getpid()}")
        return f"Worker {worker_name} completed"
    
    try:
        # Create and start a test process
        process = multiprocessing.Process(
            target=worker_test,
            args=("TestWorker",),
            name="TestProcess"
        )
        process.start()
        process.join(timeout=5)
        
        if process.exitcode == 0:
            print("✅ Multiprocessing test passed!")
            return True
        else:
            print(f"❌ Multiprocessing test failed with exit code: {process.exitcode}")
            return False
            
    except Exception as e:
        print(f"❌ Multiprocessing test error: {e}")
        return False

if __name__ == "__main__":
    # Critical for Windows multiprocessing
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)
    
    success = run_simple_test()
    
    if success:
        print("\n🎉 All tests passed! Ready for full system.")
    else:
        print("\n❌ Tests failed. Check configuration.")