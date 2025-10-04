# AI Personal Assistant - Framework Reference Guide

## Quick Reference for Discord.py and CrewAI Integration

### 🤖 Discord.py Quick Start

#### Basic Bot Setup
```python
import discord
from discord.ext import commands

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!ai', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command(name='status')
async def status(ctx):
    await ctx.send('🤖 AI Assistant is online!')

# Run bot
bot.run('YOUR_BOT_TOKEN')
```

#### Essential Discord.py Imports
```python
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
```

#### Common Embed Patterns
```python
# Success embed
embed = discord.Embed(
    title="✅ Success",
    description="Operation completed",
    color=discord.Color.green()
)

# Error embed  
embed = discord.Embed(
    title="❌ Error",
    description="Something went wrong",
    color=discord.Color.red()
)

# Info embed
embed = discord.Embed(
    title="ℹ️ Information", 
    description="Details here",
    color=discord.Color.blue()
)
```

### 🛠️ CrewAI Quick Start

#### Basic Crew Setup
```python
from crewai import Agent, Task, Crew, Process

# Create agents
analyst = Agent(
    role='Code Analyst',
    goal='Analyze code quality',
    backstory='Expert in code review',
    verbose=True
)

developer = Agent(
    role='Developer',
    goal='Implement improvements', 
    backstory='Skilled programmer',
    verbose=True
)

# Create tasks
analyze_task = Task(
    description='Analyze the codebase for issues',
    expected_output='List of code quality issues',
    agent=analyst
)

improve_task = Task(
    description='Fix identified issues',
    expected_output='Improved code with fixes',
    agent=developer,
    context=[analyze_task]
)

# Create and run crew
crew = Crew(
    agents=[analyst, developer],
    tasks=[analyze_task, improve_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
```

#### YAML Configuration Pattern
```yaml
# agents.yaml
researcher:
  role: Senior Researcher
  goal: Find accurate information
  backstory: Expert research analyst
  
writer:
  role: Content Writer  
  goal: Create engaging content
  backstory: Skilled technical writer

# tasks.yaml
research_task:
  description: Research the given topic thoroughly
  expected_output: Comprehensive research report
  agent: researcher
  
writing_task:
  description: Write article based on research
  expected_output: Well-structured article
  agent: writer
  context: [research_task]
```

### 🔗 Integration Examples

#### Discord Command with CrewAI
```python
@bot.command(name='analyze')
async def analyze_code(ctx, *, file_path):
    async with ctx.typing():
        # Run CrewAI analysis
        crew = create_analysis_crew()
        result = crew.kickoff(inputs={'file_path': file_path})
    
    embed = discord.Embed(
        title=f"📊 Analysis Complete: {file_path}",
        description=result.get('summary', 'Analysis finished'),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
```

#### Notification System
```python
async def notify_crew_progress(channel, status):
    embed = discord.Embed(
        title="🔄 AI Crew Update",
        description=status,
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    await channel.send(embed=embed)
```

### 📚 Key Documentation Links

#### Discord.py Resources
- **Main Docs**: https://discordpy.readthedocs.io/en/stable/
- **API Reference**: https://discordpy.readthedocs.io/en/stable/api.html
- **Commands Extension**: https://discordpy.readthedocs.io/en/stable/ext/commands/
- **Examples**: https://github.com/Rapptz/discord.py/tree/master/examples

#### CrewAI Resources  
- **GitHub Repo**: https://github.com/crewAIInc/crewAI
- **Documentation**: https://docs.crewai.com/
- **Examples**: https://github.com/crewAIInc/crewAI-examples
- **Tools**: https://docs.crewai.com/concepts/tools

### 🎯 Common Patterns for AI Assistant

#### 1. Development Workflow Automation
```python
@CrewBase
class DevWorkflowCrew:
    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            role='Code Reviewer',
            goal='Review code quality and suggest improvements',
            tools=[FileReadTool(), DirectoryReadTool()],
            verbose=True
        )
    
    @task  
    def review_code(self) -> Task:
        return Task(
            description='Review code in {file_path} for quality issues',
            expected_output='Code review report with recommendations',
            agent=self.code_reviewer()
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

#### 2. Real-time Development Notifications
```python
class AINotificationBot:
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
    
    async def notify_analysis_start(self, file_path):
        channel = self.bot.get_channel(self.channel_id)
        embed = discord.Embed(
            title="🔍 Starting Analysis",
            description=f"Analyzing: `{file_path}`",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)
    
    async def notify_improvements_found(self, improvements):
        channel = self.bot.get_channel(self.channel_id)
        improvements_text = '\n'.join([
            f"• {imp['type']}: {imp['description']}"
            for imp in improvements[:5]
        ])
        
        embed = discord.Embed(
            title="💡 Improvements Found",
            description=improvements_text,
            color=discord.Color.green()
        )
        await channel.send(embed=embed)
```

#### 3. Human-in-the-Loop Approval
```python
class ApprovalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.approved = None
    
    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
    async def approve(self, interaction, button):
        self.approved = True
        await interaction.response.edit_message(
            content="✅ Approved! Executing changes...",
            view=None
        )
    
    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)  
    async def deny(self, interaction, button):
        self.approved = False
        await interaction.response.edit_message(
            content="❌ Denied by user",
            view=None
        )
```

### 🛡️ Security and Best Practices

#### Discord.py Security
- Always validate user permissions
- Use proper rate limiting
- Sanitize user inputs
- Handle errors gracefully

#### CrewAI Security  
- Validate file paths in tasks
- Limit tool access scope
- Monitor resource usage
- Use local models when possible

### 🔧 Troubleshooting

#### Common Discord.py Issues
- **Missing Intents**: Enable required intents in bot settings
- **Rate Limits**: Use proper async patterns and delays
- **Permission Errors**: Check bot permissions in server

#### Common CrewAI Issues
- **Model Loading**: Ensure Ollama is running and models are available
- **Task Dependencies**: Use `context` parameter for task sequencing  
- **Memory Issues**: Monitor agent memory usage with large datasets

---

This reference guide provides quick access to the most commonly used patterns and examples for integrating Discord.py and CrewAI in the AI Personal Assistant project.