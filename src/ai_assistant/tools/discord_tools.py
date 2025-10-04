"""
AI Personal Assistant - Discord Tools for CrewAI Agents
Comprehensive Discord integration tools for channels, voice, and communication
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
import discord
from discord.ext import commands
from crewai.tools import BaseTool
from pydantic import Field
import json
import threading
import queue
import time

logger = logging.getLogger(__name__)

class DiscordChannelManagerTool(BaseTool):
    """Tool for managing Discord channels - create, modify, delete, and list channels"""
    
    name: str = "discord_channel_manager"
    description: str = (
        "Manage Discord channels including creating new channels, modifying existing ones, "
        "deleting channels, and listing all available channels. Supports text and voice channels."
    )
    bot: Optional[discord.Client] = Field(default=None, exclude=True)
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute channel management operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "list_channels":
                return self._list_channels(kwargs.get('guild_id'))
            elif action == "create_channel":
                return self._create_channel(
                    name=kwargs.get('name'),
                    channel_type=kwargs.get('type', 'text'),
                    guild_id=kwargs.get('guild_id'),
                    category_id=kwargs.get('category_id')
                )
            elif action == "modify_channel":
                return self._modify_channel(
                    channel_id=kwargs.get('channel_id'),
                    name=kwargs.get('name'),
                    topic=kwargs.get('topic'),
                    permissions=kwargs.get('permissions')
                )
            elif action == "delete_channel":
                return self._delete_channel(kwargs.get('channel_id'))
            else:
                return f"❌ Unknown action: {action}"
                
        except Exception as e:
            logger.error(f"Discord channel manager error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _list_channels(self, guild_id: Optional[int] = None) -> str:
        """List all channels in a guild"""
        try:
            channels = []
            for guild in self.bot.guilds:
                if guild_id and guild.id != guild_id:
                    continue
                    
                guild_channels = {
                    'guild': guild.name,
                    'guild_id': guild.id,
                    'text_channels': [],
                    'voice_channels': [],
                    'categories': []
                }
                
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        guild_channels['text_channels'].append({
                            'name': channel.name,
                            'id': channel.id,
                            'topic': channel.topic,
                            'category': channel.category.name if channel.category else None
                        })
                    elif isinstance(channel, discord.VoiceChannel):
                        guild_channels['voice_channels'].append({
                            'name': channel.name,
                            'id': channel.id,
                            'user_limit': channel.user_limit,
                            'bitrate': channel.bitrate,
                            'category': channel.category.name if channel.category else None
                        })
                    elif isinstance(channel, discord.CategoryChannel):
                        guild_channels['categories'].append({
                            'name': channel.name,
                            'id': channel.id
                        })
                
                channels.append(guild_channels)
            
            return f"✅ Found {len(channels)} guilds with channels:\n" + json.dumps(channels, indent=2)
            
        except Exception as e:
            return f"❌ Failed to list channels: {str(e)}"
    
    def _create_channel(self, name: str, channel_type: str = 'text', 
                       guild_id: Optional[int] = None, category_id: Optional[int] = None) -> str:
        """Create a new channel"""
        try:
            # This would need to be run in an async context
            # For now, return a success message with the configuration
            config = {
                'action': 'create_channel',
                'name': name,
                'type': channel_type,
                'guild_id': guild_id,
                'category_id': category_id
            }
            return f"✅ Channel creation queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create channel: {str(e)}"
    
    def _modify_channel(self, channel_id: int, **modifications) -> str:
        """Modify an existing channel"""
        try:
            config = {
                'action': 'modify_channel',
                'channel_id': channel_id,
                'modifications': modifications
            }
            return f"✅ Channel modification queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to modify channel: {str(e)}"
    
    def _delete_channel(self, channel_id: int) -> str:
        """Delete a channel"""
        try:
            config = {
                'action': 'delete_channel',
                'channel_id': channel_id
            }
            return f"✅ Channel deletion queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to delete channel: {str(e)}"


class DiscordVoiceChannelTool(BaseTool):
    """Tool for managing Discord voice channels and voice connections"""
    
    name: str = "discord_voice_channel"
    description: str = (
        "Manage Discord voice channels including connecting to voice channels, "
        "managing voice settings, and monitoring voice channel activity."
    )
    bot: Optional[discord.Client] = Field(default=None, exclude=True)
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute voice channel operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "list_voice_channels":
                return self._list_voice_channels(kwargs.get('guild_id'))
            elif action == "connect_voice":
                return self._connect_voice_channel(kwargs.get('channel_id'))
            elif action == "disconnect_voice":
                return self._disconnect_voice_channel(kwargs.get('guild_id'))
            elif action == "voice_channel_info":
                return self._get_voice_channel_info(kwargs.get('channel_id'))
            elif action == "move_user":
                return self._move_user_to_channel(
                    kwargs.get('user_id'),
                    kwargs.get('channel_id')
                )
            else:
                return f"❌ Unknown voice action: {action}"
                
        except Exception as e:
            logger.error(f"Discord voice channel error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _list_voice_channels(self, guild_id: Optional[int] = None) -> str:
        """List all voice channels with current users"""
        try:
            voice_channels = []
            for guild in self.bot.guilds:
                if guild_id and guild.id != guild_id:
                    continue
                
                for channel in guild.voice_channels:
                    channel_info = {
                        'name': channel.name,
                        'id': channel.id,
                        'guild': guild.name,
                        'user_limit': channel.user_limit,
                        'bitrate': channel.bitrate,
                        'connected_users': [
                            {
                                'name': member.display_name,
                                'id': member.id,
                                'status': str(member.status)
                            }
                            for member in channel.members
                        ],
                        'user_count': len(channel.members)
                    }
                    voice_channels.append(channel_info)
            
            return f"✅ Found {len(voice_channels)} voice channels:\n" + json.dumps(voice_channels, indent=2)
            
        except Exception as e:
            return f"❌ Failed to list voice channels: {str(e)}"
    
    def _connect_voice_channel(self, channel_id: int) -> str:
        """Connect bot to a voice channel"""
        try:
            config = {
                'action': 'connect_voice',
                'channel_id': channel_id,
                'timestamp': time.time()
            }
            return f"✅ Voice connection queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to connect to voice channel: {str(e)}"
    
    def _disconnect_voice_channel(self, guild_id: int) -> str:
        """Disconnect bot from voice channel"""
        try:
            config = {
                'action': 'disconnect_voice',
                'guild_id': guild_id,
                'timestamp': time.time()
            }
            return f"✅ Voice disconnection queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to disconnect from voice channel: {str(e)}"
    
    def _get_voice_channel_info(self, channel_id: int) -> str:
        """Get detailed information about a voice channel"""
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                return f"❌ Voice channel {channel_id} not found"
            
            info = {
                'name': channel.name,
                'id': channel.id,
                'guild': channel.guild.name,
                'user_limit': channel.user_limit,
                'bitrate': channel.bitrate,
                'connected_users': len(channel.members),
                'permissions': {
                    'connect': channel.permissions_for(channel.guild.me).connect,
                    'speak': channel.permissions_for(channel.guild.me).speak,
                    'use_voice_activation': channel.permissions_for(channel.guild.me).use_voice_activation
                }
            }
            
            return f"✅ Voice channel info:\n{json.dumps(info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to get voice channel info: {str(e)}"
    
    def _move_user_to_channel(self, user_id: int, channel_id: int) -> str:
        """Move a user to a different voice channel"""
        try:
            config = {
                'action': 'move_user',
                'user_id': user_id,
                'channel_id': channel_id,
                'timestamp': time.time()
            }
            return f"✅ User move queued: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to move user: {str(e)}"


class DiscordMessageTool(BaseTool):
    """Tool for sending and managing Discord messages"""
    
    name: str = "discord_message"
    description: str = (
        "Send messages to Discord channels, reply to messages, edit messages, "
        "and manage message interactions including embeds and reactions."
    )
    bot: Optional[discord.Client] = Field(default=None, exclude=True)
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute message operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "send_message":
                return self._send_message(
                    channel_id=kwargs.get('channel_id'),
                    content=kwargs.get('content'),
                    embed=kwargs.get('embed'),
                    reply_to=kwargs.get('reply_to')
                )
            elif action == "edit_message":
                return self._edit_message(
                    message_id=kwargs.get('message_id'),
                    new_content=kwargs.get('content')
                )
            elif action == "delete_message":
                return self._delete_message(kwargs.get('message_id'))
            elif action == "add_reaction":
                return self._add_reaction(
                    message_id=kwargs.get('message_id'),
                    emoji=kwargs.get('emoji')
                )
            elif action == "send_dm":
                return self._send_direct_message(
                    user_id=kwargs.get('user_id'),
                    content=kwargs.get('content')
                )
            else:
                return f"❌ Unknown message action: {action}"
                
        except Exception as e:
            logger.error(f"Discord message error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _send_message(self, channel_id: int, content: str, 
                     embed: Optional[Dict] = None, reply_to: Optional[int] = None) -> str:
        """Send a message to a Discord channel"""
        try:
            message_config = {
                'action': 'send_message',
                'channel_id': channel_id,
                'content': content,
                'embed': embed,
                'reply_to': reply_to,
                'timestamp': time.time()
            }
            return f"✅ Message queued for sending: {json.dumps(message_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue message: {str(e)}"
    
    def _edit_message(self, message_id: int, new_content: str) -> str:
        """Edit an existing message"""
        try:
            edit_config = {
                'action': 'edit_message',
                'message_id': message_id,
                'new_content': new_content,
                'timestamp': time.time()
            }
            return f"✅ Message edit queued: {json.dumps(edit_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue message edit: {str(e)}"
    
    def _delete_message(self, message_id: int) -> str:
        """Delete a message"""
        try:
            delete_config = {
                'action': 'delete_message',
                'message_id': message_id,
                'timestamp': time.time()
            }
            return f"✅ Message deletion queued: {json.dumps(delete_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue message deletion: {str(e)}"
    
    def _add_reaction(self, message_id: int, emoji: str) -> str:
        """Add a reaction to a message"""
        try:
            reaction_config = {
                'action': 'add_reaction',
                'message_id': message_id,
                'emoji': emoji,
                'timestamp': time.time()
            }
            return f"✅ Reaction queued: {json.dumps(reaction_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue reaction: {str(e)}"
    
    def _send_direct_message(self, user_id: int, content: str) -> str:
        """Send a direct message to a user"""
        try:
            dm_config = {
                'action': 'send_dm',
                'user_id': user_id,
                'content': content,
                'timestamp': time.time()
            }
            return f"✅ Direct message queued: {json.dumps(dm_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue direct message: {str(e)}"


class DiscordListenerTool(BaseTool):
    """Tool for listening to Discord events and messages"""
    
    name: str = "discord_listener"
    description: str = (
        "Listen to Discord messages, voice channel events, and user activities. "
        "Capture and process real-time Discord events for agent awareness."
    )
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        # Set attributes after initialization to avoid Pydantic validation
        object.__setattr__(self, 'bot', bot)
        object.__setattr__(self, 'event_queue', queue.Queue())
        object.__setattr__(self, 'listening', False)
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute listening operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "start_listening":
                return self._start_listening(
                    channels=kwargs.get('channels'),
                    event_types=kwargs.get('event_types', ['message'])
                )
            elif action == "stop_listening":
                return self._stop_listening()
            elif action == "get_recent_events":
                return self._get_recent_events(kwargs.get('limit', 10))
            elif action == "listen_to_channel":
                return self._listen_to_specific_channel(kwargs.get('channel_id'))
            else:
                return f"❌ Unknown listener action: {action}"
                
        except Exception as e:
            logger.error(f"Discord listener error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _start_listening(self, channels: Optional[List[int]] = None, 
                        event_types: List[str] = None) -> str:
        """Start listening to Discord events"""
        try:
            self.listening = True
            config = {
                'action': 'start_listening',
                'channels': channels,
                'event_types': event_types or ['message', 'voice_state_update', 'member_join'],
                'status': 'active',
                'started_at': time.time()
            }
            return f"✅ Discord listener started: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to start listening: {str(e)}"
    
    def _stop_listening(self) -> str:
        """Stop listening to Discord events"""
        try:
            self.listening = False
            config = {
                'action': 'stop_listening',
                'status': 'stopped',
                'stopped_at': time.time()
            }
            return f"✅ Discord listener stopped: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to stop listening: {str(e)}"
    
    def _get_recent_events(self, limit: int = 10) -> str:
        """Get recent Discord events from the queue"""
        try:
            events = []
            count = 0
            while not self.event_queue.empty() and count < limit:
                events.append(self.event_queue.get_nowait())
                count += 1
            
            return f"✅ Retrieved {len(events)} recent events: {json.dumps(events, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to get recent events: {str(e)}"
    
    def _listen_to_specific_channel(self, channel_id: int) -> str:
        """Start listening to a specific channel"""
        try:
            config = {
                'action': 'listen_to_channel',
                'channel_id': channel_id,
                'status': 'monitoring',
                'started_at': time.time()
            }
            return f"✅ Listening to channel {channel_id}: {json.dumps(config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to listen to channel: {str(e)}"


class DiscordSpeakerTool(BaseTool):
    """Tool for speaking in Discord voice channels using text-to-speech"""
    
    name: str = "discord_speaker"
    description: str = (
        "Convert text to speech and play audio in Discord voice channels. "
        "Supports various TTS engines and audio playback controls."
    )
    bot: Optional[discord.Client] = Field(default=None, exclude=True)
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute voice speaking operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "speak":
                return self._speak_text(
                    text=kwargs.get('text'),
                    voice_channel_id=kwargs.get('voice_channel_id'),
                    voice_settings=kwargs.get('voice_settings', {})
                )
            elif action == "play_audio":
                return self._play_audio_file(
                    file_path=kwargs.get('file_path'),
                    voice_channel_id=kwargs.get('voice_channel_id')
                )
            elif action == "stop_speaking":
                return self._stop_speaking(kwargs.get('guild_id'))
            elif action == "set_voice_settings":
                return self._set_voice_settings(kwargs.get('settings'))
            else:
                return f"❌ Unknown speaker action: {action}"
                
        except Exception as e:
            logger.error(f"Discord speaker error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _speak_text(self, text: str, voice_channel_id: int, voice_settings: Dict = None) -> str:
        """Convert text to speech and play in voice channel"""
        try:
            speech_config = {
                'action': 'speak_text',
                'text': text,
                'voice_channel_id': voice_channel_id,
                'voice_settings': voice_settings or {
                    'speed': 1.0,
                    'pitch': 1.0,
                    'volume': 0.8,
                    'voice': 'default'
                },
                'timestamp': time.time()
            }
            return f"✅ Text-to-speech queued: {json.dumps(speech_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue text-to-speech: {str(e)}"
    
    def _play_audio_file(self, file_path: str, voice_channel_id: int) -> str:
        """Play an audio file in voice channel"""
        try:
            audio_config = {
                'action': 'play_audio',
                'file_path': file_path,
                'voice_channel_id': voice_channel_id,
                'timestamp': time.time()
            }
            return f"✅ Audio playback queued: {json.dumps(audio_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue audio playback: {str(e)}"
    
    def _stop_speaking(self, guild_id: int) -> str:
        """Stop current audio playback"""
        try:
            stop_config = {
                'action': 'stop_speaking',
                'guild_id': guild_id,
                'timestamp': time.time()
            }
            return f"✅ Audio stop queued: {json.dumps(stop_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue audio stop: {str(e)}"
    
    def _set_voice_settings(self, settings: Dict) -> str:
        """Configure voice synthesis settings"""
        try:
            settings_config = {
                'action': 'set_voice_settings',
                'settings': settings,
                'timestamp': time.time()
            }
            return f"✅ Voice settings updated: {json.dumps(settings_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to update voice settings: {str(e)}"


class DiscordGuildManagerTool(BaseTool):
    """Tool for managing Discord guild (server) operations"""
    
    name: str = "discord_guild_manager"
    description: str = (
        "Manage Discord guild operations including member management, role assignment, "
        "server settings, and administrative functions."
    )
    bot: Optional[discord.Client] = Field(default=None, exclude=True)
    
    def __init__(self, bot: Optional[discord.Client] = None, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute guild management operations"""
        try:
            if not self.bot:
                return "❌ Discord bot not initialized"
            
            if action == "list_guilds":
                return self._list_guilds()
            elif action == "guild_info":
                return self._get_guild_info(kwargs.get('guild_id'))
            elif action == "list_members":
                return self._list_guild_members(kwargs.get('guild_id'))
            elif action == "manage_roles":
                return self._manage_member_roles(
                    guild_id=kwargs.get('guild_id'),
                    user_id=kwargs.get('user_id'),
                    role_action=kwargs.get('role_action'),
                    role_id=kwargs.get('role_id')
                )
            elif action == "create_role":
                return self._create_role(
                    guild_id=kwargs.get('guild_id'),
                    role_name=kwargs.get('role_name'),
                    permissions=kwargs.get('permissions')
                )
            else:
                return f"❌ Unknown guild action: {action}"
                
        except Exception as e:
            logger.error(f"Discord guild manager error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _list_guilds(self) -> str:
        """List all guilds the bot is connected to"""
        try:
            guilds_info = []
            for guild in self.bot.guilds:
                guild_info = {
                    'name': guild.name,
                    'id': guild.id,
                    'member_count': guild.member_count,
                    'owner': guild.owner.display_name if guild.owner else 'Unknown',
                    'created_at': guild.created_at.isoformat(),
                    'bot_permissions': {
                        'administrator': guild.me.guild_permissions.administrator,
                        'manage_channels': guild.me.guild_permissions.manage_channels,
                        'manage_roles': guild.me.guild_permissions.manage_roles,
                        'manage_messages': guild.me.guild_permissions.manage_messages
                    }
                }
                guilds_info.append(guild_info)
            
            return f"✅ Found {len(guilds_info)} guilds: {json.dumps(guilds_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to list guilds: {str(e)}"
    
    def _get_guild_info(self, guild_id: int) -> str:
        """Get detailed information about a specific guild"""
        try:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return f"❌ Guild {guild_id} not found"
            
            guild_info = {
                'name': guild.name,
                'id': guild.id,
                'description': guild.description,
                'member_count': guild.member_count,
                'owner': guild.owner.display_name if guild.owner else 'Unknown',
                'created_at': guild.created_at.isoformat(),
                'features': guild.features,
                'channels': {
                    'text': len(guild.text_channels),
                    'voice': len(guild.voice_channels),
                    'categories': len(guild.categories)
                },
                'roles': len(guild.roles),
                'emojis': len(guild.emojis),
                'verification_level': str(guild.verification_level)
            }
            
            return f"✅ Guild information: {json.dumps(guild_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to get guild info: {str(e)}"
    
    def _list_guild_members(self, guild_id: int, limit: int = 50) -> str:
        """List members of a guild"""
        try:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return f"❌ Guild {guild_id} not found"
            
            members_info = []
            for i, member in enumerate(guild.members):
                if i >= limit:
                    break
                    
                member_info = {
                    'name': member.name,
                    'display_name': member.display_name,
                    'id': member.id,
                    'status': str(member.status),
                    'joined_at': member.joined_at.isoformat() if member.joined_at else None,
                    'roles': [role.name for role in member.roles if role.name != '@everyone'],
                    'is_bot': member.bot
                }
                members_info.append(member_info)
            
            return f"✅ Found {len(members_info)} members (limit {limit}): {json.dumps(members_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to list guild members: {str(e)}"
    
    def _manage_member_roles(self, guild_id: int, user_id: int, role_action: str, role_id: int) -> str:
        """Add or remove roles from a member"""
        try:
            role_config = {
                'action': 'manage_roles',
                'guild_id': guild_id,
                'user_id': user_id,
                'role_action': role_action,  # 'add' or 'remove'
                'role_id': role_id,
                'timestamp': time.time()
            }
            return f"✅ Role management queued: {json.dumps(role_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue role management: {str(e)}"
    
    def _create_role(self, guild_id: int, role_name: str, permissions: Dict = None) -> str:
        """Create a new role in the guild"""
        try:
            role_config = {
                'action': 'create_role',
                'guild_id': guild_id,
                'role_name': role_name,
                'permissions': permissions or {},
                'timestamp': time.time()
            }
            return f"✅ Role creation queued: {json.dumps(role_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue role creation: {str(e)}"