"""
Ollama Model Discovery CLI

A command-line tool to discover and pull Ollama models from https://ollama.com/search
"""

import argparse
import subprocess
import sys
from pathlib import Path
from ollama_model_manager import OllamaModelManager


def print_models(models, title="Models", show_details=True):
    """Print a formatted list of models."""
    if not models:
        print(f"No {title.lower()} found.")
        return
    
    print(f"\n{title} ({len(models)}):")
    print("-" * 50)
    
    for i, model in enumerate(models, 1):
        if hasattr(model, 'name'):  # ModelInfo object
            print(f"{i:2d}. {model.name}")
            if show_details:
                if model.description:
                    print(f"     {model.description}")
                
                # Show technical specifications
                specs = []
                if hasattr(model, 'context_size') and model.context_size:
                    specs.append(f"Context: {model.context_size:,} tokens")
                if hasattr(model, 'parameter_count') and model.parameter_count:
                    specs.append(f"Params: {model.parameter_count}")
                if hasattr(model, 'model_family') and model.model_family:
                    specs.append(f"Family: {model.model_family}")
                if hasattr(model, 'quantization') and model.quantization:
                    specs.append(f"Quant: {model.quantization}")
                
                if specs:
                    print(f"     📊 {' | '.join(specs)}")
                
                if model.pulls > 0:
                    print(f"     Downloads: {model.pulls:,}")
                if model.size:
                    print(f"     Size: {model.size}")
                
                # Show capabilities if available
                if hasattr(model, 'capabilities') and model.capabilities:
                    caps_str = ", ".join(model.capabilities)
                    print(f"     🎯 Capabilities: {caps_str}")
                    
                print()
        else:  # String (local model)
            print(f"{i:2d}. {model}")


def discover_command(args):
    """Discover available models."""
    manager = OllamaModelManager()
    
    if args.category:
        print(f"Discovering models in category: {args.category}")
        models = manager.search_by_category(args.category)
    elif args.query:
        print(f"Searching for models: {args.query}")
        models = manager.search_models(args.query, page_limit=args.pages)
    else:
        print("Discovering popular models...")
        models = manager.get_popular_models(limit=args.limit)
    
    # Apply filters
    if args.min_pulls:
        models = [m for m in models if m.pulls >= args.min_pulls]
    
    if args.exclude_local:
        local_models = manager.get_local_models()
        local_names = {m.split(':')[0] for m in local_models}
        models = [m for m in models if m.name not in local_names]
    
    print_models(models, "Discovered Models")
    
    # Save to file if requested
    if args.output:
        manager.save_model_list(models, args.output)
        print(f"\nSaved {len(models)} models to {args.output}")
    
    return models


def pull_command(args):
    """Pull models."""
    manager = OllamaModelManager()
    
    if args.models:
        # Pull specific models
        model_names = args.models
    elif args.file:
        # Load from file
        try:
            models = manager.load_model_list(args.file)
            model_names = [m.name for m in models[:args.limit]]
        except Exception as e:
            print(f"Error loading models from file: {e}")
            return
    elif args.popular:
        # Pull popular models
        print("Discovering popular models...")
        models = manager.get_popular_models(limit=args.limit)
        
        # Filter out local models
        local_models = manager.get_local_models()
        local_names = {m.split(':')[0] for m in local_models}
        new_models = [m for m in models if m.name not in local_names]
        
        if not new_models:
            print("All popular models are already installed.")
            return
        
        print_models(new_models[:args.limit], "Models to Pull")
        
        if not args.yes:
            confirm = input(f"\nPull these {len(new_models[:args.limit])} models? (y/n): ")
            if not confirm.lower().startswith('y'):
                print("Operation cancelled.")
                return
        
        model_names = [m.name for m in new_models[:args.limit]]
    else:
        print("No models specified. Use --models, --file, or --popular")
        return
    
    # Pull models
    print(f"\nPulling {len(model_names)} models...")
    if args.parallel and len(model_names) > 1:
        results = manager.pull_models_batch(
            model_names, 
            max_workers=args.workers,
            show_progress=not args.quiet
        )
        
        # Show results
        success = sum(results.values())
        print(f"\nResults: {success}/{len(model_names)} models pulled successfully")
        
        if success < len(model_names):
            failed = [name for name, status in results.items() if not status]
            print(f"Failed models: {', '.join(failed)}")
    else:
        # Pull sequentially
        success = 0
        for model_name in model_names:
            if manager.pull_model(model_name, show_progress=not args.quiet):
                success += 1
        
        print(f"\nResults: {success}/{len(model_names)} models pulled successfully")


def list_command(args):
    """List local models."""
    manager = OllamaModelManager()
    
    local_models = manager.get_local_models()
    print_models(local_models, "Local Models", show_details=False)
    
    if args.details:
        print("\nDetailed information:")
        for model in local_models:
            try:
                # Get model size and details
                import subprocess
                result = subprocess.run(['ollama', 'show', model], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"\n{model}:")
                    lines = result.stdout.split('\n')
                    for line in lines[:10]:  # Show first 10 lines
                        if line.strip():
                            print(f"  {line}")
            except Exception:
                pass


def recommend_command(args):
    """Get recommended models by category."""
    manager = OllamaModelManager()
    
    print("Discovering recommended models by category...")
    recommendations = manager.discover_recommended_models()
    
    for category, models in recommendations.items():
        if args.category and category != args.category:
            continue
            
        print(f"\n{category.upper()} MODELS")
        print("=" * 40)
        
        for i, model in enumerate(models[:args.limit], 1):
            print(f"{i:2d}. {model.name}")
            if model.description:
                print(f"     {model.description}")
            if model.pulls > 0:
                print(f"     Downloads: {model.pulls:,}")
            print()
        
        if args.pull and models:
            confirm = input(f"Pull top {min(args.pull_count, len(models))} {category} models? (y/n): ")
            if confirm.lower().startswith('y'):
                to_pull = [m.name for m in models[:args.pull_count]]
                manager.pull_models_batch(to_pull, show_progress=True)


def search_command(args):
    """Search for specific models."""
    manager = OllamaModelManager()
    
    print(f"Searching for: {args.query}")
    models = manager.search_models(args.query, page_limit=args.pages)
    
    if args.category:
        models = [m for m in models 
                 if any(args.category.lower() in tag.lower() for tag in m.tags)]
    
    print_models(models, f"Search Results for '{args.query}'")
    
    if args.pull and models:
        print("\nSelect models to pull:")
        for i, model in enumerate(models[:10], 1):
            print(f"{i:2d}. {model.name}")
        
        choices = input("Enter model numbers (comma-separated): ").strip()
        if choices:
            try:
                indices = [int(x.strip()) - 1 for x in choices.split(',')]
                to_pull = [models[i].name for i in indices if 0 <= i < len(models)]
                
                if to_pull:
                    manager.pull_models_batch(to_pull, show_progress=True)
            except ValueError:
                print("Invalid input")


def remove_command(args):
    """Remove models."""
    manager = OllamaModelManager()
    
    if args.all:
        # Remove all models
        results = manager.remove_all_models(confirm=not args.yes)
        if results:
            success = sum(results.values())
            print(f"\nResults: {success}/{len(results)} models removed successfully")
            
            if success < len(results):
                failed = [name for name, status in results.items() if not status]
                print(f"Failed to remove: {', '.join(failed)}")
    
    elif args.models:
        # Remove specific models
        model_names = args.models
        
        # Verify models exist locally
        local_models = manager.get_local_models()
        valid_models = [name for name in model_names if name in local_models]
        invalid_models = [name for name in model_names if name not in local_models]
        
        if invalid_models:
            print(f"Models not found locally: {', '.join(invalid_models)}")
        
        if not valid_models:
            print("No valid models to remove.")
            return
        
        print(f"\nRemoving {len(valid_models)} models:")
        for model in valid_models:
            print(f"  - {model}")
        
        if not args.yes:
            confirm = input(f"\nRemove these {len(valid_models)} models? (y/n): ")
            if not confirm.lower().startswith('y'):
                print("Operation cancelled.")
                return
        
        # Remove models
        if args.parallel and len(valid_models) > 1:
            results = manager.remove_models_batch(
                valid_models, 
                max_workers=args.workers,
                show_progress=not args.quiet
            )
        else:
            # Remove sequentially
            results = {}
            for model_name in valid_models:
                results[model_name] = manager.remove_model(model_name, show_progress=not args.quiet)
        
        # Show results
        success = sum(results.values())
        print(f"\nResults: {success}/{len(valid_models)} models removed successfully")
        
        if success < len(valid_models):
            failed = [name for name, status in results.items() if not status]
            print(f"Failed to remove: {', '.join(failed)}")
    
    else:
        # Interactive removal
        local_models = manager.get_local_models()
        if not local_models:
            print("No models installed.")
            return
        
        print_models(local_models, "Installed Models", show_details=False)
        
        print("\nRemoval options:")
        print("1. Remove specific models")
        print("2. Remove all models")
        print("3. Cancel")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            choices = input("Enter model numbers to remove (comma-separated): ").strip()
            if choices:
                try:
                    indices = [int(x.strip()) - 1 for x in choices.split(',')]
                    to_remove = [local_models[i] for i in indices if 0 <= i < len(local_models)]
                    
                    if to_remove:
                        confirm = input(f"Remove {len(to_remove)} models? (y/n): ")
                        if confirm.lower().startswith('y'):
                            manager.remove_models_batch(to_remove, show_progress=True)
                except ValueError:
                    print("Invalid input")
        
        elif choice == "2":
            manager.remove_all_models(confirm=True)
        
        else:
            print("Operation cancelled.")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Discover and pull Ollama models from https://ollama.com/search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s discover --popular --limit 10
  %(prog)s discover --query "embedding" --pages 3
  %(prog)s pull --popular --limit 3 --yes
  %(prog)s pull --models llama3.2 gemma2 phi3
  %(prog)s recommend --category code --pull
  %(prog)s search "vision" --pull
  %(prog)s list --details
  %(prog)s remove --models llama3.2 gemma2
  %(prog)s remove --all --yes
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover available models')
    discover_parser.add_argument('--query', help='Search query')
    discover_parser.add_argument('--category', help='Model category')
    discover_parser.add_argument('--limit', type=int, default=20, help='Maximum models to show')
    discover_parser.add_argument('--pages', type=int, default=3, help='Pages to search')
    discover_parser.add_argument('--min-pulls', type=int, help='Minimum download count')
    discover_parser.add_argument('--exclude-local', action='store_true', 
                               help='Exclude already installed models')
    discover_parser.add_argument('--output', help='Save results to JSON file')
    
    # Pull command
    pull_parser = subparsers.add_parser('pull', help='Pull models')
    pull_parser.add_argument('--models', nargs='+', help='Specific models to pull')
    pull_parser.add_argument('--file', help='Load models from JSON file')
    pull_parser.add_argument('--popular', action='store_true', help='Pull popular models')
    pull_parser.add_argument('--limit', type=int, default=5, help='Maximum models to pull')
    pull_parser.add_argument('--parallel', action='store_true', help='Pull models in parallel')
    pull_parser.add_argument('--workers', type=int, default=3, help='Parallel workers')
    pull_parser.add_argument('--yes', action='store_true', help='Auto-confirm pulls')
    pull_parser.add_argument('--quiet', action='store_true', help='Suppress progress output')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List local models')
    list_parser.add_argument('--details', action='store_true', help='Show detailed information')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get recommended models')
    recommend_parser.add_argument('--category', help='Specific category')
    recommend_parser.add_argument('--limit', type=int, default=5, help='Models per category')
    recommend_parser.add_argument('--pull', action='store_true', help='Offer to pull models')
    recommend_parser.add_argument('--pull-count', type=int, default=2, help='Models to pull per category')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for models')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--pages', type=int, default=2, help='Pages to search')
    search_parser.add_argument('--pull', action='store_true', help='Offer to pull found models')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove models')
    remove_parser.add_argument('--models', nargs='+', help='Specific models to remove')
    remove_parser.add_argument('--all', action='store_true', help='Remove all models')
    remove_parser.add_argument('--parallel', action='store_true', help='Remove models in parallel')
    remove_parser.add_argument('--workers', type=int, default=3, help='Parallel workers')
    remove_parser.add_argument('--yes', action='store_true', help='Auto-confirm removals')
    remove_parser.add_argument('--quiet', action='store_true', help='Suppress progress output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'discover':
            discover_command(args)
        elif args.command == 'pull':
            pull_command(args)
        elif args.command == 'list':
            list_command(args)
        elif args.command == 'recommend':
            recommend_command(args)
        elif args.command == 'search':
            search_command(args)
        elif args.command == 'remove':
            remove_command(args)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()