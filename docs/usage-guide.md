# 📖 AGOR Usage Guide - Comprehensive Overview

**Complete guide to understanding and using AgentOrchestrator effectively**

## 🚀 Installation & Platform Setup

This section provides detailed setup instructions for initializing AGOR agents on different platforms. Choose the platform that matches your environment.

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
- Copy and paste the complete User Guidelines from: [docs/augment_user_guidelines.md](augment_user_guidelines.md)

_This ensures the agent follows AGOR protocols and creates mandatory snapshots_

**Step 4: Agent Initialization Requirements**

**CRITICAL**: The agent must read these files before starting any work:

- `src/agor/tools/README_ai.md` (role selection and initialization)
- `src/agor/tools/AGOR_INSTRUCTIONS.md` (comprehensive operational guide)
- `src/agor/tools/agent-start-here.md` (quick startup guide)
- `src/agor/tools/index.md` (documentation index for efficient lookup)



**Step 5: Agent Initialization Prompt**

**Copy and paste this initialization prompt to your agent:**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files from the workspace sources to understand the system:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
- src/agor/tools/agent-start-here.md (quick startup guide)
- src/agor/tools/index.md (documentation index for efficient lookup)

After reading these files, help me initialize AGOR for this project and select the appropriate role (Worker Agent or Project Coordinator) based on the task requirements.

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

**Note: First copy and paste the User Guidelines from [docs/augment_user_guidelines.md](augment_user_guidelines.md) into your AugmentCode extension, if you have not already, then proceed with the rest.**

**Agent Initialization Prompt (Copy & Paste to Remote Agent):**

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please execute these commands to initialize AGOR:

# Clone AGOR to temporary location
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor

# Load protocol and return to project
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md

# Install ONLY the dependencies needed for agent dev tools (NOT requirements.txt)
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

# Test AGOR development tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import test_all_tools, get_current_timestamp_formatted

# Verify tooling works
test_all_tools()
print(f'Session started at: {get_current_timestamp_formatted()}')
"

# Review agent startup guide
cat src/agor/tools/agent-start-here.md

# Now return to your project's directory with AGOR initialized

After initialization, select your role based on the task:
- Worker Agent: Code analysis, implementation, debugging, task execution
- Project Coordinator: Planning, architecture, multi-agent coordination

# <--- Add your detailed step-by-step instructions below --->
```

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

After reading these files, help me initialize AGOR for this project and select the appropriate role (Worker Agent or Project Coordinator).

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

## 💬 Example User Prompts

**📖 For comprehensive examples with emphasis on using AGOR tools, see: [Agent Prompt Examples](agent-prompt-examples.md)**

Here are key examples of how to ask agents to use AGOR tools:

### 📸 Creating Snapshots & Handoffs

**End of work session:**
> "**Use AGOR's snapshot tools** to create a development snapshot of our progress, then **generate a handoff prompt** so another agent can continue this work. **Wrap the output in a single codeblock** so I can copy and paste easily for a clean transition."

**Before switching tasks:**
> "**Use `create_development_snapshot()`** to save our current progress, then **use AGOR's PR tools** to generate a description for this work. **Run both through dev tools and wrap each in separate codeblocks** for easy copy-paste."

**Regular progress saving:**
> "**Use AGOR's `quick_commit_and_push()`** to commit our progress and **create an AGOR snapshot** in case we need to hand this off later. **Wrap the snapshot output in a single codeblock.**"

### 🚀 Release & PR Management

**After completing a feature:**
> "**Use AGOR's `quick_commit_and_push()`** to commit our authentication feature changes, then **use the dev tools to generate release notes** for this update. **Wrap the release notes in a single codeblock** for easy copy-paste."

**When work is ready for review:**
> "**Use `generate_pr_description_output()`** to create a properly formatted PR description that explains what we built and why. **Wrap the final output in a single codeblock** so I can copy and paste it directly."

**For bug fixes:**
> "**Use AGOR's commit tools** to save this login fix, then **generate release notes using AGOR tools** about what was resolved. **Format the output in a single codeblock.**"

### 🔄 Agent Coordination

**Starting work from a handoff:**
> "I received a handoff from another agent. Can you load the latest snapshot and show me what needs to be done next?"

**Checking project status:**
> "What's the current status of this project? Can you create a progress snapshot so I understand where we are?"

**Multi-agent collaboration:**
> "Another agent will be working on the frontend while I handle the backend. Can you create a coordination snapshot and update the agent conversation log?"

### 🛠️ Development Workflow

**Before major changes:**
> "I'm about to refactor the database layer. Let's create a snapshot first so we can roll back if needed."

**After testing:**
> "All tests are passing now. Can you commit our changes and generate release notes for the QA team?"

**Code review preparation:**
> "This branch is ready for code review. Generate a PR description that highlights the key changes and testing approach."

<details>
<summary><b>Google AI Studio Pro (Free Tier Phase-Out)</b></summary>

### Google AI Studio Pro

**⚠️ Note**: The free version of Google AI Studio Pro is being phased out. Most existing users rely on the free tier.

**Setup:**

- Use **Bundled Mode** with `.zip` format
- **Any role works** - choose based on your workflow needs
- To enable Function Calling in your project settings
- Memory synchronization works automatically

**Workflow:**

```bash
agor bundle your-project -f zip
# Upload to Google AI Studio Pro
# Select role based on your needs:
# • Worker Agent: For code analysis and implementation
# • Project Coordinator: For planning and strategy
# All roles work with copy-paste workflow
```

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

# Install ONLY the dependencies needed for agent dev tools (NOT requirements.txt)
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

# Test AGOR development tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import test_all_tools, get_current_timestamp_formatted

# Verify tooling works
test_all_tools()
print(f'Session started at: {get_current_timestamp_formatted()}')
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

## 🎯 NEW USERS: Start with Workflow Optimization

**ESSENTIAL READING**: After setup, read [Agent Workflow Optimization Guide](agent-workflow-optimization.md) to learn proven strategies for maintaining seamless agent coordination. This guide contains real-world examples and troubleshooting that will save you time and improve your AGOR experience significantly.

**Why this matters**: AGOR's power comes from seamless agent coordination. The workflow optimization guide teaches you how to structure prompts, maintain context, and avoid common coordination breakdowns that can frustrate new users.

## 🎭 Role Selection Deep Dive

### 🔍 Worker Agent

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

- Comprehensive codebase analysis and exploration
- Implementation and development work
- Technical documentation and explanation
- Development tooling for snapshots and handoffs

**Typical Workflow:**

1. Analyze codebase using detailed prompts and context
2. Explore specific code areas based on requirements
3. Implement changes or provide detailed explanations
4. Use development tools for snapshots and documentation

**Why Use AGOR as a Worker Agent?**

While "Orchestrator" might suggest a multi-agent focus, AGOR provides significant benefits even for individual development work:

- **Structured Work Management**: AGOR's protocols encourage a methodical approach to tasks. Even if you're the only "agent," thinking in terms of analysis, implementation, and (self-)snapshots can bring clarity to complex projects.
- **Context Preservation**: AI assistants often have context window limits. Using AGOR's snapshot creation functionality (even if you're creating a snapshot for yourself for a later session or a different AI model) allows you to create a comprehensive snapshot of your current work, including code changes, analysis, and next steps. This means you can pick up exactly where you left off without losing valuable context.
- **Tool Integration**: AGOR provides a consistent interface for interacting with your codebase, including integrated Git commands and analysis tools, all within the AI's workflow.
- **Future Scalability**: If your solo project grows to involve more collaborators (human or AI), you'll already have a structured process in place.
- **Team Integration**: When part of a team, the Worker Agent excels at executing specific tasks assigned by a Project Coordinator, often based on detailed work snapshots, and integrates smoothly into established multi-agent workflows.

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

- Initialize various coordination strategies (e.g., Parallel Divergent, Pipeline, Swarm).
- Create specialized agent teams.
- Design snapshot procedures and prompts.
- Monitor team progress and coordination

**Typical Workflow:**

1. Analyze project requirements.
2. Select an optimal strategy.
3. Create a specialized team.
4. Initialize strategy and coordinate agents

## 🎼 Multi-Agent Coordination Strategies

AGOR is exploring several advanced strategies for multi-agent collaboration. While these are areas of ongoing development and refinement, they illustrate various approaches to coordinating multiple AI agents:

### When to Use Each Strategy

**🔄 Parallel Divergent** - Multiple independent solutions

- **Use for**: Feature design, architecture decisions, creative problem-solving
- **Roles**: Multiple Worker Agent agents working independently
- **Outcome**: Best ideas synthesized into final solution

**⚡ Pipeline** - Sequential work via snapshots with specialization

- **Use for**: Complex features requiring different expertise
- **Roles**: Specialized agents (Backend → Frontend → Testing → DevOps)
- **Outcome**: Polished, well-integrated solution

**🐝 Swarm** - Dynamic task assignment

- **Use for**: Large projects with many independent tasks
- **Roles**: Multiple AGENT WORKER agents pulling from task queue
- **Outcome**: Maximum parallelism and efficiency

**⚔️ Red Team** - Adversarial build/break cycles

- **Use for**: Security-critical features, robust system design
- **Roles**: Builder agents vs. Breaker agents
- **Outcome**: Highly robust, security-tested solution

**👥 Mob Programming** - Collaborative coding

- **Use for**: Complex algorithms, learning scenarios, critical code
- **Roles**: Rotating Driver, Navigator, Observers, Researcher
- **Outcome**: High-quality, well-understood code

## 🚀 Getting Started Recommendations

### For Beginners

1. **Start with Bundled Mode** using Google AI Studio Pro (free)
2. **Choose any role** based on what you want to do:
   - **Worker Agent**: For code analysis and implementation
   - **Project Coordinator**: For planning and strategy
3. **Try basic operations like analyzing the codebase, viewing full files, or checking the system status.**
4. **Practice with small projects** before attempting multi-agent workflows

### For Advanced Users

1. **Try Standalone Mode** with git-capable agents
2. **Experiment with different roles** based on your needs
3. **Initialize different multi-agent strategies.**
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
2. Ensure all agents are regularly synchronizing their work.
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

_This guide evolves with AGOR. Suggest improvements through GitHub issues or by providing feedback through the AGOR system._
