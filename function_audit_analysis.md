# AGOR Function Duplication and Inconsistency Audit

## Critical Issues Identified

### 1. **Snapshot Function Signature Inconsistencies**

**Problem**: Multiple functions expect `next_steps` as a list, but agents naturally want to provide strings.

**Affected Functions**:
- `create_snapshot(title, context, next_steps: list)` in snapshots.py
- `generate_snapshot_document(next_steps: List[str])` in snapshot_templates.py
- `create_seamless_handoff(next_steps: list)` in snapshots.py
- `create_snapshot_legacy(next_steps: list)` in snapshots.py

**User Requirement**: Change to accept strings, let agents number them if they want.

### 2. **Handoff Prompt Function Confusion**

**Problem**: Multiple functions with confusing signatures that don't match agent expectations.

**Affected Functions**:
- `generate_handoff_prompt_output(handoff_content: str)` - only takes content, not parameters
- `generate_handoff_prompt_only(work_completed: List[str], ...)` - takes many parameters
- `generate_agent_handoff_prompt_extended(task_description, snapshot_content, ...)` - different signature
- `generate_session_end_prompt(task_description, brief_context)` - minimal parameters

**User Requirement**: Rationalize to have intuitive signatures matching agent expectations.

### 3. **Function Duplications Across Modules**

**Timestamp Functions**:
- `get_current_timestamp()` in git_operations.py
- `get_file_timestamp()` in git_operations.py
- `get_precise_timestamp()` in git_operations.py (mentioned in dev_tools)
- `get_ntp_timestamp()` in git_operations.py (mentioned in dev_tools)

**Commit Functions**:
- `quick_commit_push()` in git_operations.py
- `quick_commit_push_wrapper()` in hotkeys.py (wrapper around the above)
- `quick_commit_and_push()` in dev_tools.py (imports from git_operations)
- `emergency_commit()` in hotkeys.py (calls quick_commit_push)

**Status Functions**:
- `get_project_status()` in hotkeys.py
- `get_workspace_status()` in dev_tools.py
- `quick_status_check()` in hotkeys.py
- `display_project_status()` in hotkeys.py
- `display_workspace_status()` in dev_tools.py

**Memory Functions**:
- `auto_commit_memory()` in memory_manager.py
- `commit_to_memory_branch()` in memory_manager.py
- `commit_memory_to_branch()` mentioned in dev_tools guidelines

### 4. **Dev Tools as Dumping Ground**

**Problem**: dev_tools.py has become a catch-all that imports from everywhere, encouraging duplication.

**Current State**:
- 1943 lines (way over 500 LOC target)
- Imports from: snapshots, hotkeys, checklist, git_operations, memory_manager, agent_prompts, dev_testing
- Contains many wrapper functions that just call other modules
- Agents will keep adding functions here instead of finding proper homes

### 5. **CLI vs Agent Tools Confusion**

**Problem**: I installed the CLI package, but agents should use tools directly.

**Current Issues**:
- Agent requirements.txt suggests agents need to install packages
- But agents should access source directly
- Unclear separation between CLI tools and agent tools

## Recommended Migration Plan

### Phase 1: Fix Data Types
1. Change all `next_steps` parameters from `List[str]` to `str`
2. Update function signatures to be intuitive
3. Fix handoff prompt functions to have consistent, expected signatures

### Phase 2: Consolidate Duplications
1. Keep one implementation of each function in the most appropriate module
2. Remove wrapper functions and duplicates
3. Update all imports to point to canonical implementations

### Phase 3: Migrate from dev_tools.py
1. Move remaining functions to appropriate specialized modules
2. Either empty dev_tools.py or remove it entirely
3. Update all imports across the codebase

### Phase 4: Clarify CLI vs Agent Separation
1. Document which tools are for CLI vs agents
2. Remove agent dependency on installed packages
3. Ensure agents can access tools directly from source
