# 🛠️ AGOR Development Guide

**For AI agents and developers working on AGOR itself**

This guide ensures consistency, quality, and proper protocol management when developing AGOR. Use this checklist for all changes to maintain the integrity of the multi-agent coordination platform.

> **📜 Related Documentation:**
>
> - **[AGOR Development Log](agor-development-log.md)**: Technical history, architectural decisions, and lessons learned
> - **This Guide**: Current status, guidelines, and checklists for active development

## 🧠 CORE CONTEXT FOR ALL AGENTS

**⚠️ CRITICAL: This section contains permanent context that ALL agents must understand. Do NOT modify this section.**

### 🎯 AGOR Architecture Understanding

#### 📦 CLI vs Agent Tools - FUNDAMENTAL DISTINCTION

**AGOR CLI Purpose**: Primarily for **bundling repositories** for AI assistant upload
- `agor bundle <repo>` - Main use case
- `agor version`, `agor config`, `agor git-config` - Utility functions
- Most users interact with AGOR through bundling, not direct CLI usage

**Agent Tools Purpose**: For **agents working within coordination systems**
- Located in `src/agor/tools/` directory
- Include coordination files, strategy modules, memory systems
- Used by agents within `.agor/` coordination workflows

#### 🤖 CLI Commands vs Agent Hotkeys - CRITICAL DISTINCTION

**THERE ARE TWO COMPLETELY DIFFERENT TYPES OF "COMMANDS":**

**Real CLI Commands** (in `src/agor/main.py`):
- **[CLI] Commands**: `bundle`, `config`, `git-config`, `version` - for developers using AGOR
- **[AGENT] Commands**: `init`, `pd`, `ss`, `status`, `sync`, `agent-status`, `custom-instructions`, `generate-agor-feedback` - for agents when they need CLI access
- These are actual typer commands that can be run from terminal
- They appear in `agor --help` output
- Prefixed with [CLI] or [AGENT] to show intended user

**Agent Protocol Hotkeys** (in agent instructions):
- **Hotkeys**: `a`, `f`, `co`, `da`, `m`, `bfs`, `grep`, `tree`, `edit`, `commit`, etc.
- These are menu options/verbal commands in agent workflow instructions
- They are implemented as Python functions in `src/agor/tools/`
- They are NOT CLI commands - they're protocol directives
- They work within agent coordination workflows and `.agor/` files
- They are documented in `README_ai.md` as workflow options

**KEY RULE**: CLI commands with [CLI] prefix don't appear in agent hotkey menus. Agent hotkeys are not CLI commands.

#### 📋 Agent Coordination Documents

**REALITY CHECK**: AGOR bundles do NOT include setup manifests. Agent coordination uses snapshot documents (which can function as work orders or completion reports).

**Work Snapshots & Completion Reports** (Agent Coordination):
- **Location**: `.agor/snapshots/` directory.
- **Work Snapshots (as Work Orders)**: Task assignments with context, requirements, next steps.
- **Completion Snapshots/Reports**: Results summary, commits, issues, recommendations.
- **Used for**: Multi-agent coordination, work transitions, and state capture.
- **Implementation**: `handoff_templates.py` (Note: module name might be dated, but generates snapshot documents).

**Bundle Contents** (What's Actually in Bundles):
- **Project files**: Cloned repository with git history
- **AGOR tools**: `agor_tools/` directory with coordination scripts
- **Git binary**: Portable git executable for bundle environments
- **README**: `agor_tools/README_ai.md` with agent instructions
- **NO MANIFESTS**: Bundles do not contain setup manifests

#### 🏗️ File Structure Understanding

**Bundle Mode** (Most Common):
- Agent receives bundled archive with AGOR tools
- Works within extracted bundle
- Uses coordination files in `.agor/` directory
- Does NOT use CLI commands - works with files directly

**Standalone Mode** (Less Common):
- Agent has direct repository access
- Might use some CLI commands for status/coordination
- Still works primarily with `.agor/` coordination files

### 🚦 Development Safety Levels

**✅ Safe to Implement (Low Risk)**:
- Documentation improvements and clarifications
- Bug fixes in existing implementations
- Hotkey documentation enhancements
- Agent best practices reinforcement

**⚠️ Requires Coordination (Medium Risk)**:
- Changes to existing hotkey behavior
- New hotkey additions
- Changes to .agor file structure
- New strategy module additions

**🛑 Requires Team Discussion (High Risk)**:
- Changes to core coordination protocols
- Modifications to existing strategy implementations
- Breaking changes to agent_coordination.py
- Version number changes or protocol modifications

### 📁 Key Directories and Their Purposes

- **`src/agor/`**: Core AGOR package code
- **`src/agor/tools/`**: Agent coordination tools and templates
- **`src/agor/tools/strategies/`**: Multi-agent strategy implementations
- **`.agor/`**: Project coordination directory (created by agents)
- **`.agor/snapshots/`**: Agent snapshot documents.
- **`docs/`**: Documentation for users and developers

### 🔄 Commit and Push Protocol

**ALWAYS**: Commit often and push often
- Problems can happen and unpushed work is lost
- Use: `git add . && git commit -m "message" && git push`
- Update development guide as you work
- If agent struggles, generate a snapshot prompt for continuation

---

### 📚 Essential Files for Agent Understanding

**Always read these first when working on AGOR**:
- **`src/agor/tools/README_ai.md`**: Complete AI agent protocol and instructions
- **`src/agor/tools/handoff_templates.py`**: Agent coordination and snapshot system (Note: module name might be dated)
- **`docs/agor-development-guide.md`**: This file - development guidelines and context
- **`src/agor/main.py`**: CLI commands (for understanding what's user-facing vs internal)

### 🔍 Quick Context Checks

**Before making changes, always verify**:
```bash
# Check current AGOR version
python -c "from agor import __version__; from agor.constants import PROTOCOL_VERSION; print(f'AGOR: {__version__}, Protocol: {PROTOCOL_VERSION}')"

# See available CLI commands (user-facing)
./run_agor.sh --help

# Check agent tools directory
ls src/agor/tools/

# Check if .agor coordination exists
ls .agor/ 2>/dev/null || echo "No .agor directory - not in coordination mode"
```

### 🤝 Multi-Agent Coordination Principles

1. **Snapshots are a primary coordination mechanism** - not CLI commands
2. **Bundle manifests are for setup** - snapshot documents are for work transitions and state capture
3. **Most 'commands' are agent menu hotkeys** - not terminal commands
4. **The .agor/ directory is the coordination hub** - all agent state lives here
5. **Commit and push frequently** - work can be lost in agent environments
6. **Bidirectional workflow is required** - agents must report completion back to coordinators

### 🔄 Work Snapshot & Completion Report Workflow

**CRITICAL**: Agent coordination can be a two-way process using snapshots:

#### 📤 Coordinator → Agent (Work Snapshot as Work Order)
- **Hotkey**: `snapshot` - Create a work snapshot for an agent.
- **Contains**: Task description, context, requirements, next steps.
- **File**: `.agor/snapshots/YYYY-MM-DD_HHMMSS_task-summary_snapshot.md` (Note: directory and filename convention may evolve).

#### 📥 Agent → Coordinator (Completion Snapshot/Report)
- **Hotkey**: `complete` - Create a completion snapshot or report.
- **Contains**: Results summary, commits made, issues, recommendations.
- **File**: `.agor/snapshots/YYYY-MM-DD_HHMMSS_COMPLETED_task-summary_snapshot.md`
- **Purpose**: Coordinator review, quality assurance, integration decisions.

#### 📝 Communication Protocol
- **All snapshot events logged in**: `.agor/agentconvo.md`
- **Work Snapshot (as Work Order)**: `[COORDINATOR-ID] [timestamp] - WORK SNAPSHOT CREATED: description`
- **Snapshot Receipt**: `[AGENT-ID] [timestamp] - SNAPSHOT RECEIVED: description`
- **Task completion**: `[AGENT-ID] [timestamp] - TASK COMPLETED: description`
- **Coordinator review**: `[COORDINATOR-ID] [timestamp] - REPORT REVIEWED: status`

---

**🎯 Remember**: AGOR is primarily a bundling tool with sophisticated agent coordination capabilities built on top. The CLI is for bundling; the real power is in the agent tools and coordination system.

**🚨 IMPORTANT**: This "Core Context" section should remain stable and always be available to new agents. Only add to it, don't remove or significantly change existing content.

## 📊 Implementation Status Tracking

**Last Updated**: 2024-07-24 10:00 UTC | **AGOR Version**: 0.2.5 | **Protocol Version**: 0.4.0 | **Latest**: Protocol version bump and snapshot terminology updates.

> **🕐 Getting Current Date/Time Programmatically:**
>
> - **NTP Server (Accurate)**: `curl -s "http://worldtimeapi.org/api/timezone/UTC" | jq -r '.datetime[:16]' | tr 'T' ' '` + " UTC"
> - **Shell (Local)**: `date -u +"%Y-%m-%d %H:%M UTC"` (may be inaccurate in containers)
> - **Python**: `from datetime import datetime; datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")`
> - **Always use NTP for accurate timestamps** when updating this document to track development progress
>
> **📋 Getting Current Version Information:**
>
> - **AGOR Version**: Check `src/agor/__init__.py` (fallback: "0.2.3") or `pyproject.toml`
> - **Protocol Version**: Check `src/agor/constants.py` (current: "0.4.0" - development phase)
> - **Programmatic Check**: `python -c "from agor import __version__; from agor.constants import PROTOCOL_VERSION; print(f'AGOR: {__version__}, Protocol: {PROTOCOL_VERSION}')"`
> - **Protocol versioning**: 0.x.x = Development/testing, 1.0.0+ = Production-ready
> - **Protocol changes require version bump** - increment when coordination protocols, hotkeys, or agent behavior changes

### ✅ Fully Implemented Features

| Feature                 | Hotkey                                | Implementation                       | Status      |
| ----------------------- | ------------------------------------- | ------------------------------------ | ----------- |
| **Code Analysis**       | `a`, `f`, `co`, `tree`, `grep`        | code_exploration.py                  | ✅ Complete |
| **Snapshot System**     | `snapshot`, `load_snapshot`, `list_snapshots`      | handoff_templates.py (generates snapshots) | ✅ Complete |
| **SQLite Memory**       | Internal system only                  | sqlite_memory.py                     | ✅ Complete (Internal) |
| **Parallel Divergent**  | `pd`                                  | strategies/parallel_divergent.py     | ✅ Complete |
| **Pipeline Strategy**   | `pl`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Swarm Strategy**      | `sw`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Strategy Selection**  | `ss`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Strategic Planning**  | `sp`                                  | project_planning_templates.py        | ✅ Complete |
| **Architecture Review** | `ar`                                  | project_planning_templates.py        | ✅ Complete |
| **Project Breakdown**   | `bp`                                  | strategies/project_breakdown.py      | ✅ Complete |
| **Team Creation**       | `ct`                                  | strategies/team_creation.py          | ✅ Complete |
| **Workflow Design**     | `wf`                                  | strategies/workflow_design.py        | ✅ Complete |
| **Snapshot Prompts**    | `hp`                                  | strategies/handoff_prompts.py (generates snapshot prompts) | ✅ Complete |
| **Red Team Strategy**   | `rt`                                  | strategies/red_team.py               | ✅ Complete |
| **Mob Programming**     | `mb`                                  | strategies/mob_programming.py        | ✅ Complete |
| **Team Management**     | `tm`                                  | strategies/team_management.py        | ✅ Complete |
| **Quality Gates**       | `qg`                                  | strategies/quality_gates.py          | ✅ Complete |
| **Error Optimization**  | `eo`                                  | strategies/error_optimization.py     | ✅ Complete |
| **Dependency Planning** | `dp`                                  | strategies/dependency_planning.py    | ✅ Complete |
| **Risk Planning**       | `rp`                                  | strategies/risk_planning.py          | ✅ Complete |
| **Agent Discovery**     | N/A                                   | agent_coordination.py                | ✅ Complete |
| **Bundle Mode**         | N/A                                   | Complete documentation               | ✅ Complete |
| **AGOR Meta**           | `meta`                                | agor-meta.md                         | ✅ Complete |

### 🟡 Partially Implemented Features

| Feature           | Hotkey | Template | Execution Protocol | Priority |
| ----------------- | ------ | -------- | ------------------ | -------- |
| **ALL COMPLETED** | -      | -        | -                  | ✅ DONE  |

**Note**: All partially implemented features have been completed and moved to fully implemented.

### ❌ Missing Implementations

**ALL FEATURES COMPLETED!** 🎉

All planned AGOR strategy modules have been implemented and are fully functional.

### 🎯 Development Status Summary

**🎆 ALL MAJOR DEVELOPMENT COMPLETED!**

1. **✅ COMPLETED**: All multi-agent strategies (Parallel Divergent, Pipeline, Swarm, Red Team, Mob Programming)
2. **✅ COMPLETED**: All project coordination features (Project Breakdown, Team Creation, Workflow Design)
3. **✅ COMPLETED**: All management features (Team Management, Quality Gates, Snapshot Prompts)
4. **✅ COMPLETED**: All optimization features (Error Optimization, Dependency Planning, Risk Planning)
5. **✅ COMPLETED**: Code modularization - monolithic strategy_protocols.py removed, all features in focused modules
6. **✅ COMPLETED**: All strategy modules tested and working correctly

**Next Phase**: Maintenance, documentation improvements, and community feedback integration.

## 🔍 Current Development Priorities

### 🎯 CLI User/Agent Command Separation (✅ COMPLETED)

**Status**: ✅ COMPLETED - Clear distinction implemented

**Problem**: CLI mixed user-facing commands with agent coordination commands, causing confusion about what's for developers vs AI agents.

**Solution Implemented**:
- ✅ **Completed**: Added [CLI] prefixes to user commands: `bundle`, `config`, `git-config`, `version`
- ✅ **Completed**: Added [AGENT] prefixes to agent commands: `init`, `pd`, `ss`, `status`, `sync`, `agent-status`, `custom-instructions`, `generate-agor-feedback`
- ✅ **Completed**: Updated development guide with clear distinction between CLI commands and agent hotkeys
- ✅ **Completed**: Clarified that agent hotkeys (`a`, `f`, `co`, etc.) are protocol directives, not CLI commands

**Implementation Details**:
- **[CLI] Commands**: `bundle`, `config`, `git-config`, `version` - for developers using AGOR
- **[AGENT] Commands**: `init`, `pd`, `ss`, `status`, `sync`, `agent-status`, `custom-instructions`, `generate-agor-feedback` - for agents when they need CLI access
- **Agent Hotkeys**: `a`, `f`, `co`, `da`, `m`, `bfs`, `grep`, `tree`, `edit`, `commit`, etc. - protocol directives in agent instructions, NOT CLI commands

**Key Achievement**: Eliminated confusion between CLI commands and agent protocol hotkeys. Future agents will clearly understand the distinction when reading the codebase.

### 🔧 Role Bootstrapping Fix (✅ COMPLETED)

**Problem**: Role selection menu was broken in bundle uploads - AI was skipping role selection and jumping to default initialization, creating a "jumbled mess" of output.

**Root Cause Analysis**:
1. **Bundle Creation**: Works correctly - copies README_ai.md to agor_tools/ and generates proper prompt
2. **AI Prompt**: Works correctly - tells AI to "read agor_tools/README_ai.md completely"
3. **Role Selection Instructions**: Were too weak - AI was ignoring "Before proceeding, determine your role"
4. **Menu Structure**: Had confusing headers mixed into user-facing display

**Solution Implemented**:
- ✅ **Strong mandatory warnings**: Added explicit "DO NOT PROCEED WITHOUT ROLE SELECTION" instructions
- ✅ **Preserved Role A/B/C headers**: Kept formal role identifiers as requested
- ✅ **Clean menu display**: Role headers inside menu but properly formatted
- ✅ **Stop instruction**: Added "STOP HERE AND WAIT FOR USER RESPONSE" after menu
- ✅ **SINGLE-AGENT vs MULTI-AGENT guidance**: Clear workflow distinction

**Files Modified**:
- `src/agor/tools/README_ai.md` - Enhanced role selection protocol
- `.agor/handoff/restore_role_boot.md` - Documentation of changes

**Testing**: Role selection menu should now display properly when bundles are uploaded to AI platforms.

### 📝 Documentation Enhancement (High Priority)

Based on comprehensive audit findings, the following documentation improvements are prioritized:

#### 1. Hotkey Documentation Clarity ✅ COMPLETED

- **Target**: `src/agor/tools/README_ai.md` (Hotkey Actions section)
- **Issue**: Some hotkeys lack clear behavior descriptions and parameter details (ensure descriptions reflect snapshot terminology where applicable).
- **Examples**: PC `init`, Solo Developer `m`/`commit`/`diff`, Agent Worker `ch`/`task`/`complete`/`log`/`report`. Hotkeys like `da` (detailed analysis/snapshot), `hp` (snapshot prompts), and `handoff` (create snapshot) are key.
- **Action**: ✅ Enhanced all hotkey descriptions with detailed behavior, parameters, and usage examples, reflecting snapshot terminology.

#### 2. Undocumented Hotkey Functionality ✅ COMPLETED

- **Target**: `src/agor/tools/README_ai.md` (Project Coordinator Menu)
- **Issue**: PC hotkeys `as` (assign specialists) and `tc` (team coordination) listed but not described
- **Action**: ✅ Marked as "[FUTURE IMPLEMENTATION]" with clear status in documentation

#### 3. Agent Best Practices Reinforcement ✅ COMPLETED

- **Target**: Agent instructional materials
- **Issue**: Need stronger guidance on shared file access patterns
- **Action**: ✅ Added comprehensive shared file access section with CRITICAL guidelines for multi-agent coordination

### 🔧 Optional Enhancements (Low Priority)

#### 1. Convenience Hotkeys

- **Context**: Consider helper hotkeys for common sequences
- **Examples**: `project_status_overview`, `git_add_commit`, `git_push`
- **Trade-off**: Convenience vs maintaining direct CLI emphasis

#### 2. Strategy Parameter Documentation ✅ COMPLETED

- **Target**: Strategy initialization documentation
- **Issue**: Unclear how parameters translate to concrete states in `.agor/` files
- **Action**: ✅ Added comprehensive parameter effects section with concrete file mapping

#### 3. SQLite Memory System (Internal Use Only)

- **Status**: Experimental internal system, not for agent use
- **Purpose**: Advanced coordination logging and state management
- **Agent Interface**: Removed from hotkey menus, agents use `.agor/memory.md`

### ✅ Completed Audit Items

- ✅ **Clear Role Definitions**: SOLO DEVELOPER, PROJECT COORDINATOR, AGENT WORKER
- ✅ **Excellent Agent Documentation**: Comprehensive `README_ai.md`
- ✅ **Robust Git Integration**: Direct binary usage with clear instructions
- ✅ **Structured Communication**: Well-defined `.agor/` directory protocols
- ✅ **Snapshot Procedures**: Clear agent transition and context capture workflows
- ✅ **Modular Strategy Design**: All 12 strategy modules implemented
- ✅ **Code Exploration Tools**: Comprehensive analysis capabilities
- ✅ **Meta Feedback System**: `meta` hotkey for platform improvement
- ✅ **Trunk Linting Configuration**: Disabled bandit, configured reasonable markdown rules
- ✅ **Trunk Upgrade**: Updated to latest CLI (1.22.15) and linter versions

## 🎯 CLI Usage Patterns and Agent Expectations

### 📦 Primary CLI Purpose: Bundling Mode

The AGOR CLI is **primarily designed for bundling repositories** for AI assistant upload. Most users interact with AGOR through:

```bash
agor bundle my-project          # Main use case - bundle for AI upload
agor bundle user/repo --format gz
agor custom-instructions        # Generate AI assistant instructions
```

### 🤖 Agent Manifest vs CLI Commands - CRITICAL DISTINCTION

**❌ COMMON CONFUSION**: "Agent manifest is for standalone mode setup"

**✅ REALITY**: "Agent manifests" in AGOR context primarily refer to **snapshot documents** used for multi-agent coordination and work transitions.

#### 📋 Snapshot Documents (formerly referred to as Handoff Documents or Agent Manifests in some contexts)

**✅ CLARIFICATION**: Snapshot documents are stored in `.agor/snapshots/`.

- **Used for**: Agent-to-agent work transitions, solo context preservation, and detailed state capture.
- **Contains**: Problem definition, progress, commits, next steps, git context.
- **Generated by**: Agents using the `snapshot` hotkey.
- **Used by**: Agents receiving work (via `load_snapshot` hotkey) or by the same agent resuming work.
- **Format**: Structured markdown with comprehensive technical and project context.
- **Implementation**: `handoff_templates.py` (Note: module name might be dated, but it generates these snapshot documents).

### 🤖 Internal Commands vs User Commands

**❌ COMMON AGENT MISCONCEPTION**: "I should use `agor pd` or `agor init` commands directly"

**✅ REALITY**: Most AGOR coordination commands are for **internal use by agents within the coordination system**, not for direct CLI usage by humans or external agents.

#### 🔧 Internal Coordination Commands (Agent Use Only):

```bash
# These are used BY agents WITHIN the .agor/ coordination system
agor init <task>               # Initialize coordination (internal)
agor pd <task>                 # Parallel divergent setup (internal)
agor status                    # Check agent status (internal)
agor sync                      # Sync coordination state (internal)
agor agent-status <id> <status> # Update agent status (internal)
agor ss                        # Strategy selection (internal)
```

#### 👤 User-Facing Commands (External Use):

```bash
# These are for users and external agents
agor bundle <repo>             # Bundle repository for AI upload
agor custom-instructions       # Generate AI assistant instructions
agor generate-agor-feedback   # Generate feedback form
agor version                   # Check versions
agor config                    # Manage configuration
agor git-config               # Set up git configuration
```

#### 📝 Hotkeys vs CLI Commands - CRITICAL DISTINCTION

**❌ CONFUSION**: "Hotkeys like `pd`, `ss`, `init` are CLI commands"

**✅ REALITY**: Most "hotkeys" are **agent menu options**, not CLI commands.

- **Agent Menu Hotkeys**: `pd`, `ss`, `init`, `a`, `f`, `mem-add`, etc.
  - These are menu options agents use within coordination workflows
  - They trigger agent actions and generate coordination files
  - They are NOT direct CLI commands for users

- **Actual CLI Commands**: `bundle`, `version`, `config`, `git-config`
  - These are commands users run from terminal
  - They perform specific utility functions
  - They are documented in `--help` output

### 🎭 Agent Role Clarification

**When you're an AI agent working with AGOR:**

1. **In Bundle Mode** (most common):

   - You receive a bundled archive with AGOR tools
   - You work WITHIN the extracted bundle
   - You use the coordination files in `.agor/` directory
   - You DON'T use CLI commands - you work with the files directly

2. **In Standalone Mode** (less common):

   - You have direct repository access
   - You might use some CLI commands, but mainly for status/coordination
   - You still work primarily with `.agor/` coordination files

3. **As External Agent** (rare):
   - You might use `agor bundle` to create bundles
   - You use `agor custom-instructions` for setup
   - You DON'T use internal coordination commands

### ⚠️ Common Agent Mistakes to Avoid

#### ❌ "I'll use `agor init` to start working"

**Problem**: `agor init` is for initializing the coordination system, not for starting work on a project.
**Solution**: Look for existing `.agor/` directory or follow bundle extraction instructions.

#### ❌ "I need to run `agor pd` to set up parallel work"

**Problem**: Strategy setup commands are for coordination system initialization, not ongoing work.
**Solution**: Check `.agor/strategy.md` and `.agor/agent-instructions/` for your assigned role.

#### ❌ "I should use `agor status` to check my progress"

**Problem**: This is for internal coordination system status, not individual agent progress.
**Solution**: Update your agent memory files and check `.agor/agentconvo.md` for coordination.

#### ❌ "I need to install AGOR to work with this project"

**Problem**: In bundle mode, AGOR tools are included - no installation needed.
**Solution**: Look for `agor_tools/` directory in your bundle and read `README_ai.md`.

### 🎯 How to Determine Your Context

**Check these indicators to understand your role:**

1. **Bundle Mode Indicators**:

   - You received a `.zip`, `.tar.gz`, or `.tar.bz2` file
   - After extraction, you see `agor_tools/` directory
   - There's a `README_ai.md` file with instructions
   - You see `.agor/` coordination directory

2. **Standalone Mode Indicators**:

   - You have direct git repository access
   - AGOR is installed in the environment
   - You received an "agent manifest" with setup instructions
   - You can run `agor --help` successfully

3. **External Agent Indicators**:
   - You're helping someone SET UP AGOR for their project
   - You're creating bundles FOR other agents
   - You're not working within an existing AGOR coordination system

### 🚦 Development Safety Guidelines

#### ✅ Safe to Implement (Low Risk)

- Documentation improvements and clarifications
- Bug fixes in existing implementations
- Hotkey documentation enhancements
- Agent best practices reinforcement

#### ⚠️ Requires Coordination (Medium Risk)

- Changes to existing hotkey behavior - May affect existing users
- New hotkey additions - Need to ensure no conflicts
- Changes to .agor file structure - May break existing workflows
- New strategy module additions - Core functionality changes

#### 🛑 Requires Team Discussion (High Risk)

- Changes to core coordination protocols (agentconvo.md format, handoff structure)
- Modifications to existing strategy implementations
- Breaking changes to agent_coordination.py or core strategy modules
- Version number changes or protocol modifications

### 📈 Implementation Statistics

- **Total Features**: 25 documented features
- **Fully Implemented**: 25 features (100%)
- **Partially Implemented**: 0 features (0%)
- **Missing Implementation**: 0 features (0%)
- **Core Coordination**: 100% implemented (agent discovery, strategy execution, state management)
- **Strategy Coverage**: 100% implemented (all strategies have execution protocols)
- **Planning Tools**: 100% implemented (all planning tools complete)
- **Execution Protocols**: 100% implemented (all documented hotkeys have working implementations)

## 🔍 Pre-Development Checklist

### Understanding the Change

- [ ] **Check implementation status**: Review table above for current feature status
- [ ] **Identify impact scope**: Core protocol, documentation, tooling, or platform support?
- [ ] **Check existing issues**: Review GitHub issues for related work or conflicts
- [ ] **Understand user impact**: How will this affect existing AGOR users?
- [ ] **Review related documentation**: Ensure you understand current behavior

### Environment Setup

- [ ] **Configure git identity**: Use `agor git-config --import-env` or set manually
- [ ] **Verify attribution**: Ensure commits will be attributed correctly
- [ ] **Check environment variables**: Set GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL if using --import-env

### Branch Management

- [ ] **Create feature branch**: Use pattern `work-X.Y.Z-N` (e.g., `work-0.2.1-5`)
- [ ] **Base on latest main**: Always start from up-to-date main branch
- [ ] **Single responsibility**: One logical change per branch/PR

## 📋 Development Checklist

### Version Management

- [ ] **Update version numbers** if making protocol changes:
  - `src/agor/__init__.py` - Fallback version
  - `pyproject.toml` - Package version
  - Documentation references to version numbers
- [ ] **Protocol changes require version bump**: Any changes to hotkeys, coordination protocols, or agent behavior
- [ ] **Backward compatibility**: Consider impact on existing bundles and workflows

### Code Quality

- [ ] **Follow existing patterns**: Match coding style and architecture
- [ ] **Add type hints**: Use Python type annotations consistently
- [ ] **Update docstrings**: Document new functions and classes
- [ ] **Error handling**: Add appropriate error messages to `constants.py`
- [ ] **Logging**: Use structured logging with `structlog` for new features

### Implementation Status Updates

- [ ] **Update implementation status**: When completing features, update the status table above
- [ ] **Move features between categories**: Partial → Complete, Missing → Partial, etc.
- [ ] **Update statistics**: Recalculate percentages when adding/completing features
- [ ] **Update last updated date**: Change the date in the status tracking header
- [ ] **Update coordination-audit.md**: Keep the audit document in sync with development guide

### Documentation Updates

- [ ] **Update README.md** if adding new features or changing core functionality
- [ ] **Update relevant guides**:
  - `docs/bundle-mode.md` for platform changes
  - `docs/quick-start.md` for workflow changes
  - `src/agor/tools/README_ai.md` for protocol changes
- [ ] **Update documentation index** (`docs/index.md`) with new files or major changes
- [ ] **Check for broken links** after moving or renaming files
- [ ] **Update line counts** in documentation index if files change significantly

### Protocol and Hotkey Changes

- [ ] **Update hotkey documentation** in `README_ai.md` if adding/changing hotkeys
- [ ] **Update role-specific menus** for each role (PROJECT COORDINATOR, ANALYST/SOLO DEV, AGENT WORKER)
- [ ] **Test hotkey conflicts**: Ensure new hotkeys don't conflict with existing ones
- [ ] **Update agent prompt templates** if changing coordination protocols
- [ ] **Consider multi-agent impact**: How do changes affect agent-to-agent communication?

### File and Tool Management

- [ ] **Update MANIFEST.in** if adding new files to be included in packages
- [ ] **Update .trunk/trunk.yaml** if adding files that need linter exceptions
- [ ] **Check tool dependencies**: Ensure new tools are properly bundled
- [ ] **Test bundle creation**: Verify bundles include all necessary files
- [ ] **Validate git binary inclusion**: Ensure portable git binary is properly included

### Platform Compatibility

- [ ] **Test on target platforms**:
  - Google AI Studio (Gemini 2.5 Pro, Function Calling)
  - ChatGPT (GPT-4o, file upload)
  - Agent Mode (git-capable agents)
- [ ] **Verify bundle formats**: Test .zip and .tar.gz creation
- [ ] **Check platform-specific instructions** in bundle-mode.md
- [ ] **Test SQLite memory features** if applicable

## 🧪 Testing Checklist

### Functional Testing

- [ ] **Bundle creation**: Test `agor bundle` with various options
- [ ] **Bundle extraction**: Verify bundles extract properly on target platforms
- [ ] **Git binary functionality**: Ensure portable git works in bundle environment
- [ ] **Hotkey functionality**: Test new or modified hotkeys
- [ ] **Role initialization**: Test all three roles work properly
- [ ] **Memory systems**: Test both markdown and SQLite memory (if applicable)

### Integration Testing

- [ ] **Multi-agent workflows**: Test coordination between agents
- [ ] **Handoff procedures**: Verify handoff generation and reception
- [ ] **Communication protocols**: Test .agor/ directory structure and files
- [ ] **Cross-platform compatibility**: Test on different operating systems

### Edge Case Testing

- [ ] **Large repositories**: Test with substantial codebases
- [ ] **Special characters**: Test with non-ASCII filenames and content
- [ ] **Network issues**: Test bundle creation with poor connectivity
- [ ] **Permission issues**: Test in restricted environments

## 📝 Documentation Standards

### Writing Guidelines

- [ ] **Use consistent emoji**: Follow existing patterns (🎼 for AGOR, 📦 for bundles, etc.)
- [ ] **Token efficiency**: Write for AI consumption - clear, concise, scannable
- [ ] **Code examples**: Use proper markdown formatting with language tags
- [ ] **Platform specificity**: Clearly mark platform-specific instructions
- [ ] **Version references**: Use current version numbers consistently

### Content Requirements

- [ ] **Purpose statement**: Every doc should clearly state its purpose
- [ ] **Prerequisites**: List what users need before following instructions
- [ ] **Step-by-step procedures**: Break complex tasks into numbered steps
- [ ] **Troubleshooting sections**: Include common issues and solutions
- [ ] **Cross-references**: Link to related documentation appropriately

## 🔄 Pre-Commit Checklist

### Code Review

- [ ] **Self-review**: Read through all changes as if reviewing someone else's code
- [ ] **Check imports**: Ensure all imports are necessary and properly organized
- [ ] **Remove debug code**: Clean up any temporary debugging statements
- [ ] **Verify constants**: Use constants from `constants.py` instead of magic strings

### Attribution and Licensing

- [ ] **Maintain AgentGrunt attribution**: Keep proper attribution in appropriate files
- [ ] **License compatibility**: Ensure new dependencies are MIT-compatible
- [ ] **Copyright notices**: Add appropriate copyright for substantial new files

### Final Validation

- [ ] **Run linters**: Ensure trunk checks pass
- [ ] **Test installation**: Verify `pip install -e .` works
- [ ] **Test CLI**: Verify `agor --version` and basic commands work
- [ ] **Check bundle creation**: Create a test bundle to verify functionality

## 📤 Commit and PR Guidelines

### Commit Messages

- [ ] **Use conventional format**: `🔧 Fix bundle creation for Windows paths`
- [ ] **Include scope**: Specify what area is affected
- [ ] **Explain why**: Include reasoning for non-obvious changes
- [ ] **Reference issues**: Link to GitHub issues when applicable

### Pull Request Requirements

- [ ] **Descriptive title**: Clearly summarize the change
- [ ] **Comprehensive description**: Use the PR template format
- [ ] **Breaking changes**: Clearly mark any breaking changes
- [ ] **Testing notes**: Explain how the change was tested
- [ ] **Documentation updates**: List all documentation changes made

## 🚨 Critical Checkpoints

### Protocol Changes (Require Version Bump)

- [ ] **Hotkey additions/changes**: Any modification to the hotkey system (Note: `handoff`, `da`, `hp` hotkeys now relate to "snapshot" functionality).
- [ ] **Role behavior changes**: Modifications to role-specific functionality.
- [ ] **Communication format changes**: Changes to .agor/ file formats (e.g., snapshot structure).
- [ ] **Bundle structure changes**: Modifications to bundle contents or layout.
- [ ] **Memory system changes**: Changes to memory management or storage.

### Backward Compatibility Breaks

- [ ] **Document breaking changes**: Clearly explain what breaks and why.
- [ ] **Provide migration path**: Explain how users can adapt.
- [ ] **Update version appropriately**: Major version for breaking changes.
- [ ] **Update compatibility notes**: Modify snapshot compatibility guidelines.

## 🎯 Quality Gates

### Before Merging

- [ ] **All tests pass**: Functional and integration tests complete
- [ ] **Documentation complete**: All relevant docs updated
- [ ] **Version consistency**: All version references match
- [ ] **No broken links**: All documentation links work
- [ ] **Bundle testing**: Created and tested bundle on target platform

### Post-Merge Validation

- [ ] **PyPI compatibility**: Ensure package can be built and installed
- [ ] **User workflow testing**: Test complete user journey
- [ ] **Agent feedback**: Monitor for issues from AI agents using AGOR
- [ ] **Performance impact**: Verify no significant performance regressions

---

## 🤖 For AI Agents

When working on AGOR, you're improving the platform you're using. This creates a unique feedback loop where your development experience directly informs the quality of the tool.

**Remember**:

- Use the `meta` hotkey to provide feedback about the development process itself
- Document any pain points or inefficiencies you encounter
- Suggest improvements to this development guide based on your experience
- Test changes from the perspective of other AI agents who will use AGOR

**Your development work on AGOR helps all AI agents coordinate better!** 🎼

---

## Testing Coordination Strategies & State Management

AGOR's core functionality includes initializing and managing coordination strategies, which involves creating and modifying files within an `.agor/` directory (typically `.agor/state/` and `.agor/memory.db`). It's crucial to handle these files correctly when developing and testing AGOR itself:

### Avoid Committing Local State to the AGOR Repository

The AGOR project's root `.gitignore` file is configured to ignore common operational state files and directories, such as:
```gitignore
/.agor/state/
/.agor/memory.db
/.agor/agent-instructions/ # If these were example outputs
```
This helps prevent accidental commits of local test states into the main AGOR codebase. Always ensure your local AGOR repository is clean of such files before committing unrelated changes.

### Best Practice: Use a Separate Sample Project for Testing

To thoroughly test AGOR CLI commands that interact with or create state (e.g., `agor init`, `agor pd`, `agor status`, `agor agent-status`):

1.  **Create a dedicated sample project directory** outside of your AGOR development repository. This project can be a minimal mock-up of a typical user project.
2.  **Run `agor` commands from within this sample project's directory.** This will correctly create an `.agor/` directory and its state files *within that sample project*, mimicking real user experience without polluting the AGOR development repository.
3.  You can then inspect the state files in the sample project's `.agor/` directory to verify AGOR's behavior.

This approach provides a clean environment for testing stateful operations and ensures that the AGOR project's own `.agor/` directory (if it contains any legitimate, version-controlled template files or example outputs) remains pristine.

---

_This guide evolves with AGOR. Suggest improvements through the `meta` hotkey or GitHub issues._
