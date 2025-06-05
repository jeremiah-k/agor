"""
Agent Checklist System for AGOR - Internal Agent Task Management

This system enables agents to create their own internal checklists while ensuring
mandatory items are included. The checklist is for the AGENT'S internal use to track
their own progress and ensure they follow AGOR protocols.

Key Features:
- Agent-generated internal checklists with mandatory items
- Automatic integration with memory branch system
- Session-based checklist management stored on memory branches
- Snapshot creation enforcement
- Progress tracking and validation
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Import memory sync and dev tooling for automatic integration
try:
    from agor.memory_sync import MemorySyncManager
    from agor.tools.dev_tooling import dev_tools, get_timestamp
except ImportError:
    # Fallback for development environment
    def get_timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    class MockDevTools:
        def quick_commit_push(self, message, emoji="🔧"):
            print(f"Mock commit: {emoji} {message}")
            return True

    class MockMemorySync:
        def generate_memory_branch_name(self):
            return f"agor/mem/{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        def auto_sync_on_shutdown(self, *args, **kwargs):
            return True

    dev_tools = MockDevTools()
    MemorySyncManager = MockMemorySync


@dataclass
class ChecklistItem:
    """Individual checklist item with tracking."""
    id: str
    description: str
    mandatory: bool = False
    completed: bool = False
    notes: str = ""
    timestamp_completed: Optional[str] = None
    auto_trigger: Optional[str] = None  # Function to auto-trigger


@dataclass
class AgentChecklist:
    """Complete agent checklist with metadata."""
    agent_id: str
    session_id: str
    role: str
    task_description: str
    created_at: str
    items: List[ChecklistItem]
    completion_percentage: float = 0.0
    snapshot_created: bool = False
    session_ended: bool = False


class ChecklistManager:
    """Manages agent checklists with mandatory item enforcement and memory branch integration."""

    def __init__(self, agent_id: str = "agent", role: str = "solo_developer"):
        self.agent_id = agent_id
        self.role = role
        self.checklist_dir = Path(".agor/checklists")
        self.checklist_dir.mkdir(parents=True, exist_ok=True)
        self.current_checklist: Optional[AgentChecklist] = None

        # Initialize memory sync manager for storing checklists on memory branches
        try:
            self.memory_sync = MemorySyncManager()
        except Exception:
            self.memory_sync = None
            print("⚠️  Memory sync not available - using local storage only")
        
    def get_mandatory_items(self, role: str) -> List[ChecklistItem]:
        """Get mandatory checklist items based on agent role."""
        base_mandatory = [
            ChecklistItem(
                id="read_documentation",
                description="Read AGOR documentation (README_ai.md, AGOR_INSTRUCTIONS.md)",
                mandatory=True,
                auto_trigger="check_documentation_read"
            ),
            ChecklistItem(
                id="git_setup",
                description="Configure git identity and create feature branch",
                mandatory=True,
                auto_trigger="verify_git_setup"
            ),
            ChecklistItem(
                id="frequent_commits",
                description="Commit and push changes frequently (every 2-3 logical units)",
                mandatory=True,
                auto_trigger="track_commit_frequency"
            ),
            ChecklistItem(
                id="create_snapshot",
                description="Create comprehensive snapshot before ending session",
                mandatory=True,
                auto_trigger="enforce_snapshot_creation"
            ),
            ChecklistItem(
                id="update_coordination",
                description="Update .agor/agentconvo.md with progress and status",
                mandatory=True,
                auto_trigger="check_coordination_updates"
            )
        ]
        
        role_specific = {
            "solo_developer": [
                ChecklistItem(
                    id="codebase_analysis",
                    description="Perform comprehensive codebase analysis",
                    mandatory=True
                ),
                ChecklistItem(
                    id="test_changes",
                    description="Test all code changes before committing",
                    mandatory=True
                )
            ],
            "project_coordinator": [
                ChecklistItem(
                    id="strategy_selection",
                    description="Select and initialize appropriate development strategy",
                    mandatory=True
                ),
                ChecklistItem(
                    id="team_coordination",
                    description="Set up team coordination and communication protocols",
                    mandatory=True
                )
            ],
            "agent_worker": [
                ChecklistItem(
                    id="receive_instructions",
                    description="Receive and acknowledge task assignment from coordinator",
                    mandatory=True
                ),
                ChecklistItem(
                    id="report_completion",
                    description="Report task completion with comprehensive status",
                    mandatory=True
                )
            ]
        }
        
        return base_mandatory + role_specific.get(role, [])
    
    def create_agent_checklist(self, task_description: str, custom_items: List[str] = None) -> AgentChecklist:
        """Create a new agent checklist with mandatory and custom items."""
        session_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        # Get mandatory items
        mandatory_items = self.get_mandatory_items(self.role)
        
        # Add custom items from agent
        custom_checklist_items = []
        if custom_items:
            for i, item_desc in enumerate(custom_items):
                custom_checklist_items.append(
                    ChecklistItem(
                        id=f"custom_{i+1}",
                        description=item_desc,
                        mandatory=False
                    )
                )
        
        # Create complete checklist
        all_items = mandatory_items + custom_checklist_items
        
        checklist = AgentChecklist(
            agent_id=self.agent_id,
            session_id=session_id,
            role=self.role,
            task_description=task_description,
            created_at=get_timestamp(),
            items=all_items
        )
        
        self.current_checklist = checklist
        self.save_checklist()
        
        return checklist
    
    def save_checklist(self):
        """Save current checklist to file and memory branch."""
        if not self.current_checklist:
            return

        filename = f"{self.current_checklist.session_id}_{self.agent_id}_checklist.json"
        filepath = self.checklist_dir / filename

        # Save locally first
        with open(filepath, 'w') as f:
            json.dump(asdict(self.current_checklist), f, indent=2)

        # Save to memory branch if available
        if self.memory_sync:
            try:
                branch_name = f"agor/mem/checklist_{self.current_checklist.session_id}"
                commit_message = f"Update checklist for {self.agent_id} session {self.current_checklist.session_id}"

                # Use memory sync to save to branch
                self.memory_sync.auto_sync_on_shutdown(
                    target_branch_name=branch_name,
                    commit_message=commit_message,
                    push_changes=True,
                    restore_original_branch=None
                )
                print(f"✅ Checklist saved to memory branch: {branch_name}")
            except Exception as e:
                print(f"⚠️  Failed to save checklist to memory branch: {e}")
    
    def load_latest_checklist(self) -> Optional[AgentChecklist]:
        """Load the most recent checklist for this agent."""
        pattern = f"*_{self.agent_id}_checklist.json"
        checklist_files = list(self.checklist_dir.glob(pattern))
        
        if not checklist_files:
            return None
            
        # Get most recent file
        latest_file = max(checklist_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
            
        # Convert back to dataclass
        items = [ChecklistItem(**item) for item in data['items']]
        data['items'] = items
        
        checklist = AgentChecklist(**data)
        self.current_checklist = checklist
        
        return checklist

    def mark_item_complete(self, item_id: str, notes: str = "") -> bool:
        """Mark a checklist item as complete."""
        if not self.current_checklist:
            return False

        for item in self.current_checklist.items:
            if item.id == item_id:
                item.completed = True
                item.notes = notes
                item.timestamp_completed = get_timestamp()

                # Auto-trigger associated function if exists
                if item.auto_trigger:
                    self._execute_auto_trigger(item.auto_trigger, item)

                self._update_completion_percentage()
                self.save_checklist()
                return True

        return False

    def _update_completion_percentage(self):
        """Update completion percentage for current checklist."""
        if not self.current_checklist:
            return

        total_items = len(self.current_checklist.items)
        completed_items = sum(1 for item in self.current_checklist.items if item.completed)

        self.current_checklist.completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0

    def _execute_auto_trigger(self, trigger_name: str, item: ChecklistItem):
        """Execute auto-trigger function for checklist item."""
        trigger_functions = {
            "check_documentation_read": self._check_documentation_read,
            "verify_git_setup": self._verify_git_setup,
            "track_commit_frequency": self._track_commit_frequency,
            "enforce_snapshot_creation": self._enforce_snapshot_creation,
            "check_coordination_updates": self._check_coordination_updates
        }

        if trigger_name in trigger_functions:
            try:
                trigger_functions[trigger_name](item)
            except Exception as e:
                print(f"⚠️  Auto-trigger {trigger_name} failed: {e}")

    def _check_documentation_read(self, item: ChecklistItem):
        """Verify documentation has been read."""
        # Check if agent has accessed documentation files
        docs_to_check = [
            "src/agor/tools/README_ai.md",
            "src/agor/tools/AGOR_INSTRUCTIONS.md"
        ]

        for doc in docs_to_check:
            if not Path(doc).exists():
                print(f"📚 Documentation check: {doc} not found")
                return

        print("✅ Documentation access verified")

    def _verify_git_setup(self, item: ChecklistItem):
        """Verify git configuration and branch setup."""
        try:
            import subprocess

            # Check git config
            result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
            if not result.stdout.strip():
                print("⚠️  Git user.name not configured")
                return

            result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
            if not result.stdout.strip():
                print("⚠️  Git user.email not configured")
                return

            # Check if on feature branch
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
            current_branch = result.stdout.strip()

            if current_branch == "main" or current_branch == "master":
                print("⚠️  Working on main branch - should create feature branch")
                return

            print(f"✅ Git setup verified - on branch: {current_branch}")

        except Exception as e:
            print(f"⚠️  Git verification failed: {e}")

    def _track_commit_frequency(self, item: ChecklistItem):
        """Track commit frequency and remind if needed."""
        try:
            import subprocess

            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-10", "--since=1 hour ago"],
                capture_output=True, text=True
            )

            recent_commits = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

            if recent_commits < 2:
                print("💡 Reminder: Consider committing more frequently (every 2-3 logical units)")
            else:
                print(f"✅ Good commit frequency: {recent_commits} commits in last hour")

        except Exception as e:
            print(f"⚠️  Commit frequency check failed: {e}")

    def _enforce_snapshot_creation(self, item: ChecklistItem):
        """Enforce snapshot creation before session end."""
        if not self.current_checklist:
            return

        # Check if snapshot exists for this session
        snapshot_dir = Path(".agor/snapshots")
        if snapshot_dir.exists():
            session_snapshots = list(snapshot_dir.glob(f"*{self.current_checklist.session_id}*"))
            if session_snapshots:
                self.current_checklist.snapshot_created = True
                print("✅ Session snapshot found")
                return

        print("🚨 MANDATORY: Create snapshot before ending session")
        print("Use: snapshot hotkey or create_session_snapshot() function")

    def _check_coordination_updates(self, item: ChecklistItem):
        """Check if coordination files have been updated."""
        agentconvo_file = Path(".agor/agentconvo.md")

        if not agentconvo_file.exists():
            print("📝 Reminder: Update .agor/agentconvo.md with your progress")
            return

        # Check if file was modified recently (within last hour)
        import time
        file_mtime = agentconvo_file.stat().st_mtime
        current_time = time.time()

        if current_time - file_mtime > 3600:  # 1 hour
            print("📝 Reminder: Update .agor/agentconvo.md with recent progress")
        else:
            print("✅ Coordination files recently updated")

    def get_checklist_status(self) -> Dict:
        """Get current checklist status and recommendations."""
        if not self.current_checklist:
            return {"status": "no_checklist", "message": "No active checklist"}

        mandatory_incomplete = [
            item for item in self.current_checklist.items
            if item.mandatory and not item.completed
        ]

        optional_incomplete = [
            item for item in self.current_checklist.items
            if not item.mandatory and not item.completed
        ]

        return {
            "status": "active",
            "completion_percentage": self.current_checklist.completion_percentage,
            "mandatory_incomplete": len(mandatory_incomplete),
            "optional_incomplete": len(optional_incomplete),
            "snapshot_created": self.current_checklist.snapshot_created,
            "next_mandatory": mandatory_incomplete[0].description if mandatory_incomplete else None,
            "recommendations": self._get_recommendations()
        }

    def _get_recommendations(self) -> List[str]:
        """Get personalized recommendations based on checklist progress."""
        if not self.current_checklist:
            return []

        recommendations = []

        # Check mandatory items
        mandatory_incomplete = [
            item for item in self.current_checklist.items
            if item.mandatory and not item.completed
        ]

        if mandatory_incomplete:
            recommendations.append(f"Complete mandatory item: {mandatory_incomplete[0].description}")

        # Check completion percentage
        if self.current_checklist.completion_percentage < 50:
            recommendations.append("Focus on completing more checklist items")
        elif self.current_checklist.completion_percentage > 80:
            recommendations.append("Great progress! Consider preparing session snapshot")

        # Check snapshot status
        if not self.current_checklist.snapshot_created and self.current_checklist.completion_percentage > 70:
            recommendations.append("Consider creating a snapshot to preserve progress")

        return recommendations

    def create_session_snapshot(self, additional_context: str = "") -> bool:
        """Create a session snapshot and mark checklist item complete."""
        if not self.current_checklist:
            return False

        try:
            # Use dev tooling to create snapshot
            title = f"Session {self.current_checklist.session_id}"
            context = f"""
Task: {self.current_checklist.task_description}
Role: {self.current_checklist.role}
Completion: {self.current_checklist.completion_percentage:.1f}%

{additional_context}

## Checklist Progress
Completed Items:
{chr(10).join(f"- ✅ {item.description}" for item in self.current_checklist.items if item.completed)}

Remaining Items:
{chr(10).join(f"- ⏳ {item.description}" for item in self.current_checklist.items if not item.completed)}
"""

            success = dev_tools.create_development_snapshot(title, context)

            if success:
                self.current_checklist.snapshot_created = True
                self.mark_item_complete("create_snapshot", "Session snapshot created successfully")
                print("✅ Session snapshot created and checklist updated")
                return True
            else:
                print("❌ Failed to create session snapshot")
                return False

        except Exception as e:
            print(f"❌ Snapshot creation failed: {e}")
            return False


# Global checklist manager instance
checklist_manager = ChecklistManager()


# Convenience functions for easy access
def create_checklist(task_description: str, custom_items: List[str] = None, agent_id: str = "agent", role: str = "solo_developer") -> AgentChecklist:
    """Create a new agent checklist."""
    global checklist_manager
    checklist_manager.agent_id = agent_id
    checklist_manager.role = role
    return checklist_manager.create_agent_checklist(task_description, custom_items)


def mark_complete(item_id: str, notes: str = "") -> bool:
    """Mark a checklist item as complete."""
    return checklist_manager.mark_item_complete(item_id, notes)


def get_status() -> Dict:
    """Get current checklist status."""
    return checklist_manager.get_checklist_status()


def create_snapshot(additional_context: str = "") -> bool:
    """Create session snapshot."""
    return checklist_manager.create_session_snapshot(additional_context)


def load_checklist() -> Optional[AgentChecklist]:
    """Load the latest checklist."""
    return checklist_manager.load_latest_checklist()
