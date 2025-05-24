# AgentOrchestrator (AGOR) - Agent Mode Instructions

## Quick Start for AI Agents

**Agent Mode** is for AI agents with git access (Augment Code, Jules by Google, etc.)

### Step 1: Clone AGOR Repository

```bash
# Clone AGOR repository (no installation needed)
git clone https://github.com/jeremiah-k/agor.git
cd agor
```

### Step 2: Learn the Protocol

```bash
# Read the comprehensive AI instructions
cat src/agor/tools/README_ai.md

# This file contains the complete AGOR protocol and capabilities
```

### Step 3: Receive User Instructions

The user will provide:

- Target repository URL or local path
- Specific project goals and requirements
- Any constraints or preferences

### Step 4: Clone Target Project

```bash
# Clone the user's project (in a separate directory)
git clone [USER_SPECIFIED_REPO_URL]
cd [PROJECT_NAME]
```

### Step 5: Initialize AGOR Protocol

```bash
# Configure git identity for any commits
git config --global user.name "AgentOrchestrator"
git config --global user.email "agor@example.local"

# Load AGOR tools from the cloned repository
# Tools are available in ../agor/src/agor/tools/

# Start with comprehensive codebase analysis using 'a' command
```

### Step 6: Begin Orchestration

You now have access to all AgentOrchestrator capabilities:

- Strategic planning and project breakdown
- Multi-agent team design and coordination
- Specialized prompt engineering
- Quality assurance and validation planning
- Risk assessment and mitigation strategies

## Agent Mode vs Bundle Mode

**Agent Mode (This Mode) - For AI Agents with Git Access:**

- **No installation required** - just clone the AGOR repository
- **Direct repository access** - can work with any repository URL
- **No file size limitations** - full repository access
- **Can clone multiple repositories** for complex projects
- **Full git history and branch access**
- **Real-time updates** - can pull latest AGOR improvements
- **For**: Augment Code, Jules by Google, other advanced AI agents

**Bundle Mode - For Upload-Based AI Platforms:**

- **Requires local installation** - user installs AGOR locally
- **File upload workflow** - user bundles project and uploads .tar.gz
- **Works with upload-only platforms** like ChatGPT
- **Self-contained** - everything bundled in one file
- **For**: ChatGPT and other platforms without git access

## Usage Examples

### Example 1: Single Project Analysis

```bash
# Agent clones AGOR repository
git clone https://github.com/jeremiah-k/agor.git
cd agor

# Agent learns the protocol
cat src/agor/tools/README_ai.md

# User provides target project
# Agent clones target project
git clone https://github.com/user/project.git
cd project

# Agent applies AGOR protocol
# Start with 'a' command for codebase analysis
```

### Example 2: Multi-Repository Coordination

```bash
# Agent has AGOR repository cloned
cd agor

# User requests work on multiple related projects
# Agent clones all related repositories
git clone https://github.com/user/frontend.git
git clone https://github.com/user/backend.git
git clone https://github.com/user/shared-lib.git

# Agent coordinates across all repositories using AGOR tools
# Apply strategic planning and team coordination across projects
```

## Integration with AI Platforms

### For AI Agents with Git Access (Augment Code, Jules, etc.):

1. **User provides AGOR repository URL** to the AI agent
2. **Agent clones AGOR repository** and learns the protocol
3. **User specifies target project** and requirements
4. **Agent clones target project** and applies AGOR capabilities
5. **Agent coordinates development** using AGOR tools and frameworks

### For Automated Systems:

1. **Include AGOR as git submodule** in automated workflows
2. **Load instruction set programmatically** from AGOR tools
3. **Use prompt templates and coordination frameworks** for AI orchestration
4. **Integrate with CI/CD pipelines** for automated project coordination

## File Structure Reference

```
agor/
├── AGOR_INSTRUCTIONS.md (this file)
├── README.md (project overview)
├── src/agor/tools/
│   ├── README_ai.md (comprehensive AI instructions)
│   ├── code_exploration.py (analysis tools)
│   ├── agent_prompt_templates.py (prompt generators)
│   ├── project_planning_templates.py (coordination frameworks)
│   └── code_exploration_docs.md (tool documentation)
└── [other project files]
```

## Support and Documentation

- **Full Documentation**: See `src/agor/tools/README_ai.md`
- **Prompt Templates**: See `src/agor/tools/agent_prompt_templates.py`
- **Planning Frameworks**: See `src/agor/tools/project_planning_templates.py`
- **Tool Reference**: See `src/agor/tools/code_exploration_docs.md`

---

## 🙏 Attribution

**AgentOrchestrator is an enhanced fork of the original [AgentGrunt](https://github.com/nikvdp/agentgrunt) created by [@nikvdp](https://github.com/nikvdp).**

---

**Ready to orchestrate? Load the full instructions and begin coordinating your development project!**
