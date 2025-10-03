"""
Quick Ollama Model Discovery Tool

Simple interface to discover and pull popular Ollama models.
"""

from ollama_model_manager import OllamaModelManager


def main():
    """Interactive model discovery and installation."""
    print("🦙 OLLAMA MODEL DISCOVERY TOOL")
    print("=" * 50)
    
    manager = OllamaModelManager()
    
    try:
        # Show current local models
        print("\n📦 Current local models:")
        local_models = manager.get_local_models()
        if local_models:
            for i, model in enumerate(local_models, 1):
                print(f"  {i:2d}. {model}")
        else:
            print("  No models installed yet.")
        
        print("\n🔍 What would you like to do?")
        print("1. Discover popular models")
        print("2. Search for specific models")
        print("3. Get recommendations by category")
        print("4. Pull specific models")
        print("5. Remove models")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            discover_popular(manager)
        elif choice == "2":
            search_models(manager)
        elif choice == "3":
            get_recommendations(manager)
        elif choice == "4":
            pull_specific(manager)
        elif choice == "5":
            remove_models_menu(manager)
        elif choice == "6":
            print("Goodbye! 👋")
            return
        else:
            print("Invalid choice. Please try again.")
            main()
    
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\nError: {e}")


def discover_popular(manager):
    """Discover and optionally install popular models."""
    print("\n🔥 Discovering popular models...")
    
    try:
        # Get popular models
        popular = manager.get_popular_models(limit=15)
        
        if not popular:
            print("❌ No models found. Check your internet connection.")
            return
        
        # Filter out already installed
        local_models = manager.get_local_models()
        local_names = {m.split(':')[0] for m in local_models}
        new_models = [m for m in popular if m.name not in local_names]
        
        if not new_models:
            print("✅ All popular models are already installed!")
            return
        
        print(f"\n📋 Popular models available for installation:")
        for i, model in enumerate(new_models[:10], 1):
            pulls_str = f"{model.pulls:,}" if model.pulls > 0 else "N/A"
            size_str = f" ({model.size})" if model.size else ""
            print(f"  {i:2d}. {model.name}{size_str}")
            print(f"      {model.description}")
            print(f"      Downloads: {pulls_str}")
            print()
        
        print("📥 Installation options:")
        print("1. Install top 3 popular models")
        print("2. Install top 5 popular models")
        print("3. Choose specific models")
        print("4. Back to main menu")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            install_models = new_models[:3]
        elif choice == "2":
            install_models = new_models[:5]
        elif choice == "3":
            indices_str = input("Enter model numbers (comma-separated): ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in indices_str.split(',')]
                install_models = [new_models[i] for i in indices 
                                if 0 <= i < len(new_models)]
            except ValueError:
                print("❌ Invalid input.")
                return
        elif choice == "4":
            main()
            return
        else:
            print("❌ Invalid choice.")
            return
        
        if install_models:
            model_names = [m.name for m in install_models]
            print(f"\n🚀 Installing {len(model_names)} models...")
            print(f"Models: {', '.join(model_names)}")
            
            confirm = input("Continue? (y/n): ").lower()
            if confirm.startswith('y'):
                results = manager.pull_models_batch(model_names, show_progress=True)
                success = sum(results.values())
                print(f"\n✅ Successfully installed {success}/{len(model_names)} models!")
                
                if success < len(model_names):
                    failed = [name for name, status in results.items() if not status]
                    print(f"❌ Failed: {', '.join(failed)}")
            else:
                print("❌ Installation cancelled.")
    
    except Exception as e:
        print(f"❌ Error discovering models: {e}")


def search_models(manager):
    """Search for specific models."""
    print("\n🔍 Search for models")
    
    query = input("Enter search term (e.g., 'embedding', 'vision', 'code'): ").strip()
    if not query:
        print("❌ No search term provided.")
        return
    
    try:
        print(f"Searching for '{query}'...")
        models = manager.search_models(query, page_limit=3)
        
        if not models:
            print(f"❌ No models found for '{query}'.")
            return
        
        print(f"\n📋 Found {len(models)} models:")
        for i, model in enumerate(models[:10], 1):
            pulls_str = f"{model.pulls:,}" if model.pulls > 0 else "N/A"
            size_str = f" ({model.size})" if model.size else ""
            print(f"  {i:2d}. {model.name}{size_str}")
            print(f"      {model.description}")
            print(f"      Downloads: {pulls_str}")
            print()
        
        choice = input("Install any models? Enter numbers (comma-separated) or 'n': ").strip()
        if choice.lower() != 'n':
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                install_models = [models[i].name for i in indices 
                                if 0 <= i < len(models)]
                
                if install_models:
                    print(f"Installing: {', '.join(install_models)}")
                    results = manager.pull_models_batch(install_models, show_progress=True)
                    success = sum(results.values())
                    print(f"✅ Successfully installed {success}/{len(install_models)} models!")
            except ValueError:
                print("❌ Invalid input.")
    
    except Exception as e:
        print(f"❌ Error searching models: {e}")


def get_recommendations(manager):
    """Get model recommendations by category."""
    print("\n🎯 Model recommendations by category")
    
    categories = {
        '1': 'general',
        '2': 'code', 
        '3': 'embedding',
        '4': 'vision',
        '5': 'chat',
        '6': 'instruct'
    }
    
    print("Available categories:")
    for key, category in categories.items():
        print(f"  {key}. {category.title()}")
    
    choice = input("Choose category (1-6) or 'all' for all categories: ").strip()
    
    try:
        if choice.lower() == 'all':
            print("🔍 Discovering all categories...")
            recommendations = manager.discover_recommended_models()
            
            for category, models in recommendations.items():
                if models:
                    print(f"\n🏷️  {category.upper()} MODELS:")
                    for i, model in enumerate(models[:3], 1):
                        pulls_str = f"{model.pulls:,}" if model.pulls > 0 else "N/A"
                        print(f"    {i}. {model.name} - {model.description}")
                        print(f"       Downloads: {pulls_str}")
                    print()
        
        elif choice in categories:
            category = categories[choice]
            print(f"🔍 Searching {category} models...")
            
            # Search for models in this category
            models = manager.search_models(category, page_limit=2)
            
            if models:
                print(f"\n🏷️  {category.upper()} MODELS:")
                for i, model in enumerate(models[:5], 1):
                    pulls_str = f"{model.pulls:,}" if model.pulls > 0 else "N/A"
                    size_str = f" ({model.size})" if model.size else ""
                    print(f"  {i}. {model.name}{size_str}")
                    print(f"     {model.description}")
                    print(f"     Downloads: {pulls_str}")
                    print()
                
                install_choice = input("Install top 2 models? (y/n): ").strip()
                if install_choice.lower().startswith('y'):
                    install_models = [m.name for m in models[:2]]
                    print(f"Installing: {', '.join(install_models)}")
                    results = manager.pull_models_batch(install_models, show_progress=True)
                    success = sum(results.values())
                    print(f"✅ Successfully installed {success}/{len(install_models)} models!")
            else:
                print(f"❌ No models found for {category} category.")
        
        else:
            print("❌ Invalid choice.")
    
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")


def pull_specific(manager):
    """Pull specific models by name."""
    print("\n📥 Pull specific models")
    print("Enter model names separated by spaces or commas.")
    print("Examples: llama3.2 gemma2 phi3")
    print("          llama3.2, gemma2, phi3")
    
    models_input = input("Model names: ").strip()
    if not models_input:
        print("❌ No models specified.")
        return
    
    # Parse model names
    if ',' in models_input:
        model_names = [name.strip() for name in models_input.split(',')]
    else:
        model_names = models_input.split()
    
    model_names = [name for name in model_names if name]  # Remove empty strings
    
    if not model_names:
        print("❌ No valid model names provided.")
        return
    
    try:
        print(f"\n🚀 Pulling {len(model_names)} models:")
        for name in model_names:
            print(f"  - {name}")
        
        confirm = input("Continue? (y/n): ").strip()
        if confirm.lower().startswith('y'):
            results = manager.pull_models_batch(model_names, show_progress=True)
            success = sum(results.values())
            print(f"\n✅ Successfully pulled {success}/{len(model_names)} models!")
            
            if success < len(model_names):
                failed = [name for name, status in results.items() if not status]
                print(f"❌ Failed: {', '.join(failed)}")
        else:
            print("❌ Operation cancelled.")
    
    except Exception as e:
        print(f"❌ Error pulling models: {e}")


def remove_models_menu(manager):
    """Interactive model removal menu."""
    print("\n🗑️  Remove Models")
    print("=" * 30)
    
    # Get current local models
    local_models = manager.get_local_models()
    
    if not local_models:
        print("❌ No models installed to remove.")
        return
    
    print(f"\n📦 Installed models ({len(local_models)}):")
    for i, model in enumerate(local_models, 1):
        print(f"  {i:2d}. {model}")
    
    print("\n🔍 What would you like to do?")
    print("1. Remove specific models")
    print("2. Remove ALL models")
    print("3. Cancel")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    try:
        if choice == "1":
            # Remove specific models
            print("\nEnter model numbers to remove (comma-separated):")
            print("Example: 1,3,5 or 1 2 3")
            
            selection = input("Model numbers: ").strip()
            if not selection:
                print("❌ No selection made.")
                return
            
            # Parse selection
            try:
                if ',' in selection:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                else:
                    indices = [int(x.strip()) - 1 for x in selection.split()]
                
                # Validate indices
                valid_indices = [i for i in indices if 0 <= i < len(local_models)]
                if not valid_indices:
                    print("❌ No valid model numbers selected.")
                    return
                
                # Get models to remove
                models_to_remove = [local_models[i] for i in valid_indices]
                
                print(f"\n🗑️  Models to remove ({len(models_to_remove)}):")
                for model in models_to_remove:
                    print(f"  - {model}")
                
                confirm = input(f"\nRemove these {len(models_to_remove)} models? (y/n): ").strip()
                if confirm.lower().startswith('y'):
                    print("\n🚀 Removing models...")
                    results = manager.remove_models_batch(models_to_remove, show_progress=True)
                    success = sum(results.values())
                    print(f"\n✅ Successfully removed {success}/{len(models_to_remove)} models!")
                    
                    if success < len(models_to_remove):
                        failed = [name for name, status in results.items() if not status]
                        print(f"❌ Failed to remove: {', '.join(failed)}")
                else:
                    print("❌ Operation cancelled.")
                    
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
                
        elif choice == "2":
            # Remove all models
            print(f"\n⚠️  WARNING: This will remove ALL {len(local_models)} models!")
            print("This action cannot be undone.")
            
            confirm = input(f"\nAre you SURE you want to remove ALL {len(local_models)} models? (yes/no): ").strip()
            if confirm.lower() == 'yes':
                print("\n🚀 Removing all models...")
                results = manager.remove_all_models(confirm=False)  # Already confirmed
                if results:
                    success = sum(results.values())
                    print(f"\n✅ Successfully removed {success}/{len(local_models)} models!")
                    
                    if success < len(local_models):
                        failed = [name for name, status in results.items() if not status]
                        print(f"❌ Failed to remove: {', '.join(failed)}")
                else:
                    print("❌ No models were removed.")
            else:
                print("❌ Operation cancelled.")
                
        elif choice == "3":
            print("❌ Operation cancelled.")
            
        else:
            print("❌ Invalid choice.")
            
    except Exception as e:
        print(f"❌ Error removing models: {e}")


if __name__ == "__main__":
    main()