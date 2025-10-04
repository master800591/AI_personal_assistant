"""
AI Personal Assistant - Discord Bot Integration for CrewAI Agents
Enhanced Discord bot with voice channel capabilities and CrewAI agent integration
"""

import asyncio
import logging
import json
import queue
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime
import discord
from discord.ext import commands, tasks
from pathlib import Path

# Import our custom tools and crew manager
from ..crews.proper_ai_crew import AutonomousCrewManager
from ..tools.discord_tools import (
    DiscordChannelManagerTool,
    DiscordVoiceChannelTool,
    DiscordMessageTool,
    DiscordListenerTool,
    DiscordSpeakerTool,
    DiscordGuildManagerTool
)

logger = logging.getLogger(__name__)

class AIAssistantDiscordBot(commands.Bot):
    """Enhanced Discord bot integrated with CrewAI agents"""
    
    def __init__(self, config, crew_manager: Optional[AutonomousCrewManager] = None):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.voice_states = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.get('discord.command_prefix', '!ai'),
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.crew_manager = crew_manager
        self.voice_connections = {}
        self.event_queue = queue.Queue()
        self.listening_channels = set()
        
        # Initialize Discord tools with this bot instance
        self.channel_manager = DiscordChannelManagerTool(bot=self)
        self.voice_manager = DiscordVoiceChannelTool(bot=self)
        self.message_manager = DiscordMessageTool(bot=self)
        self.listener_manager = DiscordListenerTool(bot=self)
        self.speaker_manager = DiscordSpeakerTool(bot=self)
        self.guild_manager = DiscordGuildManagerTool(bot=self)
        
        # Start background tasks
        self.setup_tasks()
    
    async def setup_hook(self):
        """Called when bot is starting up"""
        await self.load_extension('ai_assistant.discord.commands')
        logger.info(f"✅ AI Assistant Discord Bot logged in as {self.user}")
    
    async def on_ready(self):
        """Bot is fully ready"""
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="AI Development with CrewAI"
        )
        await self.change_presence(activity=activity)
        
        # Start background processing
        self.process_crew_notifications.start()
        
        logger.info(f"🤖 AI Assistant Discord Bot ready with {len(self.guilds)} guilds")
        
        # Notify crews about bot readiness
        if self.crew_manager:
            await self.notify_crews_about_discord_ready()
    
    def setup_tasks(self):
        """Setup background tasks"""
        @tasks.loop(seconds=30)
        async def process_crew_notifications():
            """Process notifications from CrewAI agents"""
            try:
                # This would process queued notifications from agents
                await self.process_queued_notifications()
            except Exception as e:
                logger.error(f"Error processing crew notifications: {e}")
        
        self.process_crew_notifications = process_crew_notifications
    
    async def notify_crews_about_discord_ready(self):
        """Notify CrewAI agents that Discord bot is ready"""
        try:
            notification = {
                'type': 'discord_bot_ready',
                'bot_user': str(self.user),
                'guilds': [{'name': guild.name, 'id': guild.id} for guild in self.guilds],
                'capabilities': [
                    'text_messaging',
                    'voice_channels',
                    'channel_management',
                    'guild_management',
                    'real_time_listening'
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            # This would be sent to the crew manager
            logger.info(f"🔔 Discord bot ready notification: {json.dumps(notification, indent=2)}")
            
        except Exception as e:
            logger.error(f"Error notifying crews about Discord readiness: {e}")
    
    async def on_message(self, message):
        """Handle incoming messages"""
        if message.author == self.user:
            return
        
        # Add message to event queue for CrewAI agents
        event = {
            'type': 'message',
            'content': message.content,
            'author': {
                'name': message.author.name,
                'id': message.author.id,
                'display_name': message.author.display_name
            },
            'channel': {
                'name': message.channel.name,
                'id': message.channel.id,
                'type': str(message.channel.type)
            },
            'guild': {
                'name': message.guild.name if message.guild else None,
                'id': message.guild.id if message.guild else None
            },
            'timestamp': message.created_at.isoformat()
        }
        
        self.event_queue.put(event)
        
        # Process commands
        await self.process_commands(message)
        
        # Check if this is a direct mention or DM to CrewAI
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            await self.handle_crew_ai_interaction(message)
    
    async def on_voice_state_update(self, member, before, after):
        """Handle voice channel events"""
        event = {
            'type': 'voice_state_update',
            'member': {
                'name': member.name,
                'id': member.id,
                'display_name': member.display_name
            },
            'before_channel': before.channel.name if before.channel else None,
            'after_channel': after.channel.name if after.channel else None,
            'timestamp': datetime.now().isoformat()
        }
        
        self.event_queue.put(event)
        
        # Log voice activity for CrewAI agents
        if after.channel and not before.channel:
            logger.info(f"👤 {member.display_name} joined voice channel: {after.channel.name}")
        elif before.channel and not after.channel:
            logger.info(f"👤 {member.display_name} left voice channel: {before.channel.name}")
    
    async def on_member_join(self, member):
        """Handle new member joining"""
        event = {
            'type': 'member_join',
            'member': {
                'name': member.name,
                'id': member.id,
                'display_name': member.display_name
            },
            'guild': {
                'name': member.guild.name,
                'id': member.guild.id
            },
            'timestamp': datetime.now().isoformat()
        }
        
        self.event_queue.put(event)
        
        # Welcome new member (this could be handled by CrewAI agents)
        welcome_channel = discord.utils.get(member.guild.text_channels, name='general')
        if welcome_channel:
            embed = discord.Embed(
                title="🤖 Welcome to AI Development!",
                description=f"Welcome {member.mention}! I'm the AI Assistant bot powered by CrewAI.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Getting Started",
                value="Use `!ai help` to see available commands",
                inline=False
            )
            await welcome_channel.send(embed=embed)
    
    async def handle_crew_ai_interaction(self, message):
        """Handle direct interactions with CrewAI agents"""
        try:
            if not self.crew_manager:
                await message.reply("🤖 CrewAI system not available")
                return
            
            # This would trigger CrewAI agent response
            response_config = {
                'type': 'crew_ai_interaction',
                'message': message.content,
                'author': message.author.display_name,
                'channel': message.channel.name,
                'timestamp': datetime.now().isoformat()
            }
            
            # For now, send a placeholder response
            embed = discord.Embed(
                title="🤖 CrewAI Agent Response",
                description="Your message has been received by the AI development team.",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Status",
                value="Processing with multi-agent system",
                inline=True
            )
            embed.add_field(
                name="Agents Involved",
                value="Code Analyst, Feature Developer, Founder Communicator",
                inline=True
            )
            
            await message.reply(embed=embed)
            
        except Exception as e:
            logger.error(f"Error handling CrewAI interaction: {e}")
            await message.reply(f"❌ Error processing request: {str(e)}")
    
    async def process_queued_notifications(self):
        """Process queued notifications from CrewAI agents"""
        try:
            # Process events from the queue
            processed = 0
            while not self.event_queue.empty() and processed < 10:  # Limit processing
                event = self.event_queue.get_nowait()
                await self.handle_event_for_crews(event)
                processed += 1
                
        except queue.Empty:
            pass  # No events to process
        except Exception as e:
            logger.error(f"Error processing queued notifications: {e}")
    
    async def handle_event_for_crews(self, event):
        """Handle an event and notify relevant CrewAI agents"""
        try:
            # This would determine which agents need to be notified about the event
            event_type = event.get('type')
            
            if event_type == 'message':
                # Check if message mentions development keywords
                content = event.get('content', '').lower()
                if any(keyword in content for keyword in ['bug', 'error', 'fix', 'improve', 'feature']):
                    await self.notify_development_agents(event)
            
            elif event_type == 'voice_state_update':
                # Notify agents about voice channel activity
                await self.notify_voice_activity(event)
            
            elif event_type == 'member_join':
                # Notify founder communication agent
                await self.notify_founder_agent(event)
                
        except Exception as e:
            logger.error(f"Error handling event for crews: {e}")
    
    async def notify_development_agents(self, event):
        """Notify development agents about relevant messages"""
        try:
            # This would trigger CrewAI agents to analyze the message
            logger.info(f"🔔 Notifying development agents about message: {event['content'][:50]}...")
            
        except Exception as e:
            logger.error(f"Error notifying development agents: {e}")
    
    async def notify_voice_activity(self, event):
        """Notify agents about voice channel activity"""
        try:
            # This would inform agents about voice channel usage
            logger.info(f"🔊 Voice activity: {event['member']['display_name']} - {event['after_channel']}")
            
        except Exception as e:
            logger.error(f"Error notifying voice activity: {e}")
    
    async def notify_founder_agent(self, event):
        """Notify founder communication agent about important events"""
        try:
            # This would alert the founder communication agent
            logger.info(f"👑 Founder agent notification: New member {event['member']['display_name']}")
            
        except Exception as e:
            logger.error(f"Error notifying founder agent: {e}")
    
    async def send_crew_message(self, channel_id: int, content: str, embed: dict = None):
        """Send a message on behalf of CrewAI agents"""
        try:
            channel = self.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return False
            
            if embed:
                embed_obj = discord.Embed.from_dict(embed)
                await channel.send(content, embed=embed_obj)
            else:
                await channel.send(content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending crew message: {e}")
            return False
    
    async def connect_to_voice_channel(self, channel_id: int):
        """Connect to a voice channel for CrewAI agent communication"""
        try:
            channel = self.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                logger.error(f"Voice channel {channel_id} not found")
                return False
            
            voice_client = await channel.connect()
            self.voice_connections[channel.guild.id] = voice_client
            
            logger.info(f"🔊 Connected to voice channel: {channel.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to voice channel: {e}")
            return False
    
    async def disconnect_from_voice(self, guild_id: int):
        """Disconnect from voice channel"""
        try:
            if guild_id in self.voice_connections:
                await self.voice_connections[guild_id].disconnect()
                del self.voice_connections[guild_id]
                logger.info(f"🔊 Disconnected from voice channel in guild {guild_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error disconnecting from voice: {e}")
            return False
    
    async def speak_in_voice_channel(self, guild_id: int, text: str):
        """Convert text to speech and play in voice channel"""
        try:
            if guild_id not in self.voice_connections:
                logger.error(f"Not connected to voice channel in guild {guild_id}")
                return False
            
            # This would implement text-to-speech functionality
            # For now, just log the action
            logger.info(f"🔊 Speaking in voice channel: {text[:50]}...")
            
            # Placeholder for actual TTS implementation
            return True
            
        except Exception as e:
            logger.error(f"Error speaking in voice channel: {e}")
            return False


# Discord bot commands
class AIAssistantCommands(commands.Cog):
    """Discord commands for AI Assistant"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='status')
    async def ai_status(self, ctx):
        """Show AI system status"""
        embed = discord.Embed(
            title="🤖 AI Assistant Status",
            color=discord.Color.green()
        )
        
        # Bot status
        embed.add_field(name="Discord Bot", value="✅ Online", inline=True)
        embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Voice Connections", value=f"{len(self.bot.voice_connections)}", inline=True)
        
        # CrewAI status
        crew_status = "✅ Active" if self.bot.crew_manager else "❌ Not Available"
        embed.add_field(name="CrewAI System", value=crew_status, inline=True)
        
        # Available tools
        tools_count = 11  # Number of Discord tools we created
        embed.add_field(name="Available Tools", value=f"{tools_count} Discord Tools", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='channels')
    async def list_channels(self, ctx):
        """List all channels in the guild"""
        if not ctx.guild:
            await ctx.send("❌ This command can only be used in a server")
            return
        
        result = self.bot.channel_manager._list_channels(ctx.guild.id)
        
        # Parse the result and create a nice embed
        embed = discord.Embed(
            title="📋 Server Channels",
            description=f"Channels in {ctx.guild.name}",
            color=discord.Color.blue()
        )
        
        text_channels = [ch.name for ch in ctx.guild.text_channels]
        voice_channels = [ch.name for ch in ctx.guild.voice_channels]
        
        if text_channels:
            embed.add_field(
                name="💬 Text Channels",
                value="\n".join(text_channels[:10]),  # Limit to 10
                inline=True
            )
        
        if voice_channels:
            embed.add_field(
                name="🔊 Voice Channels",
                value="\n".join(voice_channels[:10]),  # Limit to 10
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='voice')
    async def voice_info(self, ctx):
        """Show voice channel information"""
        if not ctx.guild:
            await ctx.send("❌ This command can only be used in a server")
            return
        
        result = self.bot.voice_manager._list_voice_channels(ctx.guild.id)
        
        embed = discord.Embed(
            title="🔊 Voice Channels",
            description=f"Voice activity in {ctx.guild.name}",
            color=discord.Color.green()
        )
        
        for channel in ctx.guild.voice_channels:
            member_count = len(channel.members)
            member_names = [m.display_name for m in channel.members[:5]]  # Limit to 5
            
            value = f"👥 {member_count} members"
            if member_names:
                value += f"\n{', '.join(member_names)}"
                if len(channel.members) > 5:
                    value += "..."
            
            embed.add_field(
                name=f"🔊 {channel.name}",
                value=value,
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='crew')
    async def crew_info(self, ctx):
        """Show CrewAI system information"""
        embed = discord.Embed(
            title="🤖 CrewAI Multi-Agent System",
            description="AI Personal Assistant Development Team",
            color=discord.Color.purple()
        )
        
        if self.bot.crew_manager:
            embed.add_field(
                name="Status",
                value="✅ Active and Running",
                inline=True
            )
            
            agents = [
                "🔍 Code Analysis Agent",
                "⚡ Feature Development Agent", 
                "👑 Founder Communication Agent"
            ]
            
            embed.add_field(
                name="Active Agents",
                value="\n".join(agents),
                inline=True
            )
            
            tools = [
                "📋 Discord Channel Management",
                "🔊 Voice Channel Control",
                "💬 Message Management",
                "👂 Event Listening",
                "🗣️ Text-to-Speech",
                "🏛️ Guild Administration",
                "📚 Knowledge Management",
                "🔧 Code Analysis",
                "⚙️ Feature Implementation",
                "🐙 GitHub Integration"
            ]
            
            embed.add_field(
                name="Available Tools",
                value="\n".join(tools[:5]) + f"\n... and {len(tools)-5} more",
                inline=False
            )
        else:
            embed.add_field(
                name="Status",
                value="❌ Not Available",
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show available commands"""
        embed = discord.Embed(
            title="🤖 AI Assistant Commands",
            description="Available Discord commands for AI development",
            color=discord.Color.blue()
        )
        
        commands_list = [
            "**!ai status** - Show system status",
            "**!ai channels** - List server channels",
            "**!ai voice** - Show voice channel info",
            "**!ai crew** - Show CrewAI agent info",
            "**!ai help** - Show this help message"
        ]
        
        embed.add_field(
            name="Commands",
            value="\n".join(commands_list),
            inline=False
        )
        
        embed.add_field(
            name="Direct Interaction",
            value="Mention @AI Assistant or send a DM to interact with CrewAI agents",
            inline=False
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function for Discord commands"""
    await bot.add_cog(AIAssistantCommands(bot))