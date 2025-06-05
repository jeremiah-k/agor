# AGOR Augment Code Integration Guide

**For local Augment Code agents working directly in your project**

This guide provides initialization prompts and setup instructions for integrating AGOR with Augment Code's local agent capabilities.

## 🔧 Setup Instructions

### 1. Clone AGOR Repository

```bash
# Clone AGOR to your development environment
git clone https://github.com/jeremiah-k/agor.git ~/agor
```

### 2. Add AGOR as Source in Augment

1. Open Augment Code extension settings
2. Navigate to **Sources** section
3. Click **Add Source**
4. Add path: `~/agor`
5. Enable the source

### 3. Verify Integration

Ensure Augment can access these key files:

- `~/agor/src/agor/tools/README_ai.md`
- `~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md`
- `~/agor/docs/agor-development-guide.md`

## 🚀 Initialization Prompts

### Basic AGOR Initialization

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files to understand the system:
- ~/agor/src/agor/tools/README_ai.md (role selection)
- ~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive guide)

After reading these files, help me initialize AGOR for this project and select the appropriate role (Solo Developer, Project Coordinator, or Agent Worker).

# <--- Add your detailed step-by-step instructions below --->
```

### Solo Developer Focus

```
I'm using AGOR for solo development work on this project.

Please read:
- ~/agor/src/agor/tools/README_ai.md (select Role A: Solo Developer)
- ~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md (focus on Solo Developer sections)

Initialize as Solo Developer and help me analyze the codebase and plan development work.

# <--- Add your detailed step-by-step instructions below --->
```

### Project Coordination Focus

```
I'm using AGOR to coordinate a multi-agent development project.

Please read:
- ~/agor/src/agor/tools/README_ai.md (select Role B: Project Coordinator)
- ~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md (focus on Project Coordinator sections)

Initialize as Project Coordinator and help me plan the development strategy and agent coordination.

# <--- Add your detailed step-by-step instructions below --->
```

### Agent Worker Focus

```
I'm an agent worker ready to receive tasks from a project coordinator.

Please read:
- ~/agor/src/agor/tools/README_ai.md (select Role C: Agent Worker)
- ~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md (focus on Agent Worker sections)

Initialize as Agent Worker and await task assignment or snapshot instructions.

# <--- Add your detailed step-by-step instructions below --->
```

## 🎯 Token-Efficient Chaining

All prompts above end with the chainable instruction comment. This allows you to:

1. **Start with the initialization prompt**
2. **Add specific instructions** after the comment line
3. **Maximize token efficiency** by combining initialization with your specific task
4. **Avoid separate initialization prompts** that consume additional tokens

### Example Chained Usage

```
I'm using AGOR for solo development work on this project.

Please read:
- ~/agor/src/agor/tools/README_ai.md (select Role A: Solo Developer)
- ~/agor/src/agor/tools/AGOR_INSTRUCTIONS.md (focus on Solo Developer sections)

Initialize as Solo Developer and help me analyze the codebase and plan development work.

# <--- Add your detailed step-by-step instructions below --->

1. Analyze the current codebase structure and identify the main components
2. Review the recent git history to understand what changes have been made
3. Help me plan the implementation of a new authentication system
4. Create a development strategy with clear milestones
5. Set up the development environment and testing framework
```

## 🔄 Benefits of Local Integration

- **Direct file access**: No upload limits or file size restrictions
- **Real-time updates**: Access to live documentation and tools
- **Git integration**: Full version control capabilities
- **Token efficiency**: Chainable prompts reduce token consumption
- **Persistent context**: AGOR's memory system works seamlessly
- **Development tools**: Access to AGOR's development utilities

## 📸 Snapshot System Requirements

**🚨 CRITICAL: Before ending any session, you MUST provide a snapshot**

### Essential Reading:

- **Read**: `~/agor/src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- **Understand**: Snapshot system is mandatory for context preservation
- **Prepare**: Know how to create comprehensive snapshots

### End-of-Session Snapshot (REQUIRED):

Every work session must end with a snapshot in a single codeblock containing:

- Problem definition and current status
- Work completed and commits made
- Files modified and next steps
- Technical context and continuation instructions

Use this template:

```markdown
# 📸 Agent Snapshot Document

**Generated**: [timestamp]
**From Agent Role**: [your role]
**Snapshot Reason**: End of session
**AGOR Version**: 0.3.5

## 🎯 Problem Definition

[What you were working on]

## 📊 Current Status

[Progress and completion status]

## ✅ Work Completed

- [List of completed tasks]

## 📝 Commits Made

- `hash: commit message`

## 📁 Files Modified

- `file.py` - [changes made]

## 🔄 Next Steps

1. [Next immediate task]
2. [Follow-up items]

## 🧠 Technical Context

[Key decisions, gotchas, testing status]

## 🎯 Continuation Instructions

[How to continue this work]
```

## 📚 Next Steps

After initialization:

1. **Follow role-specific workflows** from AGOR_INSTRUCTIONS.md
2. **Use AGOR hotkeys** for structured development tasks
3. **Leverage snapshot system** for context management (MANDATORY)
4. **Utilize memory synchronization** for persistent state
5. **Provide feedback** using the `meta` hotkey

## 🤝 Integration Tips

- **Keep AGOR updated**: Regularly `git pull` in the `~/agor` directory
- **Use relative paths**: Reference AGOR files with `~/agor/` prefix
- **Chain prompts**: Always use the chainable format for efficiency
- **Document decisions**: Use AGOR's memory system for important choices
- **Coordinate with team**: Use snapshot system for multi-agent work

---

_This integration method is optimized for local development environments where Augment Code has direct file system access._
