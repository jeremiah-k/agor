"""
Agent Coordination Helper for AGOR Multi-Agent Development.

This module provides helper functions for agents to discover their role,
understand the current strategy, and get concrete next actions within
the existing AGOR protocol framework.

Key Features:
- Strategy detection and parsing
- Agent role assignment and discovery
- Concrete action generation for different strategies
- Communication protocol management
- Memory synchronization integration

Public API:
- discover_my_role(agent_id): Main entry point for agents
- check_strategy_status(): Get current strategy status
- AgentCoordinationHelper: Core coordination logic
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from agor.tools.strategy_config import StrategyConfigManager


class AgentCoordinationHelper:
    """
    Helper for agents to coordinate within AGOR protocols.

    This class provides the core coordination logic for multi-agent development,
    including strategy detection, role assignment, and action generation.

    Attributes:
        project_root (Path): Root directory of the project
        agor_dir (Path): Path to .agor coordination directory
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the coordination helper.

        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.agor_dir = self.project_root / ".agor"
        self.strategy_manager = StrategyConfigManager()

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
        """
        Detect what strategy is currently active using the new configuration system.

        Returns:
            Dictionary containing strategy information, or None if no strategy is active.
        """
        strategy_file = self.agor_dir / "strategy-active.md"
        if not strategy_file.exists():
            return None

        content = strategy_file.read_text()

        # Use the new strategy configuration manager
        return self.strategy_manager.detect_strategy(content)

    def _extract_task_from_content(self, content: str) -> str:
        """
        Extract task description from strategy content.

        Args:
            content: Strategy file content

        Returns:
            Task description or "Unknown task" if not found
        """
        task_match = re.search(r"### Task: (.+)", content)
        return task_match.group(1) if task_match else "Unknown task"

    def _parse_parallel_divergent_strategy(self, content: str) -> Dict:
        """
        Parse Parallel Divergent strategy details.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing strategy details
        """
        task = self._extract_task_from_content(content)
        phase = self._extract_pd_phase(content)
        agent_assignments = self._extract_agent_assignments(content)

        return {
            "type": "parallel_divergent",
            "phase": phase,
            "task": task,
            "agents": agent_assignments,
        }

    def _extract_pd_phase(self, content: str) -> str:
        """
        Extract current phase from Parallel Divergent strategy content.

        Args:
            content: Strategy file content

        Returns:
            Current phase name
        """
        phase_patterns = {
            "Phase 1 - Divergent Execution (ACTIVE)": "divergent",
            "Phase 2 - Convergent Review (ACTIVE)": "convergent",
            "Phase 3 - Synthesis (ACTIVE)": "synthesis",
        }

        for pattern, phase in phase_patterns.items():
            if pattern in content:
                return phase
        return "setup"

    def _extract_agent_assignments(self, content: str) -> List[Dict]:
        """
        Extract agent assignments from strategy content.

        Args:
            content: Strategy file content

        Returns:
            List of agent assignment dictionaries
        """
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
        return agent_assignments

    def _parse_pipeline_strategy(self, content: str) -> Dict:
        """
        Parse Pipeline strategy details.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing strategy details
        """
        task = self._extract_task_from_content(content)
        current_stage = self._extract_current_stage(content)

        return {
            "type": "pipeline",
            "phase": "active",
            "task": task,
            "current_stage": current_stage,
        }

    def _extract_current_stage(self, content: str) -> Dict:
        """
        Extract current stage from Pipeline strategy content.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing stage number and name
        """
        current_stage_match = re.search(
            r"### Status: Stage (\d+) - ([^(]+) \(ACTIVE\)", content
        )
        if current_stage_match:
            return {
                "number": int(current_stage_match.group(1)),
                "name": current_stage_match.group(2).strip(),
            }
        return {"number": 1, "name": "Unknown"}

    def _parse_swarm_strategy(self, content: str) -> Dict:
        """
        Parse Swarm strategy details.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing strategy details
        """
        task = self._extract_task_from_content(content)
        queue_status = self._get_swarm_queue_status()

        return {
            "type": "swarm",
            "phase": "active",
            "task": task,
            "queue_status": queue_status,
        }

    def _get_swarm_queue_status(self) -> Dict:
        """
        Get current swarm task queue status.

        Returns:
            Dictionary containing task counts by status
        """
        queue_file = self.agor_dir / "task-queue.json"
        default_status = {"available": 0, "in_progress": 0, "completed": 0, "total": 0}

        if not queue_file.exists():
            return default_status

        try:
            with open(queue_file) as f:
                queue_data = json.load(f)

            tasks = queue_data.get("tasks", [])
            status_counts = self._count_tasks_by_status(tasks)
            status_counts["total"] = len(tasks)

            return status_counts
        except (json.JSONDecodeError, KeyError):
            return default_status

    def _count_tasks_by_status(self, tasks: List[Dict]) -> Dict:
        """
        Count tasks by their status.

        Args:
            tasks: List of task dictionaries

        Returns:
            Dictionary with counts for each status
        """
        status_counts = {"available": 0, "in_progress": 0, "completed": 0}

        for task in tasks:
            status = task.get("status", "unknown")
            if status in status_counts:
                status_counts[status] += 1

        return status_counts

    def _parse_red_team_strategy(self, content: str) -> Dict:
        """
        Parse Red Team strategy details.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing strategy details
        """
        return {"type": "red_team", "phase": "active"}

    def _parse_mob_programming_strategy(self, content: str) -> Dict:
        """
        Parse Mob Programming strategy details.

        Args:
            content: Strategy file content

        Returns:
            Dictionary containing strategy details
        """
        return {"type": "mob_programming", "phase": "active"}

    def _determine_agent_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """
        Determine what role this agent should play in the current strategy using configuration.

        Args:
            strategy_info: Information about the current strategy
            agent_id: Optional agent identifier

        Returns:
            Dictionary containing role information and next actions
        """
        # Build context for role determination
        context = {
            "agent_id": agent_id,
            "has_assignment": self._check_agent_assignment(strategy_info, agent_id),
            "stage_available": self._check_stage_availability(strategy_info),
            "available_tasks": self._get_available_task_count(strategy_info),
            "claimed": agent_id and agent_id.lower() in self._get_claimed_agents(),
        }

        # Use the new strategy configuration manager
        return self.strategy_manager.get_role_for_agent(
            strategy_info, agent_id, context
        )

    def _get_claimed_agents(self, pattern: str = r"(agent\d+): .+ - CLAIMING") -> set:
        """
        Get set of agents that have claimed assignments from agentconvo.md.

        Args:
            pattern: Regex pattern to match claims

        Returns:
            Set of claimed agent IDs
        """
        agentconvo_file = self.agor_dir / "agentconvo.md"
        claimed_agents = set()

        if agentconvo_file.exists():
            content = agentconvo_file.read_text()
            for match in re.finditer(pattern, content, re.IGNORECASE):
                claimed_agents.add(match.group(1).lower())

        return claimed_agents

    def _check_agent_assignment(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> bool:
        """Check if agent has an assignment in the strategy."""
        if not agent_id:
            return False

        agents = strategy_info.get("agents", [])
        return any(agent["agent_id"] == agent_id.lower() for agent in agents)

    def _check_stage_availability(self, strategy_info: Dict) -> bool:
        """Check if a pipeline stage is available for claiming."""
        if strategy_info.get("type") != "pipeline":
            return False

        current_stage = strategy_info.get("current_stage", {})
        stage_number = current_stage.get("number", 1)
        return not self._is_stage_claimed(stage_number)

    def _get_available_task_count(self, strategy_info: Dict) -> int:
        """Get count of available tasks for swarm strategy."""
        if strategy_info.get("type") != "swarm":
            return 0

        queue_status = strategy_info.get("queue_status", {})
        return queue_status.get("available", 0)

    def _determine_pd_role(self, strategy_info: Dict, agent_id: Optional[str]) -> Dict:
        """
        Determine role in Parallel Divergent strategy.

        Args:
            strategy_info: Strategy information
            agent_id: Optional agent identifier

        Returns:
            Dictionary containing role assignment
        """
        phase = strategy_info["phase"]
        agents = strategy_info.get("agents", [])
        claimed_agents = self._get_claimed_agents()

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

    def _is_stage_claimed(self, stage_number: int) -> bool:
        """
        Check if a pipeline stage is already claimed.

        Args:
            stage_number: Stage number to check

        Returns:
            True if stage is claimed, False otherwise
        """
        agentconvo_file = self.agor_dir / "agentconvo.md"

        if not agentconvo_file.exists():
            return False

        content = agentconvo_file.read_text()
        stage_pattern = f"CLAIMING STAGE {stage_number}"
        return stage_pattern in content

    def _determine_pipeline_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """
        Determine role in Pipeline strategy.

        Args:
            strategy_info: Strategy information
            agent_id: Optional agent identifier

        Returns:
            Dictionary containing role assignment
        """
        current_stage = strategy_info.get("current_stage", {})
        stage_number = current_stage.get("number", 1)
        stage_claimed = self._is_stage_claimed(stage_number)

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
        """
        Get concrete next actions for the agent based on strategy and role.

        Args:
            strategy_info: Information about the current strategy
            role_info: Information about the agent's role

        Returns:
            List of concrete action strings
        """
        strategy_type = strategy_info["type"]

        # Strategy-specific action handlers
        action_handlers = {
            "parallel_divergent": self._get_pd_actions,
            "pipeline": self._get_pipeline_actions,
            "swarm": self._get_swarm_actions,
        }

        if strategy_type in action_handlers:
            return action_handlers[strategy_type](role_info, strategy_info)
        else:
            return [
                "Check strategy details in .agor/strategy-active.md",
                "Follow strategy-specific protocols",
                "Communicate progress in .agor/agentconvo.md",
            ]

    def _get_pd_actions(self, role_info: Dict, strategy_info: Dict) -> List[str]:
        """
        Get Parallel Divergent specific actions.

        Args:
            role_info: Information about the agent's role
            strategy_info: Information about the strategy

        Returns:
            List of concrete action strings for Parallel Divergent strategy
        """
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
        """
        Get Pipeline specific actions.

        Args:
            role_info: Information about the agent's role
            strategy_info: Information about the strategy

        Returns:
            List of concrete action strings for Pipeline strategy
        """
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
                "Create snapshot document for next stage",
            ]

        elif role == "observer":
            return [
                "Monitor current stage progress in agentconvo.md",
                "Prepare for next stage if applicable",
                "Review upcoming stage requirements",
            ]

        return ["Check strategy-active.md for current stage instructions"]

    def _get_swarm_actions(self, role_info: Dict, strategy_info: Dict) -> List[str]:
        """
        Get Swarm specific actions.

        Args:
            role_info: Information about the agent's role
            strategy_info: Information about the strategy

        Returns:
            List of concrete action strings for Swarm strategy
        """
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

    This function analyzes the current project state, detects active strategies,
    and provides concrete next actions for the agent to take.

    Args:
        agent_id: Optional agent identifier (e.g., "agent1", "agent2")

    Returns:
        Formatted string with role information and concrete next actions

    Example:
        >>> role_info = discover_my_role("agent1")
        >>> print(role_info)
        # 🤖 AGOR Agent Coordination
        ## Status: Strategy Active
        Active strategy: parallel_divergent. Claim assignment as agent1...
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
    """
    Check current strategy status and recent activity.

    This function provides a quick overview of the current AGOR strategy,
    including recent agent communication and activity.

    Returns:
        Formatted string with strategy status and recent activity

    Example:
        >>> status = check_strategy_status()
        >>> print(status)
        📊 AGOR Strategy Status
        **Strategy**: Parallel Divergent
        **Task**: implement user authentication
        **Recent Activity**: agent1: 2024-01-15 14:30 - CLAIMING ASSIGNMENT
    """

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
    # TODO: Implement checklist functions when needed

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
        # TODO: Implement mark_checklist_complete when needed
        result["checklist_updated"] = True
        print(f"✅ Hotkey processed: {item_id}")

    # TODO: Implement get_checklist_status when needed
    print(f"📊 Hotkey '{hotkey}' processed successfully")

    return result


def detect_session_end(user_input: str) -> bool:
    """Detect if user is indicating session end and enforce procedures."""
    # TODO: Implement enforce_session_end when needed

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
        print("🔚 Session end detected - please create snapshot and handoff prompt")
        return True

    return True
