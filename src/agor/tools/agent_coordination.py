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
        Initializes the AgentCoordinationHelper with the specified project root.
        
        If no project root is provided, defaults to the current working directory. Sets the path to the `.agor` coordination directory within the project root.
        """
        self.project_root = project_root or Path.cwd()
        self.agor_dir = self.project_root / ".agor"

    def discover_current_situation(self, agent_id: Optional[str] = None) -> Dict:
        """
        Discovers the current coordination state for an agent and provides recommended next actions.
        
        This method serves as the main entry point for agents to assess the project's coordination status. It initializes memory synchronization, checks for the existence of AGOR coordination, detects the active strategy, determines the agent's role, and generates a list of concrete next actions tailored to the agent's context.
        
        Args:
            agent_id: Optional identifier for the agent requesting coordination status.
        
        Returns:
            A dictionary containing:
                - status: Coordination status ("no_coordination", "no_strategy", or "strategy_active").
                - message: Human-readable summary of the current situation.
                - strategy: Details of the active strategy (if any).
                - role: The agent's assigned role and related information.
                - next_actions: List of recommended next steps for the agent.
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
        Detects the currently active AGOR coordination strategy by reading the strategy file.
        
        Returns:
            A dictionary with parsed strategy details if an active strategy is detected, or None if no strategy is active.
        """
        strategy_file = self.agor_dir / "strategy-active.md"
        if not strategy_file.exists():
            return None

        content = strategy_file.read_text()

        # Strategy type detection mapping
        strategy_patterns = {
            "Parallel Divergent Strategy": ("parallel_divergent", self._parse_parallel_divergent_strategy),
            "Pipeline Strategy": ("pipeline", self._parse_pipeline_strategy),
            "Swarm Strategy": ("swarm", self._parse_swarm_strategy),
            "Red Team Strategy": ("red_team", self._parse_red_team_strategy),
            "Mob Programming Strategy": ("mob_programming", self._parse_mob_programming_strategy),
        }

        for pattern, (_, parser) in strategy_patterns.items():
            if pattern in content:
                return parser(content)

        return None

    def _extract_task_from_content(self, content: str) -> str:
        """
        Extracts the task description from the provided strategy content.
        
        Args:
            content: The content of a strategy file.
        
        Returns:
            The extracted task description, or "Unknown task" if no task is found.
        """
        task_match = re.search(r"### Task: (.+)", content)
        return task_match.group(1) if task_match else "Unknown task"

    def _parse_parallel_divergent_strategy(self, content: str) -> Dict:
        """
        Parses the details of a Parallel Divergent strategy from the provided content.
        
        Extracts the overall task description, current phase, and agent assignments from the strategy file content, returning a dictionary with structured strategy information.
        
        Args:
            content: The raw content of the Parallel Divergent strategy file.
        
        Returns:
            A dictionary with keys 'type', 'phase', 'task', and 'agents' describing the strategy.
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
        Extracts the current phase name from Parallel Divergent strategy content.
        
        Args:
            content: The content of the strategy file.
        
        Returns:
            The name of the current phase: 'divergent', 'convergent', 'synthesis', or 'setup' if no active phase is found.
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
        Extracts agent assignment details from strategy content for Parallel Divergent coordination.
        
        Parses the provided strategy content to identify agent assignment sections, returning a list of dictionaries with agent ID, assigned branch, and current status for each agent.
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
        Parses details of a Pipeline strategy from the provided content.
        
        Extracts the main task description and the current stage information, returning a dictionary with the strategy type, phase, task, and current stage details.
        
        Args:
            content: The content of the strategy file.
        
        Returns:
            A dictionary with keys: "type", "phase", "task", and "current_stage".
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
        Extracts the current stage number and name from Pipeline strategy content.
        
        Args:
            content: The content of the Pipeline strategy file.
        
        Returns:
            A dictionary with the current stage's number and name. If no active stage is found, returns number 1 and name 'Unknown'.
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
        Parses the Swarm strategy content and returns structured strategy details.
        
        Args:
            content: The content of the Swarm strategy file.
        
        Returns:
            A dictionary with the strategy type, phase, extracted task description, and current task queue status.
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
        Retrieves the current status of the swarm task queue.
        
        Returns:
            A dictionary with counts of tasks by status: available, in_progress, completed, and total.
            If the queue file is missing or invalid, all counts are zero.
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
        Counts the number of tasks in each status category.
        
        Args:
            tasks: List of task dictionaries, each containing a 'status' key.
        
        Returns:
            A dictionary with the count of tasks for each recognized status: 'available', 'in_progress', and 'completed'.
        """
        status_counts = {"available": 0, "in_progress": 0, "completed": 0}

        for task in tasks:
            status = task.get("status", "unknown")
            if status in status_counts:
                status_counts[status] += 1

        return status_counts

    def _parse_red_team_strategy(self, content: str) -> Dict:
        """
        Parses the Red Team strategy details from the provided content.
        
        Args:
            content: The content of the strategy file.
        
        Returns:
            A dictionary with the strategy type set to "red_team" and the phase set to "active".
        """
        return {"type": "red_team", "phase": "active"}

    def _parse_mob_programming_strategy(self, content: str) -> Dict:
        """
        Parses Mob Programming strategy details from the provided content.
        
        Args:
            content: The content of the strategy file.
        
        Returns:
            A dictionary with the strategy type set to "mob_programming" and the phase set to "active".
        """
        return {"type": "mob_programming", "phase": "active"}

    def _determine_agent_role(
        self, strategy_info: Dict, agent_id: Optional[str]
    ) -> Dict:
        """
        Determines the agent's role based on the current strategy and agent ID.
        
        Selects a strategy-specific role determination method if available; otherwise, assigns a generic participant role.
        
        Args:
            strategy_info: Dictionary containing details about the active strategy.
            agent_id: The agent's identifier, or None if not specified.
        
        Returns:
            A dictionary with role information, including role name, status, and an optional message.
        """
        strategy_type = strategy_info["type"]

        # Strategy-specific role determination
        role_handlers = {
            "parallel_divergent": self._determine_pd_role,
            "pipeline": self._determine_pipeline_role,
            "swarm": self._determine_swarm_role,
        }

        if strategy_type in role_handlers:
            return role_handlers[strategy_type](strategy_info, agent_id)

        return {
            "role": "participant",
            "message": f"Participate in {strategy_type} strategy",
            "status": "active",
        }

    def _get_claimed_agents(self, pattern: str = r"(agent\d+): .+ - CLAIMING") -> set:
        """
        Returns a set of agent IDs that have claimed assignments in agentconvo.md.
        
        Args:
            pattern: Regular expression pattern used to identify agent claim statements.
        
        Returns:
            A set containing the IDs of agents who have claimed assignments.
        """
        agentconvo_file = self.agor_dir / "agentconvo.md"
        claimed_agents = set()

        if agentconvo_file.exists():
            content = agentconvo_file.read_text()
            for match in re.finditer(pattern, content, re.IGNORECASE):
                claimed_agents.add(match.group(1).lower())

        return claimed_agents

    def _determine_pd_role(self, strategy_info: Dict, agent_id: Optional[str]) -> Dict:
        """
        Determines the agent's role in the Parallel Divergent strategy based on the current phase and assignment status.
        
        Assigns roles such as divergent_worker, reviewer, synthesizer, observer, or participant depending on the strategy phase and whether the agent has claimed or is eligible to claim an assignment.
        
        Args:
            strategy_info: Dictionary containing details about the current Parallel Divergent strategy, including phase and agent assignments.
            agent_id: Optional identifier for the agent.
        
        Returns:
            A dictionary describing the assigned role, relevant agent ID (if applicable), a message, and status.
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
        Determines whether a specific pipeline stage has been claimed by any agent.
        
        Args:
            stage_number: The number of the pipeline stage to check.
        
        Returns:
            True if the stage is claimed in the agent conversation log; False otherwise.
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
        Determines the agent's role in a Pipeline strategy based on the current stage's claim status.
        
        If the current stage is already claimed, assigns the agent an observer role with a waiting status. If unclaimed, assigns the agent as a stage worker with instructions to claim and begin work.
        
        Args:
            strategy_info: Dictionary containing parsed Pipeline strategy details.
            agent_id: The agent's identifier, or None.
        
        Returns:
            A dictionary describing the agent's role, status, and relevant stage information.
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
        """
        Determines the agent's role in the Swarm strategy based on the current task queue status.
        
        Returns a dictionary describing the agent's role, a message with instructions, and the current status, depending on whether tasks are available, in progress, or completed.
        """

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
        Returns a list of concrete next actions for the agent based on the current strategy and assigned role.
        
        Delegates to strategy-specific action handlers for supported strategies (Parallel Divergent, Pipeline, Swarm). For unsupported strategies, provides generic instructions.
         
        Args:
            strategy_info: Dictionary containing details about the active coordination strategy.
            role_info: Dictionary describing the agent's assigned role.
        
        Returns:
            A list of strings representing the agent's next recommended actions.
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
        Returns a list of concrete next actions for an agent in the Parallel Divergent strategy.
        
        Actions are tailored to the agent's assigned role and current status, guiding divergent workers, reviewers, synthesizers, or observers through their respective responsibilities in the strategy workflow.
        
        Args:
            role_info: Dictionary containing the agent's role and status within the strategy.
            strategy_info: Dictionary with details about the active Parallel Divergent strategy.
        
        Returns:
            A list of action strings describing the agent's next recommended steps.
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
        Returns a list of next actions for an agent in the Pipeline strategy based on their role.
        
        Args:
            role_info: Dictionary containing the agent's assigned role and related details.
            strategy_info: Dictionary with parsed information about the current Pipeline strategy.
        
        Returns:
            A list of concrete action steps tailored to the agent's role and stage in the Pipeline strategy.
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
        """
        Returns a list of next actions for an agent in the Swarm strategy based on their role and status.
        
        Args:
            role_info: Dictionary containing the agent's assigned role and status within the Swarm strategy.
            strategy_info: Dictionary with details about the current Swarm strategy.
        
        Returns:
            A list of concrete action instructions tailored to the agent's Swarm role and current task status.
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
    Discovers the agent's current role and provides concrete next actions based on the active AGOR coordination strategy.
    
    Analyzes the project state to determine the active strategy, assigns the appropriate role to the agent, and generates a formatted summary with actionable next steps. The output is designed for direct agent consumption and includes status, strategy details, role, next actions, and helpful command-line shortcuts.
    
    Args:
        agent_id: Optional identifier for the agent (e.g., "agent1", "agent2").
    
    Returns:
        A formatted markdown string summarizing the agent's current status, strategy, role, next actions, and quick commands.
    
    Example:
        >>> print(discover_my_role("agent1"))
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
    Provides a summary of the current AGOR strategy status and recent agent activity.
    
    Returns:
        A formatted string summarizing the active strategy type, task, phase, recent agent communication, and relevant files to check. If no coordination or strategy is active, returns a status message indicating so.
    
    Example:
        >>> status = check_strategy_status()
        >>> print(status)
        📊 AGOR Strategy Status
        **Strategy**: Parallel Divergent
        **Task**: implement user authentication
        **Phase**: Divergent
        **Recent Activity**:
          agent1: 2024-01-15 14:30 - CLAIMING ASSIGNMENT
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
