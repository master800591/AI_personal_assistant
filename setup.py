#!/usr/bin/env python3
"""
Setup configuration for AI Personal Assistant
Professional Python project setup
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    """Read README.md for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI Personal Assistant - Autonomous Development Platform"

# Read requirements
def read_requirements():
    """Read requirements.txt"""
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="ai-personal-assistant",
    version="1.0.0",
    description="Autonomous AI Development Platform with Ollama Integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Steve Cornell",
    author_email="steve.cornell@aicorporation.dev",
    url="https://github.com/master800591/AI_personal_assistant",
    license="MIT",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    python_requires=">=3.8",
    install_requires=read_requirements(),
    
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.15.0"
        ],
        "discord": [
            "discord.py>=2.0.0"
        ],
        "ai": [
            "crewai>=0.1.0",
            "transformers>=4.20.0"
        ]
    },
    
    entry_points={
        "console_scripts": [
            "ai-assistant=ai_assistant.main:main",
            "ai-dev=ai_assistant.autonomous.developer:main",
            "ai-discord=ai_assistant.discord.bot:main",
        ]
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    
    keywords="ai assistant autonomous development ollama discord automation",
    
    project_urls={
        "Bug Reports": "https://github.com/master800591/AI_personal_assistant/issues",
        "Source": "https://github.com/master800591/AI_personal_assistant",
        "Documentation": "https://github.com/master800591/AI_personal_assistant/wiki",
    },
    
    include_package_data=True,
    zip_safe=False,
)