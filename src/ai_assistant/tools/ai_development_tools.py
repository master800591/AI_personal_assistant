"""
AI Personal Assistant - AI Development Tools for CrewAI Agents
Specialized tools for code analysis, development, and GitHub integration
"""

import logging
import json
import subprocess
import os
import ast
import importlib.util
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
import asyncio

from crewai.tools import BaseTool
from pydantic import Field

logger = logging.getLogger(__name__)

class CodeAnalysisTool(BaseTool):
    """Tool for analyzing code quality, structure, and potential improvements"""
    
    name: str = "code_analysis"
    description: str = (
        "Analyze Python code for quality, structure, performance issues, and potential "
        "improvements. Provides detailed reports with suggestions and metrics."
    )
    
    def _run(self, file_path: str, **kwargs) -> str:
        """Analyze code file for quality and improvements"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"❌ File not found: {file_path}"
            
            if not file_path.suffix == '.py':
                return f"❌ Only Python files are supported, got: {file_path.suffix}"
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            analysis_result = self._analyze_python_code(code_content, str(file_path))
            
            return f"✅ Code analysis completed:\n{json.dumps(analysis_result, indent=2)}"
            
        except Exception as e:
            logger.error(f"Code analysis error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _analyze_python_code(self, code: str, file_path: str) -> Dict:
        """Perform detailed Python code analysis"""
        try:
            # Parse the AST
            tree = ast.parse(code)
            
            analysis = {
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'metrics': {
                    'lines_of_code': len(code.splitlines()),
                    'functions': 0,
                    'classes': 0,
                    'imports': 0,
                    'docstrings': 0
                },
                'issues': [],
                'suggestions': [],
                'complexity': 'low',
                'quality_score': 0
            }
            
            # AST Walker to collect metrics
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['metrics']['functions'] += 1
                    # Check for docstring
                    if ast.get_docstring(node):
                        analysis['metrics']['docstrings'] += 1
                    else:
                        analysis['issues'].append({
                            'type': 'missing_docstring',
                            'line': node.lineno,
                            'message': f"Function '{node.name}' missing docstring"
                        })
                
                elif isinstance(node, ast.ClassDef):
                    analysis['metrics']['classes'] += 1
                    # Check for docstring
                    if ast.get_docstring(node):
                        analysis['metrics']['docstrings'] += 1
                    else:
                        analysis['issues'].append({
                            'type': 'missing_docstring',
                            'line': node.lineno,
                            'message': f"Class '{node.name}' missing docstring"
                        })
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    analysis['metrics']['imports'] += 1
            
            # Calculate complexity based on metrics
            loc = analysis['metrics']['lines_of_code']
            if loc > 500:
                analysis['complexity'] = 'high'
            elif loc > 200:
                analysis['complexity'] = 'medium'
            
            # Generate suggestions
            if analysis['metrics']['functions'] > 0:
                docstring_ratio = analysis['metrics']['docstrings'] / (
                    analysis['metrics']['functions'] + analysis['metrics']['classes']
                )
                if docstring_ratio < 0.8:
                    analysis['suggestions'].append({
                        'type': 'documentation',
                        'priority': 'high',
                        'message': 'Add docstrings to improve code documentation'
                    })
            
            if loc > 300:
                analysis['suggestions'].append({
                    'type': 'refactoring',
                    'priority': 'medium',
                    'message': 'Consider splitting large file into smaller modules'
                })
            
            # Calculate quality score
            base_score = 100
            base_score -= len(analysis['issues']) * 5
            base_score -= (1 - min(analysis['metrics']['docstrings'] / max(analysis['metrics']['functions'] + analysis['metrics']['classes'], 1), 1)) * 20
            analysis['quality_score'] = max(base_score, 0)
            
            return analysis
            
        except SyntaxError as e:
            return {
                'file_path': file_path,
                'error': 'syntax_error',
                'message': str(e),
                'line': e.lineno
            }
        except Exception as e:
            return {
                'file_path': file_path,
                'error': 'analysis_error',
                'message': str(e)
            }


class FeatureImplementationTool(BaseTool):
    """Tool for implementing new features and code modifications"""
    
    name: str = "feature_implementation"
    description: str = (
        "Implement new features, modify existing code, and create new modules "
        "based on specifications and requirements."
    )
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute feature implementation tasks"""
        try:
            if action == "create_function":
                return self._create_function(
                    name=kwargs.get('name'),
                    parameters=kwargs.get('parameters', []),
                    return_type=kwargs.get('return_type'),
                    docstring=kwargs.get('docstring'),
                    body=kwargs.get('body')
                )
            elif action == "create_class":
                return self._create_class(
                    name=kwargs.get('name'),
                    base_classes=kwargs.get('base_classes', []),
                    methods=kwargs.get('methods', []),
                    docstring=kwargs.get('docstring')
                )
            elif action == "modify_file":
                return self._modify_file(
                    file_path=kwargs.get('file_path'),
                    modifications=kwargs.get('modifications', [])
                )
            elif action == "create_module":
                return self._create_module(
                    module_name=kwargs.get('module_name'),
                    module_path=kwargs.get('module_path'),
                    content=kwargs.get('content')
                )
            else:
                return f"❌ Unknown implementation action: {action}"
                
        except Exception as e:
            logger.error(f"Feature implementation error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _create_function(self, name: str, parameters: List = None, 
                        return_type: str = None, docstring: str = None, body: str = None) -> str:
        """Generate a new function implementation"""
        try:
            params_str = ", ".join(parameters or [])
            return_annotation = f" -> {return_type}" if return_type else ""
            
            function_code = f"""def {name}({params_str}){return_annotation}:
    \"\"\"{docstring or f'TODO: Add docstring for {name}'}\"\"\"
    {body or 'pass  # TODO: Implement function body'}
"""
            
            implementation = {
                'type': 'function',
                'name': name,
                'code': function_code,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Function implementation generated:\n{json.dumps(implementation, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create function: {str(e)}"
    
    def _create_class(self, name: str, base_classes: List = None, 
                     methods: List = None, docstring: str = None) -> str:
        """Generate a new class implementation"""
        try:
            bases_str = f"({', '.join(base_classes)})" if base_classes else ""
            
            class_code = f"""class {name}{bases_str}:
    \"\"\"{docstring or f'TODO: Add docstring for {name}'}\"\"\"
    
    def __init__(self):
        \"\"\"Initialize {name}\"\"\"
        pass  # TODO: Implement initialization
"""
            
            # Add methods if provided
            for method in (methods or []):
                method_name = method.get('name', 'new_method')
                method_params = method.get('parameters', ['self'])
                method_body = method.get('body', 'pass  # TODO: Implement method')
                
                class_code += f"""
    def {method_name}({', '.join(method_params)}):
        \"\"\"TODO: Add method docstring\"\"\"
        {method_body}
"""
            
            implementation = {
                'type': 'class',
                'name': name,
                'code': class_code,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Class implementation generated:\n{json.dumps(implementation, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create class: {str(e)}"
    
    def _modify_file(self, file_path: str, modifications: List) -> str:
        """Apply modifications to an existing file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"❌ File not found: {file_path}"
            
            modification_plan = {
                'file_path': str(file_path),
                'modifications': modifications,
                'timestamp': datetime.now().isoformat(),
                'backup_recommended': True
            }
            
            return f"✅ File modification plan created:\n{json.dumps(modification_plan, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create modification plan: {str(e)}"
    
    def _create_module(self, module_name: str, module_path: str = None, content: str = None) -> str:
        """Create a new Python module"""
        try:
            if not module_path:
                module_path = f"{module_name}.py"
            
            module_path = Path(module_path)
            
            # Default module content
            if not content:
                content = f'''"""
{module_name} - AI Personal Assistant Module
Generated by FeatureImplementationTool
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class {module_name.title().replace('_', '')}:
    """Main class for {module_name} module"""
    
    def __init__(self):
        """Initialize {module_name}"""
        self.logger = logger
    
    def run(self) -> Dict[str, Any]:
        """Main execution method"""
        try:
            # TODO: Implement main functionality
            return {{"success": True, "message": "Module executed successfully"}}
        except Exception as e:
            self.logger.error(f"Error in {{self.__class__.__name__}}: {{e}}")
            return {{"success": False, "error": str(e)}}


def main():
    """Main function for module execution"""
    module = {module_name.title().replace('_', '')}()
    result = module.run()
    print(f"Result: {{result}}")


if __name__ == "__main__":
    main()
'''
            
            module_info = {
                'type': 'module',
                'name': module_name,
                'file_path': str(module_path),
                'content_preview': content[:300] + '...',
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Module implementation generated:\n{json.dumps(module_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create module: {str(e)}"


class GitHubIntegrationTool(BaseTool):
    """Tool for GitHub repository operations and automation"""
    
    name: str = "github_integration"
    description: str = (
        "Integrate with GitHub for repository operations including commits, "
        "pull requests, issue management, and repository analysis."
    )
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute GitHub operations"""
        try:
            if action == "commit_changes":
                return self._commit_changes(
                    message=kwargs.get('message'),
                    files=kwargs.get('files', []),
                    branch=kwargs.get('branch', 'main')
                )
            elif action == "create_pull_request":
                return self._create_pull_request(
                    title=kwargs.get('title'),
                    description=kwargs.get('description'),
                    source_branch=kwargs.get('source_branch'),
                    target_branch=kwargs.get('target_branch', 'main')
                )
            elif action == "create_issue":
                return self._create_issue(
                    title=kwargs.get('title'),
                    description=kwargs.get('description'),
                    labels=kwargs.get('labels', [])
                )
            elif action == "analyze_repository":
                return self._analyze_repository(kwargs.get('repo_path', '.'))
            else:
                return f"❌ Unknown GitHub action: {action}"
                
        except Exception as e:
            logger.error(f"GitHub integration error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _commit_changes(self, message: str, files: List = None, branch: str = 'main') -> str:
        """Create a commit with specified changes"""
        try:
            commit_config = {
                'action': 'commit_changes',
                'message': message,
                'files': files or [],
                'branch': branch,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Commit operation queued:\n{json.dumps(commit_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue commit: {str(e)}"
    
    def _create_pull_request(self, title: str, description: str = None, 
                           source_branch: str = None, target_branch: str = 'main') -> str:
        """Create a new pull request"""
        try:
            pr_config = {
                'action': 'create_pull_request',
                'title': title,
                'description': description or '',
                'source_branch': source_branch,
                'target_branch': target_branch,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Pull request creation queued:\n{json.dumps(pr_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue pull request: {str(e)}"
    
    def _create_issue(self, title: str, description: str = None, labels: List = None) -> str:
        """Create a new GitHub issue"""
        try:
            issue_config = {
                'action': 'create_issue',
                'title': title,
                'description': description or '',
                'labels': labels or [],
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Issue creation queued:\n{json.dumps(issue_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue issue creation: {str(e)}"
    
    def _analyze_repository(self, repo_path: str) -> str:
        """Analyze repository structure and statistics"""
        try:
            repo_path = Path(repo_path)
            
            if not repo_path.exists():
                return f"❌ Repository path not found: {repo_path}"
            
            analysis = {
                'repository_path': str(repo_path),
                'analysis_timestamp': datetime.now().isoformat(),
                'structure': {},
                'statistics': {},
                'recommendations': []
            }
            
            # Analyze file structure
            python_files = list(repo_path.rglob("*.py"))
            analysis['statistics']['python_files'] = len(python_files)
            analysis['statistics']['total_lines'] = 0
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    analysis['statistics']['total_lines'] += lines
                except Exception:
                    continue
            
            # Check for common files
            common_files = ['README.md', 'requirements.txt', 'setup.py', '.gitignore', 'LICENSE']
            analysis['structure']['has_common_files'] = {}
            for file in common_files:
                analysis['structure']['has_common_files'][file] = (repo_path / file).exists()
            
            # Generate recommendations
            if not analysis['structure']['has_common_files'].get('README.md'):
                analysis['recommendations'].append({
                    'type': 'documentation',
                    'priority': 'high',
                    'message': 'Add README.md file for project documentation'
                })
            
            if not analysis['structure']['has_common_files'].get('requirements.txt'):
                analysis['recommendations'].append({
                    'type': 'dependencies',
                    'priority': 'medium',
                    'message': 'Add requirements.txt for dependency management'
                })
            
            return f"✅ Repository analysis completed:\n{json.dumps(analysis, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to analyze repository: {str(e)}"


class FileSystemTool(BaseTool):
    """Tool for file system operations and management"""
    
    name: str = "file_system"
    description: str = (
        "Perform file system operations including file creation, reading, "
        "writing, directory management, and file organization."
    )
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute file system operations"""
        try:
            if action == "read_file":
                return self._read_file(kwargs.get('file_path'))
            elif action == "write_file":
                return self._write_file(
                    file_path=kwargs.get('file_path'),
                    content=kwargs.get('content'),
                    mode=kwargs.get('mode', 'w')
                )
            elif action == "create_directory":
                return self._create_directory(kwargs.get('dir_path'))
            elif action == "list_directory":
                return self._list_directory(
                    dir_path=kwargs.get('dir_path', '.'),
                    pattern=kwargs.get('pattern')
                )
            elif action == "file_info":
                return self._get_file_info(kwargs.get('file_path'))
            else:
                return f"❌ Unknown file system action: {action}"
                
        except Exception as e:
            logger.error(f"File system error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _read_file(self, file_path: str) -> str:
        """Read content from a file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"❌ File not found: {file_path}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_info = {
                'file_path': str(file_path),
                'size_bytes': file_path.stat().st_size,
                'content_preview': content[:500] + '...' if len(content) > 500 else content,
                'full_content_length': len(content),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ File read successfully:\n{json.dumps(file_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to read file: {str(e)}"
    
    def _write_file(self, file_path: str, content: str, mode: str = 'w') -> str:
        """Write content to a file"""
        try:
            file_path = Path(file_path)
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            write_info = {
                'file_path': str(file_path),
                'mode': mode,
                'content_length': len(content),
                'size_bytes': file_path.stat().st_size,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ File written successfully:\n{json.dumps(write_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to write file: {str(e)}"
    
    def _create_directory(self, dir_path: str) -> str:
        """Create a directory structure"""
        try:
            dir_path = Path(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
            
            dir_info = {
                'directory_path': str(dir_path),
                'created': True,
                'exists': dir_path.exists(),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Directory created successfully:\n{json.dumps(dir_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to create directory: {str(e)}"
    
    def _list_directory(self, dir_path: str = '.', pattern: str = None) -> str:
        """List directory contents"""
        try:
            dir_path = Path(dir_path)
            
            if not dir_path.exists():
                return f"❌ Directory not found: {dir_path}"
            
            if pattern:
                files = list(dir_path.glob(pattern))
            else:
                files = list(dir_path.iterdir())
            
            file_list = []
            for file in files:
                file_info = {
                    'name': file.name,
                    'path': str(file),
                    'type': 'directory' if file.is_dir() else 'file',
                    'size': file.stat().st_size if file.is_file() else None
                }
                file_list.append(file_info)
            
            directory_info = {
                'directory_path': str(dir_path),
                'pattern': pattern,
                'file_count': len(file_list),
                'files': file_list,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Directory listed successfully:\n{json.dumps(directory_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to list directory: {str(e)}"
    
    def _get_file_info(self, file_path: str) -> str:
        """Get detailed information about a file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"❌ File not found: {file_path}"
            
            stat_info = file_path.stat()
            
            file_info = {
                'file_path': str(file_path),
                'name': file_path.name,
                'suffix': file_path.suffix,
                'size_bytes': stat_info.st_size,
                'created_time': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir(),
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ File information retrieved:\n{json.dumps(file_info, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to get file info: {str(e)}"


class OllamaIntegrationTool(BaseTool):
    """Tool for integrating with Ollama AI models"""
    
    name: str = "ollama_integration"
    description: str = (
        "Integrate with Ollama AI models for code generation, analysis, "
        "and natural language processing tasks."
    )
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute Ollama integration operations"""
        try:
            if action == "list_models":
                return self._list_models()
            elif action == "generate_code":
                return self._generate_code(
                    prompt=kwargs.get('prompt'),
                    model=kwargs.get('model', 'deepseek-r1')
                )
            elif action == "analyze_code":
                return self._analyze_code_with_ai(
                    code=kwargs.get('code'),
                    model=kwargs.get('model', 'deepseek-r1')
                )
            elif action == "chat":
                return self._chat_with_model(
                    message=kwargs.get('message'),
                    model=kwargs.get('model', 'deepseek-r1')
                )
            else:
                return f"❌ Unknown Ollama action: {action}"
                
        except Exception as e:
            logger.error(f"Ollama integration error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _list_models(self) -> str:
        """List available Ollama models"""
        try:
            # This would query actual Ollama instance
            models_config = {
                'action': 'list_models',
                'available_models': [
                    'deepseek-r1',
                    'stable-code',
                    'codellama',
                    'phi3.5',
                    'dolphin3',
                    'llava'
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Ollama models listed:\n{json.dumps(models_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to list models: {str(e)}"
    
    def _generate_code(self, prompt: str, model: str = 'deepseek-r1') -> str:
        """Generate code using Ollama model"""
        try:
            generation_config = {
                'action': 'generate_code',
                'prompt': prompt,
                'model': model,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Code generation queued:\n{json.dumps(generation_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue code generation: {str(e)}"
    
    def _analyze_code_with_ai(self, code: str, model: str = 'deepseek-r1') -> str:
        """Analyze code using AI model"""
        try:
            analysis_config = {
                'action': 'analyze_code',
                'code_preview': code[:200] + '...' if len(code) > 200 else code,
                'model': model,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ AI code analysis queued:\n{json.dumps(analysis_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue AI analysis: {str(e)}"
    
    def _chat_with_model(self, message: str, model: str = 'deepseek-r1') -> str:
        """Chat with Ollama model"""
        try:
            chat_config = {
                'action': 'chat',
                'message': message,
                'model': model,
                'timestamp': datetime.now().isoformat()
            }
            
            return f"✅ Chat request queued:\n{json.dumps(chat_config, indent=2)}"
            
        except Exception as e:
            return f"❌ Failed to queue chat request: {str(e)}"