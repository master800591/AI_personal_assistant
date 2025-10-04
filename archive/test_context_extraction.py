"""
Test context size extraction and enhanced model information
"""
from ollama_model_manager import OllamaModelManager

def test_context_size_extraction():
    """Test the enhanced model information extraction."""
    print("🔍 Testing Context Size Extraction and Enhanced Model Info")
    print("=" * 60)
    
    manager = OllamaModelManager()
    
    # Test with a search for models WITH detailed fetching
    print("\n1. Searching for 'llama' models with detailed information...")
    try:
        models = manager.search_models_with_details("llama", page_limit=1, max_details=3)
        print(f"Found {len(models)} models")
        
        for i, model in enumerate(models[:3], 1):  # Show first 3
            print(f"\n{i}. Model: {model.name}")
            print(f"   Description: {model.description}")
            
            # Show technical specifications
            if model.context_size:
                print(f"   📊 Context Size: {model.context_size:,} tokens")
            else:
                print(f"   📊 Context Size: Not detected")
                
            if model.parameter_count:
                print(f"   📊 Parameters: {model.parameter_count}")
            
            if model.model_family:
                print(f"   📊 Model Family: {model.model_family}")
                
            if model.quantization:
                print(f"   📊 Quantization: {model.quantization}")
                
            if model.capabilities:
                print(f"   🎯 Capabilities: {', '.join(model.capabilities)}")
            
            if model.pulls:
                print(f"   📈 Downloads: {model.pulls:,}")
                
            if model.size:
                print(f"   💾 Size: {model.size}")
                
    except Exception as e:
        print(f"Error testing models: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 Testing single model detail extraction...")
    
    # Test direct model detail fetching
    try:
        test_models = ["llama3.2", "gemma2", "phi3"]
        for model_name in test_models:
            print(f"\nFetching details for {model_name}...")
            details = manager.get_model_details(model_name)
            
            if details:
                print(f"  Context Size: {details.get('context_size', 'Not found')}")
                print(f"  Parameters: {details.get('parameter_count', 'Not found')}")
                print(f"  Model Family: {details.get('model_family', 'Not found')}")
                print(f"  Quantization: {details.get('quantization', 'Not found')}")
            else:
                print(f"  No details found for {model_name}")
    except Exception as e:
        print(f"Error testing individual model details: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Context size extraction test complete!")
    print("\nThe enhanced model information now includes:")
    print("  • Context window size (tokens) - extracted from model pages")
    print("  • Parameter count (B/M format)")
    print("  • Model family (Llama, Mistral, etc.)")
    print("  • Quantization format (Q4, Q8, FP16, etc.)")
    print("  • Enhanced capabilities detection")
    print("  • License information (when available)")
    print("\nUse search_models_with_details() to get context sizes!")

if __name__ == "__main__":
    test_context_size_extraction()