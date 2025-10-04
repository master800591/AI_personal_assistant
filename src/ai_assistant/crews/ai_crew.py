"""
AI Personal Assistant - CrewAI Implementation
Founder: Steve Cornell (master80059)
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, CodeInterpreterTool
from crewai import LLM

class AIPersonalAssistantCrew:
    """Complete CrewAI implementation for AI Personal Assistant"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger(__name__)
        
        # Load configurations
        self.agents_config = self._load_yaml("agents.yaml")
        self.tasks_config = self._load_yaml("tasks.yaml")
        
        # Initialize tools
        self.tools = self._setup_tools()
        
        # Initialize LLM for local Ollama
        self.llm = LLM(
            model="ollama/deepseek-r1",
            base_url="http://localhost:11434",
            temperature=0.1
        )
        
        self.logger.info("🤖 AI Personal Assistant Crew initialized")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        file_path = self.config_dir / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load {filename}: {e}")
            return {}
    
    def _setup_tools(self) -> Dict[str, Any]:
        """Setup tools for agents"""
        return {
            'directory_read': DirectoryReadTool(directory='src/'),
            'file_read': FileReadTool(),
            'code_interpreter': CodeInterpreterTool(),
            'workspace_read': DirectoryReadTool(directory='.')
        }
    
    def create_founder_communication_agent(self) -> Agent:
        """Create agent for communicating with founder Steve Cornell"""
        config = self.agents_config.get('founder_communication_agent', {})
        
        return Agent(
            role=config.get('role', 'Founder Communication Specialist'),
            goal=config.get('goal', 'Communicate with founder Steve Cornell'),
            backstory=config.get('backstory', 'Direct communication link to founder'),
            tools=[self.tools['file_read']],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )
    
    def create_code_analysis_agent(self) -> Agent:
        """Create agent for code analysis"""
        config = self.agents_config.get('code_analysis_agent', {})
        
        return Agent(
            role=config.get('role', 'Senior Code Analysis Expert'),
            goal=config.get('goal', 'Analyze code for quality and improvements'),
            backstory=config.get('backstory', 'Expert Python developer'),
            tools=[
                self.tools['directory_read'],
                self.tools['file_read'],
                self.tools['code_interpreter']
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', True)
        )
    
    def create_feature_development_agent(self) -> Agent:
        """Create agent for feature development"""
        config = self.agents_config.get('feature_development_agent', {})
        
        return Agent(
            role=config.get('role', 'AI Feature Developer'),
            goal=config.get('goal', 'Implement features and improvements'),
            backstory=config.get('backstory', 'Skilled developer creating working code'),
            tools=[
                self.tools['directory_read'],
                self.tools['file_read'],
                self.tools['code_interpreter']
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', True)
        )
    
    def create_github_automation_agent(self) -> Agent:
        """Create agent for GitHub automation"""
        config = self.agents_config.get('github_automation_agent', {})
        
        return Agent(
            role=config.get('role', 'GitHub DevOps Specialist'),
            goal=config.get('goal', 'Manage GitHub repository operations'),
            backstory=config.get('backstory', 'Expert in GitHub automation'),
            tools=[
                self.tools['directory_read'],
                self.tools['file_read']
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )
    
    def create_discord_integration_agent(self) -> Agent:
        """Create agent for Discord integration"""
        config = self.agents_config.get('discord_integration_agent', {})
        
        return Agent(
            role=config.get('role', 'Discord Bot Developer'),
            goal=config.get('goal', 'Develop Discord bot functionality'),
            backstory=config.get('backstory', 'Discord.py specialist'),
            tools=[
                self.tools['file_read'],
                self.tools['code_interpreter']
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )
    
    def create_testing_agent(self) -> Agent:
        """Create agent for testing and QA"""
        config = self.agents_config.get('testing_agent', {})
        
        return Agent(
            role=config.get('role', 'Quality Assurance Engineer'),
            goal=config.get('goal', 'Create tests and ensure quality'),
            backstory=config.get('backstory', 'Meticulous QA engineer'),
            tools=[
                self.tools['directory_read'],
                self.tools['file_read'],
                self.tools['code_interpreter']
            ],
            llm=self.llm,
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', True)
        )
    
    def create_tasks(self, target_files: List[str] = None) -> List[Task]:
        """Create all tasks for the crew"""
        if target_files is None:
            target_files = ["src/ai_assistant/", "*.py"]
        
        # Create agents
        founder_agent = self.create_founder_communication_agent()
        analysis_agent = self.create_code_analysis_agent()
        dev_agent = self.create_feature_development_agent()
        github_agent = self.create_github_automation_agent()
        discord_agent = self.create_discord_integration_agent()
        testing_agent = self.create_testing_agent()
        
        tasks = []
        
        # Task 1: Communicate with founder
        founder_task = Task(
            description=self.tasks_config['communicate_with_founder']['description'],
            expected_output=self.tasks_config['communicate_with_founder']['expected_output'],
            agent=founder_agent
        )
        tasks.append(founder_task)
        
        # Task 2: Analyze codebase
        analysis_task = Task(
            description=self.tasks_config['analyze_current_codebase']['description'].format(
                target_files=", ".join(target_files)
            ),
            expected_output=self.tasks_config['analyze_current_codebase']['expected_output'],
            agent=analysis_agent
        )
        tasks.append(analysis_task)
        
        # Task 3: Implement CrewAI system
        crewai_task = Task(
            description=self.tasks_config['implement_crewai_system']['description'],
            expected_output=self.tasks_config['implement_crewai_system']['expected_output'],
            agent=dev_agent,
            context=[analysis_task]
        )
        tasks.append(crewai_task)
        
        # Task 4: Setup Discord bot
        discord_task = Task(
            description=self.tasks_config['setup_discord_bot']['description'],
            expected_output=self.tasks_config['setup_discord_bot']['expected_output'],
            agent=discord_agent,
            context=[crewai_task]
        )
        tasks.append(discord_task)
        
        # Task 5: Automate GitHub workflow
        github_task = Task(
            description=self.tasks_config['automate_github_workflow']['description'],
            expected_output=self.tasks_config['automate_github_workflow']['expected_output'],
            agent=github_agent,
            context=[discord_task]
        )
        tasks.append(github_task)
        
        # Task 6: Create comprehensive tests
        testing_task = Task(
            description=self.tasks_config['create_comprehensive_tests']['description'],
            expected_output=self.tasks_config['create_comprehensive_tests']['expected_output'],
            agent=testing_agent,
            context=[github_task]
        )
        tasks.append(testing_task)
        
        # Task 7: Deploy production system
        deploy_task = Task(
            description=self.tasks_config['deploy_production_system']['description'],
            expected_output=self.tasks_config['deploy_production_system']['expected_output'],
            agent=github_agent,
            context=[testing_task]
        )
        tasks.append(deploy_task)
        
        return tasks
    
    def create_crew(self, target_files: List[str] = None) -> Crew:
        """Create the complete crew"""
        tasks = self.create_tasks(target_files)
        
        # Extract agents from tasks
        agents = [task.agent for task in tasks]
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=self.llm
        )
        
        self.logger.info(f"✅ Created crew with {len(agents)} agents and {len(tasks)} tasks")
        return crew
    
    def run_development_cycle(self, target_files: List[str] = None) -> Dict[str, Any]:
        """Run a complete development cycle"""
        try:
            self.logger.info("🚀 Starting AI Personal Assistant development cycle")
            
            # Create and run crew
            crew = self.create_crew(target_files)
            
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
                'tasks_completed': len(crew.tasks),
                'timestamp': '2025-10-03'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Development cycle failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': '2025-10-03'
            }

# Factory function
def create_ai_assistant_crew() -> AIPersonalAssistantCrew:
    """Factory function to create AI Personal Assistant crew"""
    return AIPersonalAssistantCrew()

# Main execution for testing
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logging.basicConfig(level=logging.INFO)
        
        crew_manager = create_ai_assistant_crew()
        result = crew_manager.run_development_cycle()
        
        print(f"🎯 Development cycle result: {result}")
    
    asyncio.run(main())