# AGOR Strategy Modules
"""
Modular strategy implementations for AGOR multi-agent coordination.

This package contains specialized modules for different aspects of multi-agent development:
- Multi-agent strategies (parallel, red team, mob programming)
- Project planning and coordination
- Team management and performance tracking
- Quality assurance and error optimization
- Workflow design and handoff coordination
"""

# Import all strategy functions for backward compatibility
from .multi_agent_strategies import (
    initialize_parallel_divergent,
    initialize_red_team, 
    initialize_mob_programming,
    select_strategy
)

from .project_coordination import (
    project_breakdown,
    create_team,
    design_workflow,
    generate_handoff_prompts
)

from .team_management import (
    manage_team
)

from .quality_assurance import (
    setup_quality_gates
)

from .error_optimization import (
    optimize_error_handling
)

# Export all functions
__all__ = [
    # Multi-agent strategies
    'initialize_parallel_divergent',
    'initialize_red_team',
    'initialize_mob_programming', 
    'select_strategy',
    
    # Project coordination
    'project_breakdown',
    'create_team',
    'design_workflow',
    'generate_handoff_prompts',
    
    # Team management
    'manage_team',
    
    # Quality assurance
    'setup_quality_gates',
    
    # Error optimization
    'optimize_error_handling'
]
