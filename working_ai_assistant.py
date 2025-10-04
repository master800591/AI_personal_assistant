"""
Complete working AI Personal Assistant
"""
import asyncio
import sys
import logging
from pathlib import Path
import requests
import json

class SimpleOllamaToolkit:
    """Simple Ollama client without complex dependencies"""
    
    def __init__(self, host: str = "localhost:11434"):
        self.host = host.replace("http://", "").replace("https://", "")
        self.base_url = f"http://{self.host}"
        self.logger = logging.getLogger(__name__)
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            return []
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return []
    
    async def chat_async(self, model: str, messages):
        """Async wrapper for chat"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._chat_sync, model, messages)
    
    def _chat_sync(self, model: str, messages):
        """Synchronous chat request"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Chat request failed: {e}")
            return {"error": str(e)}

class WorkingAIAssistant:
    """Complete working AI Assistant implementation"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.ollama = SimpleOllamaToolkit()
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
    
    async def start(self):
        """Start the AI Assistant"""
        self.logger.info("🚀 Starting AI Assistant...")
        
        # Check Ollama
        if self.ollama.is_available():
            models = self.ollama.list_models()
            self.logger.info(f"✅ Ollama connected - {len(models)} models available")
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
                
                # Analyze Python files in workspace
                python_files = list(Path('.').glob('**/*.py'))[:5]  # Limit to 5 files
                
                for file_path in python_files:
                    try:
                        result = await self.analyze_file(file_path)
                        if result:
                            self.logger.info(f"📊 Analyzed: {file_path.name}")
                    except Exception as e:
                        self.logger.error(f"❌ Failed to analyze {file_path}: {e}")
                
                self.logger.info(f"✅ Cycle {cycle_count} complete")
                
                # Wait before next cycle
                await asyncio.sleep(60)  # 1 minute cycles
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Shutdown requested")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(30)
        
        self.running = False
    
    async def analyze_file(self, file_path: Path) -> dict:
        """Analyze a Python file"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if file is too large
            if len(content) > 10000:
                return {"skipped": "File too large"}
            
            # Analyze with Ollama if available
            if self.ollama.is_available():
                analysis = await self.analyze_with_ollama(content, str(file_path))
                return {"analysis": analysis, "file": str(file_path)}
            else:
                return {"skipped": "Ollama not available"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_with_ollama(self, code: str, filename: str) -> str:
        """Analyze code with Ollama"""
        prompt = f"""Analyze this Python file for improvements:

File: {filename}

Code:
```python
{code}
```

Provide 3 specific, actionable improvements."""
        
        messages = [
            {"role": "system", "content": "You are a Python code expert. Provide concise, specific improvements."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.ollama.chat_async("deepseek-r1", messages)
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            else:
                return "No analysis received"
        except Exception as e:
            return f"Analysis failed: {e}"
    
    def status(self) -> dict:
        """Get system status"""
        return {
            "running": self.running,
            "ollama_available": self.ollama.is_available(),
            "models": len(self.ollama.list_models()) if self.ollama.is_available() else 0
        }

# Main execution function
async def main():
    """Main entry point"""
    assistant = WorkingAIAssistant()
    
    try:
        await assistant.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("✅ AI Assistant stopped")

if __name__ == "__main__":
    print("🤖 Starting Working AI Assistant...")
    asyncio.run(main())