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

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import real components
from ai_assistant.crews.proper_ai_crew import AutonomousCrewManager
from ai_assistant.discord.enhanced_bot import AIAssistantDiscordBot
from ai_assistant.github.manager import GitHubManager

class EnhancedAIPersonalAssistant:
    """Enhanced AI Personal Assistant with true multi-processing"""
    
    def __init__(self, config_path: str = "config/test.yaml"):
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.running = False
        
        # Load environment and configuration
        load_dotenv()
        self.config = self._load_configuration()
        
        # Process management
        self.processes = {}
        self.process_queue = multiprocessing.Queue()
        self.shutdown_event = multiprocessing.Event()
        
        # Shared state
        self.manager = multiprocessing.Manager()
        self.shared_state = self.manager.dict({
            'system_status': 'initializing',
            'discord_connected': False,
            'crew_active': False,
            'github_ready': False,
            'last_heartbeat': time.time()
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
            'cycle_interval': 600,  # 10 minutes
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
        def run_discord_bot():
            """Discord bot process function"""
            try:
                # Set up logging for this process
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - [DISCORD] - %(name)s - %(levelname)s - %(message)s'
                )
                logger = logging.getLogger("discord_process")
                
                logger.info("🤖 Starting Discord bot process...")
                
                # Create and run Discord bot
                bot = AIAssistantDiscordBot(self.config, None)  # No crew manager needed in this process
                
                # Update shared state
                self.shared_state['discord_connected'] = True
                
                # Run the bot
                discord_token = self.config.get('discord_token')
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
                        while not self.shutdown_event.is_set():
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
                self.shared_state['discord_connected'] = False
                logger.info("🤖 Discord bot process ended")
        
        # Start Discord process
        discord_process = multiprocessing.Process(
            target=run_discord_bot,
            name="DiscordBot"
        )
        discord_process.start()
        self.processes['discord'] = discord_process
        self.logger.info("🤖 Discord bot process started")
        return discord_process
    
    def start_crewai_process(self):
        """Start CrewAI system in separate process"""
        def run_crewai_system():
            """CrewAI system process function"""
            try:
                # Set up logging for this process
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - [CREWAI] - %(name)s - %(levelname)s - %(message)s'
                )
                logger = logging.getLogger("crewai_process")
                
                logger.info("🧠 Starting CrewAI system process...")
                
                # Create CrewAI manager
                crew_manager = AutonomousCrewManager(self.config)
                
                # Update shared state
                self.shared_state['crew_active'] = True
                
                # Run development cycles
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                async def run_crew_cycles():
                    cycle_count = 0
                    
                    while not self.shutdown_event.is_set():
                        try:
                            cycle_count += 1
                            logger.info(f"🔄 Starting development cycle {cycle_count}")
                            
                            # Run CrewAI development cycle
                            result = await crew_manager.run_development_cycle()
                            logger.info(f"✅ Cycle {cycle_count} completed: {result.get('status', 'completed')}")
                            
                            # Update shared state with results
                            self.shared_state['last_cycle_result'] = {
                                'cycle': cycle_count,
                                'status': result.get('status', 'completed'),
                                'timestamp': time.time(),
                                'summary': result.get('summary', 'Development cycle completed')
                            }
                            
                            # Wait for next cycle or shutdown
                            cycle_interval = self.config.get('cycle_interval', 600)
                            for _ in range(cycle_interval):
                                if self.shutdown_event.is_set():
                                    break
                                await asyncio.sleep(1)
                                
                        except Exception as e:
                            logger.error(f"❌ Error in crew cycle {cycle_count}: {e}")
                            await asyncio.sleep(60)  # Wait before retry
                
                # Run the crew system
                loop.run_until_complete(run_crew_cycles())
                
            except Exception as e:
                logger.error(f"❌ CrewAI process error: {e}")
                import traceback
                logger.error(traceback.format_exc())
            finally:
                self.shared_state['crew_active'] = False
                logger.info("🧠 CrewAI process ended")
        
        # Start CrewAI process
        crewai_process = multiprocessing.Process(
            target=run_crewai_system,
            name="CrewAI"
        )
        crewai_process.start()
        self.processes['crewai'] = crewai_process
        self.logger.info("🧠 CrewAI process started")
        return crewai_process
    
    def start_github_monitor_process(self):
        """Start GitHub monitoring in separate process"""
        def run_github_monitor():
            """GitHub monitoring process function"""
            try:
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - [GITHUB] - %(name)s - %(levelname)s - %(message)s'
                )
                logger = logging.getLogger("github_process")
                
                logger.info("🐙 Starting GitHub monitoring process...")
                
                github_token = self.config.get('github_token')
                if github_token:
                    # Create GitHub manager
                    github_manager = GitHubManager(
                        token=github_token,
                        config={'owner': self.config.get('founder_github', 'master80059'),
                               'repo': 'AI_personal_assistant'}
                    )
                    
                    self.shared_state['github_ready'] = True
                    
                    # Monitor GitHub events
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    async def monitor_github():
                        while not self.shutdown_event.is_set():
                            try:
                                # Monitor GitHub activity
                                logger.debug("🐙 Monitoring GitHub events...")
                                
                                # Update heartbeat
                                self.shared_state['last_heartbeat'] = time.time()
                                
                                await asyncio.sleep(300)  # Check every 5 minutes
                                
                            except Exception as e:
                                logger.error(f"GitHub monitoring error: {e}")
                                await asyncio.sleep(60)
                    
                    loop.run_until_complete(monitor_github())
                else:
                    logger.warning("⚠️ No GitHub token provided")
                    
            except Exception as e:
                logger.error(f"❌ GitHub process error: {e}")
            finally:
                self.shared_state['github_ready'] = False
                logger.info("🐙 GitHub process ended")
        
        # Start GitHub process
        github_process = multiprocessing.Process(
            target=run_github_monitor,
            name="GitHubMonitor"
        )
        github_process.start()
        self.processes['github'] = github_process
        self.logger.info("🐙 GitHub monitoring process started")
        return github_process
    
    def start_system_monitor_thread(self):
        """Start system monitoring in separate thread"""
        def monitor_system():
            """System monitoring thread function"""
            try:
                while self.running:
                    # Update system status
                    self.shared_state['system_status'] = 'running'
                    
                    # Log system status periodically
                    status = {
                        'discord_connected': self.shared_state.get('discord_connected', False),
                        'crew_active': self.shared_state.get('crew_active', False),
                        'github_ready': self.shared_state.get('github_ready', False),
                        'processes_running': len([p for p in self.processes.values() if p.is_alive()]),
                        'last_heartbeat': self.shared_state.get('last_heartbeat', 0)
                    }
                    
                    self.logger.info(f"📊 System Status: {status}")
                    
                    # Check for crashes and restart if needed
                    for name, process in self.processes.items():
                        if not process.is_alive() and self.running:
                            self.logger.warning(f"⚠️ Process {name} died, restarting...")
                            if name == 'discord':
                                self.start_discord_bot_process()
                            elif name == 'crewai':
                                self.start_crewai_process()
                            elif name == 'github':
                                self.start_github_monitor_process()
                    
                    time.sleep(60)  # Check every minute
                    
            except Exception as e:
                self.logger.error(f"❌ System monitor error: {e}")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_system, name="SystemMonitor")
        monitor_thread.daemon = True
        monitor_thread.start()
        self.logger.info("📊 System monitoring thread started")
        return monitor_thread
    
    def start(self):
        """Start the complete multi-process AI Personal Assistant"""
        try:
            self.logger.info("🚀 Starting Enhanced AI Personal Assistant with multi-processing...")
            self.running = True
            
            # Start all processes
            self.start_discord_bot_process()
            time.sleep(2)  # Allow Discord to initialize
            
            self.start_crewai_process()
            time.sleep(2)  # Allow CrewAI to initialize
            
            self.start_github_monitor_process()
            time.sleep(2)  # Allow GitHub to initialize
            
            # Start system monitoring
            self.start_system_monitor_thread()
            
            self.logger.info("✅ All processes started successfully")
            self.logger.info("🌟 AI Personal Assistant running with full multi-processing")
            
            # Wait for processes and handle shutdown
            self._wait_for_shutdown()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutdown requested by user")
        except Exception as e:
            self.logger.error(f"❌ Error starting system: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.shutdown()
    
    def _wait_for_shutdown(self):
        """Wait for shutdown signal"""
        try:
            # Set up signal handlers
            def signal_handler(signum, frame):
                self.logger.info(f"🛑 Received signal {signum}")
                self.shutdown()
                
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Wait for all processes
            while self.running and any(p.is_alive() for p in self.processes.values()):
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Keyboard interrupt received")
    
    def shutdown(self):
        """Shutdown all processes gracefully"""
        self.logger.info("🛑 Shutting down Enhanced AI Personal Assistant...")
        
        self.running = False
        self.shutdown_event.set()
        
        # Wait for processes to shutdown gracefully
        for name, process in self.processes.items():
            if process.is_alive():
                self.logger.info(f"🛑 Shutting down {name} process...")
                process.join(timeout=10)
                
                if process.is_alive():
                    self.logger.warning(f"⚠️ Force terminating {name} process...")
                    process.terminate()
                    process.join(timeout=5)
                    
                    if process.is_alive():
                        self.logger.error(f"❌ Failed to terminate {name} process")
        
        self.logger.info("✅ Enhanced AI Personal Assistant shutdown complete")


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