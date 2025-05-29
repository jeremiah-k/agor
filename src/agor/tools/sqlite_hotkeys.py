"""
SQLite Memory Hotkey Implementations for AGOR.

Provides hotkey implementations for SQLite memory management to ensure
parity with markdown-based memory system. These hotkeys enable agents
to interact with the SQLite database through familiar commands.
"""

import json
from pathlib import Path

from .sqlite_memory import (
    SQLiteMemoryManager,
    get_memory_manager,
    validate_sqlite_setup,
)


def mem_add_hotkey() -> str:
    """
    Hotkey: mem-add
    Add a memory entry to the SQLite database.

    Interactive prompt for agent to add structured memory.
    """
    print("🗄️ Add Memory Entry to SQLite Database")
    print("=" * 50)

    # Get memory manager
    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Interactive input
    agent_id = input("Agent ID (e.g., agent-1): ").strip()
    if not agent_id:
        return "❌ Agent ID is required"

    print("\nMemory Types:")
    print("- context: Situational information and background")
    print("- decision: Choices made and reasoning")
    print("- learning: Insights and knowledge gained")
    print("- snapshot: Snapshot-related information")
    print("- action: Actions taken and their results")

    memory_type = input("Memory type: ").strip()
    if not memory_type:
        return "❌ Memory type is required"

    content = input("Memory content: ").strip()
    if not content:
        return "❌ Memory content is required"

    # Optional metadata
    metadata_input = input("Metadata (JSON, optional): ").strip()
    metadata = None
    if metadata_input:
        try:
            metadata = json.loads(metadata_input)
        except json.JSONDecodeError:
            return "❌ Invalid JSON metadata format"

    # Add memory
    try:
        memory_id = manager.add_memory(agent_id, memory_type, content, metadata)
        return f"✅ Memory added successfully (ID: {memory_id})"
    except Exception as e:
        return f"❌ Error adding memory: {e}"


def mem_get_hotkey() -> str:
    """
    Hotkey: mem-get
    Retrieve memories from SQLite database.

    Interactive prompt to get agent memories with filtering options.
    """
    print("🗄️ Retrieve Memories from SQLite Database")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get parameters
    agent_id = input("Agent ID (required): ").strip()
    if not agent_id:
        return "❌ Agent ID is required"

    memory_type = input("Memory type (optional, press Enter for all): ").strip()
    memory_type = memory_type if memory_type else None

    limit_input = input("Limit (default 20): ").strip()
    try:
        limit = int(limit_input) if limit_input else 20
    except ValueError:
        return "❌ Invalid limit value"

    # Retrieve memories
    try:
        memories = manager.get_memories(agent_id, memory_type, limit)

        if not memories:
            return f"📭 No memories found for {agent_id}"

        # Format output
        output = [f"📋 Found {len(memories)} memories for {agent_id}"]
        output.append("=" * 50)

        for i, memory in enumerate(memories, 1):
            output.append(
                f"\n{i}. [{memory['memory_type'].upper()}] {memory['created_at']}"
            )
            output.append(f"   {memory['content']}")
            if memory["metadata"]:
                try:
                    metadata = json.loads(memory["metadata"])
                    output.append(f"   Metadata: {metadata}")
                except json.JSONDecodeError:
                    output.append(f"   Metadata: {memory['metadata']}")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error retrieving memories: {e}"


def mem_search_hotkey() -> str:
    """
    Hotkey: mem-search
    Search memory content in SQLite database.

    Full-text search across all memories with filtering options.
    """
    print("🔍 Search Memory Content in SQLite Database")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get search parameters
    query = input("Search query: ").strip()
    if not query:
        return "❌ Search query is required"

    agent_id = input("Agent ID (optional, press Enter for all agents): ").strip()
    agent_id = agent_id if agent_id else None

    memory_type = input("Memory type (optional, press Enter for all types): ").strip()
    memory_type = memory_type if memory_type else None

    limit_input = input("Limit (default 20): ").strip()
    try:
        limit = int(limit_input) if limit_input else 20
    except ValueError:
        return "❌ Invalid limit value"

    # Perform search
    try:
        results = manager.search_memories(query, agent_id, memory_type, limit)

        if not results:
            return f"🔍 No memories found matching '{query}'"

        # Format output
        output = [f"🔍 Found {len(results)} memories matching '{query}'"]
        output.append("=" * 50)

        for i, result in enumerate(results, 1):
            output.append(
                f"\n{i}. [{result['agent_id']}] [{result['memory_type'].upper()}] {result['created_at']}"
            )
            # Highlight search term (simple approach)
            content = result["content"]
            highlighted = content.replace(query, f"**{query}**")
            output.append(f"   {highlighted}")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error searching memories: {e}"


def coord_log_hotkey() -> str:
    """
    Hotkey: coord-log
    Log coordination message between agents.

    Records agent-to-agent communication in SQLite database.
    """
    print("🤝 Log Coordination Message")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get coordination parameters
    from_agent = input("From agent ID: ").strip()
    if not from_agent:
        return "❌ From agent ID is required"

    to_agent = input("To agent ID: ").strip()
    if not to_agent:
        return "❌ To agent ID is required"

    print("\nMessage Types:")
    print("- communication: General communication")
    print("- snapshot: Work snapshot")
    print("- question: Question to another agent")
    print("- response: Response to a question")
    print("- status: Status update")

    message_type = input("Message type: ").strip()
    if not message_type:
        return "❌ Message type is required"

    message = input("Message content: ").strip()
    if not message:
        return "❌ Message content is required"

    # Log coordination
    try:
        log_id = manager.log_coordination(from_agent, to_agent, message_type, message)
        return f"✅ Coordination message logged successfully (ID: {log_id})"
    except Exception as e:
        return f"❌ Error logging coordination: {e}"


def state_set_hotkey() -> str:
    """
    Hotkey: state-set
    Set project state in SQLite database.

    Stores project-level state information.
    """
    print("📊 Set Project State")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get state parameters
    state_key = input("State key (e.g., 'project_status', 'team_config'): ").strip()
    if not state_key:
        return "❌ State key is required"

    print("\nEnter state data as JSON:")
    state_input = input("State data: ").strip()
    if not state_input:
        return "❌ State data is required"

    # Parse state data
    try:
        state_data = json.loads(state_input)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON format: {e}"

    # Set state
    try:
        manager.set_project_state(state_key, state_data)
        return f"✅ Project state '{state_key}' set successfully"
    except Exception as e:
        return f"❌ Error setting project state: {e}"


def state_get_hotkey() -> str:
    """
    Hotkey: state-get
    Get project state from SQLite database.

    Retrieves project-level state information.
    """
    print("📊 Get Project State")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get state key
    state_key = input("State key (press Enter to list all): ").strip()

    if not state_key:
        # List all state keys
        try:
            # Get all project states (this requires a new method)
            stats = manager.get_database_stats()
            if stats["project_state"] == 0:
                return "📭 No project states found"

            # For now, suggest common state keys
            return """📊 Common project state keys:
- project_status: Overall project status and progress
- team_config: Team configuration and roles
- development_phase: Current development phase
- key_decisions: Major project decisions
- completion_metrics: Progress and completion data

Use 'state-get' with a specific key to retrieve state data."""
        except Exception as e:
            return f"❌ Error accessing project states: {e}"

    # Get specific state
    try:
        state_data = manager.get_project_state(state_key)

        if state_data is None:
            return f"📭 No state found for key '{state_key}'"

        # Format output
        output = [f"📊 Project State: {state_key}"]
        output.append("=" * 50)
        output.append(json.dumps(state_data, indent=2))

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error retrieving project state: {e}"


def snapshot_create_hotkey() -> str:
    """
    Hotkey: snapshot-create
    Create snapshot record in SQLite database.

    Creates structured snapshot with all necessary information.
    """
    print("🤝 Create Database Snapshot")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get snapshot information
    snapshot_id = input("Snapshot ID (e.g., 'snapshot-001'): ").strip()
    if not snapshot_id:
        return "❌ Snapshot ID is required"

    from_agent = input("From agent: ").strip()
    if not from_agent:
        return "❌ From agent is required"

    to_agent = input("To agent (optional): ").strip()
    to_agent = to_agent if to_agent else None

    problem_description = input("Problem description: ").strip()
    if not problem_description:
        return "❌ Problem description is required"

    work_completed = input("Work completed: ").strip()
    commits_made = input("Commits made: ").strip()
    files_modified = input("Files modified: ").strip()
    current_status = input("Current status: ").strip()
    next_steps = input("Next steps: ").strip()
    context_notes = input("Context notes: ").strip()
    git_branch = input("Git branch: ").strip()
    git_commit = input("Git commit: ").strip()

    # Get AGOR version
    try:
        from agor import __version__

        agor_version = __version__
    except ImportError:
        agor_version = "unknown"

    # Create snapshot
    try:
        snapshot_db_id = manager.create_snapshot(
            snapshot_id=snapshot_id,
            from_agent=from_agent,
            to_agent=to_agent,
            problem_description=problem_description,
            work_completed=work_completed,
            commits_made=commits_made,
            files_modified=files_modified,
            current_status=current_status,
            next_steps=next_steps,
            context_notes=context_notes,
            git_branch=git_branch,
            git_commit=git_commit,
            agor_version=agor_version,
        )

        return (
            f"✅ Snapshot '{snapshot_id}' created successfully (DB ID: {snapshot_db_id})"
        )

    except Exception as e:
        return f"❌ Error creating snapshot: {e}"


def snapshot_status_hotkey() -> str:
    """
    Hotkey: snapshot-status
    Update snapshot status in SQLite database.

    Updates the status of an existing snapshot.
    """
    print("🔄 Update Snapshot Status")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    # Get handoff ID
    handoff_id = input("Handoff ID: ").strip()
    if not handoff_id:
        return "❌ Handoff ID is required"

    # Check if handoff exists
    handoff = manager.get_handoff(handoff_id)
    if not handoff:
        return f"❌ Handoff '{handoff_id}' not found"

    print(f"\nCurrent status: {handoff['status']}")
    print("\nAvailable statuses:")
    print("- active: Handoff is active and waiting")
    print("- received: Handoff has been received")
    print("- completed: Handoff work is completed")

    new_status = input("New status: ").strip()
    if not new_status:
        return "❌ New status is required"

    # Update status
    try:
        manager.update_handoff_status(handoff_id, new_status)
        return f"✅ Handoff '{handoff_id}' status updated to '{new_status}'"
    except Exception as e:
        return f"❌ Error updating handoff status: {e}"


def db_stats_hotkey() -> str:
    """
    Hotkey: db-stats
    Show SQLite database statistics.

    Displays record counts and database information.
    """
    print("📊 SQLite Database Statistics")
    print("=" * 50)

    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"

    try:
        stats = manager.get_database_stats()

        # Format output
        output = ["📊 Database Statistics"]
        output.append("=" * 30)
        output.append(f"Agent Memories: {stats['agent_memories']}")
        output.append(f"Coordination Logs: {stats['coordination_logs']}")
        output.append(f"Project States: {stats['project_state']}")
        output.append(f"Handoffs: {stats['handoffs']}")
        output.append("")

        # Database file info
        db_path = Path(manager.db_path)
        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            output.append(f"Database File: {db_path}")
            output.append(f"File Size: {size_mb:.2f} MB")

        total_records = sum(stats.values())
        output.append(f"Total Records: {total_records}")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error retrieving database statistics: {e}"


def sqlite_validate_hotkey() -> str:
    """
    Hotkey: sqlite-validate
    Validate SQLite memory system setup and path resolution.
    """
    print("🔍 SQLite Memory System Validation")
    print("=" * 50)

    # Test validation
    success, message = validate_sqlite_setup()

    if success:
        print(f"✅ {message}")

        # Show additional info
        try:
            manager = get_memory_manager()
            print(f"💾 Database Path: {manager.db_path}")
            print(f"📁 Database Exists: {manager.db_path.exists()}")
            print(
                f"💾 Database Size: {manager.db_path.stat().st_size if manager.db_path.exists() else 0} bytes"
            )

            # Test basic operations
            stats = manager.get_database_stats()
            print(f"📊 Total Records: {sum(stats.values())}")

        except Exception as e:
            print(f"⚠️ Additional info error: {e}")

        return "✅ SQLite memory system validation successful"
    else:
        print(f"❌ {message}")
        return f"❌ SQLite validation failed: {message}"


def mem_sync_start_hotkey() -> str:
    """
    Hotkey: mem-sync-start
    Initialize memory branch and sync on startup.

    Sets up memory synchronization with Git-based persistence.
    """
    print("🔄 Memory Sync: Initialize and Start")
    print("=" * 50)

    try:
        # Import memory sync manager
        import sys
        from pathlib import Path

        # Add src to path for development environments
        repo_root = Path.cwd()
        if (repo_root / "src").exists():
            sys.path.insert(0, str(repo_root / "src"))

        from agor.memory_sync import MemorySyncManager

        # Initialize memory sync manager
        manager = MemorySyncManager()

        # Get preferred branch name from user
        preferred_branch = input("Preferred memory branch name (optional): ").strip()
        preferred_branch = preferred_branch if preferred_branch else None

        print("\n🚀 Starting memory synchronization...")

        # Perform startup sync
        success = manager.auto_sync_on_startup(preferred_branch)

        if success:
            active_branch = manager.get_active_memory_branch()
            if active_branch:
                return f"✅ Memory sync started successfully on branch: {active_branch}"
            else:
                return "✅ Memory sync started successfully"
        else:
            return "❌ Failed to start memory synchronization"

    except ImportError as e:
        return f"❌ Memory sync not available: {e}"
    except Exception as e:
        return f"❌ Error starting memory sync: {e}"


def mem_sync_save_hotkey() -> str:
    """
    Hotkey: mem-sync-save
    Save current memory state to memory branch.

    Commits current memory files to the active memory branch.
    """
    print("💾 Memory Sync: Save Current State")
    print("=" * 50)

    try:
        # Import memory sync manager
        import sys
        from pathlib import Path

        # Add src to path for development environments
        repo_root = Path.cwd()
        if (repo_root / "src").exists():
            sys.path.insert(0, str(repo_root / "src"))

        from agor.memory_sync import MemorySyncManager
        from agor.tools.dev_tooling import get_precise_timestamp

        # Initialize memory sync manager
        manager = MemorySyncManager()

        # Check if we're on a memory branch
        active_branch = manager.get_active_memory_branch()
        if not active_branch:
            return "❌ Not currently on a memory branch. Use mem-sync-start first."

        # Get commit message from user
        default_message = f"Save memory state at {get_precise_timestamp()}"
        commit_message = input(f"Commit message (default: '{default_message}'): ").strip()
        commit_message = commit_message if commit_message else default_message

        print(f"\n💾 Saving memory state to branch: {active_branch}")

        # Perform save operation (without restoring original branch)
        success = manager.auto_sync_on_shutdown(
            active_branch,
            commit_message,
            push_changes=True,
            restore_original_branch=None  # Stay on memory branch
        )

        if success:
            return f"✅ Memory state saved successfully to {active_branch}"
        else:
            return "❌ Failed to save memory state"

    except ImportError as e:
        return f"❌ Memory sync not available: {e}"
    except Exception as e:
        return f"❌ Error saving memory state: {e}"


def mem_sync_restore_hotkey() -> str:
    """
    Hotkey: mem-sync-restore
    Restore memory state from a memory branch.

    Switches to and pulls latest state from a memory branch.
    """
    print("🔄 Memory Sync: Restore from Branch")
    print("=" * 50)

    try:
        # Import memory sync manager
        import sys
        from pathlib import Path

        # Add src to path for development environments
        repo_root = Path.cwd()
        if (repo_root / "src").exists():
            sys.path.insert(0, str(repo_root / "src"))

        from agor.memory_sync import MemorySyncManager

        # Initialize memory sync manager
        manager = MemorySyncManager()

        # List available memory branches
        local_branches = manager.list_memory_branches(remote=False)
        remote_branches = manager.list_memory_branches(remote=True)

        all_branches = sorted(list(set(local_branches + remote_branches)), reverse=True)

        if not all_branches:
            return "❌ No memory branches found. Use mem-sync-start to create one."

        print("\nAvailable memory branches:")
        for i, branch in enumerate(all_branches, 1):
            location = "local" if branch in local_branches else "remote"
            print(f"  {i}. {branch} ({location})")

        # Get user selection
        try:
            selection = input("\nSelect branch number (or enter branch name): ").strip()

            if selection.isdigit():
                branch_index = int(selection) - 1
                if 0 <= branch_index < len(all_branches):
                    target_branch = all_branches[branch_index]
                else:
                    return "❌ Invalid branch selection"
            else:
                target_branch = selection
                if not target_branch.startswith(manager.MEMORY_BRANCH_PREFIX):
                    target_branch = manager.MEMORY_BRANCH_PREFIX + target_branch
        except ValueError:
            return "❌ Invalid selection"

        print(f"\n🔄 Restoring from memory branch: {target_branch}")

        # Ensure branch exists and switch to it
        success = manager.ensure_memory_branch_exists(
            target_branch,
            switch_if_exists=True,
            attempt_pull=True
        )

        if success:
            return f"✅ Successfully restored memory state from {target_branch}"
        else:
            return f"❌ Failed to restore from memory branch {target_branch}"

    except ImportError as e:
        return f"❌ Memory sync not available: {e}"
    except Exception as e:
        return f"❌ Error restoring memory state: {e}"


def mem_sync_status_hotkey() -> str:
    """
    Hotkey: mem-sync-status
    Show current memory synchronization status.

    Displays active branch, available branches, and sync state.
    """
    print("📊 Memory Sync: Status Overview")
    print("=" * 50)

    try:
        # Import memory sync manager
        import sys
        from pathlib import Path

        # Add src to path for development environments
        repo_root = Path.cwd()
        if (repo_root / "src").exists():
            sys.path.insert(0, str(repo_root / "src"))

        from agor.memory_sync import MemorySyncManager

        # Initialize memory sync manager
        manager = MemorySyncManager()

        output = []

        # Current branch status
        active_branch = manager.get_active_memory_branch()
        if active_branch:
            output.append(f"🌿 Active memory branch: {active_branch}")
        else:
            output.append("📝 Not currently on a memory branch")

        # List available branches
        local_branches = manager.list_memory_branches(remote=False)
        remote_branches = manager.list_memory_branches(remote=True)

        if local_branches:
            output.append(f"\n📁 Local memory branches ({len(local_branches)}):")
            for branch in sorted(local_branches, reverse=True):
                marker = " (active)" if branch == active_branch else ""
                output.append(f"  • {branch}{marker}")

        if remote_branches:
            output.append(f"\n🌐 Remote memory branches ({len(remote_branches)}):")
            for branch in sorted(remote_branches, reverse=True):
                output.append(f"  • {branch}")

        if not local_branches and not remote_branches:
            output.append("\n❌ No memory branches found")
            output.append("💡 Use 'mem-sync-start' to initialize memory synchronization")

        # Memory file status
        memory_file_path = manager.repo_path / manager.memory_file_relative_path
        if memory_file_path.exists():
            output.append(f"\n💾 Memory file: {manager.memory_file_relative_path} (exists)")
        else:
            output.append(f"\n⚠️  Memory file: {manager.memory_file_relative_path} (not found)")

        return "\n".join(output)

    except ImportError as e:
        return f"❌ Memory sync not available: {e}"
    except Exception as e:
        return f"❌ Error checking memory sync status: {e}"


# Hotkey registry for SQLite memory commands
SQLITE_HOTKEY_REGISTRY = {
    "mem-add": mem_add_hotkey,
    "mem-get": mem_get_hotkey,
    "mem-search": mem_search_hotkey,
    "coord-log": coord_log_hotkey,
    "state-set": state_set_hotkey,
    "state-get": state_get_hotkey,
    "handoff-create": handoff_create_hotkey,
    "handoff-status": handoff_status_hotkey,
    "db-stats": db_stats_hotkey,
    "sqlite-validate": sqlite_validate_hotkey,
    # Memory synchronization hotkeys
    "mem-sync-start": mem_sync_start_hotkey,
    "mem-sync-save": mem_sync_save_hotkey,
    "mem-sync-restore": mem_sync_restore_hotkey,
    "mem-sync-status": mem_sync_status_hotkey,
}


def execute_sqlite_hotkey(hotkey: str) -> str:
    """
    Execute a SQLite memory hotkey command.

    Args:
        hotkey: The hotkey command to execute

    Returns:
        Result message from the hotkey execution
    """
    if hotkey not in SQLITE_HOTKEY_REGISTRY:
        available = ", ".join(SQLITE_HOTKEY_REGISTRY.keys())
        return f"❌ Unknown SQLite hotkey '{hotkey}'. Available: {available}"

    try:
        return SQLITE_HOTKEY_REGISTRY[hotkey]()
    except Exception as e:
        return f"❌ Error executing hotkey '{hotkey}': {e}"


def get_sqlite_hotkey_help() -> str:
    """Get help text for SQLite memory hotkeys."""
    return """🗄️ **SQLite Memory Commands:**

**Memory Management:**
- `mem-add` - Add memory entry for an agent
- `mem-get` - Retrieve memories for an agent
- `mem-search` - Search memory content across agents

**Memory Synchronization:**
- `mem-sync-start` - Initialize memory branch and sync on startup
- `mem-sync-save` - Save current memory state to memory branch
- `mem-sync-restore` - Restore memory state from a memory branch
- `mem-sync-status` - Show current memory synchronization status

**Coordination:**
- `coord-log` - Log coordination message between agents

**Project State:**
- `state-set` - Set project state data
- `state-get` - Get project state data

**Handoffs:**
- `handoff-create` - Create database handoff record
- `handoff-status` - Update handoff status

**Database:**
- `db-stats` - Show database statistics and record counts
- `sqlite-validate` - Validate SQLite setup and path resolution

**Note:** SQLite memory system provides structured storage alternative to markdown files.
Database location: `.agor/memory.db`
Memory sync uses Git branches with prefix: `agor/mem/`
"""


def check_sqlite_availability() -> bool:
    """
    Check if SQLite memory system is available.

    Returns:
        True if SQLite is available and working, False otherwise
    """
    try:
        # Try to create a temporary memory manager
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            manager = SQLiteMemoryManager(tmp.name)
            # Try a basic operation
            manager.add_memory("test", "context", "test")
            return True
    except Exception:
        return False
