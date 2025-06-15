# 🎯 AGOR Agent Workflow Optimization Guide

## For Users: How to Maintain Seamless Agent Coordination

This guide provides practical strategies for optimizing your AGOR workflow based on real-world usage patterns and lessons learned from developing AGOR itself.

## 🔄 The Seamless Feedback Loop

### The Goal: Minimal User Intervention

AGOR's primary value is enabling seamless agent-to-agent transitions where:

- Agents automatically create comprehensive handoff prompts
- Users only need to edit prompts to steer project direction
- Context is preserved across agent transitions
- Work continues without manual re-entry of requirements

### Common Workflow Breakdown Points

**❌ What Often Goes Wrong:**

- Agent completes work but doesn't create handoff prompt
- Agent creates snapshot but forgets to generate return prompt
- User has to manually remind agent multiple times
- Context gets lost between agent transitions

**✅ How to Prevent This:**

- Use specific prompting strategies (detailed below)
- Include explicit handoff requirements in every prompt
- Use memory branch references for context continuity
- Apply consistent formatting requirements

## 🎯 Proven Prompting Strategies

### 1. The "Bookend" Approach

**Start every agent session with:**

```
Before starting work, read the AGOR documentation and create a plan.
When finished, you MUST create both a snapshot and a handoff prompt
for the next agent, properly formatted in a single codeblock.
```

**End every prompt with:**

```
Remember: End your session by creating a snapshot and generating
a handoff prompt for the next agent. Process through dev tools
and wrap in a single codeblock for copy-paste.
```

### 2. The "Explicit Requirement" Method

Include this in your prompts:

```
CRITICAL: Your response must end with:
1. A development snapshot using create_development_snapshot()
2. A handoff prompt using generate_session_end_prompt()
3. Both processed through detick_content() and wrapped in codeblocks
```

### 3. The "Context Inheritance" Pattern

When handing off between agents:

```
The previous agent created snapshot [branch/file]. Read this first,
understand what was accomplished, then continue the work. When you
finish, create your own snapshot and handoff prompt referencing
your memory branch for the next agent.
```

## 📚 Real-World Examples from AGOR Development

### Example 1: CodeRabbit Review Fixes

**Initial Prompt:**

```
Fix all CodeRabbit review issues in PR #93. Read the review comments,
address each issue systematically, and test your changes. When complete,
create a snapshot documenting what was fixed and generate a handoff
prompt for the next development phase.
```

**What Happened:** Agent fixed all issues but didn't create handoff prompt.

**Optimized Prompt:**

```
Fix all CodeRabbit review issues in PR #93. Read the review comments,
address each issue systematically, and test your changes.

MANDATORY SESSION END: Create both:
1. Development snapshot with details of fixes
2. Handoff prompt for next agent (deticked, in codeblock)

Your response must end with the handoff prompt ready for copy-paste.
```

### Example 2: Role Consistency Cleanup

**Initial Approach:** "Update role names across documentation"

**What Happened:** Agent updated some files but missed others, no handoff created.

**Optimized Approach:**

```
Systematically update role names from 3-role to 2-role system across
ALL documentation. Create a checklist, work through it methodically.

REQUIRED DELIVERABLES:
- Progress snapshot after each major section
- Final handoff prompt with complete file list
- Next agent instructions for verification

End with handoff prompt in single codeblock.
```

### Example 3: Modular Architecture Refactoring

**Successful Pattern Used:**

```
Refactor dev_tools.py by moving functions to specialized modules.
Follow the <500 LOC guideline. Document your process as you work.

COORDINATION REQUIREMENTS:
- Create snapshot before major changes
- Update imports and test functionality
- Generate handoff prompt explaining the new architecture
- Include memory branch reference for next agent

Must end with deticked handoff prompt in codeblock.
```

## 🧠 Memory Branch Strategy

### Current Best Practice: One Branch Per Agent

**Generate Unique Agent ID:**

```python
import hashlib
import time
agent_id = hashlib.md5(f"agent_{time.time()}".encode()).hexdigest()[:8]
memory_branch = f"agor/mem/agent_{agent_id}"
```

**Benefits:**

- Each agent has dedicated memory space
- No conflicts between concurrent agents
- Easy to reference in handoff prompts
- Agents can manage their own snapshots

**Usage in Handoff Prompts:**

```
Your memory branch is: agor/mem/agent_a1b2c3d4
All your snapshots should commit to this branch.
Reference this branch when creating handoff prompts.
```

## 🔧 Prompt Templates for Common Scenarios

### Development Task Handoff

```
[Task Description]

AGENT REQUIREMENTS:
1. Read previous work from memory branch: [branch_name]
2. Create development plan and execute systematically
3. Use quick_commit_and_push() frequently during work
4. Create progress snapshots for major milestones

SESSION END REQUIREMENTS:
- Development snapshot with comprehensive context
- Handoff prompt for next agent (deticked, in codeblock)
- Memory branch reference for continuation
```

### Code Review and Fixes

```
Review and fix [specific issues]. Address each item systematically.

DELIVERABLES REQUIRED:
1. Fix all identified issues
2. Test changes thoroughly
3. Document what was fixed in snapshot
4. Create handoff prompt for next development phase

CRITICAL: End with handoff prompt in single codeblock for copy-paste.
```

### Documentation Updates

```
Update documentation for [specific changes]. Ensure consistency across all files.

SYSTEMATIC APPROACH:
- Create checklist of files to update
- Work through methodically
- Verify consistency
- Create snapshot with complete change list

MANDATORY: Generate handoff prompt with file modification list.
```

## 🎼 Advanced Coordination Techniques

### 1. Chain Prompting

Link multiple agents with specific handoff instructions:

```
Agent 1: "Create foundation, hand off to Agent 2 for implementation"
Agent 2: "Implement features, hand off to Agent 3 for testing"
Agent 3: "Test and validate, hand off to Agent 4 for documentation"
```

### 2. Parallel Work Coordination

For independent tasks:

```
Agent A: Work on frontend (memory branch: agor/mem/frontend_work)
Agent B: Work on backend (memory branch: agor/mem/backend_work)
Coordinator: Merge results from both memory branches
```

### 3. Iterative Refinement

```
Agent 1: Initial implementation + handoff prompt
Agent 2: Review Agent 1's work, refine + handoff prompt
Agent 3: Final polish and testing + handoff prompt
```

## 🚨 Troubleshooting Common Issues

### "Agent Didn't Create Handoff Prompt"

**Solution:** Add explicit requirement at start and end of prompt:

```
START: "You must end this session with a handoff prompt"
END: "Create handoff prompt now, deticked, in codeblock"
```

### "Context Lost Between Agents"

**Solution:** Always reference memory branches:

```
"Read previous work from agor/mem/[branch]. Continue from there."
```

### "Agent Forgot to Use Dev Tools"

**Solution:** Include import statements in prompt:

```python
Use these functions:
from agor.tools.dev_tools import create_development_snapshot
from agor.tools.agent_handoffs import detick_content
```

## 📊 Meta Feedback Integration

### When to Generate Meta Feedback

**Successful Workflows:**

```
"This handoff process worked really well! Generate meta feedback
about what made it successful for the AGOR team."
```

**Problematic Workflows:**

```
"I had to remind the agent multiple times to create handoff prompts.
Generate meta feedback about this workflow issue."
```

**System Improvements:**

```
"The memory branch strategy could be improved. Generate meta feedback
with suggestions for better agent coordination."
```

### Meta Feedback Hotkey Usage

```python
# At end of successful session
generate_meta_feedback(
    feedback_type="workflow_success",
    feedback_content="Seamless agent handoff with proper snapshot creation",
    suggestions=["Document this pattern", "Add to user guidelines"]
)

# When encountering issues
generate_meta_feedback(
    feedback_type="coordination_issue",
    feedback_content="Agent didn't create handoff prompt despite instructions",
    suggestions=["Strengthen prompt templates", "Add explicit requirements"]
)
```

## 🎯 Success Metrics

**You know AGOR is working well when:**

- Agents automatically create handoff prompts
- Context flows seamlessly between agents
- You only need to edit prompts to steer direction
- Work continues without manual intervention
- Meta feedback helps improve the system

**Red flags that indicate optimization needed:**

- Repeatedly reminding agents to create handoffs
- Context getting lost between sessions
- Manual re-entry of requirements
- Agents not following AGOR protocols

---

**Remember:** AGOR's goal is to minimize your coordination overhead while maximizing agent productivity. These patterns help achieve that seamless experience.
