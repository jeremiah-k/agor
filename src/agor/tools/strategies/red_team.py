"""
Red Team Strategy Implementation for AGOR.

This strategy involves adversarial testing with a blue team (builders) and
red team (attackers) working in cycles to create secure, battle-tested code.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

# Dual-mode importing for bundle and package compatibility
try:
    from ..project_planning_templates import generate_red_team_strategy
except ImportError:
    # Bundle-mode fallback
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from project_planning_templates import generate_red_team_strategy


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


def initialize_red_team(
    task: str, blue_team_size: int = 3, red_team_size: int = 3
) -> str:
    """Initialize Red Team strategy."""
    protocol = RedTeamProtocol()
    return protocol.initialize_strategy(task, blue_team_size, red_team_size)
