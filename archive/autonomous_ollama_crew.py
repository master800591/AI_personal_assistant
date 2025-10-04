#!/usr/bin/env python3
"""
Autonomous Ollama Development Crew
Uses local Ollama models for real autonomous development
No external APIs - all local models with actual code improvements
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from ollama_toolkit import OllamaToolkit
except ImportError:
    logger.error("❌ OllamaToolkit not found. Please ensure ollama_toolkit.py is available.")
    sys.exit(1)

@dataclass
class CodeImprovement:
    """Represents a code improvement suggestion"""
    file_path: str
    issue_type: str
    description: str
    suggested_fix: str
    priority: int
    impact: str

class AutonomousOllamaCrew:
    """Autonomous development crew using local Ollama models"""
    
    def __init__(self):
        self.ollama = OllamaToolkit()
        self.workspace_path = os.getcwd()
        self.models = self._get_available_models()
        self.cycle_count = 0
        
        logger.info(f"🤖 Autonomous Ollama Crew initialized")
        logger.info(f"📁 Workspace: {self.workspace_path}")
        logger.info(f"🧠 Available models: {', '.join(self.models)}")
        
    def _get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            models = self.ollama.list_models()
            model_names = []
            for model in models:
                if isinstance(model, dict) and 'name' in model:
                    name = model['name'].split(':')[0]
                    if name:
                        model_names.append(name)
            return model_names if model_names else ['deepseek-r1', 'stable-code', 'codellama']
        except Exception as e:
            logger.error(f"❌ Failed to get models: {e}")
            return ['deepseek-r1', 'stable-code', 'codellama']  # Fallback
    
    def _select_model_for_task(self, task_type: str) -> str:
        """Select the best model for a specific task"""
        model_preferences = {
            'analysis': ['deepseek-r1', 'codellama', 'stable-code'],
            'coding': ['stable-code', 'codellama', 'deepseek-r1'],
            'review': ['deepseek-r1', 'stable-code', 'codellama'],
            'planning': ['deepseek-r1', 'codellama', 'stable-code']
        }
        
        preferred = model_preferences.get(task_type, self.models)
        for model in preferred:
            if model in self.models:
                return model
        
        return self.models[0] if self.models else 'deepseek-r1'
    
    def analyze_codebase(self) -> List[CodeImprovement]:
        """Analyze the codebase for real improvements"""
        logger.info("🔍 Analyzing codebase for improvements...")
        
        model = self._select_model_for_task('analysis')
        improvements = []
        
        # Get Python files in workspace
        python_files = list(Path(self.workspace_path).glob("*.py"))
        
        for file_path in python_files[:5]:  # Analyze first 5 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                
                if len(code_content.strip()) == 0:
                    continue
                    
                analysis_prompt = f"""
Analyze this Python code for real improvements. Focus on:
1. Performance optimizations
2. Error handling improvements  
3. Code quality enhancements
4. Security vulnerabilities
5. Missing functionality

Code from {file_path.name}:
```python
{code_content[:2000]}  # First 2000 chars
```

Return ONLY a JSON list of improvements in this format:
[{{"issue_type": "performance", "description": "specific issue", "suggested_fix": "specific solution", "priority": 1-5, "impact": "expected benefit"}}]
"""

                response = self.ollama.sync_client.chat(
                    model=model,
                    messages=[{"role": "user", "content": analysis_prompt}],
                    options={"temperature": 0.3}
                )
                
                # Extract JSON from response
                response_text = ""
                if hasattr(response, 'message') and hasattr(response.message, 'content'):
                    response_text = response.message.content or ""
                elif isinstance(response, dict) and 'message' in response:
                    response_text = response['message'].get('content', '') if isinstance(response['message'], dict) else str(response['message'])
                else:
                    response_text = str(response)
                if response_text:
                    try:
                        # Try to extract JSON from response
                        json_start = response_text.find('[')
                        json_end = response_text.rfind(']') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_text = response_text[json_start:json_end]
                            analysis_data = json.loads(json_text)
                            
                            for item in analysis_data:
                                if isinstance(item, dict) and all(k in item for k in ['issue_type', 'description', 'suggested_fix']):
                                    improvement = CodeImprovement(
                                        file_path=str(file_path),
                                        issue_type=item.get('issue_type', 'general'),
                                        description=item.get('description', ''),
                                        suggested_fix=item.get('suggested_fix', ''),
                                        priority=item.get('priority', 3),
                                        impact=item.get('impact', 'moderate')
                                    )
                                    improvements.append(improvement)
                    except json.JSONDecodeError:
                        logger.warning(f"⚠️ Could not parse JSON from analysis of {file_path.name}")
                        
            except Exception as e:
                logger.error(f"❌ Failed to analyze {file_path}: {e}")
                
        logger.info(f"✅ Found {len(improvements)} potential improvements")
        return improvements
    
    def implement_improvement(self, improvement: CodeImprovement) -> bool:
        """Implement a specific code improvement"""
        logger.info(f"🔧 Implementing: {improvement.description}")
        
        model = self._select_model_for_task('coding')
        
        try:
            # Read the current file
            with open(improvement.file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            implementation_prompt = f"""
You are implementing a specific code improvement. 

File: {improvement.file_path}
Issue: {improvement.description}
Suggested Fix: {improvement.suggested_fix}

Current code:
```python
{current_code}
```

Provide the COMPLETE improved version of this file. Make only the necessary changes to address the specific issue. Maintain all existing functionality while implementing the improvement.

Return ONLY the complete Python code, no explanations or markdown:
"""

            response = self.ollama.sync_client.chat(
                model=model,
                messages=[{"role": "user", "content": implementation_prompt}],
                options={"temperature": 0.2}
            )
            
            improved_code = response.get('message', {}).get('content', '').strip()
            
            if improved_code and improved_code.startswith(('import ', 'from ', '#', '"""', "'''")):
                # Save backup
                backup_path = f"{improvement.file_path}.backup_{int(time.time())}"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(current_code)
                
                # Write improved code
                with open(improvement.file_path, 'w', encoding='utf-8') as f:
                    f.write(improved_code)
                
                logger.info(f"✅ Implemented improvement in {improvement.file_path}")
                logger.info(f"💾 Backup saved: {backup_path}")
                return True
            else:
                logger.warning(f"⚠️ Invalid code generated for {improvement.file_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to implement improvement: {e}")
            return False
    
    def create_new_feature(self) -> bool:
        """Create a new useful feature for the AI system"""
        logger.info("🆕 Creating new feature...")
        
        model = self._select_model_for_task('coding')
        
        feature_prompt = f"""
Create a new useful feature for this AI personal assistant system. 

Current workspace has these files: {', '.join([f.name for f in Path(self.workspace_path).glob('*.py')])}

Create a completely new Python module that adds value to the system. Some ideas:
- System monitoring and health checks
- Performance metrics collection  
- Enhanced logging and reporting
- File organization utilities
- Backup and recovery tools
- Configuration management
- User interaction improvements

Choose ONE feature and implement it completely. The file should be:
1. Immediately useful and functional
2. Well-documented with docstrings
3. Include error handling
4. Have a main function for testing
5. Follow Python best practices

Return ONLY the complete Python code for the new feature file:
"""

        try:
            response = self.ollama.sync_client.chat(
                model=model,
                messages=[{"role": "user", "content": feature_prompt}],
                options={"temperature": 0.4}
            )
            
            new_code = response.get('message', {}).get('content', '').strip()
            
            if new_code and 'def ' in new_code:
                # Generate filename from code
                feature_name = f"ai_feature_{int(time.time())}.py"
                
                # Extract a better name from docstring or class name
                lines = new_code.split('\n')
                for line in lines:
                    if 'class ' in line and 'class ' == line.strip()[:6]:
                        class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                        feature_name = f"{class_name.lower()}.py"
                        break
                
                feature_path = os.path.join(self.workspace_path, feature_name)
                
                with open(feature_path, 'w', encoding='utf-8') as f:
                    f.write(new_code)
                
                logger.info(f"✅ Created new feature: {feature_name}")
                
                # Test the new feature
                try:
                    result = subprocess.run([sys.executable, feature_path], 
                                          capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        logger.info(f"✅ New feature tested successfully")
                    else:
                        logger.warning(f"⚠️ New feature has issues: {result.stderr}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not test new feature: {e}")
                
                return True
            else:
                logger.warning("⚠️ Invalid feature code generated")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create new feature: {e}")
            return False
    
    def document_changes(self, cycle: int, improvements: List[CodeImprovement], 
                        implemented: List[bool], new_feature: bool) -> None:
        """Document the changes made in this cycle"""
        
        report_dir = f"autonomous_development/cycle_{cycle}"
        os.makedirs(report_dir, exist_ok=True)
        
        # Create detailed report
        report_path = f"{report_dir}/development_report.md"
        with open(report_path, 'w') as f:
            f.write(f"# Autonomous Development Cycle {cycle}\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n")
            f.write(f"**Models Used:** {', '.join(self.models)}\n\n")
            
            f.write("## Code Improvements\n\n")
            for i, improvement in enumerate(improvements):
                status = "✅ Implemented" if implemented[i] else "❌ Failed"
                f.write(f"### {improvement.issue_type.title()} - {improvement.file_path}\n")
                f.write(f"**Status:** {status}\n")
                f.write(f"**Priority:** {improvement.priority}/5\n")
                f.write(f"**Description:** {improvement.description}\n")
                f.write(f"**Impact:** {improvement.impact}\n")
                f.write(f"**Fix:** {improvement.suggested_fix}\n\n")
            
            if new_feature:
                f.write("## New Feature\n")
                f.write("✅ Created new feature to enhance system functionality\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Analyzed {len(improvements)} potential improvements\n")
            f.write(f"- Successfully implemented {sum(implemented)} improvements\n")
            f.write(f"- Created new feature: {'Yes' if new_feature else 'No'}\n")
        
        logger.info(f"📋 Development report saved: {report_path}")
    
    def run_development_cycle(self) -> Dict[str, Any]:
        """Run a complete autonomous development cycle"""
        self.cycle_count += 1
        logger.info(f"🚀 Starting Autonomous Development Cycle {self.cycle_count}")
        
        try:
            # Step 1: Analyze codebase
            improvements = self.analyze_codebase()
            
            if not improvements:
                logger.info("ℹ️ No improvements identified, creating new feature")
                new_feature = self.create_new_feature()
                return {
                    "cycle": self.cycle_count,
                    "success": True,
                    "improvements_found": 0,
                    "improvements_implemented": 0,
                    "new_feature_created": new_feature,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Step 2: Implement top improvements
            implemented = []
            max_implementations = min(3, len(improvements))  # Implement up to 3 improvements
            
            # Sort by priority (highest first)
            improvements.sort(key=lambda x: x.priority, reverse=True)
            
            for improvement in improvements[:max_implementations]:
                success = self.implement_improvement(improvement)
                implemented.append(success)
                if success:
                    time.sleep(2)  # Brief pause between implementations
            
            # Step 3: Create new feature (occasionally)
            new_feature = False
            if self.cycle_count % 3 == 0:  # Every 3rd cycle
                new_feature = self.create_new_feature()
            
            # Step 4: Document changes
            self.document_changes(self.cycle_count, improvements, implemented, new_feature)
            
            successful_implementations = sum(implemented)
            logger.info(f"✅ Cycle {self.cycle_count} completed: {successful_implementations}/{len(implemented)} improvements implemented")
            
            return {
                "cycle": self.cycle_count,
                "success": True,
                "improvements_found": len(improvements),
                "improvements_implemented": successful_implementations,
                "new_feature_created": new_feature,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Cycle {self.cycle_count} failed: {e}")
            return {
                "cycle": self.cycle_count,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def start_continuous_development(self):
        """Start continuous autonomous development"""
        logger.info("🔄 Starting continuous autonomous development...")
        
        while True:
            try:
                result = self.run_development_cycle()
                
                if result["success"]:
                    logger.info(f"✅ Cycle {result['cycle']} completed successfully")
                else:
                    logger.error(f"❌ Cycle {result['cycle']} failed: {result.get('error')}")
                
                # Wait between cycles (10 minutes for testing, adjust as needed)
                wait_time = 10 * 60  # 10 minutes
                logger.info(f"⏳ Next development cycle in {wait_time//60} minutes...")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                logger.info("👋 Autonomous development stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function to start autonomous development"""
    try:
        logger.info("🤖 Starting Autonomous Ollama Development Crew...")
        
        crew = AutonomousOllamaCrew()
        crew.start_continuous_development()
        
    except KeyboardInterrupt:
        logger.info("👋 Autonomous Ollama Crew stopped")
    except Exception as e:
        logger.error(f"❌ Failed to start autonomous crew: {e}")

if __name__ == "__main__":
    main()