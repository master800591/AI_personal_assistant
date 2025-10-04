"""
Test script for encoding fix
"""
from ollama_model_manager import OllamaModelManager

def test_encoding_fix():
    """Test that the encoding fix resolves the charmap issue."""
    print("Testing encoding fix...")
    
    manager = OllamaModelManager()
    
    # Test getting local models (should work without encoding errors)
    try:
        local_models = manager.get_local_models()
        print(f"✓ Local models retrieved successfully: {len(local_models)} models found")
        for model in local_models[:3]:  # Show first 3
            print(f"  - {model}")
        if len(local_models) > 3:
            print(f"  ... and {len(local_models) - 3} more")
    except Exception as e:
        print(f"✗ Error getting local models: {e}")
    
    # Test pulling a small model (if no models exist)
    if not local_models:
        print("\nNo models found. Testing pull functionality...")
        try:
            # Try to pull a small, fast model for testing
            success = manager.pull_model("qwen2.5:0.5b", show_progress=False)
            if success:
                print("✓ Model pull test successful")
            else:
                print("✗ Model pull test failed")
        except Exception as e:
            print(f"✗ Error during pull test: {e}")
    else:
        print("\nModels already installed. Encoding fix test complete.")

if __name__ == "__main__":
    test_encoding_fix()