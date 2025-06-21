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

## Detailed Migration Plan for dev_tools.py

### Current State Analysis (1943 lines - WAY over 500 LOC target)

**Functions that are just imports/wrappers (REMOVE):**
- `create_development_snapshot()` → wrapper around `snapshots.create_snapshot()`
- `quick_commit_and_push()` → wrapper around `git_operations.quick_commit_push()`
- `get_workspace_status()` → wrapper around `hotkeys.get_project_status()`
- `display_workspace_status()` → wrapper around `hotkeys.display_project_status()`
- `test_all_tools()` → wrapper around `dev_testing.test_tooling()`
- `detect_current_environment()` → wrapper around `dev_testing.detect_environment()`

**Functions that should be moved to appropriate modules:**
- `generate_handoff_prompt_output()` → move to `agent_prompts.py` (handoff functionality)
- `generate_pr_description_output()` → move to `agent_prompts.py` (output formatting)
- `provide_agor_feedback()` → move to `feedback_manager.py` (feedback functionality)
- `cleanup_agent_directories()` → move to `memory_manager.py` (memory management)
- `generate_session_end_prompt()` → move to `agent_prompts.py` (prompt generation)

**Functions that are utility/formatting (consolidate into utils module):**
- `process_content_for_codeblock()` → wrapper around `agent_prompts.detick_content()`
- `apply_output_formatting()` → move to new `output_formatting.py` module
- `generate_formatted_output()` → move to new `output_formatting.py` module

**Documentation/reference functions (move to dedicated module):**
- `get_available_functions_reference()` → move to new `agent_reference.py` module
- `get_agor_initialization_guide()` → move to new `agent_reference.py` module
- `get_snapshot_requirements()` → move to new `agent_reference.py` module
- `display_memory_architecture_info()` → move to new `agent_reference.py` module

**Workflow functions (move to workflow module):**
- `generate_workflow_prompt_template()` → move to new `workflow_templates.py` module
- `validate_agor_workflow_completion()` → move to new `workflow_templates.py` module
- `get_workflow_optimization_tips()` → move to new `workflow_templates.py` module

### Migration Strategy

#### Phase 1: Create New Specialized Modules
1. Create `src/agor/tools/output_formatting.py` for output formatting functions
2. Create `src/agor/tools/agent_reference.py` for documentation/reference functions
3. Create `src/agor/tools/workflow_templates.py` for workflow template functions

#### Phase 2: Move Functions to Appropriate Modules
1. Move handoff/prompt functions to `agent_prompts.py`
2. Move feedback functions to `feedback_manager.py`
3. Move memory cleanup functions to `memory_manager.py`
4. Move formatting functions to `output_formatting.py`
5. Move reference functions to `agent_reference.py`
6. Move workflow functions to `workflow_templates.py`

#### Phase 3: Remove Wrapper Functions
1. Remove all wrapper functions that just call other modules
2. Update imports across codebase to point directly to source modules
3. Update documentation to reference correct modules

#### Phase 4: Empty or Remove dev_tools.py
1. Either leave dev_tools.py as an empty file with a deprecation notice
2. Or remove it entirely and update all imports
3. Update agent initialization to not reference dev_tools.py

#### Phase 5: Update Documentation and Imports
1. Update all documentation to reference correct modules
2. Update agent initialization guides
3. Update function reference documentation
4. Test all imports work correctly

### Expected Outcome
- dev_tools.py either empty or removed entirely
- Functions in their logical homes
- No more dumping ground for new functions
- Clear separation of concerns
- Modules stay under 500 LOC target

## CLI vs Agent Tools Separation - CRITICAL UNDERSTANDING

### The Architecture (User was RIGHT - I was WRONG)

**CLI Tools (Installed Package):**
- `pyproject.toml` defines the CLI package with `agor = "agor.main:app"`
- `requirements.txt` contains CLI dependencies (FastAPI, Typer, etc.)
- Installed via `pip install agor` or `pipx install agor`
- Used for: `agor bundle`, `agor init`, etc. - command line operations
- For: End users who want to bundle projects for ChatGPT

**Agent Tools (Direct Source Access):**
- `src/agor/tools/agent-requirements.txt` contains minimal agent dependencies
- Only needs: pydantic, pydantic-settings, platformdirs, jinja2, httpx, tqdm
- Agents access tools directly from source: `sys.path.insert(0, 'src')`
- No installation required - just clone repo and import from source
- For: AI agents doing development work

### The Problem I Created
I installed the CLI package (`pip install -e .`) when agents should:
1. Clone the AGOR repo
2. Create venv in AGOR directory (not project directory)
3. Install only `agent-requirements.txt`
4. Import directly from source with `sys.path.insert(0, 'src')`

### Correct Agent Initialization
```bash
# For remote agents
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor
python3 -m venv .venv && source .venv/bin/activate
pip install -r src/agor/tools/agent-requirements.txt

# For local agents (Augment)
# Add AGOR directory as source in Augment settings
# No installation needed - direct source access
```

### Why This Separation Matters
1. **CLI tools** are for users bundling projects
2. **Agent tools** are for AI agents doing development
3. **Different dependencies** - CLI needs web framework, agents need minimal deps
4. **Different access patterns** - CLI is installed globally, agents access source directly
5. **Prevents conflicts** - agents don't pollute project environments with CLI deps

### Documentation Updates Needed
- Update all agent initialization guides to NOT install CLI package
- Clarify the separation in documentation
- Remove references to installing AGOR package for agents
- Emphasize direct source access for agents
