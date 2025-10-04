#!/usr/bin/env python3
"""
Autonomous Developer
Core autonomous development functionality using local Ollama models
"""

import os
import sys
import json
import time
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..utils.config import Config
from ..utils.logging import get_logger
from ..utils.helpers import backup_file, get_python_files, ensure_directory
from ..ollama.toolkit import OllamaToolkit

logger = get_logger(__name__)

class AutonomousDeveloper:
    """Autonomous developer that analyzes and improves code using AI"""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize autonomous developer"""
        self.config = config or Config()
        self.ollama = OllamaToolkit()
        self.workspace = Path.cwd()
        self.cycle_count = 0
        self.running = False
        
        # Configuration
        self.cycle_interval = self.config.get('autonomous.cycle_interval', 600)
        self.max_files_per_cycle = self.config.get('autonomous.max_files_per_cycle', 5)
        self.backup_enabled = self.config.get('autonomous.backup_before_changes', True)
        
        logger.info("🤖 Autonomous Developer initialized")
    
    async def analyze_codebase(self) -> List[Dict[str, Any]]:
        """Analyze the codebase for improvements"""
        logger.info("🔍 Analyzing codebase...")
        
        python_files = get_python_files(self.workspace)
        
        # Filter out files in archive, tests, and other directories we should skip
        skip_patterns = ['archive/', 'tests/', '.venv/', '__pycache__/', '.git/']
        filtered_files = [
            f for f in python_files 
            if not any(pattern in str(f) for pattern in skip_patterns)
        ]
        
        # Limit files per cycle
        files_to_analyze = filtered_files[:self.max_files_per_cycle]
        
        improvements = []
        
        for file_path in files_to_analyze:
            try:
                file_improvements = await self._analyze_file(file_path)
                improvements.extend(file_improvements)
                
            except Exception as e:
                logger.error(f"❌ Failed to analyze {file_path}: {e}")
        
        logger.info(f"✅ Found {len(improvements)} potential improvements")
        return improvements
    
    async def _analyze_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze a single file for improvements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            if len(code_content.strip()) < 100:
                return []  # Skip very small files
            
            prompt = f"""
Analyze this Python code and suggest specific improvements. Focus on:
1. Performance optimizations
2. Error handling improvements
3. Code clarity and maintainability
4. Security issues
5. Missing functionality

File: {file_path.name}
Code:
```python
{code_content[:2000]}  # First 2000 characters
```

Return ONLY a JSON array of improvements:
[{{"type": "performance", "description": "specific issue", "suggestion": "specific fix", "priority": 1-5, "line": 0}}]
"""

            response = await self.ollama.chat_async(
                model='deepseek-r1',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            if not response or 'message' not in response:
                return []
            
            content = response['message'].get('content', '')
            
            # Extract JSON from response
            try:
                start = content.find('[')
                end = content.rfind(']') + 1
                if start >= 0 and end > start:
                    json_text = content[start:end]
                    improvements_data = json.loads(json_text)
                    
                    # Add file path to each improvement
                    for improvement in improvements_data:
                        improvement['file_path'] = str(file_path)
                    
                    return improvements_data
                    
            except json.JSONDecodeError:
                logger.warning(f"⚠️ Could not parse JSON from analysis of {file_path.name}")
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze {file_path}: {e}")
            return []
    
    async def implement_improvement(self, improvement: Dict[str, Any]) -> bool:
        """Implement a specific improvement"""
        file_path = Path(improvement['file_path'])
        
        logger.info(f"🔧 Implementing: {improvement['description']}")
        
        try:
            # Read current file content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Create backup if enabled
            if self.backup_enabled:
                backup_file(file_path)
            
            prompt = f"""
Apply this improvement to the Python code. Return ONLY the complete improved code.

Original code:
```python
{original_content}
```

Improvement to apply:
Type: {improvement['type']}
Description: {improvement['description']}
Suggestion: {improvement['suggestion']}

Return the complete improved Python file:
"""

            response = await self.ollama.chat_async(
                model='stable-code',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            if not response or 'message' not in response:
                return False
            
            improved_code = response['message'].get('content', '').strip()
            
            # Basic validation
            if improved_code and self._validate_code(improved_code):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(improved_code)
                
                logger.info(f"✅ Applied improvement to {file_path.name}")
                return True
            else:
                logger.warning(f"⚠️ Generated code failed validation for {file_path.name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to implement improvement: {e}")
            return False
    
    def _validate_code(self, code: str) -> bool:
        """Basic validation of generated code"""
        # Check if it looks like Python code
        python_indicators = ['def ', 'class ', 'import ', 'from ', '#']
        has_python_syntax = any(indicator in code for indicator in python_indicators)
        
        # Check minimum length
        has_minimum_length = len(code.strip()) > 50
        
        # Check for common issues
        has_no_placeholders = 'TODO' not in code and '...' not in code[:100]
        
        return has_python_syntax and has_minimum_length and has_no_placeholders
    
    async def create_new_feature(self) -> bool:
        """Create a new utility feature"""
        logger.info("🆕 Creating new feature...")
        
        try:
            prompt = """
Create a useful Python utility module for an AI development system. Choose from:
- Performance monitoring utilities
- File organization helpers  
- Development workflow tools
- System health checks
- Code analysis helpers

Create a complete, functional Python module with:
1. Clear purpose and documentation
2. Error handling
3. Logging integration
4. Main function for testing

Return ONLY the complete Python code:
"""

            response = await self.ollama.chat_async(
                model='stable-code',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            if not response or 'message' not in response:
                return False
            
            code = response['message'].get('content', '').strip()
            
            if code and self._validate_code(code):
                # Generate filename based on content
                timestamp = int(time.time())
                filename = f"ai_generated_utility_{timestamp}.py"
                
                # Try to extract a better name from the code
                lines = code.split('\n')
                for line in lines:
                    if 'class ' in line:
                        class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                        filename = f"{class_name.lower()}_utility.py"
                        break
                
                utils_dir = self.workspace / "src" / "ai_assistant" / "utils"
                feature_path = utils_dir / filename
                
                with open(feature_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                logger.info(f"✅ Created new feature: {filename}")
                return True
            else:
                logger.warning("⚠️ Generated feature code failed validation")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create new feature: {e}")
            return False
    
    async def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a specific file for improvements"""
        try:
            self.logger.info(f"🔍 Analyzing file: {file_path}")
            
            # Read file content
            if not Path(file_path).exists():
                return {'error': f'File not found: {file_path}'}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use Ollama to analyze the code
            prompt = f"""
            Analyze this Python code for quality, performance, and security issues:
            
            File: {file_path}
            
            ```python
            {content}
            ```
            
            Provide specific suggestions for improvement.
            """
            
            response = await self.ollama.chat_async(
                model=self.config.get('ollama.default_model', 'deepseek-r1'),
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            analysis = {
                'file': file_path,
                'analysis': response.get('message', {}).get('content', ''),
                'timestamp': time.time(),
                'model_used': self.config.get('ollama.default_model', 'deepseek-r1')
            }
            
            self.logger.info(f"✅ Analysis complete for {file_path}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Failed to analyze {file_path}: {e}")
            return {'error': str(e)}
        """Run one complete development cycle"""
        self.cycle_count += 1
        start_time = time.time()
        
        logger.info(f"🚀 Starting development cycle {self.cycle_count}")
        
        try:
            # Step 1: Analyze codebase
            improvements = await self.analyze_codebase()
            
            # Step 2: Implement improvements
            implementation_results = []
            
            if improvements:
                # Sort by priority and implement top ones
                improvements.sort(key=lambda x: x.get('priority', 3), reverse=True)
                
                for improvement in improvements[:3]:  # Implement top 3
                    success = await self.implement_improvement(improvement)
                    implementation_results.append(success)
                    
                    if success:
                        await asyncio.sleep(1)  # Brief pause between implementations
            
            # Step 3: Create new feature occasionally
            new_feature_created = False
            if self.cycle_count % 3 == 0:  # Every 3rd cycle
                new_feature_created = await self.create_new_feature()
            
            # Step 4: Log results
            successful_implementations = sum(implementation_results)
            duration = time.time() - start_time
            
            result = {
                'cycle': self.cycle_count,
                'success': True,
                'improvements_found': len(improvements),
                'improvements_implemented': successful_implementations,
                'new_feature_created': new_feature_created,
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(
                f"✅ Cycle {self.cycle_count} completed: "
                f"{successful_implementations}/{len(improvements)} improvements, "
                f"new feature: {new_feature_created}, "
                f"duration: {duration:.1f}s"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Development cycle {self.cycle_count} failed: {e}")
            return {
                'cycle': self.cycle_count,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def run_cycle(self) -> Dict[str, Any]:
        """Run a single development cycle"""
        self.cycle_count += 1
        
        try:
            logger.info(f"🔄 Starting development cycle {self.cycle_count}")
            
            # 1. Analyze codebase
            improvements = await self.analyze_codebase()
            
            # 2. Implement high priority improvements
            implemented = 0
            for improvement in improvements[:3]:  # Implement top 3
                if await self.implement_improvement(improvement):
                    implemented += 1
            
            # 3. Optionally create new features
            if implemented == 0:  # No improvements implemented, try creating new feature
                await self.create_new_feature()
            
            return {
                'cycle': self.cycle_count,
                'success': True,
                'improvements_found': len(improvements),
                'improvements_implemented': implemented,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error in development cycle {self.cycle_count}: {e}")
            return {
                'cycle': self.cycle_count,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def start(self):
        """Start continuous autonomous development"""
        logger.info("🔄 Starting continuous autonomous development...")
        self.running = True
        
        while self.running:
            try:
                # Run development cycle
                result = await self.run_cycle()
                
                # Log cycle result
                if result['success']:
                    logger.info(f"✅ Cycle {result['cycle']} successful")
                else:
                    logger.error(f"❌ Cycle {result['cycle']} failed: {result.get('error')}")
                
                # Wait for next cycle
                if self.running:
                    logger.info(f"⏳ Next cycle in {self.cycle_interval//60} minutes...")
                    await asyncio.sleep(self.cycle_interval)
                
            except asyncio.CancelledError:
                logger.info("🛑 Autonomous development cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error in development loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
        
        self.running = False
        logger.info("✅ Autonomous development stopped")
    
    async def shutdown(self):
        """Gracefully shutdown autonomous development"""
        logger.info("🔄 Shutting down autonomous development...")
        self.running = False

def main():
    """Main entry point for autonomous developer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Autonomous Developer")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--cycles", type=int, help="Number of cycles to run (default: continuous)")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        config = Config(args.config) if args.config else Config()
        developer = AutonomousDeveloper(config)
        
        if args.cycles:
            # Run specific number of cycles
            async def run_cycles():
                for i in range(args.cycles):
                    result = await developer.run_cycle()
                    print(f"Cycle {i+1} result: {result}")
            
            asyncio.run(run_cycles())
        else:
            # Run continuously
            asyncio.run(developer.start())
            
    except KeyboardInterrupt:
        logger.info("👋 Autonomous developer stopped by user")
    except Exception as e:
        logger.error(f"❌ Autonomous developer failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()