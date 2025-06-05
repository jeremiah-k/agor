class FallbackGitManager:
        """Fallback GitManager used in development mode when agor.git_binary import fails. Provides a basic wrapper around the system 'git' binary."""

        def get_git_binary(self):
            """Return the path to the system 'git' binary by searching PATH. Raises RuntimeError if not found."""
            import shutil

    class AgentChecklist:
        """Internal agent checklist for tracking mandatory procedures."""

        def __init__(self, agent_role: str = "solo_developer"):
            """Initialize the AgentChecklist with the provided role.
            
            Sets up a new session ID and loads the mandatory checklist items for that role."""
            self.agent_role = agent_role
            self.session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            self.mandatory_items = self._get_mandatory_items()
            self.completed_items = set()
            self.snapshot_created = False

# New hotkey processing functions
def process_progress_report_hotkey(
    task_description: str = "", progress: str = "50%"
) -> str:
    """Process progress-report hotkey and create progress report snapshot."""
    from agor.tools.snapshot_templates import (
        generate_progress_report_snapshot,
        save_progress_report_snapshot,
    )

    # Get user input for progress report details
    if not task_description:
        task_description = input("📊 Enter current task description: ")
    if progress == "50%":
        progress = input("📈 Enter progress percentage (e.g., 75%): ")

    work_completed = []
    print("✅ Enter completed work items (press Enter on empty line to finish):")
    while True:
        item = input("  - ")
        if not item:
            break
        work_completed.append(item)

    blockers = []
    print("🚧 Enter current blockers (press Enter on empty line to finish):")
    while True:
        blocker = input("  - ")
        if not blocker:
            break
        blockers.append(blocker)

    next_steps = []
    print("🔄 Enter next immediate steps (press Enter on empty line to finish):")
    while True:
        step = input("  - ")
        if not step:
            break
        next_steps.append(step)

    # Generate and save progress report
    report_content = generate_progress_report_snapshot(
        current_task=task_description,
        progress_percentage=progress,
        work_completed=work_completed,
        current_blockers=blockers,
        next_immediate_steps=next_steps,
        commits_made=["Recent commits from git log"],
        files_modified=["Files from git status"],
        agent_role="Solo Developer",
        estimated_completion_time=input("⏱️ Estimated completion time: ") or "Unknown",
        additional_notes=input("💡 Additional notes: ") or "None",
    )

    snapshot_file = save_progress_report_snapshot(report_content, task_description)
    print(f"📊 Progress report snapshot created: {snapshot_file}")

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def process_work_order_hotkey(task_description: str = "") -> str:
    """Process work-order hotkey and create work order snapshot."""
    from agor.tools.snapshot_templates import (
        generate_work_order_snapshot,
        save_work_order_snapshot,
    )

    # Get user input for work order details
    if not task_description:
        task_description = input("📋 Enter task description: ")

    requirements = []
    print("📋 Enter task requirements (press Enter on empty line to finish):")
    while True:
        req = input("  - ")
        if not req:
            break
        requirements.append(req)

    acceptance_criteria = []
    print("✅ Enter acceptance criteria (press Enter on empty line to finish):")
    while True:
        criteria = input("  - ")
        if not criteria:
            break
        acceptance_criteria.append(criteria)

    files_to_modify = []
    print("📁 Enter files to modify (press Enter on empty line to finish):")
    while True:
        file = input("  - ")
        if not file:
            break
        files_to_modify.append(file)

    # Generate and save work order
    order_content = generate_work_order_snapshot(
        task_description=task_description,
        task_requirements=requirements,
        acceptance_criteria=acceptance_criteria,
        files_to_modify=files_to_modify,
        reference_materials=[
            input("📚 Reference materials: ") or "See project documentation"
        ],
        coordinator_id=input("👤 Coordinator ID: ") or "Project Coordinator",
        assigned_agent_role=input("🤖 Assigned agent role: ") or "Agent Worker",
        priority_level=input("⚡ Priority level (High/Medium/Low): ") or "Medium",
        estimated_effort=input("⏱️ Estimated effort: ") or "Unknown",
        deadline=input("📅 Deadline: ") or "None specified",
        context_notes=input("🧠 Context notes: ") or "None",
    )

    snapshot_file = save_work_order_snapshot(order_content, task_description)
    print(f"📋 Work order snapshot created: {snapshot_file}")

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def process_create_pr_hotkey(pr_title: str = "") -> str:
    """Process create-pr hotkey and generate PR description for user to copy."""
    from agor.tools.snapshot_templates import (
        generate_pr_description_snapshot,
        save_pr_description_snapshot,
    )

    # Get user input for PR description details
    if not pr_title:
        pr_title = input("🔀 Enter PR title: ")

    pr_description = input("📝 Enter PR description: ")

    work_completed = []
    print("✅ Enter completed work items (press Enter on empty line to finish):")
    while True:
        item = input("  - ")
        if not item:
            break
        work_completed.append(item)

    testing_completed = []
    print("🧪 Enter testing completed (press Enter on empty line to finish):")
    while True:
        test = input("  - ")
        if not test:
            break
        testing_completed.append(test)

    breaking_changes = []
    print("⚠️ Enter breaking changes (press Enter on empty line to finish):")
    while True:
        change = input("  - ")
        if not change:
            break
        breaking_changes.append(change)

    # Get git information using proper git manager
    try:
        git_binary = git_manager.get_git_binary()
        commits = (
            subprocess.check_output([git_binary, "log", "--oneline", "-10"], text=True)
            .strip()
            .split("\n")
        )
        files_changed = (
            subprocess.check_output(
                [git_binary, "diff", "--name-only", "main"], text=True
            )
            .strip()
            .split("\n")
        )
    except Exception as err:
        commits = [f"Git error: {err}"]
        files_changed = ["<unknown>"]
    # Get additional PR details
    target_branch = input("🎯 Target branch (default: main): ") or "main"

    reviewers_input = input("👥 Requested reviewers (comma-separated): ")
    reviewers_requested = reviewers_input.split(",") if reviewers_input.strip() else []

    issues_input = input("🔗 Related issues (comma-separated): ")
    related_issues = issues_input.split(",") if issues_input.strip() else []

    # Generate and save PR description snapshot
    pr_content = generate_pr_description_snapshot(
        pr_title=pr_title,
        pr_description=pr_description,
        work_completed=work_completed,
        commits_included=commits,
        files_changed=files_changed,
        testing_completed=testing_completed,
        breaking_changes=breaking_changes,
        agent_role="Solo Developer",
        target_branch=target_branch,
        reviewers_requested=reviewers_requested,
        related_issues=related_issues,
    )

    snapshot_file = save_pr_description_snapshot(pr_content, pr_title)
    print(f"🔀 PR description snapshot created: {snapshot_file}")
    print(
        "📋 User can copy the PR description from the snapshot to create the actual pull request"
    )

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def log_to_agentconvo(agent_id: str, message: str, memory_branch: str = None) -> bool:
    """
    Appends a message to the agent communication log and commits it to a memory branch without switching branches.
    
    If committing to the memory branch fails, falls back to a regular commit on the current branch.
    
    Args:
        agent_id: Identifier of the agent logging the message.
        message: The message to log in the agent communication log.
        memory_branch: Optional name of the memory branch to use; auto-generated if not provided.
    
    Returns:
        True if the log entry was successfully committed, False otherwise.
    """
    timestamp = dev_tools.get_precise_timestamp()
    log_entry = f"{agent_id}: {timestamp} - {message}\n"

    if not memory_branch:
        memory_branch = f"agor/mem/{dev_tools.get_timestamp_for_files()}"

    print(f"📝 Logging to agentconvo.md: {agent_id} - {message}")

    # Create agentconvo.md content
    agentconvo_content = f"""# Agent Communication Log

Format: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]

## Communication History

{log_entry}
"""

    # Write agentconvo.md file to current working directory
    agentconvo_path = dev_tools.repo_path / ".agor" / "agentconvo.md"
    agentconvo_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if agentconvo_path.exists():
        with open(agentconvo_path, "a") as f:
            f.write(log_entry)
    else:
        agentconvo_path.write_text(agentconvo_content)

    # Try to commit to memory branch using new safe system
    if dev_tools._commit_to_memory_branch(
        ".agor/agentconvo.md",
        memory_branch,
        f"Update agentconvo.md: {agent_id} - {message}",
    ):
        print(f"✅ Agentconvo logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return dev_tools.quick_commit_push(
            f"Update agentconvo.md: {agent_id} - {message}", "💬"
        )


def update_agent_memory(
    agent_id: str, memory_type: str, content: str, memory_branch: str = None
) -> bool:
    """
    Appends a memory entry for an agent to a markdown log and commits it to a memory branch.
    
    If the memory branch commit fails, falls back to a regular commit on the current branch.
    
    Args:
        agent_id: Identifier for the agent whose memory is being updated.
        memory_type: Category of the memory entry (e.g., progress, decision).
        content: The memory content to append.
        memory_branch: Optional branch name for memory storage; auto-generated if not provided.
    
    Returns:
        True if the memory update and commit succeed, False otherwise.
    """
    memory_file = f".agor/{agent_id.lower()}-memory.md"
    timestamp = dev_tools.get_current_timestamp()

    if not memory_branch:
        memory_branch = f"agor/mem/{dev_tools.get_timestamp_for_files()}"

    print(f"🧠 Updating {agent_id} memory: {memory_type}")

    # Create or update memory content
    memory_entry = f"""
## {memory_type.title()} - {timestamp}

{content}

---
"""

    # Write memory file to current working directory
    memory_path = dev_tools.repo_path / memory_file
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if memory_path.exists():
        with open(memory_path, "a") as f:
            f.write(memory_entry)
    else:
        initial_content = f"""# {agent_id.title()} Memory Log

## Current Task
[Describe the task you're working on]

## Decisions Made
- [Key architectural choices]
- [Implementation approaches]

## Files Modified
- [List of changed files with brief description]

## Problems Encountered
- [Issues hit and how resolved]

## Next Steps
- [What needs to be done next]

{memory_entry}
"""
        memory_path.write_text(initial_content)

    # Try to commit to memory branch using new safe system
    if dev_tools._commit_to_memory_branch(
        memory_file, memory_branch, f"Update {agent_id} memory: {memory_type}"
    ):
        print(f"✅ Agent memory logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return dev_tools.quick_commit_push(
            f"Update {agent_id} memory: {memory_type}", "🧠"
        )
