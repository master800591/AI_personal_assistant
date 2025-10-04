#!/usr/bin/env python3
"""
Simple Working Discord Bot
"""
import asyncio
import logging
from typing import Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

class SimpleDiscordBot:
    """Simple Discord bot implementation"""
    
    def __init__(self, token: str):
        self.token = token
        self.bot = None
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the Discord bot"""
        if not DISCORD_AVAILABLE:
            self.logger.warning("Discord.py not available")
            return
        
        if not self.token:
            self.logger.warning("No Discord token provided")
            return
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            
            self.bot = commands.Bot(
                command_prefix='!ai',
                intents=intents,
                help_command=None
            )
            
            @self.bot.event
            async def on_ready():
                self.logger.info(f"✅ Discord bot ready: {self.bot.user}")
            
            @self.bot.command(name='status')
            async def status(ctx):
                embed = discord.Embed(
                    title="🤖 AI Assistant Status",
                    description="System is operational",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            
            @self.bot.command(name='ping')
            async def ping(ctx):
                await ctx.send("🏓 Pong! AI Assistant is online!")
            
            await self.bot.start(self.token)
            
        except Exception as e:
            self.logger.error(f"❌ Discord bot error: {e}")
    
    async def close(self):
        """Close the bot"""
        if self.bot:
            await self.bot.close()