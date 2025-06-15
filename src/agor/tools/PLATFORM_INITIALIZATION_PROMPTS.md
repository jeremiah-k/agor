# 🚀 Platform-Specific AGOR Initialization Prompts

**For users to copy and paste when initializing AGOR on different AI platforms**

These prompts are designed to be used at the beginning of a session, followed by a snapshot if continuing work.

---

## 📦 Google AI Studio Pro

**Copy this prompt when uploading your AGOR bundle to Google AI Studio:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

You have access to my project bundle which includes:
- Complete project codebase with git history
- AGOR coordination tools and protocols
- Comprehensive AI instructions

Please start by reading these key files to understand the system:
1. Read src/agor/tools/README_ai.md for role selection and initialization
2. Read src/agor/tools/AGOR_INSTRUCTIONS.md for comprehensive instructions
3. Read src/agor/tools/index.md for quick reference lookup

After reading these files, help me select the appropriate role:
- Worker Agent: For code analysis, implementation, and technical work
- Project Coordinator: For planning and multi-agent coordination

Environment: Google AI Studio Pro with Function Calling enabled
Bundle Format: .zip
Mode: Bundle Mode (copy-paste workflow)

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 💬 ChatGPT (Classic Interface)

**Copy this prompt when uploading your AGOR bundle to ChatGPT:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

You have access to my project bundle which includes:
- Complete project codebase with git history
- AGOR coordination tools and protocols
- Comprehensive AI instructions

Please start by reading these key files to understand the system:
1. Read src/agor/tools/README_ai.md for role selection and initialization
2. Read src/agor/tools/AGOR_INSTRUCTIONS.md for comprehensive instructions
3. Read src/agor/tools/index.md for quick reference lookup

After reading these files, help me select the appropriate role:
- Worker Agent: For code analysis, implementation, and technical work
- Project Coordinator: For planning and multi-agent coordination

Environment: ChatGPT (classic interface, not Codex)
Bundle Format: .tar.gz
Mode: Bundle Mode (copy-paste workflow)

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 🤖 AugmentCode Local Agent

**When using the AugmentCode Local Agent (VS Code extension), use this approach:**

### Setup (One-time)

1. Clone AGOR repository locally: `git clone https://github.com/jeremiah-k/agor.git [your-preferred-directory]`
2. Add the AGOR directory to your AugmentCode workspace sources
3. Add this to your User Guidelines:

```
When working on development projects, utilize the AGOR (AgentOrchestrator) framework for structured development coordination. Read the AGOR documentation from the workspace sources to understand role selection (Worker Agent or Project Coordinator) and follow the appropriate workflows and development tools for efficient development.
```

### Session Initialization Prompt

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

AGOR is available in your workspace sources. Please:
1. Read src/agor/tools/README_ai.md for role selection and initialization
2. Read src/agor/tools/AGOR_INSTRUCTIONS.md for comprehensive instructions
3. Check my User Guidelines for any project-specific AGOR preferences

After reading these files, help me select the appropriate role:
- Worker Agent: For code analysis, implementation, and technical work
- Project Coordinator: For planning and multi-agent coordination

Environment: AugmentCode Local Agent (VS Code extension)
Mode: Local Integration (direct file access, persistent guidelines)
Benefits: No upload limits, persistent User Guidelines, Augment Memories

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 🔗 AugmentCode Remote Agents

**For AugmentCode Remote Agents with git access, use this initialization:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please execute these commands to initialize AGOR:

# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md

# Install dependencies and test development tools
pip install -r requirements.txt

# Install additional dependencies for memory manager types
pip install pydantic pydantic-settings || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    fi
}

# Test AGOR development tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import test_tooling, get_timestamp

# Verify tooling works
test_tooling()
print(f'Session started at: {get_timestamp()}')
"

# Review agent startup guide
cat src/agor/tools/agent-start-here.md

After initialization, help me select the appropriate role:
- Worker Agent: For code analysis, implementation, and technical work
- Project Coordinator: For planning and multi-agent coordination

Environment: AugmentCode Remote Agent
Mode: Standalone Mode (direct git access)
Benefits: Direct commits, real-time collaboration, no file size limits

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 🌐 Jules by Google

**For Jules by Google (requires direct URL access), use this initialization:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files to understand the system:
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/README_ai.md (role selection)
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive guide)
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/agent-start-here.md (startup guide)

After reading these files, help me select the appropriate role:
- Worker Agent: For code analysis, implementation, and technical work
- Project Coordinator: For planning and multi-agent coordination

Environment: Jules by Google
Mode: Standalone Mode (direct URL access to files)
Limitations: Cannot clone repositories not selected during environment creation

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 🚧 OpenAI Codex (Coming Soon)

**Placeholder for OpenAI Codex integration:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

OpenAI Codex integration instructions are coming soon. This new software engineering agent provides:
- Direct terminal access for git operations
- Code execution capabilities
- Integration with existing OpenAI ecosystem

Expected Mode: Standalone Mode with enhanced capabilities

For now, please refer to the AugmentCode Remote Agents initialization above as a similar approach.

# <--- Add your specific project instructions and any snapshot below --->
```

---

## 📋 Usage Instructions

1. **Choose your platform** from the options above
2. **Copy the appropriate prompt** for your AI platform
3. **Add your specific project context** in the designated section
4. **Include any snapshot** if continuing previous work
5. **Paste the complete prompt** to initialize AGOR

### Snapshot Integration

If you have a snapshot from previous work, add it after the initialization prompt:

```
# Previous Work Snapshot:
[Paste your snapshot document here]
```

This ensures the agent has both AGOR initialization and your work context in a single prompt.
