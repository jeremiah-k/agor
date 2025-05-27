# 🗂️ AGOR Documentation Index

**Purpose**: This index is designed for AI models to efficiently locate specific information without token-expensive exploration. Each entry includes the exact file path, key concepts, and specific use cases.

**For AI Models**: This index is designed to minimize token usage while maximizing information retrieval efficiency. Use the "Quick Reference by Need" section to jump directly to relevant documentation without exploration overhead.

## 🎯 Quick Reference by Need

### "I need to get started with AGOR"

- **[docs/agent-start-here.md](agent-start-here.md)** - **START HERE** - Agent entry point with immediate guidance
- **[docs/usage-guide.md](usage-guide.md)** - **COMPREHENSIVE GUIDE** - Complete overview of modes, roles, and workflows
- **[docs/quick-start.md](quick-start.md)** - 5-minute setup guide with platform selection
- **[docs/bundle-mode.md](bundle-mode.md)** - Complete Bundle Mode guide for all platforms
- **[src/agor/tools/BUNDLE_INSTRUCTIONS.md](../src/agor/tools/BUNDLE_INSTRUCTIONS.md)** - Bundle Mode setup for upload platforms

### "I need to check protocol updates or compatibility"

- **[docs/protocol-changelog.md](protocol-changelog.md)** - Protocol version history and compatibility guide
  - Current: Protocol v0.4.0 with snapshot system and standalone mode
  - Breaking changes, new capabilities, and migration notes
  - Reference commits and specific line numbers for changes

### "I need to understand roles and initialization"

- **[src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md)** - Complete AI protocol (563 lines)
  - Lines 18-40: Role selection (SOLO DEVELOPER, PROJECT COORDINATOR, AGENT WORKER)
  - Lines 120-220: Role-specific hotkey menus
  - Lines 450-550: Handoff procedures and meta-development

### "I need multi-agent coordination strategies"

- **[docs/strategies.md](strategies.md)** - 5 coordination strategies with decision matrix
  - Parallel Divergent: Independent exploration → synthesis
  - Pipeline: Sequential handoffs with specialization
  - Swarm: Dynamic task assignment
  - Red Team: Adversarial build/break cycles
  - Mob Programming: Collaborative coding

### "I need to implement/execute a strategy"

- **[src/agor/tools/strategy_protocols.py](../src/agor/tools/strategy_protocols.py)** - Concrete strategy implementation
  - Functions: initialize_parallel_divergent(), initialize_pipeline(), initialize_swarm()
  - Creates: .agor/strategy-active.md, agent memory files, task queues
  - Provides: Step-by-step execution protocols, automatic phase transitions
- **[src/agor/tools/agent_coordination.py](../src/agor/tools/agent_coordination.py)** - Agent role discovery
  - Functions: discover_my_role(), check_strategy_status()
  - Provides: Concrete next actions, role assignment, current status
- **[docs/coordination-example.md](coordination-example.md)** - Complete implementation example
  - Shows: Before/after coordination, concrete usage, file structure

### "I need to create or use a work snapshot"

- **[docs/snapshots.md](snapshots.md)** - Comprehensive system for snapshots (for multi-agent and solo context management)
- **[src/agor/tools/handoff_templates.py](../src/agor/tools/handoff_templates.py)** - Handoff generation code
  - Functions: generate_handoff_document(), get_git_context(), get_agor_version()
  - Captures: problem, progress, commits, files, next steps, git state, AGOR version

### "I need to analyze code or explore the codebase"

- **[src/agor/tools/code_exploration.py](../src/agor/tools/code_exploration.py)** - Analysis tools implementation
- **[src/agor/tools/code_exploration_docs.md](../src/agor/tools/code_exploration_docs.md)** - Tool documentation
  - Functions: bfs_find(), grep(), tree(), find_function_signatures(), extract_function_content()

### "I need database-based memory management"

- **[src/agor/tools/sqlite_memory.py](../src/agor/tools/sqlite_memory.py)** - SQLite memory system (experimental)
- **[src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md)** Lines 590-662 - SQLite mode documentation
- **[src/agor/tools/BUNDLE_INSTRUCTIONS.md](../src/agor/tools/BUNDLE_INSTRUCTIONS.md)** Lines 142-198 - SQLite bundling

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

| File                                                       | Purpose                                    | Key Sections                                    | Lines |
| ---------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------- | ----- |
| **[README.md](README.md)**                                 | Documentation overview                     | Navigation map, quick links                     | 60    |
| **[agent-start-here.md](agent-start-here.md)**             | **Agent entry point**                      | **Immediate guidance, discovery commands**      | ~100  |
| **[quick-start.md](quick-start.md)**                       | 5-minute setup guide                       | Installation, bundling, platform setup          | ~200  |
| **[bundle-mode.md](bundle-mode.md)**                       | Complete Bundle Mode guide                 | All platforms, models, troubleshooting          | ~300  |
| **[google-ai-studio.md](google-ai-studio.md)**             | Google AI Studio guide                     | Function Calling setup, troubleshooting         | ~300  |
| **[standalone-mode.md](standalone-mode.md)**               | Standalone Mode Guide                      | Setup, usage, advantages of direct git access   | ~250  |
| **[strategies.md](strategies.md)**                         | Multi-agent coordination                   | 5 strategies with examples, decision matrix     | ~400  |
| **[snapshots.md](snapshots.md)**                           | Agent state snapshots & context management | Snapshot creation, receiving, solo use benefits | ~550+ |
| **[coordination-example.md](coordination-example.md)**     | Strategy implementation                    | Complete example, before/after comparison       | ~300  |
| **[agor-development-guide.md](agor-development-guide.md)** | Development checklist                      | For agents working on AGOR itself               | ~400  |

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
| **[sqlite_memory.py](../src/agor/tools/sqlite_memory.py)**                           | SQLite memory (exp) | SQLiteMemoryManager, database operations     | ~400  |
| **[agent_prompt_templates.py](../src/agor/tools/agent_prompt_templates.py)**         | Role prompts        | Specialized agent prompts                    | ~200  |
| **[project_planning_templates.py](../src/agor/tools/project_planning_templates.py)** | Planning frameworks | Strategy templates                           | ~300  |
| **[strategy_protocols.py](../src/agor/tools/strategy_protocols.py)**                 | Strategy execution  | Concrete implementation protocols            | ~600  |
| **[agent_coordination.py](../src/agor/tools/agent_coordination.py)**                 | Agent coordination  | Role discovery, status checking              | ~400  |

## 🔍 Search by Concept

### Git Operations

- **Real git binary usage**: [src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md) Lines 5-14
- **Git context capture**: [src/agor/tools/handoff_templates.py](../src/agor/tools/handoff_templates.py) get_git_context()
- **Repository analysis**: [src/agor/tools/README_ai.md](../src/agor/tools/README_ai.md) Lines 103-120

### Role-Based Workflows

- **PROJECT COORDINATOR**: Strategic planning, team coordination, strategy selection
- **SOLO DEVELOPER**: Codebase analysis, implementation, technical deep-dives
- **AGENT WORKER**: Task execution, handoffs, coordination communication

### Platform-Specific Information

- **Bundle Mode**: [docs/bundle-mode.md](bundle-mode.md) - All platforms, models, formats
- **Google AI Studio**: Gemini 2.5 Pro, Function Calling, .zip format
- **ChatGPT**: GPT-4o, subscription required, .tar.gz format
- **Standalone Mode**: [docs/standalone-mode.md](standalone-mode.md) - Direct git access workflows

### Coordination Protocols

- **Communication**: .agor/agentconvo.md format and usage
- **Memory**: .agor/memory.md and agent-specific files
- **SQLite Memory**: .agor/memory.db database-based storage (experimental)
- **Snapshots**: Capturing work state with git context (also for solo context preservation)
- **Strategies**: 5 multi-agent patterns with implementation details
- **Strategy Implementation**: Concrete execution protocols (strategy_protocols.py)
- **Agent Discovery**: Role assignment and next actions (agent_coordination.py)
- **State Management**: .agor/strategy-active.md, task queues, phase transitions

## 🎯 Token-Efficient Lookup Patterns

### For Quick Commands

```
Need hotkey? → README_ai.md Lines 120-220
Need strategy? → strategies.md decision matrix
Need snapshot? → snapshots.md or snapshot_templates.py
```

### For Implementation Details

```
Code analysis? → code_exploration.py + code_exploration_docs.md
Prompt templates? → agent_prompt_templates.py
Planning frameworks? → project_planning_templates.py
Strategy execution? → strategy_protocols.py + coordination-example.md
Agent coordination? → agent_coordination.py + README_ai.md Lines 318-322
```

### For Setup and Troubleshooting

```
First time? → quick-start.md
Bundle Mode? → bundle-mode.md
Standalone Mode? → docs/standalone-mode.md
Platform-specific? → bundle-mode.md platform sections
```

## 📊 Documentation Status

### ✅ Complete and Current

- Core AI instructions (README_ai.md)
- Quick start guide
- Bundle Mode guide (all platforms)
- Google AI Studio guide
- Multi-agent strategies
- Snapshot system
- Code exploration tools
- AGOR development guide
- Standalone mode guide (standalone-mode.md)

### 📝 Referenced but Not Yet Created

- First coordination walkthrough (first-coordination.md)
- Role deep-dive (roles.md)
- Coordination protocol (coordination.md)
- Feedback system guide (feedback.md)
- Troubleshooting guide (troubleshooting.md)
- Contributing guide (contributing.md)
- Hotkey reference (hotkeys.md)
- Configuration guide (configuration.md)
- API reference (api.md)

---
