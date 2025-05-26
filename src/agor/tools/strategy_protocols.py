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


class RedTeamProtocol(StrategyProtocol):
    """Implementation protocol for Red Team strategy."""

    def initialize_strategy(self, task_description: str, blue_team_size: int = 3, red_team_size: int = 3) -> str:
        """Initialize Red Team strategy following AGOR protocols."""

        # Create strategy-active.md with template content
        from .project_planning_templates import generate_red_team_strategy
        strategy_content = generate_red_team_strategy()

        # Add concrete implementation details
        implementation_details = f"""
## IMPLEMENTATION PROTOCOL

### Task: {task_description}
### Blue Team: {blue_team_size} agents
### Red Team: {red_team_size} agents
### Status: Phase 1 - Blue Team Build (ACTIVE)

## TEAM ASSIGNMENTS
{self._generate_team_assignments(blue_team_size, red_team_size, task_description)}

## CURRENT PHASE: Blue Team Build

### Phase 1: Blue Team Build (ACTIVE)
**Objective**: Implement robust, secure solution
**Duration**: Until Blue Team signals completion
**Rules**:
- Blue Team works independently to build the feature
- Focus on security, robustness, and error handling
- Document security measures and assumptions
- Create comprehensive test suite
- Signal completion when ready for Red Team attack

### Phase 2: Red Team Attack (PENDING)
**Objective**: Find vulnerabilities and break the implementation
**Duration**: Until Red Team exhausts attack vectors
**Rules**:
- Red Team attempts to break Blue Team's implementation
- Document all vulnerabilities and attack vectors found
- Focus on security, performance, and edge case failures
- Provide detailed attack reports

### Phase 3: Analysis & Hardening (PENDING)
**Objective**: Fix vulnerabilities and improve robustness
**Duration**: Until Red Team can no longer break the system
**Rules**:
- Blue Team fixes all discovered vulnerabilities
- Red Team validates fixes and attempts new attacks
- Continue cycles until system is sufficiently hardened

## BLUE TEAM INSTRUCTIONS

### Current Objective: Build Robust Implementation
1. **Analyze requirements** with security mindset
2. **Design defensively** - assume adversarial usage
3. **Implement with security** - input validation, access control, error handling
4. **Test thoroughly** - unit tests, integration tests, security tests
5. **Document security measures** - what protections are in place
6. **Signal completion** when ready for Red Team attack

### Security Checklist:
- [ ] Input validation on all user inputs
- [ ] Authentication and authorization controls
- [ ] Error handling that doesn't leak information
- [ ] Rate limiting and resource protection
- [ ] Secure data storage and transmission
- [ ] Logging and monitoring capabilities

### Completion Signal:
```
BLUE_TEAM: [timestamp] - BUILD_COMPLETE - Ready for Red Team attack
```

## RED TEAM INSTRUCTIONS (Phase 2)

### Attack Vectors to Test:
1. **Security Attacks**:
   - Authentication bypass attempts
   - Authorization escalation
   - Input injection (SQL, XSS, etc.)
   - Session management flaws
   - Cryptographic weaknesses

2. **Performance Attacks**:
   - Resource exhaustion (DoS)
   - Memory leaks
   - CPU intensive operations
   - Database query bombing
   - File system attacks

3. **Logic Attacks**:
   - Race conditions
   - Edge case exploitation
   - Business logic bypass
   - State manipulation
   - Workflow circumvention

4. **Integration Attacks**:
   - API misuse
   - Dependency exploitation
   - Configuration manipulation
   - Environment variable injection
   - Third-party service abuse

### Attack Documentation Template:
```
ATTACK: [attack-name] by [red-agent-id]
VECTOR: [how the attack works]
IMPACT: [what damage could be done]
EVIDENCE: [proof of concept or reproduction steps]
SEVERITY: [Critical/High/Medium/Low]
RECOMMENDATION: [how to fix this vulnerability]
```

## CYCLE MANAGEMENT

### Phase Transitions:
1. **Blue → Red**: When Blue Team signals BUILD_COMPLETE
2. **Red → Analysis**: When Red Team completes attack phase
3. **Analysis → Blue**: When vulnerabilities are documented
4. **Repeat**: Until Red Team finds no new vulnerabilities

### Success Criteria:
- Blue Team implementation is robust and secure
- Red Team cannot find additional vulnerabilities
- All discovered issues have been fixed and validated
- System passes comprehensive security review
"""

        # Combine template with implementation
        full_strategy = strategy_content + implementation_details

        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)

        # Create team memory file templates
        self._create_team_memory_templates(blue_team_size, red_team_size)

        # Create attack tracking file
        self._create_attack_tracking_file()

        # Log strategy initialization
        self.log_communication("COORDINATOR", f"Initialized Red Team strategy: {task_description}")

        return f"""✅ Red Team Strategy Initialized

**Task**: {task_description}
**Blue Team**: {blue_team_size} agents (Builders)
**Red Team**: {red_team_size} agents (Breakers)
**Phase**: 1 - Blue Team Build

**Next Steps**:
1. Blue Team builds robust, secure implementation
2. Red Team prepares attack strategies
3. Begin adversarial cycles when Blue Team completes

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and team assignments
- `.agor/blue-team-memory.md` - Blue Team coordination
- `.agor/red-team-memory.md` - Red Team attack planning
- `.agor/attack-tracking.md` - Vulnerability and attack documentation

**Ready for Blue Team to begin building!**
"""

    def _generate_team_assignments(self, blue_team_size: int, red_team_size: int, task_description: str) -> str:
        """Generate team assignments section."""
        task_slug = task_description.lower().replace(" ", "-")[:20]

        assignments = []

        # Blue Team assignments
        assignments.append("### Blue Team (Builders)")
        blue_roles = ["Architect", "Developer", "Security-Tester", "Integration-Specialist", "Quality-Assurance"]
        for i in range(blue_team_size):
            role = blue_roles[i % len(blue_roles)]
            agent_id = f"blue{i+1}"
            branch_name = f"blue-team/{task_slug}"
            assignments.append(f"- **{agent_id}** ({role}): `{branch_name}` - 🔄 Building")

        assignments.append("\n### Red Team (Breakers)")
        red_roles = ["Security-Analyst", "Chaos-Engineer", "Edge-Case-Hunter", "Performance-Tester", "Integration-Attacker"]
        for i in range(red_team_size):
            role = red_roles[i % len(red_roles)]
            agent_id = f"red{i+1}"
            assignments.append(f"- **{agent_id}** ({role}): Attack planning - ⏳ Waiting")

        return "\n".join(assignments)

    def _create_team_memory_templates(self, blue_team_size: int, red_team_size: int):
        """Create team memory file templates."""

        # Blue Team memory file
        blue_memory_file = self.agor_dir / "blue-team-memory.md"
        blue_memory_content = f"""# Blue Team Memory Log

## Current Task
[Describe the secure implementation you're building]

## Security Strategy
[Describe your defensive approach and security measures]

## Implementation Progress
- [ ] Requirements analysis with security focus
- [ ] Defensive architecture design
- [ ] Core functionality implementation
- [ ] Security controls implementation
- [ ] Comprehensive testing
- [ ] Security documentation
- [ ] Ready for Red Team attack

## Security Measures Implemented
- [List specific security controls and protections]

## Files Modified
- [List of changed files with security implications]

## Security Assumptions
- [Document security assumptions and threat model]

## Test Coverage
- [Describe security tests and validation]

## Known Limitations
- [Document any known security limitations or trade-offs]

## Status
Current: Building secure implementation
Phase: 1 - Blue Team Build
Team Size: {blue_team_size} agents
"""
        blue_memory_file.write_text(blue_memory_content)

        # Red Team memory file
        red_memory_file = self.agor_dir / "red-team-memory.md"
        red_memory_content = f"""# Red Team Memory Log

## Target Analysis
[Analyze the Blue Team's implementation for attack vectors]

## Attack Strategy
[Describe your overall attack approach and methodology]

## Attack Planning
- [ ] Reconnaissance and target analysis
- [ ] Attack vector identification
- [ ] Exploit development
- [ ] Attack execution
- [ ] Vulnerability documentation
- [ ] Impact assessment

## Attack Vectors Identified
- [List potential attack vectors and approaches]

## Exploits Developed
- [Document working exploits and proof of concepts]

## Vulnerabilities Found
- [List discovered vulnerabilities with severity]

## Attack Results
- [Document successful attacks and their impact]

## Recommendations
- [Provide recommendations for fixing vulnerabilities]

## Status
Current: Planning attacks
Phase: 1 - Waiting for Blue Team completion
Team Size: {red_team_size} agents
"""
        red_memory_file.write_text(red_memory_content)

    def _create_attack_tracking_file(self):
        """Create attack tracking file for vulnerability documentation."""
        attack_file = self.agor_dir / "attack-tracking.md"
        attack_content = """# Red Team Attack Tracking

## Attack Summary

| Attack ID | Vector | Severity | Status | Assigned To | Fixed |
|-----------|--------|----------|--------|-------------|-------|
| | | | | | |

## Detailed Attack Reports

### Template for New Attacks
```
## ATTACK-001: [Attack Name]
**Discovered by**: [red-agent-id]
**Date**: [timestamp]
**Vector**: [attack method]
**Severity**: [Critical/High/Medium/Low]

### Description
[Detailed description of the vulnerability]

### Reproduction Steps
1. [Step by step reproduction]
2. [Include code/commands if applicable]

### Impact
[What damage could this cause?]

### Evidence
[Screenshots, logs, or proof of concept]

### Recommendation
[How to fix this vulnerability]

### Blue Team Response
[Blue Team's fix and validation]

### Validation
[Red Team validation of the fix]
```

## Attack Statistics

- **Total Attacks**: 0
- **Critical**: 0
- **High**: 0
- **Medium**: 0
- **Low**: 0
- **Fixed**: 0
- **Remaining**: 0

## Cycle History

### Cycle 1: Initial Build
- **Blue Team Build**: [timestamp] - [status]
- **Red Team Attack**: [timestamp] - [status]
- **Vulnerabilities Found**: [count]
- **Fixes Applied**: [count]

[Add additional cycles as they occur]
"""
        attack_file.write_text(attack_content)


class MobProgrammingProtocol(StrategyProtocol):
    """Implementation protocol for Mob Programming strategy."""

    def initialize_strategy(self, task_description: str, agent_count: int = 4) -> str:
        """Initialize Mob Programming strategy following AGOR protocols."""

        # Create strategy-active.md with template content
        from .project_planning_templates import generate_mob_programming_strategy
        strategy_content = generate_mob_programming_strategy()

        # Add concrete implementation details
        implementation_details = f"""
## IMPLEMENTATION PROTOCOL

### Task: {task_description}
### Agents: {agent_count}
### Status: Session 1 - Problem Definition (ACTIVE)

## AGENT ASSIGNMENTS
{self._generate_mob_assignments(agent_count, task_description)}

## CURRENT SESSION: Problem Definition

### Session Structure (Rotate every 15-20 minutes):
1. **Problem Definition** (Current) - All agents understand the task
2. **Approach Discussion** - Brief strategy alignment
3. **Coding Session** - Rotate roles while coding
4. **Review** - Collective code review and refinement

### Role Rotation Schedule:
{self._generate_rotation_schedule(agent_count)}

## CURRENT ROLES
- **Driver**: {self._get_initial_driver(agent_count)} (Types code, implements decisions)
- **Navigator**: {self._get_initial_navigator(agent_count)} (Guides direction, tactical decisions)
- **Observers**: {self._get_initial_observers(agent_count)} (Review code, suggest improvements)
- **Researcher**: {self._get_initial_researcher(agent_count)} (Documentation, investigation)

## COLLABORATION PROTOCOL

### Communication Format:
```
DRIVER: "I'm implementing [specific action]..."
NAVIGATOR: "Let's [tactical suggestion]"
OBSERVER: "Consider [improvement suggestion]"
RESEARCHER: "Found [relevant information]"
```

### Session Rules:
1. **Only Driver types** - Others guide through discussion
2. **Navigator leads direction** - Makes tactical decisions
3. **Observers catch errors** - Continuous code review
4. **Researcher provides context** - Documentation, best practices
5. **Rotate every 15-20 minutes** - Everyone gets all roles
6. **Collective decisions** - Major choices discussed by all

### Rotation Protocol:
```
ROTATION: [timestamp] - [session-number]
Previous Driver → Observer
Previous Navigator → Driver
Previous Observer → Navigator
Previous Researcher → Observer
[Next agent] → Researcher
```

## SESSION INSTRUCTIONS

### Session 1: Problem Definition (CURRENT)
**Objective**: Ensure all agents understand the task
**Duration**: 15-20 minutes
**Activities**:
- Review requirements and constraints
- Discuss success criteria
- Identify key challenges
- Align on overall approach
- Set up development environment

**Completion Signal**:
```
MOB: [timestamp] - SESSION1_COMPLETE - Ready for approach discussion
```

### Session 2: Approach Discussion (NEXT)
**Objective**: Align on technical strategy
**Duration**: 15-20 minutes
**Activities**:
- Discuss architecture options
- Choose technology approach
- Plan implementation steps
- Identify potential risks
- Create task breakdown

### Session 3+: Coding Sessions
**Objective**: Collaborative implementation
**Duration**: 15-20 minutes per rotation
**Activities**:
- Driver implements current task
- Navigator guides implementation
- Observers provide continuous review
- Researcher supports with documentation
- Rotate roles regularly

## COLLABORATION WORKSPACE

### Shared Branch: `mob-programming/{task_description.lower().replace(' ', '-')[:20]}`
### Communication: Real-time via `.agor/agentconvo.md`
### Code Review: Continuous during implementation
### Documentation: Collective in `.agor/mob-session-log.md`

## SUCCESS CRITERIA
- All agents understand the complete solution
- High-quality code through continuous review
- Knowledge shared across all team members
- Collective ownership of the implementation
- No handoff required - everyone knows everything
"""

        # Combine template with implementation
        full_strategy = strategy_content + implementation_details

        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)

        # Create mob session log
        self._create_mob_session_log(task_description, agent_count)

        # Log strategy initialization
        self.log_communication("COORDINATOR", f"Initialized Mob Programming strategy: {task_description}")

        return f"""✅ Mob Programming Strategy Initialized

**Task**: {task_description}
**Agents**: {agent_count}
**Session**: 1 - Problem Definition

**Current Roles**:
- Driver: {self._get_initial_driver(agent_count)}
- Navigator: {self._get_initial_navigator(agent_count)}
- Observers: {self._get_initial_observers(agent_count)}
- Researcher: {self._get_initial_researcher(agent_count)}

**Next Steps**:
1. All agents join collaborative session
2. Begin with problem definition and alignment
3. Rotate roles every 15-20 minutes
4. Maintain continuous communication

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and role assignments
- `.agor/mob-session-log.md` - Session tracking and decisions

**Ready for collaborative session to begin!**
"""

    def _generate_mob_assignments(self, agent_count: int, task_description: str) -> str:
        """Generate mob programming assignments."""
        task_slug = task_description.lower().replace(" ", "-")[:20]
        branch_name = f"mob-programming/{task_slug}"

        assignments = []
        assignments.append(f"### Shared Workspace: `{branch_name}`")
        assignments.append("### All Agents Collaborate Simultaneously")

        for i in range(1, agent_count + 1):
            agent_id = f"agent{i}"
            assignments.append(f"- **{agent_id}**: Collaborative participant - 🔄 Active")

        return "\n".join(assignments)

    def _generate_rotation_schedule(self, agent_count: int) -> str:
        """Generate role rotation schedule."""
        agents = [f"agent{i}" for i in range(1, agent_count + 1)]

        schedule = []
        schedule.append("| Session | Driver | Navigator | Observer(s) | Researcher |")
        schedule.append("|---------|--------|-----------|-------------|------------|")

        for session in range(1, min(agent_count + 1, 6)):  # Show first 5 rotations
            driver_idx = (session - 1) % agent_count
            navigator_idx = (session) % agent_count
            researcher_idx = (session + 1) % agent_count

            observers = []
            for i in range(agent_count):
                if i not in [driver_idx, navigator_idx, researcher_idx]:
                    observers.append(agents[i])

            observer_str = ", ".join(observers) if observers else "N/A"

            schedule.append(f"| {session} | {agents[driver_idx]} | {agents[navigator_idx]} | {observer_str} | {agents[researcher_idx]} |")

        return "\n".join(schedule)

    def _get_initial_driver(self, agent_count: int) -> str:
        return "agent1"

    def _get_initial_navigator(self, agent_count: int) -> str:
        return "agent2" if agent_count > 1 else "agent1"

    def _get_initial_observers(self, agent_count: int) -> str:
        if agent_count <= 2:
            return "N/A"
        elif agent_count == 3:
            return "agent3"
        else:
            observers = [f"agent{i}" for i in range(3, min(agent_count, 5))]
            return ", ".join(observers)

    def _get_initial_researcher(self, agent_count: int) -> str:
        return f"agent{min(agent_count, 4)}"

    def _create_mob_session_log(self, task_description: str, agent_count: int):
        """Create mob programming session log."""
        log_file = self.agor_dir / "mob-session-log.md"
        log_content = f"""# Mob Programming Session Log

## Task: {task_description}
## Team: {agent_count} agents
## Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Session History

### Session 1: Problem Definition (ACTIVE)
**Started**: [timestamp]
**Roles**: Driver: agent1, Navigator: agent2, Observer(s): [others], Researcher: agent{min(agent_count, 4)}
**Objective**: Understand requirements and align on approach
**Progress**:
- [ ] Requirements reviewed
- [ ] Success criteria defined
- [ ] Key challenges identified
- [ ] Overall approach agreed
- [ ] Development environment ready

**Decisions Made**:
- [Record key decisions and rationale]

**Next Session**: Approach Discussion

---

### Session Template for Future Sessions
```
### Session [N]: [Session Name]
**Started**: [timestamp]
**Completed**: [timestamp]
**Roles**: Driver: [agent], Navigator: [agent], Observer(s): [agents], Researcher: [agent]
**Objective**: [what this session aimed to accomplish]
**Progress**:
- [ ] [specific tasks completed]

**Code Changes**:
- [files modified and key changes]

**Decisions Made**:
- [important decisions and rationale]

**Challenges Encountered**:
- [problems faced and how resolved]

**Next Session**: [what's planned next]
```

## Collective Knowledge

### Architecture Decisions
- [Record architectural choices made collectively]

### Implementation Patterns
- [Document patterns and approaches used]

### Lessons Learned
- [Capture insights and learning from the session]

### Code Quality Notes
- [Document quality improvements and refactoring]

## Final Summary

**Total Sessions**: [count]
**Total Duration**: [time]
**Lines of Code**: [count]
**Key Achievements**:
- [major accomplishments]

**Team Feedback**:
- [what worked well]
- [what could be improved]
- [knowledge gained by each agent]
"""
        log_file.write_text(log_content)


# Factory function to get appropriate protocol
def get_strategy_protocol(strategy: str) -> StrategyProtocol:
    """Get the appropriate strategy protocol implementation."""
    protocols = {
        "pd": ParallelDivergentProtocol,
        "parallel_divergent": ParallelDivergentProtocol,
        "pl": PipelineProtocol,
        "pipeline": PipelineProtocol,
        "sw": SwarmProtocol,
        "swarm": SwarmProtocol,
        "rt": RedTeamProtocol,
        "red_team": RedTeamProtocol,
        "mb": MobProgrammingProtocol,
        "mob_programming": MobProgrammingProtocol,
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


def initialize_red_team(task: str, blue_team_size: int = 3, red_team_size: int = 3) -> str:
    """Initialize Red Team strategy."""
    protocol = RedTeamProtocol()
    return protocol.initialize_strategy(task, blue_team_size, red_team_size)


def initialize_mob_programming(task: str, agent_count: int = 4) -> str:
    """Initialize Mob Programming strategy."""
    protocol = MobProgrammingProtocol()
    return protocol.initialize_strategy(task, agent_count)


def project_breakdown(task_description: str, complexity: str = "medium") -> str:
    """Generate project breakdown with task decomposition (bp hotkey)."""

    # Import the project breakdown template
    from .project_planning_templates import generate_project_breakdown_template

    # Get the base template
    template = generate_project_breakdown_template()

    # Add concrete implementation guidance
    implementation_guidance = f"""
## IMPLEMENTATION GUIDANCE

### Task: {task_description}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## CONCRETE TASK BREAKDOWN

{_generate_concrete_breakdown(task_description, complexity)}

## AGENT ASSIGNMENT RECOMMENDATIONS

{_generate_agent_assignments(task_description, complexity)}

## EXECUTION SEQUENCE

{_generate_execution_sequence(complexity)}

## COORDINATION PROTOCOL

### Communication:
- Use `.agor/agentconvo.md` for cross-agent updates
- Update individual `.agor/agent[N]-memory.md` files
- Post task completion signals in agentconvo.md

### Task Tracking:
```
TASK_START: [agent-id] - [task-name] - [timestamp]
TASK_PROGRESS: [agent-id] - [task-name] - [percentage]% - [timestamp]
TASK_COMPLETE: [agent-id] - [task-name] - [deliverables] - [timestamp]
TASK_BLOCKED: [agent-id] - [task-name] - [blocker-description] - [timestamp]
```

### Handoff Triggers:
- When task dependencies are met
- When agent expertise is needed
- When integration points are reached
- When quality gates require validation

## QUALITY GATES

### Phase 1: Analysis Complete
- [ ] Requirements documented and validated
- [ ] Architecture design approved
- [ ] Task dependencies mapped
- [ ] Risk assessment completed

### Phase 2: Design Complete
- [ ] System design documented
- [ ] API contracts defined
- [ ] Database schema approved
- [ ] Integration points specified

### Phase 3: Implementation Complete
- [ ] Core functionality implemented
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Code review completed

### Phase 4: Quality Complete
- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Documentation updated

### Phase 5: Deployment Ready
- [ ] Deployment scripts tested
- [ ] Monitoring configured
- [ ] Documentation complete
- [ ] Stakeholder approval received

## NEXT STEPS

1. **Review breakdown** - Validate task decomposition with stakeholders
2. **Assign agents** - Match tasks to agent expertise
3. **Initialize coordination** - Set up .agor/ files and communication
4. **Begin execution** - Start with Phase 1 tasks
5. **Monitor progress** - Track completion and handle blockers
"""

    # Combine template with implementation
    full_breakdown = template + implementation_guidance

    # Save to project breakdown file
    breakdown_file = Path(".agor") / "project-breakdown.md"
    breakdown_file.parent.mkdir(exist_ok=True)
    breakdown_file.write_text(full_breakdown)

    return f"""✅ Project Breakdown Generated

**Task**: {task_description}
**Complexity**: {complexity}
**File**: `.agor/project-breakdown.md`

**Breakdown Includes**:
- Concrete task decomposition
- Agent assignment recommendations
- Execution sequence and dependencies
- Quality gates and checkpoints
- Coordination protocols

**Next Steps**:
1. Review the breakdown in `.agor/project-breakdown.md`
2. Assign tasks to appropriate agents
3. Initialize coordination with `init` command
4. Begin execution with Phase 1 tasks

**Ready to coordinate project execution!**
"""


def _generate_concrete_breakdown(task_description: str, complexity: str) -> str:
    """Generate concrete task breakdown based on description and complexity."""

    # Analyze task type
    task_lower = task_description.lower()

    if any(word in task_lower for word in ["api", "backend", "service", "endpoint"]):
        return _generate_api_breakdown(task_description, complexity)
    elif any(word in task_lower for word in ["ui", "frontend", "interface", "component"]):
        return _generate_frontend_breakdown(task_description, complexity)
    elif any(word in task_lower for word in ["database", "data", "schema", "migration"]):
        return _generate_database_breakdown(task_description, complexity)
    elif any(word in task_lower for word in ["auth", "security", "login", "permission"]):
        return _generate_security_breakdown(task_description, complexity)
    else:
        return _generate_generic_breakdown(task_description, complexity)


def _generate_api_breakdown(task_description: str, complexity: str) -> str:
    """Generate API-specific task breakdown."""
    tasks = [
        "**API Design**: Define endpoints, request/response schemas, error handling",
        "**Data Models**: Create database models and validation logic",
        "**Core Logic**: Implement business logic and data processing",
        "**Authentication**: Add authentication and authorization",
        "**Testing**: Unit tests, integration tests, API documentation",
        "**Deployment**: Containerization, deployment scripts, monitoring"
    ]

    if complexity == "complex":
        tasks.extend([
            "**Performance**: Caching, optimization, load testing",
            "**Security**: Security audit, penetration testing",
            "**Documentation**: Comprehensive API docs, examples"
        ])

    return "\n".join(f"- {task}" for task in tasks)


def _generate_frontend_breakdown(task_description: str, complexity: str) -> str:
    """Generate frontend-specific task breakdown."""
    tasks = [
        "**UI Design**: Wireframes, mockups, design system components",
        "**Component Development**: Reusable UI components and layouts",
        "**State Management**: Application state, data flow, API integration",
        "**User Experience**: Navigation, forms, error handling",
        "**Testing**: Component tests, integration tests, accessibility",
        "**Build & Deploy**: Build optimization, deployment pipeline"
    ]

    if complexity == "complex":
        tasks.extend([
            "**Performance**: Code splitting, lazy loading, optimization",
            "**Accessibility**: WCAG compliance, screen reader support",
            "**Internationalization**: Multi-language support, localization"
        ])

    return "\n".join(f"- {task}" for task in tasks)


def _generate_database_breakdown(task_description: str, complexity: str) -> str:
    """Generate database-specific task breakdown."""
    tasks = [
        "**Schema Design**: Tables, relationships, constraints, indexes",
        "**Migration Scripts**: Database creation, data migration, rollback",
        "**Data Access**: ORM setup, queries, stored procedures",
        "**Data Validation**: Input validation, business rules, constraints",
        "**Testing**: Data integrity tests, performance tests",
        "**Backup & Recovery**: Backup strategy, disaster recovery"
    ]

    if complexity == "complex":
        tasks.extend([
            "**Performance**: Query optimization, indexing strategy, partitioning",
            "**Security**: Access controls, encryption, audit logging",
            "**Scalability**: Replication, sharding, connection pooling"
        ])

    return "\n".join(f"- {task}" for task in tasks)


def _generate_security_breakdown(task_description: str, complexity: str) -> str:
    """Generate security-specific task breakdown."""
    tasks = [
        "**Authentication**: User login, session management, password policies",
        "**Authorization**: Role-based access, permissions, resource protection",
        "**Input Validation**: Sanitization, injection prevention, data validation",
        "**Secure Communication**: HTTPS, encryption, secure headers",
        "**Testing**: Security tests, vulnerability scanning",
        "**Monitoring**: Security logging, intrusion detection, alerting"
    ]

    if complexity == "complex":
        tasks.extend([
            "**Advanced Auth**: Multi-factor authentication, SSO, OAuth integration",
            "**Compliance**: GDPR, SOC2, security audit preparation",
            "**Threat Modeling**: Risk assessment, attack vector analysis"
        ])

    return "\n".join(f"- {task}" for task in tasks)


def _generate_generic_breakdown(task_description: str, complexity: str) -> str:
    """Generate generic task breakdown."""
    tasks = [
        "**Requirements Analysis**: Gather and document detailed requirements",
        "**Architecture Design**: System design, component architecture",
        "**Core Implementation**: Primary functionality development",
        "**Integration**: Connect components, external services",
        "**Testing**: Unit tests, integration tests, user acceptance",
        "**Documentation**: Technical docs, user guides, deployment"
    ]

    if complexity == "complex":
        tasks.extend([
            "**Performance Optimization**: Profiling, optimization, scalability",
            "**Security Review**: Security assessment, vulnerability testing",
            "**Monitoring & Maintenance**: Logging, monitoring, support procedures"
        ])

    return "\n".join(f"- {task}" for task in tasks)


def _generate_agent_assignments(task_description: str, complexity: str) -> str:
    """Generate agent assignment recommendations."""

    base_assignments = [
        "**Analyst Agent**: Requirements analysis, stakeholder communication",
        "**Architect Agent**: System design, technical architecture",
        "**Developer Agent**: Core implementation, coding",
        "**Tester Agent**: Test creation, quality assurance",
        "**DevOps Agent**: Deployment, infrastructure, monitoring"
    ]

    if complexity == "complex":
        base_assignments.extend([
            "**Security Agent**: Security review, vulnerability assessment",
            "**Performance Agent**: Optimization, scalability, benchmarking",
            "**Documentation Agent**: Technical writing, user guides"
        ])

    return "\n".join(f"- {assignment}" for assignment in base_assignments)


def _generate_execution_sequence(complexity: str) -> str:
    """Generate execution sequence based on complexity."""

    if complexity == "simple":
        return """
### Simple Project Sequence:
1. **Analysis** (1-2 days): Requirements → Design
2. **Implementation** (3-5 days): Development → Testing
3. **Deployment** (1 day): Deploy → Monitor

**Total Estimated Duration**: 5-8 days
**Recommended Team Size**: 2-3 agents
**Coordination Level**: Low (daily check-ins)
"""
    elif complexity == "complex":
        return """
### Complex Project Sequence:
1. **Analysis Phase** (1-2 weeks): Requirements → Architecture → Planning
2. **Design Phase** (1-2 weeks): Detailed design → Prototyping → Review
3. **Implementation Phase** (3-6 weeks): Development → Integration → Testing
4. **Quality Phase** (1-2 weeks): Security → Performance → Documentation
5. **Deployment Phase** (1 week): Deploy → Monitor → Support

**Total Estimated Duration**: 7-13 weeks
**Recommended Team Size**: 5-8 agents
**Coordination Level**: High (daily standups, weekly reviews)
"""
    else:  # medium
        return """
### Medium Project Sequence:
1. **Analysis Phase** (3-5 days): Requirements → Architecture
2. **Implementation Phase** (1-3 weeks): Development → Testing
3. **Quality Phase** (3-5 days): Review → Optimization
4. **Deployment Phase** (2-3 days): Deploy → Monitor

**Total Estimated Duration**: 2-5 weeks
**Recommended Team Size**: 3-5 agents
**Coordination Level**: Medium (bi-daily check-ins)
"""


def strategy_selection(project_analysis: str = "", team_size: int = 3, complexity: str = "medium") -> str:
    """Analyze project and recommend optimal development strategy (ss hotkey)."""

    # Import the strategy selection template
    from .agent_prompt_templates import generate_strategy_selection_prompt

    # Generate strategy analysis
    analysis = f"""
# 🎯 Strategy Selection Analysis

## Project Context
{project_analysis if project_analysis else "No specific project analysis provided"}

## Team Configuration
- **Team Size**: {team_size} agents
- **Complexity**: {complexity}

## Strategy Recommendations

### 🔄 Parallel Divergent (Score: {_score_parallel_divergent(team_size, complexity)}/10)
**Best for**: Complex problems, multiple valid approaches, creative solutions
**Process**: Independent solutions → peer review → synthesis
**Team Size**: 2-6 agents (optimal: 3-4)
**Timeline**: Medium (parallel execution + review time)

**Pros**: Redundancy, diversity, innovation, quality through peer review
**Cons**: Requires review coordination, potential for conflicting approaches

### ⚡ Pipeline (Score: {_score_pipeline(team_size, complexity)}/10)
**Best for**: Sequential dependencies, specialization, predictable workflows
**Process**: Foundation → Enhancement → Refinement → Validation
**Team Size**: 3-5 agents (optimal: 4)
**Timeline**: Medium (sequential but focused)

**Pros**: Clear dependencies, specialization, incremental progress
**Cons**: Sequential bottlenecks, less parallelism

### 🐝 Swarm (Score: {_score_swarm(team_size, complexity)}/10)
**Best for**: Many independent tasks, speed priority, large codebases
**Process**: Task queue → dynamic assignment → emergent solution
**Team Size**: 5-8 agents (optimal: 6)
**Timeline**: Fast (maximum parallelism)

**Pros**: Maximum parallelism, flexibility, resilience
**Cons**: Requires good task decomposition, potential integration challenges

### ⚔️ Red Team (Score: {_score_red_team(team_size, complexity)}/10)
**Best for**: Security-critical, high-reliability, complex integration
**Process**: Build → Break → Analyze → Harden → Repeat
**Team Size**: 4-6 agents (2-3 per team)
**Timeline**: Slow (thorough validation)

**Pros**: Robustness, security, high confidence
**Cons**: Time-intensive, requires adversarial mindset

### 👥 Mob Programming (Score: {_score_mob_programming(team_size, complexity)}/10)
**Best for**: Knowledge sharing, complex problems, team alignment
**Process**: Collaborative coding with rotating roles
**Team Size**: 3-5 agents (optimal: 4)
**Timeline**: Medium (intensive collaboration)

**Pros**: Knowledge sharing, continuous review, consensus
**Cons**: Coordination overhead, requires real-time collaboration

## 🎯 Recommendation

{_get_top_recommendation(team_size, complexity)}

## 🚀 Next Steps

To initialize your chosen strategy:

```python
# Parallel Divergent
from agor.tools.strategy_protocols import initialize_parallel_divergent
result = initialize_parallel_divergent("your task description", agent_count={team_size})

# Pipeline
from agor.tools.strategy_protocols import initialize_pipeline
result = initialize_pipeline("your task description", stages=["Foundation", "Enhancement", "Testing"])

# Swarm
from agor.tools.strategy_protocols import initialize_swarm
tasks = ["task1", "task2", "task3", "task4"]  # Define your task list
result = initialize_swarm("your task description", tasks, agent_count={team_size})

# Red Team
from agor.tools.strategy_protocols import initialize_red_team
result = initialize_red_team("your task description", blue_team_size=3, red_team_size=3)

# Mob Programming
from agor.tools.strategy_protocols import initialize_mob_programming
result = initialize_mob_programming("your task description", agent_count={team_size})
```

Or use the agent coordination helper:
```python
from agor.tools.agent_coordination import discover_my_role
print(discover_my_role("agent1"))  # Get immediate next actions
```
"""

    return analysis


def _score_parallel_divergent(team_size: int, complexity: str) -> int:
    """Score Parallel Divergent strategy for given parameters."""
    score = 7  # Base score

    if complexity == "complex":
        score += 2
    elif complexity == "simple":
        score -= 1

    if 2 <= team_size <= 4:
        score += 1
    elif team_size > 5:
        score -= 1

    return min(score, 10)


def _score_pipeline(team_size: int, complexity: str) -> int:
    """Score Pipeline strategy for given parameters."""
    score = 6  # Base score

    if complexity in ["medium", "complex"]:
        score += 1

    if 3 <= team_size <= 5:
        score += 2
    elif team_size < 3:
        score -= 1
    elif team_size > 5:
        score -= 1

    return min(score, 10)


def _score_swarm(team_size: int, complexity: str) -> int:
    """Score Swarm strategy for given parameters."""
    score = 5  # Base score

    if team_size >= 5:
        score += 3
    elif team_size < 4:
        score -= 2

    if complexity == "simple":
        score += 2
    elif complexity == "complex":
        score -= 1

    return min(score, 10)


def _score_red_team(team_size: int, complexity: str) -> int:
    """Score Red Team strategy for given parameters."""
    score = 4  # Base score

    if complexity == "complex":
        score += 3
    elif complexity == "simple":
        score -= 1

    if 4 <= team_size <= 6:
        score += 2
    elif team_size < 4:
        score -= 2

    return min(score, 10)


def _score_mob_programming(team_size: int, complexity: str) -> int:
    """Score Mob Programming strategy for given parameters."""
    score = 6  # Base score

    if complexity == "complex":
        score += 1

    if 3 <= team_size <= 5:
        score += 1
    elif team_size > 5:
        score -= 2
    elif team_size < 3:
        score -= 1

    return min(score, 10)


def _get_top_recommendation(team_size: int, complexity: str) -> str:
    """Get the top strategy recommendation."""
    scores = {
        "Parallel Divergent": _score_parallel_divergent(team_size, complexity),
        "Pipeline": _score_pipeline(team_size, complexity),
        "Swarm": _score_swarm(team_size, complexity),
        "Red Team": _score_red_team(team_size, complexity),
        "Mob Programming": _score_mob_programming(team_size, complexity)
    }

    top_strategy = max(scores, key=scores.get)
    top_score = scores[top_strategy]

    return f"**Recommended Strategy**: {top_strategy} (Score: {top_score}/10)\n\nBased on your team size ({team_size}) and complexity ({complexity}), {top_strategy} offers the best balance of effectiveness, coordination overhead, and expected outcomes."


def create_team(project_description: str, team_size: int = 4, project_type: str = "web_app", complexity: str = "medium") -> str:
    """Create and organize development team structure (ct hotkey)."""

    # Import the team creation template
    from .project_planning_templates import generate_team_creation_template

    # Get the base template
    template = generate_team_creation_template()

    # Add concrete team implementation
    implementation_details = f"""
## CONCRETE TEAM IMPLEMENTATION

### Project: {project_description}
### Team Size: {team_size} agents
### Project Type: {project_type}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## RECOMMENDED TEAM STRUCTURE

{_generate_team_structure(team_size, project_type, complexity)}

## COORDINATION SETUP

### Communication Structure:
```
.agor/agentconvo.md - Main team communication
.agor/team-structure.md - Team roles and responsibilities
.agor/agent[N]-memory.md - Individual agent memory files
.agor/team-coordination.md - Team coordination protocols
```

### Daily Coordination Protocol:
1. **Morning Standup** (async via agentconvo.md):
   ```
   [AGENT-ID] [TIMESTAMP] - STANDUP: [yesterday's work] | [today's plan] | [blockers]
   ```

2. **Progress Updates** (throughout day):
   ```
   [AGENT-ID] [TIMESTAMP] - PROGRESS: [task] - [status] - [next steps]
   ```

3. **Handoff Coordination** (when needed):
   ```
   [AGENT-ID] [TIMESTAMP] - HANDOFF_REQUEST: [to-agent] - [task] - [deliverables]
   [TO-AGENT] [TIMESTAMP] - HANDOFF_ACCEPTED: [task] - [estimated completion]
   ```

4. **Blocker Resolution** (immediate):
   ```
   [AGENT-ID] [TIMESTAMP] - BLOCKER: [description] - [help needed]
   [HELPER-ID] [TIMESTAMP] - BLOCKER_ASSIST: [solution/guidance]
   ```

## ROLE RESPONSIBILITIES

{_generate_role_responsibilities(team_size, project_type, complexity)}

## SUCCESS METRICS

### Team Performance Tracking:
- **Daily Velocity**: Tasks completed per day
- **Quality Metrics**: Code review feedback, bug rates
- **Collaboration Score**: Communication frequency, help requests/responses
- **Delivery Metrics**: Sprint completion, milestone achievement

### Individual Performance:
- **Task Completion**: On-time delivery, quality of work
- **Team Contribution**: Help provided, knowledge sharing
- **Innovation**: Creative solutions, process improvements
- **Growth**: Skill development, learning new technologies

## TEAM INITIALIZATION CHECKLIST

- [ ] **Team Structure Defined**: Roles assigned, responsibilities clear
- [ ] **Communication Setup**: .agor files created, protocols established
- [ ] **Development Environment**: Shared tools, standards, conventions
- [ ] **Project Planning**: Milestones defined, tasks prioritized
- [ ] **Quality Standards**: Code review process, testing requirements
- [ ] **Risk Assessment**: Potential issues identified, mitigation plans ready
- [ ] **Success Metrics**: KPIs defined, tracking mechanisms in place
- [ ] **Kickoff Meeting**: Team alignment, questions answered

## NEXT STEPS

1. **Review Team Structure**: Validate roles and assignments
2. **Setup Communication**: Initialize .agor coordination files
3. **Define Standards**: Establish coding standards and quality gates
4. **Plan First Sprint**: Break down initial tasks and assign owners
5. **Begin Development**: Start with team coordination and first tasks
"""

    # Combine template with implementation
    full_team_plan = template + implementation_details

    # Save to team structure file
    team_file = Path(".agor") / "team-structure.md"
    team_file.parent.mkdir(exist_ok=True)
    team_file.write_text(full_team_plan)

    # Create team coordination file
    _create_team_coordination_file(team_size, project_type)

    # Create individual agent memory templates
    _create_agent_memory_templates(team_size)

    return f"""✅ Team Structure Created

**Project**: {project_description}
**Team Size**: {team_size} agents
**Project Type**: {project_type}
**Complexity**: {complexity}

**Team Structure**:
{_get_team_summary(team_size, project_type, complexity)}

**Files Created**:
- `.agor/team-structure.md` - Complete team plan and roles
- `.agor/team-coordination.md` - Coordination protocols
- `.agor/agent[1-{team_size}]-memory.md` - Individual agent memory files

**Next Steps**:
1. Review team structure and role assignments
2. Initialize development environment and standards
3. Plan first sprint and assign initial tasks
4. Begin team coordination with daily standups

**Ready for team development to begin!**
"""


def _generate_team_structure(team_size: int, project_type: str, complexity: str) -> str:
    """Generate recommended team structure based on parameters."""

    if team_size <= 3:
        return _generate_small_team_structure(team_size, project_type)
    elif team_size <= 6:
        return _generate_medium_team_structure(team_size, project_type)
    else:
        return _generate_large_team_structure(team_size, project_type)


def _generate_small_team_structure(team_size: int, project_type: str) -> str:
    """Generate small team structure (2-3 agents)."""
    if team_size == 2:
        return """
### Small Team Structure (2 Agents)
- **Agent1**: Full-Stack Developer + Technical Lead
  - Frontend and backend development
  - Architecture decisions and technical direction
  - Code review and quality assurance

- **Agent2**: Quality Engineer + DevOps
  - Testing, validation, and quality control
  - Deployment, CI/CD, and infrastructure
  - Documentation and user acceptance
"""
    else:  # team_size == 3
        return """
### Small Team Structure (3 Agents)
- **Agent1**: Full-Stack Developer + Technical Lead
  - Primary development (frontend and backend)
  - Architecture decisions and technical direction
  - Code review and mentoring

- **Agent2**: Quality Assurance + Testing
  - Test planning, execution, and automation
  - Quality control and validation
  - Bug tracking and resolution coordination

- **Agent3**: DevOps + Support
  - Deployment, CI/CD, and infrastructure
  - Performance monitoring and optimization
  - Documentation and maintenance
"""


def _generate_medium_team_structure(team_size: int, project_type: str) -> str:
    """Generate medium team structure (4-6 agents)."""
    base_structure = f"""
### Medium Team Structure ({team_size} Agents)
- **Agent1**: Technical Lead + Architect
  - Technical direction and architecture decisions
  - Code review and quality oversight
  - Team coordination and mentoring

- **Agent2**: Frontend Developer
  - User interface development
  - Client-side logic and user experience
  - Frontend testing and optimization

- **Agent3**: Backend Developer
  - Server-side logic and API development
  - Database design and data processing
  - Backend testing and performance

- **Agent4**: DevOps Engineer
  - CI/CD pipeline and deployment
  - Infrastructure and monitoring
  - Security and performance optimization
"""

    if team_size >= 5:
        base_structure += """
- **Agent5**: Quality Assurance Engineer
  - Test planning and execution
  - Quality control and validation
  - Bug tracking and resolution
"""

    if team_size >= 6:
        if project_type in ["mobile", "data", "security"]:
            base_structure += f"""
- **Agent6**: {project_type.title()} Specialist
  - Domain-specific expertise
  - Specialized implementation
  - Technical consultation
"""
        else:
            base_structure += """
- **Agent6**: Integration Specialist
  - System integration and testing
  - Third-party service integration
  - End-to-end workflow validation
"""

    return base_structure


def _generate_large_team_structure(team_size: int, project_type: str) -> str:
    """Generate large team structure (7+ agents)."""
    return f"""
### Large Team Structure ({team_size} Agents)

#### Leadership Team
- **Agent1**: Technical Lead
  - Overall technical direction and architecture
  - Team coordination and decision making
  - Stakeholder communication

- **Agent2**: Project Coordinator
  - Timeline and resource management
  - Process coordination and optimization
  - Risk management and mitigation

#### Development Teams
- **Agent3**: Frontend Lead
  - Frontend architecture and standards
  - UI/UX implementation
  - Frontend team coordination

- **Agent4**: Backend Lead
  - Backend architecture and API design
  - Database design and optimization
  - Backend team coordination

- **Agent5**: DevOps Engineer
  - CI/CD and deployment automation
  - Infrastructure and monitoring
  - Security and compliance

- **Agent6**: Quality Assurance Lead
  - Test strategy and planning
  - Quality metrics and reporting
  - QA team coordination

{_generate_additional_large_team_roles(team_size, project_type)}
"""


def _generate_additional_large_team_roles(team_size: int, project_type: str) -> str:
    """Generate additional roles for large teams."""
    additional_roles = []

    if team_size >= 7:
        if project_type == "security":
            additional_roles.append("""
- **Agent7**: Security Engineer
  - Security architecture and review
  - Vulnerability assessment
  - Compliance and audit""")
        elif project_type == "data":
            additional_roles.append("""
- **Agent7**: Data Engineer
  - Data pipeline and processing
  - Analytics and reporting
  - Data quality and governance""")
        else:
            additional_roles.append("""
- **Agent7**: Performance Engineer
  - Performance testing and optimization
  - Scalability analysis
  - Monitoring and alerting""")

    if team_size >= 8:
        additional_roles.append("""
- **Agent8**: Integration Specialist
  - System integration and testing
  - Third-party service integration
  - End-to-end workflow validation""")

    return "\n".join(additional_roles)


def _generate_role_responsibilities(team_size: int, project_type: str, complexity: str) -> str:
    """Generate detailed role responsibilities."""
    return f"""
### Detailed Role Responsibilities

#### Technical Lead (Agent1)
- **Architecture**: Make high-level technical decisions
- **Code Review**: Review critical code changes and architectural decisions
- **Mentoring**: Guide junior developers and share knowledge
- **Coordination**: Facilitate technical discussions and resolve conflicts
- **Quality**: Ensure code quality standards and best practices

#### Development Team
- **Implementation**: Write clean, maintainable, and tested code
- **Collaboration**: Participate in code reviews and knowledge sharing
- **Documentation**: Document code, APIs, and technical decisions
- **Testing**: Write unit tests and participate in integration testing
- **Communication**: Regular updates on progress and blockers

#### Quality Assurance
- **Test Planning**: Create comprehensive test plans and strategies
- **Test Execution**: Execute manual and automated tests
- **Bug Tracking**: Identify, document, and track defects
- **Quality Metrics**: Monitor and report on quality metrics
- **Process Improvement**: Suggest improvements to development processes

#### DevOps Engineer
- **Infrastructure**: Manage development, staging, and production environments
- **Deployment**: Automate deployment processes and ensure reliability
- **Monitoring**: Set up monitoring, logging, and alerting systems
- **Security**: Implement security best practices and compliance
- **Performance**: Monitor and optimize system performance
"""


def _create_team_coordination_file(team_size: int, project_type: str):
    """Create team coordination file."""
    coord_file = Path(".agor") / "team-coordination.md"
    coord_content = f"""
# Team Coordination Protocols

## Team Configuration
- **Team Size**: {team_size} agents
- **Project Type**: {project_type}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Communication Protocols

### Daily Standup Format
```
[AGENT-ID] [TIMESTAMP] - STANDUP:
Yesterday: [what was accomplished]
Today: [planned work]
Blockers: [any impediments]
```

### Progress Update Format
```
[AGENT-ID] [TIMESTAMP] - PROGRESS: [task-name] - [percentage]% - [next-steps]
```

### Handoff Request Format
```
[FROM-AGENT] [TIMESTAMP] - HANDOFF_REQUEST: [to-agent] - [task] - [deliverables]
[TO-AGENT] [TIMESTAMP] - HANDOFF_ACCEPTED: [task] - [estimated-completion]
```

### Blocker Resolution Format
```
[AGENT-ID] [TIMESTAMP] - BLOCKER: [description] - [help-needed]
[HELPER-ID] [TIMESTAMP] - BLOCKER_ASSIST: [solution/guidance]
```

## Team Metrics

### Daily Tracking
- [ ] All agents posted standup updates
- [ ] Progress updates provided for active tasks
- [ ] Blockers identified and assistance requested
- [ ] Handoffs completed successfully

### Weekly Review
- [ ] Sprint goals achieved
- [ ] Quality metrics reviewed
- [ ] Team velocity calculated
- [ ] Process improvements identified

## Escalation Procedures

### Technical Issues
1. **Agent Level**: Try to resolve independently
2. **Peer Level**: Ask team members for assistance
3. **Lead Level**: Escalate to Technical Lead
4. **External Level**: Seek external consultation

### Process Issues
1. **Team Discussion**: Raise in daily standup
2. **Lead Review**: Discuss with Technical Lead
3. **Process Change**: Implement agreed improvements
4. **Documentation**: Update coordination protocols

## Success Criteria

### Team Performance
- **Communication**: Regular, clear, and helpful
- **Collaboration**: Effective knowledge sharing and assistance
- **Quality**: High code quality and low defect rates
- **Delivery**: Consistent progress toward goals

### Individual Performance
- **Productivity**: Consistent task completion
- **Quality**: Code meets standards and requirements
- **Collaboration**: Active participation in team activities
- **Growth**: Continuous learning and improvement
"""
    coord_file.write_text(coord_content)


def _create_agent_memory_templates(team_size: int):
    """Create individual agent memory file templates."""
    for i in range(1, team_size + 1):
        memory_file = Path(".agor") / f"agent{i}-memory.md"
        memory_content = f"""
# Agent{i} Memory Log

## Current Role
[Your assigned role and responsibilities]

## Current Tasks
- [ ] [Task 1 description]
- [ ] [Task 2 description]
- [ ] [Task 3 description]

## Decisions Made
- [Key architectural or implementation decisions]

## Files Modified
- [List of files changed with brief descriptions]

## Problems Encountered
- [Issues faced and how they were resolved]

## Knowledge Gained
- [New things learned during development]

## Team Interactions
- [Important communications with other team members]

## Next Steps
- [What needs to be done next]

## Notes for Handoffs
- [Important information for future handoffs]

## Status
Current: [current status]
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        memory_file.write_text(memory_content)


def _get_team_summary(team_size: int, project_type: str, complexity: str) -> str:
    """Get a brief team summary."""
    if team_size <= 3:
        return f"Small team ({team_size} agents) - Full-stack + QA + DevOps"
    elif team_size <= 6:
        return f"Medium team ({team_size} agents) - Specialized roles with lead"
    else:
        return f"Large team ({team_size} agents) - Multiple specialized teams with leadership"


def design_workflow(project_description: str, team_size: int = 4, project_type: str = "web_app", complexity: str = "medium") -> str:
    """Design agent workflow and coordination patterns (wf hotkey)."""

    # Import the workflow template
    from .project_planning_templates import generate_workflow_template

    # Get the base template
    template = generate_workflow_template()

    # Add concrete workflow implementation
    implementation_details = f"""
## CONCRETE WORKFLOW IMPLEMENTATION

### Project: {project_description}
### Team Size: {team_size} agents
### Project Type: {project_type}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## WORKFLOW DESIGN

{_generate_workflow_phases(project_type, complexity, team_size)}

## AGENT WORKFLOW ASSIGNMENTS

{_generate_workflow_assignments(team_size, project_type)}

## COORDINATION PROTOCOLS

### Phase Transition Rules:
```
PHASE_COMPLETE: [agent-id] - [phase-name] - [deliverables] - [timestamp]
PHASE_READY: [next-agent] - [phase-name] - [prerequisites-met] - [timestamp]
PHASE_BLOCKED: [agent-id] - [phase-name] - [blocker-description] - [timestamp]
```

### Quality Gates:
{_generate_workflow_quality_gates(complexity)}

### Handoff Procedures:
{_generate_workflow_handoffs(project_type)}

## WORKFLOW EXECUTION

### Parallel Tracks:
{_generate_parallel_tracks(team_size, project_type)}

### Dependencies:
{_generate_workflow_dependencies(project_type, complexity)}

### Timeline:
{_generate_workflow_timeline(complexity, team_size)}

## ERROR HANDLING & RECOVERY

### Common Workflow Issues:
1. **Phase Blocking**: When one phase cannot proceed
   - **Detection**: Missing prerequisites, failed quality gates
   - **Resolution**: Rollback to previous phase, fix issues, retry
   - **Prevention**: Clear phase completion criteria

2. **Integration Conflicts**: When parallel work doesn't merge cleanly
   - **Detection**: Merge conflicts, API mismatches, test failures
   - **Resolution**: Integration agent coordinates resolution
   - **Prevention**: Regular integration checkpoints

3. **Resource Bottlenecks**: When agents are waiting for others
   - **Detection**: Idle agents, delayed phase transitions
   - **Resolution**: Rebalance work, add parallel tasks
   - **Prevention**: Load balancing, buffer tasks

4. **Quality Failures**: When deliverables don't meet standards
   - **Detection**: Failed quality gates, review rejections
   - **Resolution**: Return to development phase, address issues
   - **Prevention**: Continuous quality checks

### Recovery Procedures:
```
WORKFLOW_ISSUE: [agent-id] - [issue-type] - [description] - [timestamp]
RECOVERY_PLAN: [coordinator] - [steps] - [timeline] - [timestamp]
RECOVERY_COMPLETE: [agent-id] - [resolution] - [lessons-learned] - [timestamp]
```

## WORKFLOW MONITORING

### Progress Tracking:
- **Phase Completion**: Percentage complete for each phase
- **Agent Utilization**: Active vs idle time for each agent
- **Quality Metrics**: Defect rates, rework percentage
- **Timeline Adherence**: Actual vs planned phase durations

### Performance Indicators:
- **Velocity**: Features completed per sprint
- **Quality**: Bug rates, review feedback scores
- **Efficiency**: Rework percentage, idle time
- **Collaboration**: Handoff success rate, communication frequency

## WORKFLOW OPTIMIZATION

### Continuous Improvement:
1. **Weekly Retrospectives**: What worked, what didn't, improvements
2. **Metrics Review**: Analyze performance indicators, identify bottlenecks
3. **Process Refinement**: Adjust phases, handoffs, quality gates
4. **Tool Enhancement**: Improve coordination tools and templates

### Adaptation Triggers:
- **Performance Degradation**: Velocity drops, quality issues increase
- **Team Changes**: New agents, role changes, skill gaps
- **Project Evolution**: Scope changes, new requirements, technology shifts
- **External Factors**: Timeline pressure, resource constraints

## WORKFLOW INITIALIZATION CHECKLIST

- [ ] **Workflow Design Approved**: All agents understand the process
- [ ] **Phase Definitions Clear**: Entry/exit criteria defined
- [ ] **Quality Gates Established**: Standards and review processes
- [ ] **Handoff Procedures Documented**: Clear transition protocols
- [ ] **Monitoring Setup**: Progress tracking and metrics collection
- [ ] **Error Handling Defined**: Recovery procedures and escalation
- [ ] **Communication Protocols**: Regular updates and coordination
- [ ] **Tool Integration**: .agor files and coordination systems

## NEXT STEPS

1. **Review Workflow Design**: Validate phases and assignments with team
2. **Setup Coordination**: Initialize .agor workflow tracking files
3. **Define Standards**: Establish quality gates and handoff criteria
4. **Begin Execution**: Start with first phase and monitor progress
5. **Iterate and Improve**: Regular retrospectives and optimization
"""

    # Combine template with implementation
    full_workflow = template + implementation_details

    # Save to workflow design file
    workflow_file = Path(".agor") / "workflow-design.md"
    workflow_file.parent.mkdir(exist_ok=True)
    workflow_file.write_text(full_workflow)

    # Create workflow tracking file
    _create_workflow_tracking_file(team_size, project_type)

    # Create phase coordination files
    _create_phase_coordination_files(project_type, complexity)

    return f"""✅ Workflow Design Created

**Project**: {project_description}
**Team Size**: {team_size} agents
**Project Type**: {project_type}
**Complexity**: {complexity}

**Workflow Structure**:
{_get_workflow_summary(project_type, complexity, team_size)}

**Files Created**:
- `.agor/workflow-design.md` - Complete workflow plan and coordination
- `.agor/workflow-tracking.md` - Progress tracking and metrics
- `.agor/phase-[name].md` - Individual phase coordination files

**Next Steps**:
1. Review workflow design with team
2. Initialize phase coordination and tracking
3. Begin execution with first phase
4. Monitor progress and optimize workflow

**Ready for coordinated workflow execution!**
"""


def _generate_workflow_phases(project_type: str, complexity: str, team_size: int) -> str:
    """Generate workflow phases based on project characteristics."""

    if project_type == "api":
        return _generate_api_workflow_phases(complexity)
    elif project_type == "web_app":
        return _generate_webapp_workflow_phases(complexity)
    elif project_type == "mobile":
        return _generate_mobile_workflow_phases(complexity)
    elif project_type == "data":
        return _generate_data_workflow_phases(complexity)
    else:
        return _generate_generic_workflow_phases(complexity)


def _generate_api_workflow_phases(complexity: str) -> str:
    """Generate API-specific workflow phases."""
    base_phases = """
### API Development Workflow

#### Phase 1: API Design (Sequential)
- **API Specification**: Define endpoints, schemas, error handling
- **Data Modeling**: Design database schema and relationships
- **Security Planning**: Authentication, authorization, rate limiting
- **Documentation**: API documentation and examples

#### Phase 2: Core Implementation (Parallel)
- **Backend Development**: API endpoints and business logic
- **Database Implementation**: Schema creation and data access layer
- **Authentication System**: User management and security
- **Testing Framework**: Unit tests and API testing

#### Phase 3: Integration & Testing (Sequential)
- **API Integration**: Connect all components
- **End-to-End Testing**: Full API workflow testing
- **Performance Testing**: Load testing and optimization
- **Security Testing**: Vulnerability assessment

#### Phase 4: Deployment (Sequential)
- **Environment Setup**: Production infrastructure
- **Deployment Pipeline**: CI/CD and automation
- **Monitoring**: Logging, metrics, and alerting
- **Documentation**: Deployment and maintenance guides
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Advanced Features (Parallel)
- **Caching Layer**: Redis/Memcached implementation
- **API Gateway**: Rate limiting, routing, analytics
- **Microservices**: Service decomposition and communication
- **Advanced Security**: OAuth, JWT, encryption
"""

    return base_phases


def _generate_webapp_workflow_phases(complexity: str) -> str:
    """Generate web application workflow phases."""
    base_phases = """
### Web Application Workflow

#### Phase 1: Foundation (Sequential)
- **Architecture Design**: Frontend/backend architecture
- **UI/UX Design**: Wireframes, mockups, design system
- **Database Design**: Schema and data relationships
- **Development Environment**: Setup and configuration

#### Phase 2: Core Development (Parallel)
- **Frontend Development**: UI components and user interface
- **Backend Development**: API and business logic
- **Database Implementation**: Data layer and migrations
- **Authentication**: User management and security

#### Phase 3: Integration (Sequential)
- **Frontend-Backend Integration**: API connections
- **Database Integration**: Data flow and persistence
- **User Experience**: Navigation and interaction flows
- **Testing**: Integration and user acceptance testing

#### Phase 4: Quality & Deployment (Parallel)
- **Quality Assurance**: Testing and bug fixes
- **Performance Optimization**: Speed and scalability
- **Deployment Setup**: Production environment
- **Documentation**: User guides and technical docs
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Advanced Features (Parallel)
- **Real-time Features**: WebSockets, notifications
- **Advanced UI**: Animations, responsive design
- **Analytics**: User tracking and reporting
- **SEO & Accessibility**: Search optimization and compliance
"""

    return base_phases


def _generate_mobile_workflow_phases(complexity: str) -> str:
    """Generate mobile application workflow phases."""
    return """
### Mobile Application Workflow

#### Phase 1: Design & Planning (Sequential)
- **UX Design**: User flows and wireframes
- **UI Design**: Visual design and components
- **Architecture**: App structure and data flow
- **Platform Strategy**: iOS, Android, or cross-platform

#### Phase 2: Core Development (Parallel)
- **UI Implementation**: Screens and components
- **Business Logic**: App functionality and features
- **Data Layer**: Local storage and API integration
- **Navigation**: Screen transitions and routing

#### Phase 3: Platform Integration (Parallel)
- **Platform Features**: Camera, GPS, notifications
- **Performance**: Memory management and optimization
- **Testing**: Device testing and compatibility
- **App Store Preparation**: Metadata and assets

#### Phase 4: Release (Sequential)
- **Final Testing**: QA and user acceptance
- **App Store Submission**: Review and approval
- **Launch Preparation**: Marketing and support
- **Post-Launch**: Monitoring and updates
"""


def _generate_data_workflow_phases(complexity: str) -> str:
    """Generate data project workflow phases."""
    return """
### Data Project Workflow

#### Phase 1: Data Discovery (Sequential)
- **Data Assessment**: Available data sources and quality
- **Requirements Analysis**: Business needs and objectives
- **Architecture Design**: Data pipeline and storage
- **Tool Selection**: Technologies and frameworks

#### Phase 2: Data Pipeline (Sequential)
- **Data Ingestion**: Collection and import processes
- **Data Cleaning**: Quality checks and transformation
- **Data Storage**: Database design and optimization
- **Data Validation**: Quality assurance and testing

#### Phase 3: Analysis & Modeling (Parallel)
- **Exploratory Analysis**: Data exploration and insights
- **Model Development**: Machine learning or analytics
- **Visualization**: Dashboards and reporting
- **Performance Tuning**: Optimization and scaling

#### Phase 4: Deployment (Sequential)
- **Production Pipeline**: Automated data processing
- **Monitoring**: Data quality and system health
- **Documentation**: Process and maintenance guides
- **Training**: User education and support
"""


def _generate_generic_workflow_phases(complexity: str) -> str:
    """Generate generic workflow phases."""
    base_phases = """
### Generic Development Workflow

#### Phase 1: Analysis & Design (Sequential)
- **Requirements Analysis**: Gather and document needs
- **System Design**: Architecture and component design
- **Technical Planning**: Technology choices and approach
- **Project Setup**: Environment and tool configuration

#### Phase 2: Implementation (Parallel)
- **Core Development**: Primary functionality
- **Component Development**: Individual modules
- **Integration Development**: Component connections
- **Testing Development**: Test suites and validation

#### Phase 3: Integration & Testing (Sequential)
- **System Integration**: Combine all components
- **Quality Assurance**: Testing and validation
- **Performance Testing**: Load and stress testing
- **User Acceptance**: Stakeholder validation

#### Phase 4: Deployment & Support (Sequential)
- **Deployment Preparation**: Production setup
- **Go-Live**: System launch and monitoring
- **Documentation**: User and technical guides
- **Support Setup**: Maintenance and help systems
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Optimization (Parallel)
- **Performance Optimization**: Speed and efficiency
- **Security Hardening**: Vulnerability mitigation
- **Feature Enhancement**: Additional capabilities
- **Process Improvement**: Workflow optimization
"""

    return base_phases


def _generate_workflow_assignments(team_size: int, project_type: str) -> str:
    """Generate workflow assignments for agents."""
    if team_size <= 3:
        return """
### Small Team Workflow Assignments
- **Agent1**: Lead Developer - Handles design, core development, and coordination
- **Agent2**: Quality Engineer - Testing, integration, and quality assurance
- **Agent3**: DevOps Specialist - Deployment, monitoring, and infrastructure
"""
    elif team_size <= 6:
        return """
### Medium Team Workflow Assignments
- **Agent1**: Technical Lead - Architecture, coordination, and code review
- **Agent2**: Frontend Developer - UI/UX implementation and client-side logic
- **Agent3**: Backend Developer - API development and business logic
- **Agent4**: Quality Assurance - Testing, validation, and quality control
- **Agent5**: DevOps Engineer - Deployment, infrastructure, and monitoring
- **Agent6**: Integration Specialist - Component integration and system testing
"""
    else:
        return """
### Large Team Workflow Assignments
- **Agent1**: Project Coordinator - Overall workflow management and coordination
- **Agent2**: Technical Architect - System design and technical direction
- **Agent3**: Frontend Lead - UI/UX team coordination and implementation
- **Agent4**: Backend Lead - API and business logic team coordination
- **Agent5**: Quality Lead - Testing strategy and quality assurance
- **Agent6**: DevOps Lead - Infrastructure and deployment coordination
- **Agent7+**: Specialized Developers - Domain-specific implementation
"""


def _generate_workflow_quality_gates(complexity: str) -> str:
    """Generate quality gates for workflow phases."""
    base_gates = """
#### Phase 1 Quality Gates:
- [ ] Requirements documented and approved
- [ ] Architecture design reviewed and signed off
- [ ] Technical approach validated
- [ ] Development environment ready

#### Phase 2 Quality Gates:
- [ ] Code review completed for all components
- [ ] Unit tests passing with >80% coverage
- [ ] Security review completed
- [ ] Performance benchmarks met

#### Phase 3 Quality Gates:
- [ ] Integration tests passing
- [ ] End-to-end workflows validated
- [ ] Performance testing completed
- [ ] Security testing passed

#### Phase 4 Quality Gates:
- [ ] Production deployment successful
- [ ] Monitoring and alerting active
- [ ] Documentation complete and reviewed
- [ ] User acceptance criteria met
"""

    if complexity == "complex":
        base_gates += """

#### Phase 5 Quality Gates:
- [ ] Advanced features tested and validated
- [ ] Scalability requirements met
- [ ] Security hardening completed
- [ ] Performance optimization verified
"""

    return base_gates


def _generate_workflow_handoffs(project_type: str) -> str:
    """Generate handoff procedures for workflow."""
    return f"""
#### Standard Handoff Procedure:
1. **Completion Signal**: Agent signals phase completion with deliverables
2. **Quality Check**: Next agent validates prerequisites and quality gates
3. **Knowledge Transfer**: Brief handoff meeting or documentation review
4. **Acceptance**: Receiving agent confirms readiness to proceed

#### Handoff Documentation Template:
```
HANDOFF: [from-agent] → [to-agent] - [phase-name]
COMPLETED:
- [Deliverable 1 with location]
- [Deliverable 2 with location]
- [Quality gates passed]

NEXT PHASE:
- [Task 1 for receiving agent]
- [Task 2 for receiving agent]
- [Prerequisites and dependencies]

NOTES:
- [Important context or decisions]
- [Known issues or considerations]
- [Recommendations for next phase]
```

#### Emergency Handoff Procedure:
- **Immediate**: Critical blocker requires different expertise
- **Planned**: Scheduled agent rotation or availability change
- **Quality**: Phase fails quality gates, needs rework
"""


def _generate_parallel_tracks(team_size: int, project_type: str) -> str:
    """Generate parallel execution tracks."""
    if project_type == "web_app":
        return """
#### Parallel Development Tracks:

**Track A: Frontend Development**
- UI component development
- User experience implementation
- Client-side testing
- Frontend optimization

**Track B: Backend Development**
- API endpoint development
- Business logic implementation
- Database integration
- Backend testing

**Track C: Infrastructure & Quality**
- Development environment setup
- CI/CD pipeline configuration
- Testing framework setup
- Deployment preparation

**Synchronization Points:**
- Daily: Progress updates and blocker resolution
- Weekly: Integration testing and alignment
- Phase End: Complete integration and handoff
"""
    else:
        return """
#### Parallel Development Tracks:

**Track A: Core Development**
- Primary functionality implementation
- Core business logic
- Main feature development

**Track B: Supporting Systems**
- Infrastructure and tooling
- Testing and validation
- Documentation and guides

**Track C: Quality & Integration**
- Quality assurance
- System integration
- Performance optimization

**Synchronization Points:**
- Regular integration checkpoints
- Quality gate validations
- Phase completion reviews
"""


def _generate_workflow_dependencies(project_type: str, complexity: str) -> str:
    """Generate workflow dependencies."""
    return """
#### Critical Dependencies:

**Phase Dependencies:**
- Phase 1 → Phase 2: Architecture approval required
- Phase 2 → Phase 3: Core components completed
- Phase 3 → Phase 4: Integration testing passed
- Phase 4 → Launch: Quality gates satisfied

**Resource Dependencies:**
- Development Environment: Required for all development phases
- Test Environment: Required for integration and testing phases
- Production Environment: Required for deployment phase
- External APIs: May block integration if unavailable

**Knowledge Dependencies:**
- Domain Expertise: Required for business logic implementation
- Technical Skills: Specific technology knowledge needed
- Process Knowledge: Understanding of workflow and quality standards

**Dependency Management:**
- **Early Identification**: Map dependencies during planning
- **Risk Mitigation**: Prepare alternatives for critical dependencies
- **Regular Review**: Monitor dependency status and adjust plans
- **Communication**: Keep team informed of dependency changes
"""


def _generate_workflow_timeline(complexity: str, team_size: int) -> str:
    """Generate workflow timeline estimates."""
    if complexity == "simple":
        return """
#### Simple Project Timeline:
- **Phase 1**: 2-3 days (Analysis & Design)
- **Phase 2**: 5-7 days (Implementation)
- **Phase 3**: 2-3 days (Integration & Testing)
- **Phase 4**: 1-2 days (Deployment)

**Total Duration**: 10-15 days
**Team Utilization**: High (minimal idle time)
**Risk Buffer**: 20% additional time for unexpected issues
"""
    elif complexity == "complex":
        return """
#### Complex Project Timeline:
- **Phase 1**: 1-2 weeks (Analysis & Design)
- **Phase 2**: 3-4 weeks (Implementation)
- **Phase 3**: 1-2 weeks (Integration & Testing)
- **Phase 4**: 1 week (Deployment)
- **Phase 5**: 1-2 weeks (Advanced Features)

**Total Duration**: 7-11 weeks
**Team Utilization**: Medium (coordination overhead)
**Risk Buffer**: 30% additional time for complexity management
"""
    else:  # medium
        return """
#### Medium Project Timeline:
- **Phase 1**: 3-5 days (Analysis & Design)
- **Phase 2**: 2-3 weeks (Implementation)
- **Phase 3**: 1 week (Integration & Testing)
- **Phase 4**: 2-3 days (Deployment)

**Total Duration**: 4-6 weeks
**Team Utilization**: High (good balance)
**Risk Buffer**: 25% additional time for coordination
"""


def _create_workflow_tracking_file(team_size: int, project_type: str):
    """Create workflow tracking file."""
    tracking_file = Path(".agor") / "workflow-tracking.md"
    tracking_content = f"""
# Workflow Progress Tracking

## Project Configuration
- **Team Size**: {team_size} agents
- **Project Type**: {project_type}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Phase Progress

### Phase 1: Analysis & Design
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 2: Implementation
- **Status**: Not Started
- **Assigned**: [agent-ids]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 3: Integration & Testing
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 4: Deployment
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

## Metrics Tracking

### Daily Metrics
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Active Agents**: 0/{team_size}
- **Completed Tasks**: 0
- **Blockers**: 0
- **Quality Issues**: 0

### Weekly Summary
- **Week**: [week-number]
- **Velocity**: [tasks completed]
- **Quality Score**: [percentage]
- **Team Utilization**: [percentage]
- **Timeline Adherence**: [on-track/delayed/ahead]

## Issue Tracking

### Active Issues
- [No issues currently]

### Resolved Issues
- [No issues resolved yet]

## Workflow Adjustments

### Process Changes
- [No changes made yet]

### Lessons Learned
- [Lessons will be captured here]
"""
    tracking_file.write_text(tracking_content)


def _create_phase_coordination_files(project_type: str, complexity: str):
    """Create individual phase coordination files."""
    phases = ["analysis-design", "implementation", "integration-testing", "deployment"]
    if complexity == "complex":
        phases.append("optimization")

    for phase in phases:
        phase_file = Path(".agor") / f"phase-{phase}.md"
        phase_content = f"""
# Phase: {phase.replace('-', ' ').title()}

## Phase Overview
[Description of this phase and its objectives]

## Assigned Agents
- [List of agents working on this phase]

## Tasks
- [ ] [Task 1 description]
- [ ] [Task 2 description]
- [ ] [Task 3 description]

## Quality Gates
- [ ] [Quality requirement 1]
- [ ] [Quality requirement 2]
- [ ] [Quality requirement 3]

## Deliverables
- [Deliverable 1 with location]
- [Deliverable 2 with location]

## Dependencies
- [Dependency 1 description]
- [Dependency 2 description]

## Progress Updates

### {datetime.now().strftime('%Y-%m-%d')}
- **Status**: Not Started
- **Progress**: 0%
- **Blockers**: None
- **Next Steps**: [What needs to be done next]

## Handoff Preparation

### Prerequisites for Next Phase
- [Requirement 1]
- [Requirement 2]

### Handoff Documentation
- [Will be completed when phase is done]

## Notes
- [Important notes and decisions for this phase]
"""
        phase_file.write_text(phase_content)


def _get_workflow_summary(project_type: str, complexity: str, team_size: int) -> str:
    """Get workflow summary."""
    phase_count = 4 if complexity != "complex" else 5
    return f"{phase_count} phases, {project_type} optimized, {team_size} agents coordinated"


def generate_handoff_prompts(handoff_type: str = "standard", from_role: str = "developer", to_role: str = "reviewer", context: str = "") -> str:
    """Generate handoff prompts and coordination templates (hp hotkey)."""

    # Import handoff templates
    from .agent_prompt_templates import generate_handoff_prompt, generate_specialist_prompt
    from .handoff_templates import generate_handoff_document, generate_receive_handoff_prompt

    # Generate comprehensive handoff guidance
    implementation_details = f"""
## HANDOFF PROMPTS IMPLEMENTATION

### Handoff Type: {handoff_type}
### From Role: {from_role}
### To Role: {to_role}
### Context: {context if context else "General development handoff"}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## HANDOFF PROMPT TEMPLATES

{_generate_handoff_prompt_templates(handoff_type, from_role, to_role)}

## ROLE-SPECIFIC PROMPTS

{_generate_role_specific_prompts(from_role, to_role, context)}

## HANDOFF COORDINATION PROTOCOLS

### Standard Handoff Process:
1. **Preparation Phase**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_PREP: [task] - Preparing handoff materials
   ```

2. **Handoff Creation**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_CREATED: [task] - Handoff document ready
   ```

3. **Handoff Delivery**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_REQUEST: [to-agent] - [task] - [handoff-location]
   ```

4. **Handoff Reception**:
   ```
   [TO-AGENT] [TIMESTAMP] - HANDOFF_RECEIVED: [task] - Reviewing materials
   ```

5. **Handoff Acceptance**:
   ```
   [TO-AGENT] [TIMESTAMP] - HANDOFF_ACCEPTED: [task] - Work resumed
   ```

### Emergency Handoff Process:
1. **Immediate Notification**:
   ```
   [FROM-AGENT] [TIMESTAMP] - EMERGENCY_HANDOFF: [critical-issue] - Immediate assistance needed
   ```

2. **Quick Context Transfer**:
   ```
   [FROM-AGENT] [TIMESTAMP] - CONTEXT: [current-state] - [blocker] - [urgency-level]
   ```

3. **Emergency Response**:
   ```
   [TO-AGENT] [TIMESTAMP] - EMERGENCY_RESPONSE: [task] - Taking over immediately
   ```

## HANDOFF QUALITY ASSURANCE

### Handoff Checklist:
- [ ] **Work Status**: Current progress clearly documented
- [ ] **Deliverables**: All completed work identified and accessible
- [ ] **Context**: Technical decisions and rationale explained
- [ ] **Next Steps**: Clear tasks for receiving agent
- [ ] **Dependencies**: External dependencies and blockers identified
- [ ] **Quality**: Code quality and testing status documented
- [ ] **Timeline**: Estimated completion time provided
- [ ] **Communication**: Handoff logged in agentconvo.md

### Handoff Validation:
- [ ] **Completeness**: All required information provided
- [ ] **Clarity**: Instructions are clear and actionable
- [ ] **Accessibility**: All referenced files and resources available
- [ ] **Context**: Sufficient background for receiving agent
- [ ] **Quality**: Work meets standards for handoff

## SPECIALIZED HANDOFF SCENARIOS

{_generate_specialized_handoff_scenarios()}

## HANDOFF TEMPLATES LIBRARY

{_generate_handoff_templates_library()}

## HANDOFF METRICS & OPTIMIZATION

### Success Metrics:
- **Handoff Time**: Time from request to acceptance
- **Context Transfer**: Receiving agent understanding score
- **Continuation Quality**: Work quality after handoff
- **Rework Rate**: Percentage of work requiring revision

### Optimization Strategies:
- **Template Standardization**: Use consistent handoff formats
- **Context Documentation**: Maintain detailed work logs
- **Regular Checkpoints**: Frequent progress updates
- **Knowledge Sharing**: Cross-training and documentation

## HANDOFF TROUBLESHOOTING

### Common Issues:
1. **Incomplete Context**: Missing technical details or decisions
   - **Solution**: Use comprehensive handoff templates
   - **Prevention**: Regular documentation during work

2. **Unclear Next Steps**: Receiving agent unsure how to proceed
   - **Solution**: Provide specific, actionable tasks
   - **Prevention**: Break down work into clear steps

3. **Missing Dependencies**: Required resources not available
   - **Solution**: Document all dependencies and provide access
   - **Prevention**: Dependency mapping during planning

4. **Quality Issues**: Work not ready for handoff
   - **Solution**: Complete quality checks before handoff
   - **Prevention**: Continuous quality assurance

### Escalation Procedures:
1. **Agent Level**: Direct communication between agents
2. **Team Level**: Involve technical lead or coordinator
3. **Project Level**: Escalate to project management
4. **Emergency Level**: Immediate intervention required

## HANDOFF AUTOMATION

### Automated Handoff Generation:
```python
# Generate handoff document
from agor.tools.handoff_templates import generate_handoff_document
handoff = generate_handoff_document(
    problem_description="User authentication system",
    work_completed=["API endpoints", "Database schema", "Unit tests"],
    commits_made=["feat: add auth endpoints", "fix: validation logic"],
    current_status="80% complete - needs frontend integration",
    next_steps=["Create login UI", "Implement session management"],
    files_modified=["src/auth/api.py", "src/models/user.py"],
    context_notes="Uses JWT tokens, 24hr expiry",
    agent_role="Backend Developer",
    handoff_reason="Frontend development needed"
)
```

### Automated Prompt Generation:
```python
# Generate role-specific prompts
from agor.tools.agent_prompt_templates import generate_handoff_prompt
prompt = generate_handoff_prompt(
    from_agent="backend-dev",
    to_agent="frontend-dev",
    work_completed="Authentication API complete",
    next_tasks="Build login interface",
    context="JWT-based auth with 24hr tokens"
)
```

## NEXT STEPS

1. **Review Handoff Templates**: Validate prompt templates and formats
2. **Setup Handoff Directory**: Initialize .agor/handoffs/ structure
3. **Train Team**: Ensure all agents understand handoff protocols
4. **Monitor Quality**: Track handoff success metrics
5. **Iterate and Improve**: Refine templates based on usage
"""

    # Save to handoff prompts file
    handoff_file = Path(".agor") / "handoff-prompts.md"
    handoff_file.parent.mkdir(exist_ok=True)
    handoff_file.write_text(implementation_details)

    # Create handoff templates directory
    _create_handoff_templates_directory()

    # Create role-specific prompt files
    _create_role_specific_prompt_files(from_role, to_role)

    return f"""✅ Handoff Prompts Generated

**Handoff Type**: {handoff_type}
**From Role**: {from_role}
**To Role**: {to_role}
**Context**: {context if context else "General development"}

**Generated Resources**:
- Comprehensive handoff prompt templates
- Role-specific coordination protocols
- Quality assurance checklists
- Specialized handoff scenarios
- Automation examples and scripts

**Files Created**:
- `.agor/handoff-prompts.md` - Complete handoff guidance
- `.agor/handoff-templates/` - Template library
- `.agor/role-prompts/` - Role-specific prompts

**Next Steps**:
1. Review handoff templates and customize as needed
2. Train team on handoff protocols
3. Begin using standardized handoff processes
4. Monitor handoff quality and optimize

**Ready for seamless agent handoffs!**
"""


def _generate_handoff_prompt_templates(handoff_type: str, from_role: str, to_role: str) -> str:
    """Generate handoff prompt templates."""
    if handoff_type == "emergency":
        return f"""
### Emergency Handoff Template
```
EMERGENCY HANDOFF: {from_role} → {to_role}

CRITICAL ISSUE: [Describe the urgent problem]
CURRENT STATE: [What's working/broken]
IMMEDIATE ACTION NEEDED: [What must be done now]
TIME CONSTRAINT: [Deadline or urgency level]

CONTEXT:
- [Key technical details]
- [Recent changes that may be related]
- [Resources and access needed]

EMERGENCY CONTACT: [How to reach original agent if needed]
```
"""
    elif handoff_type == "planned":
        return f"""
### Planned Handoff Template
```
PLANNED HANDOFF: {from_role} → {to_role}

SCHEDULED: [Date and time]
REASON: [Why handoff is happening]
PREPARATION TIME: [How long to prepare]

WORK COMPLETED:
- [Deliverable 1 with location]
- [Deliverable 2 with location]
- [Quality gates passed]

NEXT PHASE:
- [Task 1 for receiving agent]
- [Task 2 for receiving agent]
- [Success criteria]

TRANSITION PLAN:
- [Knowledge transfer sessions]
- [Documentation review]
- [Overlap period if needed]
```
"""
    else:  # standard
        return f"""
### Standard Handoff Template
```
HANDOFF: {from_role} → {to_role}

COMPLETED WORK:
- [List of deliverables with locations]
- [Quality checks performed]
- [Tests passing]

CURRENT STATUS:
- [Overall progress percentage]
- [What's working well]
- [Known issues or limitations]

NEXT STEPS:
- [Immediate tasks for receiving agent]
- [Medium-term objectives]
- [Success criteria]

CONTEXT:
- [Technical decisions made]
- [Architecture choices]
- [Important constraints or requirements]

RESOURCES:
- [Documentation links]
- [Code repositories]
- [Access credentials or permissions needed]
```
"""


def _generate_role_specific_prompts(from_role: str, to_role: str, context: str) -> str:
    """Generate role-specific handoff prompts."""
    role_prompts = {
        "developer": {
            "to_reviewer": """
### Developer → Reviewer Handoff
**Focus**: Code quality, standards compliance, security review

**Developer Deliverables**:
- Complete, tested code implementation
- Unit tests with >80% coverage
- Documentation for new features
- Self-review checklist completed

**Reviewer Tasks**:
- Code quality assessment
- Security vulnerability scan
- Performance impact analysis
- Standards compliance verification

**Handoff Criteria**:
- All tests passing
- Code follows team standards
- Documentation is complete
- No obvious security issues
""",
            "to_tester": """
### Developer → Tester Handoff
**Focus**: Functional testing, integration validation, user acceptance

**Developer Deliverables**:
- Working feature implementation
- Unit tests and test data
- Feature documentation
- Known limitations or edge cases

**Tester Tasks**:
- Functional testing execution
- Integration testing
- User acceptance validation
- Bug reporting and tracking

**Handoff Criteria**:
- Feature is functionally complete
- Basic testing completed
- Test environment ready
- Test data available
""",
            "to_devops": """
### Developer → DevOps Handoff
**Focus**: Deployment readiness, infrastructure requirements, monitoring

**Developer Deliverables**:
- Production-ready code
- Deployment configuration
- Infrastructure requirements
- Monitoring and logging setup

**DevOps Tasks**:
- Deployment pipeline setup
- Infrastructure provisioning
- Monitoring configuration
- Performance optimization

**Handoff Criteria**:
- Code is deployment-ready
- Configuration is documented
- Dependencies are specified
- Monitoring requirements defined
"""
        },
        "reviewer": {
            "to_developer": """
### Reviewer → Developer Handoff
**Focus**: Required fixes, improvements, optimization recommendations

**Reviewer Deliverables**:
- Detailed review report
- Prioritized fix list
- Security recommendations
- Performance suggestions

**Developer Tasks**:
- Address critical issues
- Implement security fixes
- Optimize performance
- Update documentation

**Handoff Criteria**:
- Review is complete
- Issues are prioritized
- Fix guidance is clear
- Timeline is realistic
"""
        },
        "tester": {
            "to_developer": """
### Tester → Developer Handoff
**Focus**: Bug fixes, test failures, quality improvements

**Tester Deliverables**:
- Test results and reports
- Bug reports with reproduction steps
- Test coverage analysis
- Quality metrics

**Developer Tasks**:
- Fix identified bugs
- Improve test coverage
- Address quality issues
- Update implementation

**Handoff Criteria**:
- Testing is complete
- Bugs are documented
- Reproduction steps provided
- Priority levels assigned
"""
        }
    }

    key = f"{from_role}_to_{to_role}"
    if from_role in role_prompts and f"to_{to_role}" in role_prompts[from_role]:
        return role_prompts[from_role][f"to_{to_role}"]
    else:
        return f"""
### {from_role.title()} → {to_role.title()} Handoff
**Focus**: Role transition and work continuation

**{from_role.title()} Deliverables**:
- Completed work with documentation
- Current status and progress
- Next steps and requirements
- Context and technical details

**{to_role.title()} Tasks**:
- Review handoff materials
- Continue work from current state
- Address any immediate issues
- Maintain quality standards

**Handoff Criteria**:
- Work is properly documented
- Context is clearly explained
- Next steps are actionable
- Quality standards maintained
"""


def _generate_specialized_handoff_scenarios() -> str:
    """Generate specialized handoff scenarios."""
    return """
### Cross-Functional Handoffs

#### Backend → Frontend
- **Focus**: API integration, data contracts, user experience
- **Key Items**: API documentation, data schemas, authentication flow
- **Success Criteria**: Frontend can consume APIs successfully

#### Frontend → Backend
- **Focus**: Data requirements, performance needs, user workflows
- **Key Items**: User stories, data models, performance requirements
- **Success Criteria**: Backend supports all frontend needs

#### Development → Operations
- **Focus**: Deployment readiness, monitoring, scalability
- **Key Items**: Deployment configs, monitoring setup, scaling requirements
- **Success Criteria**: System deploys and runs reliably

### Temporal Handoffs

#### End of Sprint
- **Focus**: Sprint completion, next sprint preparation
- **Key Items**: Sprint summary, backlog updates, lessons learned
- **Success Criteria**: Clean transition to next sprint

#### End of Phase
- **Focus**: Phase completion, next phase readiness
- **Key Items**: Phase deliverables, quality gates, next phase planning
- **Success Criteria**: Phase objectives met, next phase can begin

#### Project Completion
- **Focus**: Project closure, maintenance handoff
- **Key Items**: Final deliverables, documentation, support procedures
- **Success Criteria**: Project successfully closed, maintenance ready

### Emergency Handoffs

#### Critical Bug
- **Focus**: Immediate issue resolution
- **Key Items**: Bug description, impact assessment, immediate fixes
- **Success Criteria**: Critical issue resolved quickly

#### Agent Unavailability
- **Focus**: Work continuation without original agent
- **Key Items**: Current state, immediate tasks, contact information
- **Success Criteria**: Work continues without significant delay

#### Deadline Pressure
- **Focus**: Accelerated delivery, scope management
- **Key Items**: Priority tasks, scope decisions, resource needs
- **Success Criteria**: Deadline met with acceptable quality
"""


def _generate_handoff_templates_library() -> str:
    """Generate handoff templates library."""
    return """
### Quick Handoff Templates

#### Minimal Handoff
```
QUICK HANDOFF: [from] → [to]
TASK: [brief description]
STATUS: [current state]
NEXT: [immediate action needed]
FILES: [key files to check]
```

#### Bug Fix Handoff
```
BUG HANDOFF: [from] → [to]
BUG: [description and impact]
REPRODUCTION: [steps to reproduce]
INVESTIGATION: [what's been tried]
NEXT: [suggested approach]
```

#### Feature Handoff
```
FEATURE HANDOFF: [from] → [to]
FEATURE: [description and requirements]
PROGRESS: [what's implemented]
REMAINING: [what's left to do]
TESTS: [testing status]
```

#### Review Handoff
```
REVIEW HANDOFF: [from] → [to]
CODE: [location and scope]
CRITERIA: [review requirements]
TIMELINE: [review deadline]
CONTACT: [for questions]
```

### Comprehensive Templates

#### Full Project Handoff
- Complete project context
- All deliverables and documentation
- Team structure and responsibilities
- Timeline and milestones
- Risk assessment and mitigation
- Success criteria and metrics

#### Phase Transition Handoff
- Phase completion summary
- Quality gate validation
- Next phase preparation
- Resource allocation
- Dependency management
- Stakeholder communication
"""


def _create_handoff_templates_directory():
    """Create handoff templates directory structure."""
    templates_dir = Path(".agor") / "handoff-templates"
    templates_dir.mkdir(exist_ok=True)

    # Create template files
    templates = {
        "standard-handoff.md": """
# Standard Handoff Template

## Handoff Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID]
- **Date**: [Timestamp]
- **Type**: Standard

## Work Completed
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

## Current Status
**Progress**: [Percentage]%
**Quality**: [Status]
**Testing**: [Status]

## Next Steps
1. [Immediate task]
2. [Follow-up task]
3. [Future consideration]

## Context & Notes
[Important technical details, decisions, constraints]

## Resources
- [Documentation links]
- [Code repositories]
- [Access requirements]
""",
        "emergency-handoff.md": """
# Emergency Handoff Template

## Emergency Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID]
- **Date**: [Timestamp]
- **Urgency**: [Critical/High/Medium]

## Critical Issue
**Problem**: [Description]
**Impact**: [Business/technical impact]
**Deadline**: [When this must be resolved]

## Current State
**What's Working**: [Functional components]
**What's Broken**: [Failed components]
**Last Known Good**: [Previous working state]

## Immediate Actions
1. [First priority action]
2. [Second priority action]
3. [Fallback option]

## Emergency Contacts
- **Original Agent**: [Contact info]
- **Technical Lead**: [Contact info]
- **Escalation**: [Contact info]
""",
        "review-handoff.md": """
# Review Handoff Template

## Review Information
- **Reviewer**: [Agent Role/ID]
- **Developer**: [Agent Role/ID]
- **Date**: [Timestamp]
- **Scope**: [What's being reviewed]

## Review Criteria
- [ ] Code quality and standards
- [ ] Security considerations
- [ ] Performance impact
- [ ] Test coverage
- [ ] Documentation completeness

## Code Location
**Repository**: [Repo URL/path]
**Branch**: [Branch name]
**Files**: [List of files to review]
**Commits**: [Relevant commit hashes]

## Review Timeline
**Deadline**: [When review must be complete]
**Priority**: [High/Medium/Low]
**Complexity**: [Simple/Medium/Complex]

## Review Results
[To be filled by reviewer]

## Action Items
[To be filled by reviewer]
"""
    }

    for filename, content in templates.items():
        template_file = templates_dir / filename
        template_file.write_text(content)


def _create_role_specific_prompt_files(from_role: str, to_role: str):
    """Create role-specific prompt files."""
    prompts_dir = Path(".agor") / "role-prompts"
    prompts_dir.mkdir(exist_ok=True)

    # Create role-specific prompt file
    prompt_file = prompts_dir / f"{from_role}-to-{to_role}.md"
    prompt_content = f"""
# {from_role.title()} to {to_role.title()} Handoff Prompts

## Role Transition Context
**From Role**: {from_role}
**To Role**: {to_role}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Handoff Prompt
{_generate_role_specific_prompts(from_role, to_role, "")}

## Communication Templates

### Handoff Request
```
[{from_role.upper()}] [TIMESTAMP] - HANDOFF_REQUEST: {to_role} - [task-description] - [handoff-location]
```

### Handoff Acceptance
```
[{to_role.upper()}] [TIMESTAMP] - HANDOFF_ACCEPTED: [task-description] - Work resumed
```

### Progress Update
```
[{to_role.upper()}] [TIMESTAMP] - PROGRESS: [task-description] - [status] - [next-steps]
```

## Quality Checklist
- [ ] All deliverables documented
- [ ] Context clearly explained
- [ ] Next steps actionable
- [ ] Resources accessible
- [ ] Timeline realistic

## Success Criteria
- Receiving agent understands the work
- Work continues without significant delay
- Quality standards maintained
- Communication protocols followed
"""
    prompt_file.write_text(prompt_content)


def manage_team(project_name: str = "Current Project", team_size: int = 4, management_focus: str = "performance") -> str:
    """Manage ongoing team coordination and performance (tm hotkey)."""

    # Import the team management template
    from .project_planning_templates import generate_team_management_template

    # Get the base template
    template = generate_team_management_template()

    # Add concrete team management implementation
    implementation_details = f"""
## TEAM MANAGEMENT IMPLEMENTATION

### Project: {project_name}
### Team Size: {team_size} agents
### Management Focus: {management_focus}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## CURRENT TEAM STATUS

{_generate_current_team_status(team_size, project_name)}

## PERFORMANCE DASHBOARD

{_generate_performance_dashboard(team_size, management_focus)}

## TEAM COORDINATION PROTOCOLS

### Daily Management Routine:
1. **Morning Status Check** (9:00 AM):
   ```
   TEAM_STATUS: [timestamp] - Daily team status review
   - Active agents: [count]
   - Blocked tasks: [count]
   - Completed yesterday: [count]
   - Planned today: [count]
   ```

2. **Midday Progress Review** (1:00 PM):
   ```
   PROGRESS_CHECK: [timestamp] - Midday progress assessment
   - On track: [agent-list]
   - Behind schedule: [agent-list]
   - Blockers identified: [blocker-list]
   - Help needed: [help-requests]
   ```

3. **End of Day Summary** (5:00 PM):
   ```
   DAY_SUMMARY: [timestamp] - Daily completion summary
   - Completed tasks: [task-list]
   - Incomplete tasks: [task-list]
   - Tomorrow's priorities: [priority-list]
   - Team health: [assessment]
   ```

### Weekly Management Cycle:
- **Monday**: Sprint planning and goal setting
- **Wednesday**: Mid-week progress review and adjustments
- **Friday**: Sprint retrospective and improvement planning

## ISSUE MANAGEMENT SYSTEM

### Issue Classification:
{_generate_issue_classification()}

### Resolution Workflows:
{_generate_resolution_workflows()}

## PERFORMANCE OPTIMIZATION

### Team Efficiency Metrics:
{_generate_efficiency_metrics(team_size)}

### Improvement Strategies:
{_generate_improvement_strategies(management_focus)}

## COMMUNICATION MANAGEMENT

### Communication Channels Setup:
```
.agor/team-status.md - Real-time team status
.agor/team-metrics.md - Performance tracking
.agor/team-issues.md - Issue tracking and resolution
.agor/team-retrospective.md - Weekly improvement notes
.agor/agent-assignments.md - Current task assignments
```

### Communication Protocols:
{_generate_communication_protocols()}

## RESOURCE ALLOCATION

### Current Assignments:
{_generate_resource_allocation(team_size)}

### Capacity Management:
{_generate_capacity_management(team_size)}

## QUALITY MANAGEMENT

### Quality Gates:
- [ ] **Daily**: All agents provide status updates
- [ ] **Daily**: Blockers identified and escalated
- [ ] **Weekly**: Performance metrics reviewed
- [ ] **Weekly**: Process improvements identified
- [ ] **Monthly**: Team satisfaction assessed

### Quality Metrics:
{_generate_quality_metrics()}

## TEAM DEVELOPMENT

### Skill Development Tracking:
{_generate_skill_development_tracking(team_size)}

### Knowledge Sharing:
{_generate_knowledge_sharing_protocols()}

## RISK MANAGEMENT

### Active Risk Monitoring:
{_generate_risk_monitoring()}

### Contingency Planning:
{_generate_contingency_planning(team_size)}

## MANAGEMENT AUTOMATION

### Automated Status Collection:
```python
# Collect team status
from agor.tools.agent_coordination import get_team_status
status = get_team_status()
print(f"Active agents: {status['active_count']}/{team_size}")
print(f"Blocked tasks: {status['blocked_count']}")
print(f"Completion rate: {status['completion_rate']}%")
```

### Automated Metrics Tracking:
```python
# Track performance metrics
from agor.tools.strategy_protocols import collect_team_metrics
metrics = collect_team_metrics(team_size)
print(f"Team velocity: {metrics['velocity']} tasks/day")
print(f"Quality score: {metrics['quality_score']}/10")
print(f"Collaboration index: {metrics['collaboration_index']}/10")
```

## NEXT STEPS

1. **Initialize Team Management**: Set up coordination files and protocols
2. **Establish Baselines**: Collect initial performance metrics
3. **Begin Daily Routine**: Start daily status checks and progress reviews
4. **Monitor and Adjust**: Track metrics and optimize processes
5. **Continuous Improvement**: Regular retrospectives and process refinement
"""

    # Combine template with implementation
    full_management_plan = template + implementation_details

    # Save to team management file
    management_file = Path(".agor") / "team-management.md"
    management_file.parent.mkdir(exist_ok=True)
    management_file.write_text(full_management_plan)

    # Create team management coordination files
    _create_team_management_files(team_size, project_name)

    # Initialize team metrics tracking
    _initialize_team_metrics(team_size)

    return f"""✅ Team Management Initialized

**Project**: {project_name}
**Team Size**: {team_size} agents
**Management Focus**: {management_focus}

**Management Features**:
- Real-time team status tracking
- Performance metrics and dashboards
- Issue management and resolution workflows
- Communication protocols and automation
- Resource allocation and capacity planning
- Quality management and improvement processes

**Files Created**:
- `.agor/team-management.md` - Complete management plan and protocols
- `.agor/team-status.md` - Real-time team status tracking
- `.agor/team-metrics.md` - Performance metrics dashboard
- `.agor/team-issues.md` - Issue tracking and resolution
- `.agor/agent-assignments.md` - Current task assignments

**Next Steps**:
1. Review team management protocols
2. Begin daily status tracking routine
3. Establish performance baselines
4. Start weekly improvement cycles

**Ready for comprehensive team management!**
"""


def _generate_current_team_status(team_size: int, project_name: str) -> str:
    """Generate current team status overview."""
    return f"""
### Team Status Overview
- **Project**: {project_name}
- **Team Size**: {team_size} agents
- **Active Agents**: [To be updated with actual count]
- **Current Phase**: [To be updated with current development phase]
- **Overall Health**: [To be assessed - Green/Yellow/Red]

### Agent Status Summary
{chr(10).join([f"- **Agent{i}**: [Role] - [Current Task] - [Status: Active/Blocked/Idle]" for i in range(1, team_size + 1)])}

### Today's Priorities
- [Priority task 1 - assigned to Agent X]
- [Priority task 2 - assigned to Agent Y]
- [Priority task 3 - assigned to Agent Z]

### Current Blockers
- [No blockers currently identified]

### Recent Completions
- [Tasks completed in last 24 hours]
"""


def _generate_performance_dashboard(team_size: int, management_focus: str) -> str:
    """Generate performance dashboard based on focus area."""
    if management_focus == "velocity":
        return """
### Velocity-Focused Dashboard
- **Daily Task Completion**: [X tasks/day target vs actual]
- **Sprint Velocity**: [Story points completed per sprint]
- **Cycle Time**: [Average time from start to completion]
- **Throughput**: [Tasks completed per agent per day]
- **Bottleneck Analysis**: [Identification of process bottlenecks]
"""
    elif management_focus == "quality":
        return """
### Quality-Focused Dashboard
- **Code Review Score**: [Average review rating 1-10]
- **Bug Rate**: [Bugs per 100 lines of code]
- **Test Coverage**: [Percentage of code covered by tests]
- **Rework Rate**: [Percentage of work requiring revision]
- **Customer Satisfaction**: [Stakeholder feedback scores]
"""
    elif management_focus == "collaboration":
        return """
### Collaboration-Focused Dashboard
- **Communication Frequency**: [Messages per agent per day]
- **Help Request Response Time**: [Average time to respond to help requests]
- **Knowledge Sharing**: [Documentation contributions per agent]
- **Cross-Training**: [Skills shared across team members]
- **Team Satisfaction**: [Team morale and engagement scores]
"""
    else:  # performance (default)
        return """
### Performance Dashboard
- **Overall Productivity**: [Tasks completed vs planned]
- **Quality Metrics**: [Code review scores, bug rates]
- **Team Velocity**: [Consistent delivery speed]
- **Collaboration Index**: [Team communication and cooperation]
- **Individual Performance**: [Per-agent productivity and quality]
"""


def _generate_issue_classification() -> str:
    """Generate issue classification system."""
    return """
#### Issue Types and Priorities

**P0 - Critical (Resolve within 2 hours)**
- Production outages
- Security vulnerabilities
- Complete team blockers

**P1 - High (Resolve within 1 day)**
- Individual agent blockers
- Quality failures
- Integration issues

**P2 - Medium (Resolve within 3 days)**
- Process improvements
- Tool issues
- Documentation gaps

**P3 - Low (Resolve within 1 week)**
- Nice-to-have improvements
- Training needs
- Long-term optimizations

#### Issue Categories
- **Technical**: Code, infrastructure, tool issues
- **Process**: Workflow, communication, coordination issues
- **Resource**: Capacity, skill, availability issues
- **Quality**: Standards, review, testing issues
"""


def _generate_resolution_workflows() -> str:
    """Generate issue resolution workflows."""
    return """
#### Standard Resolution Workflow
1. **Issue Identification**: Agent identifies and reports issue
2. **Triage**: Team lead assesses priority and assigns owner
3. **Investigation**: Owner investigates root cause
4. **Resolution**: Owner implements fix or workaround
5. **Validation**: Team validates resolution
6. **Documentation**: Resolution documented for future reference

#### Escalation Workflow
- **Level 1**: Agent attempts self-resolution (30 minutes)
- **Level 2**: Peer assistance requested (1 hour)
- **Level 3**: Team lead involvement (2 hours)
- **Level 4**: External escalation (4 hours)

#### Communication Templates
```
ISSUE_REPORTED: [agent-id] - [issue-type] - [priority] - [description]
ISSUE_ASSIGNED: [owner] - [issue-id] - [estimated-resolution-time]
ISSUE_RESOLVED: [owner] - [issue-id] - [resolution-summary]
```
"""


def _generate_efficiency_metrics(team_size: int) -> str:
    """Generate team efficiency metrics."""
    return f"""
#### Key Efficiency Indicators
- **Agent Utilization**: [Percentage of time spent on productive work]
- **Idle Time**: [Percentage of time agents are waiting/blocked]
- **Context Switching**: [Frequency of task changes per agent]
- **Handoff Efficiency**: [Success rate and speed of agent handoffs]
- **Meeting Overhead**: [Time spent in coordination vs development]

#### Productivity Targets
- **Individual Productivity**: {6 if team_size <= 3 else 5 if team_size <= 6 else 4} tasks per agent per day
- **Team Velocity**: {team_size * 5} tasks per day (team target)
- **Quality Gate**: >90% first-time pass rate for code reviews
- **Response Time**: <2 hours for help requests
- **Handoff Success**: >95% successful handoffs without rework
"""


def _generate_improvement_strategies(management_focus: str) -> str:
    """Generate improvement strategies based on focus."""
    strategies = {
        "velocity": """
#### Velocity Improvement Strategies
- **Task Decomposition**: Break large tasks into smaller, manageable pieces
- **Parallel Processing**: Identify opportunities for concurrent work
- **Automation**: Automate repetitive tasks and processes
- **Skill Development**: Cross-train agents to reduce bottlenecks
- **Tool Optimization**: Improve development tools and workflows
""",
        "quality": """
#### Quality Improvement Strategies
- **Code Review Standards**: Establish and enforce quality criteria
- **Test-Driven Development**: Implement TDD practices
- **Continuous Integration**: Automated testing and quality checks
- **Pair Programming**: Collaborative development for quality
- **Quality Metrics**: Track and improve quality indicators
""",
        "collaboration": """
#### Collaboration Improvement Strategies
- **Communication Protocols**: Standardize team communication
- **Knowledge Sharing**: Regular tech talks and documentation
- **Mentoring Programs**: Pair experienced with junior agents
- **Team Building**: Activities to improve team cohesion
- **Feedback Culture**: Regular feedback and improvement discussions
"""
    }

    return strategies.get(management_focus, """
#### General Improvement Strategies
- **Process Optimization**: Continuously improve development processes
- **Skill Development**: Invest in team member growth
- **Tool Enhancement**: Upgrade and optimize development tools
- **Communication**: Improve team communication and coordination
- **Quality Focus**: Maintain high standards for deliverables
""")


def _generate_communication_protocols() -> str:
    """Generate communication protocols for team management."""
    return """
#### Daily Communication
- **Morning Standup**: 15-minute status update (9:00 AM)
- **Progress Check**: Mid-day coordination (1:00 PM)
- **End of Day**: Summary and planning (5:00 PM)

#### Weekly Communication
- **Monday**: Sprint planning and goal setting
- **Wednesday**: Mid-week review and adjustments
- **Friday**: Retrospective and improvement planning

#### Communication Templates
```
STATUS_UPDATE: [agent-id] [timestamp] - [current-task] - [progress] - [blockers] - [help-needed]
PROGRESS_REPORT: [agent-id] [timestamp] - [completed] - [in-progress] - [planned]
BLOCKER_ALERT: [agent-id] [timestamp] - [blocker-description] - [impact] - [help-requested]
HELP_REQUEST: [agent-id] [timestamp] - [help-type] - [urgency] - [context]
```
"""


def _generate_resource_allocation(team_size: int) -> str:
    """Generate resource allocation overview."""
    return f"""
#### Current Agent Assignments
{chr(10).join([f"- **Agent{i}**: [Role] - [Current Task] - [Estimated Completion]" for i in range(1, team_size + 1)])}

#### Workload Distribution
- **High Utilization** (>80%): [List agents with high workload]
- **Medium Utilization** (50-80%): [List agents with medium workload]
- **Low Utilization** (<50%): [List agents with low workload]

#### Skill Allocation
- **Frontend Work**: [Agents assigned to frontend tasks]
- **Backend Work**: [Agents assigned to backend tasks]
- **Testing Work**: [Agents assigned to testing tasks]
- **DevOps Work**: [Agents assigned to infrastructure tasks]
"""


def _generate_capacity_management(team_size: int) -> str:
    """Generate capacity management overview."""
    total_capacity = team_size * 8  # 8 hours per agent per day
    return f"""
#### Daily Capacity Overview
- **Total Capacity**: {total_capacity} hours/day ({team_size} agents × 8 hours)
- **Committed Capacity**: [X hours committed to current tasks]
- **Available Capacity**: [Y hours available for new work]
- **Buffer Capacity**: [Z hours reserved for unexpected work]

#### Capacity Utilization Targets
- **Optimal Utilization**: 70-80% (allows for flexibility)
- **Maximum Utilization**: 90% (short-term only)
- **Buffer Requirement**: 20% (for unexpected work and improvements)

#### Capacity Planning
- **Next Sprint**: [Planned capacity allocation]
- **Upcoming Features**: [Capacity requirements for planned features]
- **Skill Gaps**: [Areas where additional capacity is needed]
"""


def _generate_quality_metrics() -> str:
    """Generate quality metrics tracking."""
    return """
#### Code Quality Metrics
- **Review Score**: [Average code review rating 1-10]
- **Bug Rate**: [Bugs per 100 lines of code]
- **Test Coverage**: [Percentage of code covered by tests]
- **Documentation Coverage**: [Percentage of code with documentation]

#### Process Quality Metrics
- **Handoff Success Rate**: [Percentage of successful agent handoffs]
- **Rework Rate**: [Percentage of work requiring revision]
- **First-Time Pass Rate**: [Percentage passing review on first attempt]
- **Communication Effectiveness**: [Response time and clarity scores]

#### Quality Targets
- **Code Review Score**: >8.0/10
- **Bug Rate**: <2 bugs per 100 lines
- **Test Coverage**: >80%
- **Handoff Success**: >95%
- **First-Time Pass**: >90%
"""


def _generate_skill_development_tracking(team_size: int) -> str:
    """Generate skill development tracking."""
    return f"""
#### Individual Skill Development
{chr(10).join([f"- **Agent{i}**: [Current Skills] - [Learning Goals] - [Progress]" for i in range(1, team_size + 1)])}

#### Team Skill Matrix
- **Frontend**: [Skill levels: Expert/Intermediate/Beginner]
- **Backend**: [Skill levels: Expert/Intermediate/Beginner]
- **DevOps**: [Skill levels: Expert/Intermediate/Beginner]
- **Testing**: [Skill levels: Expert/Intermediate/Beginner]
- **Domain Knowledge**: [Skill levels: Expert/Intermediate/Beginner]

#### Skill Development Goals
- **Cross-Training**: [Plans to develop backup expertise]
- **Specialization**: [Plans to deepen specific skills]
- **Knowledge Sharing**: [Plans to share expertise across team]

#### Training Resources
- **Internal**: [Mentoring, pair programming, code reviews]
- **External**: [Courses, conferences, certifications]
- **Documentation**: [Internal knowledge base and best practices]
"""


def _generate_knowledge_sharing_protocols() -> str:
    """Generate knowledge sharing protocols."""
    return """
#### Knowledge Sharing Activities
- **Tech Talks**: Weekly 30-minute presentations by team members
- **Code Reviews**: Detailed reviews with learning focus
- **Pair Programming**: Collaborative development sessions
- **Documentation**: Shared knowledge base and best practices

#### Knowledge Sharing Schedule
- **Monday**: Tech talk or knowledge sharing session
- **Wednesday**: Pair programming or mentoring session
- **Friday**: Documentation review and updates

#### Knowledge Areas
- **Technical Skills**: Programming languages, frameworks, tools
- **Domain Knowledge**: Business requirements, user needs
- **Process Knowledge**: Development workflows, best practices
- **Problem Solving**: Debugging techniques, optimization strategies
"""


def _generate_risk_monitoring() -> str:
    """Generate risk monitoring framework."""
    return """
#### Risk Categories

**Technical Risks**
- **Key Person Dependencies**: Critical knowledge held by single agent
- **Technology Risks**: Outdated or problematic technology choices
- **Integration Risks**: Complex system integration challenges

**Process Risks**
- **Communication Breakdown**: Poor team communication
- **Quality Issues**: Declining code quality or testing
- **Coordination Problems**: Poor handoffs or collaboration

**Resource Risks**
- **Capacity Constraints**: Insufficient team capacity
- **Skill Gaps**: Missing critical skills on team
- **Agent Availability**: Team member unavailability

#### Risk Monitoring
- **Daily**: Monitor for immediate risks and blockers
- **Weekly**: Assess process and coordination risks
- **Monthly**: Review strategic and technical risks

#### Risk Indicators
- **Red Flags**: Immediate attention required
- **Yellow Flags**: Monitor closely, may need intervention
- **Green Flags**: Low risk, continue monitoring
"""


def _generate_contingency_planning(team_size: int) -> str:
    """Generate contingency planning."""
    return f"""
#### Contingency Scenarios

**Agent Unavailability**
- **Single Agent**: Redistribute work, pair with backup
- **Multiple Agents**: Adjust scope, extend timeline
- **Key Agent**: Activate knowledge transfer protocols

**Technical Issues**
- **Tool Failures**: Switch to backup tools, manual processes
- **Integration Problems**: Rollback, isolate, fix incrementally
- **Performance Issues**: Optimize, scale, or redesign

**Process Breakdowns**
- **Communication Issues**: Increase check-ins, clarify protocols
- **Quality Problems**: Increase reviews, add quality gates
- **Coordination Failures**: Simplify processes, add oversight

#### Response Teams
- **Technical Issues**: [Lead developer + specialist]
- **Process Issues**: [Team lead + coordinator]
- **Resource Issues**: [Manager + team lead]

#### Escalation Procedures
1. **Team Level**: Team attempts resolution (2 hours)
2. **Lead Level**: Team lead involvement (4 hours)
3. **Management Level**: Manager escalation (8 hours)
4. **External Level**: Outside help requested (24 hours)
"""


def _create_team_management_files(team_size: int, project_name: str):
    """Create team management coordination files."""

    # Create team status file
    status_file = Path(".agor") / "team-status.md"
    status_content = f"""
# Team Status Dashboard

## Project: {project_name}
## Team Size: {team_size} agents
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Status

### Active Agents
{chr(10).join([f"- **Agent{i}**: [Status] - [Current Task] - [Progress]" for i in range(1, team_size + 1)])}

### Today's Progress
- **Completed**: [List completed tasks]
- **In Progress**: [List current tasks]
- **Blocked**: [List blocked tasks]
- **Planned**: [List planned tasks]

### Team Health
- **Overall Status**: [Green/Yellow/Red]
- **Communication**: [Effective/Needs Improvement]
- **Coordination**: [Smooth/Some Issues/Major Issues]
- **Morale**: [High/Medium/Low]

## Daily Updates

### {datetime.now().strftime('%Y-%m-%d')}
- **Morning Status**: [Team status at start of day]
- **Midday Check**: [Progress and issues at midday]
- **End of Day**: [Summary of day's work]

## Issues and Blockers

### Active Issues
- [No active issues currently]

### Resolved Today
- [No issues resolved today]

## Tomorrow's Plan
- [Priorities for next day]
"""
    status_file.write_text(status_content)

    # Create team metrics file
    metrics_file = Path(".agor") / "team-metrics.md"
    metrics_content = f"""
# Team Performance Metrics

## Project: {project_name}
## Tracking Period: {datetime.now().strftime('%Y-%m-%d')} onwards

## Key Performance Indicators

### Productivity Metrics
- **Team Velocity**: [Tasks completed per day]
- **Individual Productivity**: [Tasks per agent per day]
- **Cycle Time**: [Average time from start to completion]
- **Throughput**: [Work items completed per time period]

### Quality Metrics
- **Code Review Score**: [Average rating 1-10]
- **Bug Rate**: [Bugs per 100 lines of code]
- **Test Coverage**: [Percentage of code tested]
- **Rework Rate**: [Percentage requiring revision]

### Collaboration Metrics
- **Communication Frequency**: [Messages per agent per day]
- **Help Response Time**: [Average time to respond to requests]
- **Knowledge Sharing**: [Documentation contributions]
- **Handoff Success Rate**: [Percentage of successful handoffs]

## Daily Tracking

### {datetime.now().strftime('%Y-%m-%d')}
- **Tasks Completed**: 0
- **Active Agents**: 0/{team_size}
- **Blockers**: 0
- **Quality Issues**: 0

## Weekly Summary

### Week of {datetime.now().strftime('%Y-%m-%d')}
- **Velocity**: [Tasks completed this week]
- **Quality Score**: [Average quality rating]
- **Team Utilization**: [Percentage of capacity used]
- **Issues Resolved**: [Number of issues resolved]

## Trends and Analysis

### Performance Trends
- [Analysis of performance over time]

### Improvement Opportunities
- [Areas for improvement identified]
"""
    metrics_file.write_text(metrics_content)

    # Create team issues file
    issues_file = Path(".agor") / "team-issues.md"
    issues_content = f"""
# Team Issue Tracking

## Project: {project_name}
## Issue Tracking Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Active Issues

### Critical (P0)
- [No critical issues currently]

### High Priority (P1)
- [No high priority issues currently]

### Medium Priority (P2)
- [No medium priority issues currently]

### Low Priority (P3)
- [No low priority issues currently]

## Issue History

### Resolved Issues
- [No issues resolved yet]

### Issue Templates

#### New Issue Template
```
**Issue ID**: [Unique identifier]
**Priority**: [P0/P1/P2/P3]
**Category**: [Technical/Process/Resource/Quality]
**Reporter**: [Agent who reported]
**Assigned**: [Agent responsible for resolution]
**Created**: [Timestamp]
**Description**: [Detailed description of issue]
**Impact**: [How it affects team/project]
**Steps to Reproduce**: [If applicable]
**Expected Resolution**: [Target date]
**Status**: [Open/In Progress/Resolved]
```

#### Resolution Template
```
**Issue ID**: [Reference to original issue]
**Resolution**: [How the issue was resolved]
**Root Cause**: [What caused the issue]
**Prevention**: [How to prevent similar issues]
**Lessons Learned**: [What the team learned]
**Resolved By**: [Agent who resolved]
**Resolved Date**: [Timestamp]
```

## Issue Statistics

### Current Period
- **Total Issues**: 0
- **Resolved Issues**: 0
- **Average Resolution Time**: [To be calculated]
- **Most Common Category**: [To be determined]
"""
    issues_file.write_text(issues_content)

    # Create agent assignments file
    assignments_file = Path(".agor") / "agent-assignments.md"
    newline = chr(10)
    agent_sections = newline.join([f"### Agent{i}{newline}- **Role**: [Assigned role]{newline}- **Current Task**: [Task description]{newline}- **Priority**: [High/Medium/Low]{newline}- **Estimated Completion**: [Date/time]{newline}- **Dependencies**: [What this task depends on]{newline}- **Blockers**: [Current blockers if any]{newline}" for i in range(1, team_size + 1)])

    assignments_content = f"""
# Agent Task Assignments

## Project: {project_name}
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Assignments

{agent_sections}

## Assignment History

### {datetime.now().strftime('%Y-%m-%d')}
- [Assignment changes and updates will be tracked here]

## Workload Balance

### High Workload
- [Agents with >80% capacity utilization]

### Medium Workload
- [Agents with 50-80% capacity utilization]

### Low Workload
- [Agents with <50% capacity utilization]

## Skill Utilization

### Frontend Tasks
- [Agents working on frontend]

### Backend Tasks
- [Agents working on backend]

### Testing Tasks
- [Agents working on testing]

### DevOps Tasks
- [Agents working on infrastructure]

## Assignment Guidelines

### Task Assignment Criteria
- **Skill Match**: Assign tasks matching agent expertise
- **Workload Balance**: Distribute work evenly across team
- **Learning Opportunities**: Include skill development tasks
- **Dependencies**: Consider task dependencies and sequencing

### Assignment Process
1. **Task Analysis**: Understand requirements and complexity
2. **Skill Assessment**: Identify required skills and expertise
3. **Capacity Check**: Verify agent availability and workload
4. **Assignment**: Assign task to most suitable agent
5. **Communication**: Notify agent and update tracking
"""
    assignments_file.write_text(assignments_content)


def _initialize_team_metrics(team_size: int):
    """Initialize team metrics tracking system."""

    # Create team retrospective file
    retro_file = Path(".agor") / "team-retrospective.md"
    retro_content = f"""
# Team Retrospective Notes

## Retrospective Schedule
- **Frequency**: Weekly (every Friday)
- **Duration**: 30 minutes
- **Participants**: All {team_size} team members

## Retrospective Format

### What Went Well
- [Things that worked well this week]

### What Could Be Improved
- [Areas for improvement identified]

### Action Items
- [Specific actions to take next week]

### Experiments
- [Process improvements to try]

## Retrospective History

### Week of {datetime.now().strftime('%Y-%m-%d')}
- **What Went Well**: [To be filled during retrospective]
- **Improvements**: [To be filled during retrospective]
- **Action Items**: [To be filled during retrospective]
- **Experiments**: [To be filled during retrospective]

## Improvement Tracking

### Implemented Improvements
- [Improvements that have been successfully implemented]

### Ongoing Experiments
- [Process improvements currently being tested]

### Lessons Learned
- [Key insights from retrospectives]

## Team Health Indicators

### Communication
- **Frequency**: [How often team communicates]
- **Quality**: [Effectiveness of communication]
- **Issues**: [Communication problems identified]

### Collaboration
- **Handoffs**: [Quality of work handoffs]
- **Help Requests**: [Response to help requests]
- **Knowledge Sharing**: [Sharing of expertise]

### Satisfaction
- **Work Satisfaction**: [Team satisfaction with work]
- **Process Satisfaction**: [Satisfaction with processes]
- **Team Dynamics**: [Quality of team relationships]
"""
    retro_file.write_text(retro_content)


def _generate_gate_ownership() -> str:
    """Generate gate ownership assignments."""
    return """
#### Gate Ownership Assignments
- **Requirements Gate**: Product Owner / Business Analyst
- **Design Gate**: Technical Architect / Lead Developer
- **Implementation Gate**: Development Team / Code Reviewers
- **Integration Gate**: Integration Team / QA Lead
- **System Gate**: QA Team / Test Lead
- **Deployment Gate**: DevOps Team / Release Manager
"""


def _generate_gate_dependencies() -> str:
    """Generate gate dependencies mapping."""
    return """
#### Gate Dependencies
- **Design Gate** depends on Requirements Gate completion
- **Implementation Gate** depends on Design Gate approval
- **Integration Gate** depends on Implementation Gate success
- **System Gate** depends on Integration Gate validation
- **Deployment Gate** depends on System Gate approval

#### Parallel Gate Opportunities
- **Documentation** can be developed in parallel with Implementation
- **Test Planning** can occur during Design phase
- **Deployment Preparation** can begin during System testing
"""


def _generate_gate_scheduling() -> str:
    """Generate gate scheduling framework."""
    return """
#### Gate Scheduling
- **Requirements Gate**: Project start + 1-2 days
- **Design Gate**: Requirements complete + 2-3 days
- **Implementation Gate**: Per feature/component completion
- **Integration Gate**: Weekly or per integration milestone
- **System Gate**: End of development phase
- **Deployment Gate**: Pre-release validation

#### Gate Review Meetings
- **Frequency**: As needed based on gate triggers
- **Duration**: 30-60 minutes per gate
- **Participants**: Gate owner + stakeholders + development team
- **Format**: Criteria review + go/no-go decision
"""


def _create_quality_gate_files(quality_focus: str, automation_level: str):
    """Create quality gate coordination files."""

    # Create quality metrics file
    metrics_file = Path(".agor") / "quality-metrics.md"
    metrics_content = f"""
# Quality Metrics Dashboard

## Quality Focus: {quality_focus}
## Automation Level: {automation_level}
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Quality Status

### Code Quality Metrics
- **Code Coverage**: [X%] (Target: >80%)
- **Cyclomatic Complexity**: [X] (Target: <10)
- **Technical Debt**: [X hours] (Target: <40 hours)
- **Bug Density**: [X bugs/kloc] (Target: <2 bugs/kloc)
- **Code Review Score**: [X/10] (Target: >8/10)

### Process Quality Metrics
- **Gate Pass Rate**: [X%] (Target: >90%)
- **Rework Rate**: [X%] (Target: <10%)
- **Defect Escape Rate**: [X%] (Target: <5%)
- **Time to Resolution**: [X hours] (Target: <24 hours)
- **Customer Satisfaction**: [X/10] (Target: >8/10)

## Quality Gate Status

### Gate 1: Requirements Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

### Gate 2: Design Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

### Gate 3: Implementation Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

### Gate 4: Integration Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

### Gate 5: System Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

### Gate 6: Deployment Quality
- **Status**: [Not Started/In Progress/Complete]
- **Score**: [X/100]
- **Issues**: [List any issues]
- **Next Action**: [What needs to be done]

## Quality Trends

### Weekly Quality Summary
- **Week of {datetime.now().strftime('%Y-%m-%d')}**:
  - Gates Passed: [X/6]
  - Quality Score: [X/100]
  - Issues Resolved: [X]
  - Improvement Actions: [X]

## Quality Improvement Actions

### Active Improvements
- [No active improvements currently]

### Completed Improvements
- [No improvements completed yet]

### Planned Improvements
- [No improvements planned yet]
"""
    metrics_file.write_text(metrics_content)

    # Create quality standards file
    standards_file = Path(".agor") / "quality-standards.md"
    standards_content = f"""
# Quality Standards

## Quality Focus: {quality_focus}
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Code Quality Standards

### Naming Conventions
- **Variables**: camelCase for JavaScript, snake_case for Python
- **Functions**: Descriptive verbs (e.g., getUserData, calculateTotal)
- **Classes**: PascalCase (e.g., UserManager, DataProcessor)
- **Constants**: UPPER_SNAKE_CASE (e.g., MAX_RETRY_COUNT)

### Code Structure
- **File Length**: Maximum 500 lines per file
- **Function Length**: Maximum 50 lines per function
- **Class Length**: Maximum 300 lines per class
- **Nesting Depth**: Maximum 4 levels of nesting

### Documentation Standards
- **Functions**: JSDoc/docstring for all public functions
- **Classes**: Class-level documentation with purpose and usage
- **APIs**: OpenAPI/Swagger documentation for all endpoints
- **README**: Comprehensive setup and usage instructions

### Testing Standards
- **Unit Tests**: >80% code coverage required
- **Integration Tests**: All API endpoints must have tests
- **Test Naming**: Descriptive test names (should_return_error_when_invalid_input)
- **Test Structure**: Arrange-Act-Assert pattern

## Process Quality Standards

### Code Review Standards
- **Review Required**: All code changes must be reviewed
- **Review Criteria**: Functionality, security, performance, maintainability
- **Review Timeline**: Reviews completed within 24 hours
- **Approval Required**: At least one approval before merge

### Git Standards
- **Commit Messages**: Conventional commits format
- **Branch Naming**: feature/description, bugfix/description, hotfix/description
- **Pull Requests**: Template with description, testing, and checklist
- **Merge Strategy**: Squash and merge for feature branches

### Quality Gate Standards
- **Gate Criteria**: Objective, measurable criteria for each gate
- **Gate Documentation**: All gate results must be documented
- **Gate Approval**: Designated gate owner must approve
- **Gate Escalation**: Failed gates must be escalated within 2 hours

## Security Standards

### Input Validation
- **All Inputs**: Validate and sanitize all user inputs
- **SQL Injection**: Use parameterized queries or ORM
- **XSS Prevention**: Escape output, use Content Security Policy
- **CSRF Protection**: Use CSRF tokens for state-changing operations

### Authentication & Authorization
- **Password Policy**: Minimum 8 characters, complexity requirements
- **Session Management**: Secure session handling, timeout policies
- **Access Control**: Role-based access control (RBAC)
- **API Security**: Authentication required for all API endpoints

### Data Protection
- **Encryption**: Encrypt sensitive data at rest and in transit
- **PII Handling**: Special handling for personally identifiable information
- **Data Retention**: Clear data retention and deletion policies
- **Backup Security**: Encrypted backups with access controls

## Performance Standards

### Response Time Standards
- **API Responses**: <200ms for 95% of requests
- **Page Load**: <3 seconds for initial page load
- **Database Queries**: <100ms for simple queries, <1s for complex
- **File Operations**: <500ms for file uploads/downloads

### Resource Usage Standards
- **Memory Usage**: <500MB per application instance
- **CPU Usage**: <70% average CPU utilization
- **Database Connections**: Connection pooling with max 20 connections
- **File Storage**: Efficient file storage with cleanup policies

### Scalability Standards
- **Horizontal Scaling**: Application must support horizontal scaling
- **Load Testing**: Must handle 10x current load
- **Caching**: Implement caching for frequently accessed data
- **CDN Usage**: Use CDN for static assets

## Quality Enforcement

### Automated Enforcement
- **Linting**: Automated code style checking
- **Testing**: Automated test execution in CI/CD
- **Security Scanning**: Automated vulnerability scanning
- **Performance Testing**: Automated performance benchmarking

### Manual Enforcement
- **Code Reviews**: Manual review of all code changes
- **Architecture Reviews**: Manual review of design decisions
- **Security Reviews**: Manual security assessment
- **Performance Reviews**: Manual performance analysis

### Quality Metrics
- **Compliance Rate**: Percentage of code meeting standards
- **Violation Trends**: Tracking of standard violations over time
- **Improvement Rate**: Rate of quality improvement over time
- **Team Adoption**: Team adoption of quality practices
"""
    standards_file.write_text(standards_content)

    # Create individual gate files
    gates = [
        ("requirements", "Requirements Quality Gate"),
        ("design", "Design Quality Gate"),
        ("implementation", "Implementation Quality Gate"),
        ("integration", "Integration Quality Gate"),
        ("system", "System Quality Gate"),
        ("deployment", "Deployment Quality Gate")
    ]

    for gate_id, gate_name in gates:
        gate_file = Path(".agor") / f"gate-{gate_id}.md"
        gate_content = f"""
# {gate_name}

## Gate Overview
- **Gate ID**: {gate_id}
- **Gate Name**: {gate_name}
- **Owner**: [To be assigned]
- **Status**: Not Started
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Entry Criteria
- [Criteria that must be met to trigger this gate]

## Validation Criteria
- [ ] [Specific quality check 1]
- [ ] [Specific quality check 2]
- [ ] [Specific quality check 3]
- [ ] [Specific quality check 4]

## Exit Criteria
- [Criteria that must be met to pass this gate]

## Gate Execution

### Validation Process
1. [Step 1 of validation process]
2. [Step 2 of validation process]
3. [Step 3 of validation process]
4. [Step 4 of validation process]

### Validation Results
- **Executed By**: [Agent/team who executed validation]
- **Execution Date**: [When validation was performed]
- **Results**: [Pass/Fail with details]
- **Score**: [X/100]
- **Issues Found**: [List of issues if any]

### Gate Decision
- **Decision**: [Pass/Fail/Conditional Pass]
- **Decision By**: [Gate owner who made decision]
- **Decision Date**: [When decision was made]
- **Rationale**: [Reason for decision]
- **Next Actions**: [What needs to happen next]

## Issue Tracking

### Issues Found
- [No issues found yet]

### Issues Resolved
- [No issues resolved yet]

## Gate History

### Execution History
- [No executions yet]

### Improvement History
- [No improvements yet]

## Notes
- [Additional notes and context for this gate]
"""
        gate_file.write_text(gate_content)


def _initialize_quality_metrics(project_name: str):
    """Initialize quality metrics tracking."""

    # Create quality tracking summary file
    summary_file = Path(".agor") / "quality-summary.md"
    summary_content = f"""
# Quality Summary Dashboard

## Project: {project_name}
## Quality System Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Quality Status
- **Quality Score**: [To be calculated]
- **Gates Passed**: 0/6
- **Active Issues**: 0
- **Quality Trend**: [To be determined]

## Quick Quality Metrics

### Code Quality
- **Coverage**: [X%]
- **Complexity**: [X]
- **Debt**: [X hours]
- **Bugs**: [X/kloc]

### Process Quality
- **Gate Pass Rate**: [X%]
- **Rework Rate**: [X%]
- **Resolution Time**: [X hours]
- **Satisfaction**: [X/10]

## Recent Quality Activities

### Today ({datetime.now().strftime('%Y-%m-%d')})
- Quality gates system initialized
- Quality standards established
- Metrics tracking started

## Quality Improvement Plan

### Short Term (This Week)
- [ ] Complete requirements quality gate
- [ ] Establish baseline metrics
- [ ] Train team on quality standards

### Medium Term (This Month)
- [ ] Implement automated quality checks
- [ ] Complete design and implementation gates
- [ ] Optimize quality processes

### Long Term (This Quarter)
- [ ] Achieve target quality metrics
- [ ] Establish quality culture
- [ ] Continuous quality improvement

## Quality Resources

### Documentation
- `.agor/quality-gates.md` - Complete quality gate system
- `.agor/quality-standards.md` - Quality standards and guidelines
- `.agor/quality-metrics.md` - Detailed metrics dashboard
- `.agor/gate-[name].md` - Individual gate tracking

### Tools and Automation
- [Quality tools to be configured]
- [Automation scripts to be developed]
- [Integration points to be established]

### Training and Support
- [Quality training materials]
- [Team support resources]
- [Quality champion program]
"""
    summary_file.write_text(summary_content)


def setup_quality_gates(project_name: str = "Current Project", quality_focus: str = "comprehensive", automation_level: str = "medium") -> str:
    """Setup quality gates and validation checkpoints (qg hotkey)."""

    # Import the quality gates template
    from .project_planning_templates import generate_quality_gates_template

    # Get the base template
    template = generate_quality_gates_template()

    # Add concrete quality gates implementation
    implementation_details = f"""
## QUALITY GATES IMPLEMENTATION

### Project: {project_name}
### Quality Focus: {quality_focus}
### Automation Level: {automation_level}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ACTIVE QUALITY GATES

{_generate_active_quality_gates(quality_focus)}

## QUALITY GATE EXECUTION PROTOCOLS

### Gate Validation Process:
1. **Gate Trigger**: Automatic detection when deliverable is ready
   ```
   GATE_TRIGGERED: [gate-name] - [deliverable] - [timestamp] - [responsible-agent]
   ```

2. **Quality Validation**: Execute all gate criteria checks
   ```
   GATE_VALIDATION: [gate-name] - [criteria-checked] - [pass/fail] - [details]
   ```

3. **Gate Decision**: Go/no-go decision based on validation results
   ```
   GATE_DECISION: [gate-name] - [PASS/FAIL] - [score] - [next-action]
   ```

4. **Gate Communication**: Notify stakeholders of gate results
   ```
   GATE_NOTIFICATION: [stakeholders] - [gate-name] - [result] - [impact]
   ```

### Gate Failure Handling:
1. **Immediate Response**: Stop progression, identify issues
2. **Root Cause Analysis**: Determine why gate failed
3. **Remediation Plan**: Create plan to address issues
4. **Re-validation**: Re-run gate after fixes
5. **Process Improvement**: Update gates based on learnings

## AUTOMATED QUALITY CHECKS

{_generate_automated_quality_checks(automation_level)}

## QUALITY METRICS TRACKING

{_generate_quality_metrics_tracking()}

## QUALITY STANDARDS ENFORCEMENT

{_generate_quality_standards_enforcement(quality_focus)}

## CONTINUOUS QUALITY IMPROVEMENT

### Quality Feedback Loops:
- **Real-time**: Immediate feedback during development
- **Daily**: Daily quality metrics review
- **Weekly**: Quality trends analysis
- **Monthly**: Quality process improvement

### Quality Learning:
- **Defect Analysis**: Learn from quality failures
- **Best Practices**: Capture and share quality successes
- **Tool Improvement**: Enhance quality tools and automation
- **Standard Evolution**: Evolve quality standards based on experience

## QUALITY GATE COORDINATION

### Gate Ownership:
{_generate_gate_ownership()}

### Gate Dependencies:
{_generate_gate_dependencies()}

### Gate Scheduling:
{_generate_gate_scheduling()}

## QUALITY ASSURANCE AUTOMATION

### Automated Gate Execution:
```python
# Execute quality gate
from agor.tools.strategy_protocols import execute_quality_gate
result = execute_quality_gate(
    gate_name="implementation_quality",
    deliverable="user_auth_module",
    criteria=["code_review", "unit_tests", "security_scan"]
)
print(f"Gate result: {result['status']} - Score: {result['score']}/100")
```

### Quality Metrics Collection:
```python
# Collect quality metrics
from agor.tools.strategy_protocols import collect_quality_metrics
metrics = collect_quality_metrics(project_name)
print(f"Code coverage: {metrics['coverage']}%")
print(f"Bug density: {metrics['bug_density']} bugs/kloc")
print(f"Gate pass rate: {metrics['gate_pass_rate']}%")
```

## QUALITY CULTURE DEVELOPMENT

### Quality Champions Program:
- **Quality Advocates**: Agents who promote quality practices
- **Knowledge Sharing**: Regular quality best practices sessions
- **Mentoring**: Quality coaching for team members
- **Innovation**: Exploring new quality tools and techniques

### Quality Training:
- **Quality Standards**: Training on coding and process standards
- **Tool Usage**: Training on quality tools and automation
- **Best Practices**: Sharing quality best practices and lessons learned
- **Continuous Learning**: Ongoing quality skill development

## NEXT STEPS

1. **Review Quality Gates**: Validate gate definitions and criteria
2. **Setup Automation**: Configure automated quality checks
3. **Train Team**: Ensure all agents understand quality standards
4. **Begin Execution**: Start using quality gates in development process
5. **Monitor and Improve**: Track quality metrics and optimize gates
"""

    # Combine template with implementation
    full_quality_plan = template + implementation_details

    # Save to quality gates file
    quality_file = Path(".agor") / "quality-gates.md"
    quality_file.parent.mkdir(exist_ok=True)
    quality_file.write_text(full_quality_plan)

    # Create quality gate coordination files
    _create_quality_gate_files(quality_focus, automation_level)

    # Initialize quality metrics tracking
    _initialize_quality_metrics(project_name)

    return f"""✅ Quality Gates Established

**Project**: {project_name}
**Quality Focus**: {quality_focus}
**Automation Level**: {automation_level}

**Quality Gate Features**:
- 6-stage quality validation process (Requirements → Deployment)
- Automated quality checks and validation
- Quality metrics tracking and reporting
- Gate failure handling and remediation
- Continuous quality improvement processes

**Files Created**:
- `.agor/quality-gates.md` - Complete quality gate plan and standards
- `.agor/quality-metrics.md` - Quality metrics tracking dashboard
- `.agor/quality-standards.md` - Coding and process standards
- `.agor/gate-[name].md` - Individual gate validation files

**Next Steps**:
1. Review and customize quality standards
2. Configure automated quality checks
3. Train team on quality gate processes
4. Begin quality gate execution
5. Monitor quality metrics and optimize

**Ready for comprehensive quality assurance!**
"""