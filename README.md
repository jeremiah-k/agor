# 🎼 AgentOrchestrator (AGOR)

**Multi-Agent Development Coordination Platform**

Transform AI assistants into sophisticated development coordinators. Plan complex projects, design specialized agent teams, and orchestrate coordinated development workflows.

**Supports**: Linux, macOS, Windows | **Free Option**: Google AI Studio Pro | **Subscription**: ChatGPT

> **🔬 Alpha Protocol**: AGOR coordination strategies are actively evolving based on real-world usage. [Contribute feedback](https://github.com/jeremiah-k/agor/issues) to help shape AI coordination patterns.

## 🚀 Quick Start

<details>
<summary><b>Bundle Mode - Google AI Studio, ChatGPT (without Codex)</b></summary>

**For Google AI Studio, ChatGPT (classic interface), and other upload-based platforms:**

```bash
# Install AGOR locally
pipx install agor

# Bundle your project
agor bundle https://github.com/your-username/your-repo
agor bundle /path/to/local/project

# Upload bundle to your AI platform and follow embedded instructions
```

**Bundle Options**: Use `-f zip` for Google AI Studio, `--branch` for specific branches

> **First time?** AGOR will guide you through an interactive setup menu to configure your preferred platform and options.

</details>

<details>
<summary><b>AugmentCode Integration (Local & Remote Agents)</b></summary>

<details>
<summary><b>📋 User Guidelines for AugmentCode (Copy & Paste)</b></summary>

**Copy this complete guideline into your AugmentCode User Guidelines:**

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
You are operating in **AugmentCode Local Agent** environment with:
- Direct workspace access to AGOR documentation
- Full file system access without upload limitations
- Persistent User Guidelines across sessions
- Enhanced memory through Augment system

## 🛠️ AGOR Workflow Protocols

### Core Hotkeys (Use These Frequently)
- `a` - Comprehensive codebase analysis
- `f` - Display complete files with formatting
- `edit` - Modify files with targeted changes
- `commit` - Save changes with descriptive messages
- `snapshot` - Create work snapshot (MANDATORY before ending sessions)
- `status` - Check coordination and project status
- `sp` - Strategic planning (for coordinators)
- `bp` - Break down project into tasks

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

</details>

<details>
<summary><b>🏠 AugmentCode Local Agent Setup</b></summary>

**For the AugmentCode Local Agent (VS Code extension) with local workspace integration:**

#### Prerequisites:
- VS Code with AugmentCode extension installed
- Git access for cloning repositories
- Basic familiarity with VS Code workspace management

#### Step 1: Clone AGOR Repository

```bash
# Clone AGOR to your development environment
git clone https://github.com/jeremiah-k/agor.git ~/agor
```

#### Step 2: Add AGOR as Workspace Context

1. Open VS Code with Augment extension installed
2. Click the folder icon in the Augment sidebar panel
3. Click **+ Add more...** at the bottom of Source Folders
4. Select the `~/agor` directory and click **Add Source Folder**

*This gives the agent direct access to all AGOR documentation and tools*

#### Step 3: Configure User Guidelines

1. In Augment Chat, click the **Context menu** or use **@-mention**
2. Select **User Guidelines**
3. Copy and paste the complete User Guidelines from the dropdown section above

*This ensures the agent follows AGOR protocols and creates mandatory snapshots*

#### Step 4: Agent Initialization Requirements

**CRITICAL**: The agent must read these files before starting any work:
- `src/agor/tools/README_ai.md` (role selection and initialization)
- `src/agor/tools/AGOR_INSTRUCTIONS.md` (comprehensive operational guide)
- `src/agor/tools/agent-start-here.md` (quick startup guide)
- `src/agor/tools/index.md` (documentation index for efficient lookup)

#### Step 5: Optional - Add Workspace Guidelines

Create `.augment-guidelines` file in your project root:

```
- Use AGOR framework for development coordination when available in workspace sources
- Follow AGOR role-based workflows for structured development
- Utilize AGOR hotkeys and snapshot system for context management
- Reference AGOR documentation for best practices and coordination protocols
```

**Benefits:**

- Direct access to AGOR tools and documentation through workspace context
- Persistent guidelines ensure consistent AGOR usage across sessions
- No file upload limits or token efficiency concerns
- Seamless integration with existing VS Code workflow
- Mandatory snapshot system prevents context loss

</details>

<details>
<summary><b>☁️ AugmentCode Remote Agent Setup</b></summary>

**For Augment Code Remote Agents with git access - Agent should execute:**

```bash
# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to your project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md

# Install dependencies and test development tooling
pip install -r requirements.txt

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

</details>

<details>
<summary><b>Jules by Google</b></summary>

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
<summary><b>OpenAI Codex (Software Engineering Agent)</b></summary>

**For OpenAI Codex - the new software engineering agent:**

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

AGOR facilitates AI-driven development through a distinct set of interactions. While the name "Orchestrator" suggests a multi-agent focus, AGOR's robust protocols for structured work, context management (especially via its snapshot capabilities), and tool integration are highly valuable even for **solo developers**. These interactions include: commands for developers using the AGOR CLI (e.g., `agor bundle`), conversational hotkeys for AI-user collaboration (e.g., `sp`, `edit`), and internal tools (like a bundled `git`) used directly by the AI agent. Understanding these layers is key to leveraging AGOR effectively, whether working alone or in a team. For more details on this architecture and comprehensive usage, please refer to our **[Complete Usage Guide](docs/usage-guide.md)**.

## 📚 Documentation

### For Users

**[📖 Complete Usage Guide](docs/usage-guide.md)** - Comprehensive overview of modes, roles, and workflows
**[🚀 Quick Start Guide](docs/quick-start.md)** - Step-by-step getting started instructions
**[📦 Bundle Mode Guide](docs/bundle-mode.md)** - Complete platform setup (Google AI Studio, ChatGPT)
**[🔄 Multi-Agent Strategies](docs/strategies.md)** - Coordination strategies and when to use them
**[📸 Snapshot System](docs/snapshots.md)** - Context preservation and agent transitions

### For AI Agents

**[🤖 Agent Entry Point](src/agor/tools/README_ai.md)** - Role selection and initialization (start here)
**[📋 User Guidelines for AugmentCode Local](docs/augment_user_guidelines.md)** - Complete guidelines for local agent integration
**[🚀 Platform Initialization Prompts](src/agor/tools/PLATFORM_INITIALIZATION_PROMPTS.md)** - Copy-paste prompts for each platform
**[📋 Comprehensive Instructions](src/agor/tools/AGOR_INSTRUCTIONS.md)** - Complete operational guide
**[📋 Documentation Index](src/agor/tools/index.md)** - Token-efficient lookup for AI models
**[🛠️ AGOR Development Guide](docs/agor-development-guide.md)** - For agents working on AGOR itself
**[💬 Agent Meta Feedback](src/agor/tools/agor-meta.md)** - Help improve AGOR through feedback

## 🔄 Operational Modes

AGOR enhances the original AgentGrunt capabilities by offering two primary operational modes with improved multi-agent coordination and flexible deployment options:

### 🚀 Standalone Mode (Direct Git Access)

**For agents with repository access** (AugmentCode Remote Agents, Jules by Google, etc.)

- **Direct commits**: Agents can make commits directly if they have commit access
- **Fallback method**: Copy-paste codeblocks if no commit access
- **Full git operations**: Branch creation, merging, pull requests
- **Real-time collaboration**: Multiple agents working on live repositories
- **No file size limits**: Complete repository access

### 📦 Bundled Mode (Upload-Based Platforms)

**For upload-based platforms** (Google AI Studio, ChatGPT, etc.)

- **Copy-paste workflow**: Users manually copy edited files from agent output
- **Manual commits**: Users handle git operations themselves
- **Platform flexibility**: Works with any AI platform that accepts file uploads
- **Free tier compatible**: Excellent for Google AI Studio Pro (free)

> **💡 Key Point**: All AGOR roles (Solo Developer, Project Coordinator, Agent Worker) function effectively in both Standalone and Bundled modes. The primary difference lies in how code changes are applied: direct Git commits are possible in Standalone Mode (if the agent has access), while Bundled Mode typically relies on a copy-paste workflow where the user handles the final commit.

## 🎯 Core Capabilities & Features

### Role-Based Workflows

AGOR defines distinct roles to structure AI-driven development tasks. Each role is equipped with a specialized set of tools and designed for specific types of activities:

**🔹 SOLO DEVELOPER**: Focuses on deep codebase analysis, implementation, and answering technical questions. Ideal for solo development tasks, feature implementation, and detailed debugging.

**🔹 PROJECT COORDINATOR**: Handles strategic planning, designs multi-agent workflows, and orchestrates team activities. Best suited for multi-agent project planning, strategy design, and overall team coordination.

**🔹 AGENT WORKER**: Executes specific tasks assigned by a Project Coordinator and participates in coordinated work snapshots. Primarily used for task execution within a team and following established multi-agent workflows.

### Multi-Agent Strategies

- **Parallel Divergent**: Independent exploration → peer review → synthesis
- **Pipeline**: Sequential snapshots with specialization
- **Swarm**: Dynamic task assignment for maximum parallelism
- **Red Team**: Adversarial build/break cycles for robustness
- **Mob Programming**: Collaborative coding with rotating roles

### Key Development Tools

- **Git integration** with portable binary (works in any environment)
- **Codebase analysis** with language-specific exploration
- **Memory persistence** with markdown files and git branch synchronization
- **Mandatory snapshot system** for context preservation and agent transitions
- **Quality gates** and validation checkpoints
- **Structured Snapshot Protocols** (for multi-agent coordination and solo context management)

## 📊 Hotkey Interface

AGOR utilizes a conversational hotkey system for AI-user interaction. The AI will typically present these options in a menu. This list includes common hotkeys; for comprehensive lists, refer to the role-specific menus in `AGOR_INSTRUCTIONS.md`.

**Strategic Planning**:

- `sp`: strategic plan
- `bp`: break down project
- `ar`: architecture review

**Strategy Selection**:

- `ss`: strategy selection
- `pd`: parallel divergent
- `pl`: pipeline
- `sw`: swarm

**Team Management**:

- `ct`: create team
- `tm`: team manifest
- `hp`: snapshot prompts

**Analysis**:

- `a`: analyze codebase
- `f`: full files
- `co`: changes only
- `da`: detailed snapshot

**Memory**:

- `mem-add`: add memory
- `mem-search`: search memories

**Editing & Version Control**:

- `edit`: modify files
- `commit`: save changes
- `diff`: show changes

**Coordination**:

- `init`: initialize
- `status`: check state
- `sync`: update
- `meta`: provide feedback

## 🏢 Platform Support

### Bundle Mode Platforms

- **Google AI Studio Pro** (Function Calling enabled, use `.zip` format) - _Free tier available_
- **ChatGPT** (requires subscription, use `.tar.gz` format)
- **Other upload-based platforms** (use appropriate format)

### Remote Agent Platforms

- **Augment Code Remote Agents** (cloud-based agents with direct git access)
- **Jules by Google** (direct URL access to files, limited git capabilities)
- **Any AI agent with git and shell access**

### Local Integration Platforms

- **AugmentCode Local Agent** (flagship local extension with workspace context)
- **Any local AI assistant** with file system access
- **Development environments** with AI integration

**Requirements**: Ability to read local files, Git access (optional but recommended), Python 3.10+ for advanced features

## 🏗️ Use Cases

**Large-Scale Refactoring** - Coordinate specialized agents for database, API, frontend, and testing
**Feature Development** - Break down complex features with clear snapshot points
**System Integration** - Plan integration with specialized validation procedures
**Code Quality Initiatives** - Coordinate security, performance, and maintainability improvements
**Technical Debt Reduction** - Systematic planning and execution across components

## 🔧 Advanced Commands

```bash
# Version information and updates
agor version                                # Show versions and check for updates

# Git configuration management
agor git-config --import-env                # Import from environment variables
agor git-config --name "Your Name" --email "your@email.com"  # Set manually
agor git-config --show                      # Show current configuration

# Custom bundle options
agor bundle repo --branch feature-branch   # Specific branch

agor bundle repo -f zip                     # Google AI Studio format
```

**Requirements**: Python 3.10+ | **Platforms**: Linux, macOS, Windows

---

## 🙏 Attribution

### Original AgentGrunt

- **Created by**: [@nikvdp](https://github.com/nikvdp)
- **Repository**: <https://github.com/nikvdp/agentgrunt>
- **License**: MIT License
- **Core Contributions**: Innovative code bundling concept, git integration, basic AI instruction framework

### AGOR Enhancements

- **Enhanced by**: [@jeremiah-k](https://github.com/jeremiah-k) (Jeremiah K)
- **Repository**: <https://github.com/jeremiah-k/agor>
- **License**: MIT License (maintaining original)
- **Major Additions**: Multi-agent coordination, strategic planning, prompt engineering, quality assurance frameworks, dual deployment modes
