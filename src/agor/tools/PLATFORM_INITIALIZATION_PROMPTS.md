# 🚀 Platform-Specific AGOR Initialization Prompts

**For users to copy and paste when initializing AGOR on different AI platforms**

These prompts are designed to be used at the beginning of a session, followed by a snapshot if continuing work.

---

## 📦 Google AI Studio Pro

**Copy this prompt when uploading your AGOR bundle to Google AI Studio:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

You will start in the Worker Agent role, but don't focus on that heavily at the moment.

You have access to my project bundle which includes:
- Complete project codebase with git history
- AGOR coordination tools and protocols
- Comprehensive AI instructions

Please extract the bundle and execute these functions in order to initialize the AGOR system:

# Initialize and display comprehensive setup guide
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import get_agor_initialization_guide, get_available_functions_reference, display_memory_architecture_info, test_all_tools

print('🚀 AGOR INITIALIZATION')
print('=' * 50)
print(get_agor_initialization_guide())

print('\n📋 AVAILABLE FUNCTIONS REFERENCE')
print('=' * 50)
print(get_available_functions_reference())

print('\n🧠 MEMORY ARCHITECTURE')
print('=' * 50)
display_memory_architecture_info()

print('\n🧪 TESTING TOOLS')
print('=' * 50)
test_all_tools()
print('✅ AGOR initialization complete!')
"

Examine the available dev tools, use these whenever possible for a more seamless workflow across agents.

If the above functions don't work properly, use our fallback method of reading these files:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive instructions)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)
- src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md (snapshot requirements and templates, must understand this system in full)
- src/agor/tools/meta-feedback-workflows.md (meta-feedback system for AGOR improvements)

Environment: Google AI Studio Pro with Function Calling enabled
Bundle Format: .zip
Mode: Bundle Mode (copy-paste workflow)

# <--- Add your specific project instructions and any snapshot below --->

As you get close to the end of your work, finish every set of actions by generating a detailed snapshot of the work that you have completed, with any important context included, so that the next agent can seamlessly pick up where you left off if necessary.

When asked, be prepared to create a PR summary, release notes, and or a handoff prompt using the dev tools, wrapping the output of each in a single codeblock (for easy copying & pasting).

When generating a handoff prompt, include full initialization instructions and how to use the dev tools to read the snapshot with the rest of the context, if applicable.
```

---

## 💬 ChatGPT (Classic Interface)

**Copy this prompt when uploading your AGOR bundle to ChatGPT:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

You will start in the Worker Agent role, but don't focus on that heavily at the moment.

You have access to my project bundle which includes:
- Complete project codebase with git history
- AGOR coordination tools and protocols
- Comprehensive AI instructions

Please extract the bundle and execute these functions in order to initialize the AGOR system:

# Initialize and display comprehensive setup guide
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import get_agor_initialization_guide, get_available_functions_reference, display_memory_architecture_info, test_all_tools

print('🚀 AGOR INITIALIZATION')
print('=' * 50)
print(get_agor_initialization_guide())

print('\n📋 AVAILABLE FUNCTIONS REFERENCE')
print('=' * 50)
print(get_available_functions_reference())

print('\n🧠 MEMORY ARCHITECTURE')
print('=' * 50)
display_memory_architecture_info()

print('\n🧪 TESTING TOOLS')
print('=' * 50)
test_all_tools()
print('✅ AGOR initialization complete!')
"

Examine the available dev tools, use these whenever possible for a more seamless workflow across agents.

If the above functions don't work properly, use our fallback method of reading these files:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive instructions)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)
- src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md (snapshot requirements and templates, must understand this system in full)
- src/agor/tools/meta-feedback-workflows.md (meta-feedback system for AGOR improvements)

Environment: ChatGPT (classic interface, not Codex)
Bundle Format: .tar.gz
Mode: Bundle Mode (copy-paste workflow)

# <--- Add your specific project instructions and any snapshot below --->

As you get close to the end of your work, finish every set of actions by generating a detailed snapshot of the work that you have completed, with any important context included, so that the next agent can seamlessly pick up where you left off if necessary.

When asked, be prepared to create a PR summary, release notes, and or a handoff prompt using the dev tools, wrapping the output of each in a single codeblock (for easy copying & pasting).

When generating a handoff prompt, include full initialization instructions and how to use the dev tools to read the snapshot with the rest of the context, if applicable.
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

You will start in the Worker Agent role, but don't focus on that heavily at the moment.

AGOR is available in your workspace sources. Please:

1. Create a venv in .venv and install the AGOR agent requirements:
python3 -m venv .venv && source .venv/bin/activate
pip install -r {agor_path}/src/agor/tools/agent-requirements.txt

The agor repo should be available to you somewhere in your workspace sources.

2. Execute these functions in order to initialize the AGOR system:

# Initialize and display comprehensive setup guide
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import get_agor_initialization_guide, get_available_functions_reference, display_memory_architecture_info, test_all_tools

print('🚀 AGOR INITIALIZATION')
print('=' * 50)
print(get_agor_initialization_guide())

print('\n📋 AVAILABLE FUNCTIONS REFERENCE')
print('=' * 50)
print(get_available_functions_reference())

print('\n🧠 MEMORY ARCHITECTURE')
print('=' * 50)
display_memory_architecture_info()

print('\n🧪 TESTING TOOLS')
print('=' * 50)
test_all_tools()
print('✅ AGOR initialization complete!')
"

3. Examine the available dev tools, use these whenever possible for a more seamless workflow across agents.

4. Check my User Guidelines for any project-specific AGOR preferences

If the above functions don't work properly, use our fallback method of reading these files:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive instructions)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)
- src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md (snapshot requirements and templates, must understand this system in full)
- src/agor/tools/meta-feedback-workflows.md (meta-feedback system for AGOR improvements)

Environment: AugmentCode Local Agent (VS Code extension)
Mode: Local Integration (direct file access, persistent guidelines)
Benefits: No upload limits, persistent User Guidelines, Augment Memories

# <--- Add your specific project instructions and any snapshot below --->

As you get close to the end of your work, finish every set of actions by generating a detailed snapshot of the work that you have completed, with any important context included, so that the next agent can seamlessly pick up where you left off if necessary.

When asked, be prepared to create a PR summary, release notes, and or a handoff prompt using the dev tools, wrapping the output of each in a single codeblock (for easy copying & pasting).

When generating a handoff prompt, include full initialization instructions and how to use the dev tools to read the snapshot with the rest of the context, if applicable.
```

---

## 🔗 AugmentCode Remote Agents

**For AugmentCode Remote Agents with git access, use this initialization:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

You will start in the Worker Agent role, but don't focus on that heavily at the moment.

Please execute these commands to initialize AGOR:

# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Install AGOR agent development dependencies
python3 -m pip install -r src/agor/tools/agent-requirements.txt

# Execute these functions in order to initialize the AGOR framework
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import get_agor_initialization_guide, get_available_functions_reference, display_memory_architecture_info, test_all_tools

print('🚀 AGOR INITIALIZATION')
print('=' * 50)
print(get_agor_initialization_guide())

print('\n📋 AVAILABLE FUNCTIONS REFERENCE')
print('=' * 50)
print(get_available_functions_reference())

print('\n🧠 MEMORY ARCHITECTURE')
print('=' * 50)
display_memory_architecture_info()

print('\n🧪 TESTING TOOLS')
print('=' * 50)
test_all_tools()
print('✅ AGOR initialization complete!')
"

# If the above functions don't work properly, use our fallback method:
# cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md && cat src/agor/tools/agent-start-here.md

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

You will start in the Worker Agent role, but don't focus on that heavily at the moment.

First, install the AGOR agent requirements:
pip install -r https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/agent-requirements.txt

Since you cannot clone repositories, please read these key files directly to understand the AGOR system:

# Core initialization files (read these in order)
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/README_ai.md
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/AGOR_INSTRUCTIONS.md
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/agent-start-here.md
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/index.md
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md
curl -s https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/meta-feedback-workflows.md

# Alternative: Use wget if curl is not available
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/README_ai.md
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/AGOR_INSTRUCTIONS.md
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/agent-start-here.md
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/index.md
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md
wget -qO- https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/tools/meta-feedback-workflows.md

Environment: Jules by Google
Mode: Standalone Mode (direct URL access to files)
Limitations: Cannot clone repositories not selected during environment creation

# <--- Add your specific project instructions and any snapshot below --->

As you get close to the end of your work, finish every set of actions by generating a detailed snapshot of the work that you have completed, with any important context included, so that the next agent can seamlessly pick up where you left off if necessary.

When asked, be prepared to create a PR summary, release notes, and or a handoff prompt using available tools, wrapping the output of each in a single codeblock (for easy copying & pasting).

When generating a handoff prompt, include full initialization instructions and how to access the documentation with the rest of the context, if applicable.
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
