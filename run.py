#!/usr/bin/env python3
"""
AI Personal Assistant - Complete Working System
Entry point for the autonomous AI development platform
"""

import asyncio
import argparse
import sys
import signal
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_assistant.main import AIAssistant
from ai_assistant.utils.config import Config
from ai_assistant.utils.logging import setup_logging, get_logger

logger = get_logger(__name__)

class AIPersonalAssistant:
    """Main application controller"""
    
    def __init__(self):
        self.ai_assistant: Optional[AIAssistant] = None
        self.shutdown_event = asyncio.Event()
    
    async def start(self, config_path: str = None, **kwargs):
        """Start the AI Personal Assistant"""
        try:
            # Load configuration
            config = Config(config_path) if config_path else Config()
            
            # Setup logging
            setup_logging(config)
            logger.info("🚀 Starting AI Personal Assistant...")
            
            # Initialize AI Assistant
            self.ai_assistant = AIAssistant(config)
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            # Start the system
            await self.ai_assistant.start(**kwargs)
            
            logger.info("✅ AI Personal Assistant started successfully")
            
            # Keep running until shutdown
            await self.shutdown_event.wait()
            
        except Exception as e:
            logger.error(f"❌ Failed to start AI Personal Assistant: {e}")
            raise
        finally:
            if self.ai_assistant:
                await self.ai_assistant.shutdown()
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"🛑 Received signal {signum}, shutting down...")
            self.shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Personal Assistant')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--dev-mode', action='store_true', help='Enable development mode')
    parser.add_argument('--discord-only', action='store_true', help='Run Discord bot only')
    parser.add_argument('--autonomous-only', action='store_true', help='Run autonomous developer only')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    args = parser.parse_args()
    
    app = AIPersonalAssistant()
    
    try:
        await app.start(
            config_path=args.config,
            dev_mode=args.dev_mode,
            discord_only=args.discord_only,
            autonomous_only=args.autonomous_only,
            test_mode=args.test
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())