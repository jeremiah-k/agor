# 🗂️ AGOR Documentation Index

**Purpose**: This index is designed for AI models to efficiently locate specific information without token-expensive exploration. Each entry includes the exact file path, key concepts, and specific use cases.

## 🎯 Quick Reference by Need

### "I need to get started with AGOR"

- **[docs/quick-start.md](quick-start.md)** - 5-minute setup guide with platform selection
- **[docs/google-ai-studio.md](google-ai-studio.md)** - Google AI Studio setup (Function Calling required)
- **[src/agor/tools/BUNDLE_INSTRUCTIONS.md](../src/agor/tools/BUNDLE_INSTRUCTIONS.md)** - Bundle Mode setup for upload platforms

### "I need to understand roles and initialization"

- **[src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md)** - Complete AI protocol (563 lines)
  - Lines 18-40: Role selection (PROJECT COORDINATOR, ANALYST/SOLO DEV, AGENT WORKER)
  - Lines 120-220: Role-specific hotkey menus
  - Lines 450-550: Handoff procedures and meta-development

### "I need multi-agent coordination strategies"

- **[docs/strategies.md](strategies.md)** - 5 coordination strategies with decision matrix
  - Parallel Divergent: Independent exploration → synthesis
  - Pipeline: Sequential handoffs with specialization
  - Swarm: Dynamic task assignment
  - Red Team: Adversarial build/break cycles
  - Mob Programming: Collaborative coding

### "I need to hand off work to another agent"

- **[docs/handoffs.md](handoffs.md)** - Comprehensive handoff system
- **[src/agor/tools/handoff_templates.py](../src/agor/tools/handoff_templates.py)** - Handoff generation code
  - Functions: generate_handoff_document(), get_git_context(), get_agor_version()
  - Captures: problem, progress, commits, files, next steps, git state, AGOR version

### "I need to analyze code or explore the codebase"

- **[src/agor/tools/code_exploration.py](../src/agor/tools/code_exploration.py)** - Analysis tools implementation
- **[src/agor/tools/code_exploration_docs.md](../src/agor/tools/code_exploration_docs.md)** - Tool documentation
  - Functions: bfs_find(), grep(), tree(), find_function_signatures(), extract_function_content()

### "I need hotkey commands reference"

- **[src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md)** Lines 120-220 - Role-specific menus
  - PROJECT COORDINATOR: sp, bp, ar, ss, pd, pl, sw, rt, mb, ct, tm, hp
  - ANALYST/SOLO DEV: a, f, co, da, bfs, grep, tree, edit, commit, diff
  - AGENT WORKER: status, sync, ch, log, msg, report, task, complete, handoff

### "I need to provide feedback on AGOR"

- **[src/agor/tools/agor-meta.md](../src/agor/tools/agor-meta.md)** - Feedback system and templates
- **[src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md)** Lines 450-485 - Meta-development procedures

### "I need prompt templates for coordination"

- **[src/agor/tools/agent_prompt_templates.py](../src/agor/tools/agent_prompt_templates.py)** - Agent role prompts
- **[src/agor/tools/project_planning_templates.py](../src/agor/tools/project_planning_templates.py)** - Planning frameworks

## 📁 Complete File Inventory

### Core Documentation (docs/)

| File                                           | Purpose                  | Key Sections                                | Lines |
| ---------------------------------------------- | ------------------------ | ------------------------------------------- | ----- |
| **[README.md](README.md)**                     | Documentation overview   | Navigation map, quick links                 | 51    |
| **[quick-start.md](quick-start.md)**           | 5-minute setup guide     | Installation, bundling, platform setup      | ~200  |
| **[google-ai-studio.md](google-ai-studio.md)** | Google AI Studio guide   | Function Calling setup, troubleshooting     | ~300  |
| **[strategies.md](strategies.md)**             | Multi-agent coordination | 5 strategies with examples, decision matrix | ~400  |
| **[handoffs.md](handoffs.md)**                 | Agent transition system  | Handoff creation, receiving, best practices | ~500  |

### AI Instructions (src/agor/tools/)

| File                                                                   | Purpose              | Key Sections                         | Lines |
| ---------------------------------------------------------------------- | -------------------- | ------------------------------------ | ----- |
| **[README_ai.md](../src/agor/tools/README_ai.md)**                     | Complete AI protocol | Role selection, hotkeys, procedures  | 563   |
| **[AGOR_INSTRUCTIONS.md](../src/agor/tools/AGOR_INSTRUCTIONS.md)**     | Agent Mode setup     | Git clone workflow, initialization   | ~180  |
| **[BUNDLE_INSTRUCTIONS.md](../src/agor/tools/BUNDLE_INSTRUCTIONS.md)** | Bundle Mode setup    | Upload workflow, platform comparison | ~150  |
| **[agor-meta.md](../src/agor/tools/agor-meta.md)**                     | Feedback system      | Feedback pathways, templates         | ~200  |

### Technical Tools (src/agor/tools/)

| File                                                                                 | Purpose             | Key Functions                                | Lines |
| ------------------------------------------------------------------------------------ | ------------------- | -------------------------------------------- | ----- |
| **[code_exploration.py](../src/agor/tools/code_exploration.py)**                     | Codebase analysis   | bfs_find, grep, tree, analyze_file_structure | ~300  |
| **[code_exploration_docs.md](../src/agor/tools/code_exploration_docs.md)**           | Tool documentation  | Function reference, examples                 | 179   |
| **[handoff_templates.py](../src/agor/tools/handoff_templates.py)**                   | Handoff generation  | generate_handoff_document, git_context       | ~400  |
| **[agent_prompt_templates.py](../src/agor/tools/agent_prompt_templates.py)**         | Role prompts        | Specialized agent prompts                    | ~200  |
| **[project_planning_templates.py](../src/agor/tools/project_planning_templates.py)** | Planning frameworks | Strategy templates                           | ~300  |

## 🔍 Search by Concept

### Git Operations

- **Real git binary usage**: [src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md) Lines 5-14
- **Git context capture**: [src/agor/tools/handoff_templates.py](../src/agor/tools/handoff_templates.py) get_git_context()
- **Repository analysis**: [src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md) Lines 103-120

### Role-Based Workflows

- **PROJECT COORDINATOR**: Strategic planning, team coordination, strategy selection
- **ANALYST/SOLO DEV**: Codebase analysis, implementation, technical deep-dives
- **AGENT WORKER**: Task execution, handoffs, coordination communication

### Platform-Specific Information

- **Google AI Studio**: [docs/google-ai-studio.md](google-ai-studio.md) - Function Calling, .zip format
- **ChatGPT**: [src/agor/tools/BUNDLE_INSTRUCTIONS.md](../src/agor/tools/BUNDLE_INSTRUCTIONS.md) - .tar.gz format
- **Agent Mode**: [src/agor/tools/AGOR_INSTRUCTIONS.md](../src/agor/tools/AGOR_INSTRUCTIONS.md) - Direct git access

### Coordination Protocols

- **Communication**: .agor/agentconvo.md format and usage
- **Memory**: .agor/memory.md and agent-specific files
- **Handoffs**: Complete transition procedures with git state
- **Strategies**: 5 multi-agent patterns with implementation details

## 🎯 Token-Efficient Lookup Patterns

### For Quick Commands

```
Need hotkey? → README_ai.md Lines 120-220
Need strategy? → strategies.md decision matrix
Need handoff? → handoffs.md or handoff_templates.py
```

### For Implementation Details

```
Code analysis? → code_exploration.py + code_exploration_docs.md
Prompt templates? → agent_prompt_templates.py
Planning frameworks? → project_planning_templates.py
```

### For Setup and Troubleshooting

```
First time? → quick-start.md
Google AI Studio? → google-ai-studio.md
Bundle Mode? → BUNDLE_INSTRUCTIONS.md
Agent Mode? → AGOR_INSTRUCTIONS.md
```

## 📊 Documentation Status

### ✅ Complete and Current

- Core AI instructions (README_ai.md)
- Quick start guide
- Google AI Studio guide
- Multi-agent strategies
- Handoff system
- Code exploration tools

### 📝 Referenced but Not Yet Created

- Platform setup guide (platform-setup.md)
- First coordination walkthrough (first-coordination.md)
- Role deep-dive (roles.md)
- Coordination protocol (coordination.md)
- ChatGPT guide (chatgpt.md)
- Agent mode guide (agent-mode.md)
- Feedback system guide (feedback.md)
- Troubleshooting guide (troubleshooting.md)
- Contributing guide (contributing.md)
- Hotkey reference (hotkeys.md)
- Configuration guide (configuration.md)
- API reference (api.md)

---

**For AI Models**: This index is designed to minimize token usage while maximizing information retrieval efficiency. Use the "Quick Reference by Need" section to jump directly to relevant documentation without exploration overhead.
