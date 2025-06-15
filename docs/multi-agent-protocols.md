# 🤝 Multi-Agent Coordination Protocols

**Purpose**: Comprehensive protocols for coordinating multiple AI agents in AGOR development workflows. This document provides concrete implementation guidelines for all coordination strategies and communication patterns.

## 🎯 Protocol Overview

AGOR supports structured multi-agent coordination through:

- **5 Core Strategies** with specific implementation protocols
- **Mandatory Communication Patterns** for agent coordination
- **Session Management** with automatic handoff generation
- **Role-Based Workflows** with clear responsibilities

## 📋 Core Coordination Requirements

### Universal Agent Requirements

**Every agent MUST:**

1. **Read Documentation First**: README_ai.md, AGOR_INSTRUCTIONS.md, agent-start-here.md
2. **Select Appropriate Role**: Worker Agent or Project Coordinator
3. **Use Dev Tools**: All coordination via our backtick processing functions
4. **Generate Session End Prompts**: Mandatory before ending any session
5. **Follow Git Protocols**: Pull before work, commit frequently, push regularly

### Communication Protocol

**IMPORTANT**: The `.agor` directory does NOT exist on main or feature branches. It only exists on dedicated memory branches and is accessed exclusively through our dev tools functions.

**Memory Branch System**:

- **Memory branches**: Created automatically by dev tools (e.g., `agor/mem/2025-06-07_1300`)
- **Cross-branch commits**: Dev tooling commits to memory branches without switching your working branch
- **Coordination files**: Stored on memory branches, accessed via dev tools functions
- **No direct file access**: Never manually create/edit `.agor` files

**Coordination Through Dev Tools**:

```python
# Create snapshots and memories (auto-commits to memory branches)
auto_commit_memory(content, "session_progress", "agent_id")
generate_mandatory_session_end_prompt(work_completed, status, instructions, context)

# Load previous snapshots/memories (reads from memory branches)
# Use dev tools functions to access coordination data
```

**Required Functions**:

```python
# Mandatory session end
generate_mandatory_session_end_prompt(
    work_completed=['List of completed items'],
    current_status='Current project status',
    next_agent_instructions=['Instructions for next agent'],
    critical_context='Important context to preserve',
    files_modified=['Files modified this session']
)

# Meta feedback generation
generate_meta_feedback(
    current_project='Project name',
    agor_issues_encountered=['Issues with AGOR'],
    suggested_improvements=['Suggestions for AGOR'],
    workflow_friction_points=['Friction points'],
    positive_experiences=['Positive experiences']
)
```

## 🔄 Strategy Implementation Protocols

### 1. Parallel Divergent Strategy

**Use Case**: Multiple approaches to the same problem
**Team Size**: 2–4 agents
**Coordination Level**: Medium

**Implementation Protocol**:

```python
# Coordinator initializes
from agor.tools.dev_tools import generate_handoff_prompt_only

# Phase 1: Divergent Work (No Coordination)
outputs = generate_handoff_prompt_only(
    task_description='Parallel Divergent: [Problem Description]',
    work_completed=['Strategy initialized', 'Agent assignments created'],
    next_steps=[
        'Agent 1: Approach A on branch solution-agent1',
        'Agent 2: Approach B on branch solution-agent2',
        'Agent 3: Approach C on branch solution-agent3',
        'NO coordination until all complete'
    ],
    brief_context='Parallel Divergent Phase 1: Independent exploration'
)

# Phase 2: Convergent Review (Full Coordination)
# Phase 3: Synthesis (Collaborative Integration)
```

**Agent Workflow**:

1. **Divergent Phase**: Work independently on assigned branch
2. **Signal Completion**: Use `auto_commit_memory()` to record "PHASE1_COMPLETE" status
3. **Review Phase**: Use dev tools to access other agents' progress from memory branches
4. **Synthesis Phase**: Collaborate using snapshots and memory-based coordination

### 2. Pipeline Strategy

**Use Case**: Sequential tasks with dependencies
**Team Size**: 3–6 agents
**Coordination Level**: High

**Implementation Protocol**:

```python
# Sequential handoffs with snapshots
# Agent 1 → Snapshot → Agent 2 → Snapshot → Agent 3

# Each agent MUST generate handoff:
generate_mandatory_session_end_prompt(
    work_completed=['Completed pipeline stage X'],
    current_status='Ready for next pipeline stage',
    next_agent_instructions=['Specific instructions for next stage'],
    critical_context='Dependencies and requirements for continuation'
)
```

### 3. Swarm Strategy

**Use Case**: Many independent parallel tasks
**Team Size**: 4–8 agents
**Coordination Level**: Low

**Implementation Protocol**:

```python
# Task queue management
# Agents pick tasks dynamically from shared queue
# Minimal coordination except for task claiming

# Task completion reporting:
generate_handoff_prompt_only(
    task_description='Swarm Task Completion',
    work_completed=['Completed task: [Task Name]'],
    next_steps=['Task available for next agent pickup'],
    brief_context='Swarm coordination - task completed'
)
```

### 4. Red Team Strategy

**Use Case**: Adversarial testing and security validation
**Team Size**: 2–4 agents (Blue Team + Red Team)
**Coordination Level**: High

**Implementation Protocol**:

```python
# Blue Team builds, Red Team attacks
# Iterative cycles with coordination between teams

# Blue Team completion:
generate_mandatory_session_end_prompt(
    work_completed=['Built secure implementation'],
    current_status='Ready for Red Team testing',
    next_agent_instructions=['Red Team: Attack this implementation'],
    critical_context='Security assumptions and design decisions'
)

# Red Team findings:
generate_mandatory_session_end_prompt(
    work_completed=['Found vulnerabilities: [List]'],
    current_status='Vulnerabilities documented',
    next_agent_instructions=['Blue Team: Fix identified issues'],
    critical_context='Attack vectors and exploitation methods'
)
```

### 5. Mob Programming Strategy

**Use Case**: Complex problems requiring collective intelligence
**Team Size**: 3–5 agents
**Coordination Level**: Very High

**Implementation Protocol**:

```python
# Rotating roles: Driver, Navigator, Observers
# Continuous coordination and knowledge sharing

# Role rotation handoff:
generate_handoff_prompt_only(
    task_description='Mob Programming Role Rotation',
    work_completed=['Completed driver session'],
    next_steps=['Next agent takes driver role'],
    brief_context='Mob programming continuous collaboration'
)
```

## 🛠️ Session Management Protocols

### Session Initialization

**Every agent session MUST start with**:

1. `git pull origin [branch-name]` - Get latest changes
2. Use dev tools to check for previous session memories and coordination status
3. Install dependencies: `python3 -m pip install -r src/agor/tools/agent-requirements.txt`
4. Initialize dev tools and test functionality

### Session Termination

**Every agent session MUST end with**:

1. Commit all changes with descriptive messages using `quick_commit_push()`
2. Generate session end prompt using `generate_mandatory_session_end_prompt()`
3. Create memory entry using `auto_commit_memory()` with session summary
4. Clean up any temporary files created during the session

### Handoff Generation

**Use our dev tools functions**:

- `generate_handoff_prompt_only()` - Quick handoffs
- `generate_mandatory_session_end_prompt()` - Full session end
- `generate_complete_project_outputs()` - Comprehensive outputs

### Temporary Files and Cleanup

**If you must create temporary files for dev tools execution**:

1. **Chain commands** to minimize tool calls:

```bash
# Good: One-shot execution with cleanup
python temp_script.py && rm temp_script.py

# Better: Use dev tools functions directly without temp files
python3 -c "
import sys; sys.path.insert(0, 'src')
from agor.tools.dev_tools import quick_commit_push
quick_commit_push('Your message', '🔧')
"
```

2. **Immediate cleanup**: Always remove temporary files in the same command chain
3. **Minimize file creation**: Prefer direct dev tools function calls over temporary scripts
4. **Document cleanup**: If other agents need to create temp files, remind them to clean up immediately

**Best Practice**: Use dev tools functions directly rather than creating temporary files whenever possible.

## 🎯 Role-Specific Protocols

### Worker Agent Protocols

**Responsibilities**:

- Execute assigned tasks
- Follow strategy protocols
- Generate progress reports
- Create handoff prompts

**Required Actions**:

- Select "Worker Agent" role during initialization
- Use session-end hotkey before ending sessions
- Test new features (meta mode, 2-role system)
- Focus on substantial progress, not celebration

### Project Coordinator Protocols

**Core Philosophy**: The Project Coordinator is a **strategic overseer and delegator**, not a direct executor. Focus on high-level planning, task delegation, progress tracking, quality assurance, and code review.

**Primary Responsibilities**:

- **Strategic Oversight**: High-level planning, architecture decisions, and project direction
- **Task Delegation**: Breaking down work and assigning to appropriate Worker Agents
- **Progress Tracking**: Monitoring agent progress and coordination across the team
- **Quality Assurance**: Reviewing outputs, ensuring standards, and maintaining project quality
- **Code Review**: Reviewing changes made by agents, providing feedback and approval
- **Course Correction**: Providing guidance when agents get off track or need redirection

**Delegation Model**:

- **Assign Tasks**: Delegate specific work to Worker Agents with clear instructions
- **Review Results**: Examine completed work for quality and integration
- **Provide Feedback**: Guide agents on improvements and next steps
- **Synthesize Information**: Combine agent outputs for strategic decision-making
- **Avoid Direct Execution**: Focus on coordination rather than hands-on coding

**Required Actions**:

- Select "Project Coordinator" role during initialization
- Initialize strategies using appropriate functions
- Create work orders and snapshots for Worker Agents
- Monitor agent progress through coordination files
- Review and approve agent deliverables
- Provide strategic guidance and course correction
- Conduct code reviews of agent changes

## 🔧 Technical Implementation

### Dev Tools Integration

**All coordination MUST use our dev tools**:

```python
# Import dev tools
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import (
    generate_handoff_prompt_only,
    generate_mandatory_session_end_prompt,
    generate_meta_feedback,
    generate_complete_project_outputs
)

# Use functions for all coordination
# Never create manual prompts or codeblocks
```

### Backtick Processing

**Critical**: All generated prompts automatically process backticks:

- Triple backticks (``) → Double backticks (`)
- Ensures single codeblock format for agent handoffs
- Prevents broken coordination due to formatting issues

### Memory Branch Management

**Coordination files saved to memory branches**:

- Snapshots automatically saved to adjacent memory branches
- Working branch remains clean
- Memory sync handles cross-branch coordination

## ⚠️ Critical Success Factors

### What Works

✅ **Direct Instructions**: Work orders TO agents, not ABOUT agents
✅ **Mandatory Session End**: Automatic coordination prompt generation
✅ **Dev Tools Usage**: Consistent backtick processing
✅ **Substantial Progress**: Focus on real work, not just coordination
✅ **Role Clarity**: 2-role system eliminates confusion

### What Fails

❌ **Manual Coordination**: Creating prompts without dev tools
❌ **Missing Handoffs**: Ending sessions without return prompts
❌ **Confusing Instructions**: Meta-instructions about telling other agents
❌ **Premature Celebration**: Declaring completion without substantial work
❌ **Role Confusion**: Unclear role selection and responsibilities

## 🚀 Quick Reference

### Essential Hotkeys

- `meta` - Generate AGOR feedback
- `session-end` - Mandatory session end prompt
- `handoff` - Generate handoff prompt
- `outputs` - Complete project outputs

### Essential Functions

- `generate_mandatory_session_end_prompt()` - Required before ending
- `generate_handoff_prompt_only()` - Quick coordination
- `generate_meta_feedback()` - AGOR improvement feedback

### Essential Files

- `src/agor/tools/README_ai.md` - Role selection and initialization
- `src/agor/tools/AGOR_INSTRUCTIONS.md` - Operational guide with hotkeys
- `docs/strategies.md` - Strategy decision matrix and examples
- `src/agor/tools/dev_tools.py` - Memory and coordination functions
- Memory branches (accessed via dev tools) - Session memories and coordination data

---

**Remember**: Successful multi-agent coordination requires consistent use of protocols, mandatory session end prompts, and focus on substantial progress over coordination overhead.
