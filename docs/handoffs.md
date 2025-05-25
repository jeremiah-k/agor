# 🤝 Agent Handoff System

One of AGOR's most powerful features is seamless agent transitions. Whether you're switching roles, passing work to a specialist, or need to step away mid-task, AGOR's handoff system ensures no context is lost.

## 🎯 Why Handoffs Matter

In traditional development, context switching is expensive. When one developer hands off work to another, critical information gets lost:

- **Why** certain decisions were made
- **What** approaches were tried and failed
- **Where** the current implementation stands
- **How** to continue the work effectively

AGOR's handoff system solves this by capturing **complete context** in a structured, actionable format.

## 🔄 Handoff Scenarios

### 1. Role Switching

```
PROJECT COORDINATOR → ANALYST/SOLO DEV
"I've planned the architecture, now I need someone to implement it"
```

### 2. Specialization Handoff

```
ANALYST/SOLO DEV → AGENT WORKER (Security Specialist)
"I've built the feature, now I need security review and hardening"
```

### 3. Time-Based Transitions

```
AGENT WORKER → AGENT WORKER (Different Shift)
"I'm ending my work session, here's where I left off"
```

### 4. Escalation Handoffs

```
AGENT WORKER → PROJECT COORDINATOR
"I've hit a blocker that needs architectural decision"
```

## 🛠️ How It Works

### Creating a Handoff

**Step 1: Use the `handoff` hotkey**

```
handoff
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

- Creates handoff document in `.agor/handoffs/`
- Updates coordination logs
- Generates handoff prompt for receiving agent

### Receiving a Handoff

**Step 1: Use the `receive` hotkey**

```
receive
```

**Step 2: Review handoff document**

- Read problem definition and context
- Understand work completed so far
- Review commits and file changes
- Verify current repository state

**Step 3: Confirm understanding and continue**

- Update `.agor/agentconvo.md` with receipt confirmation
- Begin work on next steps
- Maintain documentation standards

## 📋 Handoff Document Structure

Every handoff document includes:

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

### 🎯 Handoff Instructions

How to continue the work:

- Environment setup requirements
- Testing procedures
- Debugging tips
- Key files to review first

## 💡 Best Practices

### For Handoff Creators

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

### For Handoff Recipients

**Verify Everything**

- Check that repository state matches handoff
- Verify you're on the correct git branch and commit
- Confirm AGOR version compatibility
- Confirm all described changes are present
- Test that current implementation works as described

**Ask Questions**

- If anything is unclear, ask for clarification
- Don't assume you understand complex decisions
- Verify your interpretation before proceeding

**Maintain Standards**

- Update handoff document with your progress
- Follow the same documentation quality
- Create your own handoff when passing work forward

## 🔍 AGOR Version Compatibility

Each handoff document includes the AGOR version used to create it. This is critical for maintaining protocol compatibility:

### Why Version Matters

- **Protocol Evolution**: AGOR coordination protocols evolve over time
- **Hotkey Changes**: New hotkeys and commands are added in different versions
- **Template Updates**: Handoff templates and procedures may change
- **Feature Compatibility**: New features may not be available in older versions

### Version Verification

When receiving a handoff:

```bash
# Check your current AGOR version
agor --version

# If versions don't match, consider checking out the handoff version
git checkout v0.1.5  # Example: checkout the version used in handoff

# Or update to latest if handoff is from newer version
pipx upgrade agor
```

### Version Compatibility Guidelines

**Same Major.Minor Version**: ✅ Fully compatible

- Example: 0.1.4 ↔️ 0.1.5
- All protocols and hotkeys should work identically

**Different Minor Version**: ⚠️ Mostly compatible

- Example: 0.1.x ↔️ 0.2.x
- Core protocols compatible, some new features may be missing

**Different Major Version**: ❌ May have breaking changes

- Example: 0.x.x ↔️ 1.x.x
- Significant protocol changes possible, review carefully

### Handling Version Mismatches

**If you have older AGOR version:**

```bash
# Option 1: Upgrade to match or exceed handoff version
pipx upgrade agor

# Option 2: Use git to checkout handoff version
git checkout v0.1.5  # Use version from handoff
```

**If you have newer AGOR version:**

- Usually safe to proceed with newer version
- New features will be available
- Core protocols should remain compatible

**If major version difference:**

- Review handoff document carefully
- Check for protocol changes in release notes
- Consider using exact version match for critical handoffs

## 🔧 Advanced Handoff Patterns

### Multi-Agent Handoffs

When work needs to go to multiple agents:

```
COORDINATOR creates handoff for parallel work:
├── Agent A: Frontend implementation
├── Agent B: Backend API
└── Agent C: Database schema
```

### Iterative Handoffs

For complex features requiring multiple passes:

```
Round 1: ANALYST → Basic implementation
Round 2: SECURITY AGENT → Security hardening
Round 3: PERFORMANCE AGENT → Optimization
Round 4: INTEGRATION AGENT → System integration
```

### Emergency Handoffs

When urgent issues arise:

```
CURRENT AGENT creates emergency handoff:
- Immediate problem description
- Current debugging state
- Attempted solutions
- Escalation path
```

## 📊 Handoff Quality Metrics

### Good Handoffs Include:

- ✅ Clear problem definition
- ✅ Complete work inventory
- ✅ Specific git commits
- ✅ Detailed next steps
- ✅ Technical context and decisions
- ✅ Testing and verification steps

### Poor Handoffs Lack:

- ❌ Vague problem description
- ❌ Incomplete work summary
- ❌ Missing commit information
- ❌ Unclear next steps
- ❌ No technical context
- ❌ No verification procedures

## 🎯 Integration with AGOR Strategies

Handoffs work seamlessly with all AGOR strategies:

**Parallel Divergent**: Handoffs between exploration and synthesis phases
**Pipeline**: Structured handoffs between pipeline stages
**Swarm**: Dynamic handoffs as agents complete tasks
**Red Team**: Handoffs between build and break phases
**Mob Programming**: Handoffs during role rotations

## 🔄 Handoff Lifecycle

1. **Creation**: Agent creates comprehensive handoff document
2. **Notification**: Receiving agent is notified via coordination channels
3. **Review**: Receiving agent reviews and verifies handoff
4. **Confirmation**: Receipt is confirmed in coordination logs
5. **Continuation**: Work continues seamlessly from handoff point
6. **Completion**: Handoff is marked complete when work finishes

---

**Ready to create your first handoff?** Use the `handoff` hotkey and experience seamless agent transitions! 🚀
