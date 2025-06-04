# 🛠️ AGOR Development Guide

**For AI agents and developers working on AGOR itself**

This guide ensures consistency, quality, and proper protocol management when developing AGOR. Use this checklist for all changes to maintain the integrity of the multi-agent coordination platform.

> **📜 Related Documentation:**
>
> - **[AGOR Development Log](agor-development-log.md)**: Technical history, architectural decisions, and lessons learned
> - **This Guide**: Current status, guidelines, and checklists for active development

## 🧠 CORE CONTEXT FOR ALL AGENTS

**⚠️ CRITICAL: This section contains permanent context that ALL agents must understand. Do NOT modify this section.**

### 🎯 AGOR Architecture Understanding

(No changes needed in this section)

#### 📦 CLI vs Agent Tools - FUNDAMENTAL DISTINCTION

(No changes needed)

#### 🤖 CLI Commands vs Agent Hotkeys - CRITICAL DISTINCTION

(No changes needed)

#### 📋 Agent Coordination Documents

(No changes needed, already refers to snapshot_templates.py)

#### 🏗️ File Structure Understanding

(No changes needed)

### 🚦 Development Safety Levels

(No changes needed)

### 📁 Key Directories and Their Purposes

(No changes needed)

### 🔄 Commit and Push Protocol

**⚠️ CRITICAL: Commit and push frequently - ALWAYS together!** (Applies to project working branches)

**Frequent commits AND pushes are essential** for AGOR development (when working on the AGOR codebase itself or project codebase).

**Why this approach works well**:

- Agent environments can be unstable, making frequent saves important
- Collaboration benefits from visible progress for snapshots
- Recovery from errors is easier with regular checkpoints
- Git history becomes a useful development log
- **Remote backup prevents work loss** when agent sessions end unexpectedly
- **Enables seamless snapshots** between agents working on the same task

**Recommended Command Pattern (for project working branches):**

```bash
git add . && git commit -m "🔧 Descriptive message" && git push
```

**🛠️ Development Tooling Available (for AGOR development itself):**
For streamlined development when working on AGOR, use the dev tooling functions in `src/agor/tools/dev_tooling.py`:

```python
from agor.tools.dev_tooling import quick_commit_push, auto_commit_memory, create_snapshot

# Quick commit and push (project's working branch)
quick_commit_push("Fix memory sync integration", "🔧")

# Auto-commit memory to its dedicated memory branch (via Memory Synchronization System)
# This is typically handled automatically for standard agents.
# For AGOR developers, this tool can help manage memory branches during dev.
auto_commit_memory("Implemented memory sync hotkeys", "progress", "dev")

# Create comprehensive development snapshot (persisted via Memory Synchronization System)
create_snapshot("Memory Integration", "Completed hotkey implementation")
```

**Good times to commit and push (on project working branches)**:
(No changes needed)

**Commit Message Guidelines**:
(No changes needed)

---

### 📚 Essential Files for Agent Understanding

(No changes needed, already refers to snapshot_templates.py)

### 🔍 Quick Context Checks

(No changes needed)

### 🧪 **CRITICAL: Test Development Tooling During Initialization**

(No changes needed)

### 🤝 Multi-Agent Coordination Principles

1.  **Snapshots are a primary coordination mechanism** - not CLI commands. These are managed by the Memory Synchronization System on memory branches.
2.  **Bundle manifests are for setup** - snapshot documents are for work transitions and state capture, managed by the Memory Synchronization System.
3.  **Most 'commands' are agent menu hotkeys** - not terminal commands.
4.  **The .agor/ directory is the coordination hub** - its contents (agent state, logs, snapshots) are persisted on dedicated memory branches by the Memory Synchronization System. Standard agents should not commit this directory to their project working branches.
5.  **Commit and push frequently (on project working branches)** - work can be lost in agent environments. Memory and coordination state is handled by the Memory Synchronization System.
6.  **Bidirectional workflow is required** - agents must report completion back to coordinators, often through snapshots managed by the Memory Synchronization System.

### 🔄 Work Snapshot & Completion Report Workflow

(No changes needed, consistent with snapshot terminology and system)

---

**🎯 Remember**: AGOR is primarily a bundling tool with sophisticated agent coordination capabilities built on top. The CLI is for bundling; the real power is in the agent tools and coordination system, including the automated Memory Synchronization System.

**🚨 IMPORTANT**: This "Core Context" section should remain stable and always be available to new agents. Only add to it, don't remove or significantly change existing content.

## 📊 Implementation Status Tracking

(No changes needed)

### ✅ Fully Implemented Features

(No changes needed, already refers to snapshot_templates.py and snapshot_prompts.py)

### 🟡 Partially Implemented Features

(No changes needed)

### ❌ Missing Implementations

(No changes needed)

### 🎯 Development Status Summary

(No changes needed)

## 🔍 Current Development Priorities

(No changes needed, references to 'handoff' already updated to 'snapshot')

### 📝 Documentation Enhancement (High Priority)

(No changes needed)

#### 3. SQLite Memory System (Primarily for Internal/Advanced Use)

- **Status**: Experimental system.
- **Purpose**: Advanced coordination logging and state management, primarily for internal AGOR system needs or specialized development tasks.
- **Agent Interface**: **Not the default for standard agent memory.** Standard agents use the markdown-based Memory Synchronization System. SQLite hotkeys (`mem-add`, `mem-search`, etc. related to direct DB interaction) are generally not for standard agent use unless explicitly directed by a coordinator for a specific advanced setup. The main agent memory (e.g., `.agor/memory.md`, `agentN-memory.md`) is markdown-based and managed by the automated Memory Synchronization System.

### ✅ Completed Audit Items

(No changes needed)

## 🎯 CLI Usage Patterns and Agent Expectations

(No changes needed)

### 🤖 Agent Manifest vs CLI Commands - CRITICAL DISTINCTION

(No changes needed, consistent with snapshot documents)

#### 📋 Snapshot Documents (formerly referred to as Snapshot Documents or Agent Manifests in some contexts)

(No changes needed, consistent with snapshot_templates.py)

### 🤖 Internal Commands vs User Commands

(No changes needed)

### 🎭 Agent Role Clarification

(No changes needed)

### ⚠️ Common Agent Mistakes to Avoid

(Add clarification about `.agor/` directory)

#### ❌ "I'll use `agor init` to start working"

(No changes needed)

#### ❌ "I need to run `agor pd` to set up parallel work"

(No changes needed)

#### ❌ "I should use `agor status` to check my progress"

(No changes needed)

#### ❌ "I need to install AGOR to work with this project"

(No changes needed)

#### ❌ "I should commit the `.agor/` directory to my main project branch"

**Problem**: Committing AGOR's operational state files (like `agentconvo.md`, `agentN-memory.md`, `strategy-active.md`) to the main project branch clutters the project history with transient coordination data.
**Solution**: **The AGOR Memory Synchronization System automatically handles the persistence of the `.agor/` directory and its contents on dedicated memory branches (e.g., `agor/mem/BRANCH_NAME`).** Standard agents should not manually commit these files to their project's working or main branches. Project repositories may even include `.agor/` in their `.gitignore` for this reason, which is compatible with the Memory Synchronization System's operation on its dedicated branches.

### 🎯 How to Determine Your Context

(No changes needed)

### 🚦 Development Safety Guidelines

(No changes needed, already mentions snapshot structure)

### 📈 Implementation Statistics

(No changes needed)

## 🔍 Pre-Development Checklist

(No changes needed)

## 📋 Development Checklist

(No changes needed)

### Protocol and Hotkey Changes

(Change `handoff` to `snapshot` if any linger, but seems updated)

- [ ] **Hotkey additions/changes**: Any modification to the hotkey system (Note: `snapshot`, `da`, `hp` hotkeys now relate to "snapshot" functionality).
- [ ] **Role behavior changes**: Modifications to role-specific functionality.
- [ ] **Communication format changes**: Changes to .agor/ file formats (e.g., snapshot structure), managed by Memory Sync System.
- [ ] **Bundle structure changes**: Modifications to bundle contents or layout.
- [ ] **Memory system changes**: Changes to memory management or storage (primarily impacting Memory Sync System).

### Integration Testing

- [ ] **Multi-agent workflows**: Test coordination between agents (data persisted via Memory Sync System).
- [ ] **Snapshot procedures**: Verify snapshot generation and reception (data persisted via Memory Sync System).
- [ ] **Communication protocols**: Test .agor/ directory structure and files (on memory branches via Memory Sync System).

## 🚨 Critical Checkpoints

(No changes needed, consistent with snapshot terminology)

## Testing Coordination Strategies & State Management

(This section is key for developers working on AGOR itself)

AGOR's core functionality includes initializing and managing coordination strategies, which involves creating and modifying files within an `.agor/` directory. For **standard agent operation in a target project**, these files are automatically managed by the **Memory Synchronization System** on dedicated memory branches.

**When developing or testing AGOR itself**, developers (or agents acting as developers of AGOR) need to be mindful of this:

### Avoid Committing Local State to the AGOR Repository (Main/Working Branches)

The AGOR project's root `.gitignore` file is configured to ignore common operational state files and directories that might be generated during testing (e.g., `/.agor/state/`, `/.agor/memory.db`). This is crucial to prevent committing local test states into the main AGOR codebase's working branches.

### Best Practice: Use a Separate Sample Project for Testing AGOR's Effect on Projects

To thoroughly test AGOR CLI commands that initialize strategies or manage state within a _target project_ (e.g., `agor init`, `agor pd` when run by a user on _their_ project):
(No changes to the numbered list, it's already good practice)

### Testing the Memory Synchronization System Itself

When developing features related to the **Memory Synchronization System** or features that interact heavily with memory branches:

- Utilize the manual memory sync hotkeys (`mem-sync-start`, `mem-sync-save`, `mem-sync-restore`, `mem-sync-status`) to control and inspect the synchronization process.
- Verify that `.agor/` contents are correctly committed to and retrieved from the specified memory branches (e.g., `agor/mem/BRANCH_NAME`).
- Test fallback mechanisms: ensure agents can continue operating if a memory sync operation fails temporarily.
- Ensure that the system correctly handles `.gitignore` on the main project branch while still committing `.agor/` to memory branches.

---

_This guide evolves with AGOR. Suggest improvements through the `meta` hotkey or GitHub issues._
