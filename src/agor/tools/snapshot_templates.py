"""
Snapshot templates and procedures for seamless agent transitions and context saving.

Enables agents to create snapshots of their work for other agents or for themselves,
with complete context, including problem definition, progress made, commits, and next steps.
"""

import datetime
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Dict, List

def get_git_context() -> Dict[str, str]:
    """Get the current Git context.

    Retrieves the active branch name, the current commit hash, porcelain status,
    a list of recent commits, uncommitted changes, and staged changes.

    Returns:
        Dict[str, str]: A mapping with keys:
            branch: str              # current Git branch name
            current_commit: str      # full SHA of HEAD
            status: str              # output of `git status --porcelain`
            recent_commits: str      # output of `git log --oneline -10`
            uncommitted_changes: List[str]  # paths with local modifications
            staged_changes: List[str]       # paths staged for commit
    """
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
    """Get the AGOR version.

    Attempts to retrieve the version from the installed 'agor' package metadata.
    Falls back to using the latest Git tag, and if that fails, returns 'development'.

    Returns:
        str: The AGOR version string, or 'development' if unavailable.
    """
    try:
        return version("agor")
    except (PackageNotFoundError, Exception):
        try:
            tag = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            return tag
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
    snapshot_reason: str,
    estimated_completion: str = "Unknown",
) -> str:
    """Generate a comprehensive snapshot document for agent transitions or context saving.

    Args:
        problem_description (str): Description of the problem or task.
        work_completed (List[str]): Items of work that have been completed.
        commits_made (List[str]): List of commit identifiers representing work done.
        current_status (str): Current overall status of the work.
        next_steps (List[str]): Ordered list of next steps to be taken.
        files_modified (List[str]): List of file paths that have been modified.
        context_notes (str): Additional context or important notes.
        agent_role (str): Role or identifier of the agent creating the snapshot.
        snapshot_reason (str): Reason for creating this snapshot.
        estimated_completion (str, optional): Estimated completion time or status (default 'Unknown').

    Returns:
        str: A formatted markdown string containing the snapshot document.
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
    """Generate a prompt for creating a snapshot of work for another agent.

    Args:
        snapshot_file_path (str): The file path to the snapshot document.

    Returns:
        str: A markdown-formatted prompt instructing how to access and review the snapshot.
    """
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
    """Generate a prompt for receiving a work snapshot from another agent.

    Returns:
        str: A markdown-formatted prompt requesting necessary snapshot information and verification steps.
    """
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
    """Create the .agor/snapshots directory and initialize the snapshot index file.

    Creates (if not existing) the .agor/snapshots directory and an index.md file within it.

    Returns:
        Path: The path to the snapshots directory.
    """
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
    """Save a snapshot document to the .agor/snapshots directory.

    Args:
        snapshot_content (str): The content of the snapshot document to save.
        problem_summary (str): A short summary of the problem, used in the filename.

    Returns:
        Path: The path to the saved snapshot file.
    """
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
    """Update the snapshot index with a new or completed snapshot entry.

    Args:
        filename (str): Name of the snapshot file to add or move.
        problem_summary (str): Summary description of the snapshot content.
        status (str): Status of the snapshot ('active', 'completed', or 'archived').

    Returns:
        None
    """
    index_file = Path(".agor/snapshots/index.md")
    if not index_file.exists():
        create_snapshot_directory()  # Ensures directory and index exist

    content = index_file.read_text()

    if status == "active":
        content = content.replace(
            "## Active Snapshots\n- None currently",
            f"## Active Snapshots\n- `{filename}` - {problem_summary}",
        )
        if "- None currently" not in content and f"`{filename}`" not in content:
            content = content.replace(
                "## Active Snapshots\n",
                f"## Active Snapshots\n- `{filename}` - {problem_summary}\n",
            )
    elif status in ("completed", "archived"):
        content = content.replace(
            f"- `{filename}` - {problem_summary}", ""
        )
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
    """Generate a task completion report snapshot document for returning completed work to a coordinator.

    Args:
        original_task (str): Description of the original task completed.
        work_completed (List[str]): Items of work that have been completed.
        commits_made (List[str]): List of commit identifiers representing work done.
        final_status (str): The final status of the task (e.g., 'Completed', 'Failed').
        files_modified (List[str]): List of file paths that were modified.
        results_summary (str): Summary of the task results.
        agent_role (str): Role or identifier of the agent creating the report.
        coordinator_id (str): Identifier of the coordinator or recipient.
        issues_encountered (str, optional): Description of any issues encountered (default 'None').
        recommendations (str, optional): Recommendations for future work (default 'None').

    Returns:
        str: A formatted markdown string containing the completion report.
    """
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
    """Save a completion report snapshot document for coordinator review.

    Args:
        report_content (str): The content of the completion report.
        task_summary (str): A short summary of the completed task, used in the filename.
        coordinator_id (str): Identifier of the coordinator receiving the report.

    Returns:
        Path: The path to the saved completion report file.
    """
    snapshot_dir = create_snapshot_directory()  # Use new directory function

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_COMPLETED_{safe_summary}_snapshot.md"

    report_file = snapshot_dir / filename
    report_file.write_text(report_content)

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
    """Generate a progress report snapshot document summarizing the current task status.

    Args:
        current_task (str): Description of the task being reported.
        progress_percentage (str): Current progress percentage (e.g., '60%').
        work_completed (List[str]): List of completed work items.
        current_blockers (List[str]): List of current blockers or impediments.
        next_immediate_steps (List[str]): Ordered list of next steps to be taken.
        commits_made (List[str]): List of recent commit identifiers or messages.
        files_modified (List[str]): List of file paths that were modified.
        agent_role (str): Role or identifier of the reporting agent.
        estimated_completion_time (str, optional): Estimated time to completion (default 'Unknown').
        additional_notes (str, optional): Any additional notes or context (default 'None').

    Returns:
        str: A formatted markdown string containing the progress report snapshot.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()

    return f"""# 📈 AGOR Snapshot: Progress Report

... (template continues unchanged) ..."""

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
    """Generate a work order snapshot document for assigning tasks to an agent.

    Args:
        task_description (str): Description of the work order task.
        task_requirements (List[str]): List of requirements to fulfill.
        acceptance_criteria (List[str]): List of acceptance criteria items.
        files_to_modify (List[str]): List of file paths to be modified.
        reference_materials (List[str]): List of supporting reference materials or links.
        coordinator_id (str): Identifier of the coordinating agent.
        assigned_agent_role (str): Role or identifier of the agent assigned to the task.
        priority_level (str, optional): Priority level of the task (default 'Medium').
        estimated_effort (str, optional): Estimated effort required (default 'Unknown').
        deadline (str, optional): Deadline for task completion (default 'None specified').
        context_notes (str, optional): Additional context or notes (default 'None').

    Returns:
        str: A formatted markdown string containing the work order snapshot.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()

    return f"""# 📦 AGOR Snapshot: Work Order

... (template continues unchanged) ..."""

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
    """Generate a formatted pull request (PR) description snapshot for users to copy when creating a PR.

    Args:
        pr_title (str): Title of the pull request.
        pr_description (str): Detailed description of the pull request.
        work_completed (List[str]): List of work items completed.
        commits_included (List[str]): List of commit identifiers included in the PR.
        files_changed (List[str]): List of file paths changed.
        testing_completed (List[str]): List of testing steps or tests completed.
        breaking_changes (List[str]): List of breaking changes introduced (if any).
        agent_role (str): Role or identifier of the agent creating the PR description.
        target_branch (str, optional): Target branch for the PR (default 'main').
        reviewers_requested (List[str], optional): List of requested reviewers (default None).
        related_issues (List[str], optional): List of related issue identifiers (default None).

    Returns:
        str: A formatted markdown string containing the PR description snapshot.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_context = get_git_context()
    get_agor_version()
    reviewers_requested = reviewers_requested or []
    related_issues = related_issues or []

    return f"""# 🔀 AGOR Snapshot: PR Description

... (template continues unchanged) ..."""

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
    """Save a progress report snapshot for status updates.

    Args:
        report_content (str): The progress report content to save.
        task_summary (str): A short summary of the reported task, used in the filename.

    Returns:
        Path: The path to the saved progress report snapshot file.
    """
    snapshot_dir = create_snapshot_directory()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_PROGRESS_{safe_summary}_snapshot.md"

    report_file = snapshot_dir / filename
    report_file.write_text(report_content)

    update_snapshot_index(filename, f"PROGRESS: {task_summary}", "active")

    return report_file

def save_work_order_snapshot(order_content: str, task_summary: str) -> Path:
    """Save a work order snapshot for task assignment.

    Args:
        order_content (str): The work order content to save.
        task_summary (str): A short summary of the work order, used in the filename.

    Returns:
        Path: The path to the saved work order snapshot file.
    """
    snapshot_dir = create_snapshot_directory()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in task_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_WORKORDER_{safe_summary}_snapshot.md"

    order_file = snapshot_dir / filename
    order_file.write_text(order_content)

    update_snapshot_index(filename, f"WORK ORDER: {task_summary}", "active")

    return order_file

def save_pr_description_snapshot(pr_content: str, pr_title: str) -> Path:
    """Save a PR description snapshot for the user to copy when creating a pull request.

    Args:
        pr_content (str): The content of the PR description to save.
        pr_title (str): Title of the pull request used in the filename.

    Returns:
        Path: The path to the saved PR description snapshot file.
    """
    snapshot_dir = create_snapshot_directory()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_title = "".join(c for c in pr_title if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_PR_DESC_{safe_title}_snapshot.md"

    pr_file = snapshot_dir / filename
    pr_file.write_text(pr_content)

    update_snapshot_index(filename, f"PR DESC: {pr_title}", "active")

    return pr_file