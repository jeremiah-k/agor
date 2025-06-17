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

### "I need external project integration" (CRITICAL for Augment local agents)

- **[EXTERNAL_INTEGRATION_GUIDE.md](EXTERNAL_INTEGRATION_GUIDE.md)** - **ESSENTIAL** - Integration when AGOR is installed separately
  - Addresses critical meta feedback: tool location, module import failures, missing integration patterns
  - Automatic AGOR detection, fallback mechanisms, standardized workflows
  - Required for Augment local agents working on external projects
- **[external_integration.py](external_integration.py)** - External integration system implementation
- **[agor_wrapper.py](agor_wrapper.py)** - Command-line wrapper for external project usage

### "I need to check protocol updates or compatibility"

- **[docs/protocol-changelog.md](../../../docs/protocol-changelog.md)** - Protocol version history and compatibility guide
  - Current: Protocol v0.5.1 with security fixes and single memory branch architecture
  - Secure agent identification, directory-based isolation, enhanced coordination
  - Breaking changes, new capabilities, and migration notes
  - Reference commits and specific line numbers for changes

### "I need to understand roles and initialization"

- **[README_ai.md](README_ai.md)** - Complete AI protocol (563 lines)
  - Lines 18-40: Role selection (Worker Agent, Project Coordinator)
  - Lines 120-220: Role-specific hotkey menus
  - Lines 450-550: Snapshot procedures and meta-development

### "I need multi-agent coordination strategies"

- **[docs/strategies.md](../../../docs/strategies.md)** - 5 coordination strategies with decision matrix
  - Parallel Divergent: Independent exploration → synthesis
  - Pipeline: Sequential snapshots with specialization
  - Swarm: Dynamic task assignment
  - Red Team: Adversarial build/break cycles
  - Mob Programming: Collaborative coding
- **[docs/multi-agent-protocols.md](../../../docs/multi-agent-protocols.md)** - **COMPREHENSIVE** - Complete coordination protocols
  - Implementation protocols for all 5 strategies
  - Session management and handoff requirements
  - Role-specific workflows and responsibilities
  - Technical implementation with dev tools integration

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

- **[src/agor/tools/memory_manager.py](memory_manager.py)** - Low-level memory branch commit logic. For the overall system, see Memory Synchronization System in `AGOR_INSTRUCTIONS.md` (Section 6.1) and potentially `src/agor/memory_sync.py` (if it's the higher-level interface).
- **[README_ai.md](README_ai.md)** Lines 590-662 - Memory system documentation (refers to overall system)

### "I need hotkey commands reference"

- **[README_ai.md](README_ai.md)** Lines 120-220 - Role-specific menus
  - PROJECT COORDINATOR: sp, bp, ar, ss, pd, pl, sw, rt, mb, ct, tm, hp
  - ANALYST/SOLO DEV: a, f, co, da, bfs, grep, tree, edit, commit, diff
  - Worker Agent: Development tooling functions for analysis and implementation

### "I need to provide feedback on AGOR"

- **[agor-meta.md](agor-meta.md)** - Feedback system and templates
- **[README_ai.md](README_ai.md)** Lines 450-485 - Meta-development procedures

### "I need prompt templates for coordination"

- **[agent_prompt_templates.py](agent_prompt_templates.py)** - Agent role prompts
- **[project_planning_templates.py](project_planning_templates.py)** - Planning frameworks

## 📁 Complete File Inventory

### Core Documentation (docs/)

| File                                                                                   | Purpose                                    | Key Sections                                     | Lines |
| -------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------ | ----- |
| **[../../../docs/README.md](../../../docs/README.md)**                                 | Documentation overview                     | Navigation map, quick links                      | 60    |
| **[agent-start-here.md](agent-start-here.md)**                                         | **Agent entry point**                      | **Immediate guidance, discovery commands**       | ~100  |
| **[../../../docs/quick-start.md](../../../docs/quick-start.md)**                       | 5-minute setup guide                       | Installation, bundling, platform setup           | ~200  |
| **[../../../docs/bundle-mode.md](../../../docs/bundle-mode.md)**                       | Complete Bundle Mode guide                 | All platforms, models, troubleshooting           | ~300  |
| **[../../../docs/google-ai-studio.md](../../../docs/google-ai-studio.md)**             | Google AI Studio guide                     | Function Calling setup, troubleshooting          | ~300  |
| **[../../../docs/standalone-mode.md](../../../docs/standalone-mode.md)**               | Standalone Mode Guide                      | Setup, usage, advantages of direct git access    | ~250  |
| **[../../../docs/strategies.md](../../../docs/strategies.md)**                         | Multi-agent coordination                   | 5 strategies with examples, decision matrix      | ~400  |
| **[../../../docs/multi-agent-protocols.md](../../../docs/multi-agent-protocols.md)**   | **COMPREHENSIVE coordination protocols**   | **Implementation protocols, session management** | ~300  |
| **[../../../docs/snapshots.md](../../../docs/snapshots.md)**                           | Agent state snapshots & context management | Snapshot creation, receiving, solo use benefits  | ~550+ |
| **[coordination-example.md](coordination-example.md)**                                 | Strategy implementation                    | Complete example, before/after comparison        | ~300  |
| **[../../../docs/agor-development-guide.md](../../../docs/agor-development-guide.md)** | Development checklist                      | For agents working on AGOR itself                | ~400  |

### AI Instructions (src/agor/tools/)

| File                                                 | Purpose              | Key Sections                         | Lines |
| ---------------------------------------------------- | -------------------- | ------------------------------------ | ----- |
| **[README_ai.md](README_ai.md)**                     | Complete AI protocol | Role selection, hotkeys, procedures  | 563   |
| **[AGOR_INSTRUCTIONS.md](AGOR_INSTRUCTIONS.md)**     | Agent Mode setup     | Git clone workflow, initialization   | ~180  |
| **[BUNDLE_INSTRUCTIONS.md](BUNDLE_INSTRUCTIONS.md)** | Bundle Mode setup    | Upload workflow, platform comparison | ~150  |
| **[agor-meta.md](agor-meta.md)**                     | Feedback system      | Feedback pathways, templates         | ~200  |

### Technical Tools (src/agor/tools/)

| File                                                     | Purpose                                                                                         | Key Functions                                                              | Lines  |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------ |
| **[dev_tools.py](dev_tools.py)**                         | Main interface for dev utilities + secure agent identification                                  | sanitize_slug(), initialize_agent_workspace(), cleanup_agent_directories() | ~1500+ |
| **[git_operations.py](git_operations.py)**               | Handles core Git command execution, safety checks (safe_git_push), and timestamp utilities.     | run_git_command, safe_git_push, get_current_timestamp                      | ~200   |
| **[memory_manager.py](memory_manager.py)**               | Manages memory branch creation and commits (commit_to_memory_branch) ensuring clean separation. | commit_to_memory_branch, auto_commit_memory                                | ~300   |
| **[agent_handoffs.py](agent_handoffs.py)**               | Provides utilities for agent coordination, including prompt generation and backtick processing. | generate_handoff_prompt_only, detick_content                               | ~150   |
| **[dev_testing.py](dev_testing.py)**                     | Contains environment detection logic and test functions for AGOR tooling.                       | detect_environment, test_tooling                                           | ~100   |
| **[code_exploration.py](code_exploration.py)**           | Codebase analysis                                                                               | bfs_find, grep, tree, analyze_file_structure                               | ~300   |
| **[code_exploration_docs.md](code_exploration_docs.md)** | Tool documentation                                                                              | Function reference, examples                                               | 179    |
| **[snapshot_templates.py](snapshot_templates.py)**       | Snapshot generation                                                                             | generate_snapshot_document, git_context                                    | ~400   |
| **[external_integration.py](external_integration.py)**   | **External project integration system** - addresses critical meta feedback                      | AgorExternalTools, get_agor_tools, automatic detection with fallbacks      | ~300   |
| **[agor_wrapper.py](agor_wrapper.py)**                   | Command-line wrapper for external projects                                                      | CLI interface for AGOR tools when installed separately                     | ~200   |

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
- **Worker Agent**: Codebase analysis, implementation, technical deep-dives

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
