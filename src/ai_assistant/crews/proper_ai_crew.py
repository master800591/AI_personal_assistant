#!/usr/bin/env python3
"""
AI Personal Assistant - Proper CrewAI Implementation Following GitHub Copilot Instructions
Founder: Steve Cornell (master80059)
Enhanced with Discord Tools and Knowledge Management
"""

import logging
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from crewai import Agent, Crew, Task, Process
from crewai_tools import DirectoryReadTool, FileReadTool, CodeInterpreterTool
from crewai import LLM

# Import our custom tools
from ..tools.discord_tools import (
    DiscordChannelManagerTool,
    DiscordVoiceChannelTool,
    DiscordMessageTool,
    DiscordListenerTool,
    DiscordSpeakerTool,
    DiscordGuildManagerTool
)
from ..tools.knowledge_tools import (
    KnowledgeManagerTool,
    KnowledgeQueryTool,
    KnowledgeAddTool,
    KnowledgeUpdateTool,
    DocumentProcessorTool
)
from ..tools.ai_development_tools import (
    CodeAnalysisTool,
    FeatureImplementationTool,
    GitHubIntegrationTool,
    FileSystemTool,
    OllamaIntegrationTool
)

class AIAssistantCrew:
    """AI Personal Assistant development crew following proper CrewAI patterns"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger(__name__)
        
        # Load configurations
        self.agents_config = self._load_yaml("agents.yaml")
        self.tasks_config = self._load_yaml("tasks.yaml")
        
        # Initialize LLM for local Ollama
        self.llm = LLM(
            model="ollama/deepseek-r1",
            base_url="http://localhost:11434",
            temperature=0.1
        )
        
        self.logger.info("🤖 AI Assistant CrewAI system initialized")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        file_path = self.config_dir / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load {filename}: {e}")
            return {}
    
    def code_analyst(self) -> Agent:
        """Senior Code Quality Analyst with enhanced Discord and Knowledge tools"""
        config = self.agents_config.get('code_analysis_agent', {})
        
        # Create Discord tools (these would be configured with actual bot instances)
        discord_channel_tool = DiscordChannelManagerTool()
        discord_message_tool = DiscordMessageTool()
        discord_listener_tool = DiscordListenerTool()
        
        # Create Knowledge tools
        knowledge_manager = KnowledgeManagerTool()
        knowledge_query = KnowledgeQueryTool()
        knowledge_add = KnowledgeAddTool()
        
        # Create AI development tools
        code_analysis_tool = CodeAnalysisTool()
        file_system_tool = FileSystemTool()
        ollama_tool = OllamaIntegrationTool()
        github_tool = GitHubIntegrationTool()
        
        return Agent(
            role=config.get('role', 'Senior Code Analysis Expert with Discord Integration'),
            goal=config.get('goal', 
                'Analyze code for quality and improvements while managing Discord '
                'communications and maintaining comprehensive knowledge bases'
            ),
            backstory=config.get('backstory', 
                'Expert Python developer with advanced Discord management skills '
                'and comprehensive knowledge base maintenance capabilities'
            ),
            tools=[
                # Standard CrewAI tools
                DirectoryReadTool(directory='src/'),
                FileReadTool(),
                CodeInterpreterTool(),
                # Discord communication tools
                discord_channel_tool,
                discord_message_tool,
                discord_listener_tool,
                # Knowledge management tools
                knowledge_manager,
                knowledge_query,
                knowledge_add,
                # AI development tools
                code_analysis_tool,
                file_system_tool,
                ollama_tool,
                github_tool
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )
    
    def feature_developer(self) -> Agent:
        """AI Feature Developer with Discord and Voice capabilities"""
        config = self.agents_config.get('feature_development_agent', {})
        
        # Create Discord tools with voice channel capabilities
        discord_voice_tool = DiscordVoiceChannelTool()
        discord_speaker_tool = DiscordSpeakerTool()
        discord_guild_tool = DiscordGuildManagerTool()
        
        # Create Knowledge and development tools
        knowledge_update = KnowledgeUpdateTool()
        doc_processor = DocumentProcessorTool()
        feature_implementation = FeatureImplementationTool()
        file_system_tool = FileSystemTool()
        
        return Agent(
            role=config.get('role', 'AI Feature Developer with Discord Voice Integration'),
            goal=config.get('goal', 
                'Implement features and improvements while managing Discord voice '
                'channels and providing spoken updates to the development team'
            ),
            backstory=config.get('backstory', 
                'Skilled developer creating working code with advanced Discord voice '
                'communication capabilities and document processing expertise'
            ),
            tools=[
                # Standard CrewAI tools
                FileReadTool(),
                CodeInterpreterTool(),
                DirectoryReadTool(directory='src/'),
                # Discord voice and management tools
                discord_voice_tool,
                discord_speaker_tool,
                discord_guild_tool,
                # Knowledge and development tools
                knowledge_update,
                doc_processor,
                feature_implementation,
                file_system_tool
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', True)
        )
    
    def founder_communicator(self) -> Agent:
        """Founder Communication Specialist with comprehensive Discord management"""
        config = self.agents_config.get('founder_communication_agent', {})
        
        # Create comprehensive Discord communication suite
        discord_channel_tool = DiscordChannelManagerTool()
        discord_message_tool = DiscordMessageTool()
        discord_listener_tool = DiscordListenerTool()
        discord_voice_tool = DiscordVoiceChannelTool()
        discord_speaker_tool = DiscordSpeakerTool()
        discord_guild_tool = DiscordGuildManagerTool()
        
        # Knowledge management for founder communications
        knowledge_manager = KnowledgeManagerTool()
        knowledge_add = KnowledgeAddTool()
        
        return Agent(
            role=config.get('role', 'Founder Communication Specialist with Discord Mastery'),
            goal=config.get('goal', 
                'Communicate with founder Steve Cornell through all Discord channels, '
                'voice communications, and maintain comprehensive knowledge documentation'
            ),
            backstory=config.get('backstory', 
                'Direct communication link to founder with mastery of all Discord '
                'communication methods including voice, text, and channel management'
            ),
            tools=[
                # Standard tools
                FileReadTool(),
                # Complete Discord communication suite
                discord_channel_tool,
                discord_message_tool,
                discord_listener_tool,
                discord_voice_tool,
                discord_speaker_tool,
                discord_guild_tool,
                # Knowledge management
                knowledge_manager,
                knowledge_add
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )
    
    def analyze_codebase(self) -> Task:
        """Analyze codebase for improvements"""
        config = self.tasks_config.get('analyze_current_codebase', {})
        return Task(
            description=config.get('description', 'Analyze the AI Personal Assistant codebase for improvements'),
            expected_output=config.get('expected_output', 'Detailed analysis report with recommendations'),
            agent=self.code_analyst()
        )
    
    def implement_improvements(self) -> Task:
        """Implement code improvements"""
        config = self.tasks_config.get('implement_crewai_system', {})
        return Task(
            description=config.get('description', 'Implement CrewAI system improvements'),
            expected_output=config.get('expected_output', 'Working CrewAI implementation'),
            agent=self.feature_developer(),
            context=[self.analyze_codebase()]
        )
    
    def communicate_with_founder(self) -> Task:
        """Communicate with founder Steve Cornell"""
        config = self.tasks_config.get('communicate_with_founder', {})
        return Task(
            description=config.get('description', 'Communicate with founder Steve Cornell about project status'),
            expected_output=config.get('expected_output', 'Communication report with founder feedback'),
            agent=self.founder_communicator()
        )
    
    def create_crew(self) -> Crew:
        """Create the AI Assistant development crew"""
        agents = [
            self.code_analyst(),
            self.feature_developer(),
            self.founder_communicator()
        ]
        
        tasks = [
            self.communicate_with_founder(),
            self.analyze_codebase(),
            self.implement_improvements()
        ]
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
    
    def run_development_cycle(self, target_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run a complete development cycle"""
        if target_files is None:
            target_files = ["src/ai_assistant/", "*.py"]
        try:
            self.logger.info("🚀 Starting AI Personal Assistant development cycle")
            
            # Create and run crew
            crew = self.create_crew()
            
            inputs = {
                'target_files': target_files or ["src/ai_assistant/", "*.py"],
                'founder': "Steve Cornell (master80059)",
                'current_date': '2025-10-03',
                'project_name': 'AI Personal Assistant'
            }
            
            result = crew.kickoff(inputs=inputs)
            
            self.logger.info("✅ Development cycle completed successfully")
            
            return {
                'success': True,
                'result': str(result),
                'agents_used': len(crew.agents),
                'tasks_completed': len(crew.tasks)
            }
        
        except Exception as e:
            self.logger.error(f"❌ Development cycle failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

class AutonomousCrewManager:
    """Manages CrewAI workflows for autonomous development"""
    
    def __init__(self, config=None, ollama_toolkit=None):
        self.config = config
        self.ollama = ollama_toolkit
        self.crew_instance = None
        self.logger = logging.getLogger(__name__)
    
    async def initialize_crew(self):
        """Initialize the AI Assistant crew"""
        try:
            self.crew_instance = AIAssistantCrew()
            return self.crew_instance.create_crew()
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize crew: {e}")
            raise
    
    async def run_development_cycle(self, file_path: Optional[str] = None):
        """Run a complete development cycle"""
        try:
            if not self.crew_instance:
                await self.initialize_crew()
            
            # Use the crew's run_development_cycle method
            result = self.crew_instance.run_development_cycle(
                target_files=[file_path] if file_path else ["src/ai_assistant/", "*.py"]
            )
            
            self.logger.info("✅ CrewAI development cycle completed")
            return result
        
        except Exception as e:
            self.logger.error(f"❌ CrewAI development cycle failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def run_specific_analysis(self, task_type: str, target: str):
        """Run specific analysis task"""
        try:
            if not self.crew_instance:
                await self.initialize_crew()
            
            # Create a simple single-task crew for specific analysis
            analyst = self.crew_instance.code_analyst()
            task = Task(
                description=f"Perform {task_type} analysis on {target}",
                expected_output=f"Detailed {task_type} report for {target}",
                agent=analyst
            )
            
            custom_crew = Crew(
                agents=[analyst],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            return custom_crew.kickoff(inputs={'target': target})
        
        except Exception as e:
            self.logger.error(f"❌ Specific analysis failed: {e}")
            return {'success': False, 'error': str(e)}

# Factory function for main.py integration
def create_crew_manager(config=None, ollama_toolkit=None) -> AutonomousCrewManager:
    """Factory function to create crew manager"""
    return AutonomousCrewManager(config, ollama_toolkit)