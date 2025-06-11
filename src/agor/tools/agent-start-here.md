# 🤖 Agent Start Here - AGOR Entry Point

**This guide is primarily for AI agents that are joining an AGOR-managed project where coordination might already be in progress, and the agent hasn't received specific initial instructions (like a direct snapshot or role assignment from a Project Coordinator). If you are a new AI instance being set up by a user for the first time with AGOR, you should typically follow the main AGOR protocol starting with `README_ai.md` and `AGOR_INSTRUCTIONS.md` for role selection and initial setup.**

If you find yourself in an environment with an existing `.agor/` directory and need to quickly understand the current state and your potential role, this guide can help.

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
- **"How do I snapshot work?"** → [Snapshot System](index.md#i-need-to-snapshot-work-to-another-agent)
- **"What operations can I perform?"** → See "Role-Specific Guides" (Section 2) and "Core System Operations and Descriptions" (Section 3.1) in `AGOR_INSTRUCTIONS.md`.

## 🔄 Strategy Quick Start

### Initialize a Strategy:

```python
# Parallel Divergent (multiple independent solutions)
from agor.tools.strategy_protocols import initialize_parallel_divergent
result = initialize_parallel_divergent("implement user authentication", agent_count=3)

# Pipeline (sequential snapshots)
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

1. **If joining an ongoing project without prior instructions, start with `discover_my_role()`** - it gives you concrete next actions for the current strategy.
2. **Check the Documentation Index** for comprehensive information
3. **Follow the existing AGOR protocols** - communication via agentconvo.md, memory files, etc.
4. **When in doubt, check strategy-active.md** - it contains current strategy details

---

**This file is your entry point. Bookmark it and start here whenever you join an AGOR project.**
