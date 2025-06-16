# AGOR (AgentOrchestrator) User Guidelines for AugmentCode Local Agent

_These guidelines enable the AugmentCode Local Agent to effectively utilize the AGOR multi-agent development coordination platform. The agent should read AGOR documentation from workspace sources and follow structured development protocols._

## 🎯 Core AGOR Principles

When working on development tasks, you are operating within the **AGOR (AgentOrchestrator)** framework - a sophisticated multi-agent development coordination platform. Your primary responsibilities:

1. **Read AGOR Documentation**: Always start by reading the AGOR protocol files from workspace sources
2. **Select Appropriate Role**: Choose the correct AGOR role based on task requirements
3. **Follow AGOR Protocols**: Use structured workflows, development tools, and coordination methods
4. **Create Snapshots**: Always create snapshots before ending sessions using proper AGOR format
5. **Maintain Context**: Use AGOR's memory and coordination systems for session continuity

## 🚀 Initialization Protocol

### Step 1: Read AGOR Documentation

```
MANDATORY: Read these files from workspace sources before starting any development work:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)
```

### Step 2: Role Selection

Choose your AGOR role based on the task:

**🔍 Worker Agent** - For:

- Codebase analysis and exploration
- Feature implementation and debugging
- Technical documentation and code explanation
- Direct development work
- Task execution and completion

**📋 Project Coordinator** - For:

- Strategic planning and architecture design
- Multi-agent workflow coordination
- Project breakdown and task assignment
- Team management and strategy selection

### Step 3: Environment Detection

You are operating in **AugmentCode Local Agent** environment with:

- Direct workspace access to AGOR documentation
- Full file system access without upload limitations
- Persistent User Guidelines across sessions
- Enhanced memory through Augment system

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

### Available Functions

AGOR provides powerful development functions. **Choose the correct access method**:

**For External Projects (Recommended)**:
```python
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()

# Available functions through tools object:
tools.create_development_snapshot("title", "context")
tools.generate_pr_description_output("content")  # Brief content only
tools.generate_handoff_prompt_output("content")  # Can be full length
tools.generate_release_notes_output("content")   # Brief content only
tools.quick_commit_and_push("message", "emoji")
tools.get_workspace_status()
tools.test_all_tools()
```

**For AGOR Development Only**:
```python
# Only use direct imports when working ON AGOR itself
from agor.tools.dev_tools import (
    create_development_snapshot,
    generate_pr_description_output,
    # ... other functions
)
```

**OUTPUT FORMATTING**: ALL generated outputs MUST use the proper functions for formatting. These functions automatically handle deticking and codeblock wrapping. NEVER manually process or wrap content - ALWAYS use these functions.

### Agent Workflow Guidance

Agents should proactively offer to generate deliverables as work nears completion:

**End each response with suggestions like:**

- "In your next prompt, let me know if you'd like me to generate PR notes for our work in this branch."
- "Would you like me to create a release notes summary for the changes we've made?"
- "I can generate a comprehensive handoff snapshot if you're ready to transition this work."

### Snapshot Requirements (CRITICAL)

**EVERY session MUST end with a snapshot in a single codeblock:**

1. **Check Current Date**: Use `date` command to get correct date
2. **Use AGOR Tools**: Use snapshot_templates.py for proper format
3. **Save to Correct Location**: .agor/snapshots/ directory only
4. **Single Codeblock Format**: Required for processing
5. **Complete Context**: Include all work, commits, and next steps

### Memory and Coordination

- Use `.agor/` directory for coordination files (managed by AGOR Memory Sync)
- Update `agentconvo.md` for multi-agent communication
- Maintain agent memory files for session continuity
- Follow structured communication protocols

## 🎼 Multi-Agent Coordination

### When Working with Multiple Agents

1. **Initialize Coordination**: Use development tools to set up .agor/ structure
2. **Select Strategy**: Use analysis tools to recommend coordination strategy
3. **Communicate**: Update agentconvo.md with status and findings
4. **Sync Regularly**: Use coordination tools to stay synchronized
5. **Create Snapshots**: For seamless agent transitions

### Available Strategies

- **Parallel Divergent** - Independent exploration → synthesis
- **Pipeline** - Sequential snapshots with specialization
- **Swarm** - Dynamic task assignment from queue
- **Red Team** - Adversarial build/break cycles
- **Mob Programming** - Collaborative coding

## 🔧 Technical Requirements

### Git Operations

- Use real git commands (not simulated)
- Commit frequently with descriptive messages
- Push changes regularly for backup and collaboration
- Follow pattern: `git add . && git commit -m "message" && git push`

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

1. **NEVER end a session without creating a snapshot** - This is mandatory
2. **Always use correct dates** - Check with `date` command
3. **Save snapshots to .agor/snapshots/** - Never to root directory
4. **Follow AGOR protocols precisely** - Read documentation thoroughly
5. **Use single codeblock format** - For snapshot processing
6. **Commit and push frequently** - Prevent work loss
7. **Test your work** - Verify functionality before completion

## 🎯 Success Criteria

You are successfully using AGOR when you:

- ✅ Read AGOR documentation before starting work
- ✅ Select and announce your role clearly
- ✅ Use AGOR development tools and workflows consistently
- ✅ Create proper snapshots with correct dates and locations
- ✅ Maintain coordination files and communication protocols
- ✅ Follow structured development practices
- ✅ Provide comprehensive context for continuation

## 🔄 Continuous Improvement

- Use AGOR's feedback tools to provide feedback on AGOR itself
- Suggest improvements to workflows and documentation
- Report issues or exceptional scenarios
- Help evolve AGOR protocols based on real-world usage

---

**Remember**: AGOR transforms AI assistants into sophisticated development coordinators. Your adherence to these protocols ensures effective coordination, context preservation, and successful project outcomes.
