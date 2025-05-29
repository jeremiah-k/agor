# 🎼 AgentOrchestrator (AGOR)

**Multi-Agent Development Coordination Platform**

Transform AI assistants into sophisticated development coordinators. Plan complex projects, design specialized agent teams, and orchestrate coordinated development workflows.

**Supports**: Linux, macOS, Windows | **Free Option**: Google AI Studio Pro | **Subscription**: ChatGPT

> **🔬 Alpha Protocol**: AGOR coordination strategies are actively evolving based on real-world usage. [Contribute feedback](https://github.com/jeremiah-k/agor/issues) to help shape AI coordination patterns.

## 🚀 Quick Start

### Bundle Mode (Upload to AI Platform)

**For Google AI Studio, ChatGPT, and other upload-based platforms:**

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

### 🚀 Standalone Mode (Direct Git Access)

**For AI agents with direct git access and file system capabilities (e.g., Augment Code Remote Agents).**

These agents operate directly on a cloned repository and do not use pre-packaged bundles.

**Initialization Protocol for Direct Access Agents:**

1.  **Ensure AGOR Protocols are Accessible:**
    *   **If working on the AGOR project itself:** The necessary instruction files (`src/agor/tools/README_ai.md`, `src/agor/tools/AGOR_INSTRUCTIONS.md`) and utility scripts are directly available within the `src/agor/tools/` directory of the AGOR repository.
    *   **If working on a separate user project:**
        *   **Option A (AGOR tools embedded):** The project may already have AGOR tools (e.g., in a `.agor_tools/` directory or similar). You will need the path to these files.
        *   **Option B (Clone AGOR separately):** If the project does not embed AGOR tools, you may need to clone the AGOR repository into a known temporary location (e.g., `/tmp/agor_repo/`) to access its instructional files and Python utilities.
        ```bash
        # Example: If needing to clone AGOR separately
        git clone https://github.com/jeremiah-k/agor.git /tmp/agor_repo
        ```

2.  **Load AGOR Instructions:**
    *   Read and internalize `README_ai.md` first, followed by `AGOR_INSTRUCTIONS.md`.
    *   Adjust paths as per step 1. Example if AGOR was cloned to `/tmp/agor_repo/`:
        ```bash
        cat /tmp/agor_repo/src/agor/tools/README_ai.md
        cat /tmp/agor_repo/src/agor/tools/AGOR_INSTRUCTIONS.md
        ```
    *   If AGOR tools are embedded in the project (e.g., in `.agor_tools/`), use that path:
        ```bash
        cat .agor_tools/README_ai.md
        cat .agor_tools/AGOR_INSTRUCTIONS.md
        ```

3.  **Operating Environment:**
    *   You are working directly within the user's project repository.
    *   Use standard `git` commands available in your environment for version control.
    *   Python utility scripts (e.g., for code exploration, strategy management) may need to be invoked using their path from the AGOR tools location (e.g., `python /tmp/agor_repo/src/agor/tools/code_exploration.py ...`). Ensure these scripts are executable or run via `python`.

4.  **Follow AGOR Protocols:** After role selection (guided by `README_ai.md`), follow the operational procedures, hotkey interactions, and coordination mechanisms detailed in `AGOR_INSTRUCTIONS.md`.



## 📚 Documentation

**[📖 Complete Usage Guide](docs/usage-guide.md)** - Comprehensive overview of modes, roles, and workflows
**[📋 Documentation Index](docs/index.md)** - Token-efficient lookup for AI models
**[Bundle Mode Guide](docs/bundle-mode.md)** - Complete platform setup (Google AI Studio, ChatGPT)
**[AGOR_INSTRUCTIONS.md](src/agor/tools/AGOR_INSTRUCTIONS.md)** - Comprehensive AI Operational Guide
**[README_ai.md](src/agor/tools/README_ai.md)** - Initial AI Bootstrap (Role Selection)
**[AGOR Development Guide](docs/agor-development-guide.md)** - For agents working on AGOR itself (includes Core Context section)
**[src/agor/tools/agor-meta.md](src/agor/tools/agor-meta.md)** - Feedback system

## 🔄 Operational Modes

AGOR enhances the original AgentGrunt capabilities by offering two primary operational modes with improved multi-agent coordination and flexible deployment options:

### 🚀 Standalone Mode (Direct Git Access)

**For AI agents with direct git access and file system capabilities (e.g., Augment Code Remote Agents).**

These agents operate directly on a cloned repository and do not use pre-packaged bundles.

**Initialization Protocol for Direct Access Agents:**

1.  **Ensure AGOR Protocols are Accessible:**
    *   **If working on the AGOR project itself:** The necessary instruction files (`src/agor/tools/README_ai.md`, `src/agor/tools/AGOR_INSTRUCTIONS.md`) and utility scripts are directly available within the `src/agor/tools/` directory of the AGOR repository.
    *   **If working on a separate user project:**
        *   **Option A (AGOR tools embedded):** The project may already have AGOR tools (e.g., in a `.agor_tools/` directory or similar). You will need the path to these files.
        *   **Option B (Clone AGOR separately):** If the project does not embed AGOR tools, you may need to clone the AGOR repository into a known temporary location (e.g., `/tmp/agor_repo/`) to access its instructional files and Python utilities.
        ```bash
        # Example: If needing to clone AGOR separately
        git clone https://github.com/jeremiah-k/agor.git /tmp/agor_repo
        ```

2.  **Load AGOR Instructions:**
    *   Read and internalize `README_ai.md` first, followed by `AGOR_INSTRUCTIONS.md`.
    *   Adjust paths as per step 1. Example if AGOR was cloned to `/tmp/agor_repo/`:
        ```bash
        cat /tmp/agor_repo/src/agor/tools/README_ai.md
        cat /tmp/agor_repo/src/agor/tools/AGOR_INSTRUCTIONS.md
        ```
    *   If AGOR tools are embedded in the project (e.g., in `.agor_tools/`), use that path:
        ```bash
        cat .agor_tools/README_ai.md
        cat .agor_tools/AGOR_INSTRUCTIONS.md
        ```

3.  **Operating Environment:**
    *   You are working directly within the user's project repository.
    *   Use standard `git` commands available in your environment for version control.
    *   Python utility scripts (e.g., for code exploration, strategy management) may need to be invoked using their path from the AGOR tools location (e.g., `python /tmp/agor_repo/src/agor/tools/code_exploration.py ...`). Ensure these scripts are executable or run via `python`.

4.  **Follow AGOR Protocols:** After role selection (guided by `README_ai.md`), follow the operational procedures, hotkey interactions, and coordination mechanisms detailed in `AGOR_INSTRUCTIONS.md`.



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
- **Memory persistence** via Memory Branches (which includes an SQLite backend for structured data alongside markdown files for notes).
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

**✅ Bundled Mode Platforms**

- **Google AI Studio Pro** (Function Calling enabled, use `.zip` format) - _Free tier available_
- **ChatGPT** (requires subscription, use `.tar.gz` format)
- **Other upload-based platforms** (use appropriate format)

**✅ Standalone Mode Platforms**

- **Augment Code Remote Agents** (direct git access)

- **Any AI agent with git and shell access**

**Bundle Formats**

- `.zip` - Optimized for Google AI Studio
- `.tar.gz` - Standard format for ChatGPT and other platforms
- `.tar.bz2` - High compression option

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
