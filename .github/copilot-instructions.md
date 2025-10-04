# AI Personal Assistant - GitHub Copilot Instructions

## Project Overview

The AI Personal Assistant is a professional autonomous development platform that leverages local Ollama models for intelligent code analysis, improvement, and feature development. This is a production-ready Python project with proper structure and industry best practices.

## Architecture & Technology Stack

### Core Technologies
- **Python 3.8+**: Primary development language
- **Ollama**: Local AI model integration (deepseek-r1, stable-code, codellama, phi3.5)
- **Discord.py**: Bot integration for real-time communication
- **GitHub API**: Repository management and automation
- **AsyncIO**: Asynchronous programming for high performance
- **PyYAML**: Configuration management
- **pytest**: Testing framework

### Project Structure
```
ai_personal_assistant/
├── src/ai_assistant/              # Main package
│   ├── main.py                    # Application entry point
│   ├── autonomous/                # Autonomous development
│   │   ├── developer.py           # Core developer logic
│   │   ├── analyzer.py            # Code analysis
│   │   └── generator.py           # Feature generation
│   ├── ollama/                    # Ollama integration
│   │   ├── toolkit.py             # Ollama toolkit wrapper
│   │   └── models.py              # Model management
│   ├── discord/                   # Discord bot
│   │   ├── bot.py                 # Bot implementation
│   │   └── commands.py            # Bot commands
│   ├── github/                    # GitHub integration
│   │   └── manager.py             # Repository management
│   └── utils/                     # Utilities
│       ├── config.py              # Configuration management
│       ├── logging.py             # Logging setup
│       └── helpers.py             # Helper functions
├── tests/                         # Test suite
├── docs/                          # Documentation
├── scripts/                       # Utility scripts
├── config/                        # Configuration files
└── logs/                          # Log files
```

## Development Guidelines

### Code Quality Standards
1. **Type Hints**: Use comprehensive type hints for all functions and classes
2. **Docstrings**: Google-style docstrings for all modules, classes, and functions
3. **Error Handling**: Comprehensive exception handling with proper logging
4. **Async/Await**: Use async patterns for I/O operations
5. **Configuration**: All settings through config system, no hardcoded values
6. **Logging**: Structured logging with appropriate levels

### Naming Conventions
- **Classes**: PascalCase (e.g., `AutonomousDeveloper`)
- **Functions/Methods**: snake_case (e.g., `analyze_code_quality`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_MODEL_NAME`)
- **Files**: snake_case (e.g., `autonomous_developer.py`)
- **Packages**: lowercase (e.g., `ai_assistant`)

### Import Organization
```python
# Standard library imports
import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Third-party imports
import yaml
import discord
from discord.ext import commands

# Local imports
from ..utils.config import Config
from ..utils.logging import get_logger
from .models import ModelManager
```

## Core Components

### 1. Configuration System (`utils/config.py`)
- Centralized configuration management
- Environment variable support
- YAML/JSON configuration files
- Dot notation access (e.g., `config.get('ollama.host')`)
- Default value system

**Usage Example:**
```python
from ai_assistant.utils.config import Config

config = Config('config.yaml')
ollama_host = config.get('ollama.host', 'localhost:11434')
```

### 2. Ollama Integration (`ollama/toolkit.py`)
- Comprehensive Ollama client wrapper
- Async and sync support
- Model management
- Tool integration
- Error handling and retries

**Usage Example:**
```python
from ai_assistant.ollama import OllamaToolkit

toolkit = OllamaToolkit()
response = await toolkit.chat_async(
    model='deepseek-r1',
    messages=[{'role': 'user', 'content': 'Analyze this code'}]
)
```

### 3. Autonomous Development (`autonomous/developer.py`)
- Code analysis and improvement
- Feature generation
- Backup system
- GitHub integration
- Continuous development cycles

**Key Features:**
- Analyzes Python files for improvements
- Implements fixes automatically
- Creates new utility modules
- Integrates with version control
- Comprehensive logging and reporting

### 4. Discord Integration (`discord/bot.py`)
- Real-time development notifications
- Command interface for AI control
- Status monitoring
- Admin role support

**Commands:**
- `!ai status` - Show system status
- `!ai analyze [file]` - Analyze specific file
- `!ai models` - List available models
- `!ai config [key]` - Show configuration

### 5. GitHub Management (`github/manager.py`)
- Repository operations
- Automated commits
- Issue management
- PR creation
- Release management

## AI Model Integration

### Supported Models
1. **deepseek-r1**: Advanced reasoning and analysis
2. **stable-code**: Code generation and optimization
3. **codellama**: Code understanding and refactoring
4. **phi3.5**: Lightweight general purpose
5. **dolphin3**: Conversational AI
6. **llava**: Multimodal capabilities

### Model Selection Strategy
```python
def select_model_for_task(task_type: str) -> str:
    """Select optimal model for specific task"""
    model_preferences = {
        'analysis': ['deepseek-r1', 'codellama'],
        'generation': ['stable-code', 'codellama'],
        'conversation': ['dolphin3', 'phi3.5'],
        'multimodal': ['llava']
    }
    return model_preferences.get(task_type, ['deepseek-r1'])[0]
```

## Environment Configuration

### Required Environment Variables
```bash
# Discord Integration (Optional)
DISCORD_BOT_TOKEN=your_discord_bot_token

# GitHub Integration (Required)
GITHUB_TOKEN=your_github_personal_access_token

# AI Corporation Settings
AI_CORP_FOUNDER=Your Name
AI_CORP_MISSION=Autonomous AI Development

# Ollama Configuration (Optional)
OLLAMA_HOST=localhost:11434

# Logging Configuration (Optional)
LOG_LEVEL=INFO
```

### Configuration File Example
```yaml
# config/ai_assistant.yaml
logging:
  level: INFO
  file: logs/ai_assistant.log

ollama:
  host: localhost:11434
  default_model: deepseek-r1
  timeout: 30

autonomous:
  enabled: true
  cycle_interval: 600  # 10 minutes
  max_files_per_cycle: 5
  backup_before_changes: true

discord:
  enabled: false
  command_prefix: "!ai"
  admin_roles: ["AI Developer", "Admin"]

github:
  auto_commit: true
  commit_message_prefix: "[AI-DEV]"
  default_branch: main
```

## Development Workflows

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement in appropriate package (follow structure)
3. Add comprehensive tests
4. Update documentation
5. Create pull request

### Code Analysis Workflow
1. **File Discovery**: Scan Python files in workspace
2. **Model Selection**: Choose appropriate model for analysis
3. **Analysis**: Generate improvement suggestions
4. **Implementation**: Apply fixes with backups
5. **Validation**: Test changes
6. **Documentation**: Log all changes

### Testing Strategy
```python
# tests/test_autonomous_developer.py
import pytest
from ai_assistant.autonomous.developer import AutonomousDeveloper

@pytest.mark.asyncio
async def test_code_analysis():
    """Test code analysis functionality"""
    developer = AutonomousDeveloper()
    result = await developer.analyze_file('sample.py')
    assert result is not None
    assert 'improvements' in result
```

## Error Handling Patterns

### Standard Error Handling
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def safe_operation() -> Optional[Any]:
    """Example of proper error handling"""
    try:
        result = await risky_operation()
        logger.info("✅ Operation completed successfully")
        return result
        
    except SpecificException as e:
        logger.warning(f"⚠️ Expected error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise
```

### Configuration Validation
```python
def validate_config(config: Config) -> bool:
    """Validate configuration settings"""
    required_keys = ['github.token', 'ai_corp.founder']
    
    for key in required_keys:
        if not config.has(key):
            logger.error(f"❌ Missing required config: {key}")
            return False
    
    return True
```

## Performance Optimization

### Async Patterns
- Use `asyncio.gather()` for concurrent operations
- Implement proper connection pooling
- Use async context managers
- Handle backpressure appropriately

### Caching Strategy
- Cache model responses for similar queries
- Implement file hash-based caching
- Use TTL for configuration caching
- Memory-efficient data structures

### Resource Management
```python
async def process_files_concurrently(files: List[Path]) -> List[Result]:
    """Process multiple files with concurrency control"""
    semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
    
    async def process_file(file_path: Path) -> Result:
        async with semaphore:
            return await analyze_file(file_path)
    
    tasks = [process_file(f) for f in files]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## Security Considerations

### Token Management
- Store tokens in environment variables or secure config
- Never commit tokens to version control
- Implement token rotation capabilities
- Use minimal permission scopes

### File Operations
- Validate file paths to prevent directory traversal
- Create backups before modifications
- Implement file size limits
- Sanitize user inputs

### API Security
```python
def sanitize_input(user_input: str) -> str:
    """Sanitize user input for safety"""
    # Remove potentially dangerous characters
    safe_input = re.sub(r'[<>:"\/\\|?*]', '', user_input)
    # Limit length
    return safe_input[:1000]
```

## Monitoring & Observability

### Logging Strategy
- Structured logging with JSON format
- Separate log files per component
- Centralized error aggregation
- Performance metrics logging

### Health Checks
```python
async def health_check() -> Dict[str, Any]:
    """Comprehensive system health check"""
    health = {
        'ollama': await check_ollama_connection(),
        'github': await check_github_connection(),
        'disk_space': check_disk_space(),
        'memory_usage': get_memory_usage(),
        'uptime': get_uptime()
    }
    return health
```

### Metrics Collection
- Development cycle success rates
- Model response times
- Error frequencies
- Resource utilization

## Testing Guidelines

### Unit Tests
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_autonomous_development():
    """Test autonomous development workflow"""
    with patch('ai_assistant.ollama.OllamaToolkit') as mock_ollama:
        mock_ollama.return_value.chat_async = AsyncMock(
            return_value={'message': {'content': 'test response'}}
        )
        
        developer = AutonomousDeveloper()
        result = await developer.run_cycle()
        
        assert result['success'] is True
        mock_ollama.assert_called_once()
```

### Integration Tests
- Test full development workflows
- Validate configuration loading
- Test error recovery scenarios
- Performance regression tests

### Test Data Management
- Use fixtures for consistent test data
- Mock external dependencies
- Clean up test artifacts
- Parameterized tests for multiple scenarios

## Deployment & Operations

### Entry Points
```bash
# Main application
ai-assistant --config config.yaml

# Development mode
ai-assistant --dev-mode --autonomous-only

# Discord bot only
ai-discord --config discord_config.yaml
```

### Docker Support
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

RUN pip install -e .

CMD ["ai-assistant"]
```

### Production Considerations
- Use process managers (systemd, supervisor)
- Implement graceful shutdown
- Configure log rotation
- Monitor resource usage
- Set up alerting

## Troubleshooting Guide

### Common Issues
1. **Ollama Connection Failed**
   - Check if Ollama is running: `ollama serve`
   - Verify host configuration
   - Check firewall settings

2. **Discord Bot Not Responding**
   - Verify bot token validity
   - Check bot permissions in server
   - Review Discord API rate limits

3. **GitHub API Errors**
   - Validate token permissions
   - Check rate limit status
   - Verify repository access

### Debug Mode
```python
# Enable debug logging
import logging
logging.getLogger('ai_assistant').setLevel(logging.DEBUG)

# Run with debug configuration
ai-assistant --dev-mode --config debug_config.yaml
```

## Contributing Guidelines

### Code Review Checklist
- [ ] Type hints added for all new functions
- [ ] Comprehensive docstrings added
- [ ] Unit tests written and passing
- [ ] Error handling implemented
- [ ] Logging added for important operations
- [ ] Configuration properly externalized
- [ ] Documentation updated

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes without migration guide
```

## Future Roadmap

### Planned Features
- [ ] Web interface for monitoring
- [ ] Plugin system for extensions
- [ ] Multi-language support (JavaScript, Go, Rust)
- [ ] Advanced AI model fine-tuning
- [ ] Team collaboration features
- [ ] Cloud deployment options
- [ ] Performance analytics dashboard
- [ ] Automated testing generation

### Technical Debt
- [ ] Migrate to Pydantic for configuration
- [ ] Implement proper dependency injection
- [ ] Add comprehensive API documentation
- [ ] Optimize memory usage
- [ ] Improve error recovery mechanisms

## Discord.py Integration Reference

### Core Discord.py Architecture

The AI Personal Assistant uses Discord.py v2.3+ for real-time development notifications and command interfaces.

#### ✅ **Essential Discord.py Patterns**

##### Bot Setup with Async Architecture
```python
import discord
from discord.ext import commands
import asyncio
from typing import Optional

class AIAssistantBot(commands.Bot):
    """Production Discord bot for AI development notifications"""
    
    def __init__(self, config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=config.get('discord.command_prefix', '!ai'),
            intents=intents,
            help_command=None
        )
        
        self.config = config
    
    async def setup_hook(self):
        """Called when bot is starting up"""
        await self.load_extension('ai_assistant.discord.commands')
        print(f"✅ Bot logged in as {self.user}")
    
    async def on_ready(self):
        """Bot is fully ready"""
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="AI Development"
        )
        await self.change_presence(activity=activity)
```

##### Command Framework Implementation
```python
from discord.ext import commands
import discord

class DevelopmentCommands(commands.Cog):
    """Development commands for AI Assistant"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ai_assistant = None  # Will be injected
    
    @commands.command(name='status')
    async def ai_status(self, ctx):
        """Show AI system status"""
        embed = discord.Embed(
            title="🤖 AI Assistant Status",
            color=discord.Color.green()
        )
        embed.add_field(name="Ollama", value="✅ Connected", inline=True)
        embed.add_field(name="Models", value="5 Available", inline=True)
        embed.add_field(name="Uptime", value="2h 45m", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='analyze')
    async def analyze_file(self, ctx, *, file_path: str = None):
        """Analyze a specific file"""
        if not file_path:
            await ctx.send("❌ Please provide a file path to analyze")
            return
        
        async with ctx.typing():
            # Trigger autonomous development analysis
            result = await self.ai_assistant.analyze_file(file_path)
        
        embed = discord.Embed(
            title=f"📊 Analysis: {file_path}",
            description=result.get('summary', 'Analysis complete'),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='models')
    async def list_models(self, ctx):
        """List available Ollama models"""
        models = await self.ai_assistant.ollama.list_models()
        
        model_list = '\n'.join([
            f"• **{model['name']}** - {model.get('description', 'No description')}"
            for model in models.get('models', [])
        ])
        
        embed = discord.Embed(
            title="🧠 Available Models",
            description=model_list or "No models available",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DevelopmentCommands(bot))
```

##### Event Handling and Notifications
```python
class AINotificationHandler:
    """Handles AI development event notifications"""
    
    def __init__(self, bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self.channel = None
    
    async def setup(self):
        """Initialize notification channel"""
        self.channel = self.bot.get_channel(self.channel_id)
        if not self.channel:
            print(f"⚠️ Could not find channel {self.channel_id}")
    
    async def notify_analysis_complete(self, file_path: str, improvements: list):
        """Notify when file analysis is complete"""
        if not self.channel:
            return
        
        embed = discord.Embed(
            title="🔍 Analysis Complete",
            description=f"File: `{file_path}`",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        
        improvements_text = '\n'.join([
            f"• {improvement['type']}: {improvement['description']}"
            for improvement in improvements[:5]  # Limit to 5
        ])
        
        embed.add_field(
            name="Improvements Found",
            value=improvements_text or "No improvements suggested",
            inline=False
        )
        
        await self.channel.send(embed=embed)
    
    async def notify_error(self, error: str, context: str = None):
        """Notify about errors"""
        embed = discord.Embed(
            title="❌ Error Occurred",
            description=f"```{error}```",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        
        if context:
            embed.add_field(name="Context", value=context, inline=False)
        
        await self.channel.send(embed=embed)
```

#### ✅ **Discord.py Best Practices for AI Assistant**

1. **Rate Limit Handling**: Always use `async with ctx.typing()` for long operations
2. **Embed Usage**: Use rich embeds for AI notifications and status updates
3. **Error Handling**: Implement comprehensive error handling with user feedback
4. **Permission Checks**: Validate user permissions for sensitive commands
5. **Async Patterns**: Use proper async/await patterns throughout

##### Error Handling Example
```python
@commands.command(name='deploy')
@commands.has_role('AI Developer')
async def deploy_changes(self, ctx, *, branch: str = 'main'):
    """Deploy AI changes to specified branch"""
    try:
        async with ctx.typing():
            result = await self.ai_assistant.deploy_to_branch(branch)
        
        if result['success']:
            embed = discord.Embed(
                title="🚀 Deployment Successful",
                description=f"Deployed to `{branch}` branch",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Deployment Failed",
                description=result.get('error', 'Unknown error'),
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)
    
    except commands.MissingRole:
        await ctx.send("❌ You need the 'AI Developer' role to use this command")
    except Exception as e:
        await ctx.send(f"❌ Unexpected error: {str(e)}")
        # Log error for debugging
        print(f"Deploy command error: {e}")
```

## CrewAI Integration Reference

### Core CrewAI Architecture for AI Assistant

The AI Personal Assistant integrates CrewAI for orchestrating multiple AI agents working together on development tasks.

#### ✅ **CrewAI Foundation Patterns**

##### Agent Definition with YAML Configuration
```yaml
# config/agents.yaml
code_analyst:
  role: >
    Senior Code Quality Analyst
  goal: >
    Analyze code for quality, performance, and security issues
  backstory: >
    You are an expert code analyst with deep knowledge of Python best practices,
    design patterns, and security vulnerabilities. You can identify issues and
    suggest concrete improvements.

feature_developer:
  role: >
    AI Feature Developer
  goal: >
    Generate and implement new features based on analysis
  backstory: >
    You are a skilled developer who can take analysis results and create
    working code implementations. You focus on clean, maintainable code.

documentation_writer:
  role: >
    Technical Documentation Specialist
  goal: >
    Create comprehensive documentation for AI systems
  backstory: >
    You excel at writing clear, detailed documentation that helps developers
    understand and maintain AI systems.
```

##### Task Configuration with YAML
```yaml
# config/tasks.yaml
analyze_codebase:
  description: >
    Analyze the AI Personal Assistant codebase in {file_path}
    Focus on code quality, performance optimization opportunities,
    and potential security issues. Current year is 2025.
  expected_output: >
    A detailed analysis report with:
    - Code quality score (1-10)
    - List of specific issues found
    - Recommended improvements with priority levels
    - Security assessment
  agent: code_analyst

implement_improvements:
  description: >
    Based on the analysis report, implement the top 3 highest priority
    improvements in the codebase. Ensure all changes follow Python
    best practices and maintain backward compatibility.
  expected_output: >
    Implementation report with:
    - Code changes made
    - Files modified
    - Testing instructions
    - Deployment notes
  agent: feature_developer
  context: [analyze_codebase]

update_documentation:
  description: >
    Update documentation to reflect code changes and improvements.
    Include new features, API changes, and usage examples.
  expected_output: >
    Updated documentation including:
    - README.md updates
    - API documentation
    - Configuration guides
    - Example usage
  agent: documentation_writer
  context: [implement_improvements]
  output_file: docs/updated_docs.md
```

##### CrewAI Integration in AI Assistant
```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, CodeInterpreterTool
from typing import List

@CrewBase
class AIAssistantCrew:
    """AI Personal Assistant development crew"""
    
    agents: List[Agent]
    tasks: List[Task]
    
    # Configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def code_analyst(self) -> Agent:
        """Senior Code Quality Analyst"""
        return Agent(
            config=self.agents_config['code_analyst'],
            tools=[
                DirectoryReadTool(directory='src/'),
                FileReadTool(),
                CodeInterpreterTool()
            ],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def feature_developer(self) -> Agent:
        """AI Feature Developer"""
        return Agent(
            config=self.agents_config['feature_developer'],
            tools=[
                FileReadTool(),
                CodeInterpreterTool(),
                DirectoryReadTool(directory='src/')
            ],
            verbose=True,
            allow_delegation=True
        )
    
    @agent
    def documentation_writer(self) -> Agent:
        """Technical Documentation Specialist"""
        return Agent(
            config=self.agents_config['documentation_writer'],
            tools=[
                FileReadTool(),
                DirectoryReadTool(directory='docs/')
            ],
            verbose=True
        )
    
    @task
    def analyze_codebase(self) -> Task:
        """Analyze codebase for improvements"""
        return Task(
            config=self.tasks_config['analyze_codebase'],
            agent=self.code_analyst()
        )
    
    @task
    def implement_improvements(self) -> Task:
        """Implement code improvements"""
        return Task(
            config=self.tasks_config['implement_improvements'],
            agent=self.feature_developer()
        )
    
    @task
    def update_documentation(self) -> Task:
        """Update project documentation"""
        return Task(
            config=self.tasks_config['update_documentation'],
            agent=self.documentation_writer()
        )
    
    @crew
    def crew(self) -> Crew:
        """Create the AI Assistant development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,  # Enable planning for complex workflows
            planning_llm="deepseek-r1"  # Use local Ollama model
        )
```

#### ✅ **CrewAI Integration Patterns**

##### Autonomous Development Workflow
```python
class AutonomousCrewManager:
    """Manages CrewAI workflows for autonomous development"""
    
    def __init__(self, config, ollama_toolkit):
        self.config = config
        self.ollama = ollama_toolkit
        self.crew_instance = None
    
    async def initialize_crew(self):
        """Initialize the AI Assistant crew"""
        self.crew_instance = AIAssistantCrew()
        return self.crew_instance.crew()
    
    async def run_development_cycle(self, file_path: str = None):
        """Run a complete development cycle"""
        if not self.crew_instance:
            await self.initialize_crew()
        
        inputs = {
            'file_path': file_path or 'src/ai_assistant/',
            'current_date': '2025-10-03',
            'focus_areas': ['code_quality', 'performance', 'security']
        }
        
        try:
            crew = self.crew_instance.crew()
            result = crew.kickoff(inputs=inputs)
            
            return {
                'success': True,
                'result': result,
                'files_analyzed': inputs['file_path'],
                'timestamp': asyncio.get_event_loop().time()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': asyncio.get_event_loop().time()
            }
    
    async def run_specific_analysis(self, task_type: str, target: str):
        """Run specific analysis task"""
        custom_crew = Crew(
            agents=[self.crew_instance.code_analyst()],
            tasks=[self._create_custom_task(task_type, target)],
            process=Process.sequential,
            verbose=True
        )
        
        return custom_crew.kickoff(inputs={'target': target})
    
    def _create_custom_task(self, task_type: str, target: str) -> Task:
        """Create custom task for specific analysis"""
        return Task(
            description=f"Perform {task_type} analysis on {target}",
            expected_output=f"Detailed {task_type} report for {target}",
            agent=self.crew_instance.code_analyst()
        )
```

##### CrewAI with Ollama Local Models
```python
from crewai import LLM

class LocalOllamaIntegration:
    """Integrate CrewAI with local Ollama models"""
    
    def __init__(self, ollama_host: str = "localhost:11434"):
        self.ollama_host = ollama_host
    
    def get_crew_llm(self, model_name: str = "deepseek-r1") -> LLM:
        """Get LLM instance for CrewAI using local Ollama"""
        return LLM(
            model=f"ollama/{model_name}",
            base_url=f"http://{self.ollama_host}",
            temperature=0.1,
            timeout=120
        )
    
    def create_specialized_agent(self, role: str, model: str = None) -> Agent:
        """Create agent with specialized local model"""
        llm = self.get_crew_llm(model or self._select_model_for_role(role))
        
        return Agent(
            role=role,
            goal=f"Excel at {role.lower()} tasks using local AI",
            backstory=f"Expert {role.lower()} with access to local AI models",
            llm=llm,
            verbose=True
        )
    
    def _select_model_for_role(self, role: str) -> str:
        """Select optimal local model for specific role"""
        model_mapping = {
            'code_analyst': 'deepseek-r1',      # Best for code analysis
            'feature_developer': 'stable-code',  # Optimized for code generation
            'documentation_writer': 'phi3.5',   # Good for documentation
            'security_auditor': 'codellama',     # Strong for security analysis
        }
        return model_mapping.get(role.lower(), 'deepseek-r1')
```

#### ✅ **CrewAI Best Practices for AI Assistant**

1. **Task Sequencing**: Use `context` parameter to create task dependencies
2. **Agent Specialization**: Create focused agents for specific development tasks
3. **Local Model Integration**: Use Ollama models for privacy and performance
4. **Error Recovery**: Implement fallback strategies for failed tasks
5. **Result Validation**: Always validate crew outputs before applying changes

##### Human-in-the-Loop Integration
```python
from crewai import Task

class HumanApprovalTask(Task):
    """Task that requires human approval before proceeding"""
    
    def __init__(self, *args, human_input_required=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.human_input = human_input_required
    
    async def execute_with_approval(self, discord_bot=None, channel_id=None):
        """Execute task with Discord approval mechanism"""
        if self.human_input and discord_bot:
            # Send approval request to Discord
            channel = discord_bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="🤖 AI Task Approval Required",
                    description=f"Task: {self.description}",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="Expected Output",
                    value=self.expected_output,
                    inline=False
                )
                
                message = await channel.send(
                    embed=embed,
                    view=ApprovalView()  # Custom Discord view with approve/deny buttons
                )
                
                # Wait for approval (implement timeout)
                approved = await self.wait_for_approval(message)
                
                if approved:
                    return self.execute()
                else:
                    return "Task cancelled by human operator"
        
        return self.execute()

class ApprovalView(discord.ui.View):
    """Discord UI for task approval"""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
        self.approved = None
    
    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green, emoji='✅')
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.approved = True
        await interaction.response.edit_message(
            content="✅ Task approved and executing...",
            view=None
        )
        self.stop()
    
    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red, emoji='❌')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.approved = False
        await interaction.response.edit_message(
            content="❌ Task denied by human operator",
            view=None
        )
        self.stop()
```

### Integration Examples

#### Complete AI Development Workflow
```python
async def run_ai_development_workflow():
    """Complete AI development workflow with Discord notifications"""
    
    # Initialize components
    crew_manager = AutonomousCrewManager(config, ollama_toolkit)
    discord_bot = AIAssistantBot(config)
    notification_handler = AINotificationHandler(discord_bot, channel_id)
    
    try:
        # Run crew analysis
        await notification_handler.notify_start("Starting AI development cycle")
        
        result = await crew_manager.run_development_cycle('src/ai_assistant/')
        
        if result['success']:
            await notification_handler.notify_analysis_complete(
                result['files_analyzed'],
                result.get('improvements', [])
            )
        else:
            await notification_handler.notify_error(
                result['error'],
                "AI Development Cycle"
            )
    
    except Exception as e:
        await notification_handler.notify_error(str(e), "Workflow Exception")
```

This comprehensive integration provides:
- **Local AI Model Integration**: Uses Ollama for privacy and performance
- **Discord Real-time Notifications**: Keep developers informed of AI activities
- **Human-in-the-Loop Approval**: Critical changes require human approval
- **Structured Task Management**: YAML-based configuration for maintainability
- **Error Handling and Recovery**: Robust error management with user feedback

---

**Remember: This is a production-quality system. Always follow best practices, write comprehensive tests, and maintain high code quality standards.**
