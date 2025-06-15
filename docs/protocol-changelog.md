# 🔄 AGOR Protocol Changelog

**Track coordination protocol changes and compatibility**

This changelog documents changes to AGOR's coordination protocols, agent instructions, and multi-agent workflows. It's separate from the application changelog and focuses specifically on protocol compatibility and agent behavior changes.

## How to Use This Changelog

- **Agents**: Check this when asked about protocol updates or compatibility
- **Developers**: Reference when making protocol-breaking changes
- **Users**: Understand what's changed in agent coordination capabilities

## Version Format

- **0.x.x**: Development/testing phase - protocols may change
- **1.0.0+**: Production-ready - backward compatibility guaranteed

---

## Protocol v0.5.0 (2025-06-15)

### 🆔 **MAJOR FEATURE: Agent Unique Identification System**

**Agent Identity Management**

- **Persistent Agent IDs**: Each agent gets a unique, persistent identifier (e.g., `agent_7cb9e6d4`)
- **Agent-Specific Memory Branches**: Agents use dedicated memory branches (`agor/mem/{agent_id}`)
- **Isolated Agent Storage**: Prevents agents from interfering with each other's snapshots
- **Cross-Agent Communication**: Enhanced agentconvo.md protocol with agent IDs

### 🔧 Technical Implementation

**New Functions** (`src/agor/tools/dev_tools.py`)

- `get_or_create_agent_id()`: Creates persistent agent ID stored in `.agor/agent_id`
- `cleanup_agent_memory_branches()`: Cleans up old memory branches
- `generate_agent_memory_branch(agent_id)`: Creates agent-specific memory branch names

**Enhanced Snapshot System**

- All snapshots now include agent ID in metadata
- Snapshots automatically commit to agent-specific memory branches
- Enhanced handoff prompts with agent context

### 📚 Documentation Improvements

**User Experience Enhancements**

- **Agent Prompt Examples** (`docs/agent-prompt-examples.md`): Comprehensive examples with emphasis on using AGOR tools
- **Platform Reorganization**: AugmentCode moved to top, Google AI Studio to bottom (free tier being phased out)
- **CLI vs Agent Tool Distinction**: Clear separation between developer CLI commands and agent development tools
- **Linked User Guidelines**: Replaced large codeblocks with links to `augment_user_guidelines.md`

### 🎯 Protocol Compatibility

**Breaking Changes**: None - all changes are backward compatible

**New Capabilities**:

- Agents maintain persistent identity across sessions
- Isolated memory branches prevent agent conflicts
- Enhanced agent coordination with unique identification
- Better user guidance with explicit tool usage examples

**Agent Responsibilities Added**:

- Agents should look for opportunities to update the dev tools index
- Agents should look for opportunities to add useful prompts to example prompts
- Agents should use persistent agent IDs for all memory operations

---

## Protocol v0.4.0 (2024-12-27)

### 🔄 **BREAKING CHANGE: Handoff → Snapshot Terminology**

**Global Terminology Update**

- **"Handoff"** terminology replaced with **"Snapshot"** throughout all documentation and code
- Hotkey changes: `handoff` → `snapshot`, `receive` → `load_snapshot`, `snapshots` → `list_snapshots`
- File renames: `docs/snapshots.md` → `docs/snapshots.md`, `snapshot_templates.py` → `snapshot_templates.py`
- Directory structure: `.agor/snapshots/` → `.agor/snapshots/`

### 🆕 Major Features Added

**Enhanced Agent Snapshot System** (`docs/snapshots.md`)

- Complete context preservation for agent transitions
- Self-snapshot capability for individual developers
- Structured snapshot templates with git context
- Cross-session work continuity support

**Standalone Mode** (`docs/standalone-mode.md`)

- Direct Git repository access for integrated AI environments
- Real-time collaboration protocols
- Enhanced Git operation workflows

**Enhanced State Management**

- Improved coordination file structures
- Better agent memory systems
- Refined snapshot procedures

### 📚 Documentation Overhaul

**Core Instructions** (`src/agor/tools/AGOR_INSTRUCTIONS.md`)

- Lines 1-50: Enhanced role selection clarity
- Lines 255-400: Improved coordination protocols
- Lines 500+: New snapshot integration procedures

**Agent Start Guide** (`src/agor/tools/agent-start-here.md`)

- Streamlined discovery workflow
- Better hotkey organization
- Clearer next-action guidance

**Development Guide** (`docs/agor-development-guide.md`)

- Updated protocol tracking (lines 165-195)
- Enhanced agent collaboration patterns (lines 320-360)
- Improved contribution guidelines

### 🔧 Technical Changes

**New Utilities** (`src/agor/tools/snapshot_templates.py`)

- `create_snapshot()`: Generate comprehensive agent snapshots
- `get_git_context()`: Capture complete repository state
- Template system for structured transitions

**Enhanced Snapshots** (`src/agor/tools/strategies/snapshot_prompts.py`)

- Improved work order generation
- Better completion report templates
- Enhanced agent coordination protocols
- Updated terminology throughout codebase

### 🎯 Protocol Compatibility

**Breaking Changes**:

- Terminology change from "handoff" to "snapshot" (hotkeys and file names changed)
- Agents using old hotkey names will need to update to new terminology

**New Capabilities**:

- Agents can now create and consume snapshots (formerly handoffs)
- Enhanced context preservation across sessions
- Improved multi-agent coordination workflows
- Standalone mode for direct Git repository access

**Migration Required**: Update hotkey usage from `handoff`/`receive`/`handoffs` to `snapshot`/`load_snapshot`/`list_snapshots`

---

## Protocol v0.3.0 (2024-05-26)

### 🔧 Foundation Improvements

**CLI Usage Clarification**

- Clear separation between user-facing and internal commands
- Agent role context guidance (Bundle/Standalone/External modes)
- Prevention of coordination system misuse

**Strategy Modularization**

- Split monolithic strategy files into focused modules
- Improved maintainability and agent navigation
- All 12 strategy modules implemented and functional

**Feedback System Implementation**

- `generate-agor-feedback` CLI command
- Structured feedback collection with system context
- Dual output modes for different environments

### 📋 Reference Commits

- `519fe63`: Major documentation overhaul and state management
- `a85e894`: Role bootstrapping improvements
- `4858dfe`: CLI command separation and role restoration

---

## Protocol v0.2.0 (Initial Release)

### 🎯 Core Protocol Establishment

**Multi-Agent Coordination**

- `.agor/` directory structure
- `agentconvo.md` communication protocol
- Individual agent memory files
- Strategy-based coordination

**Role System**

- Worker Agent (Role A)
- Project Coordinator (Role B)

**Development Strategies**

- Parallel Divergent
- Pipeline
- Swarm
- Red Team
- Mob Programming

---

## Quick Protocol Check

**Current Protocol Version**: `0.5.0`

**Check Your Version**:

```python
from agor.constants import PROTOCOL_VERSION
print(f"Protocol Version: {PROTOCOL_VERSION}")
```

**Key Files to Review for Updates**:

- `docs/snapshots.md` - New snapshot system
- `docs/standalone-mode.md` - Direct Git access mode
- `src/agor/tools/AGOR_INSTRUCTIONS.md` - Enhanced instructions
- `src/agor/tools/snapshot_templates.py` - New utilities

**Migration Notes**: No migration required from v0.3.x - all changes are additive.
