#!/usr/bin/env python3
"""
Helper Functions
Common utilities and helper functions
"""

import os
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def get_file_hash(file_path: Union[str, Path]) -> str:
    """Get SHA256 hash of a file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Read JSON file safely"""
    path = Path(file_path)
    if not path.exists():
        return {}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def write_json_file(file_path: Union[str, Path], data: Dict[str, Any]) -> None:
    """Write data to JSON file"""
    path = Path(file_path)
    ensure_directory(path.parent)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_python_files(directory: Union[str, Path], recursive: bool = True) -> List[Path]:
    """Get all Python files in a directory"""
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    if recursive:
        return list(dir_path.rglob("*.py"))
    else:
        return list(dir_path.glob("*.py"))

def run_command(
    command: Union[str, List[str]], 
    cwd: Optional[Union[str, Path]] = None,
    capture_output: bool = True,
    timeout: Optional[int] = None
) -> subprocess.CompletedProcess:
    """Run a command safely"""
    if isinstance(command, str):
        # Split command string into list
        command = command.split()
    
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        timeout=timeout
    )

def backup_file(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Path:
    """Create a backup of a file"""
    source_path = Path(file_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")
    
    if backup_dir is None:
        backup_dir = source_path.parent / "backups"
    
    backup_dir = Path(backup_dir)
    ensure_directory(backup_dir)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_path.stem}_{timestamp}{source_path.suffix}"
    backup_path = backup_dir / backup_name
    
    # Copy file
    import shutil
    shutil.copy2(source_path, backup_path)
    
    return backup_path

def is_binary_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is binary"""
    path = Path(file_path)
    if not path.exists():
        return False
    
    try:
        with open(path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return True

def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_bytes(bytes_count: int) -> str:
    """Format byte count as human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"

def get_git_info(repo_path: Union[str, Path] = ".") -> Dict[str, Optional[str]]:
    """Get git repository information"""
    repo_path = Path(repo_path)
    
    info = {
        'branch': None,
        'commit': None,
        'dirty': None,
        'remote': None
    }
    
    try:
        # Get current branch
        result = run_command(['git', 'branch', '--show-current'], cwd=repo_path)
        if result.returncode == 0:
            info['branch'] = result.stdout.strip()
        
        # Get current commit
        result = run_command(['git', 'rev-parse', 'HEAD'], cwd=repo_path)
        if result.returncode == 0:
            info['commit'] = result.stdout.strip()[:8]  # Short hash
        
        # Check if dirty
        result = run_command(['git', 'status', '--porcelain'], cwd=repo_path)
        if result.returncode == 0:
            info['dirty'] = bool(result.stdout.strip())
        
        # Get remote URL
        result = run_command(['git', 'remote', 'get-url', 'origin'], cwd=repo_path)
        if result.returncode == 0:
            info['remote'] = result.stdout.strip()
            
    except Exception:
        pass  # Git not available or not a git repo
    
    return info

def safe_filename(filename: str) -> str:
    """Make a filename safe for filesystem"""
    import re
    # Remove or replace unsafe characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip('. ')
    # Limit length
    return safe_name[:255]

def load_yaml_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load YAML file safely"""
    path = Path(file_path)
    if not path.exists():
        return {}
    
    try:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def save_yaml_file(file_path: Union[str, Path], data: Dict[str, Any]) -> None:
    """Save data to YAML file"""
    path = Path(file_path)
    ensure_directory(path.parent)
    
    try:
        import yaml
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)
    except ImportError:
        # Fallback to JSON if PyYAML not available
        write_json_file(file_path.with_suffix('.json'), data)