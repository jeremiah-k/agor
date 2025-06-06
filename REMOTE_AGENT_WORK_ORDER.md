
# 🤖 REMOTE AGENT WORK ORDER

**Generated**: 2025-06-06 17:49 UTC
**From**: Project Coordinator
**To**: Remote Agent (AugmentCode)
**Branch**: work-0.4.3-2
**Commit**: 575a2786

## 🎯 MISSION: AGOR Hotkey System Improvement & Remote Agent Coordination Testing

### 📚 STEP 1: Initialize Your Environment

**CRITICAL**: You must read these files first:
```bash
# Read these files in order:
1. src/agor/tools/README_ai.md (role selection and initialization)
2. src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive operational guide)
3. src/agor/tools/agent-start-here.md (quick startup guide)
```

**Install Dependencies**:
```bash
python3 -m pip install -r src/agor/tools/agent-requirements.txt
```

### 📸 STEP 2: Fetch Latest Changes and Sync

**Get Latest State**:
```bash
# Ensure you're on the correct branch
git checkout work-0.4.3-2

# Pull latest changes
git pull origin work-0.4.3-2

# Verify you're at the correct commit
git log --oneline -1
# Should show: 575a2786...
```

### 🎯 STEP 3: Your Primary Task

**MISSION**: Improve the AGOR hotkey system by replacing useless placeholder hotkeys with practical dev tooling integration.

**Current Problems**:
- Placeholder hotkeys like `sp`, `edit`, `?` are not useful
- Hotkeys should integrate with our actual dev tooling functions
- Need hotkeys for snapshot generation, handoff prompts, role/strategy management
- Users want practical functions they'll actually use

**Your Objectives**:
1. **Analyze Current Hotkeys**: Review `src/agor/tools/AGOR_INSTRUCTIONS.md` and identify placeholder/useless hotkeys
2. **Design Better Hotkeys**: Create hotkeys that integrate with our dev tooling functions:
   - Snapshot generation (`generate_complete_project_outputs`)
   - Handoff prompt creation (`generate_handoff_prompt_only`)
   - Role display/change functionality
   - Strategy display/change functionality
   - Quick status checks
3. **Implement Changes**: Update the hotkey system to use practical functions
4. **Test Integration**: Ensure hotkeys work with our dev tooling
5. **Update Documentation**: Update AGOR_INSTRUCTIONS.md with new useful hotkeys

### 🛠️ STEP 4: Use Our Dev Tooling

**Key Functions Available**:
```python
# In src/agor/tools/dev_tooling.py
from agor.tools.dev_tooling import (
    generate_complete_project_outputs,
    generate_handoff_prompt_only,
    generate_pr_description_only,
    generate_release_notes_only,
    HandoffRequest
)
```

**Create Snapshots**:
```python
# Use our tooling to create snapshots
request = HandoffRequest(
    task_description="Your task description",
    work_completed=["List of completed items"],
    next_steps=["List of next steps"],
    brief_context="Brief context"
)
outputs = generate_complete_project_outputs(request)
```

### 🔄 STEP 5: Communication Protocol

**Report Back Protocol**:
1. **Start Work**: Create initial status snapshot using our dev tooling
2. **Progress Updates**: Use snapshot generation to report progress
3. **Completion**: Create final handoff snapshot with results
4. **Save to Memory**: Use our tooling to save snapshots for coordination

**Snapshot Creation Command**:
```python
# Use this pattern for all communication
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import generate_handoff_prompt_only

outputs = generate_handoff_prompt_only(
    task_description='Your progress update',
    work_completed=['What you completed'],
    next_steps=['What comes next'],
    brief_context='Current status'
)
print(outputs['handoff_prompt'])
"
```

### 📋 STEP 6: Specific Implementation Requirements

**Hotkey Integration Points**:
1. **Snapshot Hotkey**: Quick snapshot generation and save
2. **Handoff Hotkey**: Generate handoff prompt for coordination
3. **Role Hotkey**: Display current role and allow role changes
4. **Strategy Hotkey**: Display current strategy and allow changes
5. **Status Hotkey**: Quick project status and branch info
6. **Dev Tools Hotkey**: Access to our dev tooling functions

**Files to Modify**:
- `src/agor/tools/AGOR_INSTRUCTIONS.md` - Update hotkey documentation
- Hotkey implementation files (identify during analysis)
- Any configuration files that define hotkey mappings

### ⚠️ CRITICAL REQUIREMENTS

1. **Read Documentation First**: Do not start coding until you've read all required docs
2. **Use Our Dev Tooling**: Integrate with existing functions, don't recreate
3. **Test Everything**: Ensure hotkeys work with our coordination system
4. **Create Snapshots**: Use our tooling for all progress reporting
5. **Commit Frequently**: Small, focused commits with clear messages
6. **Branch Safety**: Never switch branches, use our safe commit methods

### 🎯 SUCCESS CRITERIA

**You succeed when**:
- ✅ Useless placeholder hotkeys are replaced with practical functions
- ✅ Hotkeys integrate seamlessly with our dev tooling
- ✅ Users can quickly generate snapshots, handoffs, and status reports
- ✅ Role and strategy management is accessible via hotkeys
- ✅ Documentation is updated with new useful hotkeys
- ✅ System is tested and working correctly
- ✅ Final handoff snapshot is created using our tooling

### 🚀 GET STARTED

1. **Read the docs** (src/agor/tools/README_ai.md, AGOR_INSTRUCTIONS.md, agent-start-here.md)
2. **Install dependencies** (agent-requirements.txt)
3. **Sync your environment** (git pull, verify commit)
4. **Create initial status snapshot** using our dev tooling
5. **Begin hotkey analysis and improvement**

**Remember**: This is a test of our remote agent coordination workflow. Your success validates our snapshot-based coordination system and dev tooling integration.

---

**Project Coordinator**: Waiting for your initial status snapshot and progress updates. Use our dev tooling for all communication!
