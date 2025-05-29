"""
Team Management Strategy Implementation for AGOR.

This module provides comprehensive team performance and coordination capabilities,
enabling real-time team status tracking, performance metrics, issue management,
and continuous improvement processes.
"""

from datetime import datetime
from pathlib import Path


def manage_team(
    project_name: str = "Current Project",
    team_size: int = 4,
    management_focus: str = "performance",
) -> str:
    """Manage ongoing team coordination and performance (tm hotkey)."""

    # Import the team management template - dual-mode for bundle compatibility
    try:
        from ..project_planning_templates import generate_team_management_template
    except ImportError:
        # Bundle-mode fallback
        import os
        import sys

        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from project_planning_templates import generate_team_management_template

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
print(f"Active agents: {{status['active_count']}}/{team_size}")
print(f"Blocked tasks: {{status['blocked_count']}}")
print(f"Completion rate: {{status['completion_rate']}}%")
```

### Automated Metrics Tracking:
```python
# Track performance metrics
def collect_team_metrics(team_size):
    return {
        'velocity': team_size * 2.5,  # Estimated tasks per day
        'quality_score': 8.5,  # Quality score out of 10
        'collaboration_index': min(10, team_size * 1.8)  # Collaboration index
    }

metrics = collect_team_metrics(team_size)
print(f"Team velocity: {{metrics['velocity']}} tasks/day")
print(f"Quality score: {{metrics['quality_score']}}/10")
print(f"Collaboration index: {{metrics['collaboration_index']}}/10")
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

    # Create .agor directory
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)

    # Save to team management file
    management_file = agor_dir / "team-management.md"
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
- `.agor/team-retrospective.md` - Weekly improvement notes

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
- **Snapshot Efficiency**: [Success rate and speed of agent snapshots]
- **Meeting Overhead**: [Time spent in coordination vs development]

#### Productivity Targets
- **Individual Productivity**: {6 if team_size <= 3 else 5 if team_size <= 6 else 4} tasks per agent per day
- **Team Velocity**: {team_size * 5} tasks per day (team target)
- **Quality Gate**: >90% first-time pass rate for code reviews
- **Response Time**: <2 hours for help requests
- **Snapshot Success**: >95% successful snapshots without rework
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
""",
    }

    return strategies.get(
        management_focus,
        """
#### General Improvement Strategies
- **Process Optimization**: Continuously improve development processes
- **Skill Development**: Invest in team member growth
- **Tool Enhancement**: Upgrade and optimize development tools
- **Communication**: Improve team communication and coordination
- **Quality Focus**: Maintain high standards for deliverables
""",
    )


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
- **Snapshot Success Rate**: [Percentage of successful agent snapshots]
- **Rework Rate**: [Percentage of work requiring revision]
- **First-Time Pass Rate**: [Percentage passing review on first attempt]
- **Communication Effectiveness**: [Response time and clarity scores]

#### Quality Targets
- **Code Review Score**: >8.0/10
- **Bug Rate**: <2 bugs per 100 lines
- **Test Coverage**: >80%
- **Snapshot Success**: >95%
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
- **Coordination Problems**: Poor snapshots or collaboration

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
    return """
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
- **Snapshot Success Rate**: [Percentage of successful snapshots]

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
    agent_sections = newline.join(
        [
            f"### Agent{i}{newline}- **Role**: [Assigned role]{newline}- **Current Task**: [Task description]{newline}- **Priority**: [High/Medium/Low]{newline}- **Estimated Completion**: [Date/time]{newline}- **Dependencies**: [What this task depends on]{newline}- **Blockers**: [Current blockers if any]{newline}"
            for i in range(1, team_size + 1)
        ]
    )

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
- **Snapshots**: [Quality of work snapshots]
- **Help Requests**: [Response to help requests]
- **Knowledge Sharing**: [Sharing of expertise]

### Satisfaction
- **Work Satisfaction**: [Team satisfaction with work]
- **Process Satisfaction**: [Satisfaction with processes]
- **Team Dynamics**: [Quality of team relationships]
"""
    retro_file.write_text(retro_content)
