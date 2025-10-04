"""
Simple working Ollama toolkit without complex dependencies
"""
import requests
import json
import asyncio
import logging
from typing import Dict, Any, List

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
    
    def list_models(self) -> List[Dict[str, Any]]:
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
    
    def chat(self, model: str, messages: List[Dict[str, str]], 
             stream: bool = False) -> Dict[str, Any]:
        """Send chat request to Ollama"""
        try:
            payload: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "stream": stream
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                if stream:
                    # Handle streaming response
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'message' in data and 'content' in data['message']:
                                full_response += data['message']['content']
                    return {"message": {"content": full_response}}
                else:
                    return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Chat request failed: {e}")
            return {"error": str(e)}
    
    async def chat_async(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Async wrapper for chat"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.chat, model, messages, False)
    
    def analyze_code(self, code: str, model: str = "deepseek-r1") -> str:
        """Analyze code and return suggestions"""
        messages = [
            {
                "role": "system",
                "content": "You are a code analysis expert. Analyze the provided code and suggest specific improvements."
            },
            {
                "role": "user", 
                "content": f"Analyze this Python code and suggest improvements:\n\n```python\n{code}\n```"
            }
        ]
        
        response = self.chat(model, messages)
        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
        elif 'error' in response:
            return f"Error: {response['error']}"
        else:
            return "No response received"
    
    def generate_code(self, prompt: str, model: str = "stable-code") -> str:
        """Generate code based on prompt"""
        messages = [
            {
                "role": "system",
                "content": "You are a Python code generator. Generate clean, well-documented Python code."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat(model, messages)
        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
        elif 'error' in response:
            return f"Error: {response['error']}"
        else:
            return "No response received"

# Test function
def test_ollama():
    """Test Ollama connectivity"""
    toolkit = SimpleOllamaToolkit()
    
    print("🧪 Testing Ollama Toolkit")
    print(f"Available: {toolkit.is_available()}")
    
    if toolkit.is_available():
        models = toolkit.list_models()
        print(f"Models: {len(models)} available")
        
        if models:
            # Test chat
            model_name = models[0]['name']
            response = toolkit.chat(model_name, [
                {"role": "user", "content": "Hello, can you help with Python?"}
            ])
            print(f"Test response: {response.get('message', {}).get('content', 'No content')[:100]}...")

if __name__ == "__main__":
    test_ollama()