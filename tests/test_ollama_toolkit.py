"""
Simple test script for Ollama Toolkit

This script tests basic functionality of the Ollama Toolkit
to ensure everything is working correctly.
"""

import sys
from ollama_toolkit import (
    OllamaToolkit, 
    list_available_models, 
    model_exists, 
    quick_chat
)


def test_basic_functionality():
    """Test basic functionality of the toolkit."""
    print("Testing Ollama Toolkit...")
    print("=" * 40)
    
    # Test 1: List available models
    print("\n1. Testing model listing:")
    try:
        models = list_available_models()
        if models:
            print(f"   ✓ Found {len(models)} models:")
            for model in models[:3]:  # Show first 3
                print(f"     - {model}")
            test_model = models[0]
        else:
            print("   ✗ No models found!")
            print("     Please install a model: ollama pull llama3.2")
            return False
    except Exception as e:
        print(f"   ✗ Error listing models: {e}")
        return False
    
    # Test 2: Check model existence
    print(f"\n2. Testing model existence check:")
    try:
        exists = model_exists(test_model)
        print(f"   ✓ Model '{test_model}' exists: {exists}")
    except Exception as e:
        print(f"   ✗ Error checking model: {e}")
        return False
    
    # Test 3: Initialize toolkit
    print(f"\n3. Testing toolkit initialization:")
    try:
        toolkit = OllamaToolkit()
        print(f"   ✓ Toolkit initialized successfully")
        print(f"   ✓ Host: {toolkit.host}")
    except Exception as e:
        print(f"   ✗ Error initializing toolkit: {e}")
        return False
    
    # Test 4: Simple chat (if models are available)
    print(f"\n4. Testing simple chat:")
    try:
        response = quick_chat(test_model, "Hello! Respond with just 'Hi there!'")
        print(f"   ✓ Chat successful")
        print(f"   ✓ Response: {response[:50]}{'...' if len(response) > 50 else ''}")
    except Exception as e:
        print(f"   ✗ Error in chat: {e}")
        return False
    
    # Test 5: Model information
    print(f"\n5. Testing model information:")
    try:
        info = toolkit.get_model_info(test_model)
        if 'error' not in info:
            print(f"   ✓ Model info retrieved")
            print(f"   ✓ Modified: {info.get('modified_at', 'Unknown')}")
        else:
            print(f"   ! Model info error: {info['error']}")
    except Exception as e:
        print(f"   ✗ Error getting model info: {e}")
        return False
    
    # Test 6: List models with toolkit
    print(f"\n6. Testing detailed model listing:")
    try:
        models_response = toolkit.list_models()
        print(f"   ✓ Retrieved {len(models_response.models)} models via toolkit")
    except Exception as e:
        print(f"   ✗ Error listing models via toolkit: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("✓ All basic tests passed!")
    return True


def test_conversation():
    """Test conversation functionality."""
    print("\n" + "=" * 40)
    print("Testing Conversation Management...")
    print("=" * 40)
    
    models = list_available_models()
    if not models:
        print("No models available for conversation test")
        return False
    
    test_model = models[0]
    
    try:
        from ollama_toolkit import OllamaConversation
        
        toolkit = OllamaToolkit()
        conversation = OllamaConversation(
            toolkit, 
            test_model, 
            system_prompt="You are a helpful assistant. Keep responses brief."
        )
        
        # Test conversation
        print(f"\n1. Testing conversation with {test_model}:")
        response1 = conversation.chat("What is 2+2? Answer with just the number.")
        print(f"   ✓ First response: {response1.message.content.strip()}")
        
        response2 = conversation.chat("What did I just ask you?")
        print(f"   ✓ Second response: {response2.message.content[:50]}...")
        
        # Check history
        history = conversation.get_history()
        print(f"   ✓ Conversation has {len(history)} messages")
        
        print("✓ Conversation test passed!")
        return True
        
    except Exception as e:
        print(f"   ✗ Conversation test failed: {e}")
        return False


def test_embeddings():
    """Test embedding functionality."""
    print("\n" + "=" * 40)
    print("Testing Embeddings...")
    print("=" * 40)
    
    # Check for embedding models
    embedding_models = ['nomic-embed-text', 'mxbai-embed-large', 'all-minilm']
    available_model = None
    
    for model in embedding_models:
        if model_exists(model):
            available_model = model
            break
    
    if not available_model:
        print("No embedding models found. Try: ollama pull nomic-embed-text")
        return False
    
    try:
        from ollama_toolkit import quick_embed
        
        print(f"Using embedding model: {available_model}")
        
        # Test single embedding
        embedding = quick_embed(available_model, "Hello, world!")
        print(f"   ✓ Single embedding generated: {len(embedding)} dimensions")
        
        # Test batch embedding
        toolkit = OllamaToolkit()
        texts = ["Hello", "World", "Test"]
        embeddings = toolkit.embed_batch(available_model, texts)
        print(f"   ✓ Batch embeddings generated: {len(embeddings)} vectors")
        
        print("✓ Embedding test passed!")
        return True
        
    except Exception as e:
        print(f"   ✗ Embedding test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("OLLAMA TOOLKIT - BASIC TESTS")
    print("=" * 50)
    
    success = True
    
    # Run basic tests
    if not test_basic_functionality():
        success = False
    
    # Run conversation tests
    if not test_conversation():
        success = False
    
    # Run embedding tests
    if not test_embeddings():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("The Ollama Toolkit is working correctly.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check your Ollama installation and available models.")
    
    print("\nAvailable models:")
    try:
        models = list_available_models()
        for model in models:
            print(f"  - {model}")
        
        if not models:
            print("  No models found!")
            print("  Install models with: ollama pull <model-name>")
            print("  Recommended models:")
            print("    - ollama pull llama3.2")
            print("    - ollama pull gemma2")
            print("    - ollama pull nomic-embed-text")
    except Exception as e:
        print(f"  Error listing models: {e}")
    
    print("=" * 50)
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)