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
