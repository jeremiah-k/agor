"""
Multi-Agent Strategy Implementation Protocols for AGOR.

This module provides concrete implementation protocols for AGOR's multi-agent strategies:
- Parallel Divergent: Multiple agents work independently then converge
- Red Team: Adversarial testing with blue team vs red team
- Mob Programming: Collaborative development with role rotation
- Strategy Selection: Intelligent strategy recommendation
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Dual-mode importing for bundle and package compatibility
try:
    from ..project_planning_templates import (
        generate_mob_programming_strategy,
        generate_parallel_divergent_strategy,
        generate_red_team_strategy,
    )
except ImportError:
    # Bundle-mode fallback
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from project_planning_templates import (
        generate_mob_programming_strategy,
        generate_parallel_divergent_strategy,
        generate_red_team_strategy,
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


class RedTeamProtocol(StrategyProtocol):
    """Implementation protocol for Red Team strategy."""

    def initialize_strategy(
        self, task: str, blue_team_size: int = 3, red_team_size: int = 3
    ) -> str:
        """Initialize Red Team strategy with adversarial testing."""

        # Create strategy-active.md with template content
        strategy_content = generate_red_team_strategy()

        # Add concrete implementation details
        implementation_details = f"""
## RED TEAM IMPLEMENTATION PROTOCOL

### Task: {task}
### Blue Team: {blue_team_size} agents (Builders)
### Red Team: {red_team_size} agents (Attackers)
### Status: Cycle 1 - Blue Team Build Phase (ACTIVE)

## TEAM ASSIGNMENTS

### Blue Team (Builders)
{self._generate_blue_team_assignments(blue_team_size, task)}

### Red Team (Attackers)
{self._generate_red_team_assignments(red_team_size, task)}

## CURRENT CYCLE: Blue Team Build Phase

### Blue Team Rules:
1. **Build secure solution** - Focus on security from the start
2. **Document security measures** - Record all security decisions
3. **Prepare for attack** - Anticipate potential vulnerabilities
4. **Signal completion** - Post "BLUE_BUILD_COMPLETE" when ready

### Red Team Rules:
1. **Prepare attack strategies** - Plan your attack approach
2. **Research vulnerabilities** - Study common attack vectors
3. **Wait for blue team** - Do not attack until build phase complete
4. **Document attack plans** - Record your attack strategies

### Cycle Completion:
When blue team signals completion, red team attack phase begins automatically.

{self._generate_red_team_instructions(blue_team_size, red_team_size, task)}
"""

        # Combine template with implementation
        full_strategy = strategy_content + implementation_details

        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)

        # Create team memory files
        self._create_red_team_memory_files(blue_team_size, red_team_size)

        # Log strategy initialization
        self.log_communication("COORDINATOR", f"Initialized Red Team strategy: {task}")

        return f"""✅ Red Team Strategy Initialized

**Task**: {task}
**Blue Team**: {blue_team_size} agents (Builders)
**Red Team**: {red_team_size} agents (Attackers)
**Phase**: Cycle 1 - Blue Team Build

**Next Steps**:
1. Blue team: Begin secure implementation
2. Red team: Prepare attack strategies
3. Follow cycle-based adversarial process

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and team assignments
- `.agor/blue-team-memory.md` - Blue team coordination
- `.agor/red-team-memory.md` - Red team attack planning

**Ready for adversarial development!**
"""

    def _generate_blue_team_assignments(self, team_size: int, task: str) -> str:
        """Generate blue team assignments."""
        assignments = []
        for i in range(1, team_size + 1):
            assignments.append(
                f"""
- **Blue Agent {i}**: Security-focused implementation of {task}
  - Branch: `blue-solution-{i}`
  - Focus: Secure coding practices and vulnerability prevention
"""
            )
        return "\n".join(assignments)

    def _generate_red_team_assignments(self, team_size: int, task: str) -> str:
        """Generate red team assignments."""
        assignments = []
        attack_types = [
            "injection",
            "authentication",
            "authorization",
            "data-validation",
            "session-management",
        ]
        for i in range(1, team_size + 1):
            attack_focus = attack_types[(i - 1) % len(attack_types)]
            assignments.append(
                f"""
- **Red Agent {i}**: Attack specialist for {task}
  - Focus: {attack_focus} vulnerabilities
  - Goal: Find and exploit security weaknesses
"""
            )
        return "\n".join(assignments)

    def _generate_red_team_instructions(
        self, blue_size: int, red_size: int, task: str
    ) -> str:
        """Generate detailed red team instructions."""
        return f"""
## DETAILED INSTRUCTIONS

### Blue Team Phase 1: Secure Build
1. **Security-First Development**: Build {task} with security as primary concern
2. **Threat Modeling**: Consider potential attack vectors
3. **Secure Coding**: Follow security best practices
4. **Documentation**: Record all security measures implemented
5. **Testing**: Test for basic security vulnerabilities
6. **Completion Signal**: Post "BLUE_BUILD_COMPLETE" when ready for attack

### Red Team Phase 1: Attack Preparation
1. **Attack Planning**: Develop comprehensive attack strategies
2. **Tool Preparation**: Prepare security testing tools
3. **Vulnerability Research**: Research common vulnerabilities for this type of system
4. **Attack Documentation**: Document planned attack vectors
5. **Wait for Signal**: Begin attacks only after blue team completion signal

### Red Team Phase 2: Attack Execution
1. **Systematic Testing**: Execute planned attacks methodically
2. **Vulnerability Discovery**: Document all vulnerabilities found
3. **Exploit Development**: Develop working exploits for vulnerabilities
4. **Impact Assessment**: Assess business impact of vulnerabilities
5. **Attack Report**: Comprehensive report of findings and recommendations

### Blue Team Phase 2: Defense and Hardening
1. **Vulnerability Analysis**: Review red team findings
2. **Security Hardening**: Fix identified vulnerabilities
3. **Additional Protections**: Implement additional security measures
4. **Testing**: Verify fixes and test against known attacks
5. **Documentation**: Update security documentation

### Cycle Completion and Iteration
- After blue team hardens, red team attacks again
- Continue cycles until no critical vulnerabilities remain
- Final deliverable: Secure, battle-tested implementation
"""

    def _create_red_team_memory_files(self, blue_size: int, red_size: int):
        """Create red team memory files."""
        # Blue team memory
        blue_memory = self.agor_dir / "blue-team-memory.md"
        blue_content = f"""# Blue Team Memory

## Team Composition
{blue_size} agents focused on secure implementation

## Current Phase
Cycle 1 - Secure Build Phase

## Security Measures Implemented
[Document security measures as they are implemented]

## Threat Model
[Document identified threats and mitigations]

## Build Progress
[Track implementation progress]

## Lessons Learned
[Document lessons from red team attacks]
"""
        blue_memory.write_text(blue_content)

        # Red team memory
        red_memory = self.agor_dir / "red-team-memory.md"
        red_content = f"""# Red Team Memory

## Team Composition
{red_size} agents focused on security testing

## Current Phase
Cycle 1 - Attack Preparation

## Attack Strategies
[Document planned attack vectors]

## Vulnerabilities Discovered
[Track vulnerabilities found during attacks]

## Exploit Development
[Document working exploits]

## Recommendations
[Security recommendations for blue team]
"""
        red_memory.write_text(red_content)


class MobProgrammingProtocol(StrategyProtocol):
    """Implementation protocol for Mob Programming strategy."""

    def initialize_strategy(self, task: str, agent_count: int = 4) -> str:
        """Initialize Mob Programming strategy with role rotation."""

        # Create strategy-active.md with template content
        strategy_content = generate_mob_programming_strategy()

        # Add concrete implementation details
        implementation_details = f"""
## MOB PROGRAMMING IMPLEMENTATION PROTOCOL

### Task: {task}
### Mob Size: {agent_count} agents
### Status: Session 1 - Role Assignment (ACTIVE)

## CURRENT SESSION ROLES
{self._generate_mob_roles(agent_count)}

## MOB PROGRAMMING RULES

### Driver Rules:
1. **Type only what navigator says** - No independent decisions
2. **Ask for clarification** - If instructions unclear, ask navigator
3. **Focus on implementation** - Translate navigator's intent to code
4. **Rotate every 15 minutes** - Pass driver role to next agent

### Navigator Rules:
1. **Think strategically** - Focus on high-level approach and design
2. **Give clear instructions** - Tell driver exactly what to type
3. **Explain reasoning** - Help mob understand your thinking
4. **Rotate every 15 minutes** - Pass navigator role to next agent

### Mob Rules:
1. **Stay engaged** - Actively participate in discussions
2. **Respectful communication** - Be kind and constructive
3. **Share ideas** - Contribute thoughts and suggestions
4. **Learn together** - Help each other understand the code

### Session Management:
- **15-minute rotations** - Strict time limits for role changes
- **5-minute breaks** - Every hour for mob rest
- **Session documentation** - Record decisions and progress

## ROTATION SCHEDULE
{self._generate_rotation_schedule(agent_count)}

## SESSION COORDINATION

### Communication Protocol:
```
MOB_SESSION_START: [session-number] - [driver] - [navigator] - [timestamp]
MOB_ROTATION: [new-driver] - [new-navigator] - [session-number] - [timestamp]
MOB_DECISION: [decision] - [rationale] - [session-number] - [timestamp]
MOB_SESSION_END: [session-number] - [progress] - [next-session-plan] - [timestamp]
```

### Progress Tracking:
- Update `.agor/mob-progress.md` after each session
- Document key decisions and rationale
- Track learning and knowledge sharing

{self._generate_mob_instructions(agent_count, task)}
"""

        # Combine template with implementation
        full_strategy = strategy_content + implementation_details

        # Save to strategy-active.md
        strategy_file = self.agor_dir / "strategy-active.md"
        strategy_file.write_text(full_strategy)

        # Create mob coordination files
        self._create_mob_coordination_files(agent_count)

        # Log strategy initialization
        self.log_communication(
            "COORDINATOR", f"Initialized Mob Programming strategy: {task}"
        )

        return f"""✅ Mob Programming Strategy Initialized

**Task**: {task}
**Mob Size**: {agent_count} agents
**Session**: 1 - Ready to begin

**Current Roles**:
- Driver: Agent1
- Navigator: Agent2
- Mob: Agent3, Agent4{', ...' if agent_count > 4 else ''}

**Next Steps**:
1. Begin first 15-minute session
2. Follow rotation schedule
3. Document progress and decisions

**Files Created**:
- `.agor/strategy-active.md` - Strategy details and rotation schedule
- `.agor/mob-progress.md` - Session progress tracking
- `.agor/mob-decisions.md` - Decision log

**Ready for collaborative programming!**
"""

    def _generate_mob_roles(self, agent_count: int) -> str:
        """Generate current mob role assignments."""
        roles = []
        roles.append(
            "- **Driver**: Agent1 - Controls keyboard, implements navigator's instructions"
        )
        roles.append(
            "- **Navigator**: Agent2 - Provides strategic direction and detailed instructions"
        )

        for i in range(3, agent_count + 1):
            roles.append(
                f"- **Mob Member**: Agent{i} - Actively participates, provides ideas and feedback"
            )

        return "\n".join(roles)

    def _generate_rotation_schedule(self, agent_count: int) -> str:
        """Generate rotation schedule for mob programming."""
        schedule = []
        for session in range(1, 5):  # Show first 4 rotations
            driver_idx = ((session - 1) % agent_count) + 1
            navigator_idx = (session % agent_count) + 1
            schedule.append(
                f"**Session {session}**: Driver=Agent{driver_idx}, Navigator=Agent{navigator_idx}"
            )

        schedule.append(
            "**Pattern continues**: Each agent rotates through driver and navigator roles"
        )
        return "\n".join(schedule)

    def _generate_mob_instructions(self, agent_count: int, task: str) -> str:
        """Generate detailed mob programming instructions."""
        return """
## DETAILED MOB INSTRUCTIONS

### Session Structure (15 minutes each):
1. **Role Assignment** (1 minute): Confirm driver and navigator
2. **Planning** (2 minutes): Navigator explains approach for this session
3. **Implementation** (10 minutes): Driver implements with navigator guidance
4. **Review** (2 minutes): Mob reviews progress and provides feedback

### Communication Guidelines:
- **Navigator to Driver**: Clear, specific instructions
- **Mob to Navigator**: Suggestions and alternative approaches
- **Driver to Navigator**: Questions for clarification
- **All**: Respectful, constructive communication

### Decision Making:
- **Small decisions**: Navigator decides quickly
- **Medium decisions**: Brief mob discussion (< 2 minutes)
- **Large decisions**: Pause session, full mob discussion

### Progress Documentation:
After each session, update mob-progress.md with:
- What was accomplished
- Key decisions made
- Challenges encountered
- Next session goals

### Quality Standards:
- **Code Quality**: Maintain high standards through mob review
- **Testing**: Write tests as part of mob programming
- **Documentation**: Document decisions and rationale
- **Refactoring**: Continuously improve code quality

### Mob Etiquette:
- **Be present**: Full attention during sessions
- **Be patient**: Allow others to learn and contribute
- **Be kind**: Constructive feedback only
- **Be engaged**: Actively participate in discussions
"""

    def _create_mob_coordination_files(self, agent_count: int):
        """Create mob programming coordination files."""
        # Mob progress tracking
        progress_file = self.agor_dir / "mob-progress.md"
        progress_content = f"""# Mob Programming Progress

## Mob Composition
{agent_count} agents working collaboratively

## Session Log

### Session 1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Driver**: Agent1
- **Navigator**: Agent2
- **Mob**: {', '.join([f'Agent{i}' for i in range(3, agent_count + 1)])}
- **Progress**: [To be updated during session]
- **Decisions**: [Key decisions made]
- **Next**: [Goals for next session]

## Overall Progress
- **Completed**: [Features/tasks completed]
- **In Progress**: [Current work]
- **Planned**: [Upcoming work]

## Learning Outcomes
- **Knowledge Shared**: [What the mob learned together]
- **Skills Developed**: [Skills improved through collaboration]
- **Best Practices**: [Practices discovered or reinforced]
"""
        progress_file.write_text(progress_content)

        # Mob decisions log
        decisions_file = self.agor_dir / "mob-decisions.md"
        decisions_content = """# Mob Programming Decisions

## Decision Log

### Session 1 Decisions
[Decisions will be recorded here during mob sessions]

## Decision Categories

### Technical Decisions
[Architecture, design, implementation choices]

### Process Decisions
[How the mob works together, process improvements]

### Quality Decisions
[Testing strategies, code quality standards]

## Decision Rationale
[Why decisions were made, alternatives considered]
"""
        decisions_file.write_text(decisions_content)


# Public API functions
def initialize_parallel_divergent(task: str, agent_count: int = 3) -> str:
    """Initialize Parallel Divergent strategy."""
    protocol = ParallelDivergentProtocol()
    return protocol.initialize_strategy(task, agent_count)


def initialize_red_team(
    task: str, blue_team_size: int = 3, red_team_size: int = 3
) -> str:
    """Initialize Red Team strategy."""
    protocol = RedTeamProtocol()
    return protocol.initialize_strategy(task, blue_team_size, red_team_size)


def initialize_mob_programming(task: str, agent_count: int = 4) -> str:
    """Initialize Mob Programming strategy."""
    protocol = MobProgrammingProtocol()
    return protocol.initialize_strategy(task, agent_count)


def select_strategy(
    project_analysis: str = "", team_size: int = 3, complexity: str = "medium"
) -> str:
    """Intelligent strategy selection based on project characteristics."""

    # Import the strategy selection template

    # Analyze project characteristics
    analysis_factors = {
        "team_size": team_size,
        "complexity": complexity,
        "project_type": _analyze_project_type(project_analysis),
        "collaboration_need": _analyze_collaboration_need(project_analysis, team_size),
        "quality_requirements": _analyze_quality_requirements(project_analysis),
        "innovation_need": _analyze_innovation_need(project_analysis),
    }

    # Generate strategy recommendation
    recommendation = _generate_strategy_recommendation(analysis_factors)

    # Create strategy selection document
    selection_content = f"""# Strategy Selection Analysis

## Project Analysis
{project_analysis if project_analysis else "No specific project analysis provided"}

## Analysis Factors
- **Team Size**: {team_size} agents
- **Complexity**: {complexity}
- **Project Type**: {analysis_factors['project_type']}
- **Collaboration Need**: {analysis_factors['collaboration_need']}
- **Quality Requirements**: {analysis_factors['quality_requirements']}
- **Innovation Need**: {analysis_factors['innovation_need']}

## Strategy Recommendation

{recommendation}

## Implementation Guidance

{_generate_implementation_guidance(recommendation)}

## Alternative Strategies

{_generate_alternative_strategies(analysis_factors)}
"""

    # Save strategy selection analysis
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)
    selection_file = agor_dir / "strategy-selection.md"
    selection_file.write_text(selection_content)

    return f"""✅ Strategy Selection Complete

**Recommended Strategy**: {recommendation.split(':')[0] if ':' in recommendation else recommendation}

**Analysis Factors**:
- Team Size: {team_size} agents
- Complexity: {complexity}
- Project Type: {analysis_factors['project_type']}

**Next Steps**:
1. Review strategy selection analysis in `.agor/strategy-selection.md`
2. Initialize recommended strategy using appropriate function
3. Begin coordinated development

**Files Created**:
- `.agor/strategy-selection.md` - Complete analysis and recommendations

**Ready to initialize selected strategy!**
"""


def _analyze_project_type(analysis: str) -> str:
    """Analyze project type from description."""
    analysis_lower = analysis.lower()
    if any(
        word in analysis_lower for word in ["api", "backend", "service", "microservice"]
    ):
        return "API/Backend"
    elif any(
        word in analysis_lower
        for word in ["frontend", "ui", "interface", "react", "vue"]
    ):
        return "Frontend"
    elif any(
        word in analysis_lower
        for word in ["fullstack", "full-stack", "web app", "application"]
    ):
        return "Full-Stack"
    elif any(word in analysis_lower for word in ["mobile", "ios", "android", "app"]):
        return "Mobile"
    elif any(
        word in analysis_lower
        for word in ["data", "analytics", "ml", "ai", "machine learning"]
    ):
        return "Data/Analytics"
    else:
        return "General Development"


def _analyze_collaboration_need(analysis: str, team_size: int) -> str:
    """Analyze collaboration requirements."""
    if team_size <= 2:
        return "Low"
    elif team_size <= 4:
        return "Medium"
    else:
        return "High"


def _analyze_quality_requirements(analysis: str) -> str:
    """Analyze quality requirements from description."""
    analysis_lower = analysis.lower()
    if any(
        word in analysis_lower
        for word in ["security", "secure", "critical", "production", "enterprise"]
    ):
        return "High"
    elif any(
        word in analysis_lower for word in ["prototype", "poc", "experiment", "quick"]
    ):
        return "Low"
    else:
        return "Medium"


def _analyze_innovation_need(analysis: str) -> str:
    """Analyze innovation requirements."""
    analysis_lower = analysis.lower()
    if any(
        word in analysis_lower
        for word in ["innovative", "creative", "novel", "research", "experimental"]
    ):
        return "High"
    elif any(
        word in analysis_lower
        for word in ["standard", "typical", "conventional", "maintenance"]
    ):
        return "Low"
    else:
        return "Medium"


def _generate_strategy_recommendation(factors: Dict) -> str:
    """Generate strategy recommendation based on analysis factors."""
    team_size = factors["team_size"]
    complexity = factors["complexity"]
    quality_req = factors["quality_requirements"]
    innovation_need = factors["innovation_need"]

    # High quality requirements suggest Red Team
    if quality_req == "High":
        return "Red Team Strategy: High quality requirements indicate need for adversarial testing and security focus"

    # High innovation need suggests Parallel Divergent
    elif innovation_need == "High":
        return "Parallel Divergent Strategy: High innovation need benefits from multiple independent approaches"

    # Large teams with high collaboration need suggest Mob Programming
    elif team_size >= 4 and factors["collaboration_need"] == "High":
        return "Mob Programming Strategy: Large team with high collaboration need benefits from shared knowledge"

    # Medium teams with medium complexity suggest Parallel Divergent
    elif team_size >= 3 and complexity in ["medium", "complex"]:
        return "Parallel Divergent Strategy: Multiple agents can explore different approaches to complex problems"

    # Default to Mob Programming for collaboration
    else:
        return "Mob Programming Strategy: Collaborative approach suitable for most development scenarios"


def _generate_implementation_guidance(recommendation: str) -> str:
    """Generate implementation guidance for recommended strategy."""
    strategy_name = recommendation.split(":")[0].strip()

    if "Red Team" in strategy_name:
        return """
### Red Team Implementation:
1. Divide team into blue team (builders) and red team (attackers)
2. Blue team builds secure implementation
3. Red team attacks and finds vulnerabilities
4. Iterate until security standards are met
5. Use `initialize_red_team(task, blue_size, red_size)` to begin
"""
    elif "Parallel Divergent" in strategy_name:
        return """
### Parallel Divergent Implementation:
1. Each agent works independently on the same problem
2. No coordination during divergent phase
3. Agents converge to review and synthesize solutions
4. Best elements from all solutions are combined
5. Use `initialize_parallel_divergent(task, agent_count)` to begin
"""
    elif "Mob Programming" in strategy_name:
        return """
### Mob Programming Implementation:
1. All agents work together on same code
2. Rotate driver and navigator roles every 15 minutes
3. Continuous collaboration and knowledge sharing
4. High code quality through group review
5. Use `initialize_mob_programming(task, agent_count)` to begin
"""
    else:
        return "### Implementation guidance not available for this strategy."


def _generate_alternative_strategies(factors: Dict) -> str:
    """Generate alternative strategy options."""
    return """
### Alternative Strategy Options:

**Parallel Divergent**: Good for complex problems requiring creative solutions
- Use when: Multiple valid approaches exist, innovation is important
- Team size: 3-4 agents optimal

**Red Team**: Excellent for security-critical applications
- Use when: Security is paramount, adversarial testing needed
- Team size: 4-6 agents (split into blue/red teams)

**Mob Programming**: Great for knowledge sharing and collaboration
- Use when: Team learning is important, code quality is critical
- Team size: 3-5 agents optimal

**Consider project requirements, team dynamics, and quality needs when making final decision.**
"""
