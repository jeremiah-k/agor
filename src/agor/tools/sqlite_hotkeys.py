"""
SQLite Memory Hotkey Implementations for AGOR.

Provides hotkey implementations for SQLite memory management to ensure
parity with markdown-based memory system. These hotkeys enable agents
to interact with the SQLite database through familiar commands.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from .sqlite_memory import SQLiteMemoryManager, get_memory_manager


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
    print("- handoff: Handoff-related information")
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
            output.append(f"\n{i}. [{memory['memory_type'].upper()}] {memory['created_at']}")
            output.append(f"   {memory['content']}")
            if memory['metadata']:
                try:
                    metadata = json.loads(memory['metadata'])
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
            output.append(f"\n{i}. [{result['agent_id']}] [{result['memory_type'].upper()}] {result['created_at']}")
            # Highlight search term (simple approach)
            content = result['content']
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
    print("- handoff: Work handoff")
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


def handoff_create_hotkey() -> str:
    """
    Hotkey: handoff-create
    Create handoff record in SQLite database.
    
    Creates structured handoff with all necessary information.
    """
    print("🤝 Create Database Handoff")
    print("=" * 50)
    
    try:
        manager = get_memory_manager()
    except Exception as e:
        return f"❌ Error accessing SQLite database: {e}"
    
    # Get handoff information
    handoff_id = input("Handoff ID (e.g., 'handoff-001'): ").strip()
    if not handoff_id:
        return "❌ Handoff ID is required"
    
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
    
    # Create handoff
    try:
        handoff_db_id = manager.create_handoff(
            handoff_id=handoff_id,
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
            agor_version=agor_version
        )
        
        return f"✅ Handoff '{handoff_id}' created successfully (DB ID: {handoff_db_id})"
        
    except Exception as e:
        return f"❌ Error creating handoff: {e}"


def handoff_status_hotkey() -> str:
    """
    Hotkey: handoff-status
    Update handoff status in SQLite database.
    
    Updates the status of an existing handoff.
    """
    print("🔄 Update Handoff Status")
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

**Note:** SQLite memory system provides structured storage alternative to markdown files.
Database location: `.agor/memory.db`
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
