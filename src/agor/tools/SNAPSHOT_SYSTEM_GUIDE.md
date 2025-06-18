# 📸 AGOR Snapshot System - Essential Guide for Agents

**Critical for all agents: You MUST provide a snapshot before ending your session**

## 🎯 What is the Snapshot System?

The snapshot system is AGOR's core mechanism for seamless agent transitions with minimal user intervention:

- **Context Preservation** - Complete work state maintained across agent transitions
- **Automatic Handoffs** - Generated prompts eliminate manual context re-entry
- **Session Continuity** - Agents resume exactly where previous agents left off
- **Primary Use Case** - Context limit handoffs when agents reach capacity

(For a quick summary of these guidelines callable from your agent environment, use `get_snapshot_guidelines_summary()` from `dev_tools.py`.)

## 🚨 MANDATORY: End-of-Session Snapshot

**EVERY agent session MUST end with a snapshot in a single codeblock.**

### When to Create Snapshots:

- **End of work session** (REQUIRED - ensures continuity)
- **Context limit reached** (PRIMARY USE CASE - seamless handoff)
- **Task completion** (for documentation and review)
- **Session progress checkpoints** (for planning and tracking)

### Snapshot Format (Single Codeblock):

```markdown
# 📸 Agent Snapshot Document

**Generated**: 2024-01-27 14:30:00
**From Agent Role**: [Your Role]
**Snapshot Reason**: [End of session/Handoff/Blocker/etc.]
**AGOR Version**: 0.4.4

## 🔧 Environment Context

**Git Branch**: `feature/authentication`
**Current Commit**: `abc12345...`
**Repository Status**: Clean/Has uncommitted changes

## 🎯 Problem Definition

[Clear description of what you were working on]

## 📊 Current Status

**Overall Progress**: [Percentage or description]
**Estimated Completion**: [Time estimate or "Unknown"]

## ✅ Work Completed

- [List of completed tasks]
- [Features implemented]
- [Bugs fixed]

## 📝 Commits Made

- `commit-hash: commit message`
- `commit-hash: commit message`

## 📁 Files Modified

- `path/to/file.py` - [What was changed]
- `path/to/another.js` - [What was changed]

## 🔄 Next Steps

1. [Immediate next task]
2. [Follow-up tasks]
3. [Long-term considerations]

## 🧠 Technical Context

**Key Decisions Made**: [Important architectural or implementation decisions]
**Gotchas/Warnings**: [Things the next agent should know]
**Dependencies**: [External dependencies or blockers]
**Testing Status**: [What's tested, what needs testing]

## 🎯 Continuation Instructions

[Specific guidance for the next agent or future session]
```

## 🛠️ How to Create Snapshots

### Method 1: Use AGOR Dev Tools (Recommended)

```python
from agor.tools.dev_tools import create_development_snapshot

# Create comprehensive snapshot with full user context
snapshot_content = create_development_snapshot(
    title='Descriptive title reflecting user goals',
    context='COMPREHENSIVE user reasoning, decision-making process, and full context - like a transcriptionist record',
    next_steps=['Detailed steps with user strategic thinking', 'More steps with full rationale']
)
```

### Method 2: Use AGOR Hotkey (If available)

```
snapshot
```

This will prompt you for all necessary information and generate the snapshot automatically.

### Method 3: Manual Creation (If other methods unavailable)

1. **Gather comprehensive context** - Review ALL user input, reasoning, and decision-making process
2. **Capture user voice** - Include their detailed explanations, priorities, and strategic thinking
3. **Fill out template** - Use the format above with complete context
4. **Save to .agor/agents/{agent_id}/snapshots/** - Use timestamp naming: `YYYY-MM-DD_HHMMSS_summary_snapshot.md`
5. **Update coordination logs** - Add entry to `.agor/agentconvo.md`

## 📝 Comprehensive Context Capture Guide

### What "Transcriptionist-Level" Context Means:

**Capture the full essence of user reasoning:**
- Every detailed explanation they provide
- Their decision-making process and rationale
- Strategic thinking and long-term vision
- Priorities, emphasis, and direction
- Technical preferences and requirements
- Philosophy behind architectural choices

**Example of GOOD context capture:**
```
User emphasized that multi-agent coordination strategies are largely untested and need more work,
preferring to focus on the snapshot/memory branch system and dev tools as the more developed features.
They want users to understand these mature features and how to use them effectively. The user specifically
noted that agents should never manually interact with snapshots - all memory management must be done
using dev tools. They also emphasized the importance of quick_commit_and_push() functionality for
efficiency and branch synchronization when multiple users/agents are working on projects.
```

**Example of POOR context capture:**
```
Updated user guidelines and fixed some issues.
```

## 📋 Snapshot Quality Checklist

### 🚨 CRITICAL: Comprehensive Context Capture

**Snapshots must be like transcriptionist records - capturing the full essence of user reasoning and decision-making, ideally word-for-word, but at minimum the complete context.**

### Essential Information (MUST HAVE):

- [ ] Clear problem definition with full user reasoning
- [ ] Current status and progress with detailed context
- [ ] All work completed this session with explanations
- [ ] All commits made with full explanations and rationale
- [ ] All files modified with detailed reasons and user context
- [ ] Specific next steps with user's strategic thinking
- [ ] Git repository state with complete technical context

### User Context & Reasoning (CRITICAL):

- [ ] **Full user reasoning** - All detailed explanations and decision-making process
- [ ] **Context behind decisions** - Why certain choices were made, not just what was done
- [ ] **Technical rationale** - The reasoning behind technical decisions and architectural choices
- [ ] **User philosophy** - The user's thinking about priorities, emphasis, and direction
- [ ] **Strategic context** - Long-term vision and how current work fits into larger goals
- [ ] **Comprehensive record** - Like a transcriptionist capturing the essence, ideally word-for-word

### Technical Context (SHOULD HAVE):

- [ ] Key decisions and complete rationale with user input
- [ ] Warnings or gotchas with full context
- [ ] Testing status with user preferences
- [ ] Performance considerations with user priorities
- [ ] Security implications with user requirements

### Continuation Guidance (MUST HAVE):

- [ ] How to continue the work with user's strategic vision
- [ ] What to review first based on user priorities
- [ ] Environment setup needs with user preferences
- [ ] Testing procedures aligned with user requirements

## 🔄 Loading Snapshots

### When Starting Work:

1. **Check for snapshots** - Look in `.agor/agents/{agent_id}/snapshots/` directory
2. **Load latest relevant snapshot** - Use `load_snapshot` hotkey or read manually
3. **Verify repository state** - Ensure git branch and commit match snapshot
4. **Confirm understanding** - Update `.agor/agentconvo.md` with receipt confirmation

### Snapshot Loading Hotkey:

```
load_snapshot
```

## 📁 Snapshot Storage

**Important:** The `.agor/agents/{agent_id}/snapshots/` directory and its contents are stored on dedicated memory branches (e.g., `agor/mem/BRANCH_NAME`), not typically on your main working branch. This is managed by AGOR's dev tools and Memory Synchronization System.

Snapshots are stored in:

```
.agor/
├── agents/
│   ├── agent_abc123_1234567890/
│   │   ├── snapshots/
│   │   │   ├── 2024-01-27_143000_auth-system_snapshot.md
│   │   │   └── 2024-01-27_160000_frontend-integration_snapshot.md
│   │   ├── work_log.md
│   │   └── agent_info.md
├── agentconvo.md
└── memory.md
```

## 🎯 Best Practices

### For Snapshot Creators:

- **Be comprehensive like a transcriptionist** - Capture the full essence of user reasoning, ideally word-for-word
- **Include ALL user context** - Every detailed explanation, decision rationale, and strategic thinking
- **Capture user philosophy** - Their priorities, emphasis, direction, and long-term vision
- **Document the "why" not just the "what"** - Full reasoning behind every decision and choice
- **Be specific** - Exact file paths, commit hashes, error messages, and complete technical context
- **Be forward-thinking** - What would you want to know if you were continuing this work?
- **Test your instructions** - Could someone else follow your next steps with full context?
- **Preserve user voice** - Maintain the user's reasoning patterns and decision-making process

### For Snapshot Receivers:

- **Read completely** - Don't skip sections
- **Verify state** - Ensure your environment matches the snapshot
- **Ask questions** - Use coordination channels if anything is unclear
- **Confirm receipt** - Update coordination logs

## 🚨 Critical Reminders

1. **NEVER end a session without a snapshot** - Use `create_development_snapshot()` function
2. **Capture comprehensive user context** - Like a transcriptionist, include ALL user reasoning and decision-making
3. **Include the snapshot in a single codeblock** - For easy copying/processing
4. **Be thorough with user voice** - Missing user context causes delays and confusion
5. **Document user philosophy** - Their priorities, strategic thinking, and long-term vision
6. **Update regularly** - Don't wait until the end to document your work
7. **Test continuity** - Ensure someone else could pick up where you left off with full context
8. **Never manually create .agor files** - All memory management through dev tools only

## 📚 Related Documentation

- **Full snapshot guide**: `docs/snapshots.md`
- **Snapshot templates**: `src/agor/tools/snapshot_templates.py`
- **Work orders guide**: `docs/work-orders-and-memory-guide.md`
- **Agent coordination**: `src/agor/tools/agent_coordination.py`

---

**Remember**: The snapshot system is what makes AGOR's multi-agent coordination possible. Your snapshot is the bridge between your work and the next agent's success.
