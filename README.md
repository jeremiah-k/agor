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

**Bundle Options**: Use `-f zip` for Google AI Studio, `--sqlite` for memory features, `--branch` for specific branches

> **First time?** AGOR will guide you through an interactive setup menu to configure your preferred platform and options.

### Agent Mode (Direct Git Access)

**For AI agents with git access (Augment Code, Jules by Google, etc.) - Agent should execute:**

```bash
# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to your project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md
```

## 🎯 Core Capabilities

**Role-Based Initialization**

AGOR offers three primary roles when agents load the protocol:

- **PROJECT COORDINATOR** *(Multi-Agent)*: Strategic planning and team coordination
- **ANALYST/SOLO DEV** *(Solo or Multi-Agent)*: Deep codebase analysis and implementation
- **AGENT WORKER** *(Multi-Agent)*: Task execution and coordination handoffs

> **💡 Flexibility Note**: While PROJECT COORDINATOR and AGENT WORKER are designed for multi-agent workflows, ANALYST/SOLO DEV can operate both independently (great for bundled mode with Google AI Studio) and as part of larger multi-agent teams.

**Multi-Agent Strategies**

- **Parallel Divergent**: Independent exploration → peer review → synthesis
- **Pipeline**: Sequential handoffs with specialization
- **Swarm**: Dynamic task assignment for maximum parallelism
- **Red Team**: Adversarial build/break cycles for robustness
- **Mob Programming**: Collaborative coding with rotating roles

**Development Tools**

- **Git integration** with portable binary (works in any environment)
- **Codebase analysis** with language-specific exploration
- **Memory persistence** with markdown files or SQLite database (experimental)
- **Quality gates** and validation checkpoints
- **Cross-agent coordination** with structured handoff protocols

## 🔄 Operational Modes

**Born from AgentGrunt** - AGOR evolved from the innovative AgentGrunt project, maintaining its core strength in standalone operations while adding sophisticated multi-agent coordination.

### 🚀 Standalone Mode (Direct Git Access)

**For agents with repository access** (Augment Code, Jules by Google, etc.)

- **Direct commits**: Agents can make commits directly to repositories
- **Full git operations**: Branch creation, merging, pull requests
- **Real-time collaboration**: Multiple agents working on live repositories
- **No file size limits**: Complete repository access

### 📦 Bundled Mode (Upload-Based Platforms)

**For upload-based platforms** (Google AI Studio, ChatGPT, etc.)

- **Copy-paste workflow**: Users manually copy edited files from agent output
- **Manual commits**: Users handle git operations themselves
- **Platform flexibility**: Works with any AI platform that accepts file uploads
- **Free tier compatible**: Excellent for Google AI Studio Pro (free)

## 📊 Hotkey Interface

**Strategic Planning**: `sp` strategic plan | `bp` break down project | `ar` architecture review
**Strategy Selection**: `ss` strategy selection | `pd` parallel divergent | `pl` pipeline | `sw` swarm
**Team Management**: `ct` create team | `tm` team manifest | `hp` handoff prompts
**Analysis**: `a` analyze codebase | `f` full files | `co` changes only | `da` detailed handoff
**Memory**: `mem-add` add memory | `mem-search` search memories | `db-stats` database stats (SQLite mode)
**Coordination**: `init` initialize | `status` check state | `sync` update | `meta` provide feedback

## 🏢 Platform Support

**✅ Bundled Mode Platforms**

- **Google AI Studio Pro** (Function Calling enabled, use `.zip` format) - *Free tier available*
- **ChatGPT** (requires subscription, use `.tar.gz` format)
- **Claude** (via file upload, use `.tar.gz` format)
- **Other upload-based platforms** (use appropriate format)

**✅ Standalone Mode Platforms**

- **Augment Code Remote Agents** (direct git access)
- **Jules by Google** (direct git access)
- **Any AI agent with git and shell access**

**Bundle Formats**

- `.zip` - Optimized for Google AI Studio
- `.tar.gz` - Standard format for ChatGPT and other platforms
- `.tar.bz2` - High compression option

## 🏗️ Use Cases

**Large-Scale Refactoring** - Coordinate specialized agents for database, API, frontend, and testing
**Feature Development** - Break down complex features with clear handoff points
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

# Generate agent manifest for standalone mode
agor agent-manifest                         # Generate and copy manifest
agor agent-manifest --format json          # JSON format

# Custom bundle options
agor bundle repo --branch feature-branch   # Specific branch
agor bundle repo --sqlite                   # With SQLite memory
agor bundle repo -f zip                     # Google AI Studio format
```

**Requirements**: Python 3.10+ | **Platforms**: Linux, macOS, Windows

---

## 📚 Documentation

**[📖 Complete Usage Guide](docs/usage-guide.md)** - Comprehensive overview of modes, roles, and workflows
**[📋 Documentation Index](docs/index.md)** - Token-efficient lookup for AI models
**[Bundle Mode Guide](docs/bundle-mode.md)** - Complete platform setup (Google AI Studio, ChatGPT)
**[AGOR_INSTRUCTIONS.md](src/agor/tools/AGOR_INSTRUCTIONS.md)** - Agent Mode setup
**[src/agor/tools/README_ai.md](src/agor/tools/README_ai.md)** - Complete AI protocol
**[AGOR Development Guide](docs/agor-development-guide.md)** - For agents working on AGOR itself
**[src/agor/tools/agor-meta.md](src/agor/tools/agor-meta.md)** - Feedback system

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
