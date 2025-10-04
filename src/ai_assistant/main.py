#!/usr/bin/env python3
"""
Main AI Assistant Entry Point
Professional entry point for the AI Personal Assistant
"""

import sys
import logging
import asyncio
from pathlib import Path
from typing import Optional

from .utils.config import Config
from .utils.logging import setup_logging, get_logger
from .crews.proper_ai_crew import AutonomousCrewManager
from .discord.bot import DiscordBot
from .github.manager import GitHubManager
from .ollama.toolkit import OllamaToolkit

class AIAssistant:
    """Main AI Assistant orchestrator"""
    
    def __init__(self, config: Config):
        """Initialize AI Assistant with configuration"""
        self.config = config
        self.logger = get_logger(__name__)
        
        # Core components
        self.ollama_toolkit: Optional[OllamaToolkit] = None
        self.crew_manager: Optional[AutonomousCrewManager] = None
        self.discord_bot: Optional[DiscordBot] = None
        self.github_manager: Optional[GitHubManager] = None
        
        # State
        self.running = False
        
        self.logger.info("🤖 AI Assistant initialized")
    
    async def start(self, dev_mode: bool = False, discord_only: bool = False, 
                   autonomous_only: bool = False, test_mode: bool = False) -> None:
        """Start the AI Assistant with specified modes"""
        try:
            self.logger.info("🚀 Starting AI Assistant components...")
            
            # Initialize Ollama toolkit
            await self._initialize_ollama()
            
            # Initialize components based on mode
            if not discord_only:
                await self._initialize_ai_crew()
            
            if not autonomous_only and self.config.get('discord.enabled', False):
                await self._initialize_discord_bot()
            
            if not test_mode and self.config.get('github.enabled', True):
                await self._initialize_github_manager()
            
            self.running = True
            self.logger.info("✅ AI Assistant started successfully")
            
            # Start main loop based on mode
            if discord_only:
                await self._run_discord_only()
            elif autonomous_only:
                await self._run_autonomous_only()
            elif test_mode:
                await self._run_test_mode()
            else:
                await self._run_full_mode()
                
        except Exception as e:
            self.logger.error(f"❌ Failed to start AI Assistant: {e}")
            raise
    
    async def _initialize_ollama(self) -> None:
        """Initialize Ollama toolkit"""
        try:
            host = self.config.get('ollama.host', 'localhost:11434')
            self.ollama_toolkit = OllamaToolkit(host=host)
            self.logger.info("✅ Ollama toolkit initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Ollama: {e}")
            raise
    
    async def _initialize_ai_crew(self) -> None:
        """Initialize AI CrewAI system"""
        try:
            self.crew_manager = AutonomousCrewManager(self.config, self.ollama_toolkit)
            await self.crew_manager.initialize_crew()
            self.logger.info("✅ AI CrewAI system initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AI Crew: {e}")
            raise
    
    async def _initialize_discord_bot(self) -> None:
        """Initialize Discord bot"""
        try:
            discord_token = self.config.get('discord.token')
            if discord_token:
                self.discord_bot = DiscordBot(discord_token, self.config)
                self.logger.info("✅ Discord bot initialized")
            else:
                self.logger.warning("⚠️ Discord token not found, skipping Discord bot")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Discord bot: {e}")
            raise
    
    async def _initialize_github_manager(self) -> None:
        """Initialize GitHub manager"""
        try:
            if self.config.get('github.token'):
                self.github_manager = GitHubManager(
                    self.config.get('github.token'),
                    self.config
                )
                self.logger.info("✅ GitHub manager initialized")
            else:
                self.logger.warning("⚠️ GitHub token not found, skipping GitHub integration")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize GitHub manager: {e}")
    
    async def _run_discord_only(self) -> None:
        """Run Discord bot only"""
        if self.discord_bot:
            self.logger.info("🤖 Running Discord bot only mode")
            await self.discord_bot.start()
        else:
            self.logger.error("❌ Discord bot not initialized")
    
    async def _run_autonomous_only(self) -> None:
        """Run CrewAI development cycles only"""
        if self.crew_manager:
            self.logger.info("🔄 Running CrewAI development mode")
            while self.running:
                try:
                    result = await self.crew_manager.run_development_cycle()
                    self.logger.info(f"✅ Development cycle completed: {result.get('success', False)}")
                    await asyncio.sleep(self.config.get('autonomous.cycle_interval', 600))
                except Exception as e:
                    self.logger.error(f"❌ Error in CrewAI cycle: {e}")
                    await asyncio.sleep(60)  # Brief pause before retry
        else:
            self.logger.error("❌ AI Crew Manager not initialized")
    
    async def _run_test_mode(self) -> None:
        """Run in test mode"""
        self.logger.info("🧪 Running in test mode")
        if self.crew_manager:
            result = await self.crew_manager.run_development_cycle('src/ai_assistant/main.py')
            self.logger.info(f"📊 Test CrewAI result: {result.get('success', False)}")
        await asyncio.sleep(5)  # Brief test run
        self.running = False
    
    async def _run_full_mode(self) -> None:
        """Run full AI Assistant mode"""
        self.logger.info("🚀 Running full AI Assistant mode")
        
        # Start Discord bot if available
        discord_task = None
        if self.discord_bot:
            discord_task = asyncio.create_task(self.discord_bot.start())
        
        # Run CrewAI development cycles
        while self.running:
            try:
                if self.crew_manager:
                    result = await self.crew_manager.run_development_cycle()
                    self.logger.info(f"✅ CrewAI cycle completed: {result.get('success', False)}")
                await asyncio.sleep(self.config.get('autonomous.cycle_interval', 600))
            except Exception as e:
                self.logger.error(f"❌ Error in full mode cycle: {e}")
                await asyncio.sleep(60)
        
        # Cleanup Discord task
        if discord_task:
            discord_task.cancel()
    
    async def shutdown(self) -> None:
        """Graceful shutdown"""
        self.logger.info("🛑 Shutting down AI Assistant...")
        self.running = False
        
        if self.discord_bot:
            # Discord bot will be shutdown via shutdown() method
            pass
        
        self.logger.info("✅ AI Assistant shutdown complete")
    
    async def initialize_components(self):
        """Initialize all AI components"""
        try:
            # Initialize AI Crew Manager
            if self.config.get('autonomous.enabled', True):
                self.crew_manager = AutonomousCrewManager(self.config, self.ollama_toolkit)
                await self.crew_manager.initialize_crew()
                self.logger.info("✅ AI Crew Manager initialized")
            
            # Initialize Discord bot
            if self.config.get('discord.enabled', False):
                discord_token = self.config.get('discord.bot_token')
                if discord_token:
                    self.discord_bot = DiscordBot(discord_token, self.config)
                    self.logger.info("✅ Discord Bot initialized")
                else:
                    self.logger.warning("⚠️ Discord enabled but no token provided")
            
            # Initialize GitHub manager
            github_token = self.config.get('github.token')
            if github_token:
                self.github_manager = GitHubManager(github_token, self.config)
                self.logger.info("✅ GitHub Manager initialized")
            else:
                self.logger.warning("⚠️ No GitHub token provided")
                
        except Exception as e:
            self.logger.error(f"❌ Component initialization failed: {e}")
            raise
    
    async def start(self):
        """Start the AI Assistant"""
        self.logger.info("🚀 Starting AI Assistant...")
        
        try:
            await self.initialize_components()
            
            # Create tasks for concurrent execution
            tasks = []
            
            # Start autonomous development if enabled
            if self.crew_manager and self.config.get('autonomous.enabled', True):
                tasks.append(asyncio.create_task(self._run_autonomous_loop()))
            
            # CrewAI runs synchronously when needed, not as background task
            # Start Discord bot
            if self.discord_bot:
                tasks.append(asyncio.create_task(self.discord_bot.start()))
            
            # Wait for all tasks to complete
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            else:
                self.logger.warning("⚠️ No components enabled, exiting")
                
        except KeyboardInterrupt:
            self.logger.info("👋 AI Assistant stopped by user")
        except Exception as e:
            self.logger.error(f"❌ AI Assistant error: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def _run_autonomous_loop(self):
        """Run autonomous development in a loop"""
        cycle_interval = self.config.get('autonomous.cycle_interval', 600)  # 10 minutes default
        
        while True:
            try:
                self.logger.info("🤖 Starting autonomous development cycle")
                result = await self.crew_manager.run_development_cycle()
                
                if result.get('success'):
                    self.logger.info("✅ Autonomous development cycle completed successfully")
                else:
                    self.logger.warning(f"⚠️ Autonomous development cycle failed: {result.get('error')}")
                
                # Wait for next cycle
                await asyncio.sleep(cycle_interval)
                
            except asyncio.CancelledError:
                self.logger.info("🛑 Autonomous development loop cancelled")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in autonomous development loop: {e}")
                # Wait before retrying
                await asyncio.sleep(60)
    
    async def shutdown(self):
        """Gracefully shutdown all components"""
        self.logger.info("🔄 Shutting down AI Assistant...")
        
        shutdown_tasks = []
        
        # Shutdown AI Crew Manager (no async shutdown needed)
        if self.crew_manager:
            self.logger.info("💫 Shutting down AI Crew Manager...")
        
        if self.discord_bot:
            shutdown_tasks.append(asyncio.create_task(self.discord_bot.shutdown()))
        
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        self.logger.info("✅ AI Assistant shutdown complete")
    
    def run(self):
        """Run the AI Assistant (sync wrapper)"""
        try:
            if sys.version_info >= (3, 7):
                asyncio.run(self.start())
            else:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            print("👋 AI Assistant stopped")
        except Exception as e:
            print(f"❌ AI Assistant failed: {e}")
            sys.exit(1)

def main():
    """Main entry point for console script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Personal Assistant")
    parser.add_argument(
        "--config", 
        "-c", 
        help="Configuration file path", 
        default=None
    )
    parser.add_argument(
        "--dev-mode", 
        action="store_true", 
        help="Enable development mode"
    )
    parser.add_argument(
        "--discord-only", 
        action="store_true", 
        help="Run Discord bot only"
    )
    parser.add_argument(
        "--autonomous-only", 
        action="store_true", 
        help="Run autonomous developer only"
    )
    
    args = parser.parse_args()
    
    # Create configuration object
    config = Config(args.config)
    
    # Create and run assistant
    assistant = AIAssistant(config)
    
    # Override config based on arguments
    if args.dev_mode:
        assistant.config.set('logging.level', 'DEBUG')
        assistant.config.set('autonomous.cycle_interval', 60)  # 1 minute cycles
    
    if args.discord_only:
        assistant.config.set('autonomous.enabled', False)
        assistant.config.set('discord.enabled', True)
    
    if args.autonomous_only:
        assistant.config.set('discord.enabled', False)
        assistant.config.set('autonomous.enabled', True)
    
    assistant.run()

if __name__ == "__main__":
    main()