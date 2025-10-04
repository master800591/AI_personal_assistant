"""
GitHub Integration for AI Personal Assistant
Founder: Steve Cornell (master80059)
Automated repository management and CI/CD
"""

import os
import git
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from github import Github
from datetime import datetime

class GitHubAutomation:
    """GitHub automation and repository management"""
    
    def __init__(self, token: str, repo_name: str = "AI_personal_assistant"):
        self.token = token
        self.repo_name = repo_name
        self.github = Github(token)
        self.logger = logging.getLogger(__name__)
        
        # Get repository
        try:
            self.repo = self.github.get_repo(f"master800591/{repo_name}")
            self.local_repo = git.Repo(".")
            self.logger.info(f"✅ Connected to repository: {self.repo.full_name}")
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to GitHub: {e}")
            self.repo = None
            self.local_repo = None
    
    def is_connected(self) -> bool:
        """Check if GitHub connection is working"""
        return self.repo is not None and self.local_repo is not None
    
    async def create_automated_commit(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Create automated commit for AI changes"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            # Add files to git
            if files:
                for file_path in files:
                    if Path(file_path).exists():
                        self.local_repo.index.add([file_path])
            else:
                # Add all changes
                self.local_repo.git.add('.')
            
            # Create commit
            commit_message = f"[AI-DEV] {message}"
            commit = self.local_repo.index.commit(commit_message)
            
            self.logger.info(f"📝 Created commit: {commit.hexsha[:8]} - {commit_message}")
            
            return {
                "success": True,
                "commit_hash": commit.hexsha,
                "message": commit_message,
                "files_changed": len(files) if files else "all"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create commit: {e}")
            return {"success": False, "error": str(e)}
    
    async def push_changes(self, branch: str = "main") -> Dict[str, Any]:
        """Push local changes to GitHub"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            # Push to origin
            origin = self.local_repo.remote('origin')
            push_info = origin.push(branch)
            
            self.logger.info(f"⬆️ Pushed changes to {branch}")
            
            return {
                "success": True,
                "branch": branch,
                "push_info": str(push_info)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to push changes: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_feature_branch(self, branch_name: str, base_branch: str = "main") -> Dict[str, Any]:
        """Create a new feature branch"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            # Create and checkout new branch
            new_branch = self.local_repo.create_head(branch_name, base_branch)
            new_branch.checkout()
            
            self.logger.info(f"🌿 Created and switched to branch: {branch_name}")
            
            return {
                "success": True,
                "branch_name": branch_name,
                "base_branch": base_branch,
                "current_branch": self.local_repo.active_branch.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create branch: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_pull_request(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> Dict[str, Any]:
        """Create a pull request"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            pr = self.repo.create_pull(
                title=f"[AI-DEV] {title}",
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            self.logger.info(f"📋 Created pull request: #{pr.number} - {title}")
            
            return {
                "success": True,
                "pr_number": pr.number,
                "pr_url": pr.html_url,
                "title": title,
                "head_branch": head_branch,
                "base_branch": base_branch
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create pull request: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a GitHub issue"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            # Add AI-DEV label by default
            issue_labels = labels or []
            if "AI-DEV" not in issue_labels:
                issue_labels.append("AI-DEV")
            
            issue = self.repo.create_issue(
                title=f"[AI-DEV] {title}",
                body=body,
                labels=issue_labels
            )
            
            self.logger.info(f"🐛 Created issue: #{issue.number} - {title}")
            
            return {
                "success": True,
                "issue_number": issue.number,
                "issue_url": issue.html_url,
                "title": title,
                "labels": issue_labels
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create issue: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_repository_status(self) -> Dict[str, Any]:
        """Get current repository status"""
        if not self.is_connected():
            return {"connected": False, "error": "Not connected to GitHub"}
        
        try:
            # Local repo info
            current_branch = self.local_repo.active_branch.name
            is_dirty = self.local_repo.is_dirty()
            untracked = len(self.local_repo.untracked_files)
            
            # Remote repo info
            open_prs = len(list(self.repo.get_pulls(state='open')))
            open_issues = len(list(self.repo.get_issues(state='open')))
            
            # Recent commits
            commits = list(self.repo.get_commits()[:5])
            recent_commits = [
                {
                    "sha": commit.sha[:8],
                    "message": commit.commit.message.split('\n')[0],
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat()
                }
                for commit in commits
            ]
            
            return {
                "connected": True,
                "repository": self.repo.full_name,
                "current_branch": current_branch,
                "has_changes": is_dirty,
                "untracked_files": untracked,
                "open_pull_requests": open_prs,
                "open_issues": open_issues,
                "recent_commits": recent_commits
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get repository status: {e}")
            return {"connected": False, "error": str(e)}
    
    async def deploy_to_production(self, version: str = None) -> Dict[str, Any]:
        """Deploy changes to production"""
        if not self.is_connected():
            return {"success": False, "error": "Not connected to GitHub"}
        
        try:
            # Create deployment tag
            if not version:
                version = f"v1.0.{datetime.now().strftime('%Y%m%d%H%M')}"
            
            # Tag current commit
            latest_commit = self.local_repo.head.commit
            tag = self.local_repo.create_tag(version, ref=latest_commit, message=f"AI-DEV Release {version}")
            
            # Push tag
            origin = self.local_repo.remote('origin')
            origin.push(tags=True)
            
            self.logger.info(f"🚀 Deployed to production: {version}")
            
            return {
                "success": True,
                "version": version,
                "commit_hash": latest_commit.hexsha,
                "deployment_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to deploy: {e}")
            return {"success": False, "error": str(e)}

class CI_CD_Pipeline:
    """CI/CD pipeline management"""
    
    def __init__(self, github_automation: GitHubAutomation):
        self.github = github_automation
        self.logger = logging.getLogger(__name__)
    
    async def run_automated_workflow(self, trigger: str = "development_cycle") -> Dict[str, Any]:
        """Run automated development workflow"""
        workflow_steps = []
        
        try:
            # Step 1: Create feature branch
            branch_name = f"ai-dev-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            branch_result = await self.github.create_feature_branch(branch_name)
            workflow_steps.append({"step": "create_branch", "result": branch_result})
            
            if not branch_result["success"]:
                return {"success": False, "error": "Failed to create branch", "steps": workflow_steps}
            
            # Step 2: Commit changes (if any)
            if self.github.local_repo.is_dirty() or self.github.local_repo.untracked_files:
                commit_result = await self.github.create_automated_commit(f"AI development cycle - {trigger}")
                workflow_steps.append({"step": "commit_changes", "result": commit_result})
                
                if commit_result["success"]:
                    # Step 3: Push changes
                    push_result = await self.github.push_changes(branch_name)
                    workflow_steps.append({"step": "push_changes", "result": push_result})
                    
                    if push_result["success"]:
                        # Step 4: Create pull request
                        pr_body = f"""
## AI Development Cycle Results

**Trigger:** {trigger}
**Branch:** {branch_name}
**Timestamp:** {datetime.now().isoformat()}

### Changes Made:
- Automated code improvements
- Feature implementations
- Bug fixes and optimizations

### Review Notes:
This pull request was automatically generated by the AI Personal Assistant development system.
Please review the changes and merge if approved.

**Founder:** Steve Cornell (master80059)
**System:** AI Personal Assistant CrewAI
                        """
                        
                        pr_result = await self.github.create_pull_request(
                            title=f"AI Development Cycle - {trigger}",
                            body=pr_body,
                            head_branch=branch_name
                        )
                        workflow_steps.append({"step": "create_pr", "result": pr_result})
            
            return {
                "success": True,
                "branch_name": branch_name,
                "workflow_steps": workflow_steps,
                "trigger": trigger,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Workflow failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "workflow_steps": workflow_steps
            }

# Factory functions
def create_github_automation(token: str = None) -> GitHubAutomation:
    """Create GitHub automation instance"""
    if not token:
        token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        raise ValueError("GitHub token required - set GITHUB_TOKEN environment variable")
    
    return GitHubAutomation(token)

def create_cicd_pipeline(github_automation: GitHubAutomation) -> CI_CD_Pipeline:
    """Create CI/CD pipeline instance"""
    return CI_CD_Pipeline(github_automation)

# Main testing
if __name__ == "__main__":
    import asyncio
    
    async def test_github_integration():
        logging.basicConfig(level=logging.INFO)
        
        try:
            github = create_github_automation()
            status = await github.get_repository_status()
            print(f"🔍 Repository status: {status}")
            
            if status.get("connected"):
                pipeline = create_cicd_pipeline(github)
                result = await pipeline.run_automated_workflow("test")
                print(f"🚀 Workflow result: {result}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    asyncio.run(test_github_integration())