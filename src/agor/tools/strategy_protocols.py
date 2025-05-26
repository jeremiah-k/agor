"""
Strategy Implementation Protocols for AGOR Multi-Agent Coordination.

This module provides concrete implementation protocols that bridge the gap between
AGOR's strategy documentation and actual agent execution. These protocols work with
the existing template system to provide step-by-step execution guidance.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .project_planning_templates import (
    generate_parallel_divergent_strategy,
    generate_pipeline_strategy, 
    generate_swarm_strategy,
    generate_red_team_strategy,
    generate_mob_programming_strategy
)


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
            "memory.md": "# Project Memory\n\n## Current Strategy\nNone active\n\n"
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
        self.log_communication("COORDINATOR", f"Initialized Parallel Divergent strategy: {task_description}")
        
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
    
    def _generate_agent_assignments(self, agent_count: int, task_description: str) -> str:
        """Generate agent assignments section."""
        task_slug = task_description.lower().replace(" ", "-")[:20]
        assignments = []
        
        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            branch_name = f"solution-{agent_id}"
            assignments.append(f"""
### Agent{i} Assignment
- **Agent ID**: {agent_id}
- **Branch**: `{branch_name}`
- **Memory File**: `.agor/{agent_id}-memory.md`
- **Status**: ⚪ Not Started
- **Mission**: {task_description} (independent approach)
""")
        
        return "\n".join(assignments)
    
    def _generate_individual_instructions(self, agent_count: int, task_description: str) -> str:
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
        """Create agent memory file templates."""
        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            memory_file = self.agor_dir / f"{agent_id}-memory.md"
            
            if not memory_file.exists():
                memory_content = f"""# {agent_id.upper()} Memory Log

## Current Task
[Describe the task you're working on]

## My Approach
[Describe your unique approach to solving this problem]

## Decisions Made
- [Key architectural choices]
- [Implementation approaches]
- [Technology decisions]

## Files Modified
- [List of changed files with brief description]

## Problems Encountered
- [Issues hit and how resolved]

## Next Steps
- [ ] Planning complete
- [ ] Core implementation
- [ ] Testing complete
- [ ] Documentation updated
- [ ] Ready for review

## Notes for Review
- [Important points for peer review phase]
- [Innovative approaches used]
- [Potential improvements]

## Status
Current: Working on independent solution
Phase: 1 - Divergent Execution
"""
                memory_file.write_text(memory_content)
    
    def check_phase_transition(self) -> Optional[str]:
        """Check if phase transition should occur."""
        agentconvo_file = self.agor_dir / "agentconvo.md"
        
        if not agentconvo_file.exists():
            return None
        
        content = agentconvo_file.read_text()
        completion_signals = content.count("PHASE1_COMPLETE")
        
        # Count expected agents from strategy file
        strategy_file = self.agor_dir / "strategy-active.md"
        if strategy_file.exists():
            strategy_content = strategy_file.read_text()
            expected_agents = strategy_content.count("### Agent")
            
            if completion_signals >= expected_agents:
                return "transition_to_convergent"
        
        return None
    
    def transition_to_convergent_phase(self) -> str:
        """Transition from divergent to convergent phase."""
        strategy_file = self.agor_dir / "strategy-active.md"
        
        if not strategy_file.exists():
            return "❌ No active strategy found"
        
        content = strategy_file.read_text()
        
        # Update phase status
        updated_content = content.replace(
            "### Status: Phase 1 - Divergent Execution (ACTIVE)",
            "### Status: Phase 2 - Convergent Review (ACTIVE)"
        )
        
        # Add convergent phase instructions
        convergent_instructions = """

## PHASE 2: CONVERGENT REVIEW (ACTIVE)

### Review Protocol
All agents now review each other's solutions and provide feedback.

### Review Process:
1. **Examine all solutions** - Check every agent's branch
2. **Document findings** - Use the review template below
3. **Identify strengths** - Note innovative approaches and solid implementations
4. **Flag weaknesses** - Point out problems, bugs, or missing requirements
5. **Propose synthesis** - Recommend which components to combine

### Review Template:
For each agent's solution, add a review to agentconvo.md:

```
REVIEW: [agent-id] by [your-agent-id]
BRANCH: [branch-name]

STRENGTHS:
- [Specific good implementations]
- [Clever approaches]
- [Robust error handling]

WEAKNESSES:
- [Problematic code]
- [Missing edge cases]
- [Performance issues]

RECOMMENDATIONS:
- ADOPT: [Components to use in final solution]
- AVOID: [Components to reject]
- MODIFY: [Components needing changes]

OVERALL SCORE: [1-10]
```

### Convergent Phase Completion:
- All agents review all solutions
- Synthesis recommendations are documented
- Consensus on final approach is reached
- Ready to move to Phase 3 (Synthesis)
"""
        
        updated_content += convergent_instructions
        strategy_file.write_text(updated_content)
        
        # Log phase transition
        self.log_communication("COORDINATOR", "PHASE TRANSITION: Divergent → Convergent Review")
        
        return """✅ Phase Transition Complete

**New Phase**: 2 - Convergent Review
**Action Required**: All agents review each other's solutions

**Next Steps**:
1. Examine all agent branches
2. Document findings using review template
3. Propose synthesis approach
4. Build consensus on final solution

**Phase 2 is now active!**
"""


class PipelineProtocol(StrategyProtocol):
    """Implementation protocol for Pipeline strategy."""
    
    def initialize_strategy(self, task_description: str, stages: List[str] = None) -> str:
        """Initialize Pipeline strategy following AGOR protocols."""
        
        if stages is None:
            stages = ["Foundation", "Enhancement", "Refinement", "Validation"]
        
        # Create strategy-active.md with template content
        strategy_content = generate_pipeline_strategy()
        
        # Add concrete implementation details
        implementation_details = f"""
## IMPLEMENTATION PROTOCOL

### Task: {task_description}
### Stages: {len(stages)}
### Status: Stage 1 - {stages[0]} (ACTIVE)

## PIPELINE STAGES
{self._generate_stage_assignments(stages)}

## CURRENT STAGE: {stages[0]}

### Stage Assignment Protocol:
1. **One agent per stage** - Only one agent works on active stage
2. **Sequential execution** - Stages must complete in order
3. **Handoff required** - Each stage creates handoff for next stage
4. **Quality gates** - Each stage includes validation before handoff

### Stage Completion Protocol:
1. Complete all stage deliverables
2. Test your work thoroughly
3. Create handoff document using template
4. Signal stage completion in agentconvo.md
5. Next agent claims the following stage

## STAGE INSTRUCTIONS

### Current Stage: {stages[0]}
**Status**: Waiting for agent assignment
**Agent**: TBD

**To claim this stage**, post to agentconvo.md:
```
[agent-id]: [timestamp] - CLAIMING STAGE 1: {stages[0]}
```

{self._generate_stage_instructions(stages)}
"""
        
        # Combine template with implementation
        full_strategy = strategy_content + implementation_details
        
        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)
        
        # Create handoff directory
        handoff_dir = self.agor_dir / "handoffs"
        handoff_dir.mkdir(exist_ok=True)
        
        # Log strategy initialization
        self.log_communication("COORDINATOR", f"Initialized Pipeline strategy: {task_description}")
        
        return f"""✅ Pipeline Strategy Initialized

**Task**: {task_description}
**Stages**: {len(stages)}
**Current Stage**: 1 - {stages[0]}

**Next Steps**:
1. First agent claims Stage 1: {stages[0]}
2. Complete stage deliverables
3. Create handoff for next stage
4. Continue pipeline sequence

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and stage assignments
- `.agor/handoffs/` - Directory for stage handoffs

**Ready for first agent to claim Stage 1!**
"""
    
    def _generate_stage_assignments(self, stages: List[str]) -> str:
        """Generate stage assignments section."""
        assignments = []
        
        for i, stage in enumerate(stages, 1):
            status = "🔄 ACTIVE" if i == 1 else "⏳ PENDING"
            assignments.append(f"""
### Stage {i}: {stage}
- **Status**: {status}
- **Agent**: TBD
- **Deliverables**: [Stage-specific deliverables]
- **Handoff**: Required for next stage
""")
        
        return "\n".join(assignments)
    
    def _generate_stage_instructions(self, stages: List[str]) -> str:
        """Generate instructions for each stage."""
        instructions = []
        
        stage_responsibilities = {
            "Foundation": [
                "Create basic project structure",
                "Implement core functionality", 
                "Set up testing framework",
                "Establish coding standards"
            ],
            "Enhancement": [
                "Add advanced features",
                "Implement business logic",
                "Create API endpoints",
                "Add error handling"
            ],
            "Refinement": [
                "Optimize performance",
                "Improve error handling",
                "Add logging and monitoring",
                "Code cleanup and refactoring"
            ],
            "Validation": [
                "Comprehensive testing",
                "Security review",
                "Documentation completion",
                "Deployment preparation"
            ]
        }
        
        for i, stage in enumerate(stages, 1):
            responsibilities = stage_responsibilities.get(stage, [f"Complete {stage} requirements"])
            
            instruction = f"""
### Stage {i}: {stage} Instructions

**Responsibilities**:
{chr(10).join(f"- {resp}" for resp in responsibilities)}

**Deliverables**:
- Working implementation for this stage
- Updated tests and documentation
- Handoff document for next stage

**Handoff Template**:
```
# Stage {i} to Stage {i+1} Handoff

## Completed Work
- [List everything completed in this stage]
- [Include file paths and descriptions]

## Key Decisions Made
- [Important choices and rationale]

## For Next Stage Agent
- [Specific tasks for next stage]
- [Context and constraints]
- [Files to focus on]

## Validation
- [How to verify the work]
- [Tests to run]
- [Acceptance criteria]
```

**Completion Signal**:
```
[agent-id]: [timestamp] - STAGE{i}_COMPLETE: {stage} - Handoff ready
```
"""
            instructions.append(instruction)
        
        return "\n".join(instructions)


class SwarmProtocol(StrategyProtocol):
    """Implementation protocol for Swarm strategy."""
    
    def initialize_strategy(self, task_description: str, task_list: List[str], agent_count: int = 4) -> str:
        """Initialize Swarm strategy following AGOR protocols."""
        
        # Create strategy-active.md with template content
        strategy_content = generate_swarm_strategy()
        
        # Create task queue file
        task_queue = {
            "strategy": "swarm",
            "description": task_description,
            "created": datetime.now().isoformat(),
            "total_agents": agent_count,
            "tasks": [
                {
                    "id": i + 1,
                    "description": task,
                    "status": "available",
                    "assigned_to": None,
                    "started_at": None,
                    "completed_at": None
                }
                for i, task in enumerate(task_list)
            ]
        }
        
        # Save task queue
        queue_file = self.agor_dir / "task-queue.json"
        with open(queue_file, "w") as f:
            json.dump(task_queue, f, indent=2)
        
        # Add implementation details to strategy
        implementation_details = f"""
## IMPLEMENTATION PROTOCOL

### Task: {task_description}
### Total Tasks: {len(task_list)}
### Agents: {agent_count}
### Status: ACTIVE

## TASK QUEUE
See `task-queue.json` for current task status.

## SWARM PROTOCOL

### Task Claiming Process:
1. **Check available tasks**: Look at `task-queue.json`
2. **Pick a task**: Choose based on your skills/interest
3. **Claim the task**: Update JSON file with your agent ID
4. **Announce claim**: Post to agentconvo.md
5. **Work independently**: Complete your claimed task
6. **Mark complete**: Update JSON and announce completion
7. **Pick next task**: Repeat until queue is empty

### Task Queue Management:
```bash
# View available tasks
cat .agor/task-queue.json | grep '"status": "available"'

# Claim task (edit the JSON file):
# 1. Find task with "status": "available"
# 2. Change "status" to "in_progress"
# 3. Set "assigned_to" to your agent ID
# 4. Set "started_at" to current timestamp
```

### Communication Protocol:
```
# Claim announcement
[agent-id]: [timestamp] - CLAIMED TASK [N]: [task description]

# Completion announcement  
[agent-id]: [timestamp] - COMPLETED TASK [N]: [task description]
```

## CURRENT TASK STATUS
{self._generate_task_status(task_list)}

## AGENT INSTRUCTIONS

### For All Agents:
1. **Check task queue** regularly for available tasks
2. **Claim tasks** by updating task-queue.json
3. **Work independently** on your claimed tasks
4. **Communicate progress** via agentconvo.md
5. **Help others** if you finish early and queue is empty

### Task Completion Criteria:
- Task implementation is complete and tested
- Code is committed to repository
- Task status is updated in queue
- Completion is announced in agentconvo.md
"""
        
        # Combine template with implementation
        full_strategy = strategy_content + implementation_details
        
        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)
        
        # Log strategy initialization
        self.log_communication("COORDINATOR", f"Initialized Swarm strategy with {len(task_list)} tasks")
        
        return f"""✅ Swarm Strategy Initialized

**Task**: {task_description}
**Total Tasks**: {len(task_list)}
**Agents**: {agent_count}

**Next Steps**:
1. Agents check task queue in `.agor/task-queue.json`
2. Claim available tasks by updating the JSON
3. Work independently on claimed tasks
4. Mark complete and claim next task

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and instructions
- `.agor/task-queue.json` - Task queue with {len(task_list)} tasks

**Ready for agents to start claiming tasks!**
"""
    
    def _generate_task_status(self, task_list: List[str]) -> str:
        """Generate current task status display."""
        status_lines = []
        
        for i, task in enumerate(task_list, 1):
            status_lines.append(f"- **Task {i}**: {task} (Status: Available)")
        
        return "\n".join(status_lines)


# Factory function to get appropriate protocol
def get_strategy_protocol(strategy: str) -> StrategyProtocol:
    """Get the appropriate strategy protocol implementation."""
    protocols = {
        "pd": ParallelDivergentProtocol,
        "parallel_divergent": ParallelDivergentProtocol,
        "pl": PipelineProtocol,
        "pipeline": PipelineProtocol,
        "sw": SwarmProtocol,
        "swarm": SwarmProtocol
    }
    
    protocol_class = protocols.get(strategy.lower(), StrategyProtocol)
    return protocol_class()


# Convenience functions for strategy initialization
def initialize_parallel_divergent(task: str, agent_count: int = 3) -> str:
    """Initialize Parallel Divergent strategy."""
    protocol = ParallelDivergentProtocol()
    return protocol.initialize_strategy(task, agent_count)


def initialize_pipeline(task: str, stages: List[str] = None) -> str:
    """Initialize Pipeline strategy."""
    protocol = PipelineProtocol()
    return protocol.initialize_strategy(task, stages)


def initialize_swarm(task: str, task_list: List[str], agent_count: int = 4) -> str:
    """Initialize Swarm strategy."""
    protocol = SwarmProtocol()
    return protocol.initialize_strategy(task, task_list, agent_count)
