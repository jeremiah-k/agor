"""
Strategy management for AGOR multi-agent coordination.

Handles initialization, state management, and coordination for different
development strategies including Parallel Divergent, Pipeline, Swarm, etc.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from agor.tools.git_operations import run_git_command

from .memory_sync import MemorySyncManager


class StrategyManager:
    """Manages multi-agent development strategies and coordination state."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize strategy manager."""
        self.project_root = project_root or Path.cwd()
        self.agor_dir = self.project_root / ".agor"
        self.state_dir = self.agor_dir / "state"
        self.memory_manager = MemorySyncManager(self.project_root)

    def init_coordination(self, task: str, agents: int = 3) -> None:
        """Initialize .agor/ directory and coordination files."""
        print("🎼 Initializing AGOR coordination system...")

        # Create directory structure
        self._create_agor_structure()

        # Initialize basic coordination files
        self._init_basic_files(task, agents)

        # Initialize memory sync for agent workflows
        self._init_memory_sync_for_agents()

        # Log initialization
        self._log_event(f"Initialized .agor/ coordination for task: {task}")

        print(f"✅ AGOR coordination initialized for {agents} agents")
        print(f"📁 Directory: {self.agor_dir}")
        print(f"🎯 Task: {task}")

    def setup_parallel_divergent(self, task: str, agents: int = 3) -> None:
        """Set up Parallel Divergent strategy with state management."""
        if agents < 2 or agents > 6:
            print("❌ Error: Parallel Divergent requires 2-6 agents")
            return

        print(f"🔄 Setting up Parallel Divergent strategy for {agents} agents...")

        # Ensure coordination is initialized
        if not self.agor_dir.exists():
            self.init_coordination(task, agents)

        # Create state directory and files
        self._create_state_structure()

        # Generate agent branches
        agent_branches = self._create_agent_branches(task, agents)

        # Initialize strategy state files
        self._init_pd_state_files(task, agents, agent_branches)

        # Create agent prompts and instructions
        self._create_agent_instructions(task, agents, agent_branches)

        # Log strategy setup
        self._log_event(f"Initialized Parallel Divergent strategy for task: {task}")

        print("✅ Parallel Divergent strategy initialized!")
        print(f"🌿 Agent branches: {', '.join(agent_branches.values())}")
        print("📋 Next: Assign agents to their respective branches")
        print("📖 Instructions: See .agor/agent-instructions/")

    def show_status(self) -> None:
        """Display current coordination status."""
        if not self.agor_dir.exists():
            print("❌ No AGOR coordination found. Run 'agor init <task>' first.")
            return

        print("📊 AGOR Coordination Status")
        print("=" * 50)

        # Show basic info
        if (self.agor_dir / "memory.md").exists():
            print("✅ Basic coordination files present")

        # Show strategy info
        if self.state_dir.exists():
            strategy_file = self.state_dir / "strategy.json"
            if strategy_file.exists():
                with open(strategy_file) as f:
                    strategy = json.load(f)
                print(f"🔄 Active Strategy: {strategy.get('mode', 'unknown')}")
                print(f"🎯 Task: {strategy.get('task', 'unknown')}")
                print(f"👥 Agents: {len(strategy.get('agents', []))}")

        # Show memory sync status
        self._show_memory_sync_status()

        # Show agent status
        self._show_agent_status()

        # Show recent activity
        self._show_recent_activity()

    def sync_state(self) -> None:
        """Pull latest changes and update coordination status."""
        print("🔄 Syncing coordination state...")

        try:
            # Pull latest changes
            success, output = run_git_command(["pull"])

            if success:
                print("✅ Git pull successful")
            else:
                # output from run_git_command contains stderr in case of error
                print(f"⚠️  Git pull warning/error: {output}")

            # Update sync flags
            if self.state_dir.exists():
                sync_file = self.state_dir / "sync_flags.yaml"
                sync_data = {"last_sync": datetime.now().isoformat()}

                if sync_file.exists():
                    with open(sync_file) as f:
                        existing = yaml.safe_load(f) or {}
                    sync_data.update(existing)

                with open(sync_file, "w") as f:
                    yaml.dump(sync_data, f, default_flow_style=False)

            self._log_event("Synchronized coordination state")
            print("✅ Coordination state synchronized")

        except Exception as e:
            print(f"❌ Sync failed: {e}")

    def suggest_strategy(self, complexity: str, team_size: int) -> None:
        """Analyze project and recommend optimal development strategy."""
        print("🧠 Analyzing project for strategy recommendation...")
        print("=" * 50)

        # Basic project analysis
        project_files = (
            list(self.project_root.glob("**/*.py"))
            + list(self.project_root.glob("**/*.js"))
            + list(self.project_root.glob("**/*.ts"))
            + list(self.project_root.glob("**/*.java"))
            + list(self.project_root.glob("**/*.go"))
        )

        file_count = len(project_files)

        print(f"📁 Project files: {file_count}")
        print(f"🔧 Complexity: {complexity}")
        print(f"👥 Team size: {team_size}")
        print()

        # Strategy recommendations
        recommendations = self._analyze_strategy_fit(complexity, team_size, file_count)

        print("🎯 Strategy Recommendations:")
        print("-" * 30)

        for i, (strategy, score, reason) in enumerate(recommendations, 1):
            print(f"{i}. {strategy} (Score: {score}/10)")
            print(f"   {reason}")
            print()

        print("💡 To initialize recommended strategy:")
        best_strategy = recommendations[0][0]
        if "Parallel Divergent" in best_strategy:
            print(f'   agor pd "your-task-description" --agents {team_size}')
        elif "Pipeline" in best_strategy:
            print(f'   agor pl "your-task-description" --agents {team_size}')
        elif "Swarm" in best_strategy:
            print(f'   agor sw "your-task-description" --agents {team_size}')

    def _create_agor_structure(self) -> None:
        """Create basic .agor directory structure."""
        self.agor_dir.mkdir(exist_ok=True)
        (self.agor_dir / "snapshots").mkdir(exist_ok=True)  # Changed from handoffs
        (self.agor_dir / "agent-instructions").mkdir(exist_ok=True)

    def _create_state_structure(self) -> None:
        """Create .agor/state directory structure."""
        self.state_dir.mkdir(exist_ok=True)

    def _init_basic_files(self, task: str, agents: int) -> None:
        """Initialize basic coordination files."""
        # Agent communication log
        agentconvo_file = self.agor_dir / "agentconvo.md"
        if not agentconvo_file.exists():
            agentconvo_file.write_text("# Agent Communication Log\n\n")

        # Project memory
        memory_file = self.agor_dir / "memory.md"
        if not memory_file.exists():
            memory_content = f"""# Project Memory

## Task
{task}

## Team Configuration
- Agents: {agents}
- Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Decisions
- Strategy coordination initialized

## Current State
- Coordination system ready
- Awaiting strategy selection
"""
            memory_file.write_text(memory_content)

    def _create_agent_branches(self, task: str, agents: int) -> Dict[str, str]:
        """Create git branches for each agent."""
        agent_branches = {}
        task_slug = task.lower().replace(" ", "-").replace("_", "-")[:20]

        for i in range(1, agents + 1):
            agent_id = f"agent{i}"
            branch_name = f"{agent_id}/{task_slug}"
            agent_branches[agent_id] = branch_name

            # Create branch if it doesn't exist
            # Using run_git_command. Assuming project_root is the correct cwd.
            # run_git_command doesn't have check=False, it returns (success, output).
            # We want to create if not exists, so if it fails because it exists, that's okay.
            # If it fails for other reasons, that might be an issue.
            # For now, mimic check=False by not strictly checking `success`.
            run_git_command(["checkout", "-b", branch_name])
            # Original code used try/except Exception: pass. This is similar.

        # Return to main branch
        # Try 'main' first, then 'master'
        success_main, _ = run_git_command(["checkout", "main"])
        if not success_main:
            run_git_command(["checkout", "master"])
            # Ignoring success/failure of checkout master as per original logic

        return agent_branches

    def _init_pd_state_files(
        self, task: str, agents: int, agent_branches: Dict[str, str]
    ) -> None:
        """Initialize Parallel Divergent state files."""
        # Strategy configuration
        strategy_data = {
            "mode": "pd",
            "task": task,
            "agents": list(agent_branches.keys()),
            "created": datetime.now().isoformat(),
            "status": "initialized",
        }

        with open(self.state_dir / "strategy.json", "w") as f:
            json.dump(strategy_data, f, indent=2)

        # Agent branches mapping
        with open(self.state_dir / "agent_branches.json", "w") as f:
            json.dump(agent_branches, f, indent=2)

        # Active tasks status
        active_tasks = {agent: "pending" for agent in agent_branches.keys()}
        with open(self.state_dir / "active_tasks.json", "w") as f:
            json.dump(active_tasks, f, indent=2)

        # Parallel Divergent evaluation template
        pd_eval_content = f"""# Parallel Divergent Evaluation

## Task: {task}

## Agents & Branches
{chr(10).join(f"- **{agent}**: `{branch}`" for agent, branch in agent_branches.items())}

## Phase 1: Divergent Execution (In Progress)
- [ ] Agent 1 solution
- [ ] Agent 2 solution
- [ ] Agent 3 solution

## Phase 2: Convergent Review (Pending)
- [ ] Cross-agent code review
- [ ] Solution comparison
- [ ] Best practices identification

## Phase 3: Synthesis (Pending)
- [ ] Merge best approaches
- [ ] Final implementation
- [ ] Documentation update

## Notes
*Add evaluation notes here as agents complete their work*
"""

        with open(self.state_dir / "pd_evaluation.md", "w") as f:
            f.write(pd_eval_content)

        # Sync flags
        sync_data = {
            "pd_merge_pending": False,
            "last_sync": datetime.now().isoformat(),
            "agents_ready": 0,
            "total_agents": agents,
        }

        with open(self.state_dir / "sync_flags.yaml", "w") as f:
            yaml.dump(sync_data, f, default_flow_style=False)

    def _create_agent_instructions(
        self, task: str, agents: int, agent_branches: Dict[str, str]
    ) -> None:
        """Create individual agent instruction files."""
        instructions_dir = self.agor_dir / "agent-instructions"
        instructions_dir.mkdir(exist_ok=True)

        for agent_id, branch_name in agent_branches.items():
            instruction_content = f"""# {agent_id.upper()} Instructions

## Mission
{task}

## Your Branch
`{branch_name}`

## Strategy: Parallel Divergent
You are working **independently** with {agents-1} other agents on the same problem.

### Phase 1: Divergent Execution (Current)
1. **Switch to your branch**: `git checkout {branch_name}`
2. **Work independently** - no coordination with other agents
3. **Implement your solution** using your unique approach
4. **Commit regularly** with clear messages
5. **Document your approach** in your solution

### Phase 2: Convergent Review (Later)
- Review other agents' solutions
- Provide constructive feedback
- Identify best practices and innovations

### Phase 3: Synthesis (Final)
- Collaborate to merge best approaches
- Create final unified solution

## Success Criteria
- Complete, working implementation
- Clear documentation of your approach
- Code that passes existing tests
- Innovative or unique perspective on the problem

## Communication
- Update `.agor/agentconvo.md` with major progress
- Use your agent memory file: `.agor/{agent_id}-memory.md`
- No coordination during Phase 1 - work independently!

## Ready to Start?
1. `git checkout {branch_name}`
2. Begin your independent implementation
3. Focus on your unique approach to the problem
"""

            with open(instructions_dir / f"{agent_id}-instructions.md", "w") as f:
                f.write(instruction_content)

    def _log_event(self, message: str) -> None:
        """Log coordination event to state.log."""
        if not self.state_dir.exists():
            return

        log_file = self.state_dir / "state.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(log_file, "a") as f:
            f.write(log_entry)

    def _show_agent_status(self) -> None:
        """Show current agent status."""
        if not self.state_dir.exists():
            return

        tasks_file = self.state_dir / "active_tasks.json"
        if tasks_file.exists():
            with open(tasks_file) as f:
                tasks = json.load(f)

            print("\n👥 Agent Status:")
            for agent, status in tasks.items():
                status_icon = (
                    "🟢"
                    if status == "completed"
                    else "🟡" if status == "in-progress" else "⚪"
                )
                print(f"   {status_icon} {agent}: {status}")

    def _show_recent_activity(self) -> None:
        """Show recent coordination activity."""
        if not self.state_dir.exists():
            return

        log_file = self.state_dir / "state.log"
        if log_file.exists():
            print("\n📝 Recent Activity:")
            lines = log_file.read_text().strip().split("\n")
            for line in lines[-5:]:  # Show last 5 entries
                if line.strip():
                    print(f"   {line}")

    def update_agent_status(self, agent_id: str, status: str) -> None:
        """Update agent status in coordination system."""
        if not self.state_dir.exists():
            print("❌ No active strategy found. Run 'agor pd <task>' first.")
            return

        valid_statuses = ["pending", "in-progress", "completed"]
        if status not in valid_statuses:
            print(f"❌ Invalid status. Use: {', '.join(valid_statuses)}")
            return

        # Update active tasks
        tasks_file = self.state_dir / "active_tasks.json"
        if tasks_file.exists():
            with open(tasks_file) as f:
                tasks = json.load(f)

            if agent_id not in tasks:
                print(f"❌ Agent {agent_id} not found in current strategy")
                return

            old_status = tasks[agent_id]
            tasks[agent_id] = status

            with open(tasks_file, "w") as f:
                json.dump(tasks, f, indent=2)

            # Update sync flags if agent completed
            if status == "completed" and old_status != "completed":
                self._update_completion_count()

            # Log the status change
            self._log_event(f"Agent {agent_id} status: {old_status} → {status}")

            print(f"✅ Updated {agent_id} status: {old_status} → {status}")

            # Check if all agents are ready for merge
            self._check_merge_readiness()
        else:
            print("❌ No active tasks file found")

    def _update_completion_count(self) -> None:
        """Update the count of completed agents in sync flags."""
        tasks_file = self.state_dir / "active_tasks.json"
        sync_file = self.state_dir / "sync_flags.yaml"

        if tasks_file.exists() and sync_file.exists():
            with open(tasks_file) as f:
                tasks = json.load(f)

            completed_count = sum(
                1 for status in tasks.values() if status == "completed"
            )

            with open(sync_file) as f:
                sync_data = yaml.safe_load(f) or {}

            sync_data["agents_ready"] = completed_count
            sync_data["last_update"] = datetime.now().isoformat()

            with open(sync_file, "w") as f:
                yaml.dump(sync_data, f, default_flow_style=False)

    def _check_merge_readiness(self) -> None:
        """Check if all agents are ready for merge phase."""
        tasks_file = self.state_dir / "active_tasks.json"
        sync_file = self.state_dir / "sync_flags.yaml"

        if tasks_file.exists() and sync_file.exists():
            with open(tasks_file) as f:
                tasks = json.load(f)

            with open(sync_file) as f:
                sync_data = yaml.safe_load(f) or {}

            completed_count = sum(
                1 for status in tasks.values() if status == "completed"
            )
            total_agents = len(tasks)

            if completed_count == total_agents:
                sync_data["pd_merge_pending"] = True

                with open(sync_file, "w") as f:
                    yaml.dump(sync_data, f, default_flow_style=False)

                self._log_event("All agents completed - merge phase ready")
                print("🎉 All agents completed! Ready for convergent review phase.")
                print("📋 Next steps:")
                print("   1. Review all agent solutions")
                print("   2. Compare approaches in .agor/state/pd_evaluation.md")
                print("   3. Merge best practices into final solution")

    def _analyze_strategy_fit(
        self, complexity: str, team_size: int, file_count: int
    ) -> List[tuple]:
        """Analyze and score different strategies for the project."""
        strategies = []

        # Parallel Divergent scoring
        pd_score = 7
        if complexity == "complex":
            pd_score += 2
        if 2 <= team_size <= 4:
            pd_score += 1
        if file_count > 50:
            pd_score += 1

        strategies.append(
            (
                "🔄 Parallel Divergent",
                min(pd_score, 10),
                "Multiple independent solutions, then peer review and synthesis",
            )
        )

        # Pipeline scoring
        pl_score = 6
        if complexity in ["medium", "complex"]:
            pl_score += 1
        if 3 <= team_size <= 5:
            pl_score += 2
        if file_count > 20:
            pl_score += 1

        strategies.append(
            (
                "⚡ Pipeline",
                min(pl_score, 10),
                "Sequential work via snapshots with specialization at each stage",
            )
        )

        # Swarm scoring
        sw_score = 5
        if team_size >= 5:
            sw_score += 3
        if file_count > 100:
            sw_score += 2
        if complexity == "simple":
            sw_score += 1

        strategies.append(
            (
                "🐝 Swarm",
                min(sw_score, 10),
                "Dynamic task assignment from shared queue - great for many small tasks",
            )
        )

        # Sort by score (descending)
        strategies.sort(key=lambda x: x[1], reverse=True)

        return strategies

    def _init_memory_sync_for_agents(self) -> None:
        """Initialize memory sync for agent workflows."""
        try:
            # Memory sync is already initialized via MemorySyncManager
            # This method provides explicit feedback about memory sync status
            if self.memory_manager:
                active_branch = self.memory_manager.get_active_memory_branch()
                if active_branch:
                    print(f"🧠 Memory sync active on branch: {active_branch}")
                else:
                    print("🧠 Memory sync initialized (no active branch yet)")
            else:
                print(
                    "⚠️ Memory sync not available - continuing without memory persistence"
                )
        except Exception as e:
            print(f"⚠️ Memory sync initialization warning: {e}")
            # Don't fail coordination setup if memory sync has issues

    def _show_memory_sync_status(self) -> None:
        """Show current memory sync status."""
        try:
            if (
                hasattr(self.memory_manager, "memory_sync_manager")
                and self.memory_manager.memory_sync_manager
            ):
                active_branch = self.memory_manager.get_active_memory_branch()
                if active_branch:
                    print(f"🧠 Memory Sync: Active on branch '{active_branch}'")

                    # Show available memory branches
                    memory_sync = self.memory_manager.memory_sync_manager
                    local_branches = memory_sync.list_memory_branches(remote=False)
                    remote_branches = memory_sync.list_memory_branches(remote=True)

                    if local_branches or remote_branches:
                        all_branches = sorted(
                            list(set(local_branches + remote_branches)), reverse=True
                        )
                        print(
                            f"   Available memory branches: {', '.join(all_branches[:3])}{'...' if len(all_branches) > 3 else ''}"
                        )
                else:
                    print("🧠 Memory Sync: Initialized (no active branch)")
            else:
                print("⚠️ Memory Sync: Not available")
        except Exception as e:
            print(f"⚠️ Memory Sync: Error - {e}")
