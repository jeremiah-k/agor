# 📸 AGOR Snapshot System - Essential Guide for Agents

**Critical for all agents: You MUST provide a snapshot before ending your session**

## 🎯 What is the Snapshot System?

The snapshot system is AGOR's core mechanism for seamless agent transitions with minimal user intervention:

- **Context Preservation** - Complete work state maintained across agent transitions
- **Automatic Handoffs** - Generated prompts eliminate manual context re-entry
- **Session Continuity** - Agents resume exactly where previous agents left off
- **Primary Use Case** - Context limit handoffs when agents reach capacity

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

### Method 1: Use AGOR Hotkey (Recommended)

```
snapshot
```

This will prompt you for all necessary information and generate the snapshot automatically.

### Method 2: Manual Creation (If hotkey unavailable)

1. **Gather context** - Review your work, commits, and current state
2. **Fill out template** - Use the format above
3. **Save to .agor/agents/{agent_id}/snapshots/** - Use timestamp naming: `YYYY-MM-DD_HHMMSS_summary_snapshot.md`
4. **Update coordination logs** - Add entry to `.agor/agentconvo.md`

## 📋 Snapshot Quality Checklist

### Essential Information (MUST HAVE):

- [ ] Clear problem definition
- [ ] Current status and progress
- [ ] All work completed this session
- [ ] All commits made with explanations
- [ ] All files modified with reasons
- [ ] Specific next steps
- [ ] Git repository state

### Technical Context (SHOULD HAVE):

- [ ] Key decisions and rationale
- [ ] Warnings or gotchas
- [ ] Testing status
- [ ] Performance considerations
- [ ] Security implications

### Continuation Guidance (MUST HAVE):

- [ ] How to continue the work
- [ ] What to review first
- [ ] Environment setup needs
- [ ] Testing procedures

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

- **Be comprehensive** - Include all relevant context
- **Be specific** - Exact file paths, commit hashes, error messages
- **Be forward-thinking** - What would you want to know if you were continuing this work?
- **Test your instructions** - Could someone else follow your next steps?

### For Snapshot Receivers:

- **Read completely** - Don't skip sections
- **Verify state** - Ensure your environment matches the snapshot
- **Ask questions** - Use coordination channels if anything is unclear
- **Confirm receipt** - Update coordination logs

## 🚨 Critical Reminders

1. **NEVER end a session without a snapshot** - This is mandatory
2. **Include the snapshot in a single codeblock** - For easy copying/processing
3. **Be thorough** - Missing context causes delays and confusion
4. **Update regularly** - Don't wait until the end to document your work
5. **Test continuity** - Ensure someone else could pick up where you left off

## 📚 Related Documentation

- **Full snapshot guide**: `docs/snapshots.md`
- **Snapshot templates**: `src/agor/tools/snapshot_templates.py`
- **Work orders guide**: `docs/work-orders-and-memory-guide.md`
- **Agent coordination**: `src/agor/tools/agent_coordination.py`

---

**Remember**: The snapshot system is what makes AGOR's multi-agent coordination possible. Your snapshot is the bridge between your work and the next agent's success.
