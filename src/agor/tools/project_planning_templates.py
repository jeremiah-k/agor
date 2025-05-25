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


def generate_parallel_divergent_strategy():
    """Template for parallel divergent development strategy"""
    return """
# Parallel Divergent Strategy Template

## Overview
Multiple agents work independently on the same problem, then converge through peer review.

## Phase 1: Divergent Execution (Parallel)
### Setup
- **Agents**: Multiple independent agents (typically 2-5)
- **Branches**: Each agent gets own branch (e.g., `solution-a`, `solution-b`, `solution-c`)
- **Mission**: Identical problem statement and success criteria
- **Isolation**: No coordination during execution phase

### Agent Instructions
```
MISSION: [Identical for all agents]
BRANCH: solution-{agent-id}
CONSTRAINTS: [Same constraints for all]
SUCCESS CRITERIA: [Identical metrics]
NO COORDINATION: Work independently until review phase
```

## Phase 2: Convergent Review (Collaborative)
### Review Process
1. **Cross-Review**: Each agent reviews all other solutions
2. **Strength Analysis**: Identify best aspects of each approach
3. **Weakness Identification**: Flag problems and limitations
4. **Synthesis Proposal**: Recommend optimal combination

### Review Template
```
REVIEWING: solution-{other-agent}
STRENGTHS:
- [Specific good implementations]
- [Clever approaches]
- [Robust error handling]

WEAKNESSES:
- [Problematic code]
- [Missing edge cases]
- [Performance issues]

RECOMMENDATION:
- Use: [Specific components to adopt]
- Avoid: [Components to reject]
- Modify: [Components needing changes]
```

## Phase 3: Consensus Building
### Final Integration
- **Synthesis Agent**: Creates final solution from best components
- **Validation**: All agents verify the integrated solution
- **Sign-off**: Consensus approval before merge

## Benefits
- **Redundancy**: Bad ideas filtered naturally
- **Diversity**: Multiple implementation perspectives
- **Quality**: Peer review ensures robustness
- **Innovation**: Independent thinking prevents groupthink

## Best Use Cases
- Complex architectural decisions
- Multiple valid implementation approaches
- High-risk or critical components
- When creativity and exploration are needed

## Team Size
- **Optimal**: 3-4 agents (manageable review load)
- **Minimum**: 2 agents (basic comparison)
- **Maximum**: 5-6 agents (review complexity limit)
- **Flexible**: Scale based on problem complexity and available resources
"""


def generate_pipeline_strategy():
    """Template for sequential pipeline development strategy"""
    return """
# Pipeline Strategy Template

## Overview
Agents work in sequence, each building on the previous agent's work.

## Structure
```
Agent A → Agent B → Agent C → Agent D
  ↓        ↓        ↓        ↓
Output   Enhanced  Refined  Final
```

## Phase Flow
1. **Foundation Agent**: Creates basic structure and core logic
2. **Enhancement Agent**: Adds features and functionality
3. **Refinement Agent**: Optimizes performance and error handling
4. **Validation Agent**: Tests, documents, and finalizes

## Handoff Protocol
```
FROM: {previous-agent}
TO: {next-agent}
COMPLETED:
- [Specific deliverables]
- [Files modified]
- [Tests passing]

NEXT TASKS:
- [Specific requirements]
- [Expected outputs]
- [Quality criteria]
```

## Benefits
- **Incremental Progress**: Each step builds value
- **Specialization**: Agents focus on their strengths
- **Quality Gates**: Each handoff includes validation
- **Clear Dependencies**: Linear progression is easy to track

## Best Use Cases
- Well-defined requirements
- Sequential dependencies
- When expertise specialization matters
- Predictable, structured problems
"""


def generate_swarm_strategy():
    """Template for swarm intelligence development strategy"""
    return """
# Swarm Strategy Template

## Overview
Many agents work on small, independent tasks that combine into emergent solutions.

## Structure
- **Task Decomposition**: Break problem into 10-20 micro-tasks
- **Agent Pool**: 5-8 agents pick up tasks dynamically
- **Coordination**: Lightweight task queue and status board
- **Emergence**: Solution emerges from combined micro-contributions

## Task Queue Example
```
[ ] Implement core feature
[ ] Add input validation
[ ] Create error handling
[ ] Write unit tests
[ ] Add logging
[ ] Update documentation
[✓] Setup data layer
[✓] Create data models
```

## Agent Behavior
1. **Pick Task**: Agent selects available task from queue
2. **Execute**: Complete task independently
3. **Integrate**: Merge changes to shared branch
4. **Report**: Update status and pick next task

## Benefits
- **Parallelism**: Maximum concurrent work
- **Flexibility**: Agents adapt to changing priorities
- **Resilience**: No single point of failure
- **Speed**: Many small tasks complete quickly

## Best Use Cases
- Large codebases with many independent components
- Bug fixes and maintenance tasks
- Feature development with clear boundaries
- When speed is more important than coordination
"""


def generate_red_team_strategy():
    """Template for adversarial red team development strategy"""
    return """
# Red Team Strategy Template

## Overview
Two teams work adversarially: one builds, one breaks, forcing robust solutions.

## Team Structure
### Blue Team (Builders)
- **Architect**: Designs system
- **Developer**: Implements features
- **Tester**: Creates test suites

### Red Team (Breakers)
- **Security Analyst**: Finds vulnerabilities
- **Chaos Engineer**: Tests failure scenarios
- **Edge Case Hunter**: Finds boundary conditions

## Process
1. **Blue Phase**: Blue team implements feature
2. **Red Phase**: Red team attempts to break it
3. **Analysis**: Document failures and attack vectors
4. **Hardening**: Blue team fixes discovered issues
5. **Repeat**: Continue until red team can't break it

## Attack Vectors
- **Security**: Access control bypass, input validation failures
- **Performance**: Load testing, resource exhaustion
- **Logic**: Edge cases, race conditions
- **Integration**: Interface misuse, dependency failures

## Benefits
- **Robustness**: Forces consideration of failure modes
- **Security**: Proactive vulnerability discovery
- **Quality**: Higher confidence in final product
- **Learning**: Teams learn from each other's perspectives

## Best Use Cases
- Security-critical applications
- High-reliability systems
- Complex integration scenarios
- When failure costs are high
"""


def generate_mob_programming_strategy():
    """Template for mob programming development strategy"""
    return """
# Mob Programming Strategy Template

## Overview
All agents collaborate simultaneously on the same code, with rotating roles.

## Roles (Rotating Every 15-30 Minutes)
- **Driver**: Types the code, implements decisions
- **Navigator**: Guides direction, makes tactical decisions
- **Observers**: Review code, suggest improvements, catch errors
- **Researcher**: Looks up documentation, investigates approaches

## Session Structure
1. **Problem Definition**: All agents understand the task
2. **Approach Discussion**: Brief strategy alignment
3. **Coding Session**: Rotate roles while coding
4. **Review**: Collective code review and refinement

## Communication Protocol
```
DRIVER: "I'm implementing the validation logic..."
NAVIGATOR: "Let's add error handling for edge cases"
OBSERVER: "Consider using a try-catch block here"
RESEARCHER: "The standard library has a validate() method we should use"
```

## Benefits
- **Knowledge Sharing**: All agents learn from each other
- **Quality**: Continuous review catches errors immediately
- **Consensus**: Decisions are made collectively
- **No Handoffs**: No context loss between agents

## Best Use Cases
- Complex problems requiring multiple perspectives
- Knowledge transfer scenarios
- When team alignment is critical
- Learning new technologies or domains
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
