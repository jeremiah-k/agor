"""
Parallel Divergent Strategy Implementation for AGOR.

This strategy involves multiple agents working independently on the same problem,
then converging to review and synthesize the best solution from all approaches.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

# Dual-mode importing for bundle and package compatibility
try:
    from ..project_planning_templates import generate_parallel_divergent_strategy
except ImportError:
    # Bundle-mode fallback
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from project_planning_templates import generate_parallel_divergent_strategy


class StrategyProtocol:
    """Base class for strategy implementation protocols."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.agor_dir = self.project_root / ".agor"
        self.ensure_agor_structure()

    def ensure_agor_structure(self):
        """Ensure .agor directory structure exists."""
        self.agor_dir.mkdir(exist_ok=True)

        # Create essential coordination files if they don't exist
        essential_files = {
            "agentconvo.md": "# Agent Communication Log\n\n",
            "memory.md": "# Project Memory\n\n## Current Strategy\nNone active\n\n",
        }

        for filename, default_content in essential_files.items():
            file_path = self.agor_dir / filename
            if not file_path.exists():
                file_path.write_text(default_content)

    def log_communication(self, agent_id: str, message: str):
        """Log a message to agentconvo.md following AGOR protocol."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{agent_id}: {timestamp} - {message}\n"

        agentconvo_file = self.agor_dir / "agentconvo.md"
        with open(agentconvo_file, "a") as f:
            f.write(log_entry)


class ParallelDivergentProtocol(StrategyProtocol):
    """Implementation protocol for Parallel Divergent strategy."""

    def initialize_strategy(self, task_description: str, agent_count: int = 3) -> str:
        """Initialize Parallel Divergent strategy following AGOR protocols."""

        # Create strategy-active.md with template content
        strategy_content = generate_parallel_divergent_strategy()

        # Add concrete implementation details
        implementation_details = f"""
## IMPLEMENTATION PROTOCOL

### Task: {task_description}
### Agents: {agent_count}
### Status: Phase 1 - Divergent Execution (ACTIVE)

## AGENT ASSIGNMENTS
{self._generate_agent_assignments(agent_count, task_description)}

## CURRENT PHASE: Divergent Execution

### Rules for ALL Agents:
1. **NO COORDINATION** - Work completely independently
2. **Branch isolation** - Each agent works on their assigned branch
3. **Document decisions** - Update your agent memory file regularly
4. **Signal completion** - Post to agentconvo.md when Phase 1 complete

### Phase 1 Completion Criteria:
- All agents have working implementations on their branches
- All agent memory files are updated with approach documentation
- All agents have posted "PHASE1_COMPLETE" to agentconvo.md

### Phase Transition:
When all agents signal completion, strategy automatically moves to Phase 2 (Convergent Review)

## AGENT INSTRUCTIONS

Each agent should:
1. **Read your assignment** below
2. **Create your branch**: `git checkout -b [your-branch]`
3. **Initialize memory file**: Create `.agor/[agent-id]-memory.md`
4. **Work independently** - NO coordination with other agents
5. **Document approach** in your memory file
6. **Signal completion** when done

{self._generate_individual_instructions(agent_count, task_description)}
"""

        # Combine template with implementation
        full_strategy = strategy_content + implementation_details

        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)

        # Create individual agent memory file templates
        self._create_agent_memory_templates(agent_count)

        # Log strategy initialization
        self.log_communication(
            "COORDINATOR",
            f"Initialized Parallel Divergent strategy: {task_description}",
        )

        return f"""✅ Parallel Divergent Strategy Initialized

**Task**: {task_description}
**Agents**: {agent_count}
**Phase**: 1 - Divergent Execution

**Next Steps for Agents**:
1. Check your assignment in `.agor/strategy-active.md`
2. Create your branch and memory file
3. Begin independent work
4. Signal completion when done

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and agent assignments
- `.agor/agent[N]-memory.md` - Individual agent memory templates

**Ready for agent coordination!**
"""

    def _generate_agent_assignments(
        self, agent_count: int, task_description: str
    ) -> str:
        """Generate agent assignments section."""
        assignments = []

        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            branch_name = f"solution-{agent_id}"
            assignments.append(
                f"""
### Agent{i} Assignment
- **Agent ID**: {agent_id}
- **Branch**: `{branch_name}`
- **Memory File**: `.agor/{agent_id}-memory.md`
- **Status**: ⚪ Not Started
- **Mission**: {task_description} (independent approach)
"""
            )

        return "\n".join(assignments)

    def _generate_individual_instructions(
        self, agent_count: int, task_description: str
    ) -> str:
        """Generate individual agent instructions."""
        instructions = []

        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            branch_name = f"solution-{agent_id}"

            instruction = f"""
### {agent_id.upper()} INSTRUCTIONS

**Your Mission**: {task_description}
**Your Branch**: `{branch_name}`
**Your Memory File**: `.agor/{agent_id}-memory.md`

**Setup Commands**:
```bash
# Create your branch
git checkout -b {branch_name}

# Initialize your memory file (if not already created)
# Edit .agor/{agent_id}-memory.md with your approach
```

**Work Protocol**:
1. Plan your unique approach to the problem
2. Document your approach in your memory file
3. Implement your solution independently
4. Test your implementation thoroughly
5. Update memory file with decisions and findings
6. Signal completion when ready

**Completion Signal**:
When you finish your solution, post this to agentconvo.md:
```
{agent_id}: [timestamp] - PHASE1_COMPLETE - Solution ready for review
```

**Remember**: Work independently! No coordination with other agents during Phase 1.
"""
            instructions.append(instruction)

        return "\n".join(instructions)

    def _create_agent_memory_templates(self, agent_count: int):
        """Create individual agent memory file templates."""
        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            memory_file = self.agor_dir / f"{agent_id}-memory.md"

            if not memory_file.exists():
                memory_content = f"""# {agent_id.upper()} Memory File

## Current Assignment
- **Strategy**: Parallel Divergent
- **Phase**: 1 - Divergent Execution
- **Status**: Not Started

## My Approach
[Document your unique approach to the problem here]

## Technical Decisions
[Record key technical decisions and rationale]

## Implementation Notes
[Track implementation progress and findings]

## Challenges & Solutions
[Document any challenges encountered and how you solved them]

## Phase 1 Completion
- [ ] Solution implemented
- [ ] Tests passing
- [ ] Approach documented
- [ ] Ready for review
"""
                memory_file.write_text(memory_content)


def initialize_parallel_divergent(task: str, agent_count: int = 3) -> str:
    """Initialize Parallel Divergent strategy."""
    protocol = ParallelDivergentProtocol()
    return protocol.initialize_strategy(task, agent_count)
