# AGOR Development Log

**Technical development history for developers and AI agents**

## Purpose

This log documents the technical evolution of AGOR, focusing on architectural decisions, implementation patterns, and lessons learned. It's designed to help developers and AI agents understand:

- **How AGOR evolved** from initial concept to current state
- **Why specific technical decisions** were made
- **What patterns work well** for AGOR development
- **How to contribute effectively** by understanding the development approach

## Entry Format

Each entry includes:

- **Date & Version**: When the work was done and what version
- **Technical Focus**: The main technical problem being solved
- **Implementation Details**: Specific technical choices and code changes
- **Rationale**: Why these particular decisions were made
- **Impact**: How the changes affected the codebase and functionality
- **Lessons Learned**: Key insights discovered during development
- **Next Steps**: What the changes enable for future development

---

## Development Entries (Reverse Chronological)

### 9. 2024-12-19 | Protocol v0.4.0 | Bundle Mode Menu Display Fix

**Technical Focus**: Fixing bundle mode initialization where agents were showing internal function calls instead of clean user menus.

**Implementation Details**:
- Created `BUNDLE_INITIALIZATION.md` for streamlined bundle mode setup with clear step-by-step instructions
- Added critical warnings in `AGOR_INSTRUCTIONS.md` Section 4 to prevent showing technical documentation to users
- Strengthened menu display instructions for all three roles (Solo Developer, Project Coordinator, Agent Worker)
- Updated `README_ai.md` to clearly distinguish between bundle mode and standalone mode initialization paths
- Added explicit "DO NOT SHOW TO USERS" warnings for internal technical documentation

**Rationale**:
- Bundle mode users were seeing technical function calls like `tree('.')`, `grep('.', 'def ')`, `analyze_file_structure(path)` instead of clean menu options
- This created a poor user experience and exposed internal implementation details
- Need clear separation between user-facing menus and internal technical documentation
- Bundle mode requires more streamlined initialization than standalone mode

**Impact**:
- Bundle mode agents should now display clean, professional menus instead of technical function names
- Clear distinction between bundle mode (streamlined) and standalone mode (comprehensive) initialization
- Better user experience with polished interface
- Internal technical documentation properly hidden from end users

**Lessons Learned**:
- Bundle mode and standalone mode have different UX requirements and should have separate initialization paths
- AI agents need very explicit instructions about what to show vs. hide from users
- Technical documentation sections need clear warnings to prevent accidental exposure
- Menu display instructions need to be strengthened with "CRITICAL" and "EXACTLY" language

**Next Steps**: Test bundle mode initialization with real AI platforms to verify the fix works correctly.

---

### 8. YYYY-MM-DD | Protocol v0.4.0 | Terminology and Hotkey Update (Snapshot)

**Technical Focus**: Standardizing core terminology from "handoff" to "snapshot" across the project, updating associated hotkeys, and bumping the protocol version to reflect these conceptual changes.

**Implementation Details**:
- Changed `PROTOCOL_VERSION` in `src/agor/constants.py` from "0.3.0" to "0.4.0".
- Renamed directory reference `.agor/handoffs/` to `.agor/snapshots/` in all code and documentation.
- Renamed Python module `src/agor/tools/handoff_templates.py` to `src/agor/tools/snapshot_templates.py` and updated all imports.
- Renamed relevant functions, variables, and constants within `snapshot_templates.py` (e.g., `generate_handoff_document` to `generate_snapshot_document`).
- Updated hotkeys in `src/agor/tools/AGOR_INSTRUCTIONS.md`:
    - `handoff` → `snapshot`
    - `receive` → `load_snapshot`
    - `handoffs` → `list_snapshots`
- Performed a global replacement of "handoff" terminology with "snapshot" in all relevant documentation and code comments/strings.
- Updated `docs/snapshots.md` (formerly `docs/handoffs.md`) content and title.

**Rationale**:
- The term "snapshot" is more intuitive and versatile, especially for solo developer use cases involving context preservation.
- Ensures consistency in language across all project assets (code, docs, agent instructions).
- The scope of changes (terminology, hotkeys, directory structures used by agents) constitutes a protocol update.

**Impact**:
- Agents will now be instructed using the "snapshot" terminology and new hotkeys.
- Internal code and documentation are now consistent with this change.
- Protocol version "0.4.0" signals these modifications.

**Lessons Learned**:
- Core terminology changes require thorough updates across multiple project facets (code, docs, tests, agent instructions).
- Protocol versioning is key to signaling the nature of changes to users and developers.

**Next Steps**: Continue with documentation enhancements, particularly elaborating on snapshot scenarios.

---

### 7. 2025-05-26 | Protocol v0.3.0 | CLI Usage Clarification & Agent Guidance

**Technical Focus**: Preventing agent confusion about CLI vs coordination file usage

**Implementation Details**:

- Added comprehensive CLI usage patterns section to development guide
- Documented internal vs external command categories
- Created agent role clarification (Bundle/Standalone/External modes)
- Added common misconception prevention with specific examples

**Rationale**:

- Agents were incorrectly assuming they should use internal coordination CLI commands
- Bundle mode vs standalone mode confusion was causing workflow issues
- Need clear guidance on when to use CLI vs work with `.agor/` files directly

**Impact**:

- Clear separation between user-facing and internal commands
- Reduced potential for agents to misuse coordination system
- Better onboarding experience for new agents joining projects

**Lessons Learned**:

- Documentation needs to be proactive about common misconceptions
- Agent context (bundle vs standalone) significantly affects workflow
- Clear role definitions prevent coordination system misuse

**Next Steps**: Monitor agent feedback to refine guidance further

---

### 6. 2025-05-26 | Protocol v0.3.0 | Protocol Version Reduction

**Technical Focus**: Establishing realistic protocol versioning strategy

**Implementation Details**:

- Reduced protocol version from 1.0.0 to 0.3.0
- Added versioning strategy documentation (0.x.x = development, 1.0.0+ = production)
- Updated all references in constants, development guide, and feedback system
- Added clear comments about version progression

**Rationale**:

- Version 1.0.0 should be reserved for production-ready, battle-tested protocols
- Current coordination protocols are functional but untested in real multi-agent scenarios
- Need clear upgrade path and realistic expectations

**Impact**:

- More honest representation of current protocol maturity
- Clear milestone target (1.0.0) for production readiness
- Better user expectations about stability

**Lessons Learned**:

- Version numbers carry semantic meaning and expectations
- Pre-1.0 versions communicate "still evolving" appropriately
- Protocol version should track coordination stability, not feature completeness

**Next Steps**: Real-world testing to validate protocols before 1.0.0

---

### 5. 2025-05-26 | Protocol v0.3.0 | Feedback System Implementation

**Technical Focus**: Creating user feedback collection mechanism to replace "meta" functionality

**Implementation Details**:

- Added `generate-agor-feedback` CLI command
- Implemented dual output modes: copy/paste codeblock and direct repository commit
- Integrated NTP time synchronization for accurate timestamps
- Created comprehensive feedback form with structured categories
- Added system information collection (versions, platform, git context)

**Rationale**:

- Need systematic way to collect user feedback and improvement suggestions
- Replace any previous "meta" command concept with focused feedback system
- Enable both technical and non-technical feedback collection
- Support different environments (with/without git commit access)

**Impact**:

- Structured feedback collection mechanism in place
- Users can easily provide detailed feedback with context
- Development team gets actionable improvement data

**Lessons Learned**:

- Feedback systems need to work in multiple environments
- Automatic context collection reduces user burden
- Structured forms get better feedback than free-form requests

**Next Steps**: Analyze collected feedback to prioritize improvements

---

### 4. 2025-05-26 | Protocol v0.3.0 | Strategy Implementation Completion

**Technical Focus**: Implementing all missing strategy modules to complete AGOR functionality

**Implementation Details**:

- Created `dependency_planning.py` with comprehensive dependency analysis framework
- Created `risk_planning.py` with complete risk assessment and mitigation strategies
- Updated `strategies/__init__.py` with proper imports and error handling
- Verified all strategy modules (tm, qg, eo, dp, rp) are fully functional
- Added all missing functions to package exports

**Rationale**:

- Complete the planned AGOR feature set for comprehensive multi-agent coordination
- Provide systematic approaches to dependency and risk management
- Ensure all documented hotkeys have working implementations

**Impact**:

- All planned strategy modules now implemented and tested
- Complete feature parity with documented capabilities
- No more missing functionality gaps

**Lessons Learned**:

- Systematic approach to missing features prevents oversight
- Template-driven implementation ensures consistency
- Comprehensive testing validates all integration points

**Next Steps**: Focus on real-world usage and protocol refinement

---

### 3. 2025-05-26 | Protocol v0.3.0 | Development Guide Protocol Tracking

**Technical Focus**: Adding protocol version tracking to development documentation

**Implementation Details**:

- Added protocol version to development guide header
- Created version checking instructions for both AGOR and protocol versions
- Added programmatic version checking commands
- Documented when protocol version bumps are required

**Rationale**:

- Protocol version is separate from AGOR version and needs independent tracking
- Developers need clear guidance on when to increment protocol version
- Version checking should be easy and programmatic

**Impact**:

- Clear protocol version visibility in documentation
- Defined process for protocol version management
- Easy verification of current versions

**Lessons Learned**:

- Protocol versioning needs separate tracking from application versioning
- Documentation should include both current state and how to check it
- Version bump criteria need to be explicit

**Next Steps**: Monitor protocol changes and version appropriately

---

### 2. 2025-05-26 | Protocol v0.3.0 | Modularization Cleanup Completion

**Technical Focus**: Removing obsolete monolithic files and fixing all integration issues

**Implementation Details**:

- Deleted `strategy_protocols.py` (5,397 lines) - the monolithic strategy file
- Fixed syntax errors in `strategy.py` (malformed f-strings)
- Removed duplicate `version()` function in `main.py`
- Fixed undefined function calls and bare except clauses
- Updated all import references to point to modular strategy files
- Fixed `strategies/__init__.py` import errors

**Rationale**:

- Monolithic files confuse future agents and are hard to maintain
- Clean up technical debt from modularization process
- Ensure all code actually works without hidden errors

**Impact**:

- Clean, working codebase with no critical errors
- All tests passing (10 passed, 3 skipped async)
- Clear modular structure for future development

**Lessons Learned**:

- Large refactoring requires systematic cleanup phase
- Import chains need careful validation after modularization
- Automated testing catches integration issues early

**Next Steps**: Focus on new feature development with clean foundation

---

### 1. 2025-05-26 | Protocol v0.3.0 | Strategy Modularization

**Technical Focus**: Breaking down monolithic `strategy_protocols.py` into focused modules

**Implementation Details**:

- Split 5,397-line file into 11 focused modules (200-300 lines each)
- Created individual files: `parallel_divergent.py`, `red_team.py`, `mob_programming.py`, etc.
- Maintained all functionality while improving organization
- Updated import statements and package structure
- Added proper error handling for optional imports

**Rationale**:

- Large files are difficult for AI agents to navigate and understand
- Modular structure enables parallel development by multiple agents
- Clear separation of concerns improves maintainability and testing

**Impact**:

- Much easier to find and modify specific strategy functionality
- Reduced cognitive load for developers working on individual strategies
- Enabled completion of missing strategy implementations

**Lessons Learned**:

- AI agents work much better with focused, single-purpose files
- Modularization should happen before files become too large
- Clear naming conventions are crucial for discoverability

**Next Steps**: Complete missing strategy implementations in new modular structure

---

## Development Patterns & Principles

### Code Organization Patterns

**File Size Limits**: Keep files under 500 lines when possible, definitely under 1000 lines

- **Rationale**: AI agents have context windows and work better with focused files
- **Implementation**: Split large files into logical modules
- **Exception**: Generated files or data files can be larger

**Modular Strategy Architecture**: One strategy per file with clear interfaces

- **Pattern**: `strategies/strategy_name.py` with main function and helper functions
- **Benefits**: Easy to find, test, and modify individual strategies
- **Template**: Use consistent function signatures and documentation

**Import Error Handling**: Use try/except for optional imports

- **Pattern**: Graceful degradation when optional modules aren't available
- **Implementation**: Set functions to None if import fails, check before use
- **Benefits**: Prevents cascade failures in import chains

### Testing Patterns

**Comprehensive Test Coverage**: All new functionality should have tests

- **Current**: 10 passing tests, 3 skipped async tests
- **Pattern**: Unit tests for individual functions, integration tests for workflows
- **Tools**: pytest with clear test organization

**Import Validation**: Test that all package imports work correctly

- **Pattern**: Import all public functions in test to catch import errors
- **Benefits**: Catches modularization issues early

### Documentation Patterns

**Development Guide**: Keep current and actionable, not historical

- **Focus**: What developers need to know now
- **Updates**: Timestamp and version tracking for currency
- **Scope**: Guidelines, checklists, current status

**Development Log**: Technical history and decision rationale

- **Focus**: Why decisions were made, what was learned
- **Audience**: Developers and AI agents joining the project
- **Value**: Understanding evolution and contribution patterns

**Version Tracking**: Separate AGOR version from protocol version

- **AGOR Version**: Application features and bug fixes
- **Protocol Version**: Coordination protocol compatibility
- **Documentation**: Both versions tracked in development guide

### Agent Collaboration Patterns

**CLI vs Coordination Files**: Clear separation of concerns

- **CLI**: Primarily for bundling and setup
- **Coordination**: Work with `.agor/` files directly in most cases
- **Context**: Bundle mode vs standalone mode determines approach

**Role Clarity**: Define agent contexts and expected workflows

- **Bundle Mode**: Most common, work with extracted files
- **Standalone Mode**: Direct repository access, limited CLI use
- **External Agent**: Setup and bundling for others

## Contributing Guidelines

### For New Developers

1. **Read the Development Guide**: Understand current status and guidelines
2. **Review Recent Log Entries**: Understand recent technical decisions
3. **Check Test Suite**: Ensure your environment works (`pytest tests/`)
4. **Start Small**: Pick up missing implementations or bug fixes first
5. **Follow Patterns**: Use established patterns for consistency

### For AI Agents

1. **Determine Your Context**: Bundle mode, standalone mode, or external agent?
2. **Read README_ai.md**: If in bundle mode, this is your primary guide
3. **Check .agor/ Directory**: Look for existing coordination files
4. **Don't Assume CLI**: Most coordination happens through files, not commands
5. **Ask for Clarification**: If unsure about your role or context

### For Feature Development

1. **Check Development Guide**: Ensure feature aligns with current priorities
2. **Follow Modular Patterns**: Keep files focused and under 500 lines
3. **Add Tests**: All new functionality needs test coverage
4. **Update Documentation**: Both guide and log as appropriate
5. **Version Appropriately**: Bump protocol version if coordination changes

---

_This log is maintained to help developers and AI agents understand AGOR's technical evolution and contribute effectively._
