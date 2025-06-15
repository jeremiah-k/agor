# 🎼 AgentOrchestrator (AGOR)

**Multi-Agent Development Coordination Platform**

Transform AI assistants into sophisticated development coordinators. Plan complex projects, design specialized agent teams, and orchestrate coordinated development workflows.

**Supports**: Linux, macOS, Windows | **Primary Platforms**: ChatGPT, AugmentCode, Google AI Studio

> **🔬 Alpha Protocol**: AGOR coordination strategies are actively evolving based on real-world usage. [Contribute feedback](https://github.com/jeremiah-k/agor/issues) to help shape AI coordination patterns.

> **🚧 Under Construction**: We're still figuring out what works and what doesn't for the dev tools, so be warned some functionality might be broken.

## 🚀 Installation & Deployment

AGOR supports multiple deployment modes for different AI platforms and workflows. Choose the approach that matches your environment:

**📦 Bundle Mode** - Upload-based platforms - Google AI Studio, ChatGPT (not Codex)
**🚀 Standalone Mode** - Direct git access - AugmentCode Remote, Jules by Google (limited support), Codex (currently untested)
**🏠 Local Integration** - Workspace integration (AugmentCode Local Agent)

AGOR facilitates AI-driven development through seamless context transfer and programmatic coordination tools. While the name "Orchestrator" suggests a multi-agent focus, AGOR's robust protocols for structured work, context management (especially via its snapshot capabilities), and tool integration are highly valuable even for **solo developers**. The core value lies in **transferring context between agents with minimal friction** and using development tools to programmatically guide agents through common tasks, reducing the need for specific instructions each time. Understanding these coordination capabilities is key to leveraging AGOR effectively, whether working alone or in a team.

**For installation instructions and platform-specific setup, see the [Usage Guide](docs/usage-guide.md).**

## 📚 Documentation

### For Users

**[📖 Usage Guide](docs/usage-guide.md)** - Overview of modes, roles, and workflows
**[🚀 Quick Start Guide](docs/quick-start.md)** - Step-by-step getting started instructions
**[📦 Bundle Mode Guide](docs/bundle-mode.md)** - Platform setup (Google AI Studio, ChatGPT)
**[🔄 Multi-Agent Strategies](docs/strategies.md)** - Coordination strategies and when to use them
**[📸 Snapshot System](docs/snapshots.md)** - Context preservation and agent transitions

### For AI Agents

**[🤖 Agent Entry Point](src/agor/tools/README_ai.md)** - Role selection and initialization (start here)
**[📋 User Guidelines for AugmentCode Local](docs/augment_user_guidelines.md)** - Guidelines for local agent integration
**[🚀 Platform Initialization Prompts](src/agor/tools/PLATFORM_INITIALIZATION_PROMPTS.md)** - Copy-paste prompts for each platform
**[📋 Instructions](src/agor/tools/AGOR_INSTRUCTIONS.md)** - Operational guide
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

> **💡 Key Point**: All AGOR roles (Worker Agent, Project Coordinator) function effectively in both Standalone and Bundled modes. The primary difference lies in how code changes are applied: direct Git commits are possible in Standalone Mode (if the agent has access), while Bundled Mode typically relies on a copy-paste workflow where the user handles the final commit.

## 🎯 Core Capabilities & Features

AGOR structures AI-driven development through distinct roles and a powerful set of tools:

**🔹 Worker Agent**: Focuses on deep codebase analysis, implementation, debugging, and answering technical questions. Ideal for solo development tasks, feature implementation, and executing specific tasks within a coordinated workflow. This role is crucial for hands-on development and detailed technical work.

**🔹 Project Coordinator**: Handles strategic planning, designs multi-agent workflows, and orchestrates team activities. Best suited for project oversight, breaking down complex tasks, strategy design, and overall team coordination. This role ensures that development efforts are aligned and progressing efficiently.

### Advanced Coordination Concepts (Experimental)

AGOR is exploring several advanced strategies for multi-agent collaboration. These are currently experimental and represent future directions for the framework:

- **Parallel Divergent**: Independent exploration by multiple agents, followed by peer review and synthesis of solutions.
- **Pipeline**: Sequential task handling where work is passed between specialized agents via snapshots.
- **Swarm**: Dynamic task assignment from a shared queue to maximize parallelism.
- **Red Team**: Adversarial build/break cycles to improve robustness and identify weaknesses.
- **Mob Programming**: Collaborative coding where multiple agents (or an agent and humans) work together on the same task simultaneously.

### Key Features for Context Management and Development

AGOR provides tools designed to facilitate seamless development and effective context transfer, whether working solo or in a multi-agent team:

- **Structured Snapshot System**: Capture and transfer detailed work context between development sessions or different AI agents, ensuring continuity and shared understanding. This is crucial for complex tasks and effective handoffs.
- **Agent Handoff Prompts**: Generate clear, actionable prompts for transferring tasks and context to another agent, detailing work completed, current status, and next steps.
- **Integrated Memory System**: Persist important information, decisions, and learnings using markdown files synchronized with Git branches. This allows agents to maintain context over time and across different tasks.
- **Git Integration**: A portable Git binary enables direct version control operations within the agent's environment, facilitating standard development practices.
- **Codebase Analysis Tools**: Explore and understand codebases with language-specific tools, aiding in efficient navigation and comprehension.

## ⚙️ Core Operations and Functionality

AGOR empowers users and AI agents with a range of functionalities accessible through a conversational interface. Instead of cryptic shortcuts, AGOR focuses on the actions you can perform:

**Strategic Project Management:**

- Develop comprehensive strategic plans for projects.
- Break down large projects into manageable tasks and phases.
- Conduct architectural reviews and plan for system improvements.

**Coordination and Team Setup (for multi-agent scenarios):**

- Select and initialize various multi-agent coordination strategies (such as Parallel Divergent, Pipeline, etc.).
- Design and create specialized agent teams with defined roles.
- Prepare snapshot procedures and prompts for effective agent handoffs.

**Codebase Interaction and Analysis:**

- Perform in-depth analysis of the existing codebase.
- View the full content of project files.
- Display only the changes made to files for focused review.
- Generate detailed snapshots of work for context sharing or backup.

**Memory and Context Management:**

- Add information to the persistent memory system.
- Search the existing memory for relevant information.

**Development and Version Control:**

- Modify project files with an integrated editing capability.
- Commit changes to the version control system with descriptive messages.
- View differences between versions of files.

**Session and System Management:**

- Initialize the AGOR environment for a new project or session.
- Check the current status of the project and AGOR system.
- Synchronize work with the main repository or other agents.
- Provide feedback on AGOR's performance and features.

## 🏢 Platform Support

### Bundle Mode Platforms

- **Google AI Studio Pro** (Function Calling enabled, use `.zip` format)
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
