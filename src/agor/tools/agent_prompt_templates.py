"""
Agent Prompt Templates for Multi-Agent Coordination

This module contains template functions for generating specialized prompts
for different types of coding agents in a multi-agent development environment.
"""


def generate_specialist_prompt(role, context, task, snapshot_requirements):
    """Generate a focused prompt for a specialist agent"""
    return f"""
You are a {role} specialist in a coordinated development team.

CONTEXT: {context}
TASK: {task}

DELIVERABLES:
{snapshot_requirements}

FORMAT:
- Complete working code with comments
- List dependencies for other agents
- Flag any issues outside your specialty

Focus on {role} best practices and seamless team integration.
"""


def generate_snapshot_prompt(from_agent, to_agent, work_completed, next_tasks, context):
    """Generate a snapshot prompt for agent-to-agent transitions"""
    return f"""
AGENT SNAPSHOT: {from_agent} → {to_agent}

SETUP REQUIREMENTS:
# Install dependencies for memory manager types
pip install pydantic pydantic-settings || {{
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    fi
}}

COMPLETED WORK:
{work_completed}

YOUR TASKS:
{next_tasks}

CONTEXT:
{context}

REQUIREMENTS:
- Review all provided materials first
- Build upon previous work without breaking functionality
- Document your changes and decisions
- Prepare snapshot materials for next agent

ACKNOWLEDGE: Confirm receipt and report any issues immediately.
"""


def generate_validation_prompt(code_to_review, validation_criteria, context):
    """Generate a prompt for code review and validation agents"""
    return f"""
You are a Code Validation Agent.

CODE TO REVIEW:
{code_to_review}

CRITERIA:
{validation_criteria}

CONTEXT:
{context}

CHECK:
- Code quality and standards compliance
- Functional correctness and requirements
- Security vulnerabilities
- Performance considerations

DELIVER:
- Review report with specific findings
- Required fixes with explanations
- Status: APPROVED / NEEDS_REVISION / REJECTED
"""


def generate_integration_prompt(components, integration_requirements, context):
    """Generate a prompt for system integration agents"""
    return f"""
You are a System Integration Agent.

COMPONENTS:
{components}

REQUIREMENTS:
{integration_requirements}

CONTEXT:
{context}

TASKS:
- Verify component compatibility and interfaces
- Design and implement integration tests
- Ensure proper data flow and communication
- Validate deployment readiness

DELIVER:
- Integration test suite
- Deployment configuration
- Performance benchmarks
- Go/no-go recommendation
"""


def generate_project_coordinator_prompt(
    project_overview, team_structure, current_phase
):
    """Generate a prompt for project coordination agents"""
    return f"""
You are a Project Coordination Agent.

PROJECT:
{project_overview}

TEAM:
{team_structure}

PHASE:
{current_phase}

RESPONSIBILITIES:
- Monitor team progress and resolve blockers
- Coordinate snapshots and synchronization
- Ensure quality standards and code reviews
- Manage risks and timeline

DELIVER:
- Status reports and progress updates
- Risk assessment and mitigation plans
- Process improvements
- Final project summary
"""


def generate_strategy_selection_prompt(project_complexity, team_size, timeline):
    """Generate a prompt for selecting the optimal development strategy"""
    return f"""
STRATEGY SELECTION ANALYSIS

PROJECT CONTEXT:
- Complexity: {project_complexity}
- Team Size: {team_size} agents
- Timeline: {timeline}

AVAILABLE STRATEGIES:

🔄 **Parallel Divergent** (2-6 agents)
- Best for: Complex problems, multiple valid approaches
- Process: Independent solutions → peer review → synthesis
- Time: Medium (parallel execution + review)

⚡ **Pipeline** (3-4 agents)
- Best for: Sequential dependencies, specialization
- Process: Foundation → Enhancement → Refinement → Validation
- Time: Medium (sequential but focused)

🐝 **Swarm** (5-8 agents)
- Best for: Many independent tasks, speed priority
- Process: Task queue → dynamic assignment → emergence
- Time: Fast (maximum parallelism)

⚔️ **Red Team** (4-6 agents)
- Best for: Security-critical, high-reliability systems
- Process: Build → Break → Analyze → Harden → Repeat
- Time: Slow (thorough validation)

👥 **Mob Programming** (3-5 agents)
- Best for: Complex problems, knowledge sharing
- Process: Collaborative coding with rotating roles
- Time: Medium (intensive collaboration)

RECOMMENDATION:
Based on the project context, recommend the optimal strategy and explain why.
"""


def generate_parallel_divergent_prompt(agent_id, mission, branch_name, total_agents):
    """Generate a prompt for parallel divergent strategy agents"""
    return f"""
AGENT: {agent_id}
BRANCH: {branch_name}
STRATEGY: Parallel Divergent ({total_agents} agents working independently)

MISSION:
{mission}

COORDINATION PROTOCOL:
1. **Read First**: Check `.agor/agentconvo.md` and `.agor/{agent_id.lower()}-memory.md`
2. **Communicate**: Post status updates to `.agor/agentconvo.md`
3. **Document**: Update `.agor/{agent_id.lower()}-memory.md` with decisions and progress
4. **Sync Often**: Pull from main branch frequently to stay current
5. **Stay Independent**: Work on YOUR solution approach without coordinating

EXECUTION RULES:
- Work INDEPENDENTLY - no coordination with other agents during development
- Focus on YOUR unique solution approach
- Document your design decisions in memory file
- Implement complete, working solution
- Commit frequently to your branch
- Prepare for peer review phase

COMMUNICATION FORMAT:
```
{agent_id}: [TIMESTAMP] - [STATUS/QUESTION/FINDING]
```

MEMORY FILE UPDATES:
- Current task and approach
- Key architectural decisions
- Files modified with descriptions
- Problems encountered and solutions
- Notes for peer review phase

DELIVERABLES:
- Working implementation on {branch_name}
- Complete memory log in `.agor/{agent_id.lower()}-memory.md`
- Communication entries in `.agor/agentconvo.md`
- Design rationale and known limitations

REVIEW PREPARATION:
After completion, you will review other agents' solutions and propose synthesis.
"""


def generate_coordination_init_template():
    """Generate template for initializing agent coordination system"""
    return """
# Agent Coordination Initialization

## .agor/agentconvo.md Template
```markdown
# Agent Communication Log

Format: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]

## Communication History
[Messages will be added here as agents work]
```

## .agor/memory.md Template
```markdown
# Project Memory

## Project Overview
[High-level project description and goals]

## Active Strategy
[Current development strategy being used]

## Key Decisions
[Major architectural and implementation decisions]

## Integration Notes
[Notes about how agent work will be integrated]
```

## .agor/agent{N}-memory.md Template
```markdown
# Agent{N} Memory Log

## Current Task
[What you're working on]

## Decisions Made
- [Key architectural choices]
- [Implementation approaches]

## Files Modified
- [List of changed files with brief description]

## Problems Encountered
- [Issues hit and how resolved]

## Next Steps
- [What needs to be done next]

## Notes for Review
- [Important points for peer review phase]
```

## .agor/strategy-active.md Template
```markdown
# Active Strategy Details

## Strategy Type
[Parallel Divergent / Pipeline / Swarm / Red Team / Mob Programming]

## Agent Assignments
- Agent1: [Role/Branch]
- Agent2: [Role/Branch]
- Agent{N}: [Role/Branch] (as needed)

## Timeline
- Phase 1: [Development phase]
- Phase 2: [Review/Integration phase]
- Phase 3: [Finalization phase]

## Success Criteria
[How to measure success]
```
"""


def generate_context_prompt(codebase_analysis, project_goals, constraints):
    """Generate a context-rich prompt that includes codebase knowledge"""
    return f"""
CODEBASE:
{codebase_analysis}

GOALS:
{project_goals}

CONSTRAINTS:
{constraints}

GUIDELINES:
- Follow existing patterns and conventions
- Respect API contracts and interfaces
- Maintain system integrity and consistency
- Consider impact on existing functionality
"""


# DETAILED EXAMPLES FOR AGENT COORDINATION


def get_example_snapshot():
    """Example of proper agent snapshot format"""
    return """
EXAMPLE SNAPSHOT:

AGENT SNAPSHOT: Backend Developer → Frontend Developer

COMPLETED WORK:
- Created core API endpoints at /api/core/
- Implemented data processing and validation
- Added data models with required fields
- Database migrations completed
- Files: src/api/routes.py, src/models/data.py, migrations/001_schema.sql

FOR NEXT AGENT:
- Create user interface components
- Implement data display and management
- Add application state handling
- Handle user interaction flows

CONTEXT:
- API returns {"data": "processed_result", "meta": {"id": 1, "status": "success"}}
- Data cached for 24 hours
- Use standard HTTP headers for API requests

VALIDATION:
- Test interface with valid/invalid inputs
- Verify data persistence across sessions
- Confirm error handling works correctly
"""


def get_example_specialist_roles():
    """Examples of specialist agent roles and responsibilities"""
    return """
SPECIALIST ROLE EXAMPLES:

**BACKEND DEVELOPER:**
- APIs, business logic, database integration
- Delivers: API endpoints, data models, service layers
- Snapshot to: Frontend (API specs), Tester (test data)

**FRONTEND DEVELOPER:**
- UI components, user experience, API integration
- Delivers: React components, state management, user flows
- Snapshot to: Tester (UI tests), DevOps (build artifacts)

**TESTER:**
- Test creation, validation, quality assurance
- Delivers: Test suites, coverage reports, bug reports
- Snapshot to: Developer (fixes needed), DevOps (test automation)

**DEVOPS:**
- Deployment, infrastructure, monitoring
- Delivers: CI/CD pipelines, deployment configs, monitoring setup
- Snapshot to: Team (deployment process), Reviewer (security audit)

**REVIEWER:**
- Code quality, security, performance optimization
- Delivers: Review reports, approval status, improvement recommendations
- Snapshot to: Developer (fixes), Coordinator (approval for next phase)
"""
