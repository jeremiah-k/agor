# 🚀 Quick Start Guide

Get AGOR running in 5 minutes and experience the power of coordinated AI development.

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:

- ✅ AGOR installed and working
- ✅ Your first project bundled
- ✅ An AI agent coordinating your development workflow
- ✅ Understanding of the core concepts

## 🛠️ Prerequisites

- **Python 3.10+** installed
- **A development project** you want to coordinate
- **AI platform access** (Google AI Studio recommended)

## 📦 Step 1: Install AGOR

```bash
# Install AGOR (recommended method)
pipx install agor

# Verify installation
agor --version
# Should output: agor, version 0.4.1
```

**Don't have pipx?** Install it first: `pip install pipx`

## 🎁 Step 2: Bundle Your Project

```bash
# Navigate to your project
cd /path/to/your/project

# Bundle for Google AI Studio
agor bundle . -f zip

# Or bundle for ChatGPT
agor bundle .



# AGOR creates: your-project-agor-bundle.zip (or .tar.gz)
```

**What just happened?**

- AGOR analyzed your project structure
- Packaged your code with git history
- Included a portable git binary
- Generated AI instructions
- Created an upload-ready bundle

## 🤖 Step 3: Choose Your AI Platform

### Option A: Google AI Studio

1. **Visit [Google AI Studio](https://aistudio.google.com/)**
2. **Create new chat** and **enable Function Calling** ⚠️
3. **Upload your .zip bundle**
4. **Copy-paste the generated prompt**

### Option B: ChatGPT (Subscription)

1. **Open ChatGPT**
2. **Upload your .tar.gz bundle**
3. **Copy-paste the generated prompt**

### Option C: Standalone Mode (Direct Git Access)

This mode is for AI agents that can directly clone Git repositories and execute shell commands (e.g., Jules by Google, Augment Code Remote Agents). The agent first learns the AGOR protocol:

```bash
# For AI agents with direct Git access (e.g., Jules by Google, Augment Code)
# Agent typically executes these commands to understand AGOR protocol:
cd /tmp && git clone https://github.com/jeremiah-k/agor.git && cd agor
cat src/agor/tools/README_ai.md && cat src/agor/tools/AGOR_INSTRUCTIONS.md
# Then, the agent would clone and work on your project repository.
```

## 🎭 Step 4: Select Your Role

AGOR will ask you to choose a role. Pick based on what you want to do:

### 📋 PROJECT COORDINATOR

**"I want to plan and coordinate development"**

- Strategic planning and project breakdown
- Team design and workflow orchestration
- Multi-agent strategy selection

### 🔍 SOLO DEVELOPER

**"I want to analyze and work with code"**

- Deep codebase analysis and exploration
- Implementation and debugging
- Technical deep-dives

### 🤖 AGENT WORKER

**"I'm following instructions from a coordinator"**

- Task execution and work snapshots
- Coordination communication
- Status reporting

## 🎼 Step 5: Start Coordinating

Once initialized, you'll see a hotkey menu. Try these commands:

```
# Analyze your codebase
a

# Strategic planning
sp

# Break down project
bp

# Get help anytime
?
```

## 🎯 Your First Workflow

Let's walk through a typical coordination session:

### Planning Phase (PROJECT COORDINATOR)

```
1. Type: sp
   → AGOR analyzes your project and creates strategic plan

2. Type: bp
   → Breaks down project into coordinated tasks

3. Type: ss
   → Suggests coordination strategies (Parallel, Pipeline, Swarm, etc.)

4. Type: ct
   → Designs team structure with specialized agents
```

### Implementation Phase (SOLO DEVELOPER)

```
1. Type: a
   → Comprehensive codebase analysis

2. Type: f src/main.py
   → Examine specific files

3. Type: grep "function_name"
   → Search across codebase

4. Type: da
   → Generate detailed snapshot for other agents
```

## 💡 Pro Tips

### Make It Executable (Google AI Studio)

If you see command simulation instead of execution:

```
chmod 755 /tmp/agor_tools/git
/tmp/agor_tools/git status
```

### Switch Roles Mid-Session

You can change roles by re-initializing:

```
# Upload fresh bundle
# Select different role
# Continue with new capabilities
```

### Provide Feedback

Use the `meta` hotkey to help improve AGOR:

```
meta
→ Report issues, suggest improvements, share success stories
```

### Memory Synchronization

AGOR automatically manages memory persistence using git branches:

```bash
# Memory is automatically synced to dedicated branches
# No manual setup required - works out of the box
# Use standard memory commands:
mem-add    # Add memory entries
mem-search # Search across all memories
```

## 🔄 What's Next?

Now that you have AGOR running, explore these advanced topics:

- **[Bundle Mode Guide](bundle-mode.md)** - Complete platform setup and optimization
- **[Multi-Agent Strategies](strategies.md)** - Learn coordination patterns
- **[Agent Snapshots](snapshots.md)** - Master agent transitions and context management
- **[Complete AI Protocol](../src/agor/tools/README_ai.md)** - Comprehensive instructions

## 🆘 Need Help?

**Something not working?**

- Use the `meta` hotkey to report issues
- Visit [GitHub Issues](https://github.com/jeremiah-k/agor/issues)
- Check [Bundle Mode Guide](bundle-mode.md) for platform-specific help

**Want to understand more?**

- Read [Complete AI Protocol](../src/agor/tools/README_ai.md)
- Explore [Agent Snapshots](snapshots.md)
- Try [Advanced Strategies](strategies.md)

---

**Congratulations!** 🎉 You've just set up your first AI coordination workflow. Welcome to the future of development!

_Ready to dive deeper? Check out the [Multi-Agent Strategies](strategies.md) to see what's possible._ 🚀
