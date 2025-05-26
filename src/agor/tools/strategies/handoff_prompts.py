"""
Handoff Prompts Strategy Implementation for AGOR.

This module provides comprehensive agent handoff coordination capabilities,
enabling seamless transitions between agents with standardized templates,
quality assurance, and specialized handoff scenarios.
"""

from datetime import datetime
from pathlib import Path


def generate_handoff_prompts(
    handoff_type: str = "standard",
    from_role: str = "developer",
    to_role: str = "reviewer",
    context: str = "",
) -> str:
    """Generate handoff prompts and coordination templates (hp hotkey)."""

    # Import handoff templates

    # Generate comprehensive handoff guidance
    implementation_details = f"""
## HANDOFF PROMPTS IMPLEMENTATION

### Handoff Type: {handoff_type}
### From Role: {from_role}
### To Role: {to_role}
### Context: {context if context else "General development handoff"}
### Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## HANDOFF PROMPT TEMPLATES

{_generate_handoff_prompt_templates(handoff_type, from_role, to_role)}

## ROLE-SPECIFIC PROMPTS

{_generate_role_specific_prompts(from_role, to_role, context)}

## HANDOFF COORDINATION PROTOCOLS

### Standard Handoff Process:
1. **Preparation Phase**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_PREP: [task] - Preparing handoff materials
   ```

2. **Handoff Creation**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_CREATED: [task] - Handoff document ready
   ```

3. **Handoff Delivery**:
   ```
   [FROM-AGENT] [TIMESTAMP] - HANDOFF_REQUEST: [to-agent] - [task] - [handoff-location]
   ```

4. **Handoff Reception**:
   ```
   [TO-AGENT] [TIMESTAMP] - HANDOFF_RECEIVED: [task] - Reviewing materials
   ```

5. **Handoff Acceptance**:
   ```
   [TO-AGENT] [TIMESTAMP] - HANDOFF_ACCEPTED: [task] - Work resumed
   ```

### Emergency Handoff Process:
1. **Immediate Notification**:
   ```
   [FROM-AGENT] [TIMESTAMP] - EMERGENCY_HANDOFF: [critical-issue] - Immediate assistance needed
   ```

2. **Quick Context Transfer**:
   ```
   [FROM-AGENT] [TIMESTAMP] - CONTEXT: [current-state] - [blocker] - [urgency-level]
   ```

3. **Emergency Response**:
   ```
   [TO-AGENT] [TIMESTAMP] - EMERGENCY_RESPONSE: [task] - Taking over immediately
   ```

## HANDOFF QUALITY ASSURANCE

### Handoff Checklist:
- [ ] **Work Status**: Current progress clearly documented
- [ ] **Deliverables**: All completed work identified and accessible
- [ ] **Context**: Technical decisions and rationale explained
- [ ] **Next Steps**: Clear tasks for receiving agent
- [ ] **Dependencies**: External dependencies and blockers identified
- [ ] **Quality**: Code quality and testing status documented
- [ ] **Timeline**: Estimated completion time provided
- [ ] **Communication**: Handoff logged in agentconvo.md

### Handoff Validation:
- [ ] **Completeness**: All required information provided
- [ ] **Clarity**: Instructions are clear and actionable
- [ ] **Accessibility**: All referenced files and resources available
- [ ] **Context**: Sufficient background for receiving agent
- [ ] **Quality**: Work meets standards for handoff

## SPECIALIZED HANDOFF SCENARIOS

{_generate_specialized_handoff_scenarios()}

## HANDOFF TEMPLATES LIBRARY

{_generate_handoff_templates_library()}

## HANDOFF METRICS & OPTIMIZATION

### Success Metrics:
- **Handoff Time**: Time from request to acceptance
- **Context Transfer**: Receiving agent understanding score
- **Continuation Quality**: Work quality after handoff
- **Rework Rate**: Percentage of work requiring revision

### Optimization Strategies:
- **Template Standardization**: Use consistent handoff formats
- **Context Documentation**: Maintain detailed work logs
- **Regular Checkpoints**: Frequent progress updates
- **Knowledge Sharing**: Cross-training and documentation

## HANDOFF TROUBLESHOOTING

### Common Issues:
1. **Incomplete Context**: Missing technical details or decisions
   - **Solution**: Use comprehensive handoff templates
   - **Prevention**: Regular documentation during work

2. **Unclear Next Steps**: Receiving agent unsure how to proceed
   - **Solution**: Provide specific, actionable tasks
   - **Prevention**: Break down work into clear steps

3. **Missing Dependencies**: Required resources not available
   - **Solution**: Document all dependencies and provide access
   - **Prevention**: Dependency mapping during planning

4. **Quality Issues**: Work not ready for handoff
   - **Solution**: Complete quality checks before handoff
   - **Prevention**: Continuous quality assurance

### Escalation Procedures:
1. **Agent Level**: Direct communication between agents
2. **Team Level**: Involve technical lead or coordinator
3. **Project Level**: Escalate to project management
4. **Emergency Level**: Immediate intervention required

## HANDOFF AUTOMATION

### Automated Handoff Generation:
```python
# Generate handoff document
from agor.tools.handoff_templates import generate_handoff_document
handoff = generate_handoff_document(
    problem_description="User authentication system",
    work_completed=["API endpoints", "Database schema", "Unit tests"],
    commits_made=["feat: add auth endpoints", "fix: validation logic"],
    current_status="80% complete - needs frontend integration",
    next_steps=["Create login UI", "Implement session management"],
    files_modified=["src/auth/api.py", "src/models/user.py"],
    context_notes="Uses JWT tokens, 24hr expiry",
    agent_role="Backend Developer",
    handoff_reason="Frontend development needed"
)
```

### Automated Prompt Generation:
```python
# Generate role-specific prompts
from agor.tools.agent_prompt_templates import generate_handoff_prompt
prompt = generate_handoff_prompt(
    from_agent="backend-dev",
    to_agent="frontend-dev",
    work_completed="Authentication API complete",
    next_tasks="Build login interface",
    context="JWT-based auth with 24hr tokens"
)
```

## NEXT STEPS

1. **Review Handoff Templates**: Validate prompt templates and formats
2. **Setup Handoff Directory**: Initialize .agor/handoffs/ structure
3. **Train Team**: Ensure all agents understand handoff protocols
4. **Monitor Quality**: Track handoff success metrics
5. **Iterate and Improve**: Refine templates based on usage
"""

    # Create .agor directory
    agor_dir = Path(".agor")
    agor_dir.mkdir(exist_ok=True)

    # Save to handoff prompts file
    handoff_file = agor_dir / "handoff-prompts.md"
    handoff_file.write_text(implementation_details)

    # Create handoff templates directory
    _create_handoff_templates_directory()

    # Create role-specific prompt files
    _create_role_specific_prompt_files(from_role, to_role)

    # Create handoff coordination file
    _create_handoff_coordination_file(handoff_type, from_role, to_role)

    return f"""✅ Handoff Prompts Generated

**Handoff Type**: {handoff_type}
**From Role**: {from_role}
**To Role**: {to_role}
**Context**: {context if context else "General development"}

**Generated Resources**:
- Comprehensive handoff prompt templates
- Role-specific coordination protocols
- Quality assurance checklists
- Specialized handoff scenarios
- Automation examples and scripts

**Files Created**:
- `.agor/handoff-prompts.md` - Complete handoff guidance
- `.agor/handoff-templates/` - Template library
- `.agor/role-prompts/` - Role-specific prompts
- `.agor/handoff-coordination.md` - Coordination protocols

**Next Steps**:
1. Review handoff templates and customize as needed
2. Train team on handoff protocols
3. Begin using standardized handoff processes
4. Monitor handoff quality and optimize

**Ready for seamless agent handoffs!**
"""


def _generate_handoff_prompt_templates(
    handoff_type: str, from_role: str, to_role: str
) -> str:
    """Generate handoff prompt templates."""
    if handoff_type == "emergency":
        return f"""
### Emergency Handoff Template
```
EMERGENCY HANDOFF: {from_role} → {to_role}

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
    elif handoff_type == "planned":
        return f"""
### Planned Handoff Template
```
PLANNED HANDOFF: {from_role} → {to_role}

SCHEDULED: [Date and time]
REASON: [Why handoff is happening]
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
### Standard Handoff Template
```
HANDOFF: {from_role} → {to_role}

COMPLETED WORK:
- [List of deliverables with locations]
- [Quality checks performed]
- [Tests passing]

CURRENT STATUS:
- [Overall progress percentage]
- [What's working well]
- [Known issues or limitations]

NEXT STEPS:
- [Immediate tasks for receiving agent]
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
    """Generate role-specific handoff prompts."""
    role_prompts = {
        "developer": {
            "to_reviewer": """
### Developer → Reviewer Handoff
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

**Handoff Criteria**:
- All tests passing
- Code follows team standards
- Documentation is complete
- No obvious security issues
""",
            "to_tester": """
### Developer → Tester Handoff
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

**Handoff Criteria**:
- Feature is functionally complete
- Basic testing completed
- Test environment ready
- Test data available
""",
            "to_devops": """
### Developer → DevOps Handoff
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

**Handoff Criteria**:
- Code is deployment-ready
- Configuration is documented
- Dependencies are specified
- Monitoring requirements defined
""",
        },
        "reviewer": {
            "to_developer": """
### Reviewer → Developer Handoff
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

**Handoff Criteria**:
- Review is complete
- Issues are prioritized
- Fix guidance is clear
- Timeline is realistic
"""
        },
        "tester": {
            "to_developer": """
### Tester → Developer Handoff
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

**Handoff Criteria**:
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
### {from_role.title()} → {to_role.title()} Handoff
**Focus**: Role transition and work continuation

**{from_role.title()} Deliverables**:
- Completed work with documentation
- Current status and progress
- Next steps and requirements
- Context and technical details

**{to_role.title()} Tasks**:
- Review handoff materials
- Continue work from current state
- Address any immediate issues
- Maintain quality standards

**Handoff Criteria**:
- Work is properly documented
- Context is clearly explained
- Next steps are actionable
- Quality standards maintained
"""


def _generate_specialized_handoff_scenarios() -> str:
    """Generate specialized handoff scenarios."""
    return """
### Cross-Functional Handoffs

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

### Temporal Handoffs

#### End of Sprint
- **Focus**: Sprint completion, next sprint preparation
- **Key Items**: Sprint summary, backlog updates, lessons learned
- **Success Criteria**: Clean transition to next sprint

#### End of Phase
- **Focus**: Phase completion, next phase readiness
- **Key Items**: Phase deliverables, quality gates, next phase planning
- **Success Criteria**: Phase objectives met, next phase can begin

#### Project Completion
- **Focus**: Project closure, maintenance handoff
- **Key Items**: Final deliverables, documentation, support procedures
- **Success Criteria**: Project successfully closed, maintenance ready

### Emergency Handoffs

#### Critical Bug
- **Focus**: Immediate issue resolution
- **Key Items**: Bug description, impact assessment, immediate fixes
- **Success Criteria**: Critical issue resolved quickly

#### Agent Unavailability
- **Focus**: Work continuation without original agent
- **Key Items**: Current state, immediate tasks, contact information
- **Success Criteria**: Work continues without significant delay

#### Deadline Pressure
- **Focus**: Accelerated delivery, scope management
- **Key Items**: Priority tasks, scope decisions, resource needs
- **Success Criteria**: Deadline met with acceptable quality
"""


def _generate_handoff_templates_library() -> str:
    """Generate handoff templates library."""
    return """
### Quick Handoff Templates

#### Minimal Handoff
```
QUICK HANDOFF: [from] → [to]
TASK: [brief description]
STATUS: [current state]
NEXT: [immediate action needed]
FILES: [key files to check]
```

#### Bug Fix Handoff
```
BUG HANDOFF: [from] → [to]
BUG: [description and impact]
REPRODUCTION: [steps to reproduce]
INVESTIGATION: [what's been tried]
NEXT: [suggested approach]
```

#### Feature Handoff
```
FEATURE HANDOFF: [from] → [to]
FEATURE: [description and requirements]
PROGRESS: [what's implemented]
REMAINING: [what's left to do]
TESTS: [testing status]
```

#### Review Handoff
```
REVIEW HANDOFF: [from] → [to]
CODE: [location and scope]
CRITERIA: [review requirements]
TIMELINE: [review deadline]
CONTACT: [for questions]
```

### Comprehensive Templates

#### Full Project Handoff
- Complete project context
- All deliverables and documentation
- Team structure and responsibilities
- Timeline and milestones
- Risk assessment and mitigation
- Success criteria and metrics

#### Phase Transition Handoff
- Phase completion summary
- Quality gate validation
- Next phase preparation
- Resource allocation
- Dependency management
- Stakeholder communication
"""


def _create_handoff_templates_directory():
    """Create handoff templates directory structure."""
    templates_dir = Path(".agor") / "handoff-templates"
    templates_dir.mkdir(exist_ok=True)

    # Create template files
    templates = {
        "standard-handoff.md": """
# Standard Handoff Template

## Handoff Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID]
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

## Next Steps
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
        "emergency-handoff.md": """
# Emergency Handoff Template

## Emergency Information
- **From**: [Agent Role/ID]
- **To**: [Agent Role/ID]
- **Date**: [Timestamp]
- **Urgency**: [Critical/High/Medium]

## Critical Issue
**Problem**: [Description]
**Impact**: [Business/technical impact]
**Deadline**: [When this must be resolved]

## Current State
**What's Working**: [Functional components]
**What's Broken**: [Failed components]
**Last Known Good**: [Previous working state]

## Immediate Actions
1. [First priority action]
2. [Second priority action]
3. [Fallback option]

## Emergency Contacts
- **Original Agent**: [Contact info]
- **Technical Lead**: [Contact info]
- **Escalation**: [Contact info]
""",
        "review-handoff.md": """
# Review Handoff Template

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
# {from_role.title()} to {to_role.title()} Handoff Prompts

## Role Transition Context
**From Role**: {from_role}
**To Role**: {to_role}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Handoff Prompt
{_generate_role_specific_prompts(from_role, to_role, "")}

## Communication Templates

### Handoff Request
```
[{from_role.upper()}] [TIMESTAMP] - HANDOFF_REQUEST: {to_role} - [task-description] - [handoff-location]
```

### Handoff Acceptance
```
[{to_role.upper()}] [TIMESTAMP] - HANDOFF_ACCEPTED: [task-description] - Work resumed
```

### Progress Update
```
[{to_role.upper()}] [TIMESTAMP] - PROGRESS: [task-description] - [status] - [next-steps]
```

## Quality Checklist
- [ ] All deliverables documented
- [ ] Context clearly explained
- [ ] Next steps actionable
- [ ] Resources accessible
- [ ] Timeline realistic

## Success Criteria
- Receiving agent understands the work
- Work continues without significant delay
- Quality standards maintained
- Communication protocols followed
"""
    prompt_file.write_text(prompt_content)


def _create_handoff_coordination_file(handoff_type: str, from_role: str, to_role: str):
    """Create handoff coordination tracking file."""
    coordination_file = Path(".agor") / "handoff-coordination.md"
    coordination_content = f"""
# Handoff Coordination Tracking

## Current Handoff Configuration
- **Type**: {handoff_type}
- **From Role**: {from_role}
- **To Role**: {to_role}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Active Handoffs

### Pending Handoffs
- [No pending handoffs currently]

### In Progress Handoffs
- [No handoffs in progress currently]

### Completed Handoffs
- [No completed handoffs yet]

## Handoff Metrics

### Success Rate
- **Total Handoffs**: 0
- **Successful**: 0
- **Failed**: 0
- **Success Rate**: N/A

### Average Times
- **Preparation Time**: N/A
- **Transfer Time**: N/A
- **Acceptance Time**: N/A
- **Total Handoff Time**: N/A

### Quality Metrics
- **Context Clarity Score**: N/A
- **Continuation Success Rate**: N/A
- **Rework Required**: N/A

## Handoff Process Improvements

### Identified Issues
- [Issues will be tracked here]

### Process Optimizations
- [Optimizations will be documented here]

### Template Updates
- [Template improvements will be noted here]

## Communication Log

### Handoff Requests
- [Handoff requests will be logged here]

### Status Updates
- [Status updates will be tracked here]

### Issue Reports
- [Issues and resolutions will be documented here]
"""
    coordination_file.write_text(coordination_content)
