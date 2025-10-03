# Ollama Model Manager

A comprehensive tool to discover, search, and automatically pull models from [https://ollama.com/search](https://ollama.com/search).

## 🚀 Quick Start

The easiest way to get started is with the interactive tool:

```bash
python quick_ollama_setup.py
```

This will give you a friendly menu to:
- 🔥 Discover popular models
- 🔍 Search for specific models  
- 🎯 Get recommendations by category
- 📥 Pull specific models

## 📋 Tools Included

### 1. **Quick Interactive Setup** (`quick_ollama_setup.py`)
**Perfect for beginners** - Interactive menu-driven interface

```bash
python quick_ollama_setup.py
```

Features:
- Discover popular models
- Search by keywords
- Category-based recommendations  
- Easy model installation

### 2. **Command Line Interface** (`ollama_discover.py`)
**Perfect for power users** - Full CLI with all options

```bash
# Discover popular models
python ollama_discover.py discover --popular --limit 10

# Search for specific models
python ollama_discover.py search "embedding" --pull

# Get recommendations by category
python ollama_discover.py recommend --category code --pull

# Pull specific models
python ollama_discover.py pull --models llama3.2 gemma2 phi3

# Pull popular models automatically
python ollama_discover.py pull --popular --limit 5 --yes
```

### 3. **Core Library** (`ollama_model_manager.py`)
**Perfect for developers** - Python library for custom scripts

```python
from ollama_model_manager import OllamaModelManager

manager = OllamaModelManager()

# Discover popular models
popular = manager.get_popular_models(limit=10)

# Search for models
models = manager.search_models("embedding", page_limit=3)

# Pull models
results = manager.pull_models_batch(['llama3.2', 'gemma2'])
```

## 🎯 Use Cases

### Scenario 1: New User Setup
```bash
# Interactive setup for beginners
python quick_ollama_setup.py
```
- Choose "Discover popular models"
- Select "Install top 3 popular models"
- Wait for download to complete

### Scenario 2: Find Embedding Models
```bash
# Search and install embedding models
python ollama_discover.py search "embedding" --pull
```

### Scenario 3: Get Code Models
```bash
# Get code-focused recommendations
python ollama_discover.py recommend --category code --pull
```

### Scenario 4: Bulk Install Popular Models
```bash
# Install top 5 popular models automatically
python ollama_discover.py pull --popular --limit 5 --yes
```

### Scenario 5: Custom Script Integration
```python
from ollama_model_manager import OllamaModelManager

# Create custom model discovery script
manager = OllamaModelManager()

# Get all embedding models
embedding_models = manager.search_models("embedding")
filtered = manager.filter_models(embedding_models, min_pulls=1000)

# Install best embedding models
best_embedding = [m.name for m in filtered[:3]]
manager.pull_models_batch(best_embedding)
```

## 📖 CLI Reference

### Discovery Commands

```bash
# Discover popular models
python ollama_discover.py discover --popular --limit 20

# Search with query
python ollama_discover.py discover --query "vision" --pages 3

# Filter by category
python ollama_discover.py discover --category embedding

# Exclude already installed models
python ollama_discover.py discover --popular --exclude-local

# Save results to file
python ollama_discover.py discover --popular --output models.json
```

### Pull Commands

```bash
# Pull specific models
python ollama_discover.py pull --models llama3.2 gemma2 phi3

# Pull from saved file
python ollama_discover.py pull --file models.json --limit 5

# Pull popular models
python ollama_discover.py pull --popular --limit 3

# Parallel downloads
python ollama_discover.py pull --popular --parallel --workers 3

# Auto-confirm (no prompts)
python ollama_discover.py pull --popular --yes --quiet
```

### Search Commands

```bash
# Search for models
python ollama_discover.py search "code" --pages 2

# Search and offer to install
python ollama_discover.py search "vision" --pull

# Filter by category
python ollama_discover.py search "llama" --category instruct
```

### List Commands

```bash
# List installed models
python ollama_discover.py list

# Show detailed information
python ollama_discover.py list --details
```

### Recommendation Commands

```bash
# Get all category recommendations
python ollama_discover.py recommend

# Specific category
python ollama_discover.py recommend --category embedding

# Offer to install recommendations
python ollama_discover.py recommend --pull --pull-count 2
```

## 🔧 Library API

### Basic Usage

```python
from ollama_model_manager import OllamaModelManager

manager = OllamaModelManager()
```

### Model Discovery

```python
# Search models
models = manager.search_models("embedding", page_limit=3)
popular = manager.get_popular_models(limit=20)
category_models = manager.search_by_category("code")

# Get recommendations
recommendations = manager.discover_recommended_models()
```

### Model Management

```python
# Get local models
local = manager.get_local_models()

# Pull models
success = manager.pull_model("llama3.2", show_progress=True)
results = manager.pull_models_batch(["gemma2", "phi3"], max_workers=2)
```

### Model Information

```python
# Get detailed model info
details = manager.get_model_details("llama3.2")

# Filter models
filtered = manager.filter_models(
    models, 
    min_pulls=1000,
    exclude_local=True,
    size_filter="small"
)
```

### Data Persistence

```python
# Save/load model lists
manager.save_model_list(models, "my_models.json")
loaded_models = manager.load_model_list("my_models.json")
```

## 🎭 Model Categories

The tool automatically categorizes models:

- **General**: llama, gemma, phi, qwen (general purpose chat)
- **Code**: codellama, codeqwen, starcoder (code generation)
- **Embedding**: nomic-embed, mxbai-embed (text embeddings)
- **Vision**: llava, bakllava, moondream (image understanding)
- **Chat**: orca, vicuna, solar (conversational)
- **Instruct**: mixtral, wizard, dolphin (instruction following)

## 🚦 Model Filtering

Filter models by various criteria:

```python
filtered = manager.filter_models(
    models,
    min_pulls=1000,        # Minimum download count
    categories=["code"],    # Specific categories
    exclude_local=True,     # Skip installed models
    size_filter="small"     # Size preference
)
```

Size filters:
- `"small"`: < 1GB models
- `"medium"`: 1-10GB models  
- `"large"`: > 10GB models

## 🔍 Search Capabilities

The tool searches https://ollama.com/search and extracts:

- Model names and descriptions
- Download counts (popularity)
- Model sizes
- Tags and categories
- Direct links to model pages

## ⚡ Performance Features

- **Parallel Downloads**: Download multiple models simultaneously
- **Progress Tracking**: Real-time download progress
- **Caching**: Save discovered models to avoid re-searching
- **Filtering**: Smart filtering to avoid duplicate downloads
- **Batch Operations**: Efficient bulk operations

## 🛠️ Requirements

- Python 3.8+
- `requests` library for web scraping
- `ollama` CLI tool installed and running
- Internet connection for model discovery

## 📝 Examples

### Example 1: Setup for AI Development
```python
# Get best models for AI development
manager = OllamaModelManager()

# Get general purpose models
general = manager.search_models("llama", page_limit=2)
general_filtered = manager.filter_models(general, min_pulls=5000)[:2]

# Get embedding models  
embedding = manager.search_models("embedding", page_limit=2)
embedding_filtered = manager.filter_models(embedding, min_pulls=1000)[:1]

# Get code models
code = manager.search_models("code", page_limit=2) 
code_filtered = manager.filter_models(code, min_pulls=1000)[:1]

# Install all
all_models = [m.name for m in general_filtered + embedding_filtered + code_filtered]
manager.pull_models_batch(all_models)
```

### Example 2: Automated Model Updates
```python
# Discover and install latest popular models
manager = OllamaModelManager()

# Get current popular models
popular = manager.get_popular_models(limit=10)

# Filter out already installed
new_models = manager.filter_models(popular, exclude_local=True, min_pulls=2000)

# Install top 3 new popular models
if new_models:
    to_install = [m.name for m in new_models[:3]]
    print(f"Installing new popular models: {to_install}")
    manager.pull_models_batch(to_install)
```

### Example 3: Category-Specific Setup
```python
# Setup for specific use case
manager = OllamaModelManager()

use_cases = {
    'data_science': ['embedding', 'instruct'],
    'content_creation': ['general', 'chat'], 
    'development': ['code', 'instruct'],
    'research': ['general', 'vision']
}

use_case = 'data_science'
categories = use_cases[use_case]

models_to_install = []
for category in categories:
    models = manager.search_models(category, page_limit=2)
    filtered = manager.filter_models(models, min_pulls=1000)
    models_to_install.extend([m.name for m in filtered[:2]])

# Remove duplicates and install
unique_models = list(set(models_to_install))
manager.pull_models_batch(unique_models)
```

## 🎯 Tips & Best Practices

1. **Start Small**: Begin with popular, smaller models
2. **Check Space**: Large models can be 4GB+ each
3. **Use Filters**: Filter by download count to get quality models
4. **Save Lists**: Save discovered models to avoid re-searching
5. **Parallel Downloads**: Use parallel downloads for multiple models
6. **Regular Updates**: Popular models change, re-run discovery periodically

## 🚨 Troubleshooting

### Common Issues

**No models found**:
- Check internet connection
- Verify https://ollama.com is accessible
- Try different search terms

**Download failures**:
- Check Ollama is running (`ollama serve`)
- Verify disk space
- Check model name spelling

**Slow downloads**:
- Use parallel downloads sparingly (max 3 workers)
- Check network bandwidth
- Try during off-peak hours

### Debug Mode

Enable verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This tool makes it incredibly easy to discover and install the best Ollama models for your needs! 🦙✨