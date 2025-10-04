"""
Final Enhanced AI Personal Assistant with Simplified Multi-Processing
Founder: Steve Cornell (master80059) 
Working concurrent system with Discord Bot, CrewAI, and GitHub automation
"""

import os
import sys
import asyncio
import logging
import multiprocessing
import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment first
load_dotenv()

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def discord_bot_worker(config_dict, shutdown_flag):
    """Discord bot process worker - imports inside to avoid multiprocessing issues"""
    try:
        # Set up logging for this process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [DISCORD] - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("discord_worker")
        
        logger.info("🤖 Starting Discord bot process...")
        
        # Import Discord and GitHub modules inside worker to avoid multiprocessing conflicts
        import discord
        from discord.ext import commands
        from ai_assistant.discord.full_automation_bot import FullAutomationDiscordBot
        from ai_assistant.github.full_automation_manager import FullGitHubManager
        
        # Create GitHub manager first
        github_manager = None
        if config_dict.get('github_token'):
            github_manager = FullGitHubManager(config_dict['github_token'], config_dict)
            logger.info("✅ GitHub manager created with full automation")
        
        # Create Discord bot with GitHub integration
        bot = FullAutomationDiscordBot(config_dict, github_manager)
        
        # Get Discord token and run
        discord_token = config_dict.get('discord_token')
        if discord_token:
            logger.info("🔑 Discord token found, starting full automation bot...")
            
            # Run until shutdown flag is set
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_with_shutdown():
                try:
                    # Start bot
                    bot_task = asyncio.create_task(bot.start(discord_token))
                    
                    # Monitor shutdown
                    while not shutdown_flag.value:
                        await asyncio.sleep(1)
                    
                    logger.info("🛑 Shutdown requested, closing bot...")
                    await bot.close()
                    
                except Exception as e:
                    logger.error(f"❌ Bot error: {e}")
            
            loop.run_until_complete(run_with_shutdown())
        else:
            logger.error("❌ No Discord token provided")
        
    except Exception as e:
        logger.error(f"❌ Discord worker error: {e}")
        import traceback
        traceback.print_exc()

def crewai_worker(config_dict, shutdown_flag, cycle_counter):
    """CrewAI system worker - imports inside to avoid multiprocessing issues"""
    try:
        # Set up logging for this process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [CREWAI] - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("crewai_worker")
        
        logger.info("🧠 Starting CrewAI system process...")
        
        # Import CrewAI modules inside worker to avoid multiprocessing conflicts
        try:
            from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
            logger.info("✅ CrewAI imports successful")
        except Exception as e:
            logger.error(f"❌ CrewAI import failed: {e}")
            return
        
        # Create CrewAI manager
        try:
            crew_manager = AutonomousCrewManager(config_dict)
            logger.info("✅ CrewAI manager created")
        except Exception as e:
            logger.error(f"❌ CrewAI manager creation failed: {e}")
            return
        
        # Run development cycles
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_cycles():
            cycle_count = 0
            
            while not shutdown_flag.value:
                try:
                    logger.info(f"🔄 Starting development cycle #{cycle_count + 1}")
                    
                    # Run development cycle
                    result = await crew_manager.run_development_cycle()
                    
                    if result and result.get('success'):
                        logger.info(f"✅ Development cycle #{cycle_count + 1} completed successfully")
                        cycle_count += 1
                        cycle_counter.value = cycle_count
                    else:
                        logger.warning(f"⚠️ Development cycle #{cycle_count + 1} had issues")
                    
                    # Wait for next cycle or shutdown
                    logger.info(f"⏰ Waiting {config_dict.get('cycle_interval', 300)} seconds for next cycle...")
                    for _ in range(config_dict.get('cycle_interval', 300)):  # 5 minutes default
                        if shutdown_flag.value:
                            break
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.error(f"❌ Crew cycle error: {e}")
                    await asyncio.sleep(30)  # Wait before retry
            
            logger.info("🛑 CrewAI cycles stopped")
        
        # Run the cycles
        loop.run_until_complete(run_cycles())
        
    except Exception as e:
        logger.error(f"❌ CrewAI worker error: {e}")
        import traceback
        traceback.print_exc()

class SimplifiedAIPersonalAssistant:
    """Simplified AI Personal Assistant with Working Multi-Processing"""
    
    def __init__(self):
        """Initialize the assistant"""
        self.logger = self._setup_logging()
        
        # Load configuration
        self.config = self._load_configuration()
        
        # Multiprocessing components
        self.manager = multiprocessing.Manager()
        self.shutdown_flag = self.manager.Value('b', False)
        self.cycle_counter = self.manager.Value('i', 0)
        self.processes = []
        
        self.logger.info("🤖 Simplified AI Personal Assistant initialized")
        self.logger.info(f"👑 Founder: {self.config.get('founder_name', 'Steve Cornell')}")
    
    def _setup_logging(self):
        """Setup logging"""
        Path("logs").mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [MAIN] - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/ai_assistant_final.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration"""
        return {
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'founder_name': os.getenv('AI_CORP_FOUNDER', 'Steve Cornell'),
            'founder_github': 'master80059',
            'cycle_interval': 180,  # 3 minutes for testing
            'discord_enabled': bool(os.getenv('DISCORD_BOT_TOKEN')),
            'github_enabled': bool(os.getenv('GITHUB_TOKEN')),
        }
    
    def start_discord_process(self):
        """Start Discord bot process"""
        if self.config.get('discord_enabled'):
            discord_process = multiprocessing.Process(
                target=discord_bot_worker,
                args=(self.config, self.shutdown_flag),
                name="DiscordBot"
            )
            discord_process.start()
            self.processes.append(discord_process)
            self.logger.info("🤖 Discord bot process started")
        else:
            self.logger.warning("⚠️ Discord disabled - no token provided")
    
    def start_crewai_process(self):
        """Start CrewAI process"""
        crewai_process = multiprocessing.Process(
            target=crewai_worker,
            args=(self.config, self.shutdown_flag, self.cycle_counter),
            name="CrewAI"
        )
        crewai_process.start()
        self.processes.append(crewai_process)
        self.logger.info("🧠 CrewAI process started")
    
    def monitor_system(self):
        """Monitor system health"""
        self.logger.info("🔍 Starting system monitor...")
        
        try:
            while not self.shutdown_flag.value:
                # Check process health
                alive_processes = []
                for process in self.processes:
                    if process.is_alive():
                        alive_processes.append(process.name)
                    else:
                        self.logger.error(f"❌ Process {process.name} died! Exit code: {process.exitcode}")
                
                # Log status
                status_info = f"Processes: {', '.join(alive_processes)}, Cycles: {self.cycle_counter.value}"
                self.logger.info(f"📊 System Status: {status_info}")
                
                # Wait before next check
                time.sleep(30)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Monitor interrupted")
    
    def shutdown(self):
        """Shutdown all processes"""
        self.logger.info("🛑 Shutting down AI Personal Assistant...")
        
        # Signal shutdown
        self.shutdown_flag.value = True
        
        # Wait for processes
        for process in self.processes:
            self.logger.info(f"🛑 Waiting for {process.name} to stop...")
            process.join(timeout=10)
            
            if process.is_alive():
                self.logger.warning(f"⚠️ Force terminating {process.name}...")
                process.terminate()
                process.join(timeout=5)
                
                if process.is_alive():
                    self.logger.error(f"❌ Killing {process.name}...")
                    process.kill()
        
        self.logger.info("✅ Shutdown complete")
    
    def start(self):
        """Start the complete system"""
        try:
            self.logger.info("🚀 Starting Simplified AI Personal Assistant...")
            
            # Start processes
            self.start_discord_process()
            self.start_crewai_process()
            
            self.logger.info("✅ All processes started!")
            
            # Monitor system
            self.monitor_system()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Received shutdown signal")
        except Exception as e:
            self.logger.error(f"❌ System error: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.shutdown()

if __name__ == "__main__":
    # Enable multiprocessing on Windows
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)
    
    print("🤖 Final AI Personal Assistant with Multi-Processing")
    print("Founder: Steve Cornell (master80059)")
    print("=" * 60)
    
    try:
        assistant = SimplifiedAIPersonalAssistant()
        assistant.start()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()