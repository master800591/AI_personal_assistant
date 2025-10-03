# Ollama Model Management - Remove Functionality

## Overview

The Ollama Model Management tools now include comprehensive model removal capabilities through multiple interfaces:

1. **Command Line Interface (CLI)**
2. **Interactive Setup Tool**
3. **Direct Python API**

## 🗑️ Removal Methods

### 1. Command Line Interface

#### Remove Specific Models
```bash
# Remove single model
python3.11 ollama_discover.py remove --models llama3.2

# Remove multiple models
python3.11 ollama_discover.py remove --models llama3.2 gemma2 phi3

# Remove with parallel processing
python3.11 ollama_discover.py remove --models llama3.2 gemma2 --parallel --workers 2

# Auto-confirm without prompts
python3.11 ollama_discover.py remove --models llama3.2 --yes

# Quiet removal (suppress progress)
python3.11 ollama_discover.py remove --models llama3.2 --quiet
```

#### Remove All Models
```bash
# Remove all models with confirmation
python3.11 ollama_discover.py remove --all

# Remove all models without confirmation (dangerous!)
python3.11 ollama_discover.py remove --all --yes
```

#### Interactive Removal
```bash
# Interactive menu for model selection
python3.11 ollama_discover.py remove
```

### 2. Interactive Setup Tool

Run the interactive tool:
```bash
python3.11 quick_ollama_setup.py
```

Then select option 5 (Remove models) for:
- **Remove specific models**: Choose individual models from a numbered list
- **Remove ALL models**: Remove all installed models with safety confirmation
- **Cancel**: Exit without removing anything

### 3. Enhanced Batch Launcher

Run the Windows batch launcher:
```bash
run_ollama_tools_enhanced.bat
```

Select option 6 (Remove Models) for a submenu with:
1. Remove specific models (enter space-separated names)
2. Remove ALL models (requires typing "YES" for confirmation)
3. Interactive removal (numbered selection)

### 4. Direct Python API

```python
from ollama_model_manager import OllamaModelManager

manager = OllamaModelManager()

# Remove single model
success = manager.remove_model("llama3.2")

# Remove multiple models in batch
results = manager.remove_models_batch(["llama3.2", "gemma2"], show_progress=True)

# Remove all models
results = manager.remove_all_models(confirm=True)

# Get list of local models first
local_models = manager.get_local_models()
print(f"Found {len(local_models)} models: {local_models}")
```

## 🛡️ Safety Features

### Confirmation Prompts
- **Single/Multiple Models**: Asks for confirmation before removal
- **Remove All**: Requires typing "yes" or "YES" depending on interface
- **Model Validation**: Checks if models exist locally before attempting removal

### Error Handling
- **Non-existent Models**: Reports which models are not found locally
- **Failed Removals**: Reports which models failed to remove and why
- **Graceful Degradation**: Continues with successful removals even if some fail

### Progress Tracking
- **Real-time Progress**: Shows removal progress for each model
- **Success Summary**: Reports how many models were successfully removed
- **Failure Details**: Lists specific models that failed to remove

## 📊 Usage Examples

### Example 1: Clean up old models
```bash
# List current models
python3.11 ollama_discover.py list --details

# Remove specific outdated models
python3.11 ollama_discover.py remove --models old_model1 old_model2 --yes
```

### Example 2: Fresh start (remove everything)
```bash
# Remove all models for a fresh start
python3.11 ollama_discover.py remove --all

# Confirm with "yes" when prompted
```

### Example 3: Interactive cleanup
```bash
# Start interactive removal
python3.11 ollama_discover.py remove

# Select models by numbers: 1,3,5
# Confirm removal when prompted
```

### Example 4: Batch removal with error handling
```python
from ollama_model_manager import OllamaModelManager

manager = OllamaModelManager()

# Models to remove (some may not exist)
models_to_remove = ["llama3.2", "nonexistent", "gemma2"]

# Remove with error handling
results = manager.remove_models_batch(models_to_remove)

# Check results
for model, success in results.items():
    if success:
        print(f"✅ Removed: {model}")
    else:
        print(f"❌ Failed: {model}")
```

## ⚡ Performance Options

### Parallel Removal
```bash
# Remove multiple models in parallel (faster)
python3.11 ollama_discover.py remove --models model1 model2 model3 --parallel --workers 3
```

### Quiet Mode
```bash
# Remove without progress output (useful for scripts)
python3.11 ollama_discover.py remove --models model1 --quiet --yes
```

## 🔧 Advanced Features

### Batch Operations
- **Parallel Processing**: Remove multiple models simultaneously
- **Worker Control**: Specify number of parallel workers
- **Progress Monitoring**: Real-time feedback on removal status

### Validation
- **Local Model Check**: Verifies models exist before attempting removal
- **Size Information**: Shows model sizes where available
- **Dependency Check**: (Future feature) Check for model dependencies

### Integration
- **CLI Integration**: Works seamlessly with existing discovery commands
- **API Consistency**: Same interface patterns as pull/install operations
- **Error Consistency**: Standard error reporting across all operations

## 🚨 Important Notes

1. **Irreversible**: Model removal cannot be undone - models must be re-downloaded
2. **Storage Space**: Removing large models frees up significant disk space
3. **Network Usage**: Re-downloading removed models uses bandwidth
4. **Confirmation Required**: Safety prompts prevent accidental deletions
5. **Parallel Limits**: Use appropriate worker counts to avoid system overload

## 🔄 Integration with Other Commands

The remove functionality integrates seamlessly with other tools:

```bash
# Discover, then remove
python3.11 ollama_discover.py list --details
python3.11 ollama_discover.py remove --models unwanted_model

# Search and replace workflow
python3.11 ollama_discover.py search "better_model" --pull
python3.11 ollama_discover.py remove --models old_model

# Clean slate workflow
python3.11 ollama_discover.py remove --all --yes
python3.11 ollama_discover.py discover --popular --limit 5
```