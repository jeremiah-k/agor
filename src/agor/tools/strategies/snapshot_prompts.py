"""
Snapshot Prompts Strategy Implementation for AGOR.

This module provides comprehensive agent snapshot coordination capabilities,
enabling seamless transitions and context preservation between agents
(or for solo use) with standardized templates, quality assurance,
and specialized snapshot scenarios.
"""

from datetime import datetime
from pathlib import Path


def generate_snapshot_prompts(  # Renamed function
    snapshot_type: str = "standard",  # Renamed parameter
    from_role: str = "developer",
    to_role: str = "reviewer",  # Can be same as from_role for self-snapshots
    context: str = "",
) -> str:
    """Generate snapshot prompts and coordination templates (hp hotkey)."""

    # Import snapshot_templates (already updated in previous step)

    # Generate comprehensive snapshot guidance
    implementation_details = f"""
## SNAPSHOT PROMPTS IMPLEMENTATION

### Snapshot Type: {snapshot_type}
### From Role: {from_role}
### To Role: {to_role}
### Context: {context if context else "General development snapshot"}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## SNAPSHOT PROMPT TEMPLATES

{_generate_snapshot_prompt_templates(snapshot_type, from_role, to_role)}

## ROLE-SPECIFIC PROMPTS

{_generate_role_specific_prompts(from_role, to_role, context)}

## SNAPSHOT COORDINATION PROTOCOLS

### Standard Snapshot Process:
1. **Preparation Phase**:
   ```
   [FROM-AGENT] [TIMESTAMP] - SNAPSHOT_PREP: [task] - Preparing snapshot materials
   ```

2. **Snapshot Creation**:
   ```
   [FROM-AGENT] [TIMESTAMP] - SNAPSHOT_CREATED: [task] - Snapshot document ready
   ```

3. **Snapshot Delivery/Storage**:
   ```
   [FROM-AGENT] [TIMESTAMP] - SNAPSHOT_NOTICE: [to-agent/storage] - [task] - [snapshot-location]
   ```

4. **Snapshot Reception (if applicable)**:
   ```
   [TO-AGENT] [TIMESTAMP] - SNAPSHOT_RECEIVED: [task] - Reviewing materials
   ```

5. **Snapshot Acceptance/Usage (if applicable)**:
   ```
   [TO-AGENT] [TIMESTAMP] - SNAPSHOT_ACCEPTED: [task] - Work resumed or context loaded
   ```

### Emergency Snapshot Process:
1. **Immediate Notification**:
   ```
   [FROM-AGENT] [TIMESTAMP] - EMERGENCY_SNAPSHOT: [critical-issue] - Immediate context capture needed
   ```

2. **Quick Context Transfer**:
   ```
   [FROM-AGENT] [TIMESTAMP] - CONTEXT: [current-state] - [blocker] - [urgency-level]
   ```

3. **Emergency Response (if applicable)**:
   ```
   [TO-AGENT] [TIMESTAMP] - EMERGENCY_RESPONSE: [task] - Taking over immediately using snapshot
   ```

## SNAPSHOT QUALITY ASSURANCE

### Snapshot Checklist:
- [ ] **Work Status**: Current progress clearly documented
- [ ] **Deliverables**: All completed work identified and accessible
- [ ] **Context**: Technical decisions and rationale explained
- [ ] **Next Steps**: Clear tasks for receiving agent (if applicable) or future self
- [ ] **Dependencies**: External dependencies and blockers identified
- [ ] **Quality**: Code quality and testing status documented
- [ ] **Timeline**: Estimated completion time provided (if applicable)
- [ ] **Communication**: Snapshot logged in agentconvo.md (if applicable)

### Snapshot Validation:
- [ ] **Completeness**: All required information provided
- [ ] **Clarity**: Instructions are clear and actionable
- [ ] **Accessibility**: All referenced files and resources available
- [ ] **Context**: Sufficient background for receiving agent or future self
- [ ] **Quality**: Work meets standards for snapshot

## SPECIALIZED SNAPSHOT SCENARIOS

{_generate_specialized_snapshot_scenarios()}

## SNAPSHOT TEMPLATES LIBRARY

{_generate_snapshot_templates_library()}

## SNAPSHOT METRICS & OPTIMIZATION

### Success Metrics:
- **Snapshot Creation Time**: Time to generate a complete snapshot
- **Context Transfer Clarity**: Receiving agent's (or future self's) understanding score
- **Continuation Quality**: Work quality after loading snapshot
- **Rework Rate**: Percentage of work requiring revision after loading snapshot

### Optimization Strategies:
- **Template Standardization**: Use consistent snapshot formats
- **Context Documentation**: Maintain detailed work logs for easy snapshotting
- **Regular Checkpoints**: Frequent progress updates (can be mini-snapshots)
- **Knowledge Sharing**: Cross-training and documentation to improve context understanding

## SNAPSHOT TROUBLESHOOTING

### Common Issues:
1. **Incomplete Context**: Missing technical details or decisions
   - **Solution**: Use comprehensive snapshot templates
   - **Prevention**: Regular documentation during work

2. **Unclear Next Steps**: Receiving agent (or future self) unsure how to proceed
   - **Solution**: Provide specific, actionable tasks
   - **Prevention**: Break down work into clear steps

3. **Missing Dependencies**: Required resources not available
   - **Solution**: Document all dependencies and provide access
   - **Prevention**: Dependency mapping during planning

4. **Quality Issues**: Work not ready for snapshot (if for transition)
   - **Solution**: Complete quality checks before creating snapshot for others
   - **Prevention**: Continuous quality assurance

### Escalation Procedures (for multi-agent snapshots):
1. **Agent Level**: Direct communication between agents
2. **Team Level**: Involve technical lead or coordinator
3. **Project Level**: Escalate to project management
4. **Emergency Level**: Immediate intervention required

## SNAPSHOT AUTOMATION

### Automated Snapshot Generation:
```python
# Generate snapshot document
from agor.tools.snapshot_templates import generate_snapshot_document 
snapshot_doc = generate_snapshot_document( 
    problem_description="User authentication system",
    work_completed=["API endpoints", "Database schema", "Unit tests"],
    commits_made=["feat: add auth endpoints", "fix: validation logic"],
    current_status="80% complete - needs frontend integration",
    next_steps=["Create login UI", "Implement session management"],
    files_modified=["src/auth/api.py", "src/models/user.py"],
    context_notes="Uses JWT tokens, 24hr expiry",
    agent_role="Backend Developer",
    snapshot_reason="Frontend development needed" # Updated parameter name
)
```

### Automated Prompt Generation:
```python
# Generate role-specific prompts
from agor.tools.agent_prompt_templates import generate_snapshot_prompt # Assuming this function is also updated/renamed
prompt = generate_snapshot_prompt( # Assuming this function is also updated/renamed
    from_agent="backend-dev",
    to_agent="frontend-dev",
    work_completed="Authentication API complete",
    next_tasks="Build login interface",
    context="JWT-based auth with 24hr tokens"
)
```

## NEXT STEPS

1. **Review Snapshot Templates**: Validate prompt templates and formats
2. **Setup Snapshot Directory**: Initialize .agor/snapshots/ structure
3. **Train Team**: Ensure all agents understand snapshot protocols
4. **Monitor Quality**: Track snapshot success metrics
5. **Iterate and Improve**: Refine templates based on usage
"""

    # Create .agor directory
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)

    # Save to snapshot prompts file
    snapshot_prompts_file = agor_dir / "snapshot-prompts.md"  # Renamed file
    snapshot_prompts_file.write_text(implementation_details)

    # Create snapshot templates directory
    _create_snapshot_templates_directory()  # Renamed function

    # Create role-specific prompt files
    _create_role_specific_prompt_files(from_role, to_role)

    # Create snapshot coordination file
    _create_snapshot_coordination_file(
        snapshot_type, from_role, to_role
    )  # Renamed function

    return f"""✅ Snapshot Prompts Generated

**Snapshot Type**: {snapshot_type}
**From Role**: {from_role}
**To Role**: {to_role}
**Context**: {context if context else "General development"}

**Generated Resources**:
- Comprehensive snapshot prompt templates
- Role-specific coordination protocols
- Quality assurance checklists
- Specialized snapshot scenarios
- Automation examples and scripts

**Files Created**:
- `.agor/snapshot-prompts.md` - Complete snapshot guidance
- `.agor/snapshot-templates/` - Template library
- `.agor/role-prompts/` - Role-specific prompts
- `.agor/snapshot-coordination.md` - Coordination protocols

**Next Steps**:
1. Review snapshot templates and customize as needed
2. Train team on snapshot protocols
3. Begin using standardized snapshot processes
4. Monitor snapshot quality and optimize

**Ready for seamless agent context management and transitions!**
"""


def _generate_snapshot_prompt_templates(  # Renamed function
    snapshot_type: str, from_role: str, to_role: str  # Renamed parameter
) -> str:
    """Generate snapshot prompt templates."""
    if snapshot_type == "emergency":  # Renamed parameter
        return f"""
### Emergency Snapshot Template
```
EMERGENCY SNAPSHOT: {from_role} → {to_role}

CRITICAL ISSUE: [Describe the urgent problem]
CURRENT STATE: [What's working/broken]
IMMEDIATE ACTION NEEDED: [What must be done now]
TIME CONSTRAINT: [Deadline or urgency level]

CONTEXT:
- [Key technical details]
- [Recent changes that may be related]
- [Resources and access needed]

EMERGENCY CONTACT: [How to reach original agent if needed]
```
"""
    elif snapshot_type == "planned":  # Renamed parameter
        return f"""
### Planned Snapshot Template
```
PLANNED SNAPSHOT: {from_role} → {to_role}

SCHEDULED: [Date and time]
REASON: [Why snapshot is happening]
PREPARATION TIME: [How long to prepare]

WORK COMPLETED:
- [Deliverable 1 with location]
- [Deliverable 2 with location]
- [Quality gates passed]

NEXT PHASE:
- [Task 1 for receiving agent]
- [Task 2 for receiving agent]
- [Success criteria]

TRANSITION PLAN:
- [Knowledge transfer sessions]
- [Documentation review]
- [Overlap period if needed]
```
"""
    else:  # standard
        return f"""
### Standard Snapshot Template
```
SNAPSHOT: {from_role} → {to_role}

COMPLETED WORK:
- [List of deliverables with locations]
- [Quality checks performed]
- [Tests passing]

CURRENT STATUS:
- [Overall progress percentage]
- [What's working well]
- [Known issues or limitations]

NEXT STEPS:
- [Immediate tasks for receiving agent (if applicable)]
- [Medium-term objectives]
- [Success criteria]

CONTEXT:
- [Technical decisions made]
- [Architecture choices]
- [Important constraints or requirements]

RESOURCES:
- [Documentation links]
- [Code repositories]
- [Access credentials or permissions needed]
```
"""


def _generate_role_specific_prompts(from_role: str, to_role: str, context: str) -> str:
    """Generate role-specific snapshot prompts."""
    role_prompts = {
        "developer": {
            "to_reviewer": """
### Developer → Reviewer Snapshot
**Focus**: Code quality, standards compliance, security review

**Developer Deliverables**:
- Complete, tested code implementation
- Unit tests with >80% coverage
- Documentation for new features
- Self-review checklist completed

**Reviewer Tasks**:
- Code quality assessment
- Security vulnerability scan
- Performance impact analysis
- Standards compliance verification

**Snapshot Criteria**:
- All tests passing
- Code follows team standards
- Documentation is complete
- No obvious security issues
""",
            "to_tester": """
### Developer → Tester Snapshot
**Focus**: Functional testing, integration validation, user acceptance

**Developer Deliverables**:
- Working feature implementation
- Unit tests and test data
- Feature documentation
- Known limitations or edge cases

**Tester Tasks**:
- Functional testing execution
- Integration testing
- User acceptance validation
- Bug reporting and tracking

**Snapshot Criteria**:
- Feature is functionally complete
- Basic testing completed
- Test environment ready
- Test data available
""",
            "to_devops": """
### Developer → DevOps Snapshot
**Focus**: Deployment readiness, infrastructure requirements, monitoring

**Developer Deliverables**:
- Production-ready code
- Deployment configuration
- Infrastructure requirements
- Monitoring and logging setup

**DevOps Tasks**:
- Deployment pipeline setup
- Infrastructure provisioning
- Monitoring configuration
- Performance optimization

**Snapshot Criteria**:
- Code is deployment-ready
- Configuration is documented
- Dependencies are specified
- Monitoring requirements defined
""",
        },
        "reviewer": {
            "to_developer": """
### Reviewer → Developer Snapshot
**Focus**: Required fixes, improvements, optimization recommendations

**Reviewer Deliverables**:
- Detailed review report
- Prioritized fix list
- Security recommendations
- Performance suggestions

**Developer Tasks**:
- Address critical issues
- Implement security fixes
- Optimize performance
- Update documentation

**Snapshot Criteria**:
- Review is complete
- Issues are prioritized
- Fix guidance is clear
- Timeline is realistic
"""
        },
        "tester": {
            "to_developer": """
### Tester → Developer Snapshot
**Focus**: Bug fixes, test failures, quality improvements

**Tester Deliverables**:
- Test results and reports
- Bug reports with reproduction steps
- Test coverage analysis
- Quality metrics

**Developer Tasks**:
- Fix identified bugs
- Improve test coverage
- Address quality issues
- Update implementation

**Snapshot Criteria**:
- Testing is complete
- Bugs are documented
- Reproduction steps provided
- Priority levels assigned
"""
        },
    }

    if from_role in role_prompts and f"to_{to_role}" in role_prompts[from_role]:
        return role_prompts[from_role][f"to_{to_role}"]
    else:
        return f"""
### {from_role.title()} → {to_role.title()} Snapshot
**Focus**: Role transition and work continuation (or context saving)

**{from_role.title()} Deliverables**:
- Completed work with documentation
- Current status and progress
- Next steps and requirements
- Context and technical details

**{to_role.title()} Tasks (if applicable)**:
- Review snapshot materials
- Continue work from current state
- Address any immediate issues
- Maintain quality standards

**Snapshot Criteria**:
- Work is properly documented
- Context is clearly explained
- Next steps are actionable (if applicable)
- Quality standards maintained
"""


def _generate_specialized_snapshot_scenarios() -> str:  # Renamed function
    """Generate specialized snapshot scenarios."""
    return """
### Cross-Functional Snapshots

#### Backend → Frontend
- **Focus**: API integration, data contracts, user experience
- **Key Items**: API documentation, data schemas, authentication flow
- **Success Criteria**: Frontend can consume APIs successfully

#### Frontend → Backend
- **Focus**: Data requirements, performance needs, user workflows
- **Key Items**: User stories, data models, performance requirements
- **Success Criteria**: Backend supports all frontend needs

#### Development → Operations
- **Focus**: Deployment readiness, monitoring, scalability
- **Key Items**: Deployment configs, monitoring setup, scaling requirements
- **Success Criteria**: System deploys and runs reliably

### Temporal Snapshots

#### End of Sprint
- **Focus**: Sprint completion, next sprint preparation
- **Key Items**: Sprint summary, backlog updates, lessons learned
- **Success Criteria**: Clean transition to next sprint

#### End of Phase
- **Focus**: Phase completion, next phase readiness
- **Key Items**: Phase deliverables, quality gates, next phase planning
- **Success Criteria**: Phase objectives met, next phase can begin

#### Project Completion
- **Focus**: Project closure, maintenance snapshot
- **Key Items**: Final deliverables, documentation, support procedures
- **Success Criteria**: Project successfully closed, maintenance ready

### Emergency Snapshots

#### Critical Bug
- **Focus**: Immediate issue resolution, snapshot of state before fix attempt
- **Key Items**: Bug description, impact assessment, current state before intervention
- **Success Criteria**: Critical issue resolved quickly, state documented

#### Agent Unavailability
- **Focus**: Work continuation without original agent, snapshot of last known good state
- **Key Items**: Current state, immediate tasks, contact information
- **Success Criteria**: Work continues without significant delay

#### Deadline Pressure
- **Focus**: Accelerated delivery, scope management, snapshot of current best state
- **Key Items**: Priority tasks, scope decisions, resource needs
- **Success Criteria**: Deadline met with acceptable quality
"""


def _generate_snapshot_templates_library() -> str:  # Renamed function
    """Generate snapshot templates library."""
    return """
### Quick Snapshot Templates

#### Minimal Snapshot
```
QUICK SNAPSHOT: [from] → [to/self]
TASK: [brief description]
STATUS: [current state]
NEXT: [immediate action needed (if any)]
FILES: [key files to check]
```

#### Bug Fix Snapshot
```
BUG FIX SNAPSHOT: [from] → [to/self]
BUG: [description and impact]
REPRODUCTION: [steps to reproduce]
INVESTIGATION: [what's been tried]
NEXT: [suggested approach]
```

#### Feature Snapshot
```
FEATURE SNAPSHOT: [from] → [to/self]
FEATURE: [description and requirements]
PROGRESS: [what's implemented]
REMAINING: [what's left to do]
TESTS: [testing status]
```

#### Review Snapshot (Code for Review)
```
REVIEW SNAPSHOT: [from] → [to]
CODE: [location and scope]
CRITERIA: [review requirements]
TIMELINE: [review deadline]
CONTACT: [for questions]
```

### Comprehensive Templates

#### Full Project Snapshot
- Complete project context
- All deliverables and documentation
- Team structure and responsibilities
- Timeline and milestones
- Risk assessment and mitigation
- Success criteria and metrics

#### Phase Transition Snapshot
- Phase completion summary
- Quality gate validation
- Next phase preparation
- Resource allocation
- Dependency management
- Stakeholder communication
"""


def _create_snapshot_templates_directory():  # Renamed function
    """Create snapshot templates directory structure."""
    templates_dir = Path(".agor") / "snapshot-templates"  # Renamed directory
    templates_dir.mkdir(exist_ok=True)

    # Create template files
    templates = {
        "standard-snapshot.md": """ # Renamed file
# Standard Snapshot Template

## Snapshot Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID or Self]
- **Date**: [Timestamp]
- **Type**: Standard

## Work Completed
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

## Current Status
**Progress**: [Percentage]%
**Quality**: [Status]
**Testing**: [Status]

## Next Steps (if applicable)
1. [Immediate task]
2. [Follow-up task]
3. [Future consideration]

## Context & Notes
[Important technical details, decisions, constraints]

## Resources
- [Documentation links]
- [Code repositories]
- [Access requirements]
""",
        "emergency-snapshot.md": """ # Renamed file
# Emergency Snapshot Template

## Emergency Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID or Self]
- **Date**: [Timestamp]
- **Urgency**: [Critical/High/Medium]

## Critical Issue (if applicable)
**Problem**: [Description]
**Impact**: [Business/technical impact]
**Deadline**: [When this must be resolved]

## Current State
**What's Working**: [Functional components]
**What's Broken**: [Failed components]
**Last Known Good**: [Previous working state]

## Immediate Actions (if applicable)
1. [First priority action]
2. [Second priority action]
3. [Fallback option]

## Emergency Contacts (if applicable)
- **Original Agent**: [Contact info]
- **Technical Lead**: [Contact info]
- **Escalation**: [Contact info]
""",
        "review-snapshot.md": """ # Renamed file
# Review Snapshot Template (Code for Review)

## Review Information
- **Reviewer**: [Agent Role/ID]
- **Developer**: [Agent Role/ID]
- **Date**: [Timestamp]
- **Scope**: [What's being reviewed]

## Review Criteria
- [ ] Code quality and standards
- [ ] Security considerations
- [ ] Performance impact
- [ ] Test coverage
- [ ] Documentation completeness

## Code Location
**Repository**: [Repo URL/path]
**Branch**: [Branch name]
**Files**: [List of files to review]
**Commits**: [Relevant commit hashes]

## Review Timeline
**Deadline**: [When review must be complete]
**Priority**: [High/Medium/Low]
**Complexity**: [Simple/Medium/Complex]

## Review Results
[To be filled by reviewer]

## Action Items
[To be filled by reviewer]
""",
    }

    for filename, content in templates.items():
        template_file = templates_dir / filename
        template_file.write_text(content)


def _create_role_specific_prompt_files(from_role: str, to_role: str):
    """Create role-specific prompt files."""
    prompts_dir = Path(".agor") / "role-prompts"
    prompts_dir.mkdir(exist_ok=True)

    # Create role-specific prompt file
    prompt_file = prompts_dir / f"{from_role}-to-{to_role}.md"
    prompt_content = f"""
# {from_role.title()} to {to_role.title()} Snapshot Prompts

## Role Transition Context
**From Role**: {from_role}
**To Role**: {to_role}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Snapshot Prompt
{_generate_role_specific_prompts(from_role, to_role, "")}

## Communication Templates

### Snapshot Creation Notice
```
[{from_role.upper()}] [TIMESTAMP] - SNAPSHOT_CREATED: {to_role} - [task-description] - [snapshot-location]
```

### Snapshot Acceptance (if applicable)
```
[{to_role.upper()}] [TIMESTAMP] - SNAPSHOT_ACCEPTED: [task-description] - Work resumed or context loaded
```

### Progress Update
```
[{to_role.upper()}] [TIMESTAMP] - PROGRESS: [task-description] - [status] - [next-steps]
```

## Quality Checklist
- [ ] All deliverables documented
- [ ] Context clearly explained
- [ ] Next steps actionable (if applicable)
- [ ] Resources accessible
- [ ] Timeline realistic (if applicable)

## Success Criteria
- Receiving agent (or future self) understands the work
- Work continues without significant delay (if applicable)
- Quality standards maintained
- Communication protocols followed (if applicable)
"""
    prompt_file.write_text(prompt_content)


def _create_snapshot_coordination_file(
    snapshot_type: str, from_role: str, to_role: str
):  # Renamed function
    """Create snapshot coordination tracking file."""
    coordination_file = Path(".agor") / "snapshot-coordination.md"  # Renamed file
    coordination_content = f"""
# Snapshot Coordination Tracking

## Current Snapshot Configuration
- **Type**: {snapshot_type}
- **From Role**: {from_role}
- **To Role**: {to_role}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Active Snapshots

### Pending Snapshots
- [No pending snapshots currently]

### In Progress Snapshots (being worked on from)
- [No snapshots in progress currently]

### Completed/Archived Snapshots
- [No completed/archived snapshots yet]

## Snapshot Metrics

### Success Rate (for transition snapshots)
- **Total Snapshots**: 0
- **Successful Transitions**: 0
- **Failed Transitions**: 0
- **Success Rate**: N/A

### Average Times (for transition snapshots)
- **Preparation Time**: N/A
- **Transfer Time**: N/A
- **Acceptance Time**: N/A
- **Total Transition Time**: N/A

### Quality Metrics
- **Context Clarity Score**: N/A
- **Continuation Success Rate**: N/A
- **Rework Required**: N/A

## Snapshot Process Improvements

### Identified Issues
- [Issues will be tracked here]

### Process Optimizations
- [Optimizations will be documented here]

### Template Updates
- [Template improvements will be noted here]

## Communication Log (for multi-agent snapshots)

### Snapshot Creation Notices
- [Snapshot creation will be logged here]

### Status Updates
- [Status updates will be tracked here]

### Issue Reports
- [Issues and resolutions will be documented here]
"""
    coordination_file.write_text(coordination_content)
