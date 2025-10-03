#!/usr/bin/env python3
"""
Create initial GitHub issue for AI Corporation
"""
import requests
import os

def create_initial_issue():
    """Create the first issue for AI Corporation setup"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN not found in environment")
        return False
        
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    issue_data = {
        'title': '🤖 AI Corporation Initial Setup and Self-Evolution System',
        'body': '''## AI Corporation Foundation Setup

This issue tracks the initial deployment and configuration of the AI Corporation system with self-evolution capabilities.

### Core Systems Status
- [x] Self-Evolution System
- [x] Enhanced Discord Bot Integration
- [x] Multi-threaded Architecture  
- [x] GitHub Workflow Management
- [x] Production Environment Setup
- [x] Founder Protection Protocols
- [x] Multi-cloud Deployment

### Development Workflow ✅
- [x] Set up proper branch management (dev/test/production)
- [ ] Configure automated pull request creation
- [ ] Implement milestone tracking
- [ ] Set up continuous deployment pipelines

### Next Evolution Cycles
- [ ] Enhanced AI agent specialization
- [ ] Advanced global operations expansion
- [ ] Autonomous learning system improvements
- [ ] Democratic governance enhancements

**Priority**: Founder Protection → System Protection → Growth Expansion
**Status**: Operational (100% deployment success)
''',
        'labels': ['enhancement', 'ai-corporation', 'priority-high']
    }
    
    print("📝 Creating initial issue...")
    response = requests.post('https://api.github.com/repos/master800591/AI_personal_assistant/issues',
                           headers=headers,
                           json=issue_data)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"✅ Issue created: {issue['html_url']}")
        print(f"Issue #{issue['number']}: {issue['title']}")
        return issue['number']
    else:
        print(f"❌ Failed to create issue: {response.status_code}")
        print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    create_initial_issue()