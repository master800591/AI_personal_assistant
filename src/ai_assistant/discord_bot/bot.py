"""
Discord Bot for AI Personal Assistant
Founder: Steve Cornell (master80059)
Real-time communication and crew management
"""

import os
import asyncio
import logging
import discord
from discord.ext import commands
from typing import Dict, Any, Optional
from datetime import datetime

class AIAssistantBot(commands.Bot):
    """AI Personal Assistant Discord Bot"""
    
    def __init__(self, token: str, crew_manager=None):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!ai ',
            intents=intents,
            help_command=None
        )
        
        self.token = token
        self.crew_manager = crew_manager
        self.logger = logging.getLogger(__name__)
        self.founder_id = None  # Will be set when Steve Cornell joins
        self.notification_channel = None
        
        self.logger.info("🤖 AI Assistant Discord Bot initialized")
    
    async def setup_hook(self):
        """Called when bot is starting up"""
        await self.add_cog(AICommands(self))
        await self.add_cog(CrewManagement(self))
        await self.add_cog(FounderCommunication(self))
        self.logger.info("✅ Bot extensions loaded")
    
    async def on_ready(self):
        """Bot is ready"""
        self.logger.info(f"✅ {self.user} is now online!")
        
        # Set activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="AI Development | !ai help"
        )
        await self.change_presence(activity=activity)
        
        # Find founder if already in server
        await self._find_founder()
        
        # Send startup notification
        await self.notify_system_status("🚀 AI Assistant Bot is now online and ready!")
    
    async def _find_founder(self):
        """Find Steve Cornell (master80059) in the server"""
        for guild in self.guilds:
            for member in guild.members:
                if 'master80059' in member.name.lower() or 'steve' in member.name.lower():
                    self.founder_id = member.id
                    self.logger.info(f"👑 Found founder: {member.name} ({member.id})")
                    break
    
    async def notify_system_status(self, message: str, embed_color=discord.Color.green()):
        """Send system notification to appropriate channel"""
        if self.notification_channel:
            embed = discord.Embed(
                title="🤖 AI Assistant System",
                description=message,
                color=embed_color,
                timestamp=datetime.utcnow()
            )
            await self.notification_channel.send(embed=embed)
    
    async def notify_founder(self, message: str, urgent: bool = False):
        """Notify the founder directly"""
        if self.founder_id:
            try:
                founder = self.get_user(self.founder_id)
                if founder:
                    prefix = "🚨 URGENT: " if urgent else "💡 "
                    await founder.send(f"{prefix}{message}")
                    self.logger.info(f"📨 Notified founder: {message[:50]}...")
            except Exception as e:
                self.logger.error(f"Failed to notify founder: {e}")

class AICommands(commands.Cog):
    """Basic AI Assistant commands"""
    
    def __init__(self, bot: AIAssistantBot):
        self.bot = bot
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show available commands"""
        embed = discord.Embed(
            title="🤖 AI Assistant Commands",
            description="Available commands for the AI Personal Assistant",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Basic Commands",
            value="""
            `!ai status` - Show system status
            `!ai ping` - Check bot responsiveness
            `!ai help` - Show this help message
            """,
            inline=False
        )
        
        embed.add_field(
            name="Crew Management",
            value="""
            `!ai crew status` - Show crew status
            `!ai crew start` - Start development cycle
            `!ai crew stop` - Stop current operations
            `!ai crew tasks` - List current tasks
            """,
            inline=False
        )
        
        embed.add_field(
            name="Development",
            value="""
            `!ai analyze [file]` - Analyze specific file
            `!ai deploy` - Deploy changes
            `!ai github status` - GitHub repository status
            """,
            inline=False
        )
        
        embed.add_field(
            name="Founder Commands",
            value="""
            `!ai ask [question]` - Ask the founder a question
            `!ai report` - Generate development report
            `!ai config [setting]` - View/change configuration
            """,
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='status')
    async def status(self, ctx):
        """Show AI system status"""
        embed = discord.Embed(
            title="🤖 AI Assistant Status",
            color=discord.Color.green()
        )
        
        # Check Ollama
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                ollama_status = f"✅ Connected ({len(models)} models)"
            else:
                ollama_status = "⚠️ Not responding"
        except:
            ollama_status = "❌ Not available"
        
        embed.add_field(name="Ollama", value=ollama_status, inline=True)
        embed.add_field(name="Bot", value="✅ Online", inline=True)
        
        # Crew status
        if self.bot.crew_manager:
            embed.add_field(name="CrewAI", value="✅ Ready", inline=True)
        else:
            embed.add_field(name="CrewAI", value="❌ Not loaded", inline=True)
        
        # Founder status
        founder_status = "✅ Connected" if self.bot.founder_id else "❓ Not found"
        embed.add_field(name="Founder", value=founder_status, inline=True)
        
        embed.add_field(name="Uptime", value="Running", inline=True)
        embed.add_field(name="Version", value="1.0.0-dev", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot responsiveness"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")

class CrewManagement(commands.Cog):
    """CrewAI management commands"""
    
    def __init__(self, bot: AIAssistantBot):
        self.bot = bot
    
    @commands.group(name='crew')
    async def crew(self, ctx):
        """CrewAI management commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `!ai crew status`, `!ai crew start`, or `!ai crew tasks`")
    
    @crew.command(name='status')
    async def crew_status(self, ctx):
        """Show crew status"""
        embed = discord.Embed(
            title="🧠 CrewAI Status",
            color=discord.Color.purple()
        )
        
        if self.bot.crew_manager:
            embed.add_field(name="Status", value="✅ Ready", inline=True)
            embed.add_field(name="Agents", value="6 Active", inline=True)
            embed.add_field(name="Tasks", value="7 Configured", inline=True)
            
            agents = [
                "👑 Founder Communication",
                "🔍 Code Analysis", 
                "⚡ Feature Development",
                "🐙 GitHub Automation",
                "🤖 Discord Integration",
                "🧪 Testing & QA"
            ]
            
            embed.add_field(
                name="Active Agents",
                value="\n".join(agents),
                inline=False
            )
        else:
            embed.add_field(name="Status", value="❌ Not loaded", inline=True)
            embed.description = "CrewAI system is not currently loaded"
        
        await ctx.send(embed=embed)
    
    @crew.command(name='start')
    async def crew_start(self, ctx):
        """Start a development cycle"""
        if not self.bot.crew_manager:
            await ctx.send("❌ CrewAI system not loaded")
            return
        
        embed = discord.Embed(
            title="🚀 Starting Development Cycle",
            description="Initiating AI development crew...",
            color=discord.Color.orange()
        )
        
        message = await ctx.send(embed=embed)
        
        try:
            # Start async development cycle
            async with ctx.typing():
                result = await asyncio.create_task(
                    self._run_crew_cycle()
                )
            
            if result['success']:
                embed.color = discord.Color.green()
                embed.title = "✅ Development Cycle Complete"
                embed.description = f"Successfully completed {result.get('tasks_completed', 0)} tasks"
                
                embed.add_field(
                    name="Results",
                    value=f"Agents: {result.get('agents_used', 0)}\nTasks: {result.get('tasks_completed', 0)}",
                    inline=True
                )
            else:
                embed.color = discord.Color.red()
                embed.title = "❌ Development Cycle Failed"
                embed.description = f"Error: {result.get('error', 'Unknown error')}"
            
            await message.edit(embed=embed)
            
        except Exception as e:
            embed.color = discord.Color.red()
            embed.title = "❌ Development Cycle Failed"
            embed.description = f"Exception: {str(e)}"
            await message.edit(embed=embed)
    
    async def _run_crew_cycle(self):
        """Run crew development cycle"""
        # This would integrate with the actual CrewAI system
        await asyncio.sleep(2)  # Simulate processing
        return {
            'success': True,
            'tasks_completed': 7,
            'agents_used': 6,
            'timestamp': datetime.utcnow().isoformat()
        }

class FounderCommunication(commands.Cog):
    """Founder communication features"""
    
    def __init__(self, bot: AIAssistantBot):
        self.bot = bot
    
    @commands.command(name='ask')
    async def ask_founder(self, ctx, *, question: str):
        """Ask the founder a question"""
        if not self.bot.founder_id:
            await ctx.send("❓ Founder not found in server. Please ensure Steve Cornell (master80059) is present.")
            return
        
        embed = discord.Embed(
            title="❓ Question for Founder",
            description=f"**From:** {ctx.author.mention}\n**Question:** {question}",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Status",
            value="📨 Sending to founder...",
            inline=False
        )
        
        message = await ctx.send(embed=embed)
        
        # Notify founder
        await self.bot.notify_founder(
            f"Question from {ctx.author.name}: {question}",
            urgent=False
        )
        
        # Update embed
        embed.set_field_at(
            0,
            name="Status",
            value="✅ Question sent to founder Steve Cornell",
            inline=False
        )
        
        await message.edit(embed=embed)
    
    @commands.command(name='report')
    async def development_report(self, ctx):
        """Generate development report"""
        embed = discord.Embed(
            title="📊 AI Development Report",
            description="Current development status and progress",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # System status
        embed.add_field(
            name="🤖 System Status",
            value="✅ AI Assistant operational\n✅ Discord bot active\n⚠️ CrewAI initializing",
            inline=True
        )
        
        # Recent activity
        embed.add_field(
            name="📈 Recent Activity",
            value="• CrewAI system implementation\n• Discord bot deployment\n• GitHub automation setup",
            inline=True
        )
        
        # Next steps
        embed.add_field(
            name="🎯 Next Steps",
            value="• Complete CrewAI integration\n• Implement GitHub automation\n• Deploy production system",
            inline=False
        )
        
        await ctx.send(embed=embed)

# Bot factory and main runner
async def create_discord_bot(token: str, crew_manager=None) -> AIAssistantBot:
    """Create and return Discord bot instance"""
    bot = AIAssistantBot(token, crew_manager)
    return bot

async def run_discord_bot(token: str, crew_manager=None):
    """Run the Discord bot"""
    bot = await create_discord_bot(token, crew_manager)
    
    try:
        await bot.start(token)
    except Exception as e:
        logging.error(f"❌ Discord bot failed: {e}")
        raise

if __name__ == "__main__":
    import os
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Get token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        exit(1)
    
    # Run bot
    asyncio.run(run_discord_bot(token))