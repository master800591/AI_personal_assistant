"""
Discord Bot Configuration for CrewAI Integration
Configuration management for enhanced Discord bot with voice and multi-agent capabilities
"""

discord_config = {
    # Discord Bot Settings
    'bot': {
        'command_prefix': '!ai',
        'description': 'AI Personal Assistant with CrewAI Multi-Agent System',
        'case_insensitive': True,
        'strip_after_prefix': True,
        'activity': {
            'type': 'watching',
            'name': 'AI Development with CrewAI'
        },
        'status': 'online'
    },
    
    # Intent Configuration
    'intents': {
        'messages': True,
        'message_content': True,
        'guilds': True,
        'guild_messages': True,
        'guild_reactions': True,
        'voice_states': True,
        'members': True,
        'dm_messages': True,
        'guild_voice_states': True
    },
    
    # Voice Channel Settings
    'voice': {
        'auto_disconnect': True,
        'auto_disconnect_timeout': 300,  # 5 minutes
        'max_connections': 5,
        'tts_enabled': True,
        'audio_quality': 'high',
        'bitrate': 64000
    },
    
    # Channel Management
    'channels': {
        'auto_create': True,
        'development_category': 'AI Development',
        'default_channels': [
            {
                'name': 'ai-general',
                'type': 'text',
                'topic': 'General AI development discussion'
            },
            {
                'name': 'ai-code-analysis',
                'type': 'text',
                'topic': 'Code analysis and improvement discussions'
            },
            {
                'name': 'ai-features',
                'type': 'text',
                'topic': 'Feature development and implementation'
            },
            {
                'name': 'ai-voice-meeting',
                'type': 'voice',
                'bitrate': 64000,
                'user_limit': 10
            },
            {
                'name': 'ai-development-voice',
                'type': 'voice',
                'bitrate': 96000,
                'user_limit': 5
            }
        ]
    },
    
    # CrewAI Integration Settings
    'crewai': {
        'enabled': True,
        'notification_channels': ['ai-general', 'ai-code-analysis'],
        'voice_announcements': True,
        'agent_mentions': True,
        'task_progress_updates': True,
        'completion_notifications': True,
        'error_notifications': True,
        'agent_avatars': {
            'code_analyst': '🔍',
            'feature_developer': '⚡',
            'founder_communicator': '👑'
        }
    },
    
    # Notification Settings
    'notifications': {
        'development_cycle_start': True,
        'analysis_complete': True,
        'feature_implemented': True,
        'error_occurred': True,
        'git_operations': True,
        'voice_activity': True,
        'member_events': True
    },
    
    # Command Categories
    'commands': {
        'development': {
            'enabled': True,
            'roles_required': ['AI Developer', 'Admin'],
            'commands': ['analyze', 'implement', 'deploy', 'status']
        },
        'voice': {
            'enabled': True,
            'roles_required': ['AI Developer', 'Member'],
            'commands': ['join', 'leave', 'speak', 'listen']
        },
        'knowledge': {
            'enabled': True,
            'roles_required': ['AI Developer', 'Member'],
            'commands': ['add', 'search', 'update', 'query']
        },
        'general': {
            'enabled': True,
            'roles_required': [],
            'commands': ['help', 'info', 'ping', 'version']
        }
    },
    
    # Permission Settings
    'permissions': {
        'admin_roles': ['Admin', 'AI Administrator'],
        'developer_roles': ['AI Developer', 'Developer'],
        'member_roles': ['Member', 'Contributor'],
        'restricted_commands': {
            'deploy': ['Admin', 'AI Administrator'],
            'shutdown': ['Admin'],
            'config': ['Admin', 'AI Administrator']
        }
    },
    
    # Moderation Settings
    'moderation': {
        'auto_moderation': True,
        'spam_protection': True,
        'rate_limiting': {
            'commands_per_minute': 10,
            'messages_per_minute': 20
        },
        'banned_words': [],
        'warning_system': True
    },
    
    # Embed Settings
    'embeds': {
        'colors': {
            'success': 0x00ff00,    # Green
            'error': 0xff0000,      # Red
            'warning': 0xffff00,    # Yellow
            'info': 0x0099ff,       # Blue
            'crewai': 0x9932cc,     # Purple
            'development': 0xff6600  # Orange
        },
        'footer': {
            'text': 'AI Personal Assistant with CrewAI',
            'icon_url': None
        },
        'author': {
            'name': 'AI Development Team',
            'icon_url': None
        }
    },
    
    # Logging Settings
    'logging': {
        'level': 'INFO',
        'file': 'logs/discord_bot.log',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'max_size': '10MB',
        'backup_count': 5,
        'log_commands': True,
        'log_errors': True,
        'log_voice_activity': True
    },
    
    # Performance Settings
    'performance': {
        'message_cache_size': 1000,
        'max_queue_size': 100,
        'event_processing_batch_size': 10,
        'connection_timeout': 30,
        'heartbeat_timeout': 60,
        'guild_subscriptions': True
    },
    
    # Development Settings
    'development': {
        'debug_mode': False,
        'test_mode': False,
        'mock_responses': False,
        'verbose_logging': False,
        'performance_monitoring': True
    }
}

# CrewAI Agent Configuration for Discord Integration
crewai_discord_config = {
    'agents': {
        'code_analyst': {
            'discord_persona': {
                'name': '🔍 Code Analyst',
                'avatar': '🔍',
                'color': 0x0099ff,
                'status': 'Analyzing code quality and security',
                'channels': ['ai-code-analysis', 'ai-general'],
                'voice_enabled': True,
                'notification_level': 'all'
            },
            'capabilities': [
                'code_analysis',
                'security_audit',
                'performance_review',
                'best_practices_check'
            ]
        },
        
        'feature_developer': {
            'discord_persona': {
                'name': '⚡ Feature Developer',
                'avatar': '⚡',
                'color': 0xff6600,
                'status': 'Implementing features and improvements',
                'channels': ['ai-features', 'ai-general'],
                'voice_enabled': True,
                'notification_level': 'important'
            },
            'capabilities': [
                'feature_implementation',
                'code_generation',
                'refactoring',
                'optimization'
            ]
        },
        
        'founder_communicator': {
            'discord_persona': {
                'name': '👑 Founder Communicator',
                'avatar': '👑',
                'color': 0x9932cc,
                'status': 'Managing AI corporation communications',
                'channels': ['ai-general'],
                'voice_enabled': True,
                'notification_level': 'critical'
            },
            'capabilities': [
                'stakeholder_communication',
                'progress_reporting',
                'decision_making',
                'strategic_planning'
            ]
        }
    },
    
    'workflows': {
        'development_cycle': {
            'trigger': 'scheduled',
            'frequency': '30m',
            'agents': ['code_analyst', 'feature_developer'],
            'notifications': True,
            'voice_announcements': False
        },
        
        'code_review': {
            'trigger': 'git_push',
            'agents': ['code_analyst'],
            'notifications': True,
            'voice_announcements': False
        },
        
        'feature_request': {
            'trigger': 'discord_command',
            'command': '!ai implement',
            'agents': ['feature_developer', 'code_analyst'],
            'notifications': True,
            'voice_announcements': True
        },
        
        'emergency_response': {
            'trigger': 'error_detected',
            'agents': ['code_analyst', 'founder_communicator'],
            'notifications': True,
            'voice_announcements': True,
            'priority': 'high'
        }
    }
}

# Knowledge Management Configuration
knowledge_discord_config = {
    'knowledge_base': {
        'auto_save': True,
        'backup_frequency': '1h',
        'search_enabled': True,
        'categories': [
            'discord_integration',
            'crewai_agents',
            'development_workflows',
            'troubleshooting',
            'best_practices',
            'api_documentation'
        ]
    },
    
    'discord_integration': {
        'auto_document': True,
        'command_documentation': True,
        'conversation_archiving': False,
        'knowledge_sharing': True,
        'search_commands': ['!ai search', '!ai knowledge', '!ai docs']
    }
}

# Complete configuration export
complete_discord_config = {
    **discord_config,
    'crewai_integration': crewai_discord_config,
    'knowledge_management': knowledge_discord_config
}