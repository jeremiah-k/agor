# AgentOrchestrator (AGOR) - Bundle Mode Instructions

## Bundle Mode for ChatGPT Upload

**Bundle Mode** is for AI platforms that work with file uploads (currently ChatGPT).

### Step 1: Install AGOR Locally

```bash
# Install using pipx (recommended)
pipx install agor

# Or using pip
pip install agor
```

### Step 2: Bundle Your Project

```bash
# Bundle all branches (default, creates .tar.gz)
agor bundle /path/to/your/project

# Bundle with .zip format (for Google AI Studio)
agor bundle /path/to/your/project -f zip

# Bundle only main/master branch
agor bundle /path/to/your/project -m

# Bundle main/master + specific branches
agor bundle /path/to/your/project -b feature1,feature2

# Bundle with SQLite memory support (experimental)
agor bundle /path/to/your/project --sqlite
```

### Step 3: Upload to AI Platform

1. **Upload the bundle file** to your chosen AI platform:
   - **Google AI Studio**: Upload the .zip file (Pro models available)
   - **ChatGPT**: Upload the .tar.gz file (requires subscription)
   - **Other platforms**: Use appropriate format
2. **Copy and paste the prompt** that AGOR generated
3. **The AI will extract** the bundle and initialize AGOR protocol

### Step 4: Select Your Role

The AI will ask you to choose your primary role:

**a) 📋 PROJECT COORDINATOR** - Plan and coordinate multi-agent development

- Focus on strategic planning and team coordination
- Emphasizes planning tools and multi-agent strategies
- Best for: Project planning, team design, workflow orchestration

**b) 🔍 ANALYST/SOLO DEV** - Analyze, edit, and answer questions about the codebase

- Focus on detailed codebase analysis and direct code work
- Emphasizes code exploration tools and editing capabilities
- Best for: Code review, debugging, implementation, technical analysis, solo development

**c) 🤖 AGENT WORKER** - Ready to receive specific tasks from project coordinator

- Minimal initialization, waits for coordinator instructions
- Focus on executing specific tasks and coordination
- Best for: Specialized development tasks, following coordinator plans

### Step 5: Begin Work

Based on your role selection, the AI will initialize with:

- Your complete project codebase
- Role-appropriate AGOR tools and hotkeys
- Coordination and communication capabilities
- Strategic planning frameworks (if coordinator)

## Bundle Mode vs Agent Mode

**Bundle Mode (This Mode) - For Upload-Based AI Platforms:**

- **Requires local installation** - user installs AGOR locally
- **File upload workflow** - user bundles project and uploads archive
- **Multiple format support** - .zip for Google AI Studio, .tar.gz for ChatGPT
- **Self-contained** - everything bundled in one file including portable git binary
- **✅ Successfully tested with**:
  - **Google AI Studio Pro models** (Function Calling enabled, use .zip)
  - **ChatGPT** (requires subscription, use .tar.gz)
  - **Claude** and other platforms that accept file uploads

**Agent Mode - For AI Agents with Direct Git Access:**

- **No installation required** - just clone the AGOR repository
- **Direct repository access** - can work with any repository URL
- **No file size limitations** - full repository access
- **Real-time updates** - can pull latest AGOR improvements
- **For**: Augment Code, Jules by Google, other advanced AI agents

## Bundle Contents

When you create a bundle, AGOR includes:

1. **Your project files** with git history and branch information
2. **AGOR tools** - All coordination and analysis tools
3. **Git binary** - Portable git for ChatGPT environment
4. **AI instructions** - Complete protocol for ChatGPT to follow

## Troubleshooting

### Large Repository Issues

If your repository is very large:

```bash
# Bundle only main branch to reduce size
agor bundle /path/to/your/project -m

# Or bundle specific branches only
agor bundle /path/to/your/project -b main,develop
```

### Upload Limits

- ChatGPT has file size limits for uploads
- Use branch selection to reduce bundle size
- Consider using Agent Mode for very large projects

## Example Workflow

```bash
# 1. Install AGOR
pipx install agor

# 2. Bundle your project
agor bundle ~/my-project

# 3. Upload my-project.tar.gz to ChatGPT

# 4. Paste the generated prompt

# 5. ChatGPT becomes AgentOrchestrator and analyzes your project
```

## 🗄️ SQLite Memory Mode (Experimental)

AGOR can include a portable SQLite binary for database-based memory management instead of markdown files. This provides structured storage and advanced querying capabilities.

### Enabling SQLite Mode

```bash
# Bundle with SQLite support
agor bundle /path/to/your/project --sqlite

# Or combine with other options
agor bundle /path/to/your/project -f zip --sqlite
```

### SQLite Features

**Structured Memory Storage**:

- Agent memories with types (context, decision, learning, handoff)
- Cross-agent coordination logs
- Project state management
- Advanced handoff tracking with relational data

**Database Schema**:

- `agent_memories` - Individual agent memory entries
- `coordination_logs` - Cross-agent communication
- `project_state` - Key-value project state storage
- `handoffs` - Structured handoff records

**Memory Commands Available**:

- `mem-add`, `mem-get`, `mem-search` - Memory management
- `coord-log`, `state-set`, `state-get` - Coordination and state
- `handoff-create`, `handoff-status` - Database handoffs
- `db-stats` - Database statistics

### Important Notes

⚠️ **Experimental Feature**: SQLite memory mode is experimental and not fully tested.

- **Database Location**: `.agor/memory.db` in your project
- **Fallback**: Falls back to markdown files if SQLite is unavailable
- **Compatibility**: All operations are backwards compatible with file-based mode
- **Binary Source**: SQLite binary from [1bin project](https://github.com/nikvdp/1bin)

### When to Use SQLite Mode

**Use SQLite Mode When**:

- Working with multiple agents that need shared memory
- Requiring structured queries across agent memories
- Managing complex coordination workflows
- Needing persistent state across sessions

**Stick with Markdown When**:

- Working solo or with simple coordination
- Preferring human-readable memory files
- Avoiding experimental features
- Working in environments where SQLite might not be available

---

## 🙏 Attribution

**AgentOrchestrator is an enhanced fork of the original [AgentGrunt](https://github.com/nikvdp/agentgrunt) created by [@nikvdp](https://github.com/nikvdp).**

---

**Ready to bundle your project? Install AGOR and create your first bundle!**
