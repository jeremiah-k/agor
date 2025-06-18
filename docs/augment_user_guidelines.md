# AGOR (AgentOrchestrator) User Guidelines for AugmentCode Local Agent

_These guidelines enable the AugmentCode Local Agent to effectively utilize the AGOR multi-agent development coordination platform. The agent should read AGOR documentation from workspace sources and follow structured development protocols._

## 🎯 Core AGOR Principles

When working on development tasks, you are operating within the **AGOR (AgentOrchestrator)** framework - a sophisticated multi-agent development coordination platform. Your primary responsibilities:

1. **Read AGOR Documentation**: Always start by reading the AGOR protocol files from workspace sources
2. **Use AGOR Dev Tools**: Always use the programmatic dev tools for all AGOR operations
3. **Follow AGOR Protocols**: Use structured workflows, development tools, and coordination methods
4. **Create Snapshots**: Always create snapshots before ending sessions using AGOR dev tools
5. **Maintain Context**: Use AGOR's memory and coordination systems for session continuity
6. **Commit Frequently**: Use quick_commit_and_push() often to keep work synchronized

## 🚀 Initialization Protocol

### Step 1: Initialize AGOR Dev Tools

```
MANDATORY: Execute these functions to initialize the AGOR system:

python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import get_agor_initialization_guide, get_available_functions_reference, test_all_tools

print('🚀 AGOR INITIALIZATION')
print('=' * 50)
print(get_agor_initialization_guide())

print('\n📋 AVAILABLE FUNCTIONS REFERENCE')
print('=' * 50)
print(get_available_functions_reference())

print('\n🧪 TESTING TOOLS')
print('=' * 50)
test_all_tools()
print('✅ AGOR initialization complete!')
"

If the above functions don't work, read these files as fallback:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/index.md (documentation index for efficient lookup)
```

### Step 2: Understand Core AGOR Systems

**🔧 Dev Tools (Primary Interface)**:
- Always use AGOR dev tools for all operations
- Never manually create or manage .agor files
- All memory operations handled automatically by dev tools

**📸 Snapshot System**:
- Snapshots saved to `.agor/agents/{agent_id}/snapshots/` on memory branches
- Use `create_development_snapshot()` function only
- Never manually create snapshot files

**🧠 Memory Branch Architecture**:
- Memory branches (e.g., `agor/mem/main`) store all .agor files
- Working branches never contain .agor directories
- Cross-branch commits handled automatically by dev tools

### Step 3: Role Selection (Worker Agent Focus)

You will typically operate as a **🔍 Worker Agent** for:
- Codebase analysis and exploration
- Feature implementation and debugging
- Technical documentation and code explanation
- Direct development work and task execution

**Note**: Multi-agent coordination strategies are experimental and not recommended for production use. Focus on the mature snapshot/memory system and dev tools.

### Step 4: External Project Integration (CRITICAL)

**If working on external projects** (where AGOR is installed separately from the project):

```python
# ALWAYS use external integration system instead of direct imports
from agor.tools.external_integration import get_agor_tools

# Initialize with automatic AGOR detection
tools = get_agor_tools()
tools.print_status()  # Check integration status

# Use AGOR functions through the tools object
tools.generate_pr_description_output("content")
tools.create_development_snapshot("title", "context")
```

**Why this is critical**: Direct imports fail when AGOR is installed separately. The external integration system provides automatic detection and fallback mechanisms.

**See**: src/agor/tools/EXTERNAL_INTEGRATION_GUIDE.md for complete setup instructions.

## 🛠️ AGOR Development Tools

### Core Dev Tools (Always Use These)

**📸 Snapshot & Memory Management**:
- `create_development_snapshot(title, context, next_steps)` - Create comprehensive work snapshots
- `generate_session_end_prompt(task_description, brief_context)` - Generate handoff prompts
- `generate_pr_description_output(content)` - Create PR descriptions (brief content only)
- `generate_release_notes_output(content)` - Create release notes (brief content only)

**⚡ Quick Development Workflow**:
- `quick_commit_and_push(message, emoji)` - **USE FREQUENTLY** - Efficient commit and push
- `get_workspace_status()` - Check project and git status
- `test_all_tools()` - Verify all dev tools work correctly

**🧠 Memory Operations (Automatic)**:
- All memory operations happen automatically on separate memory branches
- Never manually create or edit .agor files
- Snapshots automatically saved to `.agor/agents/{agent_id}/snapshots/` on memory branches

### Function Access Methods

**For External Projects (Recommended)**:

```python
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()

# Use functions through tools object:
tools.create_development_snapshot("title", "context", ["next", "steps"])
tools.quick_commit_and_push("message", "🔧")
tools.generate_pr_description_output("content")
```

**For AGOR Development Only**:

```python
# Only use direct imports when working ON AGOR itself
from agor.tools.dev_tools import (
    create_development_snapshot,
    quick_commit_and_push,
    generate_pr_description_output,
)
```

### Critical Workflow Requirements

**🚨 MANDATORY Session End Process**:

1. **Use quick_commit_and_push() frequently** during development to keep work synchronized
2. **Create development snapshot** using `create_development_snapshot()` function
3. **Generate handoff prompt** using `generate_session_end_prompt()` function
4. **Never manually create .agor files** - all memory management is automatic

**📍 Snapshot Storage (Automatic)**:
- Snapshots automatically saved to `.agor/agents/{agent_id}/snapshots/` on memory branches
- **Never manually interact with .agor directories** - use dev tools only
- Memory branches (e.g., `agor/mem/main`) handle all coordination files automatically

### Agent Workflow Guidance

**End each response with suggestions like:**
- "Would you like me to create a development snapshot and handoff prompt for this work?"
- "I can generate PR notes using the dev tools if you're ready to create a pull request."
- "Let me know if you'd like me to commit our progress using quick_commit_and_push()."

**Remember**: Use `quick_commit_and_push()` often - it's efficient, saves actions, and keeps your branch synchronized when multiple users/agents are working on the project.

## 🔧 Technical Requirements

### Git Operations

- Use real git commands (not simulated)
- **Use quick_commit_and_push() frequently** for efficient workflow
- Push changes regularly for backup and collaboration
- Pattern: `quick_commit_and_push("Descriptive message", "🔧")` instead of manual git commands

### File Management

- Keep files under 500 lines when creating new projects
- Use modular, testable code structure
- No hard-coded environment variables
- Maintain clean separation of concerns

### Code Quality

- Write comprehensive tests using TDD approach
- Document code with clear comments and docstrings
- Follow security best practices
- Optimize for maintainability and extensibility

## 📚 Documentation Access

### Quick Reference Paths

- **Role Selection**: src/agor/tools/README_ai.md
- **Complete Guide**: src/agor/tools/AGOR_INSTRUCTIONS.md
- **Documentation Index**: src/agor/tools/index.md
- **External Integration**: src/agor/tools/EXTERNAL_INTEGRATION_GUIDE.md (CRITICAL for external projects)
- **Snapshot Guide**: src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md
- **Strategy Guide**: docs/strategies.md
- **Development Guide**: docs/agor-development-guide.md (when working on AGOR itself)

### Platform-Specific Information

- **Bundle Mode**: docs/bundle-mode.md
- **Standalone Mode**: docs/standalone-mode.md
- **Usage Guide**: docs/usage-guide.md
- **Quick Start**: docs/quick-start.md

## ⚠️ Critical Reminders

1. **NEVER end a session without creating a snapshot** - Use `create_development_snapshot()` function
2. **NEVER manually create .agor files** - All memory management is automatic via dev tools
3. **Use quick_commit_and_push() frequently** - Keep work synchronized and prevent loss
4. **Snapshots are automatically saved** - To `.agor/agents/{agent_id}/snapshots/` on memory branches
5. **Always use dev tools functions** - Never manually interact with AGOR memory system
6. **Test your work** - Verify functionality before completion
7. **Follow AGOR protocols precisely** - Read documentation and use programmatic functions

## 🎯 Success Criteria

You are successfully using AGOR when you:

- ✅ Initialize AGOR using programmatic dev tools functions
- ✅ Use quick_commit_and_push() frequently during development
- ✅ Create snapshots using create_development_snapshot() function only
- ✅ Never manually interact with .agor directories or files
- ✅ Use dev tools for all AGOR operations (snapshots, handoffs, PR descriptions)
- ✅ Follow structured development practices with frequent commits
- ✅ Provide comprehensive context through proper dev tools usage

## 🔄 Continuous Improvement

- Use AGOR's feedback tools to provide feedback on AGOR itself
- Suggest improvements to workflows and documentation
- Report issues or exceptional scenarios
- Help evolve AGOR protocols based on real-world usage

---

**Remember**: AGOR transforms AI assistants into sophisticated development coordinators. Your adherence to these protocols ensures effective coordination, context preservation, and successful project outcomes.
