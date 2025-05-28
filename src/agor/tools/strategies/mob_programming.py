"""
Mob Programming Strategy Implementation for AGOR.

This strategy involves all agents working together on the same code with
rotating driver/navigator roles for maximum collaboration and knowledge sharing.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

# Dual-mode importing for bundle and package compatibility
try:
    from ..project_planning_templates import generate_mob_programming_strategy
except ImportError:
    # Bundle-mode fallback
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from project_planning_templates import generate_mob_programming_strategy


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


def initialize_mob_programming(task: str, agent_count: int = 4) -> str:
    """Initialize Mob Programming strategy."""
    protocol = MobProgrammingProtocol()
    return protocol.initialize_strategy(task, agent_count)
