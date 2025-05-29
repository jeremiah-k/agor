# AGOR Memory - Jules Documentation Correction Task

## Task Overview - 2025-05-29 01:55:18

**Objective**: Redo Jules documentation port with corrected understanding of AGOR perspective and implementation.

## Key Corrections Identified

### 1. Perspective Problem
- **Issue**: Documentation mixed developer vs user perspectives
- **Fix**: Always present USER perspective (working on their projects, not AGOR itself)
- **Impact**: Users typically need to clone AGOR separately to `/tmp/agor_repo/` to access tools

### 2. SQLite Bundle Option Removal
- **Issue**: References to `--sqlite` flag and SQLite binary bundling
- **Reality**: SQLite memory is handled by Python files already in repo (`sqlite_memory.py`)
- **Fix**: Remove all `--sqlite` flag references and explanations

### 3. Jules Content Removal
- **Issue**: Jules-specific documentation needs to be removed for now
- **Fix**: 
  - Remove `docs/jules-direct-access-guide.md`
  - Remove Jules references from README.md and other docs
  - Remove Jules from platform support lists
  - Keep Augment Code Remote Agents as main standalone example

## Progress So Far

### ✅ Completed
- Created corrected branch: `jules-docs-port-corrected`
- Ported Jules changes (except jules-direct-access-guide.md)
- Removed SQLite bundle option from README.md
- Removed all Jules references from README.md
- Committed and pushed initial corrections

### 🔄 In Progress
- Removing SQLite references from BUNDLE_INSTRUCTIONS.md
- Checking other files for Jules/SQLite issues

### 📋 Next Steps
1. Fix BUNDLE_INSTRUCTIONS.md SQLite references
2. Check STANDALONE_INITIALIZATION.md for issues
3. Review other ported files for perspective/content issues
4. Commit and push frequently
5. Create final PR with corrected documentation

## Memory Branch Usage
- Using AGOR's memory branch system: `agor/mem/20250529_015518_jules_docs_correction`
- Memory stored separately from working branch
- Will switch back to working branch after memory commit

## Files Being Modified
- README.md ✅
- docs/state-management.md (ported)
- docs/work-orders-and-memory-guide.md (ported)
- src/agor/tools/AGOR_INSTRUCTIONS.md (ported)
- src/agor/tools/BUNDLE_INSTRUCTIONS.md (needs SQLite fixes)
- src/agor/tools/STANDALONE_INITIALIZATION.md (ported)
- src/agor/tools/agor-meta.md (ported)

## Key Understanding
- AGOR memory system uses memory branches (`agor/mem/` prefix)
- `.agor` files stored in memory branches, not working branches
- Memory sync manager handles branch switching
- This allows clean working branches while preserving agent memory
