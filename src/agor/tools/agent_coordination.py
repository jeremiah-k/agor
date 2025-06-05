"""
Agent Coordination Helper for AGOR Multi-Agent Development.

This module provides helper functions for agents to discover their role,
understand the current strategy, and get concrete next actions within
the existing AGOR protocol framework.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class AgentCoordinationHelper:
    """Helper for agents to coordinate within AGOR protocols."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.agor_dir = self.project_root / ".agor"

    def discover_current_situation(self, agent_id: Optional[str] = None) -> Dict:
        """
        Discover current coordination situation and provide next actions.
        This is the main entry point for agents joining a project.
        """

        # Initialize memory sync for agent workflows
        self._init_agent_memory_sync()

        # Check if AGOR coordination exists
        if not self.agor_dir.exists():
            return {
                "status": "no_coordination",
                "message": "No AGOR coordination found. Initialize coordination first.",
                "next_actions": [
                    "Create .agor directory structure",
                    "Initialize agentconvo.md and memory.md",
                    "Choose and initialize a development strategy",
                ],
            }

        # Check for active strategy
        strategy_info = self._detect_active_strategy()

        if not strategy_info:
            return {
                "status": "no_strategy",
                "message": "AGOR coordination exists but no strategy is active.",
                "next_actions": [
                    "Choose appropriate strategy (pd/pl/sw/rt/mb)",
                    "Initialize strategy with task description",
                    "Begin agent coordination",
                ],
            }

        # Determine agent's role in current strategy
        role_info = self._determine_agent_role(strategy_info, agent_id)

        # Get concrete next actions
        next_actions = self._get_concrete_actions(strategy_info, role_info)

        return {
            "status": "strategy_active",
            "strategy": strategy_info,
            "role": role_info,
            "next_actions": next_actions,
            "message": f"Active strategy: {strategy_info['type']}. {role_info['message']}",
        }

    def _detect_active_strategy(self) -> Optional[Dict]:
        """Detect what strategy is currently active."""

        strategy_file = self.agor_dir / "strategy-active.md"
        if not strategy_file.exists():
            return None

        content = strategy_file.read_text()

        # Detect strategy type from content
        if "Parallel Divergent Strategy" in content:
            return self._parse_parallel_divergent_strategy(content)
        elif "Pipeline Strategy" in content:
            return self._parse_pipeline_strategy(content)
        elif "Swarm Strategy" in content:
            return self._parse_swarm_strategy(content)
        elif "Red Team Strategy" in content:
            return {"type": "red_team", "phase": "active"}
        elif "Mob Programming Strategy" in content:
            return {"type": "mob_programming", "phase": "active"}

        return None

    def _parse_parallel_divergent_strategy(self, content: str) -> Dict:
        """Parse Parallel Divergent strategy details."""

        # Extract task description
        task_match = re.search(r"### Task: (.+)", content)
        task = task_match.group(1) if task_match else "Unknown task"

        # Determine current phase
        if "Phase 1 - Divergent Execution (ACTIVE)" in content:
            phase = "divergent"
        elif "Phase 2 - Convergent Review (ACTIVE)" in content:
            phase = "convergent"
        elif "Phase 3 - Synthesis (ACTIVE)" in content:
            phase = "synthesis"
        else:
            phase = "setup"

        # Extract agent assignments
        agent_assignments = []
        agent_pattern = (
            r"### (Agent\d+) Assignment.*?Branch.*?`([^`]+)`.*?Status.*?([^\n]+)"
        )
        for match in re.finditer(agent_pattern, content, re.DOTALL):
            agent_assignments.append(
                {
                    "agent_id": match.group(1).lower(),
                    "branch": match.group(2),
                    "status": match.group(3).strip(),
                }
            )

        return {
            "type": "parallel_divergent",
            "phase": phase,
            "task": task,
            "agents": agent_assignments,
        }

    def _parse_pipeline_strategy(self, content: str) -> Dict:
        """Parse Pipeline strategy details."""

        # Extract task description
        task_match = re.search(r"### Task: (.+)", content)
        task = task_match.group(1) if task_match else "Unknown task"

        # Extract current stage
        current_stage_match = re.search(
            r"### Status: Stage (\d+) - ([^(]+) \(ACTIVE\)", content
        )
        if current_stage_match:
            current_stage = {
                "number": int(current_stage_match.group(1)),
                "name": current_stage_match.group(2).strip(),
            }
        else:
            current_stage = {"number": 1, "name": "Unknown"}

        return {
            "type": "pipeline",
            "phase": "active",
            "task": task,
            "current_stage": current_stage,
        }

    def _parse_swarm_strategy(self, content: str) -> Dict:
        """Parse Swarm strategy details."""

        # Extract task description
        task_match = re.search(r"### Task: (.+)", content)
        task = task_match.group(1) if task_match else "Unknown task"

        # Get task queue status
        queue_status = self._get_swarm_queue_status()

        return {
            "type": "swarm",
            "phase": "active",
            "task": task,
            "queue_status": queue_status,
        }

    def _get_swarm_queue_status(self) -> Dict:
        """Get current swarm task queue status."""
        queue_file = self.agor_dir / "task-queue.json"

        if not queue_file.exists():
            return {"available": 0, "in_progress": 0, "completed": 0, "total": 0}

        try:
            with open(queue_file) as f:
                queue_data = json.load(f)

            tasks = queue_data.get("tasks", [])
            available = len([t for t in tasks if t["status"] == "available"])
            in_progress = len([t for t in tasks if t["status"] == "in_progress"])
            completed = len([t for t in tasks if t["status"] == "completed"])

            return {
                "available": available,
                "in_progress": in_progress,
                "completed": completed,
                "total": len(tasks),
            }
        except (json.JSONDecodeError, KeyError):
            return {"available": 0, "in_progress": 0, "completed": 0, "total": 0}

    def _determine_agent_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """Determine what role this agent should play."""

        strategy_type = strategy_info["type"]

        if strategy_type == "parallel_divergent":
            return self._determine_pd_role(strategy_info, agent_id)
        elif strategy_type == "pipeline":
            return self._determine_pipeline_role(strategy_info, agent_id)
        elif strategy_type == "swarm":
            return self._determine_swarm_role(strategy_info, agent_id)
        else:
            return {
                "role": "participant",
                "message": f"Participate in {strategy_type} strategy",
                "status": "active",
            }

    def _determine_pd_role(self, strategy_info: Dict, agent_id: Optional[str]) -> Dict:
        """Determine role in Parallel Divergent strategy."""

        phase = strategy_info["phase"]
        agents = strategy_info.get("agents", [])

        # Check agent communication for assignments
        agentconvo_file = self.agor_dir / "agentconvo.md"
        claimed_agents = set()

        if agentconvo_file.exists():
            content = agentconvo_file.read_text()
            # Look for assignment claims
            claim_pattern = r"(agent\d+): .+ - CLAIMING"
            for match in re.finditer(claim_pattern, content, re.IGNORECASE):
                claimed_agents.add(match.group(1).lower())

        if phase == "divergent":
            # Check if agent already has assignment
            if agent_id and agent_id.lower() in [a["agent_id"] for a in agents]:
                if agent_id.lower() in claimed_agents:
                    return {
                        "role": "divergent_worker",
                        "agent_id": agent_id,
                        "message": f"Continue independent work as {agent_id}",
                        "status": "working",
                    }
                else:
                    return {
                        "role": "divergent_worker",
                        "agent_id": agent_id,
                        "message": f"Claim assignment as {agent_id} and begin independent work",
                        "status": "ready_to_claim",
                    }

            # Find available assignment
            for agent_info in agents:
                if agent_info["agent_id"] not in claimed_agents:
                    return {
                        "role": "divergent_worker",
                        "agent_id": agent_info["agent_id"],
                        "message": f"Claim assignment as {agent_info['agent_id']} and begin independent work",
                        "status": "available",
                    }

            return {
                "role": "observer",
                "message": "All divergent slots filled. Wait for convergent phase.",
                "status": "waiting",
            }

        elif phase == "convergent":
            return {
                "role": "reviewer",
                "message": "Review all solutions and provide feedback",
                "status": "active",
            }

        elif phase == "synthesis":
            return {
                "role": "synthesizer",
                "message": "Help create unified solution from best approaches",
                "status": "active",
            }

        else:
            return {
                "role": "participant",
                "message": "Parallel Divergent strategy in setup phase",
                "status": "waiting",
            }

    def _determine_pipeline_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """Determine role in Pipeline strategy."""

        current_stage = strategy_info.get("current_stage", {})

        # Check if current stage is claimed
        agentconvo_file = self.agor_dir / "agentconvo.md"
        stage_claimed = False

        if agentconvo_file.exists():
            content = agentconvo_file.read_text()
            stage_pattern = f"CLAIMING STAGE {current_stage.get('number', 1)}"
            stage_claimed = stage_pattern in content

        if stage_claimed:
            return {
                "role": "observer",
                "message": f"Stage {current_stage.get('number', 1)} ({current_stage.get('name', 'Unknown')}) is claimed. Wait for completion.",
                "status": "waiting",
            }
        else:
            return {
                "role": "stage_worker",
                "message": f"Claim Stage {current_stage.get('number', 1)} ({current_stage.get('name', 'Unknown')}) and begin work",
                "status": "available",
                "stage": current_stage,
            }

    def _determine_swarm_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """Determine role in Swarm strategy."""

        queue_status = strategy_info.get("queue_status", {})
        available_tasks = queue_status.get("available", 0)

        if available_tasks > 0:
            return {
                "role": "task_worker",
                "message": f"{available_tasks} tasks available. Claim one and begin work.",
                "status": "available",
            }
        elif queue_status.get("in_progress", 0) > 0:
            return {
                "role": "helper",
                "message": "No available tasks. Help other agents or wait for task completion.",
                "status": "helping",
            }
        else:
            return {
                "role": "completed",
                "message": "All tasks completed. Swarm strategy finished.",
                "status": "done",
            }

    def _get_concrete_actions(self, strategy_info: Dict, role_info: Dict) -> List[str]:
        """Get concrete next actions for the agent."""

        strategy_type = strategy_info["type"]
        role_info["role"]
        role_info.get("status", "unknown")

        if strategy_type == "parallel_divergent":
            return self._get_pd_actions(role_info, strategy_info)
        elif strategy_type == "pipeline":
            return self._get_pipeline_actions(role_info, strategy_info)
        elif strategy_type == "swarm":
            return self._get_swarm_actions(role_info, strategy_info)
        else:
            return [
                "Check strategy details in .agor/strategy-active.md",
                "Follow strategy-specific protocols",
                "Communicate progress in .agor/agentconvo.md",
            ]

    def _get_pd_actions(self, role_info: Dict, strategy_info: Dict) -> List[str]:
        """Get Parallel Divergent specific actions."""

        role = role_info["role"]
        status = role_info.get("status", "unknown")

        if role == "divergent_worker":
            if status == "ready_to_claim" or status == "available":
                agent_id = role_info.get("agent_id", "agent1")
                return [
                    f"Post to agentconvo.md: '{agent_id}: [timestamp] - CLAIMING ASSIGNMENT'",
                    f"Create branch: git checkout -b solution-{agent_id}",
                    f"Initialize memory file: .agor/{agent_id}-memory.md",
                    "Plan your unique approach to the problem",
                    "Begin independent implementation (NO coordination with other agents)",
                ]
            elif status == "working":
                agent_id = role_info.get("agent_id", "agent1")
                return [
                    f"Continue work on your branch: solution-{agent_id}",
                    f"Update your memory file: .agor/{agent_id}-memory.md",
                    "Document decisions and progress",
                    "Test your implementation thoroughly",
                    f"When complete, post: '{agent_id}: [timestamp] - PHASE1_COMPLETE'",
                ]

        elif role == "reviewer":
            return [
                "Review all agent solutions on their branches",
                "Use review template in strategy-active.md",
                "Post reviews to agentconvo.md",
                "Identify strengths and weaknesses",
                "Propose synthesis approach",
            ]

        elif role == "synthesizer":
            return [
                "Combine best approaches from all solutions",
                "Create unified implementation",
                "Test integrated solution",
                "Document final approach",
            ]

        elif role == "observer":
            return [
                "Monitor progress in agentconvo.md",
                "Prepare for next phase",
                "Review strategy details",
            ]

        return ["Check strategy-active.md for current phase instructions"]

    def _get_pipeline_actions(self, role_info: Dict, strategy_info: Dict) -> List[str]:
        """Get Pipeline specific actions."""

        role = role_info["role"]
        status = role_info.get("status", "unknown")

        if role == "stage_worker" and status == "available":
            stage = role_info.get("stage", {})
            stage_num = stage.get("number", 1)
            stage_name = stage.get("name", "Unknown")

            return [
                f"Post to agentconvo.md: '[agent-id]: [timestamp] - CLAIMING STAGE {stage_num}: {stage_name}'",
                f"Create working branch: git checkout -b stage-{stage_num}-{stage_name.lower().replace(' ', '-')}",
                "Read stage instructions in strategy-active.md",
                "Complete stage deliverables",
                "Create handoff document for next stage",
            ]

        elif role == "observer":
            return [
                "Monitor current stage progress in agentconvo.md",
                "Prepare for next stage if applicable",
                "Review upcoming stage requirements",
            ]

        return ["Check strategy-active.md for current stage instructions"]

    def _get_swarm_actions(self, role_info: Dict, strategy_info: Dict) -> List[str]:
        """Get Swarm specific actions."""

        role = role_info["role"]
        status = role_info.get("status", "unknown")

        if role == "task_worker" and status == "available":
            return [
                "Check available tasks: cat .agor/task-queue.json",
                "Pick a task that matches your skills",
                "Edit task-queue.json to claim the task (status: in_progress, assigned_to: your_id)",
                "Post to agentconvo.md: '[agent-id]: [timestamp] - CLAIMED TASK [N]: [description]'",
                "Begin task work independently",
            ]

        elif role == "helper":
            return [
                "Check if any agents need help in agentconvo.md",
                "Look for completed tasks to verify",
                "Wait for new tasks to become available",
            ]

        elif role == "completed":
            return [
                "Verify all tasks are properly completed",
                "Help with final integration and testing",
                "Document swarm strategy results",
            ]

        return ["Check task-queue.json for current status"]


# Convenience functions for agents
def discover_my_role(agent_id: Optional[str] = None) -> str:
    """
    Main entry point for agents to discover their role and next actions.
    Returns formatted guidance for the agent.
    """

    helper = AgentCoordinationHelper()
    result = helper.discover_current_situation(agent_id)

    # Format result for agent consumption
    output = f"""# 🤖 AGOR Agent Coordination

## Status: {result['status'].replace('_', ' ').title()}

{result['message']}

"""

    if result["status"] == "strategy_active":
        strategy_info = result["strategy"]
        role_info = result["role"]

        output += f"""## Current Strategy: {strategy_info['type'].replace('_', ' ').title()}
**Task**: {strategy_info.get('task', 'Unknown')}
**Your Role**: {role_info['role'].replace('_', ' ').title()}

## Next Actions:
"""

        for i, action in enumerate(result["next_actions"], 1):
            output += f"{i}. {action}\n"

        output += f"""
## Quick Commands:
```bash
# Check strategy details
cat .agor/strategy-active.md

# Check agent communication
cat .agor/agentconvo.md | tail -10

# Check your memory file (if assigned)
cat .agor/{role_info.get('agent_id', 'agentX')}-memory.md
```
"""

    else:
        output += "## Next Steps:\n"
        for step in result.get("next_actions", []):
            output += f"- {step}\n"

    return output


def check_strategy_status() -> str:
    """Check current strategy status and recent activity."""

    helper = AgentCoordinationHelper()

    # Check if coordination exists
    if not helper.agor_dir.exists():
        return "❌ No AGOR coordination found. Initialize coordination first."

    # Get strategy info
    strategy_info = helper._detect_active_strategy()

    if not strategy_info:
        return "📋 AGOR coordination exists but no strategy is active."

    # Get recent activity
    agentconvo_file = helper.agor_dir / "agentconvo.md"
    recent_activity = "No recent activity"

    if agentconvo_file.exists():
        lines = agentconvo_file.read_text().strip().split("\n")
        recent_lines = [
            line for line in lines[-5:] if line.strip() and not line.startswith("#")
        ]
        if recent_lines:
            recent_activity = "\n".join(f"  {line}" for line in recent_lines)

    return f"""📊 AGOR Strategy Status

**Strategy**: {strategy_info['type'].replace('_', ' ').title()}
**Task**: {strategy_info.get('task', 'Unknown')}
**Phase**: {strategy_info.get('phase', 'Unknown')}

**Recent Activity**:
{recent_activity}

**Files to Check**:
- .agor/strategy-active.md - Strategy details
- .agor/agentconvo.md - Agent communication
- .agor/task-queue.json - Task queue (if Swarm strategy)
"""

    def _init_agent_memory_sync(self) -> None:
        """Initialize memory sync for agent workflows."""
        try:
            # Import and initialize MemorySyncManager for memory sync
            from ..memory_sync import MemorySyncManager

            # Initialize memory manager if .agor directory exists
            if self.agor_dir.exists():
                memory_manager = MemorySyncManager(self.project_root)

                # Check if memory sync is available
                if memory_manager:
                    active_branch = memory_manager.get_active_memory_branch()
                    if active_branch:
                        print(f"🧠 Agent memory sync active on branch: {active_branch}")
                    else:
                        print("🧠 Agent memory sync initialized")
                else:
                    print(
                        "⚠️ Agent memory sync not available - continuing without memory persistence"
                    )
            else:
                print(
                    "📝 No .agor directory found - memory sync will be initialized when coordination starts"
                )
        except Exception as e:
            print(f"⚠️ Agent memory sync initialization warning: {e}")
            # Don't fail agent discovery if memory sync has issues

    def complete_agent_work(
        self, agent_id: str, completion_message: str = "Agent work completed"
    ) -> bool:
        """Complete agent work with automatic memory sync."""
        try:
            # Import and use MemorySyncManager for completion sync
            from ..memory_sync import MemorySyncManager

            if self.agor_dir.exists():
                memory_manager = MemorySyncManager(self.project_root)

                # Perform completion sync if memory sync is available
                if memory_manager:
                    print(f"💾 Saving {agent_id} memory state...")

                    # Use auto_sync_on_shutdown to save memory state
                    active_branch = memory_manager.get_active_memory_branch()
                    if active_branch:
                        sync_success = memory_manager.auto_sync_on_shutdown(
                            target_branch_name=active_branch,
                            commit_message=f"{agent_id}: {completion_message}",
                            push_changes=True,
                            restore_original_branch=None,  # Stay on memory branch
                        )

                        if sync_success:
                            print(f"✅ {agent_id} memory state saved successfully")
                            return True
                        else:
                            print(
                                f"⚠️ {agent_id} memory sync failed - work completed but memory not saved"
                            )
                            return False
                    else:
                        print(f"📝 {agent_id} work completed (no active memory branch)")
                        return True
                else:
                    print(f"📝 {agent_id} work completed (no memory sync available)")
                    return True
            else:
                print(f"📝 {agent_id} work completed (no .agor directory)")
                return True

        except Exception as e:
            print(f"⚠️ {agent_id} completion error: {e}")
            return False


def process_agent_hotkey(hotkey: str, context: str = "") -> dict:
    """Process hotkey and update internal checklist."""
    from agor.tools.dev_tooling import get_checklist_status, mark_checklist_complete

    # Map hotkeys to checklist items
    hotkey_mapping = {
        "a": "analyze_codebase",
        "f": "analyze_codebase",
        "commit": "frequent_commits",
        "diff": "frequent_commits",
        "m": "frequent_commits",
        "snapshot": "create_snapshot",
        "progress-report": "create_snapshot",
        "work-order": "create_snapshot",
        "create-pr": "create_snapshot",
        "receive-snapshot": "create_snapshot",
        "status": "update_coordination",
        "sync": "update_coordination",
        "sp": "select_strategy",
        "bp": "select_strategy",
        "ss": "select_strategy",
    }

    result = {"hotkey": hotkey, "checklist_updated": False}

    # Update checklist if hotkey maps to an item
    if hotkey in hotkey_mapping:
        item_id = hotkey_mapping[hotkey]
        mark_checklist_complete(item_id)
        result["checklist_updated"] = True
        print(f"✅ Checklist updated: {item_id} marked complete")

    # Get current status
    status = get_checklist_status()
    if status.get("completion_percentage"):
        print(f"📊 Session progress: {status['completion_percentage']:.1f}% complete")

    return result


def detect_session_end(user_input: str) -> bool:
    """Detect if user is indicating session end and enforce procedures."""
    from agor.tools.dev_tooling import enforce_session_end

    end_indicators = [
        "thanks",
        "goodbye",
        "done",
        "finished",
        "complete",
        "end session",
        "that's all",
        "wrap up",
        "closing",
        "final",
        "submit",
    ]

    if any(indicator in user_input.lower() for indicator in end_indicators):
        return enforce_session_end()

    return True
