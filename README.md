# 🚀 AgentGrunt: Multi-Agent Project Planning & Coordination

> A comprehensive project planning and multi-agent coordination platform. Plan complex development projects, design agent teams, and generate specialized prompts for coordinated AI development workflows.

Use with any AI platform that supports file uploads to plan implementations, coordinate multiple AI agents, and manage complex development projects across your entire git repository!

## Overview

AgentGrunt now serves as a comprehensive project planning and multi-agent coordination platform. It bundles your codebase with advanced planning tools, agent coordination templates, and specialized prompt generators into a single file that transforms any AI assistant into a project planning specialist.

Upload the archive to your preferred AI platform, and you'll have access to:
- **Strategic project planning** with task breakdown and dependency mapping
- **Multi-agent team design** with specialized roles and coordination workflows
- **Prompt engineering tools** for creating agent-specific instructions
- **Quality assurance planning** with validation checkpoints and review processes
- **Full codebase analysis** with implementation planning and risk assessment

## Features

### 🎯 Strategic Planning
- **Project breakdown** into manageable tasks with clear dependencies
- **Architecture analysis** and implementation planning
- **Risk assessment** with mitigation strategies
- **Timeline and resource planning**

### 👥 Multi-Agent Coordination
- **Team structure design** with specialized agent roles
- **Workflow orchestration** with handoff procedures
- **Communication protocols** and synchronization points
- **Quality gates** and validation checkpoints

### 📝 Prompt Engineering
- **Specialized agent prompts** for different technical roles
- **Context-rich handoff prompts** for seamless transitions
- **Validation prompts** for quality assurance
- **Integration prompts** for system coordination

### 🔧 Technical Capabilities
- **Comprehensive codebase analysis** with git integration
- **Multiple output formats** (full files, changes only, detailed analysis)
- **Advanced code exploration tools** with language-specific analysis
- **Built-in hotkey menu** for efficient navigation

## Installation

### Prerequisites

- a valid ChatGPT Plus subscription and Code Interpreter enabled in ChatGPT's settings
- a working installation of python 3.9 (or newer)
- a git repository that you'd like Code Interpreter to work on with you

Once you have those in place, run these to install:

```shell
git clone https://github.com/jeremiah-k/agor.git
cd agor
pipx install .
```

If all goes well running `agentgrunt --help` will output something like this:

```text
Usage: agentgrunt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bundle               Bundle up a local or remote git repo
  custom-instructions  Copy ChatGPT custom instructions to the clipboard
```

## Usage

To start editing a repo with `agentgrunt` use `agentgrunt`'s `bundle` command:

```shell
# Bundle the default branch (current branch for local repos)
agentgrunt bundle <path-to-your-repo>

# Bundle a specific branch
agentgrunt bundle <path-to-your-repo> --branch <branch-name>

# Bundle multiple specific branches
agentgrunt bundle <path-to-your-repo> --branches branch1,branch2,branch3

# Bundle all branches
agentgrunt bundle <path-to-your-repo> --all-branches
```

It will do some work and then print out some instructions. When the process has completed you'll have a new file called `<your-repo-name>.tar.gz` in your current folder.

By default, AgentGrunt bundles only the current branch (for local repos) or the default branch (for remote repos). You can use the branch options to include specific branches or all branches in the bundle, which can be useful when you need to work with multiple branches or want to perform operations across branches.

Now do the following:

- Copy the short prompt `agentgrunt` prints out to the clipboard (or just say `y` when prompted if on macOS)
- Open up ChatGPT and start a new chat in Code Interpreter mode
- Use the + button to upload the `<your-repo-name>.tar.gz` file AgentGrunt generated
- Paste the prompt you copied a second ago into the chatbox and press send

You'll see your AI assistant transform into a project planning specialist with a comprehensive hotkey menu organized into categories:

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

Now you can plan complex projects, design agent teams, and coordinate multi-agent development workflows!

When you need to implement the planned changes, use the various display options:
- **`f`** for complete files ready for copy/paste into your IDE
- **`co`** for focused change summaries
- **`da`** for detailed analysis that can be handed off to other AI agents
- **Agent prompts** for coordinating multiple AI assistants on complex projects

## How it works

AgentGrunt creates a comprehensive project planning bundle that includes:

1. **Your complete codebase** with git history and branch information
2. **Advanced planning tools** including project templates and coordination frameworks
3. **Specialized prompt generators** for different types of AI agents
4. **Code exploration utilities** for deep codebase analysis
5. **Multi-agent coordination templates** for complex project workflows

The [`gpt_tools`](agentgrunt/gpt_tools) folder contains:
- [`README_ai.md`](agentgrunt/gpt_tools/README_ai.md) - Comprehensive AI instructions with multi-agent capabilities
- [`code_exploration.py`](agentgrunt/gpt_tools/code_exploration.py) - Advanced code analysis functions
- [`agent_prompt_templates.py`](agentgrunt/gpt_tools/agent_prompt_templates.py) - Specialized prompt generators
- [`project_planning_templates.py`](agentgrunt/gpt_tools/project_planning_templates.py) - Project coordination frameworks
- [`code_exploration_docs.md`](agentgrunt/gpt_tools/code_exploration_docs.md) - Detailed tool documentation

This creates a complete project planning environment that can coordinate multiple AI agents working together on complex development tasks.

## Best Practices

### 🎯 Project Planning
- **Start with strategic planning** (`sp`) to define clear goals and scope
- **Break down complex projects** (`bp`) into manageable, coordinated tasks
- **Analyze dependencies** (`dp`) before assigning work to different agents
- **Plan quality gates** (`qg`) and validation checkpoints throughout the project

### 👥 Multi-Agent Coordination
- **Design your team structure** (`ct`) based on project complexity and requirements
- **Create clear handoff procedures** (`hp`) to ensure smooth agent transitions
- **Establish communication protocols** (`tc`) for agent coordination
- **Plan synchronization points** (`sy`) where agents align their progress

### 📝 Prompt Engineering
- **Use context-rich prompts** (`cp`) that include relevant codebase knowledge
- **Create specialized prompts** (`gp`) for different agent roles and responsibilities
- **Design validation prompts** (`vp`) for quality assurance and code review
- **Plan integration prompts** (`ip`) for system-wide coordination

### 🔧 Technical Implementation
- **Analyze the codebase thoroughly** (`a`) before planning changes
- **Use appropriate display formats** (`f`, `co`, `da`) based on your needs
- **Refresh the context** (`r`) during long planning sessions
- **Document decisions and rationale** for future reference

## Use Cases

### 🏗️ Large-Scale Refactoring
Plan and coordinate major codebase refactoring with multiple specialized agents handling different aspects (database, API, frontend, testing).

### 🚀 Feature Development
Break down complex features into coordinated tasks with clear handoff points between frontend, backend, and testing agents.

### 🔧 System Integration
Plan integration of new systems or services with specialized agents for different integration points and validation procedures.

### 📊 Code Quality Improvement
Coordinate comprehensive code quality initiatives with agents focused on different aspects (security, performance, maintainability).

### 🎯 Technical Debt Reduction
Systematically plan and execute technical debt reduction with coordinated efforts across multiple system components.

## Future Vision

This enhanced AgentGrunt represents a new paradigm in AI-assisted development: **coordinated multi-agent project execution**. As AI agents become more capable and prevalent, the ability to plan, coordinate, and manage teams of specialized AI assistants will become increasingly valuable.

The tool provides a foundation for:
- **Enterprise-scale AI development teams**
- **Automated project planning and execution**
- **Quality-assured multi-agent workflows**
- **Scalable development process automation**

---

## 📄 License

**AgentOrchestrator (AGOR)** is released under the MIT License.

- **Repository**: https://github.com/jeremiah-k/agor
- **License**: MIT License
