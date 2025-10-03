#!/usr/bin/env python3
"""
Real CrewAI Autonomous Development Team
Using our existing Ollama models and toolkit infrastructure
"""

import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import our existing Ollama toolkit
from ollama_toolkit import OllamaToolkit

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealAIDevCrew:
    """Real AI development crew using our Ollama models"""
    
    def __init__(self):
        # Use our existing Ollama toolkit
        self.ollama = OllamaToolkit()
        
        # Get available models
        models = self.ollama.list_models()
        self.available_models = [model.model for model in models.models]
        logger.info(f"📋 Available models: {self.available_models}")
        
        # Select best models for different tasks
        self.code_model = self.select_best_model_for_task("coding")
        self.analysis_model = self.select_best_model_for_task("analysis") 
        self.general_model = self.select_best_model_for_task("general")
        
        logger.info(f"🤖 Using models - Code: {self.code_model}, Analysis: {self.analysis_model}, General: {self.general_model}")
        
    def select_best_model_for_task(self, task_type: str) -> str:
        """Select the best available model for each task type"""
        
        # Coding tasks - prefer code-specific models
        if task_type == "coding":
            if "stable-code:3b-code-q4_0" in self.available_models:
                return "stable-code:3b-code-q4_0"
            elif "codellama:latest" in self.available_models:
                return "codellama:latest"
            elif "deepseek-r1:latest" in self.available_models:
                return "deepseek-r1:latest"
                
        # Analysis tasks - prefer reasoning models  
        elif task_type == "analysis":
            if "deepseek-r1:latest" in self.available_models:
                return "deepseek-r1:latest"
            elif "phi3.5:latest" in self.available_models:
                return "phi3.5:latest"
                
        # General tasks
        elif task_type == "general":
            if "dolphin3:latest" in self.available_models:
                return "dolphin3:latest"
            elif "phi3.5:latest" in self.available_models:
                return "phi3.5:latest"
                
        # Fallback to first available model
        return self.available_models[0] if self.available_models else "llama3.2"
        
    def analyze_codebase(self) -> Dict[str, Any]:
        """Use our Ollama models to analyze the codebase"""
        
        logger.info(f"🔍 Analyzing codebase with {self.analysis_model}")
        
        # Read key files for analysis
        key_files = [
            "ollama_toolkit.py",
            "deploy_production.py", 
            "continuous_evolution_engine.py",
            "ai_platform_enhanced.py"
        ]
        
        file_contents = {}
        for file_path in key_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents[file_path] = f.read()[:5000]  # First 5k chars
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
        
        analysis_prompt = f"""You are a senior software architect analyzing the AI Corporation codebase.

Key files analyzed:
{chr(10).join([f"- {file}: {len(content)} chars" for file, content in file_contents.items()])}

Analyze these files and identify:

1. PERFORMANCE BOTTLENECKS:
   - Slow operations that can be optimized
   - Missing caching opportunities
   - Inefficient algorithms or data structures

2. SECURITY VULNERABILITIES:
   - Input validation issues
   - Credential exposure risks
   - Unsafe operations

3. CODE QUALITY ISSUES:
   - Poor error handling
   - Missing documentation
   - Code duplication
   - Anti-patterns

4. MISSING FEATURES:
   - Useful functionality gaps
   - Integration opportunities
   - User experience improvements

5. TECHNICAL DEBT:
   - Outdated dependencies
   - Legacy code patterns
   - Maintenance issues

Provide specific, actionable recommendations with file locations and exact code improvements.
Focus on high-impact changes that provide measurable benefits.

Sample file content for context:
{list(file_contents.values())[0][:1000] if file_contents else "No files found"}...
"""

        try:
            # Use the simple chat without images parameter
            messages = [{"role": "user", "content": analysis_prompt}]
            response = self.ollama.sync_client.chat(
                model=self.analysis_model,
                messages=messages,
                options={"temperature": 0.3, "top_p": 0.9}
            )
            
            analysis_result = response.message.content
            logger.info("✅ Codebase analysis completed")
            
            return {
                "success": True,
                "analysis": analysis_result,
                "model_used": self.analysis_model,
                "files_analyzed": list(file_contents.keys()),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return {"success": False, "error": str(e)}
            
    def generate_code_improvement(self, analysis: str) -> Dict[str, Any]:
        """Generate actual code improvements using our code model"""
        
        logger.info(f"💻 Generating code improvements with {self.code_model}")
        
        code_prompt = f"""Based on this codebase analysis, create a specific, working code improvement:

ANALYSIS RESULTS:
{analysis}

YOUR TASK:
1. Pick ONE high-impact improvement from the analysis
2. Write complete, working Python code that implements the improvement
3. Include proper error handling, logging, and documentation
4. Make it immediately usable and production-ready
5. Show exact file locations and integration instructions

REQUIREMENTS:
- Must be working Python code (not pseudocode)
- Include imports, class definitions, and complete functions
- Add comprehensive docstrings and comments
- Handle edge cases and errors gracefully
- Provide usage examples

OUTPUT FORMAT:
## Improvement: [Brief Description]

### File: [exact filename]

```python
[Complete working code]
```

### Integration Instructions:
[Exact steps to integrate this code]

### Usage Example:
```python
[Working example of how to use the improvement]
```

Focus on one specific, high-value improvement that solves a real problem identified in the analysis.
"""

        try:
            # Use direct client call without images parameter
            messages = [{"role": "user", "content": code_prompt}]
            response = self.ollama.sync_client.chat(
                model=self.code_model,
                messages=messages,
                options={"temperature": 0.1, "top_p": 0.8}
            )
            
            code_result = response.message.content
            logger.info("✅ Code improvement generated")
            
            return {
                "success": True,
                "code_improvement": code_result,
                "model_used": self.code_model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Code generation failed: {e}")
            return {"success": False, "error": str(e)}
            
    def implement_improvement(self, improvement_data: Dict[str, Any]) -> bool:
        """Actually implement the generated code improvement"""
        
        try:
            improvement_text = improvement_data.get("code_improvement", "")
            
            # Extract code blocks and filenames from the improvement
            import re
            
            # Look for file patterns
            file_matches = re.findall(r'### File: (.+)', improvement_text)
            code_blocks = re.findall(r'```python\n(.*?)\n```', improvement_text, re.DOTALL)
            
            if not code_blocks:
                logger.warning("No code blocks found in improvement")
                return False
                
            # Create improvement file
            timestamp = int(time.time())
            improvement_file = f"ai_improvements/improvement_{timestamp}.py"
            os.makedirs("ai_improvements", exist_ok=True)
            
            # Write the improvement code
            with open(improvement_file, 'w', encoding='utf-8') as f:
                f.write(f"""#!/usr/bin/env python3
\"\"\"
AI Corporation Code Improvement #{timestamp}
Generated by AI Development Crew using {improvement_data.get('model_used', 'unknown model')}
Created: {improvement_data.get('timestamp', datetime.now().isoformat())}

{improvement_text}
\"\"\"

{code_blocks[0] if code_blocks else '# No code block found'}
""")
            
            logger.info(f"💾 Improvement implemented: {improvement_file}")
            
            # Also create a summary file
            summary_file = f"ai_improvements/improvement_{timestamp}_summary.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(improvement_text)
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to implement improvement: {e}")
            return False
            
    def run_development_cycle(self) -> Dict[str, Any]:
        """Run a complete development cycle using our Ollama models"""
        
        cycle_start = time.time()
        logger.info("🚀 Starting AI Development Cycle with Ollama models")
        
        # Step 1: Analyze codebase
        analysis_result = self.analyze_codebase()
        if not analysis_result["success"]:
            return {"success": False, "step": "analysis", "error": analysis_result.get("error")}
            
        # Step 2: Generate code improvement
        improvement_result = self.generate_code_improvement(analysis_result["analysis"])
        if not improvement_result["success"]:
            return {"success": False, "step": "code_generation", "error": improvement_result.get("error")}
            
        # Step 3: Implement improvement
        implementation_success = self.implement_improvement(improvement_result)
        if not implementation_success:
            return {"success": False, "step": "implementation", "error": "Failed to write improvement files"}
            
        cycle_time = time.time() - cycle_start
        
        logger.info(f"✅ Development cycle completed in {cycle_time:.1f}s")
        
        return {
            "success": True,
            "cycle_time": cycle_time,
            "analysis_model": analysis_result["model_used"],
            "code_model": improvement_result["model_used"],
            "files_analyzed": analysis_result["files_analyzed"],
            "timestamp": datetime.now().isoformat()
        }
        
    def start_continuous_development(self):
        """Start continuous development using our Ollama infrastructure"""
        
        logger.info("🔄 Starting continuous AI development with Ollama models")
        logger.info(f"🎯 Models ready: {len(self.available_models)} available")
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                logger.info(f"🚀 Development Cycle #{cycle_count}")
                
                # Run development cycle
                result = self.run_development_cycle()
                
                if result["success"]:
                    logger.info(f"✅ Cycle #{cycle_count} completed successfully")
                    logger.info(f"⚡ Performance: {result['cycle_time']:.1f}s")
                    
                    # Commit improvements to git
                    self.commit_improvements(cycle_count, result)
                    
                else:
                    logger.error(f"❌ Cycle #{cycle_count} failed at {result.get('step')}: {result.get('error')}")
                
                # Wait between cycles (10-20 minutes)
                wait_time = 600 + (cycle_count * 60)  # Increasing intervals
                logger.info(f"⏳ Next cycle in {wait_time//60} minutes...")
                
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                logger.info("👋 Development crew stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error in cycle #{cycle_count}: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
                
    def commit_improvements(self, cycle: int, result: Dict[str, Any]):
        """Commit improvements to git repository"""
        
        try:
            import subprocess
            
            # Add new improvement files
            subprocess.run(['git', 'add', 'ai_improvements/'], check=True, capture_output=True)
            
            # Create commit message
            commit_msg = f"""🤖 AI Development Cycle #{cycle}

Analysis Model: {result.get('analysis_model', 'unknown')}
Code Model: {result.get('code_model', 'unknown')} 
Cycle Time: {result.get('cycle_time', 0):.1f}s
Files Analyzed: {len(result.get('files_analyzed', []))}

✨ Autonomous code improvement using Ollama models
⚡ Generated: {result.get('timestamp')}
🎯 Real AI development in action!
"""
            
            # Commit
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            # Push
            subprocess.run(['git', 'push'], check=True, capture_output=True)
            
            logger.info(f"🚀 Cycle #{cycle} committed to git repository")
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Git commit failed: {e}")
        except Exception as e:
            logger.error(f"❌ Commit error: {e}")

def main():
    """Start the real AI development crew using our Ollama models"""
    
    try:
        logger.info("🤖 Initializing AI Development Crew with Ollama")
        
        # Test Ollama connection
        toolkit = OllamaToolkit()
        models = toolkit.list_models()
        logger.info(f"✅ Ollama connected - {len(models.models)} models available")
        
        # Start the development crew
        crew = RealAIDevCrew()
        crew.start_continuous_development()
        
    except Exception as e:
        logger.error(f"❌ Failed to start AI development crew: {e}")
        logger.error("Make sure Ollama is running: ollama serve")

if __name__ == "__main__":
    main()
        
if __name__ == "__main__":
    main()