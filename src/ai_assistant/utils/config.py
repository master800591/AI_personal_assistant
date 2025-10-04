#!/usr/bin/env python3
"""
Configuration Management
Handles all configuration loading and management
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv

class Config:
    """Configuration manager for AI Assistant"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration"""
        self.config_data: Dict[str, Any] = {}
        
        # Load environment variables first
        self._load_env()
        
        # Load configuration file if provided
        if config_path:
            self._load_config_file(config_path)
        
        # Apply defaults
        self._apply_defaults()
    
    def _load_env(self):
        """Load environment variables"""
        # Load .env file if it exists
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(env_path)
        
        # Map environment variables to config
        env_mappings = {
            'DISCORD_BOT_TOKEN': 'discord.bot_token',
            'GITHUB_TOKEN': 'github.token',
            'AI_CORP_FOUNDER': 'ai_corp.founder',
            'AI_CORP_MISSION': 'ai_corp.mission',
            'OLLAMA_HOST': 'ollama.host',
            'LOG_LEVEL': 'logging.level',
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self.set(config_key, value)
    
    def _load_config_file(self, config_path: str):
        """Load configuration from file"""
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif path.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {path.suffix}")
            
            self._merge_config(data)
            
        except Exception as e:
            raise ValueError(f"Failed to load config file {config_path}: {e}")
    
    def _apply_defaults(self):
        """Apply default configuration values"""
        defaults = {
            'logging': {
                'level': 'INFO',
                'file': 'logs/ai_assistant.log',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'ollama': {
                'host': 'localhost:11434',
                'default_model': 'deepseek-r1',
                'timeout': 30
            },
            'autonomous': {
                'enabled': True,
                'cycle_interval': 600,  # 10 minutes
                'max_files_per_cycle': 5,
                'backup_before_changes': True
            },
            'discord': {
                'enabled': False,
                'command_prefix': '!ai',
                'admin_roles': ['AI Developer', 'Admin']
            },
            'github': {
                'auto_commit': True,
                'commit_message_prefix': '[AI-DEV]',
                'default_branch': 'main'
            },
            'ai_corp': {
                'founder': 'Steve Cornell',
                'mission': 'Autonomous AI Development',
                'version': '1.0.0'
            }
        }
        
        for key, value in defaults.items():
            if key not in self.config_data:
                self.config_data[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self.config_data[key]:
                        self.config_data[key][sub_key] = sub_value
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration with existing"""
        def merge_dict(target: Dict, source: Dict):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_dict(target[key], value)
                else:
                    target[key] = value
        
        merge_dict(self.config_data, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        target = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        # Set the final value
        target[keys[-1]] = value
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists"""
        return self.get(key) is not None
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config_data.copy()
    
    def save(self, path: str, format: str = 'yaml') -> None:
        """Save configuration to file"""
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if format.lower() == 'yaml':
                yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
            elif format.lower() == 'json':
                json.dump(self.config_data, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
    
    def __str__(self) -> str:
        """String representation of config"""
        return f"Config({len(self.config_data)} sections)"
    
    def __repr__(self) -> str:
        """Detailed representation of config"""
        return f"Config(sections={list(self.config_data.keys())})"