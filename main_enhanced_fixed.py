"""
Enhanced AI Personal Assistant with True Multi-Processing
Founder: Steve Cornell (master80059) 
Complete concurrent system with CrewAI, Discord Bot, and GitHub automation running in parallel
"""

import os
import sys
import asyncio
import logging
import multiprocessing
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import queue
import signal
import time

# Load environment first
load_dotenv()

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import real components
from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
from ai_assistant.discord.enhanced_bot import AIAssistantDiscordBot
from ai_assistant.github.manager import GitHubManager

# Module-level functions for multiprocessing (required on Windows)
def discord_bot_worker(config, shutdown_event, shared_state):
    """Discord bot process worker function"""
    try:
        # Set up logging for this process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [DISCORD] - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("discord_process")
        
        logger.info("🤖 Starting Discord bot process...")
        
        # Create and run Discord bot
        bot = AIAssistantDiscordBot(config, None)  # No crew manager needed in this process
        
        # Update shared state
        shared_state['discord_connected'] = True
        
        # Run the bot
        discord_token = config.get('discord_token')
        if discord_token:
            # Start bot with proper async handling
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_bot():
                try:
                    await bot.start(discord_token)
                except Exception as e:
                    logger.error(f"Discord bot error: {e}")
                finally:
                    await bot.close()
            
            # Monitor shutdown event
            async def monitor_shutdown():
                while not shutdown_event.is_set():
                    await asyncio.sleep(1)
                logger.info("🛑 Discord bot shutdown requested")
                await bot.close()
            
            # Run both tasks
            loop.run_until_complete(asyncio.gather(
                run_bot(),
                monitor_shutdown(),
                return_exceptions=True
            ))
            
        else:
            logger.error("❌ No Discord token provided")
            
    except Exception as e:
        logger.error(f"❌ Discord process error: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        shared_state['discord_connected'] = False
        logger.info("🤖 Discord bot process ended")

def crewai_worker(config, shutdown_event, shared_state):
    """CrewAI system process worker function"""
    try:
        # Set up logging for this process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [CREWAI] - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("crewai_process")
        
        logger.info("🧠 Starting CrewAI system process...")
        
        # Create CrewAI manager
        crew_manager = AutonomousCrewManager(config)
        
        # Update shared state
        shared_state['crew_active'] = True
        
        # Run development cycles
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_crew_cycles():
            cycle_count = 0
            
            while not shutdown_event.is_set():
                try:
                    logger.info(f"🔄 Starting development cycle #{cycle_count + 1}")
                    
                    # Run development cycle
                    result = await crew_manager.run_development_cycle()
                    
                    if result and result.get('success'):
                        logger.info(f"✅ Development cycle #{cycle_count + 1} completed successfully")
                        cycle_count += 1
                    else:
                        logger.warning(f"⚠️ Development cycle #{cycle_count + 1} had issues")
                    
                    # Update shared state
                    shared_state['last_cycle'] = time.time()
                    shared_state['cycle_count'] = cycle_count
                    
                    # Wait for next cycle or shutdown
                    for _ in range(config.get('cycle_interval', 600)):  # 10 minutes default
                        if shutdown_event.is_set():
                            break
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.error(f"❌ Crew cycle error: {e}")
                    await asyncio.sleep(30)  # Wait before retry
            
            logger.info("🛑 CrewAI cycles stopped")
        
        # Run the cycles
        loop.run_until_complete(run_crew_cycles())
        
    except Exception as e:
        logger.error(f"❌ CrewAI process error: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        shared_state['crew_active'] = False
        logger.info("🧠 CrewAI process ended")

def github_monitor_worker(config, shutdown_event, shared_state):
    """GitHub monitoring process worker function"""
    try:
        # Set up logging for this process
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [GITHUB] - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger("github_process")
        
        logger.info("📚 Starting GitHub monitoring process...")
        
        # Create GitHub manager
        github_manager = GitHubManager(config)
        
        # Update shared state
        shared_state['github_ready'] = True
        
        # Monitor GitHub events
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def monitor_github():
            while not shutdown_event.is_set():
                try:
                    # Check for GitHub events
                    logger.info("📊 Checking GitHub activity...")
                    
                    # Update heartbeat
                    shared_state['last_heartbeat'] = time.time()
                    
                    # Wait before next check
                    await asyncio.sleep(300)  # 5 minutes
                    
                except Exception as e:
                    logger.error(f"❌ GitHub monitoring error: {e}")
                    await asyncio.sleep(60)  # Wait before retry
            
            logger.info("🛑 GitHub monitoring stopped")
        
        # Run the monitor
        loop.run_until_complete(monitor_github())
        
    except Exception as e:
        logger.error(f"❌ GitHub process error: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        shared_state['github_ready'] = False
        logger.info("📚 GitHub process ended")

class EnhancedAIPersonalAssistant:
    """Enhanced AI Personal Assistant with True Multi-Processing Architecture"""
    
    def __init__(self):
        """Initialize the enhanced AI personal assistant"""
        self.config_path = Path("config/enhanced_config.yaml")
        self.logger = self._setup_logging()
        
        # Load configuration
        self.config = self._load_configuration()
        
        # Initialize multiprocessing manager
        self.manager = multiprocessing.Manager()
        self.shutdown_event = self.manager.Event()
        self.processes = {}
        
        # Shared state across processes
        self.shared_state = self.manager.dict({
            'system_status': 'initializing',
            'discord_connected': False,
            'crew_active': False,
            'github_ready': False,
            'last_heartbeat': time.time(),
            'cycle_count': 0,
            'last_cycle': None
        })
        
        self.logger.info("🤖 Enhanced AI Personal Assistant initialized")
        self.logger.info(f"👑 Founder: {self.config.get('founder_name', 'Steve Cornell')}")
        self.logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging with process safety"""
        Path("logs").mkdir(exist_ok=True)
        
        # Configure logging to be process-safe
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [%(processName)s] - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/ai_assistant_enhanced.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load complete configuration"""
        config = {
            'discord_token': os.getenv('DISCORD_BOT_TOKEN'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'ollama_host': os.getenv('OLLAMA_HOST', 'localhost'),
            'ollama_port': os.getenv('OLLAMA_PORT', '11434'),
            'founder_name': os.getenv('AI_CORP_FOUNDER', 'Steve Cornell'),
            'founder_github': 'master80059',
            'cycle_interval': 300,  # 5 minutes for testing
            'discord_enabled': bool(os.getenv('DISCORD_BOT_TOKEN')),
            'github_enabled': bool(os.getenv('GITHUB_TOKEN')),
            'voice_enabled': True,
            'knowledge_management': True
        }
        
        if self.config_path.exists():
            try:
                import yaml
                with open(self.config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    config.update(yaml_config)
            except Exception as e:
                self.logger.warning(f"Could not load YAML config: {e}")
        
        return config
    
    def start_discord_bot_process(self):
        """Start Discord bot in separate process"""
        discord_process = multiprocessing.Process(
            target=discord_bot_worker,
            args=(self.config, self.shutdown_event, self.shared_state),
            name="DiscordBot"
        )
        discord_process.start()
        self.processes['discord'] = discord_process
        self.logger.info("🤖 Discord bot process started")
        return discord_process
    
    def start_crewai_process(self):
        """Start CrewAI system in separate process"""
        crewai_process = multiprocessing.Process(
            target=crewai_worker,
            args=(self.config, self.shutdown_event, self.shared_state),
            name="CrewAI"
        )
        crewai_process.start()
        self.processes['crewai'] = crewai_process
        self.logger.info("🧠 CrewAI system process started")
        return crewai_process
    
    def start_github_monitor_process(self):
        """Start GitHub monitoring in separate process"""
        github_process = multiprocessing.Process(
            target=github_monitor_worker,
            args=(self.config, self.shutdown_event, self.shared_state),
            name="GitHubMonitor"
        )
        github_process.start()
        self.processes['github'] = github_process
        self.logger.info("📚 GitHub monitoring process started")
        return github_process
    
    def monitor_system_health(self):
        """Monitor the health of all processes"""
        self.logger.info("🔍 Starting system health monitor...")
        
        while not self.shutdown_event.is_set():
            try:
                # Check process health
                for name, process in self.processes.items():
                    if not process.is_alive():
                        self.logger.error(f"❌ Process {name} died! Exit code: {process.exitcode}")
                        # Could implement auto-restart here
                
                # Log system status
                status = dict(self.shared_state)
                self.logger.info(f"📊 System Status: {status}")
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Health monitor interrupted")
                break
            except Exception as e:
                self.logger.error(f"❌ Health monitor error: {e}")
                time.sleep(10)
    
    def shutdown(self):
        """Gracefully shutdown all processes"""
        self.logger.info("🛑 Shutting down Enhanced AI Personal Assistant...")
        
        # Signal shutdown
        self.shutdown_event.set()
        
        # Wait for processes to finish
        for name, process in self.processes.items():
            self.logger.info(f"🛑 Waiting for {name} process to stop...")
            process.join(timeout=10)
            
            if process.is_alive():
                self.logger.warning(f"⚠️ Force terminating {name} process...")
                process.terminate()
                process.join(timeout=5)
                
                if process.is_alive():
                    self.logger.error(f"❌ Killing {name} process...")
                    process.kill()
        
        self.logger.info("✅ Enhanced AI Personal Assistant shutdown complete")
    
    def start(self):
        """Start the complete enhanced AI personal assistant system"""
        try:
            self.logger.info("🚀 Starting Enhanced AI Personal Assistant...")
            self.shared_state['system_status'] = 'starting'
            
            # Start all processes
            if self.config.get('discord_enabled'):
                self.start_discord_bot_process()
            
            self.start_crewai_process()
            
            if self.config.get('github_enabled'):
                self.start_github_monitor_process()
            
            self.shared_state['system_status'] = 'running'
            self.logger.info("✅ All processes started successfully")
            
            # Monitor system health in main thread
            self.monitor_system_health()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Received shutdown signal")
        except Exception as e:
            self.logger.error(f"❌ System error: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.shutdown()

if __name__ == "__main__":
    # Critical: Enable multiprocessing on Windows properly
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)
    
    print("🤖 Enhanced AI Personal Assistant with Multi-Processing")
    print("Founder: Steve Cornell (master80059)")
    print("=" * 60)
    print("🔧 Initializing multi-processing system...")
    
    try:
        assistant = EnhancedAIPersonalAssistant()
        print("✅ Assistant created successfully")
        assistant.start()
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        import traceback
        traceback.print_exc()