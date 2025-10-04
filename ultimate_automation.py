#!/usr/bin/env python3
"""
AI Corporation - Ultimate Automation System
Complete Discord + GitHub + CrewAI Integration
Founder: Steve Cornell (master80059)
"""

import os
import sys
import asyncio
import logging
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv

# Load environment and setup path
load_dotenv()
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def discord_automation_worker(config_dict, shutdown_flag):
    """Complete Discord automation worker"""
    try:
        # Setup logging for Discord process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [DISCORD] - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("discord_automation")
        
        logger.info("🤖 Starting Discord Automation System...")
        
        # Import Discord modules
        from ai_assistant.discord.full_automation_bot import FullAutomationDiscordBot
        from ai_assistant.github.full_automation_manager import FullGitHubManager
        
        # Create GitHub manager for Discord bot integration
        github_manager = None
        if config_dict.get('github_token'):
            logger.info("🐙 Initializing GitHub manager...")
            github_manager = FullGitHubManager(config_dict['github_token'], config_dict)
            logger.info("✅ GitHub manager ready")
        
        # Create Discord bot with full automation
        bot = FullAutomationDiscordBot(config_dict, github_manager)
        
        # Get Discord token
        discord_token = config_dict.get('discord_token')
        if not discord_token:
            logger.error("❌ No Discord token provided")
            return
        
        logger.info("🚀 Starting Discord bot with full automation...")
        
        # Run Discord bot with proper async handling
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_discord_automation():
            try:
                # Start bot
                await bot.start(discord_token)
            except Exception as e:
                logger.error(f"❌ Discord bot error: {e}")
            finally:
                if not bot.is_closed():
                    await bot.close()
        
        # Monitor shutdown
        async def monitor_shutdown():
            while not shutdown_flag.value:
                await asyncio.sleep(1)
            logger.info("🛑 Discord automation shutdown requested")
            if not bot.is_closed():
                await bot.close()
        
        # Run both tasks
        try:
            loop.run_until_complete(asyncio.gather(
                run_discord_automation(),
                monitor_shutdown(),
                return_exceptions=True
            ))
        except KeyboardInterrupt:
            logger.info("🛑 Discord automation interrupted")
        
    except Exception as e:
        logger.error(f"❌ Discord automation error: {e}")
        import traceback
        traceback.print_exc()

def crewai_automation_worker(config_dict, shutdown_flag, stats_counter):
    """CrewAI automation worker with GitHub integration"""
    try:
        # Setup logging for CrewAI process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [CREWAI] - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("crewai_automation")
        
        logger.info("🧠 Starting CrewAI Automation System...")
        
        # Import CrewAI modules
        from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
        
        # Create CrewAI manager
        crew_manager = AutonomousCrewManager(config_dict)
        logger.info("✅ CrewAI manager initialized")
        
        # Run development cycles
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_automation_cycles():
            cycle_count = 0
            
            while not shutdown_flag.value:
                try:
                    logger.info(f"🔄 Starting AI automation cycle #{cycle_count + 1}")
                    
                    # Run development cycle
                    result = await crew_manager.run_development_cycle()
                    
                    if result and result.get('success'):
                        cycle_count += 1
                        stats_counter.value = cycle_count
                        logger.info(f"✅ Automation cycle #{cycle_count} completed successfully")
                    else:
                        logger.warning(f"⚠️ Automation cycle #{cycle_count + 1} had issues")
                    
                    # Wait for next cycle
                    wait_time = config_dict.get('cycle_interval', 600)  # 10 minutes default
                    logger.info(f"⏰ Waiting {wait_time} seconds for next cycle...")
                    
                    for _ in range(wait_time):
                        if shutdown_flag.value:
                            break
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.error(f"❌ Automation cycle error: {e}")
                    await asyncio.sleep(30)  # Wait before retry
            
            logger.info("🛑 CrewAI automation cycles stopped")
        
        # Run the automation cycles
        loop.run_until_complete(run_automation_cycles())
        
    except Exception as e:
        logger.error(f"❌ CrewAI automation error: {e}")
        import traceback
        traceback.print_exc()

class UltimateAIAutomation:
    """Ultimate AI Corporation Automation System"""
    
    def __init__(self):
        """Initialize the ultimate automation system"""
        self.logger = self._setup_logging()
        self.config = self._load_configuration()
        
        # Multiprocessing components
        self.manager = multiprocessing.Manager()
        self.shutdown_flag = self.manager.Value('b', False)
        self.stats_counter = self.manager.Value('i', 0)
        self.processes = []
        
        self.logger.info("🎯 Ultimate AI Corporation Automation System initialized")
        self.logger.info(f"👑 Founder: {self.config.get('founder_name', 'Steve Cornell')}")
    
    def _setup_logging(self):
        """Setup comprehensive logging"""
        Path("logs").mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [MAIN] - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/ai_automation_ultimate.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_configuration(self):
        """Load complete configuration"""
        return {
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'founder_name': os.getenv('AI_CORP_FOUNDER', 'Steve Cornell'),
            'founder_github': 'master80059',
            'cycle_interval': 300,  # 5 minutes for testing
            'discord_enabled': bool(os.getenv('DISCORD_BOT_TOKEN')),
            'github_enabled': bool(os.getenv('GITHUB_TOKEN')),
            'automation_level': 'ultimate'
        }
    
    def start_discord_automation(self):
        """Start Discord automation process"""
        if self.config.get('discord_enabled'):
            discord_process = multiprocessing.Process(
                target=discord_automation_worker,
                args=(self.config, self.shutdown_flag),
                name="DiscordAutomation"
            )
            discord_process.start()
            self.processes.append(discord_process)
            self.logger.info("🤖 Discord automation process started")
        else:
            self.logger.warning("⚠️ Discord automation disabled - no token provided")
    
    def start_crewai_automation(self):
        """Start CrewAI automation process"""
        crewai_process = multiprocessing.Process(
            target=crewai_automation_worker,
            args=(self.config, self.shutdown_flag, self.stats_counter),
            name="CrewAIAutomation"
        )
        crewai_process.start()
        self.processes.append(crewai_process)
        self.logger.info("🧠 CrewAI automation process started")
    
    def monitor_ultimate_system(self):
        """Monitor the ultimate automation system"""
        self.logger.info("🔍 Starting ultimate system monitor...")
        
        try:
            while not self.shutdown_flag.value:
                # Check process health
                alive_processes = []
                for process in self.processes:
                    if process.is_alive():
                        alive_processes.append(process.name)
                    else:
                        self.logger.error(f"❌ Process {process.name} died! Exit code: {process.exitcode}")
                
                # Log comprehensive status
                status_info = {
                    'processes': alive_processes,
                    'automation_cycles': self.stats_counter.value,
                    'discord_enabled': self.config['discord_enabled'],
                    'github_enabled': self.config['github_enabled']
                }
                
                self.logger.info(f"📊 Ultimate System Status: {status_info}")
                
                # Wait before next check
                import time
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Ultimate system monitor interrupted")
    
    def shutdown(self):
        """Gracefully shutdown the ultimate system"""
        self.logger.info("🛑 Shutting down Ultimate AI Corporation Automation...")
        
        # Signal shutdown
        self.shutdown_flag.value = True
        
        # Wait for processes
        for process in self.processes:
            self.logger.info(f"🛑 Waiting for {process.name} to stop...")
            process.join(timeout=15)
            
            if process.is_alive():
                self.logger.warning(f"⚠️ Force terminating {process.name}...")
                process.terminate()
                process.join(timeout=5)
                
                if process.is_alive():
                    self.logger.error(f"❌ Killing {process.name}...")
                    process.kill()
        
        self.logger.info("✅ Ultimate system shutdown complete")
    
    def start(self):
        """Start the ultimate AI automation system"""
        try:
            self.logger.info("🚀 Starting Ultimate AI Corporation Automation System...")
            
            # Display system capabilities
            self.logger.info("🎯 System Capabilities:")
            self.logger.info("   🤖 Complete Discord server automation")
            self.logger.info("   🐙 Full GitHub repository management")  
            self.logger.info("   🧠 Advanced CrewAI agent coordination")
            self.logger.info("   🔄 Continuous development workflows")
            self.logger.info("   📊 Real-time monitoring and reporting")
            
            # Start automation processes
            self.start_discord_automation()
            self.start_crewai_automation()
            
            self.logger.info("✅ All automation processes started!")
            self.logger.info("🎉 Ultimate AI Corporation is now FULLY OPERATIONAL!")
            
            # Monitor system
            self.monitor_ultimate_system()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Received shutdown signal")
        except Exception as e:
            self.logger.error(f"❌ Ultimate system error: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.shutdown()

if __name__ == "__main__":
    # Enable multiprocessing on Windows
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)
    
    print("🎯 Ultimate AI Corporation Automation System")
    print("Founder: Steve Cornell (master80059)")
    print("=" * 60)
    print("🤖 Discord: Complete server automation")
    print("🐙 GitHub: Full repository management")
    print("🧠 CrewAI: Advanced agent coordination")
    print("🔄 Workflows: dev → testing → production")
    print("=" * 60)
    
    try:
        automation = UltimateAIAutomation()
        automation.start()
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()