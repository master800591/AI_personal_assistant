#!/usr/bin/env python3
"""
Simple Ollama Autonomous Developer
Direct ollama client for autonomous development
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import ollama
except ImportError:
    logger.error("❌ Ollama package not found. Install with: pip install ollama")
    exit(1)

class SimpleAutonomousDev:
    """Simple autonomous developer using direct Ollama client"""
    
    def __init__(self):
        self.client = ollama.Client()
        self.models = self._get_models()
        self.cycle_count = 0
        
        logger.info(f"🤖 Simple Autonomous Developer initialized")
        logger.info(f"🧠 Available models: {', '.join(self.models)}")
    
    def _get_models(self):
        """Get available models"""
        try:
            response = self.client.list()
            models = [model['name'].split(':')[0] for model in response['models']]
            return list(set(models)) if models else ['deepseek-r1']
        except Exception as e:
            logger.error(f"❌ Failed to get models: {e}")
            return ['deepseek-r1']
    
    def analyze_file(self, file_path):
        """Analyze a single file for improvements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if len(code.strip()) < 50:  # Skip tiny files
                return []
            
            prompt = f"""Analyze this Python code for real improvements. Return ONLY valid JSON array:

```python
{code[:1500]}
```

Format: [{{"type":"performance","description":"specific issue","fix":"specific solution","priority":1}}]"""

            response = self.client.chat(
                model=self.models[0],
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            content = response['message']['content']
            
            # Extract JSON
            start = content.find('[')
            end = content.rfind(']') + 1
            if start >= 0 and end > start:
                json_text = content[start:end]
                try:
                    improvements = json.loads(json_text)
                    logger.info(f"✅ Found {len(improvements)} improvements for {file_path.name}")
                    return improvements
                except json.JSONDecodeError:
                    pass
                    
            return []
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze {file_path}: {e}")
            return []
    
    def implement_fix(self, file_path, improvement):
        """Implement a fix for a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            prompt = f"""Apply this improvement to the code. Return ONLY the complete fixed code:

Original code:
```python
{original_code}
```

Improvement: {improvement['description']}
Fix: {improvement['fix']}

Return complete fixed Python code:"""

            response = self.client.chat(
                model=self.models[0],
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            fixed_code = response['message']['content'].strip()
            
            # Basic validation
            if fixed_code.startswith(('import ', 'from ', '#', '"""', "'''")):
                # Backup original
                backup_path = f"{file_path}.backup_{int(time.time())}"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_code)
                
                # Write fixed code
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                
                logger.info(f"✅ Applied fix to {file_path.name}")
                return True
            else:
                logger.warning(f"⚠️ Invalid code generated for {file_path.name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to implement fix: {e}")
            return False
    
    def create_new_utility(self):
        """Create a new utility module"""
        try:
            prompt = """Create a useful Python utility module for an AI development system. Ideas:
- Performance monitoring
- File organization 
- System health checks
- Backup utilities
- Log analysis

Choose ONE and implement it completely. Return ONLY the complete Python code:"""

            response = self.client.chat(
                model=self.models[0],
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            code = response['message']['content'].strip()
            
            if 'def ' in code and 'import ' in code:
                filename = f"utility_{int(time.time())}.py"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                logger.info(f"✅ Created new utility: {filename}")
                return True
            else:
                logger.warning("⚠️ Invalid utility code generated")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create utility: {e}")
            return False
    
    def run_development_cycle(self):
        """Run one development cycle"""
        self.cycle_count += 1
        logger.info(f"🚀 Development Cycle {self.cycle_count}")
        
        # Get Python files
        python_files = list(Path('.').glob('*.py'))[:5]  # First 5 files
        
        improvements_made = 0
        
        for file_path in python_files:
            if file_path.name.startswith('utility_'):
                continue  # Skip generated utilities
                
            improvements = self.analyze_file(file_path)
            
            for improvement in improvements[:1]:  # Apply first improvement only
                if self.implement_fix(file_path, improvement):
                    improvements_made += 1
                    break
        
        # Create new utility occasionally
        new_utility = False
        if self.cycle_count % 3 == 0:
            new_utility = self.create_new_utility()
        
        # Log results
        logger.info(f"✅ Cycle {self.cycle_count} completed: {improvements_made} improvements, new utility: {new_utility}")
        
        return {
            'cycle': self.cycle_count,
            'improvements': improvements_made,
            'new_utility': new_utility,
            'timestamp': datetime.now().isoformat()
        }
    
    def start_continuous_development(self):
        """Start continuous development"""
        logger.info("🔄 Starting continuous development...")
        
        while True:
            try:
                result = self.run_development_cycle()
                
                # Wait 5 minutes between cycles
                logger.info("⏳ Next cycle in 5 minutes...")
                time.sleep(5 * 60)
                
            except KeyboardInterrupt:
                logger.info("👋 Development stopped")
                break
            except Exception as e:
                logger.error(f"❌ Cycle error: {e}")
                time.sleep(60)

def main():
    """Main function"""
    try:
        dev = SimpleAutonomousDev()
        dev.start_continuous_development()
    except Exception as e:
        logger.error(f"❌ Failed to start: {e}")

if __name__ == "__main__":
    main()