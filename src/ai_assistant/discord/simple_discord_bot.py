#!/usr/bin/env python3
"""
Simple Discord Bot for AI Corporation
Lightweight bot without privileged intents for easy deployment
"""
import discord
import asyncio
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAICorporationBot:
    """Simple AI Corporation Discord bot"""
    
    def __init__(self, token: str):
        # Use minimal intents to avoid permission issues
        intents = discord.Intents.default()
        intents.message_content = True  # For reading messages
        
        self.client = discord.Client(intents=intents)
        self.token = token
        self.setup_events()
    
    def setup_events(self):
        """Set up Discord event handlers"""
        
        @self.client.event
        async def on_ready():
            logger.info(f'✅ AI Corporation Bot connected as {self.client.user}')
            logger.info(f'📊 Connected to {len(self.client.guilds)} servers')
            
            # Set bot status
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="AI Corporation Operations"
            )
            await self.client.change_presence(activity=activity)
        
        @self.client.event
        async def on_message(message):
            # Don't respond to ourselves
            if message.author == self.client.user:
                return
            
            # Basic command handling
            if message.content.startswith('!ai'):
                await self.handle_command(message)
    
    async def handle_command(self, message):
        """Handle AI Corporation commands"""
        command = message.content.lower().strip()
        
        try:
            if command == '!ai status':
                embed = discord.Embed(
                    title="🤖 AI Corporation Status",
                    description="Autonomous AI system operational",
                    color=0x00ff00,
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="🧠 Self-Evolution", value="Active", inline=True)
                embed.add_field(name="🛡️ Security", value="Protected", inline=True)
                embed.add_field(name="🌐 Network", value="Connected", inline=True)
                embed.add_field(name="📊 Operations", value="Nominal", inline=True)
                embed.set_footer(text="AI Corporation • Autonomous Operations")
                
                await message.channel.send(embed=embed)
            
            elif command == '!ai help':
                embed = discord.Embed(
                    title="🤖 AI Corporation Commands",
                    description="Available bot commands",
                    color=0x0099ff
                )
                embed.add_field(
                    name="Commands",
                    value="""
                    `!ai status` - System status
                    `!ai help` - This help message
                    `!ai info` - Corporation information
                    `!ai ping` - Connection test
                    """,
                    inline=False
                )
                
                await message.channel.send(embed=embed)
            
            elif command == '!ai info':
                embed = discord.Embed(
                    title="🏢 AI Corporation",
                    description="Autonomous AI system with democratic governance",
                    color=0xff9900
                )
                embed.add_field(
                    name="🎯 Mission",
                    value="Self-evolving AI with founder protection protocols",
                    inline=False
                )
                embed.add_field(
                    name="🔧 Features", 
                    value="• Self-evolution system\n• GitHub workflow integration\n• P2P networking\n• Security protocols",
                    inline=False
                )
                
                await message.channel.send(embed=embed)
            
            elif command == '!ai ping':
                start_time = asyncio.get_event_loop().time()
                msg = await message.channel.send("🏓 Pinging...")
                end_time = asyncio.get_event_loop().time()
                
                latency = round((end_time - start_time) * 1000, 2)
                await msg.edit(content=f"🏓 Pong! Latency: {latency}ms")
            
            else:
                await message.channel.send("❓ Unknown command. Use `!ai help` for available commands.")
        
        except Exception as e:
            logger.error(f"Command error: {e}")
            await message.channel.send("⚠️ An error occurred processing your command.")
    
    async def start(self):
        """Start the Discord bot"""
        logger.info(f"🔍 DEBUG: Attempting to login with token: {self.token[:10]}...{self.token[-10:]}")
        logger.info(f"🔍 DEBUG: Token length: {len(self.token)}")
        logger.info(f"🔍 DEBUG: Token parts: {len(self.token.split('.'))}")
        
        try:
            await self.client.start(self.token)
        except discord.LoginFailure as e:
            logger.error(f"❌ Invalid Discord token - Discord API response: {e}")
            logger.error(f"🔍 DEBUG: Full token being used: {repr(self.token)}")
        except discord.HTTPException as e:
            logger.error(f"❌ Discord HTTP error: {e}")
            logger.error(f"🔍 DEBUG: Status code: {e.status}")
            logger.error(f"🔍 DEBUG: Response: {e.response}")
        except Exception as e:
            logger.error(f"❌ Bot startup error: {e}")
            logger.error(f"🔍 DEBUG: Exception type: {type(e)}")
            import traceback
            logger.error(f"🔍 DEBUG: Full traceback:\n{traceback.format_exc()}")

def start_simple_discord_bot():
    """Start the simple Discord bot"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN environment variable not set")
        return False
    
    bot = SimpleAICorporationBot(token)
    
    try:
        asyncio.run(bot.start())
        return True
    except KeyboardInterrupt:
        logger.info("👋 Discord bot shutdown")
        return True
    except Exception as e:
        logger.error(f"❌ Discord bot failed: {e}")
        return False

if __name__ == "__main__":
    start_simple_discord_bot()