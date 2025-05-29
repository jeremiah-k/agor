# AGOR Strategy Modules
"""
Modular strategy implementations for AGOR multi-agent coordination.

This package contains specialized modules for different aspects of multi-agent development:
- Multi-agent strategies (parallel, red team, mob programming)
- Project planning and coordination
- Team management and performance tracking
- Quality assurance and error optimization
- Workflow design and snapshot coordination
"""

from .mob_programming import MobProgrammingProtocol

# Import strategy protocol classes
from .parallel_divergent import ParallelDivergentProtocol
from .red_team import RedTeamProtocol

# Import utility functions that exist
try:
    from .error_optimization import optimize_error_handling
except ImportError:
    optimize_error_handling = None

try:
    from .multi_agent_strategies import (
        initialize_mob_programming,
        initialize_parallel_divergent,
        initialize_red_team,
        select_strategy,
    )
except ImportError:
    initialize_mob_programming = None
    initialize_parallel_divergent = None
    initialize_red_team = None
    select_strategy = None

try:
    from .team_management import manage_team
except ImportError:
    manage_team = None

try:
    from .dependency_planning import plan_dependencies
except ImportError:
    plan_dependencies = None

try:
    from .risk_planning import plan_risks
except ImportError:
    plan_risks = None

try:
    from .quality_gates import setup_quality_gates
except ImportError:
    setup_quality_gates = None

# Export all available functions and classes
__all__ = [
    # Strategy protocol classes
    "ParallelDivergentProtocol",
    "RedTeamProtocol",
    "MobProgrammingProtocol",
    # Utility functions (if available)
    "optimize_error_handling",
    "initialize_parallel_divergent",
    "initialize_red_team",
    "initialize_mob_programming",
    "select_strategy",
    "manage_team",
    "setup_quality_gates",
    "plan_dependencies",
    "plan_risks",
]
