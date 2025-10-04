#!/usr/bin/env python3
"""
Simple GitHub Setup Script
Initialize repository with labels, milestones, and issues
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment and setup path
load_dotenv()
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Setup GitHub repository"""
    
    print("🐙 AI Corporation GitHub Repository Setup")
    print("=" * 50)
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ No GitHub token found in environment!")
        print("Please set GITHUB_TOKEN in your .env file")
        return
    
    print(f"✅ GitHub token found")
    
    try:
        print("🔧 Creating GitHub manager...")
        from ai_assistant.github.full_automation_manager import FullGitHubManager
        
        config = {
            'founder_name': 'Steve Cornell',
            'founder_github': 'master80059'
        }
        
        # This will automatically initialize the repository
        github_manager = FullGitHubManager(github_token, config)
        
        print("\n🎉 GitHub Repository Setup Complete!")
        print("✅ Labels created")
        print("✅ Milestones created") 
        print("✅ Development branches created")
        print("✅ Initial issues created")
        print("\n📝 Check your repository at:")
        print("https://github.com/master800591/AI_personal_assistant")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()