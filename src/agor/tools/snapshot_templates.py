"""
Snapshot templates and procedures for seamless agent transitions and context saving.

Enables agents to create snapshots of their work for other agents or for themselves,
with complete context, including problem definition, progress made, commits, and next steps.
"""

import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List

from agor.tools.git_operations import run_git_command


def get_git_context() -> Dict[str, str]:
    """Get current git context including branch, status, and recent commits."""
    context = {
        "branch": "unknown",
        "current_commit": "unknown",
        "status": "git not available",
        "recent_commits": "git not available",
        "uncommitted_changes": [],
        "staged_changes": [],
    }
    try:
        # Get current branch
        success, branch_out = run_git_command(["branch", "--show-current"])
        if success:
            context["branch"] = branch_out.strip()

        # Get git status
        success, status_out = run_git_command(["status", "--porcelain"])
        if success:
            context["status"] = status_out.strip()

        # Get recent commits
        success, commits_out = run_git_command(["log", "--oneline", "-10"])
        if success:
            context["recent_commits"] = commits_out.strip()

        # Get current commit hash
        success, commit_hash_out = run_git_command(["rev-parse", "HEAD"])
        if success:
            context["current_commit"] = commit_hash_out.strip()

        # Get uncommitted changes
        success, uncommitted_out = run_git_command(["diff", "--name-only"])
        if success:
            context["uncommitted_changes"] = (
                uncommitted_out.strip().split("\n") if uncommitted_out.strip() else []
            )

        # Get staged changes
        success, staged_out = run_git_command(["diff", "--cached", "--name-only"])
        if success:
            context["staged_changes"] = (
                staged_out.strip().split("\n") if staged_out.strip() else []
            )

        return context
    except Exception:  # Broad exception to catch any issue during git operations
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
            success, version_out = run_git_command(["describe", "--tags", "--abbrev=0"])
            if success:
                return version_out.strip()
            return "development"  # Fallback if git describe fails
        except Exception:  # Broad exception for any other issue
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
    agent_id: str = None,
) -> str:
    """Generate a comprehensive snapshot document for agent transitions or context saving."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    agor_version = get_agor_version()

    # Generate agent ID if not provided
    if agent_id is None:
        from agor.tools.dev_tools import generate_agent_id

        agent_id = generate_agent_id()

    return f"""# 📸 Agent Snapshot Document

**Generated**: {timestamp}
**Agent ID**: {agent_id}
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
[{agent_id}] [{timestamp}] - SNAPSHOT RECEIVED: {problem_description[:50]}...
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
    """DEPRECATED: Creates local .agor directory which should NEVER be on main branch.

    Use memory branches for all .agor content instead.
    """
    print("⚠️  WARNING: create_snapshot_directory() is deprecated")
    print("⚠️  This prevents .agor files from being tracked on main branch")

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
    get_agor_version()

    return f"""# 📦 AGOR Snapshot: Task Completion Report

## Snapshot ID
{timestamp.replace(' ', 'T').replace(':', '')}-task-completion

## Author
{agent_role}

## Strategy
[Strategy from coordination system]

## Assigned To
{coordinator_id}

## Memory Branch
agor/mem/{timestamp.replace(' ', 'T').replace(':', '')[:13]}

## Context
Task completion report for: {original_task}

## Task Status
{final_status}

📘 **If you're unfamiliar with task completion reports, read the following before proceeding:**
- `src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- `src/agor/tools/AGOR_INSTRUCTIONS.md`
- `src/agor/tools/README_ai.md`
- `src/agor/tools/agent-start-here.md`

📎 **If coordination files are missing or incomplete, you may need to:**
- Confirm you're in a valid Git repo with AGOR coordination
- Use `src/agor/memory_sync.py` to sync coordination state
- Check `.agor/agentconvo.md` for recent agent communication

## Original Task
{original_task}

## Work Completed
{chr(10).join(f"- {item}" for item in work_completed)}

## Files Modified
{chr(10).join(f"- `{file}` - [Description of changes]" for file in files_modified)}

## Commits Made
{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## Results Summary
{results_summary}

## Issues Encountered
{issues_encountered}

## Recommendations
{recommendations}

## Technical Context
**Git Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Recent Commit History
```
{git_context['recent_commits']}
```

## Coordination Notes
Please review this completion report and update `.agor/agentconvo.md` with your feedback. Use `ch` to create a checkpoint when review is complete, and assign next tasks or close this work stream as appropriate.

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
    """Save completion report document (a type of snapshot) for coordinator review."""

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
    Generates a markdown-formatted progress report snapshot summarizing the current task, progress, blockers, next steps, work completed, and technical context for status updates to coordinators or team members.

    Args:
        current_task: Description of the task being reported on.
        progress_percentage: Current completion percentage of the task.
        work_completed: List of completed work items.
        current_blockers: List of current blockers or issues.
        next_immediate_steps: List of next steps to be taken.
        commits_made: List of recent commit hashes or messages.
        files_modified: List of files modified during the reporting period.
        agent_role: Role of the reporting agent.
        estimated_completion_time: Estimated time to complete the task (default "Unknown").
        additional_notes: Any additional notes or context (default "None").

    Returns:
        A markdown string containing the structured progress report snapshot.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()

    return f"""# 📈 AGOR Snapshot: Progress Report

## Snapshot ID
{timestamp.replace(' ', 'T').replace(':', '')}-progress-report

## Author
{agent_role}

## Strategy
[Strategy from coordination system]

## Assigned To
Project Coordinator

## Memory Branch
agor/mem/{timestamp.replace(' ', 'T').replace(':', '')[:13]}

## Context
Progress report for: {current_task}

📘 **If you're unfamiliar with progress reports, read the following before proceeding:**
- `src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- `src/agor/tools/AGOR_INSTRUCTIONS.md`
- `src/agor/tools/README_ai.md`
- `src/agor/tools/agent-start-here.md`

📎 **If coordination files are missing or incomplete, you may need to:**
- Confirm you're in a valid Git repo with AGOR coordination
- Use `src/agor/memory_sync.py` to sync coordination state
- Check `.agor/agentconvo.md` for recent agent communication

## 🎯 Current Task

{current_task}

## Progress Status
**Overall Progress**: {progress_percentage}
**Estimated Completion**: {estimated_completion_time}
**Current Status**: In Progress

## Work Completed
{chr(10).join(f"- {item}" for item in work_completed)}

## Current Blockers
{chr(10).join(f"- {blocker}" for blocker in current_blockers) if current_blockers else "- None"}

## Next Immediate Steps
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(next_immediate_steps))}

## Files Modified
{chr(10).join(f"- `{file}` - [Description of changes]" for file in files_modified)}

## Recent Commits
{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## Additional Notes
{additional_notes}

## Technical Context
**Git Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Recent Commit History
```
{git_context['recent_commits']}
```

## Coordination Notes
Please review this progress report and update `.agor/agentconvo.md` with your feedback. Use `ch` to create a checkpoint when review is complete, and provide guidance on next steps or address any blockers identified.
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
    Generates a markdown-formatted work order snapshot for assigning tasks to agents.

    The snapshot includes task details, requirements, acceptance criteria, files to modify, reference materials, priority, estimated effort, deadline, context notes, and technical Git context. It also provides instructions for agent acknowledgment and coordination.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()

    return f"""# 📦 AGOR Snapshot: Work Order

## Snapshot ID
{timestamp.replace(' ', 'T').replace(':', '')}-work-order

## Author
{coordinator_id}

## Strategy
[Strategy from coordination system]

## Assigned To
{assigned_agent_role}

## Memory Branch
agor/mem/{timestamp.replace(' ', 'T').replace(':', '')[:13]}

## Context
Work order assignment: {task_description}

## Priority
{priority_level}

📘 **If you're unfamiliar with work orders, read the following before proceeding:**
- `src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- `src/agor/tools/AGOR_INSTRUCTIONS.md`
- `src/agor/tools/README_ai.md`
- `src/agor/tools/agent-start-here.md`

📎 **If coordination files are missing or incomplete, you may need to:**
- Confirm you're in a valid Git repo with AGOR coordination
- Use `src/agor/memory_sync.py` to sync coordination state
- Check `.agor/agentconvo.md` for recent agent communication

## Task Description
{task_description}

## Requirements
{chr(10).join(f"- {req}" for req in task_requirements)}

## Acceptance Criteria
{chr(10).join(f"- {criteria}" for criteria in acceptance_criteria)}

## Files to Modify
{chr(10).join(f"- `{file}` - [Description of changes needed]" for file in files_to_modify)}

## Reference Materials
{chr(10).join(f"- {material}" for material in reference_materials)}

## Timeline & Priority
**Priority Level**: {priority_level}
**Estimated Effort**: {estimated_effort}
**Deadline**: {deadline}

## Context & Important Notes
{context_notes}

## Technical Context
**Git Branch**: `{git_context['branch']}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Starting Point
```
{git_context['recent_commits']}
```

## Coordination Notes
Please acknowledge receipt of this work order by updating `.agor/agentconvo.md` with your acceptance and initial plan. Use `progress-report` hotkey for regular status updates and `complete` hotkey when task is finished. Communicate any blockers or questions immediately through agentconvo.md.
"""


def generate_pr_description_snapshot(
    pr_title: str,
    pr_description: str,
    work_completed: list[str],
    commits_included: list[str],
    files_changed: list[str],
    testing_completed: list[str],
    breaking_changes: list[str],
    agent_role: str,
    target_branch: str = "main",
    reviewers_requested: list[str] = None,
    related_issues: list[str] = None,
) -> str:
    """Generate a PR description snapshot for user to copy when creating pull request."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()
    reviewers_requested = reviewers_requested or []
    related_issues = related_issues or []

    return f"""# 🔀 AGOR Snapshot: PR Description

## Snapshot ID
{timestamp.replace(' ', 'T').replace(':', '')}-pr-description

## Author
{agent_role}

## Strategy
[Strategy from coordination system]

## Assigned To
User (for PR creation)

## Memory Branch
agor/mem/{timestamp.replace(' ', 'T').replace(':', '')[:13]}

## Context
PR description for: {pr_title}

## Target Branch
{target_branch}

📘 **If you're unfamiliar with PR descriptions, read the following before proceeding:**
- `src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- `src/agor/tools/AGOR_INSTRUCTIONS.md`
- `src/agor/tools/README_ai.md`
- `src/agor/tools/agent-start-here.md`

📎 **If coordination files are missing or incomplete, you may need to:**
- Confirm you're in a valid Git repo with AGOR coordination
- Use `src/agor/memory_sync.py` to sync coordination state
- Check `.agor/agentconvo.md` for recent agent communication

## Pull Request Description (Copy & Paste)

### Title
{pr_title}

### Description
{pr_description}

## Work Completed
{chr(10).join(f"- {item}" for item in work_completed)}

## Files Changed
{chr(10).join(f"- `{file}` - [Description of changes]" for file in files_changed)}

## Commits Included
{chr(10).join(f"- `{commit}`" for commit in commits_included)}

## Testing Completed
{chr(10).join(f"- {test}" for test in testing_completed)}

## Breaking Changes
{chr(10).join(f"- {change}" for change in breaking_changes) if breaking_changes else "- None"}

## Related Issues
{chr(10).join(f"- {issue}" for issue in related_issues) if related_issues else "- None"}

## Requested Reviewers
{chr(10).join(f"- {reviewer}" for reviewer in reviewers_requested) if reviewers_requested else "- None specified"}

## Technical Context
**Source Branch**: `{git_context['branch']}`
**Target Branch**: `{target_branch}`
**Current Commit**: `{git_context['current_commit']}`
**Repository Status**: {'Clean' if not git_context['status'] else 'Has uncommitted changes'}

### Commit History for PR
```
{git_context['recent_commits']}
```

## Coordination Notes
This PR description is ready for the user to copy when creating the pull request. All work has been completed and committed. The user should create the PR using the description above and request reviews from the specified reviewers.
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


def save_progress_report_snapshot(report_content: str, task_summary: str) -> Path:
    """Save progress report snapshot for status updates."""

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


def save_work_order_snapshot(order_content: str, task_summary: str) -> Path:
    """Save work order snapshot for task assignment."""

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


def save_pr_description_snapshot(pr_content: str, pr_title: str) -> Path:
    """Save PR description snapshot for user to copy when creating pull request."""

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
