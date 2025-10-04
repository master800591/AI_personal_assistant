#!/usr/bin/env python3
"""
Model Management
Ollama model management and selection utilities
"""

import logging
from typing import List, Dict, Any, Optional
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ModelManager:
    """Manages Ollama models and selection logic"""
    
    def __init__(self, ollama_toolkit=None):
        """Initialize model manager"""
        self.ollama = ollama_toolkit
        self._available_models = []
        self._model_capabilities = {
            'deepseek-r1': {
                'reasoning': 5,
                'code_analysis': 5,
                'generation': 4,
                'conversation': 4,
                'speed': 3
            },
            'stable-code': {
                'reasoning': 3,
                'code_analysis': 4,
                'generation': 5,
                'conversation': 3,
                'speed': 4
            },
            'codellama': {
                'reasoning': 4,
                'code_analysis': 5,
                'generation': 4,
                'conversation': 3,
                'speed': 4
            },
            'phi3.5': {
                'reasoning': 3,
                'code_analysis': 3,
                'generation': 3,
                'conversation': 4,
                'speed': 5
            },
            'dolphin3': {
                'reasoning': 3,
                'code_analysis': 2,
                'generation': 3,
                'conversation': 5,
                'speed': 4
            },
            'llava': {
                'reasoning': 3,
                'code_analysis': 2,
                'generation': 2,
                'conversation': 4,
                'speed': 3,
                'multimodal': 5
            }
        }
        
        logger.info("🧠 Model Manager initialized")
    
    def refresh_available_models(self) -> List[str]:
        """Refresh the list of available models"""
        if not self.ollama:
            return []
        
        try:
            models = self.ollama.list_models()
            if hasattr(models, 'models'):
                self._available_models = [model.name.split(':')[0] for model in models.models]
            else:
                self._available_models = ['deepseek-r1', 'stable-code', 'codellama']  # Default fallback
            
            logger.info(f"📋 Available models: {', '.join(self._available_models)}")
            return self._available_models
            
        except Exception as e:
            logger.error(f"❌ Failed to refresh models: {e}")
            return []
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        if not self._available_models:
            self.refresh_available_models()
        return self._available_models
    
    def select_best_model(self, task_type: str, requirements: Optional[Dict[str, int]] = None) -> str:
        """Select the best model for a specific task"""
        available = self.get_available_models()
        
        if not available:
            return 'deepseek-r1'  # Default fallback
        
        # Define task preferences
        task_preferences = {
            'analysis': {'code_analysis': 5, 'reasoning': 4},
            'generation': {'generation': 5, 'code_analysis': 3},
            'conversation': {'conversation': 5, 'reasoning': 3},
            'reasoning': {'reasoning': 5, 'code_analysis': 3},
            'multimodal': {'multimodal': 5, 'reasoning': 3},
            'fast': {'speed': 5}
        }
        
        # Get requirements for task
        if requirements is None:
            requirements = task_preferences.get(task_type, {'reasoning': 3})
        
        # Score available models
        scores = {}
        for model in available:
            if model in self._model_capabilities:
                caps = self._model_capabilities[model]
                score = 0
                
                for requirement, weight in requirements.items():
                    model_capability = caps.get(requirement, 1)
                    score += model_capability * weight
                
                scores[model] = score
        
        if scores:
            best_model = max(scores, key=scores.get)
            logger.debug(f"🎯 Selected {best_model} for {task_type} (score: {scores[best_model]})")
            return best_model
        
        # Fallback selection
        fallback_order = ['deepseek-r1', 'stable-code', 'codellama', 'phi3.5']
        for model in fallback_order:
            if model in available:
                logger.debug(f"🔄 Fallback to {model} for {task_type}")
                return model
        
        return available[0] if available else 'deepseek-r1'
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        if model_name in self._model_capabilities:
            return {
                'name': model_name,
                'capabilities': self._model_capabilities[model_name],
                'available': model_name in self.get_available_models()
            }
        
        return {
            'name': model_name,
            'capabilities': {},
            'available': model_name in self.get_available_models()
        }
    
    def recommend_models_for_task(self, task_type: str, count: int = 3) -> List[str]:
        """Recommend multiple models for a task, ranked by suitability"""
        available = self.get_available_models()
        
        if not available:
            return ['deepseek-r1']
        
        # Get task requirements
        task_preferences = {
            'analysis': {'code_analysis': 5, 'reasoning': 4},
            'generation': {'generation': 5, 'code_analysis': 3},
            'conversation': {'conversation': 5, 'reasoning': 3},
            'reasoning': {'reasoning': 5, 'code_analysis': 3}
        }
        
        requirements = task_preferences.get(task_type, {'reasoning': 3})
        
        # Score and rank models
        model_scores = []
        for model in available:
            if model in self._model_capabilities:
                caps = self._model_capabilities[model]
                score = sum(caps.get(req, 1) * weight for req, weight in requirements.items())
                model_scores.append((model, score))
        
        # Sort by score and return top models
        model_scores.sort(key=lambda x: x[1], reverse=True)
        return [model for model, score in model_scores[:count]]
    
    def validate_model(self, model_name: str) -> bool:
        """Validate that a model is available and working"""
        if not self.ollama:
            return False
        
        available = self.get_available_models()
        return model_name in available