#!/usr/bin/env python3
"""
Discord Bot Integration
Real-time notifications and command interface for AI Assistant
"""

import logging
import asyncio
from typing import Optional, Dict, Any

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)

class DiscordBot:
    """Discord bot for AI Assistant integration"""
    
    def __init__(self, token: str, config: Optional[Config] = None):
        """Initialize Discord bot"""
        if not DISCORD_AVAILABLE:
            raise ImportError("discord.py not installed. Install with: pip install discord.py")
        
        self.token = token
        self.config = config or Config()
        self.running = False
        
        # Bot configuration
        prefix = self.config.get('discord.command_prefix', '!ai')
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        self._setup_events()
        self._setup_commands()
        
        logger.info("🤖 Discord Bot initialized")
    
    def _setup_events(self):
        """Setup Discord bot events"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f"✅ Discord Bot connected as {self.bot.user}")
            
            # Set activity status
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="AI Development"
            )
            await self.bot.change_presence(activity=activity)
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"❌ Unknown command. Use `{ctx.prefix}help` for available commands.")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send(f"❌ An error occurred: {error}")
    
    def _setup_commands(self):
        """Setup Discord bot commands"""
        
        @self.bot.command(name='status')
        async def status_command(ctx):
            """Show AI Assistant status"""
            embed = discord.Embed(
                title="🤖 AI Assistant Status",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="✅ Online", inline=True)
            embed.add_field(name="Uptime", value="Active", inline=True)
            embed.add_field(name="Version", value="1.0.0", inline=True)
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name='help')
        async def help_command(ctx):
            """Show available commands"""
            embed = discord.Embed(
                title="🤖 AI Assistant Commands",
                description="Available commands for AI Assistant",
                color=discord.Color.blue()
            )
            
            commands_list = [
                ("status", "Show system status"),
                ("help", "Show this help message"),
                ("ping", "Test bot responsiveness"),
                ("info", "Show system information")
            ]
            
            for cmd, desc in commands_list:
                embed.add_field(
                    name=f"{ctx.prefix}{cmd}",
                    value=desc,
                    inline=False
                )
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name='ping')
        async def ping_command(ctx):
            """Test bot responsiveness"""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"🏓 Pong! Latency: {latency}ms")
        
        @self.bot.command(name='info')
        async def info_command(ctx):
            """Show system information"""
            embed = discord.Embed(
                title="🤖 AI Assistant Information",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Project", value="AI Personal Assistant", inline=True)
            embed.add_field(name="Version", value="1.0.0", inline=True)
            embed.add_field(name="Framework", value="discord.py", inline=True)
            embed.add_field(name="Python", value="3.8+", inline=True)
            embed.add_field(name="AI Models", value="Ollama Local", inline=True)
            embed.add_field(name="Repository", value="GitHub", inline=True)
            
            await ctx.send(embed=embed)
    
    async def send_notification(self, channel_id: int, message: str, embed: Optional[discord.Embed] = None):
        """Send notification to a specific channel"""
        try:
            channel = self.bot.get_channel(channel_id)
            if channel:
                if embed:
                    await channel.send(message, embed=embed)
                else:
                    await channel.send(message)
                logger.info(f"📢 Notification sent to channel {channel_id}")
            else:
                logger.warning(f"⚠️ Channel {channel_id} not found")
        except Exception as e:
            logger.error(f"❌ Failed to send notification: {e}")
    
    async def notify_development_cycle(self, cycle_result: Dict[str, Any]):
        """Send development cycle notification"""
        # Get notification channel from config
        channel_id = self.config.get('discord.notification_channel')
        if not channel_id:
            return
        
        if cycle_result['success']:
            embed = discord.Embed(
                title="🚀 Development Cycle Completed",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Cycle", 
                value=f"#{cycle_result['cycle']}", 
                inline=True
            )
            embed.add_field(
                name="Improvements", 
                value=f"{cycle_result['improvements_implemented']}/{cycle_result['improvements_found']}", 
                inline=True
            )
            embed.add_field(
                name="New Feature", 
                value="✅" if cycle_result.get('new_feature_created') else "❌", 
                inline=True
            )
            
            message = "✅ Autonomous development cycle completed successfully!"
        else:
            embed = discord.Embed(
                title="❌ Development Cycle Failed",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Cycle", 
                value=f"#{cycle_result['cycle']}", 
                inline=True
            )
            embed.add_field(
                name="Error", 
                value=cycle_result.get('error', 'Unknown error'), 
                inline=False
            )
            
            message = "❌ Autonomous development cycle failed!"
        
        await self.send_notification(channel_id, message, embed)
    
    async def start(self):
        """Start the Discord bot"""
        if not self.running:
            logger.info("🚀 Starting Discord Bot...")
            self.running = True
            try:
                await self.bot.start(self.token)
            except Exception as e:
                logger.error(f"❌ Discord Bot failed to start: {e}")
                self.running = False
                raise
    
    async def shutdown(self):
        """Gracefully shutdown the Discord bot"""
        if self.running:
            logger.info("🔄 Shutting down Discord Bot...")
            self.running = False
            await self.bot.close()
            logger.info("✅ Discord Bot shutdown complete")

def main():
    """Main entry point for Discord bot"""
    import sys
    import os
    
    # Get token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN environment variable not set")
        sys.exit(1)
    
    try:
        config = Config()
        bot = DiscordBot(token, config)
        
        # Run the bot
        asyncio.run(bot.start())
        
    except KeyboardInterrupt:
        logger.info("👋 Discord Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Discord Bot failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()