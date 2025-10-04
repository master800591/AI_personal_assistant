#!/usr/bin/env python3
"""
Simple Working AI Assistant
Complete working implementation without complex dependencies
"""
import asyncio
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Simple configuration
class SimpleConfig:
    def __init__(self, config_path: str = None):
        self.data = {
            'logging': {'level': 'INFO', 'file': 'logs/ai_assistant.log'},
            'ollama': {'host': 'localhost:11434', 'default_model': 'deepseek-r1'},
            'autonomous': {'enabled': True, 'cycle_interval': 300},
            'discord': {'enabled': False, 'token': None, 'command_prefix': '!ai'},
            'github': {'enabled': False, 'token': None}
        }
    
    def get(self, key: str, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# Simple logging setup
def setup_simple_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ai_assistant.log', encoding='utf-8')
        ]
    )

class SimpleAIAssistant:
    """Simple working AI Assistant"""
    
    def __init__(self, config_path: str = None):
        self.config = SimpleConfig(config_path)
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Import components dynamically
        self.autonomous_dev = None
        self.discord_bot = None
        
        self.logger.info("🤖 Simple AI Assistant initialized")
    
    async def start(self, dev_mode: bool = False, discord_only: bool = False, 
                   autonomous_only: bool = False, test_mode: bool = False):
        """Start the AI Assistant"""
        try:
            self.logger.info("🚀 Starting Simple AI Assistant...")
            
            # Initialize components
            if not discord_only:
                await self._init_autonomous()
            
            if not autonomous_only and self.config.get('discord.enabled'):
                await self._init_discord()
            
            self.running = True
            self.logger.info("✅ AI Assistant started successfully")
            
            # Run based on mode
            if test_mode:
                await self._run_test()
            elif discord_only:
                await self._run_discord_only()
            elif autonomous_only:
                await self._run_autonomous_only()
            else:
                await self._run_main_loop()
                
        except Exception as e:
            self.logger.error(f"❌ Failed to start: {e}")
            raise
    
    async def _init_autonomous(self):
        """Initialize autonomous development"""
        try:
            from .simple_autonomous import SimpleAutonomousDeveloper
            self.autonomous_dev = SimpleAutonomousDeveloper(self.config)
            self.logger.info("✅ Autonomous developer initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to init autonomous: {e}")
    
    async def _init_discord(self):
        """Initialize Discord bot"""
        try:
            token = self.config.get('discord.token')
            if token:
                from .simple_discord import SimpleDiscordBot
                self.discord_bot = SimpleDiscordBot(token)
                self.logger.info("✅ Discord bot initialized")
            else:
                self.logger.warning("⚠️ No Discord token found")
        except Exception as e:
            self.logger.error(f"❌ Failed to init Discord: {e}")
    
    async def _run_test(self):
        """Run test mode"""
        self.logger.info("🧪 Running test mode")
        if self.autonomous_dev:
            result = await self.autonomous_dev.analyze_file('src/ai_assistant/main.py')
            self.logger.info(f"📊 Test result: {result.get('suggestions', [])}")
        await asyncio.sleep(2)
        self.running = False
    
    async def _run_autonomous_only(self):
        """Run autonomous development only"""
        self.logger.info("🔄 Running autonomous mode")
        while self.running:
            if self.autonomous_dev:
                result = await self.autonomous_dev.run_cycle()
                self.logger.info(f"📊 Cycle complete: {result.get('files_analyzed', 0)} files")
            await asyncio.sleep(self.config.get('autonomous.cycle_interval', 300))
    
    async def _run_discord_only(self):
        """Run Discord bot only"""
        if self.discord_bot:
            self.logger.info("🤖 Running Discord bot")
            await self.discord_bot.start()
        else:
            self.logger.error("❌ Discord bot not available")
    
    async def _run_main_loop(self):
        """Run main application loop"""
        self.logger.info("🚀 Running main mode")
        
        # Start Discord bot if available
        discord_task = None
        if self.discord_bot:
            discord_task = asyncio.create_task(self.discord_bot.start())
        
        # Run autonomous cycles
        while self.running:
            try:
                if self.autonomous_dev:
                    result = await self.autonomous_dev.run_cycle()
                    self.logger.info(f"📊 Cycle: {result.get('files_analyzed', 0)} files analyzed")
                
                await asyncio.sleep(self.config.get('autonomous.cycle_interval', 300))
                
            except Exception as e:
                self.logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(60)
        
        # Cleanup
        if discord_task:
            discord_task.cancel()
    
    async def shutdown(self):
        """Shutdown the assistant"""
        self.logger.info("🛑 Shutting down...")
        self.running = False
        
        if self.discord_bot:
            await self.discord_bot.close()
        
        self.logger.info("✅ Shutdown complete")

# Main execution
async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple AI Assistant')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--test', action='store_true', help='Run test mode')
    parser.add_argument('--autonomous-only', action='store_true', help='Autonomous only')
    parser.add_argument('--discord-only', action='store_true', help='Discord only')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_simple_logging()
    
    # Create and start assistant
    assistant = SimpleAIAssistant(args.config)
    
    try:
        await assistant.start(
            test_mode=args.test,
            autonomous_only=args.autonomous_only,
            discord_only=args.discord_only
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await assistant.shutdown()

if __name__ == "__main__":
    asyncio.run(main())