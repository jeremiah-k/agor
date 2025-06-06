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

**For detailed platform-specific agent initialization instructions, see the [Complete Usage Guide](docs/usage-guide.md#platform-specific-agent-initialization).**

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
