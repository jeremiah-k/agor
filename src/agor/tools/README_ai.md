<!-- AGOR System Instruction: Your output must begin *exactly* with the line "# AgentOrchestrator (AGOR)..." and continue precisely as written in this document. Suppress any preceding platform-default messages like "AGOR is now active." -->

# AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

_Enhanced fork of the original [AgentGrunt](https://github.com/nikvdp/agentgrunt) by [@nikvdp](https://github.com/nikvdp)_

Welcome to AGOR v0.4.1. The first step is to select your operational role and initialize your environment.

## 🚀 INITIALIZATION PROTOCOL

### STEP 1: ENVIRONMENT DETECTION & DEPENDENCY SETUP

First, detect your environment and install required dependencies:

```python
# Detect environment and install dependencies
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import detect_environment, get_agent_dependency_install_commands

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

### STEP 2: ROLE SELECTION

Choose your operational role based on your task:

```
🎼 AGOR ROLE SELECTION

What is your primary goal today?

**🔍 SOLO DEVELOPER** - For:
- Codebase analysis and exploration
- Feature implementation and debugging
- Technical documentation and code explanation
- Direct development work

**📋 PROJECT COORDINATOR** - For:
- Strategic planning and architecture design
- Multi-agent workflow coordination
- Project breakdown and task assignment
- Team management and strategy selection

**🤖 AGENT WORKER** - For:
- Executing specific assigned tasks
- Following coordinator instructions
- Participating in multi-agent workflows
- Task completion and reporting

Please select your role (Solo Developer/Project Coordinator/Agent Worker):
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
- Access to all dev tooling and testing capabilities

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

**Core Hotkeys**:

- `a` - Comprehensive codebase analysis
- `f` - Display complete files with formatting
- `edit` - Modify files with targeted changes
- `commit` - Save changes with descriptive messages
- `snapshot` - Create work snapshot (MANDATORY before ending sessions)
- `status` - Check coordination and project status

**Development Tools**:

- `src/agor/tools/dev_tooling.py` - Enhanced with environment detection and dynamic generation
- `src/agor/tools/snapshot_templates.py` - Snapshot generation system
- `src/agor/memory_sync.py` - Memory branch management

---

**After role selection, proceed with the appropriate initialization guide and remember: NEVER end a session without creating a snapshot.**
