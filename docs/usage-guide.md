# 📖 AGOR Usage Guide - Comprehensive Overview

**Complete guide to understanding and using AgentOrchestrator effectively**

## 🛠️ AGOR Development Tooling - Core Features

**AGOR's primary value is seamless agent-to-agent coordination and development workflow automation.**

### 🔄 Agent Handoff System

**The most important AGOR feature** - enables seamless transitions between agents:

- **Handoff Prompts**: Generate comprehensive context for agent transitions
- **Work Snapshots**: Preserve complete work state across sessions
- **Memory Branches**: Isolated storage for agent coordination and context
- **Automatic Backtick Processing**: Clean formatting for copy-paste workflows

**Key Functions:**
- `create_seamless_handoff()` - Complete agent transition with snapshot + prompt
- `generate_mandatory_session_end_prompt()` - End-of-session coordination
- `generate_handoff_snapshot()` - Comprehensive work snapshots

### 📝 Development Workflow Automation

**Streamline development tasks with automated output generation:**

- **PR Descriptions**: Auto-generate professional pull request descriptions
- **Release Notes**: Create formatted release documentation
- **Meta Feedback**: Provide structured feedback on AGOR itself
- **Commit Automation**: Quick commit/push with timestamps

**Key Functions:**
- `generate_pr_description_only()` - Professional PR descriptions
- `generate_release_notes_only()` - Formatted release notes
- `generate_meta_feedback()` - AGOR improvement feedback
- `quick_commit_push()` - Automated git operations

### 🧠 Memory & Context Management

**Preserve context across sessions and agents:**

- **Cross-Session Context**: Resume work exactly where previous agent left off
- **Multi-Agent Coordination**: Share context between multiple agents
- **Memory Branch Strategy**: Use unified memory branches per feature (not per memory)
  - **Recommended**: One memory branch per feature or session (e.g., `agor/mem/feature-name`)
  - **Avoid**: Creating a new memory branch for every individual memory operation
  - **Benefits**: Cleaner git history, easier navigation, consolidated snapshots
- **Agent Continuity**: Seamless handoffs with complete context preservation

**Key Functions:**
- `auto_commit_memory()` - Save agent state to memory branches
- `commit_to_memory_branch()` - Cross-branch memory operations
- `list_memory_branches()` - View available memory branches

**Memory Branch Best Practices:**
- Use descriptive names: `agor/mem/refactor-dev-tooling` instead of `agor/mem/2025-01-28_1234`
- Consolidate related work in the same memory branch
- Clean up old memory branches when features are complete
- Keep memory branches focused on specific features or sessions

### ⚙️ Environment Setup & Dependencies

**Ensure dev tooling works reliably:**

```bash
# Install ONLY the dependencies needed for agent dev tooling
python3 -m pip install -r src/agor/tools/agent-requirements.txt || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    fi
}

# Test AGOR development tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling, get_timestamp
test_tooling()
print(f'Session started at: {get_timestamp()}')
"
```

**Required Dependencies:**
- `pydantic>=2.0.0` - Data validation for dev tooling
- `pydantic-settings>=2.0.0` - Settings management
- `platformdirs>=3.0.0` - Cross-platform directory handling
- `httpx>=0.24.0` - HTTP requests for version checking and NTP time

## 🚀 Installation & Platform Setup

This section provides detailed setup instructions for initializing AGOR agents on different platforms. Choose the platform that matches your environment.

<details>
<summary><b>Google AI Studio Pro (Free Tier)</b></summary>

### Google AI Studio Pro (Free Tier)

**Setup:**

- Use **Bundled Mode** with `.zip` format
- **Any role works** - choose based on your workflow needs
- Enable Function Calling in your project settings
- Memory synchronization works automatically

**Workflow:**

```bash
agor bundle your-project -f zip
# Upload to Google AI Studio Pro
# Select role based on your needs:
# - SOLO DEVELOPER: For code analysis and implementation
# - PROJECT COORDINATOR: For planning and strategy
# - AGENT WORKER: For following specific instructions
# All roles work with copy-paste workflow
```

</details>

<details>
<summary><b>AugmentCode Local Agent</b></summary>

### AugmentCode Local Agent

**For the flagship AugmentCode Local Agent (VS Code extension) running locally:**

#### Prerequisites:

- VS Code with AugmentCode extension installed
- Git access for cloning repositories
- Basic familiarity with VS Code workspace management

#### Setup Steps:

**Step 1: Clone AGOR Repository**

```bash
git clone https://github.com/jeremiah-k/agor.git ~/agor
```

**Step 2: Add AGOR as Workspace Context**

- Open VS Code with Augment extension installed
- Click the folder icon in the Augment sidebar panel
- Click **+ Add more...** at the bottom of Source Folders
- Select the `~/agor` directory and click **Add Source Folder**

_This gives the agent direct access to all AGOR documentation and tools_

**Step 3: Configure User Guidelines**

- In Augment Chat, click the **Context menu** or use **@-mention**
- Select **User Guidelines**
- Copy and paste the complete User Guidelines (see below)

_This ensures the agent follows AGOR protocols and creates mandatory snapshots_

**Step 4: Agent Initialization Requirements**

**CRITICAL**: The agent must read these files before starting any work:

- `src/agor/tools/README_ai.md` (role selection and initialization)
- `src/agor/tools/AGOR_INSTRUCTIONS.md` (comprehensive operational guide)
- `src/agor/tools/agent-start-here.md` (quick startup guide)
- `src/agor/tools/index.md` (documentation index for efficient lookup)

**Complete User Guidelines for AugmentCode (Copy & Paste):**

```
# AGOR (AgentOrchestrator) User Guidelines for AugmentCode Local Agent

*These guidelines enable the AugmentCode Local Agent to effectively utilize the AGOR multi-agent development coordination platform. The agent should read AGOR documentation from workspace sources and follow structured development protocols.*

## 🎯 Core AGOR Principles

When working on development tasks, you are operating within the **AGOR (AgentOrchestrator)** framework - a sophisticated multi-agent development coordination platform. Your primary responsibilities:

1. **Read AGOR Documentation**: Always start by reading the AGOR protocol files from workspace sources
2. **Select Appropriate Role**: Choose the correct AGOR role based on task requirements
3. **Follow AGOR Protocols**: Use structured workflows, hotkeys, and coordination methods
4. **Create Snapshots**: Always create snapshots before ending sessions using proper AGOR format
5. **Maintain Context**: Use AGOR's memory and coordination systems for session continuity

## 🚀 Initialization Protocol

### Step 1: Read AGOR Documentation

MANDATORY: Read these files from workspace sources before starting any development work:

- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)

### Step 2: Utilize AGOR Tooling

**🔧 Development Tooling**
- **Snapshots**: Create comprehensive work snapshots for agent-to-agent continuity
- **Handoff Prompts**: Generate detailed context for seamless agent transitions
- **PR Descriptions**: Auto-generate professional pull request descriptions
- **Release Notes**: Create formatted release documentation
- **Meta Feedback**: Provide structured feedback on AGOR itself

**🧠 Memory System**
- **Agent Continuity**: Preserve context across sessions and agent switches
- **Memory Branches**: Isolated storage for agent state and coordination
- **Cross-Session Context**: Resume work exactly where previous agent left off
- **Multi-Agent Coordination**: Share context between multiple agents

### Step 3: Essential Dev Tools

**Core Functions (Available in all environments):**
- `snapshot` - Create work snapshot (MANDATORY before ending sessions)
- `meta` - Provide feedback on AGOR itself
- `commit` - Save changes with descriptive messages
- `status` - Check coordination and project status

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
1. **Initialize Coordination**: Use `init` hotkey to set up .agor/ structure
2. **Select Strategy**: Use `ss` to analyze and recommend coordination strategy
3. **Communicate**: Update agentconvo.md with status and findings
4. **Sync Regularly**: Use `sync` hotkey to stay coordinated
5. **Create Snapshots**: For seamless agent transitions

### Available Strategies
- **Parallel Divergent** (`pd`) - Independent exploration → synthesis
- **Pipeline** (`pl`) - Sequential snapshots with specialization
- **Swarm** (`sw`) - Dynamic task assignment from queue
- **Red Team** (`rt`) - Adversarial build/break cycles
- **Mob Programming** (`mb`) - Collaborative coding

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
- ✅ Use AGOR hotkeys and workflows consistently
- ✅ Create proper snapshots with correct dates and locations
- ✅ Maintain coordination files and communication protocols
- ✅ Follow structured development practices
- ✅ Provide comprehensive context for continuation

## 🔄 Continuous Improvement

- Use `meta` hotkey to provide feedback on AGOR itself
- Suggest improvements to workflows and documentation
- Report issues or exceptional scenarios
- Help evolve AGOR protocols based on real-world usage

---

**Remember**: AGOR transforms AI assistants into sophisticated development coordinators. Your adherence to these protocols ensures effective coordination, context preservation, and successful project outcomes.
```

**Step 5: Agent Initialization Prompt**

**Copy and paste this initialization prompt to your agent:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files from the workspace sources to understand the system:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)

After reading these files, help me initialize AGOR for this project and select the appropriate role (Solo Developer, Project Coordinator, or Agent Worker) based on the task requirements.

# <--- Add your detailed step-by-step instructions below --->
```

**Workflow:**

1. Agent reads AGOR protocol from your local Sources
2. Agent selects appropriate role for the task
3. Agent works within your local VS Code environment
4. Full codebase context and completions available
5. Manual git operations (agent provides code, you commit)

</details>

<details>
<summary><b>AugmentCode Remote Agents</b></summary>

### AugmentCode Remote Agents

**For AugmentCode Remote Agents:**

**Setup:**

- Use **Standalone Mode** with direct git access
- **Any role works** - choose based on your workflow needs
- Full multi-agent capabilities available
- Real-time collaboration possible
- Direct commits if agent has commit access, copy-paste fallback otherwise

**User Guidelines (Copy and paste this into your agent prompt):**

```
# AGOR (AgentOrchestrator) User Guidelines for AugmentCode Remote Agents

*These guidelines enable the AugmentCode Remote Agent to effectively utilize the AGOR multi-agent development coordination platform. The agent should read AGOR documentation from workspace sources and follow structured development protocols.*

## 🎯 Core AGOR Principles

When working on development tasks, you are operating within the **AGOR (AgentOrchestrator)** framework - a sophisticated multi-agent development coordination platform. Your primary responsibilities:

1. **Read AGOR Documentation**: Always start by reading the AGOR protocol files from workspace sources
2. **Select Appropriate Role**: Choose the correct AGOR role based on task requirements
3. **Follow AGOR Protocols**: Use structured workflows, hotkeys, and coordination methods
4. **Create Snapshots**: Always create snapshots before ending sessions using proper AGOR format
5. **Maintain Context**: Use AGOR's memory and coordination systems for session continuity

## 🚀 Initialization Protocol

### Step 1: Read AGOR Documentation

MANDATORY: Read these files from workspace sources before starting any development work:

- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)

### Step 2: Role Selection
Choose your AGOR role based on the task:

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

### Step 3: Environment Detection
You are operating in **AugmentCode Remote Agent** environment with:
- Direct git access to repositories
- Full development environment capabilities
- Real-time collaboration possible
- Enhanced memory through cloud infrastructure

## 🛠️ AGOR Workflow Protocols

### Core Development Tools (Use These Frequently)
- `a` - Comprehensive codebase analysis
- `f` - Display complete files with formatting
- `commit` - Save changes with descriptive messages
- `snapshot` - Create work snapshot (MANDATORY before ending sessions)
- `status` - Check coordination and project status
- `meta` - Provide feedback on AGOR itself
- Use dev tooling functions for all coordination outputs

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
1. **Initialize Coordination**: Use `init` hotkey to set up .agor/ structure
2. **Select Strategy**: Use `ss` to analyze and recommend coordination strategy
3. **Communicate**: Update agentconvo.md with status and findings
4. **Sync Regularly**: Use `sync` hotkey to stay coordinated
5. **Create Snapshots**: For seamless agent transitions

### Available Strategies
- **Parallel Divergent** (`pd`) - Independent exploration → synthesis
- **Pipeline** (`pl`) - Sequential snapshots with specialization
- **Swarm** (`sw`) - Dynamic task assignment from queue
- **Red Team** (`rt`) - Adversarial build/break cycles
- **Mob Programming** (`mb`) - Collaborative coding

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
- ✅ Use AGOR hotkeys and workflows consistently
- ✅ Create proper snapshots with correct dates and locations
- ✅ Maintain coordination files and communication protocols
- ✅ Follow structured development practices
- ✅ Provide comprehensive context for continuation

## 🔄 Continuous Improvement

- Use `meta` hotkey to provide feedback on AGOR itself
- Suggest improvements to workflows and documentation
- Report issues or exceptional scenarios
- Help evolve AGOR protocols based on real-world usage

---

**Remember**: AGOR transforms AI assistants into sophisticated development coordinators. Your adherence to these protocols ensures effective coordination, context preservation, and successful project outcomes.
```

**Agent should execute:**

```bash
# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md

# Install ONLY the dependencies needed for agent dev tooling (NOT requirements.txt)
python3 -m pip install -r src/agor/tools/agent-requirements.txt || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
    fi
    # Install dependencies after environment is ready
    python3 -m pip install -r src/agor/tools/agent-requirements.txt
}

# Test AGOR development tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling, get_timestamp

# Verify tooling works
test_tooling()
print(f'Session started at: {get_timestamp()}')
"

# Review agent startup guide
cat src/agor/tools/agent-start-here.md

# Now return to your project's directory with AGOR initialized
```

**Note**: Remote agents should also have the User Guidelines configured in their system for consistent behavior.

</details>

<details>
<summary><b>Jules by Google</b></summary>

### Jules by Google

**For Jules by Google (requires direct URL access to files):**

Use this initialization prompt with Jules:

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files to understand the system:
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/README_ai.md (role selection)
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive guide)
- https://github.com/jeremiah-k/agor/blob/main/src/agor/tools/agent-start-here.md (startup guide)

After reading these files, help me initialize AGOR for this project and select the appropriate role (Solo Developer, Project Coordinator, or Agent Worker).

# <--- Add your detailed step-by-step instructions below --->
```

**Note:** Jules cannot clone repositories that weren't selected during environment creation, so direct URL access to documentation is required.

</details>

<details>
<summary><b>ChatGPT</b></summary>

### ChatGPT

**Setup:**

- Use **Bundled Mode** with `.tar.gz` format
- **Any role works** - choose based on your workflow needs
- Requires subscription for file uploads
- All roles work with copy-paste workflow

**Workflow:**

```bash
agor bundle your-project -f tar.gz
# Upload to ChatGPT
# Select appropriate role based on your needs
```

</details>

<details>
<summary><b>OpenAI Codex (Software Engineering Agent)</b></summary>

### OpenAI Codex (Software Engineering Agent)

**Setup:**

> **🚧 Instructions Coming Soon**
>
> OpenAI Codex is a new software engineering agent that provides terminal access and direct code execution capabilities. AGOR integration instructions will be added once the platform is more widely available.
>
> **Expected Features:**
>
> - Direct terminal access for git operations
> - Code execution capabilities
> - Integration with existing OpenAI ecosystem
>
> **Likely Mode:** Standalone Mode with enhanced capabilities

</details>

## 🎯 Understanding AGOR's Dual Nature

### From AgentGrunt to AgentOrchestrator

AGOR is a fork of the innovative [AgentGrunt](https://github.com/nikvdp/agentgrunt) project by [@nikvdp](https://github.com/nikvdp). **AGOR retains all of AgentGrunt's capabilities** while adding multi-agent coordination.

**Key Changes from AgentGrunt:**

- **Retained**: All original standalone capabilities and git integration
- **Replaced**: Patch downloads with full file output in codeblocks (preserving comments, formatting, etc.)
- **Added**: Multi-agent coordination, strategic planning, and platform flexibility

## 🔄 Two Operational Modes Explained

### 🚀 Standalone Mode (Direct Git Access)

**When to Use:**

- You have an AI agent with direct repository access
- You want agents to make commits directly (if they have commit access)
- You're using platforms like Augment Code Remote Agents or Jules by Google
- You need real-time collaboration between multiple agents

**How It Works:**

1. Agent clones AGOR repository to learn the protocol
2. Agent clones your target project repository
3. Agent can make direct commits if they have commit access, or use copy-paste codeblocks as fallback
4. Multiple agents can work on the same repository simultaneously
5. Full git history and branch management available

**Example Workflow:**

```bash
# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to your project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md

# Install ONLY the dependencies needed for agent dev tooling (NOT requirements.txt)
python3 -m pip install -r src/agor/tools/agent-requirements.txt || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
    fi
    # Install dependencies after environment is ready
    python3 -m pip install -r src/agor/tools/agent-requirements.txt
}

# Test AGOR development tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling, get_timestamp

# Verify tooling works
test_tooling()
print(f'Session started at: {get_timestamp()}')
"

# Review development guide
cat docs/agor-development-guide.md
cat src/agor/tools/agent-start-here.md

# Now return to your project's directory with AGOR initialized
```

### 📦 Bundled Mode (Upload-Based Platforms)

**When to Use:**

- You're using upload-based AI platforms (Google AI Studio, ChatGPT, Claude)
- You want to work with free tiers (especially Google AI Studio Pro)
- You prefer manual control over git operations
- You're working with file size limitations

**How It Works:**

1. You bundle your project using AGOR CLI
2. Upload the bundle to your AI platform
3. Agent analyzes and works within the bundled environment. This bundle uniquely includes the **entirety of your codebase and its full Git history (all branches by default)**, giving the AI deep contextual understanding for more accurate analysis and effective editing, a capability not always present in other tools.
4. Agent provides edited files in code blocks
5. You manually copy-paste changes and commit them yourself

**Example Workflow:**

```bash
# You run these commands locally
pipx install agor
agor bundle https://github.com/your-username/your-project
# Upload the generated bundle to your AI platform
# Agent works within bundle, you handle git operations
```

## 🎭 Role Selection Deep Dive

### 🔍 SOLO DEVELOPER

**Primary Purpose:** Deep codebase analysis and implementation

**Best For:**

- Analyzing existing codebases
- Implementing specific features
- Debugging and troubleshooting
- Solo development work
- Technical deep-dives
- Managing complex tasks by breaking them down with structured context.
- Preserving detailed progress and context across multiple work sessions, especially when dealing with AI context window limitations.
- Creating 'self-snapshots' to seamlessly resume work or switch between different AI models/assistants while maintaining full context.

**Works in Both Modes:**

- **Standalone Mode**: Direct commits (if access available) or copy-paste fallback
- **Bundled Mode**: Copy-paste codeblocks with full formatting preservation
- **Independent operation** - no coordination overhead required
- **Can be incorporated** into multi-agent teams when specialized analysis is needed

**Key Capabilities:**

- Comprehensive codebase analysis (`a`)
- Code exploration and investigation (`f`, `co`)
- Implementation and development work
- Technical documentation and explanation

**Typical Workflow:**

1. Perform comprehensive analysis (`a`)
2. Explore specific code areas (`f`, `co`)
3. Implement changes or provide detailed explanations
4. Document findings and decisions

**Why Use AGOR as a Solo Developer?**

While "Orchestrator" might suggest a multi-agent focus, AGOR provides significant benefits even for solo developers:

- **Structured Work Management**: AGOR's protocols encourage a methodical approach to tasks. Even if you're the only "agent," thinking in terms of analysis, implementation, and (self-)snapshots can bring clarity to complex projects.
- **Context Preservation**: AI assistants often have context window limits. Using AGOR's `snapshot` hotkey (even if you're creating a snapshot for yourself for a later session or a different AI model) allows you to create a comprehensive snapshot of your current work, including code changes, analysis, and next steps. This means you can pick up exactly where you left off without losing valuable context.
- **Tool Integration**: AGOR provides a consistent interface for interacting with your codebase, including integrated Git commands and analysis tools, all within the AI's workflow.
- **Future Scalability**: If your solo project grows to involve more collaborators (human or AI), you'll already have a structured process in place.

### 📋 PROJECT COORDINATOR

**Primary Purpose:** Strategic planning and team orchestration

**Best For:**

- Planning new features or projects
- Designing multi-agent workflows
- Breaking down complex requirements
- Coordinating team activities

**Works in Both Modes:**

- **Standalone Mode**: Direct commits (if access available) or copy-paste fallback
- **Bundled Mode**: Copy-paste codeblocks with strategic plans and coordination files
- **Multi-agent coordination** capabilities available in both modes

**Key Capabilities:**

- Initialize coordination strategies (`pd`, `pl`, `sw`, `rt`, `mb`)
- Create specialized agent teams (`ct`)
- Design snapshot procedures (`hp` - snapshot prompts)
- Monitor team progress and coordination

**Typical Workflow:**

1. Analyze project requirements (`sp`)
2. Select optimal strategy (`ss`)
3. Create specialized team (`ct`)
4. Initialize strategy and coordinate agents

### 🤖 AGENT WORKER

**Primary Purpose:** Task execution and processing work snapshots

**Best For:**

- Receiving specific tasks from coordinators (often as snapshots)
- Executing specialized development work based on snapshots
- Following established workflows
- Team coordination and communication

**Works in Both Modes:**

- **Standalone Mode**: Direct commits (if access available) or copy-paste fallback
- **Bundled Mode**: Copy-paste codeblocks with completed tasks
- **Team coordination** capabilities available in both modes

**Key Capabilities:**

- Excels at receiving and executing work based on snapshots
- Maintains coordination with other agents
- Reports progress and status

**Typical Workflow:**

1. Check coordination status (`status`)
2. Receive task assignment (`task` - often a snapshot)
3. Execute assigned work
4. Report completion and create a new snapshot (`complete`, `snapshot`)

## 🛠️ AGOR Development Tooling

### Core Development Functions

AGOR provides powerful development tooling that agents use for coordination, memory management, and output generation. All outputs are automatically formatted for copy-paste with stripped backticks.

**📝 Snapshot Generation**
- `generate_handoff_snapshot()` - Create comprehensive work snapshots
- `generate_mandatory_session_end_prompt()` - End-of-session summaries
- All snapshots automatically saved to memory branches

**🔄 Memory Management**
- `auto_commit_memory()` - Save agent state to memory branches
- `read_from_memory_branch()` - Access previous work context
- `list_memory_branches()` - View available memory branches

**📋 Output Generation**
- `generate_meta_feedback()` - Provide feedback on AGOR itself
- `detick_content()` - Strip triple backticks for copy-paste
- All outputs formatted in single codeblocks

**⚙️ Git Operations**
- `quick_commit_push()` - Fast commit and push operations
- `run_git_command()` - Safe git command execution
- Branch-safe operations that never leave users on memory branches

### Experimental Multi-Agent Strategies

**Note**: These are experimental features being refined based on real-world usage. The core dev tooling and agent handoffs above are the proven, production-ready features.

- **Parallel Divergent** - Independent exploration then synthesis
- **Pipeline** - Sequential snapshots with specialization
- **Swarm** - Dynamic task assignment from queue
- **Red Team** - Adversarial build/break cycles
- **Mob Programming** - Collaborative coding

**Feedback Encouraged**: Use the `meta` hotkey to provide feedback on coordination experiences.

## 🚀 Getting Started Recommendations

### For Beginners

1. **Start with Bundled Mode** using Google AI Studio Pro (free)
2. **Choose any role** based on what you want to do:
   - **SOLO DEVELOPER**: For code analysis and implementation
   - **PROJECT COORDINATOR**: For planning and strategy
   - **AGENT WORKER**: For following specific instructions
3. **Use basic hotkeys**: `a` (analyze), `f` (full files), `status`
4. **Practice with small projects** before attempting multi-agent workflows

### For Advanced Users

1. **Try Standalone Mode** with git-capable agents
2. **Experiment with different roles** based on your needs
3. **Initialize multi-agent strategies** (`ss`, `pd`, `pl`)
4. **Use advanced features**: Memory synchronization, custom strategies

### For Teams

1. **Use Standalone Mode** for real-time collaboration
2. **Designate one PROJECT COORDINATOR** for planning
3. **Assign specialized AGENT WORKER** roles
4. **Implement structured snapshot procedures**

## 🔍 Troubleshooting Common Issues

### "Agent doesn't understand the protocol"

**Solution:** Ensure the agent has loaded both instruction files:

```bash
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md
```

### "Multi-agent coordination isn't working"

**Solution:**

1. Check `.agor/` directory exists and has proper files
2. Ensure all agents are using `sync` hotkey regularly
3. Verify agents are communicating via `agentconvo.md`

### "Bundle upload fails"

**Solution:**

1. Try different format (`-f zip` vs `-f tar.gz`)
2. Check file size limits on your platform
3. Use `--branch main` to reduce bundle size

### "Git operations fail in bundled mode"

**Expected:** Bundled mode requires manual git operations. Agent provides code, you handle commits.

## 📚 Additional Resources

- **[Documentation Index](../src/agor/tools/index.md)** - Quick reference for all documentation
- **[Bundle Mode Guide](bundle-mode.md)** - Platform-specific setup instructions
- **[Strategy Guide](strategies.md)** - Detailed multi-agent strategy explanations
- **[Quick Start](quick-start.md)** - Step-by-step getting started guide

---

_This guide evolves with AGOR. Suggest improvements through GitHub issues or the `meta` hotkey._
