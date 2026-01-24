# AGOR Strategy Implementation Example

Shows how strategy protocols solve the coordination gap in AGOR.

## Problem: Before Implementation Protocols

**Agent asks**: "What should I do?"

**Old response**: "Use Parallel Divergent strategy. Multiple agents work independently then peer review."

**Agent confusion**: "But HOW do I actually start? What files? When are others done?"

## Solution: With Implementation Protocols

### Step 1: Strategy Initialization

```python
from agor.tools.strategy_protocols import initialize_parallel_divergent
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
```

### Step 3: Agent Execution

Agent1 follows concrete instructions:

```bash
# 1. Claim assignment
echo "agent1: $(date '+%Y-%m-%d %H:%M:%S') - CLAIMING ASSIGNMENT" >> .agor/agentconvo.md

# 2. Create branch
git checkout -b solution-agent1

# 3. Check memory file (already created by initialization)
cat .agor/agent1-memory.md
```

### Step 4: Work and Completion

Agent1 works independently, updates memory, then signals completion:

```bash
echo "agent1: $(date '+%Y-%m-%d %H:%M:%S') - PHASE1_COMPLETE - Solution ready for review" >> .agor/agentconvo.md
```

### Step 5: Automatic Phase Transition

When all agents complete Phase 1, the protocol automatically detects and updates:

```python
from agor.tools.strategy_protocols import ParallelDivergentProtocol
protocol = ParallelDivergentProtocol()
transition = protocol.check_phase_transition()

if transition == "transition_to_convergent":
    result = protocol.transition_to_convergent_phase()
    print(result)
```

## Key Benefits

### 1. Concrete Actions

- **Before**: "Work independently then peer review" (vague)
- **After**: "Post to agentconvo.md: 'agent1: [timestamp] - CLAIMING ASSIGNMENT'" (specific)

### 2. Automatic Coordination

- **Before**: Manual coordination and phase transition confusion
- **After**: Automatic detection when all agents complete, automatic phase transition

### 3. File Management

- **Before**: Agents unsure what files to create or check
- **After**: Specific files created with templates, clear file structure

### 4. State Tracking

- **Before**: No way to know current strategy state
- **After**: `check_strategy_status()` shows current phase, recent activity, next actions

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

## Integration with AGOR

The protocols **extend** rather than **replace** existing functionality:

- ✅ Preserves existing snapshot templates
- ✅ Uses existing `.agor/` directory structure
- ✅ Follows existing `agentconvo.md` communication protocol
- ✅ Integrates with existing strategy templates
- ✅ Maintains compatibility with existing memory system

For more details, see:
- `agent_coordination.py` - Agent role discovery and coordination
- `strategy.py` - Strategy management and initialization
- `coordination-audit.md` - Complete implementation status
