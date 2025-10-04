"""
Working AI Personal Assistant - Complete System
"""
import asyncio
import logging
import requests
import json
from pathlib import Path

class WorkingAIAssistant:
    """Complete working AI Assistant implementation"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.ollama_host = "localhost:11434"
        self.ollama_url = f"http://{self.ollama_host}"
        self.running = False
        
        self.logger.info("🤖 Working AI Assistant initialized")
    
    def setup_logging(self):
        """Setup simple logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('ai_assistant.log', encoding='utf-8')
            ]
        )
    
    def is_ollama_available(self):
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_ollama_models(self):
        """Get available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            return []
        except Exception as e:
            self.logger.error(f"Failed to get models: {e}")
            return []
    
    async def chat_with_ollama(self, model, messages):
        """Chat with Ollama model"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(
                    f"{self.ollama_url}/api/chat",
                    json=payload,
                    timeout=120
                )
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Chat failed: {e}")
            return {"error": str(e)}
    
    async def start(self):
        """Start the AI Assistant"""
        self.logger.info("🚀 Starting AI Assistant...")
        
        # Check Ollama
        if self.is_ollama_available():
            models = self.get_ollama_models()
            self.logger.info(f"✅ Ollama connected - {len(models)} models available")
            
            # List models
            for model in models:
                self.logger.info(f"   📦 {model.get('name', 'Unknown')}")
        else:
            self.logger.warning("⚠️ Ollama not available")
        
        self.running = True
        self.logger.info("✅ AI Assistant started successfully")
        
        # Run main loop
        await self.run_main_loop()
    
    async def run_main_loop(self):
        """Main application loop"""
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                self.logger.info(f"🔄 Starting cycle {cycle_count}")
                
                # Find Python files to analyze
                python_files = []
                for pattern in ['*.py', 'src/**/*.py']:
                    python_files.extend(Path('.').glob(pattern))
                
                # Limit to 3 files per cycle
                files_to_analyze = python_files[:3]
                
                if not files_to_analyze:
                    self.logger.info("📁 No Python files found")
                else:
                    self.logger.info(f"📁 Found {len(python_files)} files, analyzing {len(files_to_analyze)}")
                
                # Analyze files
                for file_path in files_to_analyze:
                    if file_path.name.startswith('.'):
                        continue
                        
                    try:
                        result = await self.analyze_file(file_path)
                        if result.get('analysis'):
                            self.logger.info(f"📊 Analyzed: {file_path.name}")
                            # Log first line of analysis
                            analysis = result['analysis']
                            if analysis and len(analysis) > 100:
                                preview = analysis[:100] + "..."
                                self.logger.info(f"   💡 {preview}")
                    except Exception as e:
                        self.logger.error(f"❌ Failed to analyze {file_path}: {e}")
                
                self.logger.info(f"✅ Cycle {cycle_count} complete")
                
                # Wait before next cycle
                self.logger.info("⏳ Waiting 2 minutes before next cycle...")
                await asyncio.sleep(120)  # 2 minute cycles
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Shutdown requested")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(30)
        
        self.running = False
    
    async def analyze_file(self, file_path):
        """Analyze a Python file"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if file is too large
            if len(content) > 15000:
                return {"skipped": "File too large"}
            
            # Skip if file is too small
            if len(content) < 50:
                return {"skipped": "File too small"}
            
            # Analyze with Ollama if available
            if self.is_ollama_available():
                analysis = await self.analyze_with_ollama(content, str(file_path))
                return {"analysis": analysis, "file": str(file_path)}
            else:
                return {"skipped": "Ollama not available"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_with_ollama(self, code, filename):
        """Analyze code with Ollama"""
        # Use a model that's likely to be available
        models = self.get_ollama_models()
        if not models:
            return "No models available"
        
        # Prefer deepseek-r1 or use first available
        model_name = "deepseek-r1"
        available_names = [m.get('name', '') for m in models]
        if model_name not in available_names:
            model_name = available_names[0] if available_names else "llama2"
        
        prompt = f"""Analyze this Python file for improvements:

File: {filename}

Code (first 2000 chars):
```python
{code[:2000]}
```

Provide 2-3 specific, actionable improvements with examples."""
        
        messages = [
            {"role": "system", "content": "You are a Python code expert. Provide concise, specific improvements."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.chat_with_ollama(model_name, messages)
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            elif 'error' in response:
                return f"Analysis failed: {response['error']}"
            else:
                return "No analysis received"
        except Exception as e:
            return f"Analysis failed: {e}"
    
    def status(self):
        """Get system status"""
        models = self.get_ollama_models() if self.is_ollama_available() else []
        return {
            "running": self.running,
            "ollama_available": self.is_ollama_available(),
            "models": len(models),
            "model_names": [m.get('name', 'Unknown') for m in models[:5]]
        }

# Main execution function
async def main():
    """Main entry point"""
    print("🤖 Working AI Personal Assistant")
    print("=" * 50)
    
    assistant = WorkingAIAssistant()
    
    # Show initial status
    status = assistant.status()
    print(f"🔍 Status: {status}")
    
    try:
        await assistant.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ AI Assistant stopped")

if __name__ == "__main__":
    asyncio.run(main())