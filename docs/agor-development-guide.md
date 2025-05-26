# 🛠️ AGOR Development Guide

**For AI agents and developers working on AGOR itself**

This guide ensures consistency, quality, and proper protocol management when developing AGOR. Use this checklist for all changes to maintain the integrity of the multi-agent coordination platform.

> **📜 Related Documentation:**
>
> - **[AGOR Development Log](agor-development-log.md)**: Technical history, architectural decisions, and lessons learned
> - **This Guide**: Current status, guidelines, and checklists for active development

## 📊 Implementation Status Tracking

**Last Updated**: 2025-01-27 20:30 UTC | **AGOR Version**: 0.2.4 | **Protocol Version**: 0.3.0 | **Latest**: SQLite memory system parity analysis and testing implementation

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
> - **Protocol Version**: Check `src/agor/constants.py` (current: "0.3.0" - development phase)
> - **Programmatic Check**: `python -c "from agor import __version__; from agor.constants import PROTOCOL_VERSION; print(f'AGOR: {__version__}, Protocol: {PROTOCOL_VERSION}')"`
> - **Protocol versioning**: 0.x.x = Development/testing, 1.0.0+ = Production-ready
> - **Protocol changes require version bump** - increment when coordination protocols, hotkeys, or agent behavior changes

### ✅ Fully Implemented Features

| Feature                 | Hotkey                                | Implementation                       | Status      |
| ----------------------- | ------------------------------------- | ------------------------------------ | ----------- |
| **Code Analysis**       | `a`, `f`, `co`, `tree`, `grep`        | code_exploration.py                  | ✅ Complete |
| **Handoff System**      | `handoff`, `receive`, `handoffs`      | handoff_templates.py                 | ✅ Complete |
| **SQLite Memory**       | `mem-*`, `db-*`, `coord-*`, `state-*` | sqlite_memory.py                     | ✅ Complete |
| **Parallel Divergent**  | `pd`                                  | strategies/parallel_divergent.py     | ✅ Complete |
| **Pipeline Strategy**   | `pl`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Swarm Strategy**      | `sw`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Strategy Selection**  | `ss`                                  | strategies/multi_agent_strategies.py | ✅ Complete |
| **Strategic Planning**  | `sp`                                  | project_planning_templates.py        | ✅ Complete |
| **Architecture Review** | `ar`                                  | project_planning_templates.py        | ✅ Complete |
| **Project Breakdown**   | `bp`                                  | strategies/project_breakdown.py      | ✅ Complete |
| **Team Creation**       | `ct`                                  | strategies/team_creation.py          | ✅ Complete |
| **Workflow Design**     | `wf`                                  | strategies/workflow_design.py        | ✅ Complete |
| **Handoff Prompts**     | `hp`                                  | strategies/handoff_prompts.py        | ✅ Complete |
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
3. **✅ COMPLETED**: All management features (Team Management, Quality Gates, Handoff Prompts)
4. **✅ COMPLETED**: All optimization features (Error Optimization, Dependency Planning, Risk Planning)
5. **✅ COMPLETED**: Code modularization - monolithic strategy_protocols.py removed, all features in focused modules
6. **✅ COMPLETED**: All strategy modules tested and working correctly

**Next Phase**: Maintenance, documentation improvements, and community feedback integration.

## 🔍 Current Development Priorities

### 📝 Documentation Enhancement (High Priority)

Based on comprehensive audit findings, the following documentation improvements are prioritized:

#### 1. Hotkey Documentation Clarity ✅ COMPLETED

- **Target**: `src/agor/tools/README_ai.md` (Hotkey Actions section)
- **Issue**: Some hotkeys lack clear behavior descriptions and parameter details
- **Examples**: PC `init`, Analyst `m`/`commit`/`diff`, Agent `ch`/`task`/`complete`/`log`/`report`
- **Action**: ✅ Enhanced all hotkey descriptions with detailed behavior, parameters, and usage examples

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

#### 3. SQLite Memory Configuration

- **Context**: Currently auto-activates if binary exists
- **Consideration**: Project-level configuration for memory type selection

### ✅ Completed Audit Items

- ✅ **Clear Role Definitions**: PROJECT COORDINATOR, ANALYST/SOLO DEV, AGENT WORKER
- ✅ **Excellent Agent Documentation**: Comprehensive `README_ai.md`
- ✅ **Robust Git Integration**: Direct binary usage with clear instructions
- ✅ **Structured Communication**: Well-defined `.agor/` directory protocols
- ✅ **Handoff Procedures**: Clear agent transition workflows
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
agor agent-manifest            # Generate standalone agent manifest
```

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
agor agent-manifest           # Generate standalone mode manifest
agor generate-agor-feedback   # Generate feedback form
agor version                   # Check versions
agor config                    # Manage configuration
agor git-config               # Set up git configuration
```

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

- [ ] **Hotkey additions/changes**: Any modification to the hotkey system
- [ ] **Role behavior changes**: Modifications to role-specific functionality
- [ ] **Communication format changes**: Changes to .agor/ file formats
- [ ] **Bundle structure changes**: Modifications to bundle contents or layout
- [ ] **Memory system changes**: Changes to memory management or storage

### Backward Compatibility Breaks

- [ ] **Document breaking changes**: Clearly explain what breaks and why
- [ ] **Provide migration path**: Explain how users can adapt
- [ ] **Update version appropriately**: Major version for breaking changes
- [ ] **Update compatibility notes**: Modify handoff compatibility guidelines

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

_This guide evolves with AGOR. Suggest improvements through the `meta` hotkey or GitHub issues._
