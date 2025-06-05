"""
Snapshot templates and procedures for seamless agent transitions and context saving.

Enables agents to create snapshots of their work for other agents or for themselves,
with complete context, including problem definition, progress made, commits, and next steps.
"""

import datetime
import subprocess
from pathlib import Path
from typing import Dict, List
from importlib.metadata import PackageNotFoundError, version


def get_git_context() -> Dict[str, str]:
    """Get current git context including branch, status, and recent commits."""
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Get git status
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Get recent commits
        recent_commits = subprocess.check_output(
            ["git", "log", "--oneline", "-10"], text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Get current commit hash
        current_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Get uncommitted changes
        uncommitted = subprocess.check_output(
            ["git", "diff", "--name-only"], text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Get staged changes
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()

        return {
            "branch": branch,
            "current_commit": current_commit,
            "status": status,
            "recent_commits": recent_commits,
            "uncommitted_changes": uncommitted.split("\n") if uncommitted else [],
            "staged_changes": staged.split("\n") if staged else [],
        }
    except subprocess.CalledProcessError:
        return {
            "branch": "unknown",
            "current_commit": "unknown",
            "status": "git not available",
            "recent_commits": "git not available",
            "uncommitted_changes": [],
            "staged_changes": [],
        }


def get_agor_version() -> str:
    """Get AGOR version from package or git tag."""
    try:
        # Try to get version from package using importlib.metadata
        return version("agor")
    except (PackageNotFoundError, Exception):
        try:
            # Try to get version from git tag
            version = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            return version
        except subprocess.CalledProcessError:
            return "development"


def generate_snapshot_document(
    problem_description: str,
    work_completed: List[str],
    commits_made: List[str],
    current_status: str,
    next_steps: List[str],
    files_modified: List[str],
    context_notes: str,
    agent_role: str,
    snapshot_reason: str,  # Renamed parameter
    estimated_completion: str = "Unknown",
) -> str:
    """
    Generates a comprehensive markdown snapshot document capturing the current state of work for agent transitions or context saving.
    
    The document includes a mandatory documentation reading checklist, environment and git context, problem definition, current status, completed work, commits, files modified, next steps, context notes, and detailed technical context. It also provides step-by-step instructions for the receiving agent to verify environment, load context, confirm understanding, continue work, and follow communication protocols.
    
    Args:
        problem_description: Description of the problem or task being addressed.
        work_completed: List of completed work items.
        commits_made: List of commit messages or hashes relevant to the snapshot.
        current_status: Summary of the current progress or state.
        next_steps: Ordered list of next actions to be taken.
        files_modified: List of files changed during the work.
        context_notes: Additional notes or context for the receiving agent.
        agent_role: The role of the agent creating the snapshot.
        snapshot_reason: The reason for creating the snapshot (e.g., handoff, checkpoint).
        estimated_completion: Estimated time or percentage to completion (default "Unknown").
    
    Returns:
        A formatted markdown string representing the full snapshot document.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()

    return f"""# 📸 Agent Snapshot Document

**Generated**: {timestamp}
**From Agent Role**: {agent_role}
**Snapshot Reason**: {snapshot_reason}
**AGOR Version**: {agor_version}

## 📚 MANDATORY: Documentation Reading Requirement

**CRITICAL**: Before proceeding with any work, the receiving agent MUST read these core AGOR documentation files:

### Required Reading (In Order):
1. **`src/agor/tools/README_ai.md`** - Role selection and initialization protocol
2. **`src/agor/tools/AGOR_INSTRUCTIONS.md`** - Comprehensive operational instructions and hotkey menus
3. **`src/agor/tools/agent-start-here.md`** - Quick entry point for ongoing projects

### Verification Checklist:
- [ ] Read README_ai.md completely - understand role selection and initialization
- [ ] Read AGOR_INSTRUCTIONS.md completely - understand hotkeys, protocols, and workflows
- [ ] Read agent-start-here.md completely - understand project entry procedures
- [ ] Understand current AGOR version: {agor_version}
- [ ] Understand snapshot system and coordination protocols
- [ ] Ready to follow AGOR protocols consistently

**No work should begin until all documentation is read and understood.**

## 🔧 Environment Context

**Git Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit'][:8]}...`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

## 🎯 Problem Definition

{problem_description}

## 📊 Current Status

**Overall Progress**: {current_status}
**Estimated Completion**: {estimated_completion}

## ✅ Work Completed

{chr(10).join(f"- {item}" for item in work_completed)}

## 📝 Commits Made

{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## 📁 Files Modified

{chr(10).join(f"- `{file}`" for file in files_modified)}

## 🔄 Next Steps

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(next_steps))}

## 🧠 Context & Important Notes

{context_notes}

## 🔧 Technical Context

### Git Repository State
**Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Full Commit Hash**: `{git_context['current_commit']}`

### Repository Status
```
{git_context['status'] if git_context['status'] else 'Working directory clean'}
```

### Uncommitted Changes
{chr(10).join(f"- `{file}`" for file in git_context['uncommitted_changes']) if git_context['uncommitted_changes'] else '- None'}

### Staged Changes
{chr(10).join(f"- `{file}`" for file in git_context['staged_changes']) if git_context['staged_changes'] else '- None'}

### Recent Commit History
```
{git_context['recent_commits']}
```

### Key Files to Review
{chr(10).join(f"- `{file}` - Review recent changes and understand current state" for file in files_modified[:5])}

## 🎯 Snapshot Instructions for Receiving Agent (If Applicable)

### 1. Environment Verification
```bash
# Verify you're on the correct branch
git checkout {git_context['branch']}

# Verify you're at the correct commit
git log --oneline -1
# Should show: {git_context['current_commit'][:8]}...

# Check AGOR version compatibility
# This snapshot was created with AGOR {agor_version}
# If using different version, consider checking out tag: git checkout {agor_version}
```

### 2. Context Loading
```bash
# Review the current state
git status
git log --oneline -10

# Examine modified files
{chr(10).join(f"# Review {file}" for file in files_modified[:3])}
```

### 3. Verify Understanding
- [ ] Read and understand the problem definition
- [ ] Review all completed work items
- [ ] Examine commits and understand changes made
- [ ] Verify current status matches expectations
- [ ] Understand the next steps planned
- [ ] Verify AGOR version compatibility
- [ ] Confirm you're on the correct git branch and commit

### 4. Continue Work
- [ ] Start with the first item in "Next Steps"
- [ ] Update this snapshot document with your progress
- [ ] Commit regularly with clear messages
- [ ] Update `.agor/agentconvo.md` with your status

### 5. Communication Protocol
- Update `.agor/agentconvo.md` with snapshot received confirmation (if applicable)
- Log major decisions and progress updates
- Create new snapshot document if passing to another agent or for archival

---

**Receiving Agent**: Please confirm snapshot receipt (if applicable) by updating `.agor/agentconvo.md` with:
```
[AGENT-ID] [{timestamp}] - SNAPSHOT RECEIVED: {problem_description[:50]}...
```
"""


def generate_snapshot_prompt(snapshot_file_path: str) -> str:
    """Generate a prompt for creating a snapshot of work, potentially for another agent."""

    return f"""# 📸 Work Snapshot Created

I've created a snapshot of my current work. Here's the complete context:

## Snapshot Document
Please read the complete snapshot document at: `{snapshot_file_path}`

## Instructions for Receiving Agent (If Applicable)

### 1. Load Context
```bash
# Read the snapshot document
cat {snapshot_file_path}

# Review current repository state
git status
git log --oneline -10
```

### 2. Confirm Understanding
After reading the snapshot document, please confirm you understand:
- The problem being solved
- Work completed so far
- Current status and next steps
- Files that have been modified
- Technical context and important notes

### 3. Continue the Work
- Start with the first item in the "Next Steps" section
- Update the snapshot document with your progress (if continuing this line of work)
- Follow the communication protocol outlined in the document

### 4. Update Communication Log (If Applicable)
Add to `.agor/agentconvo.md`:
```
[YOUR-AGENT-ID] [{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - SNAPSHOT RECEIVED: [Brief description of task]
```

## Ready to Begin?
Type `receive` to confirm you've read the snapshot document and are ready to continue the work if this is a direct transfer of work. Otherwise, this snapshot is for archival or context preservation.
"""


def generate_receive_snapshot_prompt() -> str:
    """Generate a prompt for receiving a work snapshot from another agent."""

    return """# 📸 Receiving Work Snapshot

I'm ready to receive a work snapshot from another agent. Please provide:

## Required Information

### 1. Snapshot Document Location
- Path to the snapshot document (usually in `.agor/snapshots/`)
- Or paste the complete snapshot document content

### 2. Current Repository State
```bash
# Let me check the current state
git status
git log --oneline -5
```

### 3. Verification Steps
I will:
- [ ] Read and understand the complete snapshot document
- [ ] Review the problem definition and context
- [ ] Examine all completed work and commits
- [ ] Understand the current status and next steps
- [ ] Verify the technical context

### 4. Confirmation Process
Once I understand the snapshot, I will:
- [ ] Confirm receipt in `.agor/agentconvo.md` (if applicable)
- [ ] Begin work on the next steps
- [ ] Update progress regularly
- [ ] Maintain communication protocols

## Ready to Receive
Please provide the snapshot document or its location, and I'll take over the work seamlessly.
"""


def create_snapshot_directory() -> Path:
    """Create snapshot directory structure in .agor/"""

    snapshot_dir = Path(".agor/snapshots")
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Create index file if it doesn't exist
    index_file = snapshot_dir / "index.md"
    if not index_file.exists():
        index_content = """# 📸 Snapshot Index

This directory contains snapshot documents for agent transitions and context saving.

## Active Snapshots
- None currently

## Completed/Archived Snapshots
- None yet

## Snapshot Naming Convention
- `YYYY-MM-DD_HHMMSS_problem-summary_snapshot.md`
- Example: `2024-01-15_143022_fix-authentication-bug_snapshot.md`

## Usage
- Use `snapshot` hotkey to create new snapshot
- Use `receive` hotkey to accept snapshot (if applicable)
- Update this index when snapshots are created or archived
"""
        index_file.write_text(index_content)

    return snapshot_dir


def save_snapshot_document(snapshot_content: str, problem_summary: str) -> Path:
    """Save snapshot document to .agor/snapshots/ directory."""

    snapshot_dir = create_snapshot_directory()

    # Generate filename with timestamp and problem summary
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in problem_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_{safe_summary}_snapshot.md"

    snapshot_file = snapshot_dir / filename
    snapshot_file.write_text(snapshot_content)

    # Update index
    update_snapshot_index(filename, problem_summary, "active")

    return snapshot_file


def update_snapshot_index(filename: str, problem_summary: str, status: str):
    """Update the snapshot index with new or completed/archived snapshots."""

    index_file = Path(".agor/snapshots/index.md")
    if not index_file.exists():
        create_snapshot_directory()  # Ensures directory and index exist

    content = index_file.read_text()

    if status == "active":
        # Add to active snapshots
        content = content.replace(
            "## Active Snapshots\n- None currently",
            f"## Active Snapshots\n- `{filename}` - {problem_summary}",
        )
        if "- None currently" not in content and f"`{filename}`" not in content:
            content = content.replace(
                "## Active Snapshots\n",
                f"## Active Snapshots\n- `{filename}` - {problem_summary}\n",
            )
    elif status == "completed" or status == "archived":  # Added 'archived'
        # Move from active to completed/archived
        content = content.replace(
            f"- `{filename}` - {problem_summary}", ""
        )  # Remove from active if present
        content = content.replace(
            "## Completed/Archived Snapshots\n- None yet",
            f"## Completed/Archived Snapshots\n- `{filename}` - {problem_summary}",
        )
        if "- None yet" not in content and f"`{filename}`" not in content:
            content = content.replace(
                "## Completed/Archived Snapshots\n",
                f"## Completed/Archived Snapshots\n- `{filename}` - {problem_summary}\n",
            )

    index_file.write_text(content)


def generate_completion_report(
    original_task: str,
    work_completed: List[str],
    commits_made: List[str],
    final_status: str,
    files_modified: List[str],
    results_summary: str,
    agent_role: str,
    coordinator_id: str,
    issues_encountered: str = "None",
    recommendations: str = "None",
) -> str:
    """Generate a completion report document (can be a form of snapshot) to return to coordinator."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()

    return f"""# 🏁 Task Completion Report

**Generated**: {timestamp}
**From Agent Role**: {agent_role}
**To Coordinator**: {coordinator_id}
**AGOR Version**: {agor_version}
**Task Status**: {final_status}

## 🎯 Original Task

{original_task}

## ✅ Work Completed

{chr(10).join(f"- {item}" for item in work_completed)}

## 📝 Commits Made

{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## 📊 Results Summary

{results_summary}

## 📁 Files Modified

{chr(10).join(f"- `{file}`" for file in files_modified)}

## 🔧 Technical Context

### Git Repository State
**Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Recent Commit History
```
{git_context['recent_commits']}
```

## ⚠️ Issues Encountered

{issues_encountered}

## 💡 Recommendations

{recommendations}

## 🔄 Next Steps for Coordinator

1. **Review Results**: Examine all completed work and commits
2. **Verify Quality**: Test functionality and review code changes
3. **Integration**: Merge changes if satisfactory
4. **Documentation**: Update project documentation if needed
5. **Assignment**: Assign next tasks or close this work stream

## 📝 Coordinator Instructions

### 1. Verification Steps
```bash
# Verify you're on the correct branch
git checkout {git_context['branch']}

# Review recent commits
git log --oneline -10

# Check current status
git status

# Review modified files
{chr(10).join(f"# Examine {file}" for file in files_modified[:3])}
```

### 2. Quality Assurance
- [ ] Review all commits for quality and completeness
- [ ] Test functionality if applicable
- [ ] Verify task requirements were met
- [ ] Check for any technical debt or issues
- [ ] Confirm documentation is updated

### 3. Communication Protocol
Update `.agor/agentconvo.md` with completion acknowledgment:
```
[COORDINATOR-ID] [{timestamp}] - TASK COMPLETED: {original_task[:50]}... - Status: {final_status}
```

### 4. Project Coordination
- [ ] Mark task as complete in project tracking
- [ ] Update team on completion status
- [ ] Assign follow-up tasks if needed
- [ ] Archive this snapshot document

---

**Task Complete**: This completion report is ready for coordinator review and integration.
"""


def save_completion_report(
    report_content: str, task_summary: str, coordinator_id: str
) -> Path:
    """
    Saves a completion report snapshot for coordinator review.
    
    Creates a timestamped markdown file containing the completion report in the `.agor/snapshots` directory, updates the snapshot index to mark it as completed, and returns the path to the saved file.
    """

    snapshot_dir = create_snapshot_directory()  # Use new directory function

    # Generate filename with timestamp and task summary
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_COMPLETED_{safe_summary}_snapshot.md"  # Added _snapshot

    report_file = snapshot_dir / filename
    report_file.write_text(report_content)

    # Update index
    update_snapshot_index(filename, f"COMPLETED: {task_summary}", "completed")

    return report_file


def generate_progress_report_snapshot(
    current_task: str,
    progress_percentage: str,
    work_completed: List[str],
    current_blockers: List[str],
    next_immediate_steps: List[str],
    commits_made: List[str],
    files_modified: List[str],
    agent_role: str,
    estimated_completion_time: str = "Unknown",
    additional_notes: str = "None",
) -> str:
    """
    Generates a structured progress report snapshot in markdown format for providing status updates to coordinators or team members.
    
    The snapshot includes the current task, progress percentage, completed work, blockers, next steps, recent commits, files modified, agent role, estimated completion time, technical git context, additional notes, and coordinator instructions. It enforces a mandatory documentation reading requirement and provides a verification checklist to ensure protocol compliance.
    
    Returns:
        A markdown-formatted string representing the progress report snapshot.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()

    return f"""# 📊 Progress Report Snapshot

**Generated**: {timestamp}
**From Agent Role**: {agent_role}
**Snapshot Type**: Progress Report
**AGOR Version**: {agor_version}

## 📚 MANDATORY: Documentation Reading Requirement

**CRITICAL**: Before proceeding with any work, the receiving agent MUST read these core AGOR documentation files:

### Required Reading (In Order):
1. **`src/agor/tools/README_ai.md`** - Role selection and initialization protocol
2. **`src/agor/tools/AGOR_INSTRUCTIONS.md`** - Comprehensive operational instructions and hotkey menus
3. **`src/agor/tools/agent-start-here.md`** - Quick entry point for ongoing projects

### Verification Checklist:
- [ ] Read README_ai.md completely - understand role selection and initialization
- [ ] Read AGOR_INSTRUCTIONS.md completely - understand hotkeys, protocols, and workflows
- [ ] Read agent-start-here.md completely - understand project entry procedures
- [ ] Understand current AGOR version: {agor_version}
- [ ] Understand snapshot system and coordination protocols
- [ ] Ready to follow AGOR protocols consistently

**No work should begin until all documentation is read and understood.**

## 🎯 Current Task

{current_task}

## 📈 Progress Status

**Overall Progress**: {progress_percentage}
**Estimated Completion**: {estimated_completion_time}
**Current Status**: In Progress

## ✅ Work Completed

{chr(10).join(f"- {item}" for item in work_completed)}

## 🚧 Current Blockers

{chr(10).join(f"- {blocker}" for blocker in current_blockers) if current_blockers else "- None"}

## 🔄 Next Immediate Steps

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(next_immediate_steps))}

## 📝 Recent Commits

{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## 📁 Files Modified

{chr(10).join(f"- `{file}`" for file in files_modified)}

## 🔧 Technical Context

### Git Repository State
**Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Recent Commit History
```
{git_context['recent_commits']}
```

## 💡 Additional Notes

{additional_notes}

## 🎯 Coordinator Instructions

### 1. Review Progress
- [ ] Examine completed work items
- [ ] Review recent commits and changes
- [ ] Assess progress against timeline
- [ ] Identify any support needed

### 2. Address Blockers
- [ ] Review current blockers
- [ ] Provide guidance or resources
- [ ] Reassign tasks if needed
- [ ] Update project timeline if necessary

### 3. Communication Protocol
Update `.agor/agentconvo.md` with progress acknowledgment:
```
[COORDINATOR-ID] [{timestamp}] - PROGRESS REVIEWED: {current_task[:50]}... - Status: {progress_percentage}
```

---

**Progress Report**: This snapshot provides current status for coordination and planning purposes.
"""


def generate_work_order_snapshot(
    task_description: str,
    task_requirements: List[str],
    acceptance_criteria: List[str],
    files_to_modify: List[str],
    reference_materials: List[str],
    coordinator_id: str,
    assigned_agent_role: str,
    priority_level: str = "Medium",
    estimated_effort: str = "Unknown",
    deadline: str = "None specified",
    context_notes: str = "None",
) -> str:
    """
    Generates a structured work order snapshot document for assigning tasks to agents.
    
    The snapshot includes task description, requirements, acceptance criteria, files to modify, reference materials, coordinator and agent roles, priority, estimated effort, deadline, technical and context notes, and detailed instructions for both agent and coordinator. It enforces a mandatory documentation reading requirement and provides a verification checklist to ensure protocol compliance.
    
    Returns:
        A formatted markdown string representing the complete work order snapshot.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()

    return f"""# 📋 Work Order Snapshot

**Generated**: {timestamp}
**From Coordinator**: {coordinator_id}
**Assigned To**: {assigned_agent_role}
**Snapshot Type**: Work Order
**AGOR Version**: {agor_version}
**Priority**: {priority_level}

## 📚 MANDATORY: Documentation Reading Requirement

**CRITICAL**: Before proceeding with any work, the receiving agent MUST read these core AGOR documentation files:

### Required Reading (In Order):
1. **`src/agor/tools/README_ai.md`** - Role selection and initialization protocol
2. **`src/agor/tools/AGOR_INSTRUCTIONS.md`** - Comprehensive operational instructions and hotkey menus
3. **`src/agor/tools/agent-start-here.md`** - Quick entry point for ongoing projects

### Verification Checklist:
- [ ] Read README_ai.md completely - understand role selection and initialization
- [ ] Read AGOR_INSTRUCTIONS.md completely - understand hotkeys, protocols, and workflows
- [ ] Read agent-start-here.md completely - understand project entry procedures
- [ ] Understand current AGOR version: {agor_version}
- [ ] Understand snapshot system and coordination protocols
- [ ] Ready to follow AGOR protocols consistently

**No work should begin until all documentation is read and understood.**

## 🎯 Task Description

{task_description}

## 📋 Requirements

{chr(10).join(f"- {req}" for req in task_requirements)}

## ✅ Acceptance Criteria

{chr(10).join(f"- {criteria}" for criteria in acceptance_criteria)}

## 📁 Files to Modify

{chr(10).join(f"- `{file}`" for file in files_to_modify)}

## 📚 Reference Materials

{chr(10).join(f"- {material}" for material in reference_materials)}

## ⏱️ Timeline & Priority

**Priority Level**: {priority_level}
**Estimated Effort**: {estimated_effort}
**Deadline**: {deadline}

## 🔧 Technical Context

### Git Repository State
**Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Starting Point
```
{git_context['recent_commits']}
```

## 🧠 Context & Important Notes

{context_notes}

## 🎯 Agent Instructions

### 1. Task Acceptance
Update `.agor/agentconvo.md` with work order receipt:
```
[AGENT-ID] [{timestamp}] - WORK ORDER RECEIVED: {task_description[:50]}... - Priority: {priority_level}
```

### 2. Work Execution
- [ ] Review all requirements and acceptance criteria
- [ ] Examine reference materials thoroughly
- [ ] Plan implementation approach
- [ ] Create feature branch if needed
- [ ] Implement solution incrementally
- [ ] Test functionality thoroughly
- [ ] Commit frequently with clear messages

### 3. Progress Reporting
- [ ] Update progress regularly in `.agor/agentconvo.md`
- [ ] Create progress report snapshots for major milestones
- [ ] Communicate blockers immediately
- [ ] Request clarification when needed

### 4. Task Completion
- [ ] Verify all acceptance criteria are met
- [ ] Create completion report snapshot
- [ ] Update `.agor/agentconvo.md` with completion status
- [ ] Prepare code for review

### 5. Quality Assurance
- [ ] Test all functionality
- [ ] Review code for quality and standards
- [ ] Update documentation if needed
- [ ] Ensure no breaking changes

## 🔄 Coordinator Follow-up

### Expected Deliverables
- [ ] Completed implementation meeting all requirements
- [ ] Progress report snapshots for major milestones
- [ ] Completion report snapshot with results summary
- [ ] Updated documentation if applicable
- [ ] Clean commit history with descriptive messages

### Communication Protocol
- [ ] Monitor `.agor/agentconvo.md` for progress updates
- [ ] Respond to questions and blockers promptly
- [ ] Review progress report snapshots
- [ ] Provide feedback and guidance as needed

---

**Work Order**: This snapshot contains complete task assignment with all necessary context and requirements.
"""


def generate_pr_description_snapshot(
    pr_title: str,
    pr_description: str,
    work_completed: List[str],
    commits_included: List[str],
    files_changed: List[str],
    testing_completed: List[str],
    breaking_changes: List[str],
    agent_role: str,
    target_branch: str = "main",
    reviewers_requested: List[str] = None,
    related_issues: List[str] = None,
) -> str:
    """
    Generates a detailed pull request (PR) description snapshot for users to copy when creating a PR.
    
    The snapshot includes a mandatory documentation reading checklist, PR title and description, lists of work completed, commits included, files changed, testing completed, breaking changes, related issues, and requested reviewers. It also provides technical context about the git repository, a commit history, step-by-step PR creation instructions, a PR description template, post-PR actions, review process guidelines, and quality gates. This ensures all required information and protocols are followed for submitting and reviewing a PR.

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()
    reviewers_requested = reviewers_requested or []
    related_issues = related_issues or []

    return f"""# 🔀 Pull Request Description Snapshot

**Generated**: {timestamp}
**From Agent Role**: {agent_role}
**Snapshot Type**: PR Description
**AGOR Version**: {agor_version}
**Target Branch**: {target_branch}

## 📚 MANDATORY: Documentation Reading Requirement

**CRITICAL**: Before proceeding with any work, the receiving agent MUST read these core AGOR documentation files:

### Required Reading (In Order):
1. **`src/agor/tools/README_ai.md`** - Role selection and initialization protocol
2. **`src/agor/tools/AGOR_INSTRUCTIONS.md`** - Comprehensive operational instructions and hotkey menus
3. **`src/agor/tools/agent-start-here.md`** - Quick entry point for ongoing projects

### Verification Checklist:
- [ ] Read README_ai.md completely - understand role selection and initialization
- [ ] Read AGOR_INSTRUCTIONS.md completely - understand hotkeys, protocols, and workflows
- [ ] Read agent-start-here.md completely - understand project entry procedures
- [ ] Understand current AGOR version: {agor_version}
- [ ] Understand snapshot system and coordination protocols
- [ ] Ready to follow AGOR protocols consistently

**No work should begin until all documentation is read and understood.**

## 🔀 Pull Request Description (Copy & Paste)

### Title
{pr_title}

### Description
{pr_description}

## ✅ Work Completed

{chr(10).join(f"- {item}" for item in work_completed)}

## 📝 Commits Included

{chr(10).join(f"- `{commit}`" for commit in commits_included)}

## 📁 Files Changed

{chr(10).join(f"- `{file}`" for file in files_changed)}

## 🧪 Testing Completed

{chr(10).join(f"- {test}" for test in testing_completed)}

## ⚠️ Breaking Changes

{chr(10).join(f"- {change}" for change in breaking_changes) if breaking_changes else "- None"}

## 🔗 Related Issues

{chr(10).join(f"- {issue}" for issue in related_issues) if related_issues else "- None"}

## 👥 Requested Reviewers

{chr(10).join(f"- {reviewer}" for reviewer in reviewers_requested) if reviewers_requested else "- None specified"}

## 🔧 Technical Context

### Git Repository State
**Source Branch**: `{git_context['branch']}`
**Target Branch**: `{target_branch}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Commit History for PR
```
{git_context['recent_commits']}
```

## 🎯 PR Creation Instructions for User

### 1. Pre-PR Checklist
- [ ] All work is committed and pushed to feature branch
- [ ] All tests are passing
- [ ] Code follows project standards
- [ ] Documentation is updated
- [ ] No merge conflicts with target branch

### 2. Create Pull Request (User Action Required)
```bash
# Ensure branch is up to date (if needed)
git checkout {git_context['branch']}
git push origin {git_context['branch']}

# Create PR using GitHub CLI (if available)
gh pr create --title "{pr_title}" --body "See PR description below" --base {target_branch} --head {git_context['branch']}

# Or create PR manually through GitHub web interface
```

**Note**: Agent has prepared all work and description. User should create the actual PR using the description provided below.

### 3. PR Description Template
```markdown
## Summary
{pr_description}

## Changes Made
{chr(10).join(f"- {item}" for item in work_completed)}

## Testing
{chr(10).join(f"- {test}" for test in testing_completed)}

## Breaking Changes
{chr(10).join(f"- {change}" for change in breaking_changes) if breaking_changes else "None"}

## Related Issues
{chr(10).join(f"- {issue}" for issue in related_issues) if related_issues else "None"}
```

### 4. Post-PR Actions (User Responsibilities)
- [ ] Link PR to related issues
- [ ] Request reviews from specified reviewers
- [ ] Monitor CI/CD pipeline status
- [ ] Respond to review feedback promptly
- [ ] Update PR description if needed

## 🔄 Review Process

### For Reviewers
- [ ] Review code changes thoroughly
- [ ] Test functionality locally if needed
- [ ] Check for breaking changes
- [ ] Verify documentation updates
- [ ] Approve or request changes

### For Author
- [ ] Address review feedback
- [ ] Update code based on suggestions
- [ ] Respond to review comments
- [ ] Request re-review after changes
- [ ] Merge when approved

## 📊 Quality Gates

### Code Quality
- [ ] Code follows project conventions
- [ ] No code smells or technical debt
- [ ] Proper error handling
- [ ] Adequate test coverage

### Documentation
- [ ] Code is well-commented
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Changelog updated

### Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Edge cases covered
- [ ] Performance impact assessed

---

**PR Description Ready**: This snapshot contains the complete PR description for the user to copy when creating the pull request.
"""


# Hotkey integration templates
SNAPSHOT_HOTKEY_HELP = """
📸 **Snapshot Commands:**
snapshot) create work snapshot for context or another agent
progress-report) create progress report snapshot for status updates
work-order) create work order snapshot for task assignment
pr-description) generate PR description for user to copy
complete) create completion report/snapshot for coordinator
receive-snapshot) receive work snapshot from another agent (or load context)
snapshots) list all snapshot documents
"""


def save_progress_report_snapshot(
    report_content: str, task_summary: str
) -> Path:
    """
    Saves a progress report snapshot document to the snapshots directory.
    
    The snapshot is saved with a timestamped filename based on the provided task summary and marked as active in the snapshot index.
    
    Args:
        report_content: The markdown content of the progress report snapshot.
        task_summary: A brief summary of the task for filename generation.
    
    Returns:
        The path to the saved progress report snapshot file.
    """

    snapshot_dir = create_snapshot_directory()

    # Generate filename with timestamp and task summary
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_PROGRESS_{safe_summary}_snapshot.md"

    report_file = snapshot_dir / filename
    report_file.write_text(report_content)

    # Update index
    update_snapshot_index(filename, f"PROGRESS: {task_summary}", "active")

    return report_file


def save_work_order_snapshot(
    order_content: str, task_summary: str
) -> Path:
    """
    Saves a work order snapshot document for task assignment to the snapshots directory.
    
    The snapshot is saved with a timestamped filename based on the task summary, and the snapshot index is updated to mark it as active.
    
    Args:
        order_content: The markdown content of the work order snapshot.
        task_summary: A brief summary of the assigned task, used for filename generation.
    
    Returns:
        The path to the saved work order snapshot file.
    """

    snapshot_dir = create_snapshot_directory()

    # Generate filename with timestamp and task summary
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_WORKORDER_{safe_summary}_snapshot.md"

    order_file = snapshot_dir / filename
    order_file.write_text(order_content)

    # Update index
    update_snapshot_index(filename, f"WORK ORDER: {task_summary}", "active")

    return order_file


def save_pr_description_snapshot(
    pr_content: str, pr_title: str
) -> Path:
    """
    Saves a pull request description snapshot to the `.agor/snapshots` directory.
    
    The snapshot is saved with a timestamped filename based on the PR title, and the snapshot index is updated to mark it as active.
    
    Args:
        pr_content: The content of the PR description snapshot.
        pr_title: The title of the pull request, used for filename generation.
    
    Returns:
        The path to the saved PR description snapshot file.
    """

    snapshot_dir = create_snapshot_directory()

    # Generate filename with timestamp and PR title
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_title = "".join(c for c in pr_title if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_PR_DESC_{safe_title}_snapshot.md"

    pr_file = snapshot_dir / filename
    pr_file.write_text(pr_content)

    # Update index
    update_snapshot_index(filename, f"PR DESC: {pr_title}", "active")

    return pr_file
