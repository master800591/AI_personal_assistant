#!/usr/bin/env python3
"""
AI Assistant - Main Entry Point
Allows running the package as a module with: python -m ai_assistant
"""

import sys
import asyncio
from .main import main

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))