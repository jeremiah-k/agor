# AGOR Coordination Example

This example shows how the new strategy implementation protocols solve the coordination gap in AGOR.

## Problem: Before Implementation Protocols

**Agent enters project and asks**: "What should I do?"

**Old AGOR response**: "Use Parallel Divergent strategy. Multiple agents work independently then peer review."

**Agent confusion**: "But HOW do I actually start? What files do I create? How do I know when others are done?"

## Solution: With Implementation Protocols

### Step 1: Strategy Initialization

```python
from agor.tools.strategy_protocols import initialize_parallel_divergent

# Coordinator initializes strategy
result = initialize_parallel_divergent("implement e2e encryption for login", agent_count=3)
print(result)
```

**Output**:

```
✅ Parallel Divergent Strategy Initialized

Task: implement e2e encryption for login
Agents: 3
Phase: 1 - Divergent Execution

Next Steps for Agents:
1. Check your assignment in .agor/strategy-active.md
2. Create your branch and memory file
3. Begin independent work
4. Signal completion when done

Files Created:
- .agor/strategy-active.md - Strategy details and agent assignments
- .agor/agent[N]-memory.md - Individual agent memory templates

Ready for agent coordination!
```

### Step 2: Agent Discovery

```python
from agor.tools.agent_coordination import discover_my_role

# Agent1 enters project
guidance = discover_my_role("agent1")
print(guidance)
```

**Output**:

````
# 🤖 AGOR Agent Coordination

## Status: Strategy Active

Active strategy: parallel_divergent. Claim assignment as agent1 and begin independent work

## Current Strategy: Parallel Divergent
Task: implement e2e encryption for login
Your Role: Divergent Worker

## Next Actions:
1. Post to agentconvo.md: 'agent1: [timestamp] - CLAIMING ASSIGNMENT'
2. Create branch: git checkout -b solution-agent1
3. Initialize memory file: .agor/agent1-memory.md
4. Plan your unique approach to the problem
5. Begin independent implementation (NO coordination with other agents)

## Quick Commands:
```bash
# Check strategy details
cat .agor/strategy-active.md

# Check agent communication
cat .agor/agentconvo.md | tail -10

# Check your memory file
cat .agor/agent1-memory.md
````

### Step 3: Agent Execution

Agent1 follows the concrete instructions:

```bash
# 1. Claim assignment
echo "agent1: $(date '+%Y-%m-%d %H:%M:%S') - CLAIMING ASSIGNMENT" >> .agor/agentconvo.md

# 2. Create branch
git checkout -b solution-agent1

# 3. Check memory file (already created by initialization)
cat .agor/agent1-memory.md
```

**Memory file content**:

```markdown
# AGENT1 Memory Log

## Current Task

[Describe the task you're working on]

## My Approach

[Describe your unique approach to solving this problem]

## Decisions Made

- [Key architectural choices]
- [Implementation approaches]
- [Technology decisions]

## Files Modified

- [List of changed files with brief description]

## Problems Encountered

- [Issues hit and how resolved]

## Next Steps

- [ ] Planning complete
- [ ] Core implementation
- [ ] Testing complete
- [ ] Documentation updated
- [ ] Ready for review

## Notes for Review

- [Important points for peer review phase]
- [Innovative approaches used]
- [Potential improvements]

## Status

Current: Working on independent solution
Phase: 1 - Divergent Execution
```

### Step 4: Work and Completion

Agent1 works independently, updates memory file, then signals completion:

```bash
# When done with implementation
echo "agent1: $(date '+%Y-%m-%d %H:%M:%S') - PHASE1_COMPLETE - Solution ready for review" >> .agor/agentconvo.md
```

### Step 5: Automatic Phase Transition

When all agents complete Phase 1, the protocol automatically detects this and updates the strategy:

```python
from agor.tools.strategy_protocols import ParallelDivergentProtocol

protocol = ParallelDivergentProtocol()
transition = protocol.check_phase_transition()

if transition == "transition_to_convergent":
    result = protocol.transition_to_convergent_phase()
    print(result)
```

**Output**:

```
✅ Phase Transition Complete

New Phase: 2 - Convergent Review
Action Required: All agents review each other's solutions

Next Steps:
1. Examine all agent branches
2. Document findings using review template
3. Propose synthesis approach
4. Build consensus on final solution

Phase 2 is now active!
```

## Key Benefits

### 1. **Concrete Actions**

- **Before**: "Work independently then peer review" (vague)
- **After**: "Post to agentconvo.md: 'agent1: [timestamp] - CLAIMING ASSIGNMENT'" (specific)

### 2. **Automatic Coordination**

- **Before**: Manual coordination and confusion about phase transitions
- **After**: Automatic detection when all agents complete, automatic phase transition

### 3. **File Management**

- **Before**: Agents unsure what files to create or check
- **After**: Specific files created with templates, clear file structure

### 4. **State Tracking**

- **Before**: No way to know current strategy state
- **After**: `check_strategy_status()` shows current phase, recent activity, next actions

### 5. **Role Clarity**

- **Before**: Generic "agent" role
- **After**: Specific roles (divergent_worker, reviewer, synthesizer) with clear responsibilities

## Files Created by Protocols

```
.agor/
├── strategy-active.md         # Strategy details with concrete instructions
├── agentconvo.md             # Agent communication log
├── memory.md                 # Project-level decisions
├── agent1-memory.md          # Agent1 private notes and progress
├── agent2-memory.md          # Agent2 private notes and progress
├── agent3-memory.md          # Agent3 private notes and progress
└── task-queue.json           # Task queue (for Swarm strategy)
```

## Integration with Existing AGOR

The new protocols **extend** rather than **replace** existing AGOR functionality:

- ✅ **Preserves** existing snapshot templates and procedures
- ✅ **Uses** existing `.agor/` directory structure
- ✅ **Follows** existing `agentconvo.md` communication protocol
- ✅ **Integrates** with existing strategy templates
- ✅ **Maintains** compatibility with existing memory system

## Comparison: Before vs After

### Before (Documentation Only)

```
Agent: "What should I do?"
AGOR: "Use Parallel Divergent strategy"
Agent: "How do I start that?"
AGOR: "Multiple agents work independently"
Agent: "But what files do I create? How do I coordinate?"
AGOR: [No concrete answer]
```

### After (Implementation Protocols)

```python
# Agent discovers role
guidance = discover_my_role("agent1")
print(guidance)

# Gets concrete next actions:
# 1. Post to agentconvo.md: 'agent1: [timestamp] - CLAIMING ASSIGNMENT'
# 2. Create branch: git checkout -b solution-agent1
# 3. Initialize memory file: .agor/agent1-memory.md
# 4. Plan your unique approach to the problem
# 5. Begin independent implementation
```

The protocols transform AGOR from having **strategy documentation** to having **strategy implementation** - agents now know exactly what to do at each step.
