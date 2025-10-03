#!/usr/bin/env python3
"""
Real Working AI Developer
Uses existing Ollama infrastructure for actual autonomous development
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from ollama_toolkit import OllamaToolkit
except ImportError:
    logger.error("❌ OllamaToolkit not found")
    sys.exit(1)

class RealAIDeveloper:
    """Real AI developer that actually works with local models"""
    
    def __init__(self):
        self.ollama = OllamaToolkit()
        self.workspace = Path.cwd()
        logger.info(f"🤖 Real AI Developer initialized in {self.workspace}")
        
    def find_python_files(self):
        """Find Python files to work with"""
        files = list(self.workspace.glob("*.py"))
        # Skip generated files
        files = [f for f in files if not f.name.startswith(('utility_', 'ai_feature_'))]
        return files[:3]  # Work with first 3 files
    
    def analyze_code_quality(self, file_path):
        """Analyze code quality with simple prompts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if len(code.strip()) < 100:
                return "File too small to analyze"
                
            # Use a simple, direct approach
            prompt = f"""Look at this Python code and suggest ONE specific improvement:

{code[:800]}

Give exactly one improvement suggestion in format:
IMPROVEMENT: [specific change needed]"""

            # Use the generate method instead of chat for simplicity
            response = self.ollama.generate(
                model='deepseek-r1',
                prompt=prompt
            )
            
            if response and 'response' in response:
                suggestion = response['response'].strip()
                if 'IMPROVEMENT:' in suggestion:
                    improvement = suggestion.split('IMPROVEMENT:')[1].strip()
                    logger.info(f"📝 Suggestion for {file_path.name}: {improvement[:100]}...")
                    return improvement
                    
        except Exception as e:
            logger.error(f"❌ Analysis failed for {file_path}: {e}")
        
        return None
    
    def create_simple_utility(self):
        """Create a simple utility file"""
        try:
            prompt = """Create a simple Python utility function that helps with file management. 
Write only the Python code, nothing else:

def organize_files():
    # Your implementation here
    pass"""

            response = self.ollama.generate(
                model='deepseek-r1',
                prompt=prompt
            )
            
            if response and 'response' in response:
                code = response['response'].strip()
                
                timestamp = int(time.time())
                utility_file = f"utility_{timestamp}.py"
                
                with open(utility_file, 'w', encoding='utf-8') as f:
                    f.write(f"#!/usr/bin/env python3\n")
                    f.write(f'"""\nGenerated utility - {datetime.now().isoformat()}\n"""\n\n')
                    f.write(code)
                
                logger.info(f"✅ Created utility: {utility_file}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to create utility: {e}")
        
        return False
    
    def run_development_cycle(self):
        """Run one development cycle"""
        logger.info("🚀 Starting development cycle...")
        
        files = self.find_python_files()
        suggestions_made = 0
        
        for file_path in files:
            suggestion = self.analyze_code_quality(file_path)
            if suggestion:
                suggestions_made += 1
                
                # Create a suggestions log
                log_file = "development_suggestions.md"
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n## {datetime.now().isoformat()}\n")
                    f.write(f"**File:** {file_path.name}\n")
                    f.write(f"**Suggestion:** {suggestion}\n\n")
        
        # Create utility occasionally
        utility_created = False
        if suggestions_made > 0:
            utility_created = self.create_simple_utility()
        
        logger.info(f"✅ Cycle completed: {suggestions_made} suggestions, utility created: {utility_created}")
        
        return {
            'suggestions': suggestions_made,
            'utility_created': utility_created,
            'timestamp': datetime.now().isoformat()
        }
    
    def start_autonomous_development(self):
        """Start autonomous development with shorter cycles"""
        logger.info("🔄 Starting autonomous development...")
        
        cycle_count = 0
        
        while cycle_count < 3:  # Run only 3 cycles for demo
            try:
                cycle_count += 1
                logger.info(f"📊 Cycle {cycle_count}/3")
                
                result = self.run_development_cycle()
                
                logger.info(f"📈 Results: {result}")
                
                if cycle_count < 3:
                    logger.info("⏳ Next cycle in 30 seconds...")
                    time.sleep(30)
                    
            except KeyboardInterrupt:
                logger.info("👋 Development stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Cycle error: {e}")
                time.sleep(10)
        
        logger.info("🎉 Demo cycles completed!")

def main():
    """Main function"""
    try:
        # Test Ollama connection first
        toolkit = OllamaToolkit()
        models = toolkit.list_models()
        if hasattr(models, 'models'):
            model_count = len(models.models)
        else:
            model_count = len(models) if isinstance(models, list) else 1
        logger.info(f"🧠 Available models: {model_count}")
        
        # Start the developer
        developer = RealAIDeveloper()
        developer.start_autonomous_development()
        
    except Exception as e:
        logger.error(f"❌ Failed to start: {e}")

if __name__ == "__main__":
    main()