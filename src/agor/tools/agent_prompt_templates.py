"""
Agent Prompt Templates for Multi-Agent Coordination

This module contains template functions for generating specialized prompts
for different types of coding agents in a multi-agent development environment.
"""


def generate_specialist_prompt(role, context, task, handoff_requirements):
    """Generate a focused prompt for a specialist agent"""
    return f"""
You are a {role} specialist in a coordinated development team.

CONTEXT: {context}
TASK: {task}

DELIVERABLES:
{handoff_requirements}

FORMAT:
- Complete working code with comments
- List dependencies for other agents
- Flag any issues outside your specialty

Focus on {role} best practices and seamless team integration.
"""


def generate_handoff_prompt(from_agent, to_agent, work_completed, next_tasks, context):
    """Generate a handoff prompt for agent-to-agent transitions"""
    return f"""
AGENT HANDOFF: {from_agent} → {to_agent}

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
- Prepare handoff materials for next agent

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
- Coordinate handoffs and synchronization
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

🔄 **Parallel Divergent** (3-5 agents)
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


def generate_parallel_divergent_prompt(agent_id, mission, branch_name):
    """Generate a prompt for parallel divergent strategy agents"""
    return f"""
PARALLEL DIVERGENT AGENT: {agent_id}

MISSION:
{mission}

YOUR BRANCH: {branch_name}

EXECUTION RULES:
- Work INDEPENDENTLY - no coordination with other agents
- Focus on YOUR solution approach
- Document your design decisions
- Implement complete, working solution
- Prepare for peer review phase

DELIVERABLES:
- Working implementation
- Design rationale document
- Test coverage
- Known limitations

REVIEW PREPARATION:
After completion, you will review other agents' solutions and propose synthesis.
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


def get_example_handoff():
    """Example of proper agent handoff format"""
    return """
EXAMPLE HANDOFF:

AGENT HANDOFF: Backend Developer → Frontend Developer

COMPLETED WORK:
- Created user authentication API at /api/auth/login
- Implemented JWT token generation and validation
- Added user model with email/password fields
- Database migrations completed
- Files: src/auth/routes.py, src/models/user.py, migrations/001_users.sql

FOR NEXT AGENT:
- Create login form component
- Implement token storage and management
- Add authentication state to app
- Handle login/logout user flows

CONTEXT:
- API returns {"token": "jwt_string", "user": {"id": 1, "email": "user@example.com"}}
- Token expires in 24 hours
- Use Authorization: Bearer <token> header for authenticated requests

VALIDATION:
- Test login form with valid/invalid credentials
- Verify token persistence across browser sessions
- Confirm protected routes redirect to login when unauthenticated
"""


def get_example_specialist_roles():
    """Examples of specialist agent roles and responsibilities"""
    return """
SPECIALIST ROLE EXAMPLES:

**BACKEND DEVELOPER:**
- APIs, business logic, database integration
- Delivers: API endpoints, data models, service layers
- Handoff to: Frontend (API specs), Tester (test data)

**FRONTEND DEVELOPER:**
- UI components, user experience, API integration
- Delivers: React components, state management, user flows
- Handoff to: Tester (UI tests), DevOps (build artifacts)

**TESTER:**
- Test creation, validation, quality assurance
- Delivers: Test suites, coverage reports, bug reports
- Handoff to: Developer (fixes needed), DevOps (test automation)

**DEVOPS:**
- Deployment, infrastructure, monitoring
- Delivers: CI/CD pipelines, deployment configs, monitoring setup
- Handoff to: Team (deployment process), Reviewer (security audit)

**REVIEWER:**
- Code quality, security, performance optimization
- Delivers: Review reports, approval status, improvement recommendations
- Handoff to: Developer (fixes), Coordinator (approval for next phase)
"""
