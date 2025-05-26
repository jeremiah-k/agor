"""
Project Breakdown Strategy Implementation for AGOR.

This module provides intelligent task decomposition and agent assignment
based on project type, complexity, and team size.
"""

from datetime import datetime
from pathlib import Path


def project_breakdown(
    task_description: str, complexity: str = "medium", project_type: str = "auto"
) -> str:
    """Break down project into manageable tasks with agent assignments (bp hotkey)."""

    # Auto-detect project type if not specified
    if project_type == "auto":
        project_type = _detect_project_type(task_description)

    # Generate project breakdown based on type and complexity
    breakdown_details = f"""
## PROJECT BREAKDOWN IMPLEMENTATION

### Project: {task_description}
### Project Type: {project_type}
### Complexity: {complexity}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## INTELLIGENT TASK DECOMPOSITION

{_generate_task_breakdown(task_description, project_type, complexity)}

## AGENT ASSIGNMENT STRATEGY

{_generate_agent_assignments(project_type, complexity)}

## TASK COORDINATION PROTOCOLS

### Task Dependencies:
{_generate_task_dependencies(project_type)}

### Parallel Execution Opportunities:
{_generate_parallel_tasks(project_type)}

### Quality Gates:
{_generate_quality_checkpoints(complexity)}

## IMPLEMENTATION ROADMAP

{_generate_implementation_roadmap(project_type, complexity)}

## COORDINATION FILES SETUP

### Task Tracking:
- `.agor/task-breakdown.md` - Detailed task list and assignments
- `.agor/task-dependencies.md` - Task dependency mapping
- `.agor/task-progress.md` - Real-time progress tracking

### Communication Protocols:
```
TASK_ASSIGNED: [agent-id] - [task-name] - [priority] - [estimated-hours] - [timestamp]
TASK_STARTED: [agent-id] - [task-name] - [approach] - [timestamp]
TASK_BLOCKED: [agent-id] - [task-name] - [blocker] - [help-needed] - [timestamp]
TASK_COMPLETED: [agent-id] - [task-name] - [deliverables] - [timestamp]
```

## NEXT STEPS

1. **Review Task Breakdown**: Validate task decomposition and assignments
2. **Setup Coordination**: Initialize task tracking and dependency files
3. **Begin Execution**: Start with foundation tasks and parallel tracks
4. **Monitor Progress**: Track task completion and adjust as needed
5. **Quality Validation**: Ensure quality gates are met at each milestone
"""

    # Save to project breakdown file
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)
    breakdown_file = agor_dir / "project-breakdown.md"
    breakdown_file.write_text(breakdown_details)

    # Create coordination files
    _create_task_coordination_files(task_description, project_type, complexity)

    return f"""✅ Project Breakdown Complete

**Project**: {task_description}
**Type**: {project_type}
**Complexity**: {complexity}

**Breakdown Features**:
- Intelligent task decomposition based on project type
- Agent assignment strategy with role specialization
- Task dependency mapping and parallel execution planning
- Quality gates and milestone tracking
- Real-time progress coordination

**Files Created**:
- `.agor/project-breakdown.md` - Complete breakdown analysis
- `.agor/task-breakdown.md` - Detailed task list and assignments
- `.agor/task-dependencies.md` - Task dependency mapping
- `.agor/task-progress.md` - Progress tracking dashboard

**Next Steps**:
1. Review and validate task breakdown
2. Assign tasks to agents based on recommendations
3. Begin execution with foundation tasks
4. Monitor progress and adjust as needed

**Ready for coordinated project execution!**
"""


def _detect_project_type(task_description: str) -> str:
    """Auto-detect project type from task description."""
    task_lower = task_description.lower()

    # API/Backend detection
    if any(
        word in task_lower
        for word in ["api", "backend", "service", "endpoint", "database", "server"]
    ):
        return "api"

    # Frontend detection
    elif any(
        word in task_lower
        for word in [
            "frontend",
            "ui",
            "interface",
            "react",
            "vue",
            "angular",
            "website",
        ]
    ):
        return "frontend"

    # Full-stack detection
    elif any(
        word in task_lower
        for word in ["fullstack", "full-stack", "web app", "application", "platform"]
    ):
        return "web_app"

    # Mobile detection
    elif any(
        word in task_lower
        for word in ["mobile", "ios", "android", "app", "flutter", "react native"]
    ):
        return "mobile"

    # Data/Analytics detection
    elif any(
        word in task_lower
        for word in ["data", "analytics", "ml", "ai", "machine learning", "analysis"]
    ):
        return "data"

    # Security detection
    elif any(
        word in task_lower
        for word in ["security", "auth", "authentication", "encryption", "secure"]
    ):
        return "security"

    # Default to generic
    else:
        return "generic"


def _generate_task_breakdown(
    task_description: str, project_type: str, complexity: str
) -> str:
    """Generate task breakdown based on project characteristics."""

    if project_type == "api":
        return _generate_api_task_breakdown(complexity)
    elif project_type == "frontend":
        return _generate_frontend_task_breakdown(complexity)
    elif project_type == "web_app":
        return _generate_webapp_task_breakdown(complexity)
    elif project_type == "mobile":
        return _generate_mobile_task_breakdown(complexity)
    elif project_type == "data":
        return _generate_data_task_breakdown(complexity)
    elif project_type == "security":
        return _generate_security_task_breakdown(complexity)
    else:
        return _generate_generic_task_breakdown(complexity)


def _generate_api_task_breakdown(complexity: str) -> str:
    """Generate API-specific task breakdown."""
    base_tasks = """
### API Development Tasks

#### Foundation Tasks (Sequential)
1. **API Design & Specification**
   - Define API endpoints and methods
   - Create OpenAPI/Swagger documentation
   - Design request/response schemas
   - Plan error handling and status codes

2. **Database Design**
   - Design database schema
   - Create entity relationships
   - Plan data validation rules
   - Design migration strategy

3. **Authentication & Security**
   - Design authentication flow
   - Implement authorization middleware
   - Plan rate limiting and security headers
   - Design API key management

#### Core Development Tasks (Parallel)
4. **Endpoint Implementation**
   - Implement CRUD operations
   - Add business logic validation
   - Implement error handling
   - Add logging and monitoring

5. **Database Integration**
   - Implement data access layer
   - Create database migrations
   - Add connection pooling
   - Implement query optimization

6. **Testing Implementation**
   - Write unit tests for endpoints
   - Create integration tests
   - Add API contract testing
   - Implement load testing

#### Integration Tasks (Sequential)
7. **API Integration & Testing**
   - End-to-end API testing
   - Performance optimization
   - Security vulnerability testing
   - Documentation validation
"""

    if complexity == "complex":
        base_tasks += """

#### Advanced Tasks (Parallel)
8. **Advanced Features**
   - Implement caching layer
   - Add API versioning
   - Create webhook system
   - Add real-time capabilities

9. **Scalability & Monitoring**
   - Implement horizontal scaling
   - Add comprehensive monitoring
   - Create alerting system
   - Optimize for high availability
"""

    return base_tasks


def _generate_frontend_task_breakdown(complexity: str) -> str:
    """Generate frontend-specific task breakdown."""
    return """
### Frontend Development Tasks

#### Foundation Tasks (Sequential)
1. **UI/UX Design & Planning**
   - Create wireframes and mockups
   - Design component architecture
   - Plan state management strategy
   - Create design system/style guide

2. **Project Setup & Configuration**
   - Initialize project structure
   - Configure build tools and bundlers
   - Setup development environment
   - Configure testing framework

#### Core Development Tasks (Parallel)
3. **Component Development**
   - Create reusable UI components
   - Implement component styling
   - Add component documentation
   - Create component tests

4. **Page/View Implementation**
   - Implement main application pages
   - Add navigation and routing
   - Implement responsive design
   - Add accessibility features

5. **State Management & API Integration**
   - Implement state management
   - Create API service layer
   - Add data fetching and caching
   - Implement error handling

#### Integration Tasks (Sequential)
6. **Integration & Testing**
   - End-to-end testing
   - Cross-browser testing
   - Performance optimization
   - User acceptance testing
"""


def _generate_webapp_task_breakdown(complexity: str) -> str:
    """Generate web application task breakdown."""
    return """
### Web Application Development Tasks

#### Foundation Tasks (Sequential)
1. **Architecture & Planning**
   - Define application architecture
   - Plan frontend/backend integration
   - Design database schema
   - Create development roadmap

2. **Environment Setup**
   - Setup development environment
   - Configure CI/CD pipeline
   - Setup testing frameworks
   - Configure monitoring tools

#### Frontend Track (Parallel)
3. **Frontend Development**
   - UI/UX design and implementation
   - Component development
   - State management
   - API integration

#### Backend Track (Parallel)
4. **Backend Development**
   - API endpoint development
   - Database implementation
   - Authentication system
   - Business logic implementation

#### Integration Track (Sequential)
5. **System Integration**
   - Frontend-backend integration
   - End-to-end testing
   - Performance optimization
   - Security testing

6. **Deployment & Launch**
   - Production deployment
   - Monitoring setup
   - User documentation
   - Launch preparation
"""


def _generate_mobile_task_breakdown(complexity: str) -> str:
    """Generate mobile application task breakdown."""
    return """
### Mobile Application Development Tasks

#### Foundation Tasks (Sequential)
1. **Design & Planning**
   - UX design for mobile
   - Platform strategy (iOS/Android/Cross-platform)
   - Architecture planning
   - Development environment setup

2. **Core App Structure**
   - Navigation implementation
   - State management setup
   - API service layer
   - Local storage implementation

#### Feature Development (Parallel)
3. **UI Implementation**
   - Screen development
   - Component creation
   - Styling and theming
   - Responsive design

4. **Platform Integration**
   - Device feature integration
   - Push notifications
   - App store preparation
   - Platform-specific optimizations

#### Testing & Deployment (Sequential)
5. **Testing & Launch**
   - Device testing
   - Performance optimization
   - App store submission
   - Launch coordination
"""


def _generate_data_task_breakdown(complexity: str) -> str:
    """Generate data project task breakdown."""
    return """
### Data Project Development Tasks

#### Foundation Tasks (Sequential)
1. **Data Discovery & Planning**
   - Data source identification
   - Data quality assessment
   - Architecture planning
   - Tool selection

2. **Data Pipeline Setup**
   - Data ingestion implementation
   - Data cleaning and validation
   - Storage solution setup
   - Processing framework configuration

#### Analysis Track (Parallel)
3. **Data Analysis & Modeling**
   - Exploratory data analysis
   - Model development
   - Feature engineering
   - Performance optimization

#### Visualization Track (Parallel)
4. **Visualization & Reporting**
   - Dashboard development
   - Report generation
   - Interactive visualizations
   - User interface creation

#### Deployment Track (Sequential)
5. **Production Deployment**
   - Pipeline automation
   - Monitoring implementation
   - Documentation creation
   - User training
"""


def _generate_security_task_breakdown(complexity: str) -> str:
    """Generate security project task breakdown."""
    return """
### Security Project Development Tasks

#### Foundation Tasks (Sequential)
1. **Security Assessment & Planning**
   - Threat modeling
   - Security requirements analysis
   - Risk assessment
   - Security architecture design

2. **Security Implementation**
   - Authentication system
   - Authorization framework
   - Encryption implementation
   - Security monitoring setup

#### Testing Track (Parallel)
3. **Security Testing**
   - Vulnerability assessment
   - Penetration testing
   - Security code review
   - Compliance validation

#### Monitoring Track (Parallel)
4. **Security Monitoring**
   - Intrusion detection
   - Log analysis
   - Incident response
   - Security reporting

#### Compliance Track (Sequential)
5. **Compliance & Documentation**
   - Compliance validation
   - Security documentation
   - Training materials
   - Audit preparation
"""


def _generate_generic_task_breakdown(complexity: str) -> str:
    """Generate generic task breakdown."""
    return """
### Generic Development Tasks

#### Foundation Tasks (Sequential)
1. **Analysis & Planning**
   - Requirements analysis
   - System design
   - Technology selection
   - Project planning

2. **Environment Setup**
   - Development environment
   - Testing framework
   - CI/CD pipeline
   - Documentation setup

#### Development Track (Parallel)
3. **Core Implementation**
   - Feature development
   - Integration implementation
   - Testing development
   - Documentation creation

#### Quality Track (Parallel)
4. **Quality Assurance**
   - Testing execution
   - Code review
   - Performance testing
   - Security review

#### Deployment Track (Sequential)
5. **Deployment & Launch**
   - Production deployment
   - Monitoring setup
   - User documentation
   - Launch support
"""


def _generate_agent_assignments(project_type: str, complexity: str) -> str:
    """Generate agent assignment recommendations."""
    if project_type == "api":
        return """
### Recommended Agent Assignments

**Agent 1: API Architect**
- API design and specification
- Database schema design
- System architecture decisions
- Technical leadership

**Agent 2: Backend Developer**
- Endpoint implementation
- Business logic development
- Database integration
- Performance optimization

**Agent 3: Security Specialist**
- Authentication implementation
- Security testing
- Vulnerability assessment
- Security documentation

**Agent 4: QA Engineer**
- Test development and execution
- API testing and validation
- Integration testing
- Quality assurance
"""
    elif project_type == "frontend":
        return """
### Recommended Agent Assignments

**Agent 1: UI/UX Developer**
- Design implementation
- Component development
- User experience optimization
- Design system maintenance

**Agent 2: Frontend Engineer**
- Application logic
- State management
- API integration
- Performance optimization

**Agent 3: QA Engineer**
- Testing implementation
- Cross-browser testing
- User acceptance testing
- Quality assurance
"""
    else:
        return """
### Recommended Agent Assignments

**Agent 1: Technical Lead**
- Architecture decisions
- Technical coordination
- Code review
- Team guidance

**Agent 2: Full-Stack Developer**
- Feature implementation
- Integration development
- Technical problem solving
- Documentation

**Agent 3: QA Engineer**
- Testing strategy
- Quality assurance
- Bug tracking
- User acceptance testing

**Agent 4: DevOps Engineer**
- Environment setup
- Deployment automation
- Monitoring implementation
- Infrastructure management
"""


def _generate_task_dependencies(project_type: str) -> str:
    """Generate task dependency mapping."""
    return """
### Task Dependencies

**Critical Path Dependencies:**
- Foundation tasks must complete before development tasks
- Core development must complete before integration
- Integration must complete before deployment

**Parallel Opportunities:**
- Component development can happen in parallel
- Testing can be developed alongside features
- Documentation can be created during development

**Blocking Dependencies:**
- Database schema must be finalized before backend development
- API contracts must be defined before frontend integration
- Security framework must be established before feature development
"""


def _generate_parallel_tasks(project_type: str) -> str:
    """Generate parallel execution opportunities."""
    return """
### Parallel Execution Opportunities

**High Parallelism:**
- Component/feature development
- Test development
- Documentation creation
- Code review processes

**Medium Parallelism:**
- Frontend and backend development (with defined contracts)
- Different feature tracks
- Testing and development (with TDD)

**Sequential Requirements:**
- Architecture decisions
- Database schema finalization
- Security framework establishment
- Final integration and deployment
"""


def _generate_quality_checkpoints(complexity: str) -> str:
    """Generate quality checkpoints based on complexity."""
    base_checkpoints = """
### Quality Checkpoints

**Checkpoint 1: Foundation Review**
- Architecture approved
- Requirements validated
- Development environment ready
- Team assignments confirmed

**Checkpoint 2: Development Milestone**
- Core features implemented
- Unit tests passing
- Code review completed
- Integration ready

**Checkpoint 3: Integration Validation**
- System integration complete
- End-to-end testing passed
- Performance requirements met
- Security validation complete

**Checkpoint 4: Deployment Readiness**
- Production deployment tested
- Monitoring configured
- Documentation complete
- Launch criteria met
"""

    if complexity == "complex":
        base_checkpoints += """

**Checkpoint 5: Advanced Features**
- Advanced features implemented
- Scalability testing complete
- Performance optimization verified
- Advanced security measures validated
"""

    return base_checkpoints


def _generate_implementation_roadmap(project_type: str, complexity: str) -> str:
    """Generate implementation roadmap."""
    if complexity == "simple":
        return """
### Implementation Roadmap (Simple)

**Week 1: Foundation**
- Requirements analysis and planning
- Environment setup and configuration
- Basic architecture implementation

**Week 2: Core Development**
- Feature implementation
- Basic testing
- Integration work

**Week 3: Integration & Testing**
- System integration
- Testing and validation
- Bug fixes and optimization

**Week 4: Deployment**
- Production deployment
- Documentation finalization
- Launch and monitoring
"""
    elif complexity == "complex":
        return """
### Implementation Roadmap (Complex)

**Phase 1: Foundation (Weeks 1-2)**
- Comprehensive requirements analysis
- Detailed architecture design
- Environment and tooling setup
- Team coordination establishment

**Phase 2: Core Development (Weeks 3-6)**
- Feature implementation in parallel tracks
- Continuous integration and testing
- Regular code reviews and quality checks
- Progressive integration milestones

**Phase 3: Advanced Features (Weeks 7-8)**
- Advanced feature implementation
- Performance optimization
- Security hardening
- Scalability testing

**Phase 4: Integration & Testing (Weeks 9-10)**
- Comprehensive system integration
- End-to-end testing
- Performance and security validation
- User acceptance testing

**Phase 5: Deployment & Launch (Weeks 11-12)**
- Production deployment
- Monitoring and alerting setup
- Documentation and training
- Launch coordination and support
"""
    else:  # medium
        return """
### Implementation Roadmap (Medium)

**Phase 1: Foundation (Week 1)**
- Requirements analysis and planning
- Architecture design
- Environment setup
- Team coordination

**Phase 2: Development (Weeks 2-4)**
- Core feature implementation
- Testing development
- Regular integration
- Quality assurance

**Phase 3: Integration (Week 5)**
- System integration
- End-to-end testing
- Performance optimization
- Security validation

**Phase 4: Deployment (Week 6)**
- Production deployment
- Monitoring setup
- Documentation completion
- Launch preparation
"""


def _create_task_coordination_files(
    task_description: str, project_type: str, complexity: str
):
    """Create task coordination files."""
    agor_dir = Path(".agor")

    # Task breakdown file
    task_breakdown_file = agor_dir / "task-breakdown.md"
    task_breakdown_content = f"""# Task Breakdown

## Project: {task_description}
## Type: {project_type}
## Complexity: {complexity}
## Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Task List

### Foundation Tasks
- [ ] **Task 1**: [Task description]
  - **Assigned**: [Agent ID]
  - **Priority**: High
  - **Estimated Hours**: [X hours]
  - **Dependencies**: None
  - **Status**: Not Started

- [ ] **Task 2**: [Task description]
  - **Assigned**: [Agent ID]
  - **Priority**: High
  - **Estimated Hours**: [X hours]
  - **Dependencies**: Task 1
  - **Status**: Not Started

### Development Tasks
- [ ] **Task 3**: [Task description]
  - **Assigned**: [Agent ID]
  - **Priority**: Medium
  - **Estimated Hours**: [X hours]
  - **Dependencies**: Task 1, Task 2
  - **Status**: Not Started

## Task Assignment Guidelines

### Assignment Criteria
- Match agent skills to task requirements
- Balance workload across team
- Consider task dependencies
- Account for agent availability

### Task Status Updates
Use these formats in agentconvo.md:
```
TASK_ASSIGNED: [agent-id] - [task-name] - [priority] - [estimated-hours] - [timestamp]
TASK_STARTED: [agent-id] - [task-name] - [approach] - [timestamp]
TASK_COMPLETED: [agent-id] - [task-name] - [deliverables] - [timestamp]
```
"""
    task_breakdown_file.write_text(task_breakdown_content)

    # Task dependencies file
    dependencies_file = agor_dir / "task-dependencies.md"
    dependencies_content = f"""# Task Dependencies

## Project: {task_description}
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dependency Graph

### Critical Path
1. Foundation Tasks → Development Tasks → Integration Tasks → Deployment Tasks

### Parallel Opportunities
- Component development can happen in parallel
- Testing can be developed alongside features
- Documentation can be created during development

## Dependency Rules

### Blocking Dependencies
- Task A must complete before Task B can start
- Example: Database schema → Backend development

### Soft Dependencies
- Task A should complete before Task B for optimal efficiency
- Example: API design → Frontend development

### No Dependencies
- Tasks that can start immediately
- Tasks that can run in parallel

## Dependency Tracking

### Current Blockers
- [No blockers currently]

### Upcoming Dependencies
- [Dependencies that will become active soon]

### Resolved Dependencies
- [Dependencies that have been satisfied]
"""
    dependencies_file.write_text(dependencies_content)

    # Task progress file
    progress_file = agor_dir / "task-progress.md"
    progress_content = f"""# Task Progress Dashboard

## Project: {task_description}
## Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Progress
- **Total Tasks**: [X]
- **Completed**: 0
- **In Progress**: 0
- **Not Started**: [X]
- **Blocked**: 0

## Progress by Phase
- **Foundation**: 0% complete
- **Development**: 0% complete
- **Integration**: 0% complete
- **Deployment**: 0% complete

## Agent Workload
- **Agent 1**: [X tasks assigned, Y completed]
- **Agent 2**: [X tasks assigned, Y completed]
- **Agent 3**: [X tasks assigned, Y completed]

## Recent Activity

### Today ({datetime.now().strftime('%Y-%m-%d')})
- Project breakdown created
- Task coordination files initialized
- Ready for task assignment

## Upcoming Milestones
- [Milestone 1]: [Date]
- [Milestone 2]: [Date]
- [Milestone 3]: [Date]

## Issues and Blockers
- [No issues currently]

## Progress Notes
- [Progress notes and observations]
"""
    progress_file.write_text(progress_content)
