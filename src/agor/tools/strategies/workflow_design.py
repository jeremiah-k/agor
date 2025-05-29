"""
Workflow Design Strategy Implementation for AGOR.

This module provides comprehensive workflow planning and phase management capabilities,
enabling teams to design coordinated development workflows with clear phases, quality gates,
and snapshot procedures.
"""

from datetime import datetime
from pathlib import Path


def design_workflow(
    project_description: str,
    team_size: int = 4,
    project_type: str = "web_app",
    complexity: str = "medium",
) -> str:
    """Design agent workflow and coordination patterns (wf hotkey)."""

    # Import the workflow template - dual-mode for bundle compatibility
    try:
        from ..project_planning_templates import generate_workflow_template
    except ImportError:
        # Bundle-mode fallback
        import os
        import sys

        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from project_planning_templates import generate_workflow_template

    # Get the base template
    template = generate_workflow_template()

    # Add concrete workflow implementation
    implementation_details = f"""
## CONCRETE WORKFLOW IMPLEMENTATION

### Project: {project_description}
### Team Size: {team_size} agents
### Project Type: {project_type}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## WORKFLOW DESIGN

{_generate_workflow_phases(project_type, complexity, team_size)}

## AGENT WORKFLOW ASSIGNMENTS

{_generate_workflow_assignments(team_size, project_type)}

## COORDINATION PROTOCOLS

### Phase Transition Rules:
```
PHASE_COMPLETE: [agent-id] - [phase-name] - [deliverables] - [timestamp]
PHASE_READY: [next-agent] - [phase-name] - [prerequisites-met] - [timestamp]
PHASE_BLOCKED: [agent-id] - [phase-name] - [blocker-description] - [timestamp]
```

### Quality Gates:
{_generate_workflow_quality_gates(complexity)}

### Snapshot Procedures:
{_generate_workflow_snapshots(project_type)}

## WORKFLOW EXECUTION

### Parallel Tracks:
{_generate_parallel_tracks(team_size, project_type)}

### Dependencies:
{_generate_workflow_dependencies(project_type, complexity)}

### Timeline:
{_generate_workflow_timeline(complexity, team_size)}

## ERROR HANDLING & RECOVERY

### Common Workflow Issues:
1. **Phase Blocking**: When one phase cannot proceed
   - **Detection**: Missing prerequisites, failed quality gates
   - **Resolution**: Rollback to previous phase, fix issues, retry
   - **Prevention**: Clear phase completion criteria

2. **Integration Conflicts**: When parallel work doesn't merge cleanly
   - **Detection**: Merge conflicts, API mismatches, test failures
   - **Resolution**: Integration agent coordinates resolution
   - **Prevention**: Regular integration checkpoints

3. **Resource Bottlenecks**: When agents are waiting for others
   - **Detection**: Idle agents, delayed phase transitions
   - **Resolution**: Rebalance work, add parallel tasks
   - **Prevention**: Load balancing, buffer tasks

4. **Quality Failures**: When deliverables don't meet standards
   - **Detection**: Failed quality gates, review rejections
   - **Resolution**: Return to development phase, address issues
   - **Prevention**: Continuous quality checks

### Recovery Procedures:
```
WORKFLOW_ISSUE: [agent-id] - [issue-type] - [description] - [timestamp]
RECOVERY_PLAN: [coordinator] - [steps] - [timeline] - [timestamp]
RECOVERY_COMPLETE: [agent-id] - [resolution] - [lessons-learned] - [timestamp]
```

## WORKFLOW MONITORING

### Progress Tracking:
- **Phase Completion**: Percentage complete for each phase
- **Agent Utilization**: Active vs idle time for each agent
- **Quality Metrics**: Defect rates, rework percentage
- **Timeline Adherence**: Actual vs planned phase durations

### Performance Indicators:
- **Velocity**: Features completed per sprint
- **Quality**: Bug rates, review feedback scores
- **Efficiency**: Rework percentage, idle time
- **Collaboration**: Snapshot success rate, communication frequency

## WORKFLOW OPTIMIZATION

### Continuous Improvement:
1. **Weekly Retrospectives**: What worked, what didn't, improvements
2. **Metrics Review**: Analyze performance indicators, identify bottlenecks
3. **Process Refinement**: Adjust phases, snapshots, quality gates
4. **Tool Enhancement**: Improve coordination tools and templates

### Adaptation Triggers:
- **Performance Degradation**: Velocity drops, quality issues increase
- **Team Changes**: New agents, role changes, skill gaps
- **Project Evolution**: Scope changes, new requirements, technology shifts
- **External Factors**: Timeline pressure, resource constraints

## WORKFLOW INITIALIZATION CHECKLIST

- [ ] **Workflow Design Approved**: All agents understand the process
- [ ] **Phase Definitions Clear**: Entry/exit criteria defined
- [ ] **Quality Gates Established**: Standards and review processes
- [ ] **Snapshot Procedures Documented**: Clear transition protocols
- [ ] **Monitoring Setup**: Progress tracking and metrics collection
- [ ] **Error Handling Defined**: Recovery procedures and escalation
- [ ] **Communication Protocols**: Regular updates and coordination
- [ ] **Tool Integration**: .agor files and coordination systems

## NEXT STEPS

1. **Review Workflow Design**: Validate phases and assignments with team
2. **Setup Coordination**: Initialize .agor workflow tracking files
3. **Define Standards**: Establish quality gates and snapshot criteria
4. **Begin Execution**: Start with first phase and monitor progress
5. **Iterate and Improve**: Regular retrospectives and optimization
"""

    # Combine template with implementation
    full_workflow = template + implementation_details

    # Create .agor directory
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)

    # Save to workflow design file
    workflow_file = agor_dir / "workflow-design.md"
    workflow_file.write_text(full_workflow)

    # Create workflow tracking file
    _create_workflow_tracking_file(team_size, project_type)

    # Create phase coordination files
    _create_phase_coordination_files(project_type, complexity)

    # Create workflow metrics file
    _create_workflow_metrics_file(team_size, project_type, complexity)

    return f"""✅ Workflow Design Created

**Project**: {project_description}
**Team Size**: {team_size} agents
**Project Type**: {project_type}
**Complexity**: {complexity}

**Workflow Structure**:
{_get_workflow_summary(project_type, complexity, team_size)}

**Files Created**:
- `.agor/workflow-design.md` - Complete workflow plan and coordination
- `.agor/workflow-tracking.md` - Progress tracking and metrics
- `.agor/workflow-metrics.md` - Workflow performance tracking
- `.agor/phase-[name].md` - Individual phase coordination files

**Next Steps**:
1. Review workflow design with team
2. Initialize phase coordination and tracking
3. Begin execution with first phase
4. Monitor progress and optimize workflow

**Ready for coordinated workflow execution!**
"""


def _generate_workflow_phases(
    project_type: str, complexity: str, team_size: int
) -> str:
    """Generate workflow phases based on project characteristics."""

    if project_type == "api":
        return _generate_api_workflow_phases(complexity)
    elif project_type == "web_app":
        return _generate_webapp_workflow_phases(complexity)
    elif project_type == "mobile":
        return _generate_mobile_workflow_phases(complexity)
    elif project_type == "data":
        return _generate_data_workflow_phases(complexity)
    else:
        return _generate_generic_workflow_phases(complexity)


def _generate_api_workflow_phases(complexity: str) -> str:
    """Generate API-specific workflow phases."""
    base_phases = """
### API Development Workflow

#### Phase 1: API Design (Sequential)
- **API Specification**: Define endpoints, schemas, error handling
- **Data Modeling**: Design database schema and relationships
- **Security Planning**: Authentication, authorization, rate limiting
- **Documentation**: API documentation and examples

#### Phase 2: Core Implementation (Parallel)
- **Backend Development**: API endpoints and business logic
- **Database Implementation**: Schema creation and data access layer
- **Authentication System**: User management and security
- **Testing Framework**: Unit tests and API testing

#### Phase 3: Integration & Testing (Sequential)
- **API Integration**: Connect all components
- **End-to-End Testing**: Full API workflow testing
- **Performance Testing**: Load testing and optimization
- **Security Testing**: Vulnerability assessment

#### Phase 4: Deployment (Sequential)
- **Environment Setup**: Production infrastructure
- **Deployment Pipeline**: CI/CD and automation
- **Monitoring**: Logging, metrics, and alerting
- **Documentation**: Deployment and maintenance guides
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Advanced Features (Parallel)
- **Caching Layer**: Redis/Memcached implementation
- **API Gateway**: Rate limiting, routing, analytics
- **Microservices**: Service decomposition and communication
- **Advanced Security**: OAuth, JWT, encryption
"""

    return base_phases


def _generate_webapp_workflow_phases(complexity: str) -> str:
    """Generate web application workflow phases."""
    base_phases = """
### Web Application Workflow

#### Phase 1: Foundation (Sequential)
- **Architecture Design**: Frontend/backend architecture
- **UI/UX Design**: Wireframes, mockups, design system
- **Database Design**: Schema and data relationships
- **Development Environment**: Setup and configuration

#### Phase 2: Core Development (Parallel)
- **Frontend Development**: UI components and user interface
- **Backend Development**: API and business logic
- **Database Implementation**: Data layer and migrations
- **Authentication**: User management and security

#### Phase 3: Integration (Sequential)
- **Frontend-Backend Integration**: API connections
- **Database Integration**: Data flow and persistence
- **User Experience**: Navigation and interaction flows
- **Testing**: Integration and user acceptance testing

#### Phase 4: Quality & Deployment (Parallel)
- **Quality Assurance**: Testing and bug fixes
- **Performance Optimization**: Speed and scalability
- **Deployment Setup**: Production environment
- **Documentation**: User guides and technical docs
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Advanced Features (Parallel)
- **Real-time Features**: WebSockets, notifications
- **Advanced UI**: Animations, responsive design
- **Analytics**: User tracking and reporting
- **SEO & Accessibility**: Search optimization and compliance
"""

    return base_phases


def _generate_mobile_workflow_phases(complexity: str) -> str:
    """Generate mobile application workflow phases."""
    return """
### Mobile Application Workflow

#### Phase 1: Design & Planning (Sequential)
- **UX Design**: User flows and wireframes
- **UI Design**: Visual design and components
- **Architecture**: App structure and data flow
- **Platform Strategy**: iOS, Android, or cross-platform

#### Phase 2: Core Development (Parallel)
- **UI Implementation**: Screens and components
- **Business Logic**: App functionality and features
- **Data Layer**: Local storage and API integration
- **Navigation**: Screen transitions and routing

#### Phase 3: Platform Integration (Parallel)
- **Platform Features**: Camera, GPS, notifications
- **Performance**: Memory management and optimization
- **Testing**: Device testing and compatibility
- **App Store Preparation**: Metadata and assets

#### Phase 4: Release (Sequential)
- **Final Testing**: QA and user acceptance
- **App Store Submission**: Review and approval
- **Launch Preparation**: Marketing and support
- **Post-Launch**: Monitoring and updates
"""


def _generate_data_workflow_phases(complexity: str) -> str:
    """Generate data project workflow phases."""
    return """
### Data Project Workflow

#### Phase 1: Data Discovery (Sequential)
- **Data Assessment**: Available data sources and quality
- **Requirements Analysis**: Business needs and objectives
- **Architecture Design**: Data pipeline and storage
- **Tool Selection**: Technologies and frameworks

#### Phase 2: Data Pipeline (Sequential)
- **Data Ingestion**: Collection and import processes
- **Data Cleaning**: Quality checks and transformation
- **Data Storage**: Database design and optimization
- **Data Validation**: Quality assurance and testing

#### Phase 3: Analysis & Modeling (Parallel)
- **Exploratory Analysis**: Data exploration and insights
- **Model Development**: Machine learning or analytics
- **Visualization**: Dashboards and reporting
- **Performance Tuning**: Optimization and scaling

#### Phase 4: Deployment (Sequential)
- **Production Pipeline**: Automated data processing
- **Monitoring**: Data quality and system health
- **Documentation**: Process and maintenance guides
- **Training**: User education and support
"""


def _generate_generic_workflow_phases(complexity: str) -> str:
    """Generate generic workflow phases."""
    base_phases = """
### Generic Development Workflow

#### Phase 1: Analysis & Design (Sequential)
- **Requirements Analysis**: Gather and document needs
- **System Design**: Architecture and component design
- **Technical Planning**: Technology choices and approach
- **Project Setup**: Environment and tool configuration

#### Phase 2: Implementation (Parallel)
- **Core Development**: Primary functionality
- **Component Development**: Individual modules
- **Integration Development**: Component connections
- **Testing Development**: Test suites and validation

#### Phase 3: Integration & Testing (Sequential)
- **System Integration**: Combine all components
- **Quality Assurance**: Testing and validation
- **Performance Testing**: Load and stress testing
- **User Acceptance**: Stakeholder validation

#### Phase 4: Deployment & Support (Sequential)
- **Deployment Preparation**: Production setup
- **Go-Live**: System launch and monitoring
- **Documentation**: User and technical guides
- **Support Setup**: Maintenance and help systems
"""

    if complexity == "complex":
        base_phases += """

#### Phase 5: Optimization (Parallel)
- **Performance Optimization**: Speed and efficiency
- **Security Hardening**: Vulnerability mitigation
- **Feature Enhancement**: Additional capabilities
- **Process Improvement**: Workflow optimization
"""

    return base_phases


def _generate_workflow_assignments(team_size: int, project_type: str) -> str:
    """Generate workflow assignments for agents."""
    if team_size <= 3:
        return """
### Small Team Workflow Assignments
- **Agent1**: Lead Developer - Handles design, core development, and coordination
- **Agent2**: Quality Engineer - Testing, integration, and quality assurance
- **Agent3**: DevOps Specialist - Deployment, monitoring, and infrastructure
"""
    elif team_size <= 6:
        return """
### Medium Team Workflow Assignments
- **Agent1**: Technical Lead - Architecture, coordination, and code review
- **Agent2**: Frontend Developer - UI/UX implementation and client-side logic
- **Agent3**: Backend Developer - API development and business logic
- **Agent4**: Quality Assurance - Testing, validation, and quality control
- **Agent5**: DevOps Engineer - Deployment, infrastructure, and monitoring
- **Agent6**: Integration Specialist - Component integration and system testing
"""
    else:
        return """
### Large Team Workflow Assignments
- **Agent1**: Project Coordinator - Overall workflow management and coordination
- **Agent2**: Technical Architect - System design and technical direction
- **Agent3**: Frontend Lead - UI/UX team coordination and implementation
- **Agent4**: Backend Lead - API and business logic team coordination
- **Agent5**: Quality Lead - Testing strategy and quality assurance
- **Agent6**: DevOps Lead - Infrastructure and deployment coordination
- **Agent7+**: Specialized Developers - Domain-specific implementation
"""


def _generate_workflow_quality_gates(complexity: str) -> str:
    """Generate quality gates for workflow phases."""
    base_gates = """
#### Phase 1 Quality Gates:
- [ ] Requirements documented and approved
- [ ] Architecture design reviewed and signed off
- [ ] Technical approach validated
- [ ] Development environment ready

#### Phase 2 Quality Gates:
- [ ] Code review completed for all components
- [ ] Unit tests passing with >80% coverage
- [ ] Security review completed
- [ ] Performance benchmarks met

#### Phase 3 Quality Gates:
- [ ] Integration tests passing
- [ ] End-to-end workflows validated
- [ ] Performance testing completed
- [ ] Security testing passed

#### Phase 4 Quality Gates:
- [ ] Production deployment successful
- [ ] Monitoring and alerting active
- [ ] Documentation complete and reviewed
- [ ] User acceptance criteria met
"""

    if complexity == "complex":
        base_gates += """

#### Phase 5 Quality Gates:
- [ ] Advanced features tested and validated
- [ ] Scalability requirements met
- [ ] Security hardening completed
- [ ] Performance optimization verified
"""

    return base_gates


def _generate_workflow_snapshots(project_type: str) -> str:
    """Generate snapshot procedures for workflow."""
    return """
#### Standard Snapshot Procedure:
1. **Completion Signal**: Agent signals phase completion with deliverables
2. **Quality Check**: Next agent validates prerequisites and quality gates
3. **Knowledge Transfer**: Brief snapshot meeting or documentation review
4. **Acceptance**: Receiving agent confirms readiness to proceed

#### Snapshot Documentation Template:
```
SNAPSHOT: [from-agent] → [to-agent] - [phase-name]
COMPLETED:
- [Deliverable 1 with location]
- [Deliverable 2 with location]
- [Quality gates passed]

NEXT PHASE:
- [Task 1 for receiving agent]
- [Task 2 for receiving agent]
- [Prerequisites and dependencies]

NOTES:
- [Important context or decisions]
- [Known issues or considerations]
- [Recommendations for next phase]
```

#### Emergency Snapshot Procedure:
- **Immediate**: Critical blocker requires different expertise
- **Planned**: Scheduled agent rotation or availability change
- **Quality**: Phase fails quality gates, needs rework
"""


def _generate_parallel_tracks(team_size: int, project_type: str) -> str:
    """Generate parallel execution tracks."""
    if project_type == "web_app":
        return """
#### Parallel Development Tracks:

**Track A: Frontend Development**
- UI component development
- User experience implementation
- Client-side testing
- Frontend optimization

**Track B: Backend Development**
- API endpoint development
- Business logic implementation
- Database integration
- Backend testing

**Track C: Infrastructure & Quality**
- Development environment setup
- CI/CD pipeline configuration
- Testing framework setup
- Deployment preparation

**Synchronization Points:**
- Daily: Progress updates and blocker resolution
- Weekly: Integration testing and alignment
- Phase End: Complete integration and snapshot
"""
    else:
        return """
#### Parallel Development Tracks:

**Track A: Core Development**
- Primary functionality implementation
- Core business logic
- Main feature development

**Track B: Supporting Systems**
- Infrastructure and tooling
- Testing and validation
- Documentation and guides

**Track C: Quality & Integration**
- Quality assurance
- System integration
- Performance optimization

**Synchronization Points:**
- Regular integration checkpoints
- Quality gate validations
- Phase completion reviews
"""


def _generate_workflow_dependencies(project_type: str, complexity: str) -> str:
    """Generate workflow dependencies."""
    return """
#### Critical Dependencies:

**Phase Dependencies:**
- Phase 1 → Phase 2: Architecture approval required
- Phase 2 → Phase 3: Core components completed
- Phase 3 → Phase 4: Integration testing passed
- Phase 4 → Launch: Quality gates satisfied

**Resource Dependencies:**
- Development Environment: Required for all development phases
- Test Environment: Required for integration and testing phases
- Production Environment: Required for deployment phase
- External APIs: May block integration if unavailable

**Knowledge Dependencies:**
- Domain Expertise: Required for business logic implementation
- Technical Skills: Specific technology knowledge needed
- Process Knowledge: Understanding of workflow and quality standards

**Dependency Management:**
- **Early Identification**: Map dependencies during planning
- **Risk Mitigation**: Prepare alternatives for critical dependencies
- **Regular Review**: Monitor dependency status and adjust plans
- **Communication**: Keep team informed of dependency changes
"""


def _generate_workflow_timeline(complexity: str, team_size: int) -> str:
    """Generate workflow timeline estimates."""
    if complexity == "simple":
        return """
#### Simple Project Timeline:
- **Phase 1**: 2-3 days (Analysis & Design)
- **Phase 2**: 5-7 days (Implementation)
- **Phase 3**: 2-3 days (Integration & Testing)
- **Phase 4**: 1-2 days (Deployment)

**Total Duration**: 10-15 days
**Team Utilization**: High (minimal idle time)
**Risk Buffer**: 20% additional time for unexpected issues
"""
    elif complexity == "complex":
        return """
#### Complex Project Timeline:
- **Phase 1**: 1-2 weeks (Analysis & Design)
- **Phase 2**: 3-4 weeks (Implementation)
- **Phase 3**: 1-2 weeks (Integration & Testing)
- **Phase 4**: 1 week (Deployment)
- **Phase 5**: 1-2 weeks (Advanced Features)

**Total Duration**: 7-11 weeks
**Team Utilization**: Medium (coordination overhead)
**Risk Buffer**: 30% additional time for complexity management
"""
    else:  # medium
        return """
#### Medium Project Timeline:
- **Phase 1**: 3-5 days (Analysis & Design)
- **Phase 2**: 2-3 weeks (Implementation)
- **Phase 3**: 1 week (Integration & Testing)
- **Phase 4**: 2-3 days (Deployment)

**Total Duration**: 4-6 weeks
**Team Utilization**: High (good balance)
**Risk Buffer**: 25% additional time for coordination
"""


def _create_workflow_tracking_file(team_size: int, project_type: str):
    """Create workflow tracking file."""
    tracking_file = Path(".agor") / "workflow-tracking.md"
    tracking_content = f"""
# Workflow Progress Tracking

## Project Configuration
- **Team Size**: {team_size} agents
- **Project Type**: {project_type}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Phase Progress

### Phase 1: Analysis & Design
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 2: Implementation
- **Status**: Not Started
- **Assigned**: [agent-ids]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 3: Integration & Testing
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

### Phase 4: Deployment
- **Status**: Not Started
- **Assigned**: [agent-id]
- **Started**: [timestamp]
- **Completed**: [timestamp]
- **Quality Gates**: [ ] [ ] [ ] [ ]
- **Deliverables**: [list when completed]

## Metrics Tracking

### Daily Metrics
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Active Agents**: 0/{team_size}
- **Completed Tasks**: 0
- **Blockers**: 0
- **Quality Issues**: 0

### Weekly Summary
- **Week**: [week-number]
- **Velocity**: [tasks completed]
- **Quality Score**: [percentage]
- **Team Utilization**: [percentage]
- **Timeline Adherence**: [on-track/delayed/ahead]

## Issue Tracking

### Active Issues
- [No issues currently]

### Resolved Issues
- [No issues resolved yet]

## Workflow Adjustments

### Process Changes
- [No changes made yet]

### Lessons Learned
- [Lessons will be captured here]
"""
    tracking_file.write_text(tracking_content)


def _create_phase_coordination_files(project_type: str, complexity: str):
    """Create individual phase coordination files."""
    phases = ["analysis-design", "implementation", "integration-testing", "deployment"]
    if complexity == "complex":
        phases.append("optimization")

    for phase in phases:
        phase_file = Path(".agor") / f"phase-{phase}.md"
        phase_content = f"""
# Phase: {phase.replace('-', ' ').title()}

## Phase Overview
[Description of this phase and its objectives]

## Assigned Agents
- [List of agents working on this phase]

## Tasks
- [ ] [Task 1 description]
- [ ] [Task 2 description]
- [ ] [Task 3 description]

## Quality Gates
- [ ] [Quality requirement 1]
- [ ] [Quality requirement 2]
- [ ] [Quality requirement 3]

## Deliverables
- [Deliverable 1 with location]
- [Deliverable 2 with location]

## Dependencies
- [Dependency 1 description]
- [Dependency 2 description]

## Progress Updates

### {datetime.now().strftime('%Y-%m-%d')}
- **Status**: Not Started
- **Progress**: 0%
- **Blockers**: None
- **Next Steps**: [What needs to be done next]

## Snapshot Preparation

### Prerequisites for Next Phase
- [Requirement 1]
- [Requirement 2]

### Snapshot Documentation
- [Will be completed when phase is done]

## Notes
- [Important notes and decisions for this phase]
"""
        phase_file.write_text(phase_content)


def _create_workflow_metrics_file(team_size: int, project_type: str, complexity: str):
    """Create workflow metrics tracking file."""
    metrics_file = Path(".agor") / "workflow-metrics.md"
    metrics_content = f"""
# Workflow Performance Metrics

## Configuration
- **Team Size**: {team_size} agents
- **Project Type**: {project_type}
- **Complexity**: {complexity}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Performance Indicators

### Velocity Metrics
- **Daily Task Completion**: [Track tasks completed per day]
- **Sprint Velocity**: [Track features completed per sprint]
- **Phase Completion Rate**: [Track phases completed on time]

### Quality Metrics
- **Defect Rate**: [Bugs found per phase]
- **Rework Percentage**: [Work that needed to be redone]
- **Code Review Feedback**: [Average feedback items per review]
- **Quality Gate Pass Rate**: [Percentage of gates passed first time]

### Collaboration Metrics
- **Snapshot Success Rate**: [Successful snapshots vs total snapshots]
- **Communication Frequency**: [Messages per day in agentconvo.md]
- **Help Request Response Time**: [Time to respond to blockers]
- **Knowledge Sharing**: [Documentation updates per agent]

### Efficiency Metrics
- **Agent Utilization**: [Active time vs idle time per agent]
- **Parallel Work Efficiency**: [Parallel tracks vs sequential work]
- **Dependency Resolution Time**: [Time to resolve blockers]
- **Timeline Adherence**: [Actual vs planned phase durations]

## Daily Tracking

### {datetime.now().strftime('%Y-%m-%d')}
- **Tasks Completed**: 0
- **Quality Issues**: 0
- **Handoffs**: 0
- **Blockers**: 0
- **Agent Utilization**: 0%

## Weekly Summary

### Week 1
- **Velocity**: [tasks/week]
- **Quality Score**: [percentage]
- **Team Efficiency**: [percentage]
- **Timeline Status**: [on-track/delayed/ahead]

## Trend Analysis

### Performance Trends
- [Track improvements or degradations over time]

### Bottleneck Identification
- [Identify recurring issues or slow phases]

### Optimization Opportunities
- [Areas for workflow improvement]

## Benchmarks

### Target Metrics
- **Velocity**: {team_size * 2} tasks per week
- **Quality**: >90% first-time quality gate pass
- **Efficiency**: >80% agent utilization
- **Timeline**: <10% variance from planned

### Historical Performance
- [Track performance against previous projects]

## Action Items

### Process Improvements
- [Specific actions to improve workflow]

### Tool Enhancements
- [Improvements to coordination tools]

### Team Development
- [Skills or knowledge gaps to address]
"""
    metrics_file.write_text(metrics_content)


def _get_workflow_summary(project_type: str, complexity: str, team_size: int) -> str:
    """Get workflow summary."""
    phase_count = 4 if complexity != "complex" else 5
    return f"{phase_count} phases, {project_type} optimized, {team_size} agents coordinated"
