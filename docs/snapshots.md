# 📸 Agent Snapshot System

One of AGOR's most powerful features is seamless agent transitions. Whether you're switching roles, passing work to a specialist, or need to step away mid-task, AGOR's snapshot system ensures no context is lost.

## 💡 Snapshots for Everyone (Including Solo Developers!)

While the concept of a "snapshot" naturally brings to mind passing work between different agents or team members, AGOR's snapshot system is a powerful tool even for **solo developers**. Think of it as creating a comprehensive "snapshot" of your current work:

- **Context Preservation Across Sessions**: If you're stepping away from a task and want to ensure you can pick it up seamlessly later (perhaps hours, days, or even weeks later), creating a snapshot to your "future self" captures all relevant code changes, analysis, decisions, and next steps.
- **Managing AI Context Limits**: Large language models have context windows. If a task is complex and requires more back-and-forth than a single session can hold, creating a snapshot allows you to effectively "reset" the context for the AI while providing it with a structured, detailed summary of everything it needs to continue. You can then start a new conversation with the AI, provide the snapshot document, and carry on.
- **Switching Tools or Models**: If you start a task with one AI model and wish to continue with another, a snapshot document provides a standardized way to transfer the complete state of your work.
- **Structured Self-Correction**: If you've gone down a path and need to backtrack or rethink, creating a snapshot of your current state can be a useful way to document what you've done before exploring a new direction.

So, as you read about the snapshot system, remember that while many examples involve multiple agents, the underlying mechanisms and benefits offer significant advantages for managing and preserving context in solo development workflows as well.

## 🎯 Why Snapshots Matter

In traditional development, context switching is expensive. When one developer hands off work to another, critical information gets lost:

- **Why** certain decisions were made
- **What** approaches were tried and failed
- **Where** the current implementation stands
- **How** to continue the work effectively

AGOR's snapshot system solves this by capturing **complete context** in a structured, actionable format.

## 🔄 Core Snapshot Types

AGOR's snapshot system focuses on three essential scenarios that align with the platform's core purpose: seamless agent transitions with minimal user intervention.

### 1. Transition Snapshot (Primary Use Case)

```
AGENT → NEW AGENT (Context Limit Reached)
"I'm approaching my context limit, here's everything needed to continue seamlessly"
```

**When to use**: When an agent reaches context limits and needs to hand off work to continue without losing progress.

### 2. Progress Report Snapshot

```
AGENT → SAME AGENT (Session Progress)
"Here's what I've accomplished and what's planned next"
```

**When to use**: For documenting session progress, planning next steps, or creating checkpoints during long tasks.

### 3. Completion Report Snapshot

```
AGENT → USER/PROJECT COORDINATOR (Task Complete)
"Task completed successfully, here's the summary and deliverables"
```

**When to use**: When a task or project phase is complete and needs to be documented for review or next phase planning.

## 🛠️ How It Works

### Creating a Snapshot

**Step 1: Use the `snapshot` hotkey**

```
snapshot
```

**Step 2: AGOR prompts for context**

- What problem are you solving?
- What work have you completed?
- What commits have you made?
- Which files have you modified?
- What's the current status?
- What are the next steps?
- Any important context or gotchas?

**Step 3: AGOR generates comprehensive documentation**

- Creates snapshot document in `.agor/snapshots/`
- Updates coordination logs
- Generates snapshot prompt for receiving agent

### Receiving a Snapshot

**Step 1: Use the `load_snapshot` hotkey**

```
load_snapshot
```

**Step 2: Review snapshot document**

- Read problem definition and context
- Understand work completed so far
- Review commits and file changes
- Verify current repository state

**Step 3: Confirm understanding and continue**

- Update `.agor/agentconvo.md` with receipt confirmation
- Begin work on next steps
- Maintain documentation standards

## 📋 Snapshot Document Structure

Every snapshot document includes:

### 🎯 Problem Definition

Clear description of what we're trying to solve, including:

- Original requirements or bug report
- Success criteria
- Constraints and considerations

### ✅ Work Completed

Detailed list of accomplishments:

- Features implemented
- Bugs fixed
- Research conducted
- Decisions made

### 📝 Commits Made

Git history with explanations:

- Commit hashes and messages
- What each commit accomplishes
- Why certain approaches were taken

### 📁 Files Modified

Complete file change inventory:

- Which files were changed and why
- New files created
- Files deleted or moved
- Configuration changes

### 📊 Current Status

Where things stand right now:

- What's working
- What's partially complete
- What's broken or needs attention
- Test status and coverage

### 🔄 Next Steps

Prioritized action items:

- Immediate next tasks
- Medium-term goals
- Long-term considerations
- Dependencies and blockers

### 🧠 Technical Context

Important implementation details:

- **Git branch and commit information** - Exact repository state
- **AGOR version used** - For protocol compatibility
- **Uncommitted and staged changes** - Work in progress
- **Architecture decisions and rationale**
- **Performance considerations**
- **Security implications**
- **Integration points**
- **Workarounds and technical debt**

### 🎯 Snapshot Instructions

How to continue the work:

- Environment setup requirements
- Testing procedures
- Debugging tips
- Key files to review first

## 💡 Best Practices

### For Snapshot Creators

**Be Comprehensive**

- Include everything the next agent needs to know
- Don't assume they have your context
- Document your reasoning, not just your actions

**Be Specific**

- Include exact commit hashes
- Provide specific file paths and line numbers
- Give concrete next steps, not vague suggestions

**Be Honest**

- Document what didn't work
- Explain workarounds and technical debt
- Highlight areas of uncertainty

### For Snapshot Recipients

**Verify Everything**

- Check that repository state matches snapshot
- Verify you're on the correct git branch and commit
- Confirm AGOR version compatibility
- Confirm all described changes are present
- Test that current implementation works as described

**Ask Questions**

- If anything is unclear, ask for clarification
- Don't assume you understand complex decisions
- Verify your interpretation before proceeding

**Maintain Standards**

- Update snapshot document with your progress
- Follow the same documentation quality
- Create your own snapshot when passing work forward

## 🔍 AGOR Version Compatibility

Each snapshot document includes the AGOR version used to create it. This is critical for maintaining protocol compatibility:

### Why Version Matters

- **Protocol Evolution**: AGOR coordination protocols evolve over time
- **Hotkey Changes**: New hotkeys and commands are added in different versions
- **Template Updates**: Snapshot templates and procedures may change
- **Feature Compatibility**: New features may not be available in older versions

### Version Verification

When receiving a snapshot:

```bash
# Check your current AGOR version
agor --version

# If versions don't match, consider checking out the snapshot version
git checkout v0.2.0  # Example: checkout the version used in snapshot

# Or update to latest if snapshot is from newer version
pipx upgrade agor
```

### Version Compatibility Guidelines

**Same Major.Minor Version**: ✅ Fully compatible

- Example: 0.2.0 ↔️ 0.2.1
- All protocols and hotkeys should work identically

**Different Minor Version**: ⚠️ Mostly compatible

- Example: 0.2.x ↔️ 0.3.x
- Core protocols compatible, some new features may be missing

**Different Major Version**: ❌ May have breaking changes

- Example: 0.x.x ↔️ 1.x.x
- Significant protocol changes possible, review carefully

### Handling Version Mismatches

**If you have older AGOR version:**

```bash
# Option 1: Upgrade to match or exceed snapshot version
pipx upgrade agor

# Option 2: Use git to checkout snapshot version
git checkout v0.2.0  # Use version from snapshot
```

**If you have newer AGOR version:**

- Usually safe to proceed with newer version
- New features will be available
- Core protocols should remain compatible

**If major version difference:**

- Review snapshot document carefully
- Check for protocol changes in release notes
- Consider using exact version match for critical snapshots

## 🎯 Snapshot Best Practices

### Focus on Continuity

The primary goal of AGOR snapshots is **seamless continuity**. Every snapshot should enable the next agent (or the same agent in a future session) to continue work without missing context or requiring manual re-explanation.

### Automatic Prompt Generation

AGOR snapshots automatically generate the prompts needed for agent transitions, eliminating the need for users to manually craft context-heavy instructions for each handoff.

### Minimal User Intervention

The snapshot system is designed to work with minimal user involvement - agents create comprehensive snapshots that include all necessary context for continuation.

## 📊 Snapshot Quality Metrics

### Good Snapshots Include:

- ✅ Clear problem definition
- ✅ Complete work inventory
- ✅ Specific git commits
- ✅ Detailed next steps
- ✅ Technical context and decisions
- ✅ Testing and verification steps

### Poor Snapshots Lack:

- ❌ Vague problem description
- ❌ Incomplete work summary
- ❌ Missing commit information
- ❌ Unclear next steps
- ❌ No technical context
- ❌ No verification procedures

## 🎯 Core AGOR Integration

Snapshots are the foundation of AGOR's seamless agent coordination:

**Context Preservation**: Maintains complete work state across agent transitions
**Automatic Handoffs**: Generates prompts automatically for continuing agents
**Session Continuity**: Enables agents to resume work exactly where previous agents left off
**Minimal User Input**: Reduces need for manual context re-entry between agent sessions

## 🔄 Snapshot Lifecycle

1. **Creation**: Agent creates comprehensive snapshot document
2. **Notification**: Receiving agent is notified via coordination channels
3. **Review**: Receiving agent reviews and verifies snapshot
4. **Confirmation**: Receipt is confirmed in coordination logs
5. **Continuation**: Work continues seamlessly from snapshot point
6. **Completion**: Snapshot is marked complete when work finishes

---

**Ready to create your first snapshot?** Use the `snapshot` hotkey and experience seamless agent transitions! 🚀
