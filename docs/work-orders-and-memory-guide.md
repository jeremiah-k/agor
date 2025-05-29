# 📋 Work Orders and Memory System Guide

This guide explains AGOR's work order system, memory branches, and the important snapshot protocols that enable seamless agent coordination and context preservation.

## 🎯 Overview

AGOR's memory system consists of three key components:

1. **Work Orders**: Structured task definitions stored in memory branches
2. **Agent Snapshots**: Complete context preservation for agent transitions  
3. **Memory Branches**: Git branches dedicated to storing work orders, snapshots, and coordination data

## 🔧 Memory Branch Architecture

### Memory Branch Naming Convention

```
agor/mem/YYYYMMDD_HHMMSS_session_description
```

**Examples**:
- `agor/mem/20250528_174758_documentation_session`
- `agor/mem/20250528_160138_feature_development`
- `agor/mem/20250528_153950_bug_investigation`

### What Gets Stored in Memory Branches

Memory branches contain:
- **Work Orders**: `.agor/work-order-name.md`
- **Agent Snapshots**: `.agor/snapshot-timestamp.md` 
- **Coordination Logs**: `.agor/coordination.md`
- **Memory Database**: `.agor/memory.db` (SQLite)
- **Task Queues**: `.agor/task-queue.json`

### ⚠️ **CRITICAL: Memory Branch Safety Protocol**

**NEVER checkout memory branches directly**. Memory branches are for storage only and should be accessed using safe read-only methods:

#### ✅ **SAFE: Read-Only Access**
```bash
# Read files from memory branch without checking out
git show origin/agor/mem/20250528_174758_session:.agor/work-order.md

# Copy file to temporary location for review
git show origin/agor/mem/20250528_174758_session:.agor/work-order.md > temp_work_order.md
cat temp_work_order.md
rm temp_work_order.md
```

#### ❌ **UNSAFE: Direct Checkout**
```bash
# NEVER DO THIS - Can corrupt your working state
git checkout agor/mem/20250528_174758_session
```

## 🤝 Handoff Protocol Documentation

### Creating Proper Handoff Prompts

When creating handoff prompts for other agents, follow this exact protocol:

#### **Single Codeblock Format**

Handoff prompts must be contained in a **single codeblock** using **double backticks** (``):

```
``
# 🧪 CRITICAL WORK ORDER: Task Name

## Agent Assignment
**Role**: Specific Agent Role
**Task**: Clear task description

## Work Order Location
**Memory Branch**: agor/mem/YYYYMMDD_HHMMSS_session_description
**Work Order File**: .agor/work-order-filename.md

## Critical Setup (MUST DO FIRST)
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling
test_tooling()

## Access Work Order (NEVER checkout memory branch)
git show agor/mem/YYYYMMDD_HHMMSS_session:.agor/work-order-filename.md > temp_work_order.md
cat temp_work_order.md
rm temp_work_order.md

## Key Requirements
1. Requirement 1
2. Requirement 2
3. CRITICAL: Specific critical requirements

## Success Criteria
- Success criterion 1
- Success criterion 2

Ready to begin? Access work order using git show and confirm receipt.
``
```

#### **Key Protocol Rules**

1. **Single Codeblock Only**: Use exactly **two backticks** (``) to wrap the entire prompt
2. **No Nested Codeblocks**: If you need to show code examples within the prompt, use **two backticks** for nested code
3. **Memory Branch Reference**: Always include the exact memory branch name
4. **Safe Access Instructions**: Always include `git show` commands, never `git checkout`
5. **Setup Instructions**: Include any required setup steps
6. **Clear Success Criteria**: Define what constitutes successful completion

#### **Example with Nested Code (Use 2 Backticks)**

```
``
## Access Work Order
git show origin/agor/mem/20250528_174758_session:.agor/work-order.md > temp.md

## Setup Required
``
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling
test_tooling()
``

Ready to begin?
``
```

### Receiving Handoff Prompts

When receiving a handoff prompt:

1. **Follow Setup Instructions**: Execute any setup commands first
2. **Access Work Order Safely**: Use `git show` commands as provided
3. **Confirm Receipt**: Update coordination logs
4. **Verify Understanding**: Review all requirements before proceeding

## 📸 Agent Snapshot System

### Creating Snapshots

Snapshots preserve complete agent context for seamless transitions:

```bash
# Create snapshot using AGOR hotkey
snapshot
```

### Snapshot Storage

Snapshots are stored in memory branches with this structure:

```
.agor/
├── snapshot-20250528-181040.md     # Snapshot document
├── memory.db                       # SQLite database
└── coordination.md                 # Coordination logs
```

### Snapshot Document Structure

Every snapshot includes:

- **🎯 Problem Definition**: What we're solving
- **✅ Work Completed**: Accomplishments so far  
- **📝 Commits Made**: Git history with explanations
- **📁 Files Modified**: Complete change inventory
- **📊 Current Status**: Current state assessment
- **🔄 Next Steps**: Prioritized action items
- **🧠 Technical Context**: Implementation details
- **🎯 Snapshot Instructions**: How to continue

## 🗄️ SQLite Memory Database

### Database Schema

The memory database stores:

- **agent_memories**: Agent context and decisions
- **coordination_logs**: Inter-agent communication
- **project_state**: Project-wide state tracking
- **snapshots**: Structured snapshot data

### Memory Operations

```python
from agor.tools.sqlite_memory import SQLiteMemoryManager

# Initialize memory manager
manager = SQLiteMemoryManager()

# Add memory entry
manager.add_memory("agent-id", "context", "Important context", {"key": "value"})

# Create snapshot
manager.create_snapshot(
    snapshot_id="unique-id",
    from_agent="current-agent",
    problem_description="Problem being solved",
    work_completed="Work done so far",
    # ... other fields
)

# Retrieve memories
memories = manager.get_memories("agent-id", memory_type="context")
```

## 🔄 Memory Sync System

### Automatic Synchronization

The memory system automatically syncs with memory branches:

- **On Startup**: Pulls latest memory state
- **On Shutdown**: Commits and pushes memory updates
- **Branch Management**: Creates and manages memory branches

### Sync Dependencies

Memory sync requires:
- `platformdirs` package for cross-platform paths
- Git repository with remote access
- Proper branch permissions

## 🛡️ Best Practices

### For Work Order Creators

1. **Use Memory Branches**: Store all work orders in memory branches
2. **Clear Instructions**: Provide exact `git show` commands
3. **Safety First**: Never instruct agents to checkout memory branches
4. **Complete Context**: Include all necessary setup and requirements

### For Work Order Recipients

1. **Follow Protocol**: Use provided `git show` commands exactly
2. **Verify Setup**: Run setup commands before proceeding
3. **Confirm Receipt**: Update coordination logs
4. **Ask Questions**: Clarify unclear requirements

### For Memory Management

1. **Regular Snapshots**: Create snapshots at logical breakpoints
2. **Descriptive Names**: Use clear memory branch names
3. **Clean Handoffs**: Ensure complete context transfer
4. **Safe Access**: Always use read-only access methods

## 🚨 Common Pitfalls

### ❌ **What NOT to Do**

1. **Never checkout memory branches directly**
2. **Don't use nested codeblocks in handoff prompts**
3. **Don't hardcode memory branch names in documentation**
4. **Don't skip setup instructions**
5. **Don't assume context without verification**

### ✅ **What TO Do**

1. **Always use `git show` for memory branch access**
2. **Use single codeblock format for handoff prompts**
3. **Include exact memory branch references**
4. **Follow setup protocols precisely**
5. **Verify understanding before proceeding**

## 🔍 Troubleshooting

### Memory Branch Access Issues

```bash
# If memory branch doesn't exist locally, fetch it
git fetch origin agor/mem/20250528_174758_session

# Then use git show to access files
git show origin/agor/mem/20250528_174758_session:.agor/work-order.md
```

### Memory Sync Issues

```bash
# Check if platformdirs is installed
python -c "import platformdirs; print('✅ platformdirs available')"

# If not installed
pip install platformdirs
```

### Database Issues

```bash
# Validate SQLite memory setup
python -c "
from agor.tools.sqlite_memory import validate_sqlite_setup
success, message = validate_sqlite_setup()
print(f'Memory System: {\"✅ PASS\" if success else \"❌ FAIL\"} - {message}')
"
```

## 📊 Memory System Status

To check memory system health:

```python
from agor.tools.sqlite_memory import SQLiteMemoryManager

manager = SQLiteMemoryManager()
stats = manager.get_database_stats()
print("Memory Database Stats:")
for table, count in stats.items():
    print(f"  {table}: {count} records")
```

---

## 🎯 Quick Reference

### Safe Memory Branch Access
```bash
git show origin/agor/mem/BRANCH_NAME:.agor/file.md
```

### Handoff Prompt Format
```
``
# Work Order Title
## Memory Branch: agor/mem/BRANCH_NAME
## Access: git show origin/agor/mem/BRANCH_NAME:.agor/file.md
``
```

### Memory Operations
```python
from agor.tools.sqlite_memory import SQLiteMemoryManager
manager = SQLiteMemoryManager()
```

**Remember**: Memory branches are for storage, not checkout. Always use safe read-only access methods! 🛡️
