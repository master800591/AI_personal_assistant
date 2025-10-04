#!/usr/bin/env python3
"""
GitHub Manager - Full Repository Automation
Complete GitHub repository management with issues, PRs, milestones, and workflows
Founder: Steve Cornell (master80059)
"""

import logging
import requests
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

logger = logging.getLogger(__name__)

class FullGitHubManager:
    """Complete GitHub repository automation manager"""
    
    def __init__(self, token: str, config: Dict[str, Any] = None):
        """Initialize GitHub manager with full API access"""
        self.token = token
        self.config = config or {}
        self.base_url = "https://api.github.com"
        self.repo_owner = "master800591"
        self.repo_name = "AI_personal_assistant"
        
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        logger.info("🐙 Full GitHub Manager initialized")
        
        # Initialize repository structure
        self.initialize_repository()
    
    def initialize_repository(self):
        """Initialize complete repository structure"""
        try:
            logger.info("🔧 Initializing repository structure...")
            
            # Create labels
            self.create_standard_labels()
            
            # Create milestones
            self.create_project_milestones()
            
            # Create branches
            self.create_development_branches()
            
            # Create initial issues
            self.create_initial_issues()
            
            logger.info("✅ Repository structure initialized")
            
        except Exception as e:
            logger.error(f"❌ Repository initialization error: {e}")
    
    def create_standard_labels(self):
        """Create standard labels for the repository"""
        
        labels = [
            # Priority Labels
            {"name": "priority-critical", "color": "B60205", "description": "Critical priority issue"},
            {"name": "priority-high", "color": "D93F0B", "description": "High priority issue"},
            {"name": "priority-medium", "color": "FBCA04", "description": "Medium priority issue"},
            {"name": "priority-low", "color": "0E8A16", "description": "Low priority issue"},
            
            # Type Labels
            {"name": "type-bug", "color": "D73A4A", "description": "Something isn't working"},
            {"name": "type-feature", "color": "A2EEEF", "description": "New feature or request"},
            {"name": "type-enhancement", "color": "7057FF", "description": "Enhancement to existing feature"},
            {"name": "type-documentation", "color": "0075CA", "description": "Improvements or additions to documentation"},
            {"name": "type-refactor", "color": "F9D0C4", "description": "Code refactoring"},
            
            # Component Labels
            {"name": "component-discord", "color": "5865F2", "description": "Discord bot related"},
            {"name": "component-crewai", "color": "FF6B6B", "description": "CrewAI agent related"},
            {"name": "component-github", "color": "24292E", "description": "GitHub integration related"},
            {"name": "component-ollama", "color": "4ECDC4", "description": "Ollama integration related"},
            {"name": "component-api", "color": "FFE66D", "description": "API related"},
            
            # Status Labels
            {"name": "status-in-progress", "color": "FFF3CD", "description": "Currently being worked on"},
            {"name": "status-review", "color": "D1ECF1", "description": "Ready for review"},
            {"name": "status-testing", "color": "D4EDDA", "description": "In testing phase"},
            {"name": "status-blocked", "color": "F8D7DA", "description": "Blocked by dependencies"},
            
            # AI Labels
            {"name": "ai-agent", "color": "8B5CF6", "description": "AI agent task"},
            {"name": "ai-automation", "color": "EC4899", "description": "Automation related"},
            {"name": "ai-learning", "color": "10B981", "description": "AI learning and improvement"},
            
            # Workflow Labels
            {"name": "workflow-dev", "color": "34D399", "description": "Development workflow"},
            {"name": "workflow-testing", "color": "FBBF24", "description": "Testing workflow"},
            {"name": "workflow-production", "color": "EF4444", "description": "Production workflow"}
        ]
        
        for label in labels:
            self.create_label(label)
    
    def create_label(self, label_data: Dict[str, str]):
        """Create a single label"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/labels"
            
            response = requests.post(url, headers=self.headers, json=label_data)
            
            if response.status_code == 201:
                logger.info(f"🏷️ Created label: {label_data['name']}")
            elif response.status_code == 422:
                # Label already exists, update it
                self.update_label(label_data)
            else:
                logger.warning(f"⚠️ Label creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Label creation error: {e}")
    
    def update_label(self, label_data: Dict[str, str]):
        """Update an existing label"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/labels/{label_data['name']}"
            
            response = requests.patch(url, headers=self.headers, json=label_data)
            
            if response.status_code == 200:
                logger.info(f"🔄 Updated label: {label_data['name']}")
                
        except Exception as e:
            logger.error(f"❌ Label update error: {e}")
    
    def create_project_milestones(self):
        """Create project milestones"""
        
        milestones = [
            {
                "title": "Q4 2025 - AI Enhancement",
                "description": "Major AI capabilities enhancement and optimization",
                "due_on": "2025-12-31T23:59:59Z",
                "state": "open"
            },
            {
                "title": "Q4 2025 - Discord Integration",
                "description": "Complete Discord server automation and integration",
                "due_on": "2025-11-30T23:59:59Z", 
                "state": "open"
            },
            {
                "title": "Q4 2025 - GitHub Automation",
                "description": "Full GitHub repository automation and workflows",
                "due_on": "2025-11-15T23:59:59Z",
                "state": "open"
            },
            {
                "title": "Q1 2026 - Production Release",
                "description": "Production-ready release with all features",
                "due_on": "2026-03-31T23:59:59Z",
                "state": "open"
            }
        ]
        
        for milestone in milestones:
            self.create_milestone(milestone)
    
    def create_milestone(self, milestone_data: Dict[str, str]):
        """Create a single milestone"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/milestones"
            
            response = requests.post(url, headers=self.headers, json=milestone_data)
            
            if response.status_code == 201:
                logger.info(f"🎯 Created milestone: {milestone_data['title']}")
            else:
                logger.warning(f"⚠️ Milestone creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Milestone creation error: {e}")
    
    def create_development_branches(self):
        """Create development workflow branches"""
        
        branches = ["dev", "testing", "staging"]
        
        # Get main branch SHA
        main_sha = self.get_branch_sha("main")
        if not main_sha:
            logger.error("❌ Could not get main branch SHA")
            return
        
        for branch_name in branches:
            self.create_branch(branch_name, main_sha)
    
    def get_branch_sha(self, branch_name: str) -> Optional[str]:
        """Get SHA of a branch"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/git/refs/heads/{branch_name}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return data["object"]["sha"]
            else:
                logger.warning(f"⚠️ Could not get {branch_name} SHA: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Branch SHA error: {e}")
            return None
    
    def create_branch(self, branch_name: str, sha: str):
        """Create a new branch"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/git/refs"
            
            data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                logger.info(f"🌿 Created branch: {branch_name}")
            elif response.status_code == 422:
                logger.info(f"ℹ️ Branch {branch_name} already exists")
            else:
                logger.warning(f"⚠️ Branch creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Branch creation error: {e}")
    
    def create_initial_issues(self):
        """Create initial development issues"""
        
        issues = [
            {
                "title": "🤖 Enhance Discord Bot Server Management",
                "body": """## Description
Complete the Discord bot server management capabilities with full automation.

## Tasks
- [x] Create complete channel structure
- [x] Setup roles and permissions  
- [x] Implement automated notifications
- [ ] Add voice channel management
- [ ] Create custom server templates
- [ ] Add member onboarding automation

## Acceptance Criteria
- All channels are created automatically
- Roles are assigned correctly
- Voice channels work properly
- Notifications are sent reliably

## Related Components
- Discord Bot
- Server Management
- User Experience
""",
                "labels": ["type-enhancement", "component-discord", "priority-high", "ai-automation"],
                "milestone": "Q4 2025 - Discord Integration"
            },
            {
                "title": "🔧 GitHub Repository Automation",
                "body": """## Description  
Implement complete GitHub repository automation including issues, PRs, and workflows.

## Tasks
- [x] Create standard labels
- [x] Setup milestones
- [x] Create development branches
- [ ] Implement automated issue creation
- [ ] Setup PR templates
- [ ] Create GitHub Actions workflows
- [ ] Add automated testing

## Acceptance Criteria
- Issues are created automatically
- PRs follow standard template
- All workflows function correctly
- Testing is automated

## Related Components
- GitHub Integration
- CI/CD
- Automation
""",
                "labels": ["type-feature", "component-github", "priority-high", "workflow-dev"],
                "milestone": "Q4 2025 - GitHub Automation"
            },
            {
                "title": "🧠 CrewAI Agent Coordination Enhancement",
                "body": """## Description
Improve coordination between CrewAI agents for better collaboration and task management.

## Tasks
- [ ] Implement agent communication protocols
- [ ] Add shared knowledge base
- [ ] Create task prioritization system
- [ ] Add conflict resolution
- [ ] Implement progress tracking
- [ ] Add performance metrics

## Acceptance Criteria
- Agents communicate effectively
- Knowledge is shared properly
- Tasks are prioritized correctly
- Conflicts are resolved automatically

## Related Components
- CrewAI System
- AI Agents
- Knowledge Management
""",
                "labels": ["type-enhancement", "component-crewai", "priority-medium", "ai-agent"],
                "milestone": "Q4 2025 - AI Enhancement"
            },
            {
                "title": "📊 Real-time Dashboard Implementation",
                "body": """## Description
Create a comprehensive real-time dashboard for monitoring all AI Corporation activities.

## Tasks
- [ ] Design dashboard layout
- [ ] Implement real-time updates
- [ ] Add Discord activity monitoring
- [ ] Add GitHub activity tracking
- [ ] Create performance metrics
- [ ] Add alerting system

## Acceptance Criteria
- Dashboard updates in real-time
- All activities are tracked
- Metrics are accurate
- Alerts work properly

## Related Components
- Dashboard
- Monitoring
- Analytics
""",
                "labels": ["type-feature", "component-api", "priority-medium", "ai-automation"],
                "milestone": "Q4 2025 - AI Enhancement"
            },
            {
                "title": "🔐 Security and Authentication System",
                "body": """## Description
Implement comprehensive security and authentication for the AI Corporation platform.

## Tasks
- [ ] OAuth2 integration
- [ ] Role-based access control
- [ ] API rate limiting
- [ ] Security audit logging
- [ ] Encryption implementation
- [ ] Vulnerability scanning

## Acceptance Criteria
- All endpoints are secured
- Rate limiting works properly
- Audit logs are complete
- No security vulnerabilities

## Related Components
- Security
- Authentication
- API
""",
                "labels": ["type-feature", "priority-critical", "component-api", "workflow-production"],
                "milestone": "Q1 2026 - Production Release"
            }
        ]
        
        for issue in issues:
            self.create_issue(issue)
    
    def create_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a GitHub issue"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            
            # Get milestone number if specified
            milestone_number = None
            if "milestone" in issue_data:
                milestone_number = self.get_milestone_number(issue_data["milestone"])
                if milestone_number:
                    issue_data["milestone"] = milestone_number
                else:
                    del issue_data["milestone"]
            
            response = requests.post(url, headers=self.headers, json=issue_data)
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"📝 Created issue: {issue_data['title']} (#{data['number']})")
                return {
                    "success": True,
                    "number": data["number"],
                    "url": data["html_url"],
                    "data": data
                }
            else:
                logger.error(f"❌ Issue creation failed: {response.status_code}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"❌ Issue creation error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_milestone_number(self, milestone_title: str) -> Optional[int]:
        """Get milestone number by title"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/milestones"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                milestones = response.json()
                for milestone in milestones:
                    if milestone["title"] == milestone_title:
                        return milestone["number"]
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Milestone lookup error: {e}")
            return None
    
    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> Dict[str, Any]:
        """Create a pull request"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/pulls"
            
            data = {
                "title": title,
                "body": body,
                "head": head,
                "base": base
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                pr_data = response.json()
                logger.info(f"🔄 Created PR: {title} (#{pr_data['number']})")
                return {
                    "success": True,
                    "number": pr_data["number"],
                    "url": pr_data["html_url"],
                    "data": pr_data
                }
            else:
                logger.error(f"❌ PR creation failed: {response.status_code}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"❌ PR creation error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Repository info failed: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Repository info error: {e}")
            return {}
    
    def get_issues(self, state: str = "open", labels: str = None) -> List[Dict[str, Any]]:
        """Get repository issues"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            
            params = {"state": state}
            if labels:
                params["labels"] = labels
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Get issues failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Get issues error: {e}")
            return []
    
    def assign_issue(self, issue_number: int, assignees: List[str]) -> bool:
        """Assign issue to users"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/assignees"
            
            data = {"assignees": assignees}
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                logger.info(f"👤 Assigned issue #{issue_number} to {', '.join(assignees)}")
                return True
            else:
                logger.error(f"❌ Issue assignment failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Issue assignment error: {e}")
            return False
    
    def close_issue(self, issue_number: int, comment: str = None) -> bool:
        """Close an issue"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
            
            data = {"state": "closed"}
            
            response = requests.patch(url, headers=self.headers, json=data)
            
            if response.status_code == 200:
                logger.info(f"✅ Closed issue #{issue_number}")
                
                # Add closing comment if provided
                if comment:
                    self.add_issue_comment(issue_number, comment)
                
                return True
            else:
                logger.error(f"❌ Issue closing failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Issue closing error: {e}")
            return False
    
    def add_issue_comment(self, issue_number: int, comment: str) -> bool:
        """Add comment to an issue"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
            
            data = {"body": comment}
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                logger.info(f"💬 Added comment to issue #{issue_number}")
                return True
            else:
                logger.error(f"❌ Comment addition failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Comment addition error: {e}")
            return False
    
    def create_workflow_automation(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete workflow automation for an issue"""
        try:
            # 1. Create the issue
            issue_result = self.create_issue(issue_data)
            
            if not issue_result["success"]:
                return issue_result
            
            issue_number = issue_result["number"]
            
            # 2. Create feature branch
            branch_name = f"feature/issue-{issue_number}"
            main_sha = self.get_branch_sha("main")
            if main_sha:
                self.create_branch(branch_name, main_sha)
            
            # 3. Auto-assign to AI agents (simulate)
            self.assign_issue(issue_number, ["master800591"])  # Assign to founder
            
            # 4. Add automated comment
            automation_comment = f"""🤖 **Automated Workflow Initiated**

This issue has been automatically processed with:
- ✅ Issue created and labeled
- ✅ Feature branch `{branch_name}` created
- ✅ Assigned to development team
- 🔄 Ready for development

**Next Steps:**
1. Development work on feature branch
2. Create pull request to `dev` branch
3. Testing phase in `testing` branch
4. Production deployment to `main` branch

*This is an automated message from AI Corporation Bot*"""
            
            self.add_issue_comment(issue_number, automation_comment)
            
            return {
                "success": True,
                "issue_number": issue_number,
                "branch_name": branch_name,
                "workflow": "initiated"
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow automation error: {e}")
            return {"success": False, "error": str(e)}