# 🗂️ AGOR Documentation Index

**Purpose**: This index is designed for AI models to efficiently locate specific information without token-expensive exploration. Each entry includes the exact file path, key concepts, and specific use cases.

**For AI Models**: This index is designed to minimize token usage while maximizing information retrieval efficiency. Use the "Quick Reference by Need" section to jump directly to relevant documentation without exploration overhead.

## 🎯 Quick Reference by Need

### "I need to get started with AGOR"

- **[agent-start-here.md](agent-start-here.md)** - **START HERE** - Agent entry point with immediate guidance
- **[session-startup-checklist.md](session-startup-checklist.md)** - **ESSENTIAL** - Checklist for every agent session
- **[docs/usage-guide.md](../../../docs/usage-guide.md)** - **COMPREHENSIVE GUIDE** - Complete overview of modes, roles, and workflows
- **[docs/quick-start.md](../../../docs/quick-start.md)** - 5-minute setup guide with platform selection
- **[docs/bundle-mode.md](../../../docs/bundle-mode.md)** - Complete Bundle Mode guide for all platforms
- **[BUNDLE_INSTRUCTIONS.md](BUNDLE_INSTRUCTIONS.md)** - Bundle Mode setup for upload platforms

### "I need Augment Code integration"

- **[AUGMENT_INITIALIZATION.md](AUGMENT_INITIALIZATION.md)** - Local Augment setup and integration
- **[CHAINABLE_PROMPTS.md](CHAINABLE_PROMPTS.md)** - Token-efficient initialization prompts

### "I need to check protocol updates or compatibility"

- **[docs/protocol-changelog.md](../../../docs/protocol-changelog.md)** - Protocol version history and compatibility guide
  - Current: Protocol v0.4.0 with snapshot system and standalone mode
  - Breaking changes, new capabilities, and migration notes
  - Reference commits and specific line numbers for changes

### "I need to understand roles and initialization"

- **[README_ai.md](README_ai.md)** - Complete AI protocol (563 lines)
  - Lines 18-40: Role selection (SOLO DEVELOPER, PROJECT COORDINATOR, AGENT WORKER)
  - Lines 120-220: Role-specific hotkey menus
  - Lines 450-550: Snapshot procedures and meta-development

### "I need multi-agent coordination strategies"

- **[docs/strategies.md](../../../docs/strategies.md)** - 5 coordination strategies with decision matrix
  - Parallel Divergent: Independent exploration → synthesis
  - Pipeline: Sequential snapshots with specialization
  - Swarm: Dynamic task assignment
  - Red Team: Adversarial build/break cycles
  - Mob Programming: Collaborative coding

### "I need to implement/execute a strategy"

- **[strategy_protocols.py](strategy_protocols.py)** - Concrete strategy implementation
  - Functions: initialize_parallel_divergent(), initialize_pipeline(), initialize_swarm()
  - Creates: .agor/strategy-active.md, agent memory files, task queues
  - Provides: Step-by-step execution protocols, automatic phase transitions
- **[agent_coordination.py](agent_coordination.py)** - Agent role discovery
  - Functions: discover_my_role(), check_strategy_status()
  - Provides: Concrete next actions, role assignment, current status
- **[coordination-example.md](coordination-example.md)** - Complete implementation example
  - Shows: Before/after coordination, concrete usage, file structure

### "I need to create or use a work snapshot"

- **[SNAPSHOT_SYSTEM_GUIDE.md](SNAPSHOT_SYSTEM_GUIDE.md)** - Essential guide for all agents (MANDATORY reading)
- **[docs/snapshots.md](../../../docs/snapshots.md)** - Comprehensive system for snapshots (for multi-agent and solo context management)
- **[snapshot_templates.py](snapshot_templates.py)** - Snapshot generation code
  - Functions: generate_snapshot_document(), get_git_context(), get_agor_version()
  - Captures: problem, progress, commits, files, next steps, git state, AGOR version

### "I need to analyze code or explore the codebase"

- **[code_exploration.py](code_exploration.py)** - Analysis tools implementation
- **[code_exploration_docs.md](code_exploration_docs.md)** - Tool documentation
  - Functions: bfs_find(), grep(), tree(), find_function_signatures(), extract_function_content()

### "I need memory management"

- **[../memory_sync.py](../memory_sync.py)** - Memory synchronization system
- **[README_ai.md](README_ai.md)** Lines 590-662 - Memory system documentation

### "I need hotkey commands reference"

- **[README_ai.md](README_ai.md)** Lines 120-220 - Role-specific menus
  - PROJECT COORDINATOR: sp, bp, ar, ss, pd, pl, sw, rt, mb, ct, tm, hp
  - ANALYST/SOLO DEV: a, f, co, da, bfs, grep, tree, edit, commit, diff
  - AGENT WORKER: status, sync, ch, log, msg, report, task, complete, snapshot

### "I need to provide feedback on AGOR"

- **[agor-meta.md](agor-meta.md)** - Feedback system and templates
- **[README_ai.md](README_ai.md)** Lines 450-485 - Meta-development procedures

### "I need prompt templates for coordination"

- **[agent_prompt_templates.py](agent_prompt_templates.py)** - Agent role prompts
- **[project_planning_templates.py](project_planning_templates.py)** - Planning frameworks

## 📁 Complete File Inventory

### Core Documentation (docs/)

| File                                                                                   | Purpose                                    | Key Sections                                    | Lines |
| -------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------- | ----- |
| **[../../../docs/README.md](../../../docs/README.md)**                                 | Documentation overview                     | Navigation map, quick links                     | 60    |
| **[agent-start-here.md](agent-start-here.md)**                                         | **Agent entry point**                      | **Immediate guidance, discovery commands**      | ~100  |
| **[../../../docs/quick-start.md](../../../docs/quick-start.md)**                       | 5-minute setup guide                       | Installation, bundling, platform setup          | ~200  |
| **[../../../docs/bundle-mode.md](../../../docs/bundle-mode.md)**                       | Complete Bundle Mode guide                 | All platforms, models, troubleshooting          | ~300  |
| **[../../../docs/google-ai-studio.md](../../../docs/google-ai-studio.md)**             | Google AI Studio guide                     | Function Calling setup, troubleshooting         | ~300  |
| **[../../../docs/standalone-mode.md](../../../docs/standalone-mode.md)**               | Standalone Mode Guide                      | Setup, usage, advantages of direct git access   | ~250  |
| **[../../../docs/strategies.md](../../../docs/strategies.md)**                         | Multi-agent coordination                   | 5 strategies with examples, decision matrix     | ~400  |
| **[../../../docs/snapshots.md](../../../docs/snapshots.md)**                           | Agent state snapshots & context management | Snapshot creation, receiving, solo use benefits | ~550+ |
| **[coordination-example.md](coordination-example.md)**                                 | Strategy implementation                    | Complete example, before/after comparison       | ~300  |
| **[../../../docs/agor-development-guide.md](../../../docs/agor-development-guide.md)** | Development checklist                      | For agents working on AGOR itself               | ~400  |

### AI Instructions (src/agor/tools/)

| File                                                 | Purpose              | Key Sections                         | Lines |
| ---------------------------------------------------- | -------------------- | ------------------------------------ | ----- |
| **[README_ai.md](README_ai.md)**                     | Complete AI protocol | Role selection, hotkeys, procedures  | 563   |
| **[AGOR_INSTRUCTIONS.md](AGOR_INSTRUCTIONS.md)**     | Agent Mode setup     | Git clone workflow, initialization   | ~180  |
| **[BUNDLE_INSTRUCTIONS.md](BUNDLE_INSTRUCTIONS.md)** | Bundle Mode setup    | Upload workflow, platform comparison | ~150  |
| **[agor-meta.md](agor-meta.md)**                     | Feedback system      | Feedback pathways, templates         | ~200  |

### Technical Tools (src/agor/tools/)

| File                                                     | Purpose             | Key Functions                                | Lines |
| -------------------------------------------------------- | ------------------- | -------------------------------------------- | ----- |
| **[code_exploration.py](code_exploration.py)**           | Codebase analysis   | bfs_find, grep, tree, analyze_file_structure | ~300  |
| **[code_exploration_docs.md](code_exploration_docs.md)** | Tool documentation  | Function reference, examples                 | 179   |
| **[snapshot_templates.py](snapshot_templates.py)**       | Snapshot generation | generate_snapshot_document, git_context      | ~400  |

| **[agent_prompt_templates.py](agent_prompt_templates.py)** | Role prompts | Specialized agent prompts | ~200 |
| **[project_planning_templates.py](project_planning_templates.py)** | Planning frameworks | Strategy templates | ~300 |
| **[strategy_protocols.py](strategy_protocols.py)** | Strategy execution | Concrete implementation protocols | ~600 |
| **[agent_coordination.py](agent_coordination.py)** | Agent coordination | Role discovery, status checking | ~400 |
| **[AUGMENT_INITIALIZATION.md](AUGMENT_INITIALIZATION.md)** | Augment integration | Local setup, initialization prompts | ~150 |
| **[CHAINABLE_PROMPTS.md](CHAINABLE_PROMPTS.md)** | Token efficiency | Chainable initialization prompts | ~200 |

## 🔍 Search by Concept

### Git Operations

- **Real git binary usage**: [README_ai.md](README_ai.md) Lines 5-14
- **Git context capture**: [snapshot_templates.py](snapshot_templates.py) get_git_context()
- **Repository analysis**: [README_ai.md](README_ai.md) Lines 103-120

### Role-Based Workflows

- **PROJECT COORDINATOR**: Strategic planning, team coordination, strategy selection
- **SOLO DEVELOPER**: Codebase analysis, implementation, technical deep-dives
- **AGENT WORKER**: Task execution, snapshots, coordination communication

### Platform-Specific Information

- **Bundle Mode**: [docs/bundle-mode.md](../../../docs/bundle-mode.md) - All platforms, models, formats
- **Google AI Studio**: Gemini 2.5 Pro, Function Calling, .zip format
- **ChatGPT**: GPT-4o, subscription required, .tar.gz format
- **Standalone Mode**: [docs/standalone-mode.md](../../../docs/standalone-mode.md) - Direct git access workflows

### Coordination Protocols

- **Communication**: .agor/agentconvo.md format and usage
- **Memory**: .agor/memory.md and agent-specific files
- **Memory Synchronization**: .agor/memory.md with git branch synchronization
- **Snapshots**: Capturing work state with git context (also for solo context preservation)
- **Strategies**: 5 multi-agent patterns with implementation details
- **Strategy Implementation**: Concrete execution protocols (strategy_protocols.py)
- **Agent Discovery**: Role assignment and next actions (agent_coordination.py)
- **State Management**: .agor/strategy-active.md, task queues, phase transitions

## 🎯 Token-Efficient Lookup Patterns

### For Quick Commands

```
Need hotkey? → README_ai.md Lines 120-220
Need strategy? → ../../../docs/strategies.md decision matrix
Need snapshot? → ../../../docs/snapshots.md or snapshot_templates.py
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
First time? → ../../../docs/quick-start.md
Bundle Mode? → ../../../docs/bundle-mode.md
Standalone Mode? → ../../../docs/standalone-mode.md
Platform-specific? → ../../../docs/bundle-mode.md platform sections
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
