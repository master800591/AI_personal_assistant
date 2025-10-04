"""
Ollama Toolkit Examples

This file demonstrates how to use all features of the Ollama Toolkit,
including chat, generation, embeddings, model management, tools, and more.
"""

import asyncio
import json
from typing import Dict, List
from ollama_toolkit import (
    OllamaToolkit, OllamaConversation,
    quick_chat, quick_generate, quick_embed,
    list_available_models, model_exists,
    create_function_tool, create_custom_tool
)


# =====================================
# TOOL FUNCTIONS FOR EXAMPLES
# =====================================

def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city (str): The name of the city
        
    Returns:
        str: Weather information
    """
    # Mock weather data
    weather_data = {
        'london': 'Cloudy, 15°C',
        'paris': 'Sunny, 22°C',
        'new york': 'Rainy, 18°C',
        'tokyo': 'Partly cloudy, 25°C'
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")


def calculate_math(operation: str, a: float, b: float) -> float:
    """
    Perform mathematical operations.
    
    Args:
        operation (str): The operation to perform (add, subtract, multiply, divide)
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Result of the operation
    """
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else 0
    }
    return operations.get(operation.lower(), lambda x, y: 0)(a, b)


def search_knowledge_base(query: str) -> str:
    """
    Search a mock knowledge base.
    
    Args:
        query (str): Search query
        
    Returns:
        str: Search results
    """
    knowledge = {
        'python': 'Python is a high-level programming language known for its simplicity and readability.',
        'ai': 'Artificial Intelligence refers to the simulation of human intelligence in machines.',
        'ollama': 'Ollama is a platform for running large language models locally.'
    }
    
    for key, value in knowledge.items():
        if key.lower() in query.lower():
            return value
    return f"No information found for: {query}"


# =====================================
# BASIC USAGE EXAMPLES
# =====================================

def basic_examples():
    """Demonstrate basic usage of the toolkit."""
    print("=" * 50)
    print("BASIC USAGE EXAMPLES")
    print("=" * 50)
    
    # Initialize toolkit
    toolkit = OllamaToolkit()
    
    # List available models
    print("\n1. Available Models:")
    models = list_available_models()
    for i, model in enumerate(models[:5], 1):  # Show first 5 models
        print(f"   {i}. {model}")
    
    if not models:
        print("   No models available. Please pull a model first.")
        return
    
    # Use the first available model for examples
    model = models[0]
    print(f"\nUsing model: {model}")
    
    # Quick chat
    print("\n2. Quick Chat:")
    try:
        response = quick_chat(model, "What is machine learning in one sentence?")
        print(f"   Response: {response}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Quick generation
    print("\n3. Quick Generation:")
    try:
        response = quick_generate(model, "The future of AI is", options={'max_tokens': 50})
        print(f"   Generated: {response}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Model information
    print("\n4. Model Information:")
    try:
        info = toolkit.get_model_info(model)
        print(f"   Modified: {info.get('modified_at', 'Unknown')}")
        print(f"   Size: {info.get('size', 'Unknown')}")
        if info.get('details'):
            print(f"   Family: {info['details'].family}")
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# CHAT EXAMPLES
# =====================================

def chat_examples():
    """Demonstrate chat functionality."""
    print("\n" + "=" * 50)
    print("CHAT EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    models = list_available_models()
    
    if not models:
        print("No models available for chat examples.")
        return
    
    model = models[0]
    
    # Basic chat
    print("\n1. Basic Chat:")
    messages = [
        {'role': 'user', 'content': 'Explain quantum computing in simple terms.'}
    ]
    try:
        response = toolkit.chat(model, messages)
        print(f"   {response.message.content[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Chat with system prompt
    print("\n2. Chat with System Prompt:")
    messages = [
        {'role': 'system', 'content': 'You are a helpful coding assistant.'},
        {'role': 'user', 'content': 'How do I create a list in Python?'}
    ]
    try:
        response = toolkit.chat(model, messages)
        print(f"   {response.message.content[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Streaming chat
    print("\n3. Streaming Chat:")
    messages = [{'role': 'user', 'content': 'Count from 1 to 5.'}]
    try:
        print("   Streaming response: ", end="")
        for chunk in toolkit.chat(model, messages, stream=True):
            if chunk.message.content:
                print(chunk.message.content, end="", flush=True)
        print()  # New line after streaming
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# CONVERSATION EXAMPLES
# =====================================

def conversation_examples():
    """Demonstrate conversation management."""
    print("\n" + "=" * 50)
    print("CONVERSATION EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    models = list_available_models()
    
    if not models:
        print("No models available for conversation examples.")
        return
    
    model = models[0]
    
    # Create a conversation
    print("\n1. Conversation with History:")
    conversation = OllamaConversation(
        toolkit, 
        model, 
        system_prompt="You are a knowledgeable science teacher."
    )
    
    try:
        # Multiple exchanges
        response1 = conversation.chat("What is photosynthesis?")
        print(f"   Q: What is photosynthesis?")
        print(f"   A: {response1.message.content[:150]}...")
        
        response2 = conversation.chat("How does it relate to cellular respiration?")
        print(f"   Q: How does it relate to cellular respiration?")
        print(f"   A: {response2.message.content[:150]}...")
        
        # Show conversation history
        print(f"\n   Conversation has {len(conversation.get_history())} messages")
        
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# TOOL/FUNCTION CALLING EXAMPLES
# =====================================

def tool_examples():
    """Demonstrate tool and function calling."""
    print("\n" + "=" * 50)
    print("TOOL/FUNCTION CALLING EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    models = list_available_models()
    
    if not models:
        print("No models available for tool examples.")
        return
    
    model = models[0]
    
    # Function calling with automatic execution
    print("\n1. Automatic Tool Execution:")
    tools = [get_weather, calculate_math, search_knowledge_base]
    available_functions = {
        'get_weather': get_weather,
        'calculate_math': calculate_math,
        'search_knowledge_base': search_knowledge_base
    }
    
    messages = [
        {'role': 'user', 'content': 'What is the weather in London and what is 15 + 27?'}
    ]
    
    try:
        response = toolkit.chat_with_tools(
            model, messages, tools, available_functions
        )
        print(f"   Final response: {response.message.content}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Manual tool definition
    print("\n2. Custom Tool Definition:")
    custom_tool = create_custom_tool(
        name="get_time",
        description="Get the current time",
        parameters={
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone (e.g., UTC, EST)"
                }
            },
            "required": ["timezone"]
        }
    )
    print(f"   Custom tool created: {custom_tool['function']['name']}")


# =====================================
# EMBEDDING EXAMPLES
# =====================================

def embedding_examples():
    """Demonstrate embedding functionality."""
    print("\n" + "=" * 50)
    print("EMBEDDING EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    
    # Check for embedding models
    embedding_models = ['nomic-embed-text', 'mxbai-embed-large', 'all-minilm']
    available_embedding_model = None
    
    for model in embedding_models:
        if model_exists(model):
            available_embedding_model = model
            break
    
    if not available_embedding_model:
        print("No embedding models available. Try: ollama pull nomic-embed-text")
        return
    
    print(f"Using embedding model: {available_embedding_model}")
    
    # Single text embedding
    print("\n1. Single Text Embedding:")
    try:
        embedding = quick_embed(available_embedding_model, "Hello, world!")
        print(f"   Text: 'Hello, world!'")
        print(f"   Embedding dimensions: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Batch embedding
    print("\n2. Batch Embedding:")
    texts = [
        "The cat sat on the mat",
        "Dogs are loyal animals",
        "Python is a programming language",
        "Machine learning is fascinating"
    ]
    
    try:
        embeddings = toolkit.embed_batch(available_embedding_model, texts, batch_size=2)
        print(f"   Embedded {len(texts)} texts")
        print(f"   Each embedding has {len(embeddings[0])} dimensions")
        
        # Calculate similarity between first two texts
        import math
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            magnitude_a = math.sqrt(sum(x * x for x in a))
            magnitude_b = math.sqrt(sum(x * x for x in b))
            return dot_product / (magnitude_a * magnitude_b)
        
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        print(f"   Similarity between first two texts: {similarity:.4f}")
        
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# MODEL MANAGEMENT EXAMPLES
# =====================================

def model_management_examples():
    """Demonstrate model management functionality."""
    print("\n" + "=" * 50)
    print("MODEL MANAGEMENT EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    
    # List models with details
    print("\n1. Detailed Model Information:")
    try:
        models_response = toolkit.list_models()
        for i, model in enumerate(models_response.models[:3], 1):  # Show first 3
            print(f"   {i}. {model.model}")
            if model.size:
                size_mb = model.size / (1024 * 1024)  # Convert to MB
                print(f"      Size: {size_mb:.1f} MB")
            if model.modified_at:
                print(f"      Modified: {model.modified_at}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Show running processes
    print("\n2. Running Models:")
    try:
        ps_response = toolkit.ps()
        if ps_response.models:
            for model in ps_response.models:
                print(f"   - {model.model}")
                if hasattr(model, 'size_vram') and model.size_vram:
                    print(f"     VRAM: {model.size_vram}")
        else:
            print("   No models currently running")
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# ASYNC EXAMPLES
# =====================================

async def async_examples():
    """Demonstrate async functionality."""
    print("\n" + "=" * 50)
    print("ASYNC EXAMPLES")
    print("=" * 50)
    
    from ollama_toolkit import quick_chat_async, quick_generate_async
    
    models = list_available_models()
    if not models:
        print("No models available for async examples.")
        return
    
    model = models[0]
    
    # Async chat
    print("\n1. Async Chat:")
    try:
        response = await quick_chat_async(model, "What is async programming?")
        print(f"   Response: {response[:150]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Concurrent requests
    print("\n2. Concurrent Requests:")
    try:
        tasks = [
            quick_chat_async(model, "What is AI?"),
            quick_chat_async(model, "What is ML?"),
            quick_chat_async(model, "What is DL?")
        ]
        
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses, 1):
            print(f"   Response {i}: {response[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# WEB SEARCH EXAMPLES (Requires API Key)
# =====================================

def web_search_examples():
    """Demonstrate web search functionality (requires Ollama API key)."""
    print("\n" + "=" * 50)
    print("WEB SEARCH EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    
    print("Note: Web search requires an Ollama API key.")
    print("Set OLLAMA_API_KEY environment variable or use:")
    print("toolkit = OllamaToolkit(headers={'Authorization': 'Bearer YOUR_API_KEY'})")
    
    # These examples will only work with proper API key
    try:
        # Web search
        print("\n1. Web Search:")
        results = toolkit.web_search("latest AI developments", max_results=2)
        print(f"   Found {len(results.results)} results")
        for result in results.results[:2]:
            print(f"   - {result.title}")
            print(f"     {result.url}")
    except Exception as e:
        print(f"   Error (expected without API key): {type(e).__name__}")
    
    try:
        # Web fetch
        print("\n2. Web Fetch:")
        content = toolkit.web_fetch("https://example.com")
        print(f"   Fetched content length: {len(content.content) if content.content else 0}")
    except Exception as e:
        print(f"   Error (expected without API key): {type(e).__name__}")


# =====================================
# ADVANCED EXAMPLES
# =====================================

def advanced_examples():
    """Demonstrate advanced usage patterns."""
    print("\n" + "=" * 50)
    print("ADVANCED EXAMPLES")
    print("=" * 50)
    
    toolkit = OllamaToolkit()
    models = list_available_models()
    
    if not models:
        print("No models available for advanced examples.")
        return
    
    model = models[0]
    
    # Structured output with JSON format
    print("\n1. Structured JSON Output:")
    try:
        messages = [
            {
                'role': 'user', 
                'content': 'Generate a person profile with name, age, and occupation in JSON format.'
            }
        ]
        response = toolkit.chat(model, messages, format='json')
        print(f"   JSON Response: {response.message.content}")
        
        # Try to parse the JSON
        try:
            data = json.loads(response.message.content)
            print(f"   Parsed successfully: {type(data)}")
        except json.JSONDecodeError:
            print("   Response is not valid JSON")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Custom options
    print("\n2. Custom Model Options:")
    try:
        options = {
            'temperature': 0.1,  # Low temperature for more deterministic output
            'top_p': 0.9,
            'max_tokens': 100
        }
        
        response = toolkit.generate(
            model, 
            "Write a haiku about programming",
            options=options
        )
        print(f"   Haiku: {response.response}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Stream processing
    print("\n3. Stream Processing:")
    try:
        stream_response = toolkit.generate(
            model, 
            "List the first 5 prime numbers",
            stream=True
        )
        
        # Process stream and collect text
        complete_text = toolkit.stream_to_text(stream_response)
        print(f"   Complete response: {complete_text}")
        
    except Exception as e:
        print(f"   Error: {e}")


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Run all examples."""
    print("OLLAMA TOOLKIT - COMPREHENSIVE EXAMPLES")
    print("=" * 60)
    
    # Check if any models are available
    if not list_available_models():
        print("\nNo models found. Please install Ollama and pull a model:")
        print("  ollama pull llama3.2")
        print("  ollama pull gemma2")
        print("  ollama pull nomic-embed-text  # for embeddings")
        return
    
    # Run synchronous examples
    basic_examples()
    chat_examples()
    conversation_examples()
    tool_examples()
    embedding_examples()
    model_management_examples()
    web_search_examples()
    advanced_examples()
    
    # Run async examples
    print("\nRunning async examples...")
    try:
        asyncio.run(async_examples())
    except Exception as e:
        print(f"Async examples failed: {e}")
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()