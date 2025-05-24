"""
Project Planning Templates for Multi-Agent Development

This module contains templates and utilities for planning complex development
projects that will be executed by teams of specialized AI agents.
"""

def generate_project_breakdown_template():
    """Template for breaking down large projects into manageable tasks"""
    return """
# Project Breakdown Template

## Project Overview
- **Name**: [Project Name]
- **Description**: [Brief description of what this project accomplishes]
- **Goals**: [Primary objectives and success criteria]
- **Scope**: [What is included and excluded from this project]

## Architecture Analysis
- **Current State**: [Description of existing system/codebase]
- **Target State**: [Description of desired end state]
- **Key Changes**: [Major modifications required]
- **Impact Assessment**: [Areas of the system that will be affected]

## Task Breakdown
### Phase 1: Analysis & Planning
- [ ] **Codebase Analysis** (Agent: Analyst)
  - Analyze existing code structure and patterns
  - Identify integration points and dependencies
  - Document current architecture and data flow
  - Estimate: [time/complexity]

- [ ] **Requirements Analysis** (Agent: Business Analyst)
  - Define detailed functional requirements
  - Identify non-functional requirements
  - Create acceptance criteria
  - Estimate: [time/complexity]

### Phase 2: Design & Architecture
- [ ] **System Design** (Agent: Architect)
  - Design new components and modifications
  - Plan integration with existing systems
  - Define APIs and interfaces
  - Estimate: [time/complexity]

- [ ] **Database Design** (Agent: Database Specialist)
  - Design schema changes
  - Plan data migration strategies
  - Optimize queries and indexes
  - Estimate: [time/complexity]

### Phase 3: Implementation
- [ ] **Backend Development** (Agent: Backend Developer)
  - Implement core business logic
  - Create APIs and services
  - Handle data persistence
  - Estimate: [time/complexity]

- [ ] **Frontend Development** (Agent: Frontend Developer)
  - Implement user interface components
  - Integrate with backend APIs
  - Ensure responsive design
  - Estimate: [time/complexity]

### Phase 4: Quality Assurance
- [ ] **Unit Testing** (Agent: Test Developer)
  - Create comprehensive unit tests
  - Ensure code coverage targets
  - Test edge cases and error conditions
  - Estimate: [time/complexity]

- [ ] **Integration Testing** (Agent: Integration Tester)
  - Test component interactions
  - Validate end-to-end workflows
  - Performance testing
  - Estimate: [time/complexity]

- [ ] **Code Review** (Agent: Code Reviewer)
  - Review all code changes
  - Ensure coding standards compliance
  - Security vulnerability assessment
  - Estimate: [time/complexity]

### Phase 5: Deployment & Documentation
- [ ] **Deployment Preparation** (Agent: DevOps)
  - Prepare deployment scripts
  - Configure environments
  - Set up monitoring and logging
  - Estimate: [time/complexity]

- [ ] **Documentation** (Agent: Technical Writer)
  - Update technical documentation
  - Create user guides
  - Document API changes
  - Estimate: [time/complexity]

## Dependencies
- **Task A** depends on **Task B** because [reason]
- **Task C** can run in parallel with **Task D**
- **Task E** blocks **Task F** until completion

## Risk Assessment
- **High Risk**: [Description and mitigation strategy]
- **Medium Risk**: [Description and mitigation strategy]
- **Low Risk**: [Description and monitoring approach]

## Success Metrics
- [ ] All acceptance criteria met
- [ ] Performance benchmarks achieved
- [ ] Security requirements satisfied
- [ ] Documentation complete and accurate
- [ ] Deployment successful with zero downtime

## Team Coordination
- **Daily Sync**: [How agents will coordinate daily]
- **Handoff Protocol**: [How work is passed between agents]
- **Issue Escalation**: [How problems are reported and resolved]
- **Quality Gates**: [Checkpoints where work is validated]
"""

def generate_team_structure_template():
    """Template for defining multi-agent team structures"""
    return """
# Multi-Agent Team Structure Template

## Team Composition

### Core Development Team
1. **Lead Architect Agent**
   - **Role**: Overall system design and technical leadership
   - **Responsibilities**: 
     - System architecture decisions
     - Technical standard enforcement
     - Cross-team coordination
   - **Specialties**: [List specific technical areas]
   - **Handoff Points**: [When and what this agent delivers to others]

2. **Backend Developer Agent**
   - **Role**: Server-side logic and API development
   - **Responsibilities**:
     - Business logic implementation
     - Database integration
     - API design and implementation
   - **Specialties**: [Programming languages, frameworks, databases]
   - **Handoff Points**: [APIs, services, data models to frontend and testing]

3. **Frontend Developer Agent**
   - **Role**: User interface and user experience implementation
   - **Responsibilities**:
     - UI component development
     - State management
     - API integration
   - **Specialties**: [Frontend frameworks, styling, accessibility]
   - **Handoff Points**: [UI components and flows to testing and integration]

### Quality Assurance Team
4. **Test Developer Agent**
   - **Role**: Automated testing and quality validation
   - **Responsibilities**:
     - Unit test creation
     - Test automation
     - Coverage analysis
   - **Specialties**: [Testing frameworks, test strategies]
   - **Handoff Points**: [Test suites to integration and deployment teams]

5. **Code Review Agent**
   - **Role**: Code quality and standards enforcement
   - **Responsibilities**:
     - Code review and feedback
     - Security analysis
     - Performance optimization
   - **Specialties**: [Code analysis, security, performance]
   - **Handoff Points**: [Approved code to deployment team]

### Specialized Support Team
6. **Database Specialist Agent**
   - **Role**: Data architecture and optimization
   - **Responsibilities**:
     - Schema design
     - Query optimization
     - Data migration
   - **Specialties**: [Database systems, data modeling, performance tuning]
   - **Handoff Points**: [Database changes to backend and testing teams]

7. **DevOps Agent**
   - **Role**: Deployment and infrastructure management
   - **Responsibilities**:
     - CI/CD pipeline setup
     - Environment configuration
     - Monitoring and logging
   - **Specialties**: [Cloud platforms, containerization, automation]
   - **Handoff Points**: [Deployed systems to monitoring and maintenance]

## Communication Protocols

### Daily Coordination
- **Status Updates**: Each agent reports progress and blockers
- **Dependency Check**: Identify and resolve inter-agent dependencies
- **Risk Assessment**: Flag potential issues early

### Handoff Procedures
1. **Preparation Phase**:
   - Complete assigned work according to specifications
   - Run validation checks and tests
   - Document decisions and assumptions

2. **Handoff Phase**:
   - Provide complete deliverables with documentation
   - Brief receiving agent on context and decisions
   - Transfer any relevant artifacts or configurations

3. **Validation Phase**:
   - Receiving agent validates deliverables
   - Reports any issues or questions
   - Confirms readiness to proceed

### Quality Gates
- **Code Complete**: All code written and unit tested
- **Integration Ready**: Components tested together
- **Review Approved**: Code review completed successfully
- **Deployment Ready**: All deployment requirements met

## Escalation Procedures
- **Technical Issues**: Escalate to Lead Architect
- **Quality Issues**: Escalate to Code Review Agent
- **Timeline Issues**: Escalate to Project Coordinator
- **Resource Issues**: Escalate to appropriate specialist
"""

def generate_workflow_template():
    """Template for defining agent workflows and coordination"""
    return """
# Multi-Agent Workflow Template

## Workflow Overview
This workflow defines how multiple AI agents coordinate to complete complex development tasks.

## Phase 1: Project Initialization
```
[Project Coordinator] → [Lead Architect] → [All Agents]
```

### Steps:
1. **Project Coordinator** analyzes requirements and creates initial project plan
2. **Lead Architect** reviews plan and defines technical approach
3. **All Agents** receive context and understand their roles

### Deliverables:
- Project charter and scope definition
- Technical architecture overview
- Agent role assignments and responsibilities

## Phase 2: Analysis and Design
```
[Analyst] → [Architect] → [Database Specialist]
     ↓           ↓              ↓
[Business Analyst] → [All Development Agents]
```

### Steps:
1. **Analyst** performs codebase analysis and impact assessment
2. **Architect** creates detailed technical design
3. **Database Specialist** designs data layer changes
4. **Business Analyst** defines detailed requirements
5. **All Development Agents** receive design specifications

### Deliverables:
- Codebase analysis report
- Technical design documents
- Database schema and migration plans
- Detailed requirements specification

## Phase 3: Parallel Development
```
[Backend Developer] ←→ [Frontend Developer]
        ↓                      ↓
[Database Specialist] ←→ [Test Developer]
```

### Steps:
1. **Backend** and **Frontend Developers** work in parallel
2. **Database Specialist** implements schema changes
3. **Test Developer** creates tests for all components
4. Regular sync points ensure integration compatibility

### Deliverables:
- Backend services and APIs
- Frontend components and interfaces
- Database migrations and optimizations
- Comprehensive test suites

## Phase 4: Integration and Testing
```
[Integration Tester] → [Code Reviewer] → [DevOps]
```

### Steps:
1. **Integration Tester** validates component interactions
2. **Code Reviewer** performs final quality assessment
3. **DevOps** prepares deployment configuration

### Deliverables:
- Integration test results
- Code review approval
- Deployment-ready configuration

## Phase 5: Deployment and Documentation
```
[DevOps] → [Technical Writer] → [Project Coordinator]
```

### Steps:
1. **DevOps** executes deployment
2. **Technical Writer** updates documentation
3. **Project Coordinator** validates completion

### Deliverables:
- Successfully deployed system
- Updated documentation
- Project completion report

## Synchronization Points

### Daily Sync (All Agents)
- Progress updates
- Blocker identification
- Dependency coordination

### Integration Checkpoints
- **Checkpoint 1**: Design approval
- **Checkpoint 2**: Component completion
- **Checkpoint 3**: Integration testing
- **Checkpoint 4**: Deployment readiness

### Quality Gates
- **Gate 1**: Requirements validation
- **Gate 2**: Design review approval
- **Gate 3**: Code review approval
- **Gate 4**: Integration test approval
- **Gate 5**: Deployment approval

## Error Handling and Recovery

### Common Issues and Responses:
1. **Integration Failures**:
   - Rollback to last known good state
   - Identify root cause with relevant specialists
   - Implement fix and re-test

2. **Quality Issues**:
   - Return to appropriate development agent
   - Provide specific feedback and requirements
   - Re-validate after fixes

3. **Timeline Delays**:
   - Assess impact on dependent tasks
   - Adjust priorities and resource allocation
   - Communicate changes to all affected agents

4. **Technical Blockers**:
   - Escalate to Lead Architect
   - Convene technical review session
   - Implement architectural changes if needed

## Success Criteria
- [ ] All components integrate successfully
- [ ] Quality standards met at all gates
- [ ] Timeline and scope objectives achieved
- [ ] Documentation complete and accurate
- [ ] Deployment successful with monitoring active
"""
