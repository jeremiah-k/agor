# 🤖 Agent Start Here - AGOR Entry Point

**New to this project? Start here for immediate guidance.**

## 🎯 Quick Discovery

```python
# Find out what you should do right now
from agor.tools.agent_coordination import discover_my_role
print(discover_my_role("agent1"))  # Replace with your agent ID
```

This will tell you:

- What strategy is active (if any)
- Your role in the current strategy
- Concrete next actions to take
- Files to check and commands to run

## 📚 Need More Information?

**Check the [Documentation Index](index.md)** - it's designed for token-efficient lookup:

### Common Needs:

- **"What should I do?"** → Use `discover_my_role()` above
- **"How do I start a strategy?"** → [Strategy Implementation](index.md#i-need-to-implementexecute-a-strategy)
- **"How do I coordinate with other agents?"** → [Multi-agent Coordination](index.md#i-need-multi-agent-coordination-strategies)
- **"How do I hand off work?"** → [Handoff System](index.md#i-need-to-hand-off-work-to-another-agent)
- **"What are the hotkeys?"** → [README_ai.md Lines 120-220](../src/agor/tools/README_ai.md)

## 🔄 Strategy Quick Start

### Initialize a Strategy:

```python
# Parallel Divergent (multiple independent solutions)
from agor.tools.strategy_protocols import initialize_parallel_divergent
result = initialize_parallel_divergent("implement user authentication", agent_count=3)

# Pipeline (sequential handoffs)
from agor.tools.strategy_protocols import initialize_pipeline
result = initialize_pipeline("build REST API", stages=["Foundation", "Enhancement", "Testing"])

# Swarm (task queue)
from agor.tools.strategy_protocols import initialize_swarm
tasks = ["Create models", "Implement logic", "Add tests", "Write docs"]
result = initialize_swarm("user system", tasks, agent_count=4)
```

### Check Current Status:

```python
from agor.tools.agent_coordination import check_strategy_status
print(check_strategy_status())
```

## 📁 Key Files to Know

- **`.agor/strategy-active.md`** - Current strategy details and instructions
- **`.agor/agentconvo.md`** - Agent communication log
- **`.agor/agent[N]-memory.md`** - Your private notes and progress
- **`.agor/task-queue.json`** - Task queue (Swarm strategy)

## 🆘 Quick Commands

```bash
# Check strategy details
cat .agor/strategy-active.md

# Check recent agent communication
cat .agor/agentconvo.md | tail -10

# Check your memory file (replace agent1 with your ID)
cat .agor/agent1-memory.md
```

## 🎯 Remember

1. **Always start with `discover_my_role()`** - it gives you concrete next actions
2. **Check the Documentation Index** for comprehensive information
3. **Follow the existing AGOR protocols** - communication via agentconvo.md, memory files, etc.
4. **When in doubt, check strategy-active.md** - it contains current strategy details

---

**This file is your entry point. Bookmark it and start here whenever you join an AGOR project.**
