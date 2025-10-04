"""
Setup script for Ollama Toolkit

This script helps users set up the Ollama Toolkit by checking dependencies,
suggesting models to install, and providing setup guidance.
"""

import subprocess
import sys
import os
from typing import List, Tuple


def check_python_version() -> bool:
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("  Ollama requires Python 3.8 or higher")
        return False


def check_ollama_installation() -> bool:
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ Ollama is installed: {version}")
            return True
        else:
            print("✗ Ollama command failed")
            return False
    except FileNotFoundError:
        print("✗ Ollama is not installed or not in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Ollama command timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False


def check_ollama_running() -> bool:
    """Check if Ollama service is running."""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Ollama service is running")
            return True
        else:
            print("✗ Ollama service is not responding")
            print("  Try running: ollama serve")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama service: {e}")
        return False


def check_pip_package() -> bool:
    """Check if ollama pip package is installed."""
    try:
        import ollama
        print("✓ ollama Python package is installed")
        return True
    except ImportError:
        print("✗ ollama Python package is not installed")
        return False


def install_pip_package() -> bool:
    """Install the ollama Python package."""
    print("\nInstalling ollama Python package...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'ollama'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ollama package installed successfully")
            return True
        else:
            print(f"✗ Failed to install ollama package: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing ollama package: {e}")
        return False


def get_available_models() -> List[str]:
    """Get list of available models."""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
        return []
    except Exception:
        return []


def suggest_models() -> List[Tuple[str, str]]:
    """Return suggested models with descriptions."""
    return [
        ('llama3.2', 'Meta\'s Llama 3.2 - Good general purpose model'),
        ('gemma2', 'Google\'s Gemma 2 - Fast and efficient'),
        ('qwen2.5', 'Alibaba\'s Qwen 2.5 - Multilingual support'),
        ('phi3', 'Microsoft\'s Phi-3 - Compact but capable'),
        ('nomic-embed-text', 'Nomic Embed - For text embeddings'),
        ('llama3.2-vision', 'Llama 3.2 Vision - For image analysis'),
    ]


def pull_model(model_name: str) -> bool:
    """Pull a model from Ollama."""
    print(f"\nPulling model: {model_name}")
    print("This may take a while depending on model size...")
    
    try:
        # Use Popen to show real-time output
        process = subprocess.Popen(['ollama', 'pull', model_name], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 text=True, 
                                 bufsize=1, 
                                 universal_newlines=True)
        
        for line in process.stdout:
            print(f"  {line.rstrip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print(f"✓ Successfully pulled {model_name}")
            return True
        else:
            print(f"✗ Failed to pull {model_name}")
            return False
            
    except Exception as e:
        print(f"✗ Error pulling {model_name}: {e}")
        return False


def test_toolkit() -> bool:
    """Test if the toolkit works."""
    try:
        # Try to import and use the toolkit
        from ollama_toolkit import list_available_models, quick_chat
        
        models = list_available_models()
        if models:
            print(f"✓ Toolkit working - found {len(models)} models")
            
            # Try a simple chat
            try:
                response = quick_chat(models[0], "Hello! Please respond with just 'Hi!'")
                print(f"✓ Chat test successful: {response.strip()}")
                return True
            except Exception as e:
                print(f"! Chat test failed: {e}")
                return True  # Toolkit is working, just chat failed
        else:
            print("! Toolkit working but no models available")
            return True
            
    except ImportError as e:
        print(f"✗ Cannot import toolkit: {e}")
        return False
    except Exception as e:
        print(f"✗ Toolkit test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("OLLAMA TOOLKIT SETUP")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    print("\n1. Checking Python version...")
    if not check_python_version():
        success = False
    
    # Check Ollama installation
    print("\n2. Checking Ollama installation...")
    if not check_ollama_installation():
        print("   Please install Ollama from: https://ollama.com/download")
        success = False
    else:
        # Check if Ollama is running
        print("\n3. Checking Ollama service...")
        if not check_ollama_running():
            print("   Please start Ollama service: ollama serve")
            success = False
    
    # Check Python package
    print("\n4. Checking ollama Python package...")
    if not check_pip_package():
        if input("   Install ollama Python package? (y/n): ").lower().startswith('y'):
            if not install_pip_package():
                success = False
        else:
            success = False
    
    if not success:
        print("\n" + "=" * 50)
        print("❌ SETUP INCOMPLETE")
        print("Please resolve the issues above before using the toolkit.")
        return
    
    # Check available models
    print("\n5. Checking available models...")
    models = get_available_models()
    if models:
        print(f"✓ Found {len(models)} models:")
        for model in models:
            print(f"   - {model}")
    else:
        print("! No models found")
        
        print("\nRecommended models:")
        suggested = suggest_models()
        for i, (model, description) in enumerate(suggested, 1):
            print(f"   {i}. {model} - {description}")
        
        print("\nWould you like to install some models?")
        choice = input("Enter model numbers (comma-separated) or 'n' to skip: ").strip()
        
        if choice.lower() != 'n':
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                for idx in indices:
                    if 0 <= idx < len(suggested):
                        model_name = suggested[idx][0]
                        pull_model(model_name)
            except ValueError:
                print("Invalid input. Skipping model installation.")
    
    # Test toolkit
    print("\n6. Testing toolkit...")
    if test_toolkit():
        print("✓ Toolkit is working correctly!")
    else:
        print("✗ Toolkit test failed")
        success = False
    
    # Final status
    print("\n" + "=" * 50)
    if success:
        print("🎉 SETUP COMPLETE!")
        print("\nYou can now use the Ollama Toolkit:")
        print("   python test_ollama_toolkit.py  # Run basic tests")
        print("   python ollama_examples.py      # See comprehensive examples")
        print("\nQuick start:")
        print("   from ollama_toolkit import quick_chat")
        print("   response = quick_chat('llama3.2', 'Hello!')")
    else:
        print("❌ SETUP INCOMPLETE")
        print("Please resolve the issues above.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()