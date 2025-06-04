# 📖 AGOR Usage Guide - Comprehensive Overview

**Complete guide to understanding and using AgentOrchestrator effectively**

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

# Review development guide
cat docs/agor-development-guide.md
cat docs/agent-start-here.md

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

## 🔧 Platform-Specific Guidance

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

### AugmentCode VS Code Extension (Local Mode)

**For the flagship AugmentCode VS Code extension running locally:**

**Setup:**

- Clone AGOR repository to your local machine
- Add the AGOR directory to your "Sources" in the AugmentCode extension settings
- Add AGOR initialization instructions to your "User Guidelines" in AugmentCode
- Optionally add to "Augment Memories" if the agent needs reminders to use AGOR

**User Guidelines to Add:**

```
When working on development tasks, initialize AGOR by reading the protocol files:
- Read src/agor/tools/AGOR_INSTRUCTIONS.md for complete operational guide
- Read src/agor/tools/README_ai.md for role selection
- Select appropriate role based on task requirements
- Follow AGOR coordination protocols for multi-agent workflows
```

**Workflow:**

1. Agent reads AGOR protocol from your local Sources
2. Agent selects appropriate role for the task
3. Agent works within your local VS Code environment
4. Full codebase context and completions available
5. Manual git operations (agent provides code, you commit)

### AugmentCode Remote Agents

**For AugmentCode Remote Agents running in cloud environments:**

**Setup:**

- Use **Standalone Mode** with direct git access
- **Any role works** - choose based on your workflow needs
- Full multi-agent capabilities available
- Real-time collaboration possible
- Direct commits if agent has commit access, copy-paste fallback otherwise

**Workflow:**

```bash
# Agent executes:
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md
# Agent then works directly with your repositories
```

### Jules by Google

**Setup:**

- Use **Standalone Mode** with direct git access
- **Any role works** - choose based on your workflow needs
- Full multi-agent capabilities available
- Real-time collaboration possible
- Direct commits if agent has commit access, copy-paste fallback otherwise

**Workflow:**

```bash
# Agent executes:
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor
cat src/agor/tools/AGOR_INSTRUCTIONS.md && cat src/agor/tools/README_ai.md
# Agent then works directly with your repositories
```

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

## 🎼 Multi-Agent Coordination Strategies

### When to Use Each Strategy

**🔄 Parallel Divergent** - Multiple independent solutions

- **Use for**: Feature design, architecture decisions, creative problem-solving
- **Roles**: Multiple SOLO DEVELOPER agents working independently
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

- **[Documentation Index](index.md)** - Quick reference for all documentation
- **[Bundle Mode Guide](bundle-mode.md)** - Platform-specific setup instructions
- **[Strategy Guide](strategies.md)** - Detailed multi-agent strategy explanations
- **[Quick Start](quick-start.md)** - Step-by-step getting started guide

---

_This guide evolves with AGOR. Suggest improvements through GitHub issues or the `meta` hotkey._
