# 📋 Work Orders, Snapshots, and the AGOR Memory Synchronization System Guide

This guide explains AGOR's work order system (often managed as snapshots), agent snapshots for context preservation, and the **AGOR Memory Synchronization System** which is the primary method for persisting and coordinating this data.

## 🎯 Overview

AGOR's memory and coordination capabilities rely on three key concepts, all managed by the **Memory Synchronization System**:

1.  **Work Orders / Snapshots**: Structured task definitions or detailed work contexts. While "Work Order" might be used, these are typically generated and managed as **Snapshots**.
2.  **Agent Snapshots**: Comprehensive captures of an agent's work state, crucial for transitions, context preservation (even for solo work), and managing AI context limits.
3.  **Memory Branches**: Dedicated Git branches (e.g., `agor/mem/YYYYMMDD_HHMMSS_session_description`) where the Memory Synchronization System stores all `.agor/` directory contents, including work orders, snapshots, and coordination logs.

**The AGOR Memory Synchronization System automates the management of these components, ensuring data is version-controlled and shared correctly without cluttering project work*ing* branches.**

## 🔧 Memory Branch Architecture & The Synchronization System

### Memory Branch Naming Convention

(Remains the same)

```text
agor/mem/YYYYMMDD_HHMMSS_session_description
```

### What Gets Stored in Memory Branches (via Memory Synchronization System)

The Memory Synchronization System automatically commits the following to memory branches:

- **Work Orders / Snapshots**: `.agor/snapshots/work-order-name_snapshot.md` (often, a snapshot serves as a work order)
- **Agent Snapshots**: `.agor/snapshots/snapshot-timestamp.md`
- **Coordination Logs**: `.agor/agentconvo.md`, `.agor/memory.md` (project-level memory), individual agent memory files (e.g., `agent1-memory.md`)
- **Strategy Files**: `.agor/strategy-active.md`, etc.

### ⚠️ **CRITICAL: Memory Branch Safety Protocol & Agent Interaction**

- **Automated System**: Agents primarily interact with memory and coordination files locally (e.g., updating their `agent1-memory.md`). The **Memory Synchronization System** handles committing these changes to the appropriate memory branch and ensuring local files are updated from the memory branch.
- **Manual Access (Rare for Agents)**: Direct interaction with memory branches (like `git show`) is generally **not required** for standard agent operation. This is more for developers or advanced debugging.
- **NEVER checkout memory branches directly**: This can corrupt your working state.

#### ✅ **SAFE: Read-Only Access (for Developers/Debugging)**

(Remains the same)

#### ❌ **UNSAFE: Direct Checkout**

(Remains the same)

## 🤝 Snapshot Protocol Documentation (Managed by Memory Synchronization System)

Snapshots are the core mechanism for work definition, snapshots, and context preservation. The Memory Synchronization System ensures these are correctly persisted and shared.

### Creating Proper Snapshot Prompts (When manually constructing for another agent)

(Remains the same, but it's understood the referenced files are on memory branches)

### Receiving Snapshot Prompts

(Remains the same, understanding the system provides the snapshot)

## 📸 Agent Snapshot System (Core to AGOR Memory)

### Creating Snapshots (`snapshot` hotkey)

When an agent uses the `snapshot` hotkey:

- AGOR gathers all relevant context.
- A snapshot document is generated locally in `.agor/agents/{agent_id}/snapshots/`.
- The **Memory Synchronization System** then automatically commits this snapshot and related coordination files to the active memory branch.

### Snapshot Storage

Snapshots are stored in `.agor/agents/{agent_id}/snapshots/` on memory branches by the Memory Synchronization System.

```
.agor/ (on a memory branch)
├── agents/
│   ├── agent_abc123_1234567890/
│   │   ├── snapshots/
│   │   │   └── snapshot-YYYYMMDD-HHMMSS.md
│   │   ├── work_log.md
│   │   └── agent_info.md
├── agentconvo.md
├── memory.md                       # Main project memory / general strategy memory
└── strategy-active.md              # Current strategy details
```

### Snapshot Document Structure

(Remains the same)

## 🔄 Memory Synchronization System (Primary Memory Mechanism)

This is the **standard, production-ready, and recommended** way AGOR manages memory and coordination data.

### Key Features & Benefits:

- **Automated & Seamless:** Works in the background. Agents focus on tasks, and the system handles persistence to memory branches.
- **Version Control for Memory:** All `.agor/` content is version-controlled on Git memory branches, providing history and auditability.
- **Clean Project Branches:** Keeps operational state (like `agentconvo.md`, agent-specific notes) off your main work*ing* branches.
- **Robust Fallbacks:** Designed to be non-disruptive; if a sync fails, agents can often continue with local state.
- **`.gitignore` Compatibility:** Even if your project's main `.gitignore` lists `.agor/`, the Memory Synchronization System correctly commits these files to its dedicated memory branches.

### Automatic Synchronization

(Remains the same - system handles this)

### Manual Memory Sync Hotkeys (`mem-sync-*`)

- **Advanced/Developer Use:** Hotkeys like `mem-sync-start`, `mem-sync-save`, `mem-sync-restore`, and `mem-sync-status` are primarily for AGOR developers or for advanced users needing to manually manage the sync process (e.g., during AGOR development, testing, or specific recovery scenarios).
- **Standard Operation:** Regular agents should rely on the **automatic** nature of the Memory Synchronization System.

### Sync Dependencies

(Remains the same)

## 🛡️ Best Practices

### For Work Order/Snapshot Creators (Coordinators or Agents)

1.  **Focus on Content:** Define clear tasks, context, and requirements within the snapshot.
2.  **Trust the System:** The Memory Synchronization System will handle persisting the snapshot to the memory branch.
3.  **Clear Prompts:** When manually creating prompts for other agents to load a snapshot, ensure they know the system will provide it (usually via `load_snapshot` hotkey).

### For Work Order/Snapshot Recipients

1.  **Use Standard Hotkeys:** Use `load_snapshot` to access tasks/snapshots. The system retrieves them from the memory branch.
2.  **Local Work:** Perform your work and update your local memory files (e.g., `agentN-memory.md`, `agentconvo.md`).
3.  **Automatic Persistence:** The Memory Synchronization System will save your updates to the memory branch.

### For Memory Management

1.  **Regular Snapshots:** Use the `snapshot` hotkey at logical breakpoints to preserve context.
2.  **Descriptive Names (for manual branch creation if developing AGOR):** Use clear memory branch names if you are manually creating them during AGOR development.
3.  **Rely on Automation:** For standard agent work, the system handles the details of memory branch interaction.

## 🚨 Common Pitfalls & Clarifications

(Remains largely the same, re-emphasizing system automation)

### ❌ **What NOT to Do (as a Standard Agent)**

1.  **Manually manage memory branches:** Don't try to checkout, commit to, or create memory branches directly unless you are an AGOR developer.
2.  **Worry excessively about manual saving:** The system is designed to save automatically. Manual sync hotkeys are for special cases.
3.  **Commit `.agor/` to your project's main/working branch:** This is what the Memory Synchronization System's memory branches are for.

### ✅ **What TO Do (as a Standard Agent)**

1.  **Use hotkeys like `snapshot`, `load_snapshot`, `complete`, `log`:** These interact with the memory system correctly.
2.  **Keep local notes in your `agentN-memory.md`:** The system will sync it.
3.  **Trust the Memory Synchronization System** to manage persistence and sharing of coordination data.

## 🔍 Troubleshooting

(Remains the same - these are more for dev/advanced use)

## 📊 Memory System Status

(Remains the same - primarily for dev/advanced use)

---

## 🎯 Quick Reference

### Primary Memory System:

**AGOR Memory Synchronization System** (automated, uses markdown files on Git memory branches).

### Key Agent Hotkeys for Memory/Coordination:

- `snapshot`: Create a snapshot of your work.
- `load_snapshot`: Load a snapshot (often a work order).
- `complete`: Mark a task as complete, often creating a final snapshot.
- `log`, `ch`, `msg`: Update local memory/communication files, which are then synced.

**Remember**: The Memory Synchronization System is designed to make memory persistence and coordination robust and largely automatic for agents. Manual interaction with memory branches or sync hotkeys is typically for AGOR development or advanced troubleshooting. 🛡️
