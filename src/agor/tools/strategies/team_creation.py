"""
Team Creation Strategy Implementation for AGOR.

This module provides intelligent team structure generation and coordination setup
based on project requirements, team size, and project type.
"""

from datetime import datetime
from pathlib import Path


def create_team(
    project_description: str,
    team_size: int = 4,
    project_type: str = "web_app",
    complexity: str = "medium",
) -> str:
    """Create team structure and coordination setup (ct hotkey)."""

    # Generate team creation based on parameters
    team_details = f"""
## TEAM CREATION IMPLEMENTATION

### Project: {project_description}
### Team Size: {team_size} agents
### Project Type: {project_type}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## INTELLIGENT TEAM STRUCTURE

{_generate_team_structure(team_size, project_type, complexity)}

## ROLE ASSIGNMENTS AND RESPONSIBILITIES

{_generate_role_assignments(team_size, project_type)}

## TEAM COORDINATION SETUP

{_generate_coordination_setup(team_size, project_type)}

## COMMUNICATION PROTOCOLS

### Daily Coordination:
```
TEAM_STANDUP: [timestamp] - Daily team status and coordination
ROLE_UPDATE: [agent-id] - [role] - [current-task] - [status] - [timestamp]
COLLABORATION_REQUEST: [requesting-agent] - [target-agent] - [help-type] - [timestamp]
TEAM_DECISION: [decision] - [rationale] - [affected-agents] - [timestamp]
```

### Weekly Coordination:
```
TEAM_RETROSPECTIVE: [week] - [what-worked] - [improvements] - [action-items]
ROLE_ROTATION: [old-assignments] → [new-assignments] - [reason] - [timestamp]
TEAM_METRICS: [velocity] - [quality] - [collaboration-score] - [timestamp]
```

## TEAM PERFORMANCE FRAMEWORK

{_generate_performance_framework(team_size)}

## COORDINATION FILES SETUP

### Team Structure Files:
- `.agor/team-structure.md` - Complete team plan and role assignments
- `.agor/team-coordination.md` - Communication protocols and metrics
- `.agor/agent[1-N]-memory.md` - Individual agent memory templates

### Communication Files:
- `.agor/team-standup.md` - Daily standup coordination
- `.agor/team-decisions.md` - Team decision log
- `.agor/team-metrics.md` - Performance tracking

## NEXT STEPS

1. **Review Team Structure**: Validate role assignments and responsibilities
2. **Initialize Agent Memory Files**: Create individual agent coordination files
3. **Setup Communication Protocols**: Establish daily and weekly coordination
4. **Begin Team Coordination**: Start with team standup and role confirmation
5. **Monitor Team Performance**: Track metrics and optimize team dynamics
"""

    # Save to team structure file
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)
    team_file = agor_dir / "team-structure.md"
    team_file.write_text(team_details)

    # Create team coordination files
    _create_team_coordination_files(team_size, project_type, project_description)

    # Create individual agent memory files
    _create_agent_memory_files(team_size, project_type)

    return f"""✅ Team Created Successfully

**Project**: {project_description}
**Team Size**: {team_size} agents
**Project Type**: {project_type}
**Complexity**: {complexity}

**Team Structure**:
{_get_team_summary(team_size, project_type, complexity)}

**Team Features**:
- Intelligent role assignment based on project type and team size
- Complete coordination protocols for daily and weekly sync
- Individual agent memory files for role-specific coordination
- Performance tracking and team optimization frameworks
- Communication protocols for effective collaboration

**Files Created**:
- `.agor/team-structure.md` - Complete team plan and role assignments
- `.agor/team-coordination.md` - Communication protocols and metrics
- `.agor/agent[1-{team_size}]-memory.md` - Individual agent memory templates
- `.agor/team-standup.md` - Daily coordination tracking
- `.agor/team-decisions.md` - Team decision log

**Next Steps**:
1. Review and confirm role assignments
2. Initialize daily team coordination
3. Begin project work with established team structure
4. Monitor team performance and adjust as needed

**Ready for coordinated team development!**
"""


def _generate_team_structure(team_size: int, project_type: str, complexity: str) -> str:
    """Generate team structure based on size and project type."""

    if team_size <= 3:
        return _generate_small_team_structure(team_size, project_type)
    elif team_size <= 6:
        return _generate_medium_team_structure(team_size, project_type)
    else:
        return _generate_large_team_structure(team_size, project_type)


def _generate_small_team_structure(team_size: int, project_type: str) -> str:
    """Generate structure for small teams (2-3 agents)."""
    if project_type == "api":
        return """
### Small Team Structure (API Focus)

**Team Composition**: Lean, cross-functional team with shared responsibilities

**Agent 1: Lead Developer**
- Primary Role: Technical leadership and architecture
- Secondary Role: Backend development and API design
- Responsibilities: System design, code review, technical decisions

**Agent 2: Full-Stack Developer**
- Primary Role: Feature implementation and integration
- Secondary Role: Testing and quality assurance
- Responsibilities: API endpoints, database integration, testing

**Agent 3: DevOps/QA Engineer** (if 3 agents)
- Primary Role: Deployment and quality assurance
- Secondary Role: Testing and monitoring
- Responsibilities: CI/CD, testing, deployment, monitoring

**Team Dynamics**:
- High collaboration and knowledge sharing
- Shared ownership of all components
- Flexible role boundaries based on needs
- Direct communication and quick decision making
"""
    elif project_type == "frontend":
        return """
### Small Team Structure (Frontend Focus)

**Team Composition**: UI-focused team with design and development expertise

**Agent 1: UI/UX Lead**
- Primary Role: Design implementation and user experience
- Secondary Role: Component architecture
- Responsibilities: Design system, user interface, accessibility

**Agent 2: Frontend Developer**
- Primary Role: Application logic and state management
- Secondary Role: API integration
- Responsibilities: Business logic, data flow, performance

**Agent 3: QA/Integration Engineer** (if 3 agents)
- Primary Role: Testing and quality assurance
- Secondary Role: Backend integration
- Responsibilities: Testing, API integration, deployment

**Team Dynamics**:
- Design-driven development approach
- Close collaboration on user experience
- Shared responsibility for code quality
- Rapid prototyping and iteration
"""
    else:  # web_app or generic
        return """
### Small Team Structure (Full-Stack)

**Team Composition**: Versatile team covering all aspects of development

**Agent 1: Technical Lead**
- Primary Role: Architecture and coordination
- Secondary Role: Full-stack development
- Responsibilities: System design, team coordination, code review

**Agent 2: Full-Stack Developer**
- Primary Role: Feature development
- Secondary Role: Testing and integration
- Responsibilities: Frontend/backend development, feature implementation

**Agent 3: QA/DevOps Engineer** (if 3 agents)
- Primary Role: Quality assurance and deployment
- Secondary Role: Testing and monitoring
- Responsibilities: Testing strategy, CI/CD, deployment, monitoring

**Team Dynamics**:
- Everyone contributes to all layers of the stack
- High flexibility and adaptability
- Shared knowledge across all technologies
- Collaborative problem-solving approach
"""


def _generate_medium_team_structure(team_size: int, project_type: str) -> str:
    """Generate structure for medium teams (4-6 agents)."""
    if project_type == "api":
        return """
### Medium Team Structure (API Focus)

**Team Composition**: Specialized roles with clear ownership areas

**Agent 1: Technical Lead**
- Primary Role: Architecture and technical leadership
- Responsibilities: System design, technical decisions, code review coordination
- Focus Areas: API architecture, database design, performance optimization

**Agent 2: Backend Developer**
- Primary Role: Core API development
- Responsibilities: Endpoint implementation, business logic, data validation
- Focus Areas: API endpoints, authentication, business rules

**Agent 3: Database Engineer**
- Primary Role: Data layer and optimization
- Responsibilities: Database design, query optimization, data migration
- Focus Areas: Database schema, performance tuning, data integrity

**Agent 4: Security Engineer**
- Primary Role: Security implementation and testing
- Responsibilities: Authentication, authorization, security testing
- Focus Areas: API security, vulnerability assessment, compliance

**Agent 5: QA Engineer** (if 5+ agents)
- Primary Role: Testing and quality assurance
- Responsibilities: Test automation, API testing, integration testing
- Focus Areas: Test strategy, quality metrics, bug tracking

**Agent 6: DevOps Engineer** (if 6 agents)
- Primary Role: Infrastructure and deployment
- Responsibilities: CI/CD, monitoring, scalability, deployment
- Focus Areas: Infrastructure, automation, monitoring, performance

**Team Dynamics**:
- Clear specialization with defined ownership
- Regular cross-team collaboration and knowledge sharing
- Structured code review and quality processes
- Coordinated release and deployment cycles
"""
    elif project_type == "web_app":
        return """
### Medium Team Structure (Web Application)

**Team Composition**: Frontend/Backend specialization with support roles

**Agent 1: Technical Lead**
- Primary Role: Overall architecture and coordination
- Responsibilities: System design, team coordination, technical decisions
- Focus Areas: Architecture, integration, team leadership

**Agent 2: Frontend Lead**
- Primary Role: Frontend architecture and development
- Responsibilities: UI/UX implementation, frontend architecture, component design
- Focus Areas: User interface, user experience, frontend performance

**Agent 3: Backend Lead**
- Primary Role: Backend architecture and API development
- Responsibilities: API design, business logic, database integration
- Focus Areas: Server-side logic, API design, data management

**Agent 4: Full-Stack Developer**
- Primary Role: Feature implementation across stack
- Responsibilities: Feature development, integration work, bug fixes
- Focus Areas: End-to-end features, integration, versatile development

**Agent 5: QA Engineer** (if 5+ agents)
- Primary Role: Testing and quality assurance
- Responsibilities: Test automation, user testing, quality metrics
- Focus Areas: Testing strategy, quality assurance, user acceptance

**Agent 6: DevOps Engineer** (if 6 agents)
- Primary Role: Infrastructure and deployment
- Responsibilities: CI/CD, monitoring, deployment, scalability
- Focus Areas: Infrastructure, automation, performance, reliability

**Team Dynamics**:
- Frontend/Backend coordination with clear interfaces
- Regular integration and testing cycles
- Collaborative feature development
- Shared responsibility for user experience
"""
    else:  # mobile, data, security, generic
        return """
### Medium Team Structure (Specialized Project)

**Team Composition**: Role-based specialization with project focus

**Agent 1: Project Lead**
- Primary Role: Project coordination and architecture
- Responsibilities: Project planning, technical leadership, stakeholder communication
- Focus Areas: Project management, architecture, coordination

**Agent 2: Senior Developer**
- Primary Role: Core development and technical expertise
- Responsibilities: Complex feature implementation, technical problem solving
- Focus Areas: Core functionality, technical challenges, mentoring

**Agent 3: Developer**
- Primary Role: Feature development and implementation
- Responsibilities: Feature implementation, testing, documentation
- Focus Areas: Feature development, code quality, testing

**Agent 4: Specialist** (Domain-specific)
- Primary Role: Domain expertise and specialized development
- Responsibilities: Specialized features, domain knowledge, technical guidance
- Focus Areas: Domain-specific functionality, specialized tools, expertise

**Agent 5: QA Engineer** (if 5+ agents)
- Primary Role: Quality assurance and testing
- Responsibilities: Testing strategy, quality metrics, user validation
- Focus Areas: Quality assurance, testing automation, user experience

**Agent 6: Support Engineer** (if 6 agents)
- Primary Role: Infrastructure, deployment, and support
- Responsibilities: Environment setup, deployment, monitoring, support
- Focus Areas: Infrastructure, deployment, monitoring, maintenance

**Team Dynamics**:
- Expertise-driven development with knowledge sharing
- Collaborative problem-solving and decision making
- Regular knowledge transfer and cross-training
- Balanced workload with specialized contributions
"""


def _generate_large_team_structure(team_size: int, project_type: str) -> str:
    """Generate structure for large teams (7+ agents)."""
    return f"""
### Large Team Structure ({team_size} Agents)

**Team Composition**: Multi-track development with leadership hierarchy

**Leadership Track**:
**Agent 1: Project Manager**
- Primary Role: Project coordination and management
- Responsibilities: Project planning, stakeholder communication, resource allocation
- Focus Areas: Project management, coordination, communication

**Agent 2: Technical Architect**
- Primary Role: Technical leadership and architecture
- Responsibilities: System architecture, technical decisions, code review oversight
- Focus Areas: Architecture, technical strategy, quality standards

**Development Tracks**:
**Agent 3: Frontend Lead**
- Primary Role: Frontend team leadership
- Responsibilities: Frontend architecture, UI/UX coordination, frontend team management
- Focus Areas: Frontend development, user experience, team coordination

**Agent 4-5: Frontend Developers**
- Primary Role: Frontend development and implementation
- Responsibilities: UI implementation, component development, frontend testing
- Focus Areas: User interface, components, frontend functionality

**Agent 6: Backend Lead**
- Primary Role: Backend team leadership
- Responsibilities: Backend architecture, API design, backend team management
- Focus Areas: Backend development, API design, data management

**Agent 7-8: Backend Developers** (if 8+ agents)
- Primary Role: Backend development and implementation
- Responsibilities: API implementation, business logic, database integration
- Focus Areas: Server-side logic, APIs, data processing

**Support Track**:
**Agent {team_size-1}: QA Lead**
- Primary Role: Quality assurance leadership
- Responsibilities: Testing strategy, quality metrics, QA process management
- Focus Areas: Quality assurance, testing automation, quality standards

**Agent {team_size}: DevOps Engineer**
- Primary Role: Infrastructure and deployment
- Responsibilities: CI/CD, monitoring, scalability, deployment automation
- Focus Areas: Infrastructure, automation, monitoring, performance

**Team Dynamics**:
- Clear hierarchy with defined leadership roles
- Sub-team coordination with regular sync meetings
- Structured communication and decision-making processes
- Specialized tracks with cross-team collaboration
- Regular all-hands meetings and coordination sessions
"""


def _generate_role_assignments(team_size: int, project_type: str) -> str:
    """Generate detailed role assignments and responsibilities."""
    return """
### Detailed Role Assignments

#### Role Definition Framework:
Each agent has clearly defined primary and secondary responsibilities to ensure comprehensive project coverage while maintaining specialization.

#### Responsibility Matrix:
- **Primary Responsibilities**: Core duties and ownership areas
- **Secondary Responsibilities**: Supporting duties and backup coverage
- **Collaboration Points**: Key interaction areas with other team members
- **Decision Authority**: Areas where agent has final decision-making authority

#### Role Rotation Strategy:
- **Weekly Rotation**: Minor role adjustments based on project needs
- **Sprint Rotation**: Role refinement based on sprint retrospectives
- **Project Phase Rotation**: Role evolution as project progresses through phases
- **Skill Development**: Opportunities for agents to learn new roles

#### Cross-Training Plan:
- **Knowledge Sharing Sessions**: Weekly technical knowledge sharing
- **Pair Programming**: Collaborative development for knowledge transfer
- **Code Review Participation**: All agents participate in code reviews
- **Documentation Responsibility**: Each agent documents their domain expertise

#### Escalation Procedures:
- **Technical Issues**: Technical Lead → Project Manager → External consultation
- **Resource Conflicts**: Project Manager → Stakeholder communication
- **Quality Issues**: QA Lead → Technical Lead → Process improvement
- **Timeline Issues**: Project Manager → Scope adjustment → Stakeholder communication
"""


def _generate_coordination_setup(team_size: int, project_type: str) -> str:
    """Generate coordination setup and protocols."""
    return """
### Team Coordination Setup

#### Daily Coordination (15 minutes):
- **Time**: 9:00 AM daily standup
- **Format**: Round-robin status updates
- **Structure**: Yesterday's progress, today's plan, blockers/help needed
- **Documentation**: Updates logged in team-standup.md

#### Weekly Coordination (30 minutes):
- **Time**: Friday afternoon retrospective
- **Format**: Structured retrospective with action items
- **Structure**: What worked well, what could improve, action items for next week
- **Documentation**: Updates logged in team-retrospective.md

#### Sprint Coordination (60 minutes):
- **Time**: Beginning and end of each sprint
- **Format**: Sprint planning and review
- **Structure**: Sprint goals, task assignment, retrospective, next sprint planning
- **Documentation**: Updates logged in sprint-coordination.md

#### Communication Channels:
- **Primary**: .agor/agentconvo.md for real-time coordination
- **Status**: .agor/team-standup.md for daily status tracking
- **Decisions**: .agor/team-decisions.md for important decisions
- **Metrics**: .agor/team-metrics.md for performance tracking

#### Decision-Making Framework:
- **Individual Decisions**: Within agent's primary responsibility area
- **Team Decisions**: Require team discussion and consensus
- **Technical Decisions**: Technical Lead has final authority
- **Project Decisions**: Project Manager has final authority

#### Conflict Resolution:
- **Step 1**: Direct communication between involved agents
- **Step 2**: Team discussion and mediation
- **Step 3**: Leadership intervention (Technical Lead or Project Manager)
- **Step 4**: External mediation if needed
"""


def _generate_performance_framework(team_size: int) -> str:
    """Generate team performance tracking framework."""
    return """
### Team Performance Framework

#### Individual Performance Metrics:
- **Productivity**: Tasks completed per sprint, code contributions
- **Quality**: Code review scores, bug rates, test coverage
- **Collaboration**: Help provided to others, knowledge sharing, communication
- **Growth**: Skill development, learning initiatives, cross-training participation

#### Team Performance Metrics:
- **Velocity**: Story points or tasks completed per sprint
- **Quality**: Overall code quality, bug rates, customer satisfaction
- **Collaboration**: Team communication effectiveness, knowledge sharing
- **Delivery**: On-time delivery, scope completion, stakeholder satisfaction

#### Performance Review Cycle:
- **Daily**: Quick performance check during standup
- **Weekly**: Performance discussion during retrospective
- **Sprint**: Comprehensive performance review and improvement planning
- **Monthly**: Individual performance coaching and development planning

#### Performance Improvement:
- **Skill Development**: Training opportunities and learning resources
- **Process Improvement**: Workflow optimization and tool enhancement
- **Team Building**: Activities to improve collaboration and communication
- **Individual Coaching**: One-on-one coaching and mentoring

#### Recognition and Rewards:
- **Daily Recognition**: Acknowledge good work during standups
- **Weekly Highlights**: Celebrate achievements during retrospectives
- **Sprint Awards**: Recognize outstanding contributions each sprint
- **Project Completion**: Celebrate project milestones and completion

#### Performance Issues:
- **Early Identification**: Monitor metrics and team feedback
- **Root Cause Analysis**: Understand underlying causes of performance issues
- **Improvement Plans**: Create specific, actionable improvement plans
- **Support and Resources**: Provide necessary support and resources
- **Follow-up**: Regular check-ins and progress monitoring
"""


def _create_team_coordination_files(
    team_size: int, project_type: str, project_description: str
):
    """Create team coordination files."""
    agor_dir = Path(".agor")

    # Team coordination file
    coordination_file = agor_dir / "team-coordination.md"
    coordination_content = f"""# Team Coordination

## Project: {project_description}
## Team Size: {team_size} agents
## Project Type: {project_type}
## Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Team Status
- **Team Health**: Green (all agents active and coordinated)
- **Communication**: Effective (daily standups and regular sync)
- **Productivity**: On track (meeting sprint goals)
- **Collaboration**: Strong (good knowledge sharing and support)

## Daily Standup Schedule
- **Time**: 9:00 AM daily
- **Duration**: 15 minutes
- **Format**: Round-robin status updates
- **Location**: .agor/agentconvo.md

## Weekly Retrospective Schedule
- **Time**: Friday 4:00 PM
- **Duration**: 30 minutes
- **Format**: Structured retrospective
- **Location**: .agor/team-retrospective.md

## Communication Protocols

### Status Updates
```
DAILY_STATUS: [agent-id] - [yesterday] - [today] - [blockers] - [timestamp]
```

### Help Requests
```
HELP_REQUEST: [requesting-agent] - [help-type] - [urgency] - [context] - [timestamp]
HELP_RESPONSE: [responding-agent] - [help-provided] - [outcome] - [timestamp]
```

### Team Decisions
```
TEAM_DECISION: [decision] - [rationale] - [affected-agents] - [timestamp]
```

## Team Metrics Tracking

### Current Sprint Metrics
- **Velocity**: [X story points/tasks per sprint]
- **Quality**: [X% code review pass rate]
- **Collaboration**: [X help requests resolved per week]
- **Delivery**: [X% on-time completion rate]

### Team Performance Trends
- **Week 1**: [Baseline metrics]
- **Week 2**: [Performance trends]
- **Week 3**: [Improvement areas]

## Action Items
- [ ] Complete team onboarding and role confirmation
- [ ] Establish daily standup routine
- [ ] Setup weekly retrospective process
- [ ] Begin sprint planning and execution

## Team Improvement Areas
- [Areas for improvement will be identified during retrospectives]

## Team Strengths
- [Team strengths will be documented as they emerge]
"""
    coordination_file.write_text(coordination_content)

    # Team standup file
    standup_file = agor_dir / "team-standup.md"
    standup_content = f"""# Daily Team Standup

## Team: {project_description}
## Standup Time: 9:00 AM Daily

## Standup Format
1. **Round-robin updates** (2 minutes per agent)
2. **Blocker discussion** (5 minutes)
3. **Coordination planning** (3 minutes)
4. **Action items** (5 minutes)

## Today's Standup - {datetime.now().strftime('%Y-%m-%d')}

### Agent Updates
{chr(10).join([f"**Agent{i}**:" + chr(10) + "- Yesterday: [What was accomplished]" + chr(10) + "- Today: [What is planned]" + chr(10) + "- Blockers: [Any blockers or help needed]" + chr(10) for i in range(1, team_size + 1)])}

### Team Blockers
- [No blockers currently identified]

### Coordination Needs
- [No special coordination needed today]

### Action Items
- [ ] [Action item 1]
- [ ] [Action item 2]

## Standup History

### Previous Standups
- [Standup history will be maintained here]

## Standup Metrics
- **Attendance**: {team_size}/{team_size} agents
- **Duration**: [X minutes]
- **Blockers Identified**: 0
- **Action Items Created**: 0
"""
    standup_file.write_text(standup_content)

    # Team decisions file
    decisions_file = agor_dir / "team-decisions.md"
    decisions_content = f"""# Team Decisions Log

## Project: {project_description}
## Team Size: {team_size} agents

## Decision Categories

### Technical Decisions
- Architecture choices
- Technology selections
- Design patterns
- Code standards

### Process Decisions
- Development workflow
- Communication protocols
- Quality standards
- Team coordination

### Project Decisions
- Scope changes
- Timeline adjustments
- Resource allocation
- Priority changes

## Decision Log

### {datetime.now().strftime('%Y-%m-%d')} - Team Formation
- **Decision**: Team structure and role assignments established
- **Rationale**: Based on project requirements and team size optimization
- **Impact**: All agents have clear roles and responsibilities
- **Status**: Implemented

## Decision Templates

### Technical Decision Template
```
**Date**: [YYYY-MM-DD]
**Decision**: [Brief description of decision]
**Context**: [Why this decision was needed]
**Options Considered**: [Alternative options that were considered]
**Decision Rationale**: [Why this option was chosen]
**Impact**: [How this affects the team and project]
**Implementation**: [How this will be implemented]
**Review Date**: [When this decision will be reviewed]
```

### Process Decision Template
```
**Date**: [YYYY-MM-DD]
**Decision**: [Brief description of process decision]
**Current Process**: [How things are currently done]
**New Process**: [How things will be done going forward]
**Rationale**: [Why this change is needed]
**Impact**: [How this affects team workflow]
**Implementation**: [Steps to implement the change]
**Success Metrics**: [How success will be measured]
```

## Decision Review Schedule
- **Weekly**: Review recent decisions during retrospective
- **Sprint**: Evaluate decision effectiveness during sprint review
- **Monthly**: Comprehensive decision audit and optimization
"""
    decisions_file.write_text(decisions_content)


def _create_agent_memory_files(team_size: int, project_type: str):
    """Create individual agent memory files."""
    agor_dir = Path(".agor")

    for i in range(1, team_size + 1):
        agent_id = f"agent{i}"
        memory_file = agor_dir / f"{agent_id}-memory.md"

        # Determine role based on team size and position
        role = _get_agent_role(i, team_size, project_type)

        memory_content = f"""# {agent_id.upper()} Memory File

## Agent Information
- **Agent ID**: {agent_id}
- **Role**: {role}
- **Team Size**: {team_size} agents
- **Project Type**: {project_type}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Assignment
- **Primary Role**: {role}
- **Current Task**: [To be assigned]
- **Status**: Ready for assignment
- **Priority**: [To be determined]

## Role Responsibilities
{_get_role_responsibilities(role, project_type)}

## Current Work
- **Active Tasks**: [No tasks currently assigned]
- **Completed Tasks**: [No tasks completed yet]
- **Blocked Tasks**: [No blocked tasks]
- **Next Tasks**: [Awaiting task assignment]

## Collaboration
- **Working With**: [Other agents I'm collaborating with]
- **Help Provided**: [Help I've provided to other agents]
- **Help Received**: [Help I've received from other agents]
- **Knowledge Shared**: [Knowledge I've shared with the team]

## Technical Notes
- **Decisions Made**: [Important technical decisions I've made]
- **Lessons Learned**: [Key insights and lessons from my work]
- **Best Practices**: [Best practices I've discovered or applied]
- **Challenges**: [Technical challenges I've encountered and how I solved them]

## Communication Log
- **Last Standup**: [Date and key points from last standup]
- **Recent Decisions**: [Recent team decisions that affect my work]
- **Action Items**: [Action items assigned to me]
- **Follow-ups**: [Items I need to follow up on]

## Performance Tracking
- **Tasks Completed**: 0
- **Code Reviews**: 0
- **Help Requests**: 0
- **Knowledge Shares**: 0

## Goals and Development
- **Sprint Goals**: [My goals for the current sprint]
- **Learning Goals**: [Skills I want to develop]
- **Collaboration Goals**: [How I want to improve team collaboration]
- **Quality Goals**: [How I want to improve code quality]

## Notes and Observations
- [Personal notes and observations about the project and team]
"""
        memory_file.write_text(memory_content)


def _get_agent_role(agent_number: int, team_size: int, project_type: str) -> str:
    """Get agent role based on position, team size, and project type."""
    if team_size <= 3:
        roles = ["Lead Developer", "Full-Stack Developer", "QA/DevOps Engineer"]
    elif team_size <= 6:
        if project_type == "api":
            roles = [
                "Technical Lead",
                "Backend Developer",
                "Database Engineer",
                "Security Engineer",
                "QA Engineer",
                "DevOps Engineer",
            ]
        elif project_type == "web_app":
            roles = [
                "Technical Lead",
                "Frontend Lead",
                "Backend Lead",
                "Full-Stack Developer",
                "QA Engineer",
                "DevOps Engineer",
            ]
        else:
            roles = [
                "Project Lead",
                "Senior Developer",
                "Developer",
                "Specialist",
                "QA Engineer",
                "Support Engineer",
            ]
    else:
        roles = [
            "Project Manager",
            "Technical Architect",
            "Frontend Lead",
            "Frontend Developer",
            "Backend Lead",
            "Backend Developer",
            "QA Lead",
            "DevOps Engineer",
        ]
        # Extend roles if team is larger
        while len(roles) < team_size:
            roles.append(f"Developer {len(roles) - 6}")

    return roles[min(agent_number - 1, len(roles) - 1)]


def _get_role_responsibilities(role: str, project_type: str) -> str:
    """Get detailed responsibilities for a specific role."""
    responsibilities = {
        "Lead Developer": """
- **Technical Leadership**: Guide technical decisions and architecture
- **Code Review**: Review all code changes for quality and standards
- **Mentoring**: Help other team members with technical challenges
- **Coordination**: Coordinate with other team members and stakeholders
""",
        "Technical Lead": """
- **Architecture**: Design and maintain system architecture
- **Technical Decisions**: Make key technical decisions for the project
- **Code Review**: Oversee code review process and maintain quality standards
- **Team Coordination**: Coordinate technical work across team members
""",
        "Full-Stack Developer": """
- **Feature Development**: Implement features across frontend and backend
- **Integration**: Ensure smooth integration between different components
- **Testing**: Write and maintain tests for implemented features
- **Documentation**: Document code and technical decisions
""",
        "Frontend Lead": """
- **Frontend Architecture**: Design and maintain frontend architecture
- **UI/UX Implementation**: Implement user interface and user experience
- **Component Design**: Create reusable UI components
- **Frontend Team Coordination**: Coordinate frontend development efforts
""",
        "Backend Lead": """
- **Backend Architecture**: Design and maintain backend architecture
- **API Design**: Design and implement API endpoints
- **Database Design**: Design and maintain database schema
- **Backend Team Coordination**: Coordinate backend development efforts
""",
        "QA Engineer": """
- **Testing Strategy**: Develop and implement testing strategy
- **Test Automation**: Create and maintain automated tests
- **Quality Assurance**: Ensure code quality and adherence to standards
- **Bug Tracking**: Track and manage bug reports and fixes
""",
        "DevOps Engineer": """
- **Infrastructure**: Manage development and production infrastructure
- **CI/CD**: Implement and maintain continuous integration and deployment
- **Monitoring**: Setup and maintain system monitoring and alerting
- **Deployment**: Manage application deployment and releases
""",
        "Project Manager": """
- **Project Planning**: Plan and coordinate project activities
- **Stakeholder Communication**: Communicate with stakeholders and clients
- **Resource Management**: Manage team resources and allocation
- **Risk Management**: Identify and mitigate project risks
""",
    }

    return responsibilities.get(
        role,
        f"""
- **Primary Responsibilities**: [Role-specific responsibilities for {role}]
- **Secondary Responsibilities**: [Supporting duties and backup coverage]
- **Collaboration**: [Key collaboration points with other team members]
- **Decision Authority**: [Areas where this role has decision-making authority]
""",
    )


def _get_team_summary(team_size: int, project_type: str, complexity: str) -> str:
    """Get a brief team summary."""
    if team_size <= 3:
        return f"Small team ({team_size} agents) - Full-stack + QA + DevOps"
    elif team_size <= 6:
        return f"Medium team ({team_size} agents) - Specialized roles with lead"
    else:
        return f"Large team ({team_size} agents) - Multiple specialized teams with leadership"
