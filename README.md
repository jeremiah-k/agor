# 🎼 AgentOrchestrator (AGOR)

## Multi-Agent Development Coordination Platform

> Transform any AI assistant into a sophisticated project planning and multi-agent coordination specialist. Plan complex development projects, design agent teams, and orchestrate coordinated AI development workflows.

AGOR runs on Linux, macOS, and Windows.

> **⚠️ Status Note**: Bundle Mode is well-tested and works reliably. Agent Mode has been tested with basic workflows, but requires more testing in multi-agent environments.
>
> **🔬 Alpha Protocol**: The AGOR coordination protocol is actively evolving. We're continuously refining multi-agent strategies, communication patterns, and workflow templates based on real-world usage. **Want to help shape the future of AI coordination in this project?** Please [open an issue](https://github.com/jeremiah-k/agor/issues), [start a discussion](https://github.com/jeremiah-k/agor/discussions), or [submit a PR](https://github.com/jeremiah-k/agor/pulls) with your ideas and feedback!

## 🚀 Quick Start

### Agent Mode (For AI Agents with Direct Git Access)

**For Augment Code Remote Agents, Jules by Google, and other AI agents:**

```bash
# Remember your main project directory
MAIN_PROJECT_DIR=$(pwd)
echo "Main project: $MAIN_PROJECT_DIR"

# Clone AGOR to temporary location (don't interfere with main project)
cd /tmp
git clone https://github.com/jeremiah-k/agor.git
cd agor

# Load AGOR protocol and capabilities
cat AGOR_INSTRUCTIONS.md
cat src/agor/tools/README_ai.md

# Return to main project directory when ready to work
# cd "$MAIN_PROJECT_DIR"
```

### Bundle Mode (For AI Platform Upload)

**For ChatGPT, Google AI Studio, and other upload-based AI platforms:**

```bash
# User installs AGOR locally
pipx install agor

# Bundle your project for upload
agor bundle /path/to/your/project

# Upload the generated bundle to your AI platform
# Supports .zip format for Google AI Studio (free with Pro models)
# Supports .tar.gz format for ChatGPT and other platforms
```

## 🎯 Core Capabilities

### Strategic Planning

- **Project breakdown** into manageable, coordinated tasks
- **Architecture analysis** and implementation planning
- **Risk assessment** with mitigation strategies
- **Dependency mapping** and execution sequencing

### Multi-Agent Coordination

- **Team structure design** with specialized agent roles
- **Workflow orchestration** with handoff procedures
- **Communication protocols** and synchronization points
- **Quality gates** and validation checkpoints

### Prompt Engineering

- **Specialized agent prompts** for different technical roles
- **Context-rich handoff prompts** for seamless transitions
- **Validation prompts** for quality assurance
- **Integration prompts** for system coordination

### Advanced Analysis

- **Comprehensive codebase analysis** with git integration
- **Multiple output formats** (full files, changes only, detailed analysis)
- **Language-specific code exploration** tools
- **Memory persistence** across sessions

## 🎼 The Orchestration Metaphor

Like a conductor leading a symphony orchestra, AgentOrchestrator coordinates multiple AI agents, each with specialized skills, to create harmonious development workflows:

- **🎻 Frontend Agents** - User interface specialists
- **🎺 Backend Agents** - Server-side logic experts
- **🥁 Database Agents** - Data architecture specialists
- **🎹 Testing Agents** - Quality assurance focused
- **🎸 DevOps Agents** - Deployment and infrastructure
- **🎤 Integration Agents** - System coordination

## 📋 Comprehensive Hotkey Menu

```text
📊 Analysis & Display:
a ) analyze codebase    f ) display full edited files
co) show changes only   da) detailed analysis for handoff
m ) show diff of last change

🎯 Strategic Planning:
sp) strategic planning  bp) break down project
ar) architecture review dp) dependency planning
rp) risk planning

👥 Agent Team Management:
ct) create team        as) assign specialists
tc) team coordination  wf) workflow design
tm) team manifest

📝 Prompt Engineering:
gp) generate prompts   cp) context prompts
hp) handoff prompts    vp) validation prompts
ip) integration prompts

🔄 Coordination:
eo) execution order    ch) checkpoint planning
sy) sync points        qg) quality gates
rb) rollback planning
```

## 🏗️ Use Cases

### Large-Scale Refactoring

Coordinate multiple specialized agents for database, API, frontend, and testing aspects of major codebase refactoring.

### Feature Development

Break down complex features into coordinated tasks with clear handoff points between frontend, backend, and testing agents.

### System Integration

Plan integration of new systems with specialized agents for different integration points and validation procedures.

### Code Quality Initiatives

Coordinate comprehensive quality improvements with agents focused on security, performance, and maintainability.

### Technical Debt Reduction

Systematically plan and execute technical debt reduction across multiple system components.

## 🔮 Future Vision

AgentOrchestrator represents a new paradigm: **coordinated multi-agent project execution**. As AI agents become more capable, the ability to plan, coordinate, and manage teams of specialized AI assistants becomes increasingly valuable.

Foundation for:

- **Enterprise-scale AI development teams**
- **Automated project planning and execution**
- **Quality-assured multi-agent workflows**
- **Scalable development process automation**

## 🛠️ Installation

### For Bundle Mode (ChatGPT Upload)

**Users need to install AGOR locally to create bundles:**

```bash
# Install using pipx (recommended)
pipx install agor

# Or using pip
pip install agor
```

### For Agent Mode (AI Agents)

**No installation required - agents clone directly:**

```bash
# AI agents clone AGOR repository directly
git clone https://github.com/jeremiah-k/agor.git
cd agor
# Follow AGOR_INSTRUCTIONS.md
```

### Development Installation

```bash
# For AGOR development
git clone https://github.com/jeremiah-k/agor.git
cd agor
pipx install -e . --force
```

## 📁 Project Structure

```text
agor/
├── README.md (this file)
├── AGOR_INSTRUCTIONS.md (standalone mode guide)
├── src/agor/
│   ├── main.py (CLI tool)
│   └── tools/
│       ├── README_ai.md (comprehensive AI instructions)
│       ├── code_exploration.py (analysis tools)
│       ├── agent_prompt_templates.py (prompt generators)
│       ├── project_planning_templates.py (coordination frameworks)
│       └── code_exploration_docs.md (tool documentation)
└── [configuration files]
```

## 📖 Documentation

### Mode-Specific Instructions

- **[AGOR_INSTRUCTIONS.md](AGOR_INSTRUCTIONS.md)** - Agent Mode (for AI agents with direct git access)
- **[BUNDLE_INSTRUCTIONS.md](BUNDLE_INSTRUCTIONS.md)** - Bundle Mode (for AI agents that accept .zip/.tar.gz uploads)

### Technical Documentation

- **[src/agor/tools/README_ai.md](src/agor/tools/README_ai.md)** - Complete AI protocol and capabilities
- **[src/agor/tools/code_exploration_docs.md](src/agor/tools/code_exploration_docs.md)** - Tool reference and API

---

## 📄 License

**AgentOrchestrator (AGOR)** is released under the MIT License.

- **Repository**: <https://github.com/jeremiah-k/agor>
- **License**: MIT License

## 🙏 Attribution

**AgentOrchestrator is an enhanced fork of the original [AgentGrunt](https://github.com/nikvdp/agentgrunt) created by [@nikvdp](https://github.com/nikvdp).**

### Original AgentGrunt

- **Creator**: [@nikvdp](https://github.com/nikvdp) (Nik V)
- **Repository**: <https://github.com/nikvdp/agentgrunt>
- **License**: MIT License
- **Core Contributions**: Code bundling concept, git integration, AI instruction framework

### AgentOrchestrator Enhancements

- **Enhanced by**: [@jeremiah-k](https://github.com/jeremiah-k) (Jeremiah K)
- **Repository**: <https://github.com/jeremiah-k/agor>
- **License**: MIT License
- **Additions**: Multi-agent coordination, strategic planning, prompt engineering, dual deployment modes

### Additional Inspiration

- **[@NickADobos](https://twitter.com/NickADobos)** - "[AI zip bomb](https://twitter.com/NickADobos/status/1687938356813180928)" concept

---

**Ready to orchestrate your development project? Choose your deployment mode and begin coordinating!**
