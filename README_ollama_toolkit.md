# Ollama Toolkit

A comprehensive Python wrapper for the [ollama-python](https://github.com/ollama/ollama-python) library that provides easy-to-use functions and classes for all Ollama features.

## Features

- **Easy-to-use API**: Simple functions for common tasks
- **Comprehensive Coverage**: Wraps all Ollama functionality
- **Async Support**: Full async/await support for all operations
- **Tool/Function Calling**: Built-in support for function calling with automatic execution
- **Conversation Management**: Maintain chat history and context
- **Model Management**: Pull, push, create, delete, and manage models
- **Embeddings**: Generate embeddings with batch processing
- **Web Search**: Search and fetch web content (requires API key)
- **Streaming Support**: Real-time streaming responses
- **Error Handling**: Robust error handling and validation

## Installation

First, make sure you have [Ollama](https://ollama.com/download) installed and running.

```bash
# Install Ollama (if not already installed)
# Download from https://ollama.com/download

# Install the ollama Python package
pip install ollama

# Pull some models
ollama pull llama3.2
ollama pull gemma2
ollama pull nomic-embed-text  # for embeddings
```

Then copy the `ollama_toolkit.py` file to your project directory.

## Quick Start

```python
from ollama_toolkit import OllamaToolkit, quick_chat, list_available_models

# Check available models
models = list_available_models()
print("Available models:", models)

# Quick chat
response = quick_chat('llama3.2', 'What is Python?')
print(response)

# Initialize toolkit for advanced usage
toolkit = OllamaToolkit()
```

## Basic Usage Examples

### 1. Simple Chat

```python
from ollama_toolkit import OllamaToolkit

toolkit = OllamaToolkit()

messages = [
    {'role': 'user', 'content': 'Explain quantum computing in simple terms.'}
]

response = toolkit.chat('llama3.2', messages)
print(response.message.content)
```

### 2. Conversation Management

```python
from ollama_toolkit import OllamaConversation, OllamaToolkit

toolkit = OllamaToolkit()
conversation = OllamaConversation(
    toolkit, 
    'llama3.2', 
    system_prompt='You are a helpful coding assistant.'
)

# Multiple exchanges with maintained context
response1 = conversation.chat('How do I create a list in Python?')
response2 = conversation.chat('How do I add items to it?')
response3 = conversation.chat('What about removing items?')

# Save conversation
conversation.save_conversation('my_chat.json')
```

### 3. Function/Tool Calling

```python
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny, 22°C"

def calculate(operation: str, a: float, b: float) -> float:
    """Perform mathematical operations."""
    if operation == 'add':
        return a + b
    elif operation == 'multiply':
        return a * b
    return 0

# Set up tools
tools = [get_weather, calculate]
functions = {
    'get_weather': get_weather,
    'calculate': calculate
}

messages = [
    {'role': 'user', 'content': 'What is the weather in Paris and what is 15 * 7?'}
]

response = toolkit.chat_with_tools('llama3.2', messages, tools, functions)
print(response.message.content)
```

### 4. Embeddings

```python
# Single text embedding
embedding = toolkit.embed('nomic-embed-text', 'Hello, world!')
print(f"Embedding dimensions: {len(embedding.embeddings[0])}")

# Batch embeddings
texts = [
    "The cat sat on the mat",
    "Dogs are loyal animals", 
    "Python is a programming language"
]

embeddings = toolkit.embed_batch('nomic-embed-text', texts, batch_size=2)
print(f"Generated {len(embeddings)} embeddings")
```

### 5. Streaming Responses

```python
# Streaming chat
messages = [{'role': 'user', 'content': 'Tell me a story about AI.'}]

print("AI Story: ")
for chunk in toolkit.chat('llama3.2', messages, stream=True):
    if chunk.message.content:
        print(chunk.message.content, end='', flush=True)
print()  # New line
```

### 6. Model Management

```python
# List models
models = toolkit.list_models()
for model in models.models:
    print(f"Model: {model.model}, Size: {model.size}")

# Show model details
details = toolkit.show_model('llama3.2')
print(f"Template: {details.template}")
print(f"Parameters: {details.parameters}")

# Pull a new model
for progress in toolkit.pull_model('gemma2', stream=True):
    print(f"Status: {progress.status}")

# Create a custom model
response = toolkit.create_model(
    'my-assistant',
    from_='llama3.2',
    system='You are a helpful coding assistant specialized in Python.'
)
```

## Advanced Usage

### Async Operations

```python
import asyncio
from ollama_toolkit import OllamaToolkit

async def async_example():
    toolkit = OllamaToolkit()
    
    # Async chat
    messages = [{'role': 'user', 'content': 'What is async programming?'}]
    response = await toolkit.chat_async('llama3.2', messages)
    print(response.message.content)
    
    # Concurrent requests
    tasks = [
        toolkit.chat_async('llama3.2', [{'role': 'user', 'content': 'What is AI?'}]),
        toolkit.chat_async('llama3.2', [{'role': 'user', 'content': 'What is ML?'}]),
        toolkit.chat_async('llama3.2', [{'role': 'user', 'content': 'What is DL?'}])
    ]
    
    responses = await asyncio.gather(*tasks)
    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response.message.content}")

# Run async example
asyncio.run(async_example())
```

### Structured Output (JSON)

```python
messages = [
    {
        'role': 'user',
        'content': 'Generate a person profile with name, age, and occupation in JSON format.'
    }
]

response = toolkit.chat('llama3.2', messages, format='json')
print(response.message.content)

# Parse JSON response
import json
try:
    data = json.loads(response.message.content)
    print(f"Name: {data.get('name')}")
    print(f"Age: {data.get('age')}")
    print(f"Occupation: {data.get('occupation')}")
except json.JSONDecodeError:
    print("Response is not valid JSON")
```

### Custom Model Options

```python
options = {
    'temperature': 0.7,    # Creativity level (0.0 to 1.0)
    'top_p': 0.9,          # Nucleus sampling
    'top_k': 40,           # Top-k sampling
    'repeat_penalty': 1.1, # Repetition penalty
    'max_tokens': 150      # Maximum response length
}

response = toolkit.generate(
    'llama3.2',
    'Write a creative short story about time travel',
    options=options
)
print(response.response)
```

### Multimodal (Image) Support

```python
from pathlib import Path

# Chat with image
messages = [
    {
        'role': 'user',
        'content': 'What do you see in this image?',
        'images': [Path('path/to/image.jpg')]
    }
]

response = toolkit.chat('llama3.2-vision', messages)
print(response.message.content)

# Generate with image
response = toolkit.generate(
    'llama3.2-vision',
    'Describe this image in detail',
    images=['path/to/image.jpg']
)
print(response.response)
```

### Web Search (Requires API Key)

```python
# Initialize with API key
toolkit = OllamaToolkit(
    headers={'Authorization': 'Bearer YOUR_OLLAMA_API_KEY'}
)

# Search the web
results = toolkit.web_search('latest AI developments', max_results=5)
for result in results.results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Snippet: {result.content}")
    print("---")

# Fetch web page content
content = toolkit.web_fetch('https://example.com')
print(f"Page title: {content.title}")
print(f"Content length: {len(content.content)}")
```

## Convenience Functions

For quick operations, use the convenience functions:

```python
from ollama_toolkit import (
    quick_chat, quick_generate, quick_embed,
    list_available_models, model_exists
)

# Quick operations
response = quick_chat('llama3.2', 'Hello!')
text = quick_generate('llama3.2', 'The future of AI is')
embedding = quick_embed('nomic-embed-text', 'Hello world')

# Model utilities
models = list_available_models()
exists = model_exists('llama3.2')
```

## Error Handling

```python
try:
    response = toolkit.chat('nonexistent-model', messages)
except Exception as e:
    print(f"Error: {e}")
    
    # Try to pull the model if it doesn't exist
    if 'not found' in str(e).lower():
        print("Pulling model...")
        toolkit.pull_model('llama3.2')
```

## Configuration

### Custom Host

```python
# Connect to remote Ollama instance
toolkit = OllamaToolkit(host='http://remote-server:11434')
```

### Custom Headers

```python
# Add custom headers (e.g., for authentication)
toolkit = OllamaToolkit(
    headers={
        'Authorization': 'Bearer your-token',
        'X-Custom-Header': 'value'
    }
)
```

### Timeout Configuration

```python
toolkit = OllamaToolkit(timeout=60.0)  # 60 seconds timeout
```

## Best Practices

1. **Model Availability**: Always check if models are available before using them
2. **Error Handling**: Wrap API calls in try-except blocks
3. **Resource Management**: Use appropriate batch sizes for embeddings
4. **Streaming**: Use streaming for long responses to improve user experience
5. **System Prompts**: Use system prompts to set consistent behavior
6. **Temperature**: Adjust temperature based on use case (lower for factual, higher for creative)

## Examples

Run the comprehensive examples:

```python
python ollama_examples.py
```

This will demonstrate all features of the toolkit with working examples.

## API Reference

### OllamaToolkit Class

Main class providing all Ollama functionality.

#### Methods

- `chat()` - Chat with a model
- `chat_async()` - Async chat
- `chat_with_tools()` - Chat with automatic tool execution
- `generate()` - Generate text
- `generate_async()` - Async generation
- `embed()` - Generate embeddings
- `embed_async()` - Async embeddings
- `embed_batch()` - Batch embeddings
- `list_models()` - List available models
- `show_model()` - Show model details
- `pull_model()` - Pull a model
- `push_model()` - Push a model
- `create_model()` - Create custom model
- `delete_model()` - Delete a model
- `copy_model()` - Copy a model
- `ps()` - Show running models
- `web_search()` - Search the web
- `web_fetch()` - Fetch web content

### OllamaConversation Class

Manages conversation history and context.

#### Methods

- `chat()` - Send message and get response
- `add_message()` - Add message to history
- `clear_history()` - Clear conversation history
- `get_history()` - Get conversation history
- `save_conversation()` - Save to file
- `load_conversation()` - Load from file

### Convenience Functions

- `quick_chat()` - Quick chat function
- `quick_generate()` - Quick generation
- `quick_embed()` - Quick embedding
- `list_available_models()` - List model names
- `model_exists()` - Check if model exists

## License

This toolkit is designed to work with the [ollama-python](https://github.com/ollama/ollama-python) library, which is licensed under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!