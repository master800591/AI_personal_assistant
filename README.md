# AI Personal Assistant

Autonomous AI Development Platform with Local Ollama Integration

## Overview

The AI Personal Assistant is a sophisticated autonomous development platform that leverages local Ollama models for real-time code analysis, improvement, and feature development. Built with Python and integrated with Discord for seamless communication.

## Features

### 🤖 Autonomous Development
- **Real-time Code Analysis**: Analyzes Python codebases for performance, security, and quality improvements
- **Automated Code Improvements**: Implements fixes and optimizations using local AI models
- **Feature Generation**: Creates new utility modules and enhancements automatically
- **Continuous Integration**: Monitors and improves codebase continuously

### 🧠 Local AI Integration  
- **Ollama Toolkit**: Comprehensive wrapper for Ollama models
- **Multiple Model Support**: Works with deepseek-r1, stable-code, codellama, phi3.5, and more
- **No External APIs**: Everything runs locally for privacy and speed
- **Async Support**: Full async/await support for high-performance operations

### 💬 Discord Integration
- **Real-time Notifications**: Development updates sent to Discord channels
- **Command Interface**: Control AI operations through Discord commands
- **Status Monitoring**: Live status updates and logging

### 🛠️ Developer Tools
- **GitHub Integration**: Automatic repository management and updates
- **Performance Monitoring**: System health checks and metrics
- **Backup Systems**: Automatic code backups before modifications
- **Logging**: Comprehensive logging for all operations

## Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Git configured
- Discord bot token (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/master800591/AI_personal_assistant.git
cd AI_personal_assistant

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Configuration

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Configure your settings:**
```env
# Discord (Optional)
DISCORD_BOT_TOKEN=your_discord_token_here

# GitHub Integration
GITHUB_TOKEN=your_github_token_here

# AI Corporation Settings
AI_CORP_FOUNDER=Your Name
AI_CORP_MISSION=Autonomous AI Development
```

3. **Start Ollama:**
```bash
ollama serve
```

### Usage

#### Start Autonomous Development
```bash
# Using entry point
ai-dev

# Or direct execution
python -m ai_assistant.autonomous.developer
```

#### Run Discord Bot
```bash
# Using entry point
ai-discord

# Or direct execution  
python -m ai_assistant.discord.bot
```

#### Main Assistant Interface
```bash
# Using entry point
ai-assistant

# Or direct execution
python -m ai_assistant.main
```

## Project Structure

```
ai_personal_assistant/
├── src/
│   └── ai_assistant/
│       ├── __init__.py
│       ├── main.py                 # Main entry point
│       ├── autonomous/             # Autonomous development
│       │   ├── __init__.py
│       │   ├── developer.py        # Core autonomous developer
│       │   ├── analyzer.py         # Code analysis
│       │   └── generator.py        # Feature generation
│       ├── ollama/                 # Ollama integration
│       │   ├── __init__.py
│       │   ├── toolkit.py          # Ollama toolkit
│       │   └── models.py           # Model management
│       ├── discord/                # Discord integration
│       │   ├── __init__.py
│       │   ├── bot.py              # Discord bot
│       │   └── commands.py         # Bot commands
│       ├── github/                 # GitHub integration
│       │   ├── __init__.py
│       │   └── manager.py          # Repository management
│       └── utils/                  # Utilities
│           ├── __init__.py
│           ├── logging.py          # Logging configuration
│           ├── config.py           # Configuration management
│           └── helpers.py          # Helper functions
├── tests/                          # Test suite
├── docs/                           # Documentation
├── scripts/                        # Utility scripts
├── config/                         # Configuration files
├── logs/                           # Log files
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Dependencies
├── setup.py                        # Package setup
└── README.md                       # This file
```

## Development

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/
```

### Adding New Features

1. **Create feature module** in appropriate package
2. **Add tests** in `tests/` directory
3. **Update configuration** if needed
4. **Document** in relevant README sections

### Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Configuration

### Ollama Models

Supported models:
- **deepseek-r1**: Advanced reasoning and analysis
- **stable-code**: Code generation and optimization  
- **codellama**: Code understanding and refactoring
- **phi3.5**: Lightweight general purpose
- **dolphin3**: Conversational AI
- **llava**: Multimodal capabilities

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Discord bot authentication | No |
| `GITHUB_TOKEN` | GitHub API access | Yes |
| `AI_CORP_FOUNDER` | Your name/identifier | Yes |
| `AI_CORP_MISSION` | Mission statement | No |
| `OLLAMA_HOST` | Ollama server URL | No (default: localhost:11434) |

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check port availability: `netstat -an | findstr 11434`

2. **Discord Bot Not Responding**
   - Verify bot token in `.env`
   - Check bot permissions in Discord server
   - Ensure bot is invited to server

3. **GitHub Integration Issues**  
   - Verify GitHub token has proper permissions
   - Check repository access rights

### Logging

Logs are stored in `logs/` directory:
- `ai_assistant.log`: Main application logs
- `discord_bot.log`: Discord bot specific logs
- `autonomous_dev.log`: Autonomous development logs

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/master800591/AI_personal_assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/master800591/AI_personal_assistant/discussions)
- **Wiki**: [Project Wiki](https://github.com/master800591/AI_personal_assistant/wiki)

## Roadmap

- [ ] Web interface for monitoring
- [ ] Plugin system for extensions
- [ ] Multi-language support beyond Python
- [ ] Advanced AI model fine-tuning
- [ ] Team collaboration features
- [ ] Cloud deployment options

---

**Built with ❤️ by the AI Corporation team**