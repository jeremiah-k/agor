"""
Project Planning Templates for Multi-Agent Development

This module contains templates and utilities for planning complex development
projects that will be executed by teams of specialized AI agents.
"""


def generate_project_breakdown_template():
    """Template for breaking down large projects into manageable tasks"""
    return """
# Project Breakdown Template

## Overview
- **Name**: [Project Name]
- **Goals**: [Primary objectives]
- **Scope**: [What's included/excluded]

## Analysis
- **Current State**: [Existing system]
- **Target State**: [Desired end state]
- **Key Changes**: [Major modifications]
- **Impact**: [Affected areas]

## Task Breakdown
### Phase 1: Analysis
- [ ] **Codebase Analysis** (Analyst) - Structure, dependencies, architecture
- [ ] **Requirements** (Business Analyst) - Functional/non-functional requirements

### Phase 2: Design
- [ ] **System Design** (Architect) - Components, APIs, integration
- [ ] **Database Design** (DB Specialist) - Schema, migrations, optimization

### Phase 3: Implementation
- [ ] **Backend** (Backend Dev) - APIs, business logic, data persistence
- [ ] **Frontend** (Frontend Dev) - UI components, API integration

### Phase 4: Quality
- [ ] **Testing** (Tester) - Unit/integration tests, coverage
- [ ] **Review** (Reviewer) - Code quality, security, standards

### Phase 5: Deployment
- [ ] **DevOps** (DevOps) - Deployment scripts, monitoring
- [ ] **Documentation** (Writer) - Technical docs, user guides

## Dependencies
- [Task dependencies and parallel work]

## Risks
- **High**: [Description and mitigation]
- **Medium**: [Description and monitoring]

## Success Criteria
- [ ] Acceptance criteria met
- [ ] Performance benchmarks achieved
- [ ] Security requirements satisfied
- [ ] Deployment successful

## Coordination
- **Handoffs**: [Agent-to-agent work transfer]
- **Quality Gates**: [Validation checkpoints]
- **Escalation**: [Issue resolution process]
"""


def generate_team_structure_template():
    """Template for defining multi-agent team structures"""
    return """
# Team Structure Template

## Core Team
1. **Architect** - System design, technical leadership, coordination
   - Handoff: Architecture specs to all developers

2. **Backend Developer** - APIs, business logic, database integration
   - Handoff: API specs to frontend, test data to tester

3. **Frontend Developer** - UI components, user experience, API integration
   - Handoff: UI components to tester, build artifacts to DevOps

## Quality Team
4. **Tester** - Test creation, validation, quality assurance
   - Handoff: Test suites to DevOps, bug reports to developers

5. **Reviewer** - Code quality, security, performance optimization
   - Handoff: Approved code to DevOps, fixes needed to developers

## Support Team
6. **DevOps** - Deployment, infrastructure, monitoring
   - Handoff: Deployed systems to team, deployment process documentation

## Coordination
- **Daily Sync**: Status updates, dependency checks, risk assessment
- **Handoffs**: Complete work → document → validate → proceed
- **Quality Gates**: Code complete → integration ready → review approved → deployment ready
- **Escalation**: Technical → Architect, Quality → Reviewer, Timeline → Coordinator
"""


def generate_workflow_template():
    """Template for defining agent workflows and coordination"""
    return """
# Workflow Template

## Phases
1. **Analysis**: Analyst → Architect (codebase analysis, technical design)
2. **Development**: Backend ↔ Frontend (parallel implementation)
3. **Quality**: Tester → Reviewer (testing, code review)
4. **Deployment**: DevOps (deployment, monitoring)

## Checkpoints
- Design approval
- Component completion
- Integration testing
- Deployment readiness

## Error Handling
- Integration failures → rollback and fix
- Quality issues → return to developer
- Timeline delays → adjust priorities
- Technical blockers → escalate to architect
"""
