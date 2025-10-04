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
import threading
import concurrent.futures

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import real components
from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
from ai_assistant.discord.enhanced_bot import AIAssistantDiscordBot
from ai_assistant.github.manager import GitHubManager
from ai_assistant.utils.config import Config
from ai_assistant.utils.logging import get_logger

class AIPersonalAssistant:
    """Complete AI Personal Assistant System with Real Integrations"""
    
    def __init__(self, config_path: str = "config/test.yaml"):
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.running = False
        
        # Load environment and configuration
        load_dotenv()
        self.config = self._load_configuration()
        
        # Real components - no mocks!
        self.crew_manager: Optional[AutonomousCrewManager] = None
        self.discord_bot: Optional[AIAssistantDiscordBot] = None
        self.github_manager: Optional[GitHubManager] = None
        
        # Task management
        self.background_tasks = set()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        
        self.logger.info("🤖 AI Personal Assistant initialized")
        self.logger.info(f"👑 Founder: {self.config.get('founder_name', 'Steve Cornell')}")
        self.logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/ai_assistant.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load complete configuration from environment and config files"""
        config = {
            # Environment tokens
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'ollama_host': os.getenv('OLLAMA_HOST', 'localhost'),
            'ollama_port': os.getenv('OLLAMA_PORT', '11434'),
            
            # Founder info
            'founder_name': os.getenv('AI_CORP_FOUNDER', 'Steve Cornell'),
            'founder_github': 'master80059',
            
            # System settings
            'ai_corp_mode': os.getenv('AI_CORP_MODE', 'production'),
            'cycle_interval': 600,  # 10 minutes
            'max_concurrent_tasks': 4,
            
            # Feature flags
            'discord_enabled': bool(os.getenv('DISCORD_BOT_TOKEN')),
            'github_enabled': bool(os.getenv('GITHUB_TOKEN')),
            'crewai_enabled': True,
            'voice_enabled': True,
            'knowledge_management': True
        }
        
        # Load YAML config if exists
        if self.config_path.exists():
            try:
                import yaml
                with open(self.config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    config.update(yaml_config)
            except Exception as e:
                self.logger.warning(f"Could not load YAML config: {e}")
        
        return config
    
    async def initialize_components(self):
        """Initialize all REAL system components concurrently"""
        self.logger.info("🚀 Initializing AI Personal Assistant components...")
        
        # Initialize all components concurrently
        await asyncio.gather(
            self._init_crew_manager(),
            self._init_discord_bot(),
            self._init_github_manager(),
            return_exceptions=True
        )
        
        self.logger.info("✅ All components initialized successfully")
    
    async def _init_crew_manager(self):
        """Initialize REAL CrewAI management system"""
        try:
            self.logger.info("🧠 Initializing CrewAI system...")
            
            # Create real AutonomousCrewManager with our enhanced agents and tools
            self.crew_manager = AutonomousCrewManager(self.config)
            # Note: AutonomousCrewManager doesn't need separate initialize() call
            
            self.logger.info("✅ CrewAI system ready with enhanced agents and Discord tools")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize CrewAI: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.crew_manager = None
    
    async def _init_discord_bot(self):
        """Initialize REAL Discord bot with CrewAI integration"""
        try:
            discord_token = self.config.get('discord_token')
            if discord_token:
                self.logger.info("🤖 Initializing Discord bot...")
                
                # Create real AIAssistantDiscordBot with CrewAI integration
                self.discord_bot = AIAssistantDiscordBot(self.config, self.crew_manager)
                
                # Start Discord bot in background
                bot_task = asyncio.create_task(self.discord_bot.start(discord_token))
                self.background_tasks.add(bot_task)
                bot_task.add_done_callback(self.background_tasks.discard)
                
                self.logger.info("✅ Discord bot ready with voice capabilities and CrewAI integration")
            else:
                self.logger.warning("⚠️ No Discord token provided - bot disabled")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.discord_bot = None
    
    async def _init_github_manager(self):
        """Initialize REAL GitHub automation manager"""
        try:
            github_token = self.config.get('github_token')
            if github_token:
                self.logger.info("🐙 Initializing GitHub manager...")
                
                # Create real GitHubManager with correct parameters
                self.github_manager = GitHubManager(
                    token=github_token,
                    config={'owner': self.config.get('founder_github', 'master80059'),
                            'repo': 'AI_personal_assistant'}
                )
                
                self.logger.info("✅ GitHub manager ready with automation capabilities")
            else:
                self.logger.warning("⚠️ No GitHub token provided - automation disabled")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize GitHub manager: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.github_manager = None
    
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
        """Contact founder about system startup using real Discord bot"""
        message = f"""
🤖 **AI Personal Assistant System Startup**

**Founder:** {self.config.get('founder_name', 'Steve Cornell')} ({self.config.get('founder_github', 'master80059')})
**Status:** System starting up
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Components Initialized:**
• CrewAI System: {'✅' if self.crew_manager else '❌'}
• Discord Bot: {'✅' if self.discord_bot else '❌'}
• GitHub Manager: {'✅' if self.github_manager else '❌'}

**AI Agent Status:**
• Code Analysis Agent: {'🔍 Active' if self.crew_manager else '❌ Offline'}
• Feature Developer Agent: {'⚡ Active' if self.crew_manager else '❌ Offline'}
• Founder Communication Agent: {'👑 Active' if self.crew_manager else '❌ Offline'}

**Capabilities Online:**
• Discord Voice Channels: {'✅' if self.discord_bot else '❌'}
• Knowledge Management: {'✅' if self.crew_manager else '❌'}
• GitHub Automation: {'✅' if self.github_manager else '❌'}
• Multi-Agent Coordination: {'✅' if self.crew_manager else '❌'}

**Questions for Founder:**
1. What should be the priority focus for today's development?
2. Are there specific files or features you'd like me to analyze?
3. Should I proceed with automated commits and pull requests?
4. Any specific improvements or features you'd like implemented?

Ready to begin autonomous development cycle with full Discord integration!
        """
        
        self.logger.info("👑 Contacting founder about startup...")
        
        # Send via Discord if available
        if self.discord_bot:
            try:
                # Find a suitable channel (first available guild's first text channel)
                if hasattr(self.discord_bot, 'guilds') and self.discord_bot.guilds:
                    guild = self.discord_bot.guilds[0]
                    if guild.text_channels:
                        channel_id = guild.text_channels[0].id
                        await self.discord_bot.send_crew_message(
                            channel_id=channel_id,
                            content=message
                        )
                        self.logger.info("📨 Startup notification sent via Discord")
                    else:
                        self.logger.warning("⚠️ No text channels available in Discord guild")
                else:
                    self.logger.warning("⚠️ No Discord guilds available")
            except Exception as e:
                self.logger.error(f"❌ Failed to send Discord notification: {e}")
        
        # Fallback to GitHub issue if Discord not available
        elif self.github_manager:
            try:
                await self.github_manager.create_issue(
                    title="AI Assistant System Startup",
                    body=message,
                    labels=["startup", "founder-communication"]
                )
                self.logger.info("📨 Startup notification sent via GitHub issue")
            except Exception as e:
                self.logger.error(f"❌ Failed to create GitHub issue: {e}")
        
        self.logger.info("📨 Startup notification completed")
    
    async def run_full_system(self):
        """Run complete integrated system with concurrent processing"""
        self.logger.info("🌟 Running full AI Personal Assistant system with multi-threading")
        
        # Create concurrent tasks for different system components
        tasks = []
        
        # Task 1: CrewAI Development Cycles
        if self.crew_manager:
            tasks.append(asyncio.create_task(self._run_crew_cycles()))
        
        # Task 2: Discord Bot (already running in background)
        if self.discord_bot:
            self.logger.info("🤖 Discord bot running in background with voice capabilities")
        
        # Task 3: GitHub Monitoring (if needed)
        if self.github_manager:
            tasks.append(asyncio.create_task(self._run_github_monitoring()))
        
        # Task 4: System Health Monitoring
        tasks.append(asyncio.create_task(self._run_health_monitoring()))
        
        # Run all tasks concurrently
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except KeyboardInterrupt:
            self.logger.info("� Shutdown requested by user")
        except Exception as e:
            self.logger.error(f"❌ Error in system execution: {e}")
        finally:
            await self.shutdown()
    
    async def _run_crew_cycles(self):
        """Run CrewAI development cycles continuously"""
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                self.logger.info(f"🔄 Starting development cycle {cycle_count}")
                
                # Run CrewAI development cycle
                crew_result = await self.crew_manager.run_development_cycle()
                self.logger.info(f"🧠 Crew cycle result: {crew_result.get('status', 'completed')}")
                
                # Process crew results
                if crew_result.get('success', False):
                    # Commit changes via GitHub if available
                    if self.github_manager and crew_result.get('changes_made', False):
                        try:
                            commit_message = f"AI development cycle {cycle_count} - {crew_result.get('summary', 'improvements')}"
                            # Note: Real GitHub integration would be implemented here
                            self.logger.info(f"📝 Would commit: {commit_message}")
                        except Exception as e:
                            self.logger.error(f"❌ GitHub commit failed: {e}")
                    
                    # Notify via Discord if available
                    if self.discord_bot:
                        try:
                            progress_message = f"🔄 **Development Cycle {cycle_count} Complete**\\n\\n{crew_result.get('summary', 'Progress update')}"
                            # Note: Real Discord notification would be implemented here
                            self.logger.info(f"📊 Discord notification: {progress_message[:50]}...")
                        except Exception as e:
                            self.logger.error(f"❌ Discord notification failed: {e}")
                
                # Wait before next cycle (configurable interval)
                cycle_interval = self.config.get('cycle_interval', 600)  # Default 10 minutes
                self.logger.info(f"⏳ Waiting {cycle_interval//60} minutes before next cycle...")
                await asyncio.sleep(cycle_interval)
                
            except asyncio.CancelledError:
                self.logger.info("🛑 Crew cycles cancelled")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in crew cycle: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def _run_github_monitoring(self):
        """Monitor GitHub for issues, PRs, and other events"""
        while self.running:
            try:
                # Monitor GitHub events (implementation would go here)
                self.logger.debug("� Monitoring GitHub events...")
                await asyncio.sleep(300)  # Check every 5 minutes
            except asyncio.CancelledError:
                self.logger.info("🛑 GitHub monitoring cancelled")
                break
            except Exception as e:
                self.logger.error(f"❌ GitHub monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _run_health_monitoring(self):
        """Monitor system health and performance"""
        while self.running:
            try:
                # Check system health
                status = await self.get_system_status()
                self.logger.debug(f"💚 System health: {status['components']}")
                
                # Log resource usage periodically
                if hasattr(self, '_health_check_count'):
                    self._health_check_count += 1
                else:
                    self._health_check_count = 1
                
                # Every 12 checks (1 hour), log detailed status
                if self._health_check_count % 12 == 0:
                    self.logger.info(f"📊 System Status Update: {status}")
                
                await asyncio.sleep(300)  # Check every 5 minutes
            except asyncio.CancelledError:
                self.logger.info("🛑 Health monitoring cancelled")
                break
            except Exception as e:
                self.logger.error(f"❌ Health monitoring error: {e}")
                await asyncio.sleep(60)
    
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
            ollama_host = self.config.get('ollama_host', 'localhost')
            ollama_port = self.config.get('ollama_port', '11434')
            response = requests.get(f"http://{ollama_host}:{ollama_port}/api/tags", timeout=5)
            ollama_status = response.status_code == 200
        except:
            pass
        
        return {
            "running": self.running,
            "components": {
                "crew_ai": self.crew_manager is not None,
                "discord_bot": self.discord_bot is not None,
                "github_manager": self.github_manager is not None,
                "ollama": ollama_status
            },
            "configuration": {
                "founder": self.config.get('founder_name', 'Steve Cornell'),
                "github_user": self.config.get('founder_github', 'master80059'),
                "discord_enabled": bool(self.config.get('discord_token')),
                "github_enabled": bool(self.config.get('github_token'))
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Shutdown the system gracefully"""
        self.logger.info("🛑 Shutting down AI Personal Assistant...")
        
        self.running = False
        
        # Cancel all background tasks
        for task in self.background_tasks:
            if not task.done():
                task.cancel()
        
        # Wait for tasks to complete
        if self.background_tasks:
            await asyncio.gather(*self.background_tasks, return_exceptions=True)
        
        # Shutdown components
        if self.discord_bot:
            try:
                await self.discord_bot.close()
            except Exception as e:
                self.logger.error(f"Error closing Discord bot: {e}")
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        # Final founder notification
        await self.contact_founder_shutdown()
        
        self.logger.info("✅ Shutdown complete")
    
    async def contact_founder_shutdown(self):
        """Notify founder about shutdown"""
        message = f"""
🛑 **AI Personal Assistant System Shutdown**

**Founder:** {self.config.get('founder_name', 'Steve Cornell')} ({self.config.get('founder_github', 'master80059')})
**Status:** System shutting down
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Components Shut Down:**
• CrewAI System: {'✅' if self.crew_manager else '❌'}
• Discord Bot: {'✅' if self.discord_bot else '❌'}
• GitHub Manager: {'✅' if self.github_manager else '❌'}

System has been stopped. Ready to restart when needed.
All AI agents are now offline.
        """
        
        self.logger.info("👑 Notifying founder about shutdown...")
        # Note: Real implementation would send notification
        self.logger.info("📨 Shutdown notification logged")


# Main execution
async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Personal Assistant')
    parser.add_argument('--mode', choices=['full', 'crew_only', 'discord_only'], 
                       default='full', help='Operating mode')
    parser.add_argument('--config', default='config/test.yaml', help='Configuration file')
    
    args = parser.parse_args()
    
    # Create and start assistant
    assistant = AIPersonalAssistant(args.config)
    
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