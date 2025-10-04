"""
AI Personal Assistant - CrewAI Tools Package
Enhanced tools for Discord integration, voice channels, and knowledge management
"""

from .discord_tools import (
    DiscordChannelManagerTool,
    DiscordVoiceChannelTool,
    DiscordMessageTool,
    DiscordListenerTool,
    DiscordSpeakerTool,
    DiscordGuildManagerTool
)

from .knowledge_tools import (
    KnowledgeManagerTool,
    KnowledgeQueryTool,
    KnowledgeAddTool,
    KnowledgeUpdateTool,
    DocumentProcessorTool
)

from .ai_development_tools import (
    CodeAnalysisTool,
    FeatureImplementationTool,
    GitHubIntegrationTool,
    FileSystemTool,
    OllamaIntegrationTool
)

__all__ = [
    # Discord Tools
    "DiscordChannelManagerTool",
    "DiscordVoiceChannelTool", 
    "DiscordMessageTool",
    "DiscordListenerTool",
    "DiscordSpeakerTool",
    "DiscordGuildManagerTool",
    
    # Knowledge Management Tools
    "KnowledgeManagerTool",
    "KnowledgeQueryTool",
    "KnowledgeAddTool",
    "KnowledgeUpdateTool",
    "DocumentProcessorTool",
    
    # AI Development Tools
    "CodeAnalysisTool",
    "FeatureImplementationTool",
    "GitHubIntegrationTool",
    "FileSystemTool",
    "OllamaIntegrationTool"
]