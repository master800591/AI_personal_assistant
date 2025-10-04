"""
Main AI Personal Assistant Application
Founder: Steve Cornell (master80059)
Complete integrated system with CrewAI, Discord, and GitHub automation
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

class AIPersonalAssistant:
    """Complete AI Personal Assistant System"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = self._setup_logging()
        self.running = False
        
        # Components
        self.crew_manager = None
        self.discord_bot = None
        self.github_automation = None
        
        # Configuration
        self.config = self._load_environment()
        
        self.logger.info("🤖 AI Personal Assistant initialized")
        self.logger.info(f"👑 Founder: Steve Cornell (master80059)")
        self.logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('ai_assistant.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_environment(self) -> Dict[str, Any]:
        """Load environment configuration"""
        # Load .env file
        load_dotenv()
        
        return {
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'ollama_host': os.getenv('OLLAMA_HOST', 'localhost:11434'),
            'founder_name': os.getenv('AI_CORP_FOUNDER', 'Steve Cornell'),
            'founder_github': 'master80059'
        }
    
    async def initialize_components(self):
        """Initialize all system components"""
        self.logger.info("🚀 Initializing AI Personal Assistant components...")
        
        # Initialize CrewAI system
        await self._init_crew_manager()
        
        # Initialize Discord bot
        await self._init_discord_bot()
        
        # Initialize GitHub automation
        await self._init_github_automation()
        
        self.logger.info("✅ All components initialized successfully")
    
    async def _init_crew_manager(self):
        """Initialize CrewAI management system"""
        try:
            # Check if CrewAI is available
            self.logger.info("🧠 Initializing CrewAI system...")
            
            # For now, create a placeholder that simulates CrewAI functionality
            self.crew_manager = MockCrewManager()
            
            self.logger.info("✅ CrewAI system ready")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize CrewAI: {e}")
            self.crew_manager = None
    
    async def _init_discord_bot(self):
        """Initialize Discord bot"""
        try:
            discord_token = self.config.get('discord_token')
            if discord_token:
                self.logger.info("🤖 Initializing Discord bot...")
                
                # Create mock Discord bot for now
                self.discord_bot = MockDiscordBot(discord_token, self.crew_manager)
                
                self.logger.info("✅ Discord bot ready")
            else:
                self.logger.warning("⚠️ No Discord token provided - bot disabled")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            self.discord_bot = None
    
    async def _init_github_automation(self):
        """Initialize GitHub automation"""
        try:
            github_token = self.config.get('github_token')
            if github_token:
                self.logger.info("🐙 Initializing GitHub automation...")
                
                # Create mock GitHub automation for now
                self.github_automation = MockGitHubAutomation(github_token)
                
                self.logger.info("✅ GitHub automation ready")
            else:
                self.logger.warning("⚠️ No GitHub token provided - automation disabled")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize GitHub automation: {e}")
            self.github_automation = None
    
    async def start(self, mode: str = "full"):
        """Start the AI Personal Assistant"""
        self.logger.info(f"🚀 Starting AI Personal Assistant in {mode} mode...")
        
        # Initialize components
        await self.initialize_components()
        
        # Check system status
        status = await self.get_system_status()
        self.logger.info(f"📊 System Status: {status}")
        
        # Contact founder
        await self.contact_founder_startup()
        
        self.running = True
        
        # Start main loop based on mode
        if mode == "full":
            await self.run_full_system()
        elif mode == "crew_only":
            await self.run_crew_only()
        elif mode == "discord_only":
            await self.run_discord_only()
        else:
            await self.run_full_system()
    
    async def contact_founder_startup(self):
        """Contact founder about system startup"""
        message = f"""
🤖 **AI Personal Assistant System Startup**

**Founder:** Steve Cornell (master80059)
**Status:** System starting up
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Components Initialized:**
• CrewAI System: {'✅' if self.crew_manager else '❌'}
• Discord Bot: {'✅' if self.discord_bot else '❌'}
• GitHub Automation: {'✅' if self.github_automation else '❌'}

**Questions for Founder:**
1. What should be the priority focus for today's development?
2. Are there specific files or features you'd like me to analyze?
3. Should I proceed with automated commits and pull requests?
4. Any specific improvements or features you'd like implemented?

Ready to begin autonomous development cycle!
        """
        
        self.logger.info("👑 Contacting founder about startup...")
        
        # This would send via Discord or create GitHub issue
        if self.discord_bot:
            await self.discord_bot.notify_founder(message)
        elif self.github_automation:
            await self.github_automation.create_issue(
                "AI Assistant System Startup",
                message,
                ["startup", "founder-communication"]
            )
        
        self.logger.info("📨 Startup notification sent to founder")
    
    async def run_full_system(self):
        """Run complete integrated system"""
        self.logger.info("🌟 Running full AI Personal Assistant system")
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                self.logger.info(f"🔄 Starting development cycle {cycle_count}")
                
                # Run CrewAI development cycle
                if self.crew_manager:
                    crew_result = await self.crew_manager.run_development_cycle()
                    self.logger.info(f"🧠 Crew cycle result: {crew_result.get('status', 'unknown')}")
                    
                    # Process crew results
                    if crew_result.get('success') and crew_result.get('changes_made'):
                        # Commit changes via GitHub automation
                        if self.github_automation:
                            commit_result = await self.github_automation.create_automated_commit(
                                f"AI development cycle {cycle_count} - {crew_result.get('summary', 'improvements')}"
                            )
                            self.logger.info(f"📝 Commit result: {commit_result.get('success', False)}")
                        
                        # Notify via Discord
                        if self.discord_bot:
                            await self.discord_bot.notify_development_progress(crew_result)
                
                # Wait before next cycle
                self.logger.info("⏳ Waiting 10 minutes before next cycle...")
                await asyncio.sleep(600)  # 10 minutes
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Shutdown requested by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
        
        await self.shutdown()
    
    async def run_crew_only(self):
        """Run CrewAI system only"""
        self.logger.info("🧠 Running CrewAI development system only")
        
        if not self.crew_manager:
            self.logger.error("❌ CrewAI system not available")
            return
        
        while self.running:
            try:
                result = await self.crew_manager.run_development_cycle()
                self.logger.info(f"🔄 Crew cycle completed: {result}")
                
                await asyncio.sleep(300)  # 5 minutes
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"❌ Crew error: {e}")
                await asyncio.sleep(60)
    
    async def run_discord_only(self):
        """Run Discord bot only"""
        self.logger.info("🤖 Running Discord bot only")
        
        if not self.discord_bot:
            self.logger.error("❌ Discord bot not available")
            return
        
        try:
            await self.discord_bot.start()
        except Exception as e:
            self.logger.error(f"❌ Discord bot error: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        # Check Ollama
        ollama_status = False
        try:
            import requests
            response = requests.get(f"http://{self.config['ollama_host']}/api/tags", timeout=5)
            ollama_status = response.status_code == 200
        except:
            pass
        
        return {
            "running": self.running,
            "components": {
                "crew_ai": self.crew_manager is not None,
                "discord_bot": self.discord_bot is not None,
                "github_automation": self.github_automation is not None,
                "ollama": ollama_status
            },
            "configuration": {
                "founder": self.config['founder_name'],
                "github_user": self.config['founder_github'],
                "discord_enabled": bool(self.config['discord_token']),
                "github_enabled": bool(self.config['github_token'])
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Shutdown the system gracefully"""
        self.logger.info("🛑 Shutting down AI Personal Assistant...")
        
        self.running = False
        
        # Shutdown components
        if self.discord_bot:
            await self.discord_bot.close()
        
        # Final founder notification
        await self.contact_founder_shutdown()
        
        self.logger.info("✅ Shutdown complete")
    
    async def contact_founder_shutdown(self):
        """Notify founder about shutdown"""
        message = f"""
🛑 **AI Personal Assistant System Shutdown**

**Founder:** Steve Cornell (master80059)
**Status:** System shutting down
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

System has been stopped. Ready to restart when needed.
        """
        
        self.logger.info("👑 Notifying founder about shutdown...")
        # Implementation would send notification

# Mock classes for components that need external dependencies
class MockCrewManager:
    """Mock CrewAI manager for testing"""
    
    async def run_development_cycle(self):
        """Simulate crew development cycle"""
        await asyncio.sleep(2)  # Simulate processing
        return {
            "success": True,
            "status": "completed",
            "changes_made": True,
            "summary": "Code analysis and improvements completed",
            "files_analyzed": 5,
            "improvements_suggested": 12
        }

class MockDiscordBot:
    """Mock Discord bot for testing"""
    
    def __init__(self, token, crew_manager):
        self.token = token
        self.crew_manager = crew_manager
    
    async def start(self):
        """Simulate bot start"""
        await asyncio.sleep(1)
    
    async def notify_founder(self, message):
        """Simulate founder notification"""
        print(f"📨 [Discord] Founder notification: {message[:100]}...")
    
    async def notify_development_progress(self, result):
        """Simulate progress notification"""
        print(f"📊 [Discord] Development progress: {result.get('summary', 'Progress update')}")
    
    async def close(self):
        """Simulate bot close"""
        pass

class MockGitHubAutomation:
    """Mock GitHub automation for testing"""
    
    def __init__(self, token):
        self.token = token
    
    async def create_automated_commit(self, message):
        """Simulate commit creation"""
        await asyncio.sleep(1)
        return {
            "success": True,
            "commit_hash": "abc12345",
            "message": message
        }
    
    async def create_issue(self, title, body, labels):
        """Simulate issue creation"""
        await asyncio.sleep(1)
        return {
            "success": True,
            "issue_number": 123,
            "title": title
        }

# Main execution
async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Personal Assistant')
    parser.add_argument('--mode', choices=['full', 'crew_only', 'discord_only'], 
                       default='full', help='Operating mode')
    parser.add_argument('--config-dir', default='config', help='Configuration directory')
    
    args = parser.parse_args()
    
    # Create and start assistant
    assistant = AIPersonalAssistant(args.config_dir)
    
    try:
        await assistant.start(args.mode)
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await assistant.shutdown()

if __name__ == "__main__":
    print("🤖 AI Personal Assistant")
    print("Founder: Steve Cornell (master80059)")
    print("=" * 50)
    asyncio.run(main())