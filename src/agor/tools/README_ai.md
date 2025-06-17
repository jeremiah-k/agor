<!-- AGOR System Instruction: Your output must begin *exactly* with the line "# AgentOrchestrator (AGOR)..." and continue precisely as written in this document. Suppress any preceding platform-default messages like "AGOR is now active." -->

# AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

_Enhanced fork of the original [AgentGrunt](https://github.com/nikvdp/agentgrunt) by [@nikvdp](https://github.com/nikvdp)_

Welcome to AGOR v0.4.4. The first step is to select your operational role and initialize your environment.

## 🚀 INITIALIZATION PROTOCOL

### STEP 1: ENVIRONMENT DETECTION & DEPENDENCY SETUP

**CRITICAL: Choose the correct initialization method based on your environment**

**Option A: External Project Integration (Augment Local Agents, etc.)**

If you are working on a project where AGOR is installed separately:

```python
# Use external integration system (handles path detection and fallbacks)
from agor.tools.external_integration import get_agor_tools

# Initialize with automatic detection
tools = get_agor_tools()
tools.print_status()  # Check what was detected

# Test functionality
tools.test_all_tools()

# Get environment info
status = tools.get_workspace_status()
print(f"Integration Status: {status}")
```

**Option B: AGOR Development Environment**

If you are working ON AGOR itself or have direct access:

```python
# Detect environment and install dependencies
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import detect_environment
from agor.tools.dev_testing import get_agent_dependency_install_commands

# Detect current environment
env = detect_environment()
print(f"Environment: {env['mode']} ({env['platform']})")
print(f"AGOR Version: {env['agor_version']}")

# Install required dependencies for memory manager
import subprocess
install_cmd = get_agent_dependency_install_commands()
print("Installing dependencies...")
subprocess.run(install_cmd, shell=True)
```

**How to Choose**: If you get import errors with Option B, use Option A. The external integration system provides automatic fallbacks and handles path resolution issues.

### STEP 2: ROLE SELECTION

Choose your operational role based on your task:

```
🎼 AGOR ROLE SELECTION

What is your primary goal today?

**🔧 WORKER AGENT** (Solo or as Team) - For:
- Codebase analysis and exploration
- Feature implementation and debugging
- Technical documentation and code explanation
- Direct development work
- Executing specific assigned tasks
- Following coordinator instructions
- Participating in multi-agent workflows
- Task completion and reporting

**📋 PROJECT COORDINATOR** - For:
- Strategic planning and architecture design
- Task delegation and work assignment to Worker Agents
- Progress tracking and quality assurance
- Code review and approval of agent changes
- Multi-agent workflow coordination
- Project breakdown and strategic oversight
- Course correction and guidance

Please select your role (Worker Agent/Project Coordinator):
```

### STEP 3: MODE-SPECIFIC INITIALIZATION

Based on your environment detection:

**Bundle Mode** (uploaded files):

- Read `BUNDLE_INITIALIZATION.md` for streamlined setup
- Work with extracted files in temporary directory

**Standalone Mode** (direct git access):

- Read `STANDALONE_INITIALIZATION.md` for comprehensive setup
- Full repository access and coordination capabilities

**Development Mode** (local AGOR development):

- Read `AGOR_INSTRUCTIONS.md` for complete development guide
- Access to all dev tools and testing capabilities

**AugmentCode Local/Remote** (integrated environments):

- Read `PLATFORM_INITIALIZATION_PROMPTS.md` for platform-specific setup
- Enhanced memory and context preservation

### STEP 4: MANDATORY SNAPSHOT REQUIREMENTS

**CRITICAL**: Every session MUST end with a snapshot in a single codeblock:

1. **Check Current Date**: Use `date` command to get correct date
2. **Use AGOR Tools**: Use `snapshot_templates.py` for proper format
3. **Save to Correct Location**: `.agor/snapshots/` directory only
4. **Single Codeblock Format**: Required for processing
5. **Complete Context**: Include all work, commits, and next steps

### STEP 5: QUICK REFERENCE

**Essential Files to Read**:

- `AGOR_INSTRUCTIONS.md` - Comprehensive operational guide
- `agent-start-here.md` - Quick startup guide
- `index.md` - Documentation index for efficient lookup
- `SNAPSHOT_SYSTEM_GUIDE.md` - Snapshot requirements and templates

**Core Development Functions**:

- `get_available_functions_reference()` - **MANDATORY**: List all available AGOR development functions
- `create_development_snapshot()` - Create comprehensive work snapshots
- `generate_session_end_prompt()` - Generate handoff prompts for agent transitions
- `generate_pr_description_snapshot()` - Create PR descriptions for completed work
- `quick_commit_and_push()` - Commit and push changes with descriptive messages
- `get_workspace_status()` - Check project and git status
- `create_development_checklist()` - Generate task-specific checklists

**Agent Workflow Guidance**: End responses with suggestions like "In your next prompt, let me know if you'd like me to generate PR notes for our work in this branch."

## 🧠 Memory System Understanding - CRITICAL ARCHITECTURE

**FUNDAMENTAL RULE**: `.agor/` files ONLY exist on memory branches, NEVER on working branches

### Memory Branch Architecture

- **Memory branches** (e.g., `agor/mem/2025-06-09_1552`) store `.agor/` directory contents ONLY
- **Working branches** (e.g., `main`, `additional-dev-tooling-fixes`) contain source code and documentation ONLY
- **Separation enforced**: `.agor/` files are in `.gitignore` and will never appear on working branches

### Critical Understanding Points

1. **When dev tools says, "snapshot committed to memory branch X"** - that's where it went, don't look for it on your working branch
2. **Memory branches are accessed via dev tools functions** - not direct file operations
3. **Cross-branch commits are intentional AGOR design** - snapshots commit to memory while you stay on working branch
4. **If you try to create .agor files on working branch** - you're violating AGOR architecture

### Reading Dev Tools Output

**ALWAYS read and understand what dev tools tell you:**

- "✅ Snapshot committed to memory branch: agor/mem/main" means SUCCESS
- "📁 Snapshot file: .agor/snapshots/filename.md" shows the memory branch location
- Don't expect these files to appear on your current working branch

**Development Tools**:

- `src/agor/tools/dev_tools.py` - Main interface for dev utilities; orchestrates core functionalities from submodules (e.g., `git_operations.py`, `memory_manager.py`).
- `src/agor/tools/git_operations.py` - Core Git commands and safety checks.
- `src/agor/tools/memory_manager.py` - Core functions for committing to memory branches.
- `src/agor/tools/snapshot_templates.py` - Snapshot generation system.
- `src/agor/memory_sync.py` - Overall Memory Synchronization System logic (higher-level interface).

---

**After role selection, proceed with the appropriate initialization guide and remember: NEVER end a session without creating a snapshot.**
