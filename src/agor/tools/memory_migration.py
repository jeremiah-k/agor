"""
Memory Migration Utilities for AGOR.

Provides bidirectional migration between markdown-based memory system
and SQLite-based memory system to ensure interoperability and allow
users to switch between systems seamlessly.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .sqlite_memory import SQLiteMemoryManager


class MemoryMigrationManager:
    """Manages migration between markdown and SQLite memory systems."""

    def __init__(self, agor_dir: Path):
        """Initialize migration manager."""
        self.agor_dir = Path(agor_dir)
        self.db_path = self.agor_dir / "memory.db"
        self.sqlite_manager = SQLiteMemoryManager(str(self.db_path))

    def migrate_markdown_to_sqlite(self, preserve_markdown: bool = True) -> Dict[str, int]:
        """
        Migrate markdown memory files to SQLite database.

        Args:
            preserve_markdown: If True, keep original markdown files

        Returns:
            Dictionary with migration statistics
        """
        stats = {
            "agent_memories": 0,
            "coordination_logs": 0,
            "project_state": 0,
            "handoffs": 0,
            "errors": 0
        }

        try:
            # Migrate project memory (memory.md)
            memory_file = self.agor_dir / "memory.md"
            if memory_file.exists():
                project_data = self._parse_project_memory(memory_file)
                if project_data:
                    self.sqlite_manager.set_project_state("project_overview", project_data)
                    stats["project_state"] += 1

            # Migrate agent memory files (agent{N}-memory.md)
            agent_files = list(self.agor_dir.glob("agent*-memory.md"))
            for agent_file in agent_files:
                agent_id = self._extract_agent_id(agent_file.name)
                if agent_id:
                    memories = self._parse_agent_memory(agent_file)
                    for memory_type, content, metadata in memories:
                        self.sqlite_manager.add_memory(agent_id, memory_type, content, metadata)
                        stats["agent_memories"] += 1

            # Migrate agent communication (agentconvo.md)
            agentconvo_file = self.agor_dir / "agentconvo.md"
            if agentconvo_file.exists():
                coord_logs = self._parse_agentconvo(agentconvo_file)
                for from_agent, to_agent, msg_type, message, timestamp in coord_logs:
                    self.sqlite_manager.log_coordination(from_agent, to_agent, msg_type, message)
                    stats["coordination_logs"] += 1

            # Migrate handoff files
            handoff_dir = self.agor_dir / "handoffs"
            if handoff_dir.exists():
                handoff_files = list(handoff_dir.glob("*.md"))
                for handoff_file in handoff_files:
                    handoff_data = self._parse_handoff_file(handoff_file)
                    if handoff_data:
                        self.sqlite_manager.create_handoff(**handoff_data)
                        stats["handoffs"] += 1

            # Optionally backup markdown files
            if not preserve_markdown:
                self._backup_markdown_files()

        except Exception as e:
            stats["errors"] += 1
            print(f"❌ Migration error: {e}")

        return stats

    def migrate_sqlite_to_markdown(self, overwrite_existing: bool = False) -> Dict[str, int]:
        """
        Migrate SQLite database to markdown memory files.

        Args:
            overwrite_existing: If True, overwrite existing markdown files

        Returns:
            Dictionary with migration statistics
        """
        stats = {
            "agent_memory_files": 0,
            "coordination_entries": 0,
            "project_state_entries": 0,
            "handoff_files": 0,
            "errors": 0
        }

        try:
            # Get all unique agent IDs from database
            agent_ids = self._get_all_agent_ids()

            # Create agent memory files
            for agent_id in agent_ids:
                agent_file = self.agor_dir / f"{agent_id}-memory.md"

                if agent_file.exists() and not overwrite_existing:
                    print(f"⚠️  Skipping {agent_file.name} (already exists)")
                    continue

                memories = self.sqlite_manager.get_memories(agent_id, limit=1000)
                if memories:
                    markdown_content = self._generate_agent_memory_markdown(agent_id, memories)
                    agent_file.write_text(markdown_content)
                    stats["agent_memory_files"] += 1

            # Create/update agentconvo.md
            agentconvo_file = self.agor_dir / "agentconvo.md"
            coord_logs = self._get_all_coordination_logs()
            if coord_logs:
                if agentconvo_file.exists() and not overwrite_existing:
                    # Append new entries
                    existing_content = agentconvo_file.read_text()
                    new_entries = self._generate_agentconvo_entries(coord_logs)
                    agentconvo_file.write_text(existing_content + "\n" + new_entries)
                else:
                    # Create new file
                    markdown_content = self._generate_agentconvo_markdown(coord_logs)
                    agentconvo_file.write_text(markdown_content)
                stats["coordination_entries"] += len(coord_logs)

            # Create/update memory.md with project state
            memory_file = self.agor_dir / "memory.md"
            project_state = self.sqlite_manager.get_project_state("project_overview")
            if project_state:
                if memory_file.exists() and not overwrite_existing:
                    print(f"⚠️  Skipping {memory_file.name} (already exists)")
                else:
                    markdown_content = self._generate_project_memory_markdown(project_state)
                    memory_file.write_text(markdown_content)
                    stats["project_state_entries"] += 1

            # Create handoff files
            handoffs = self._get_all_handoffs()
            handoff_dir = self.agor_dir / "handoffs"
            handoff_dir.mkdir(exist_ok=True)

            for handoff in handoffs:
                handoff_file = handoff_dir / f"{handoff['handoff_id']}.md"
                if handoff_file.exists() and not overwrite_existing:
                    continue

                markdown_content = self._generate_handoff_markdown(handoff)
                handoff_file.write_text(markdown_content)
                stats["handoff_files"] += 1

        except Exception as e:
            stats["errors"] += 1
            print(f"❌ Migration error: {e}")

        return stats

    def sync_systems(self, direction: str = "bidirectional") -> Dict[str, int]:
        """
        Synchronize between markdown and SQLite systems.

        Args:
            direction: "markdown_to_sqlite", "sqlite_to_markdown", or "bidirectional"

        Returns:
            Dictionary with sync statistics
        """
        stats = {"total_synced": 0, "errors": 0}

        try:
            if direction in ["markdown_to_sqlite", "bidirectional"]:
                md_stats = self.migrate_markdown_to_sqlite(preserve_markdown=True)
                stats.update({f"md_to_sql_{k}": v for k, v in md_stats.items()})
                stats["total_synced"] += sum(md_stats.values()) - md_stats.get("errors", 0)

            if direction in ["sqlite_to_markdown", "bidirectional"]:
                sql_stats = self.migrate_sqlite_to_markdown(overwrite_existing=False)
                stats.update({f"sql_to_md_{k}": v for k, v in sql_stats.items()})
                stats["total_synced"] += sum(sql_stats.values()) - sql_stats.get("errors", 0)

        except Exception as e:
            stats["errors"] += 1
            print(f"❌ Sync error: {e}")

        return stats

    def _parse_project_memory(self, memory_file: Path) -> Optional[Dict]:
        """Parse project memory.md file into structured data."""
        try:
            content = memory_file.read_text()

            # Extract structured information
            project_data = {
                "source": "memory.md",
                "migrated_at": datetime.now().isoformat()
            }

            # Parse task
            task_match = re.search(r"## Task\s*\n(.+?)(?=\n##|\n$)", content, re.DOTALL)
            if task_match:
                project_data["task"] = task_match.group(1).strip()

            # Parse team configuration
            team_match = re.search(r"## Team Configuration\s*\n(.+?)(?=\n##|\n$)", content, re.DOTALL)
            if team_match:
                project_data["team_configuration"] = team_match.group(1).strip()

            # Parse key decisions
            decisions_match = re.search(r"## Key Decisions\s*\n(.+?)(?=\n##|\n$)", content, re.DOTALL)
            if decisions_match:
                project_data["key_decisions"] = decisions_match.group(1).strip()

            # Parse current state
            state_match = re.search(r"## Current State\s*\n(.+?)(?=\n##|\n$)", content, re.DOTALL)
            if state_match:
                project_data["current_state"] = state_match.group(1).strip()

            return project_data

        except Exception as e:
            print(f"❌ Error parsing {memory_file}: {e}")
            return None

    def _parse_agent_memory(self, agent_file: Path) -> List[Tuple[str, str, Optional[Dict]]]:
        """Parse agent memory file into structured memories."""
        memories = []

        try:
            content = agent_file.read_text()

            # Split content by sections
            sections = re.split(r'\n## ', content)

            for section in sections[1:]:  # Skip first empty section
                lines = section.split('\n', 1)
                if len(lines) < 2:
                    continue

                section_title = lines[0].strip()
                section_content = lines[1].strip()

                # Map section titles to memory types
                memory_type = self._map_section_to_memory_type(section_title)

                if memory_type and section_content:
                    # Extract metadata if present (simple approach)
                    metadata = None
                    if "Metadata:" in section_content:
                        try:
                            metadata_match = re.search(r"Metadata:\s*({.+?})", section_content)
                            if metadata_match:
                                metadata = json.loads(metadata_match.group(1))
                        except json.JSONDecodeError:
                            pass

                    memories.append((memory_type, section_content, metadata))

        except Exception as e:
            print(f"❌ Error parsing {agent_file}: {e}")

        return memories

    def _parse_agentconvo(self, agentconvo_file: Path) -> List[Tuple[str, str, str, str, str]]:
        """Parse agentconvo.md file into coordination logs."""
        coord_logs = []

        try:
            content = agentconvo_file.read_text()

            # Parse entries with format: [AGENT-ID] [TIMESTAMP] - [MESSAGE]
            pattern = r'\[([^\]]+)\]\s*\[([^\]]+)\]\s*-\s*(.+)'
            matches = re.findall(pattern, content, re.MULTILINE)

            for agent_id, timestamp, message in matches:
                # Determine message type and target agent
                msg_type = "communication"
                to_agent = "all"  # Default to broadcast

                if "handoff" in message.lower():
                    msg_type = "handoff"
                elif "question" in message.lower() or "?" in message:
                    msg_type = "question"
                elif "status" in message.lower():
                    msg_type = "status"

                coord_logs.append((agent_id.strip(), to_agent, msg_type, message.strip(), timestamp.strip()))

        except Exception as e:
            print(f"❌ Error parsing {agentconvo_file}: {e}")

        return coord_logs

    def _parse_handoff_file(self, handoff_file: Path) -> Optional[Dict]:
        """Parse handoff markdown file into structured data."""
        try:
            content = handoff_file.read_text()

            # Extract handoff ID from filename
            handoff_id = handoff_file.stem

            # Parse handoff sections
            handoff_data = {
                "handoff_id": handoff_id,
                "from_agent": "unknown",
                "to_agent": None,
                "problem_description": "",
                "work_completed": "",
                "commits_made": "",
                "files_modified": "",
                "current_status": "",
                "next_steps": "",
                "context_notes": "",
                "git_branch": "",
                "git_commit": "",
                "agor_version": "unknown"
            }

            # Simple parsing - look for common patterns
            sections = {
                "problem_description": r"## Problem Description\s*\n(.+?)(?=\n##|\n$)",
                "work_completed": r"## Work Completed\s*\n(.+?)(?=\n##|\n$)",
                "commits_made": r"## Commits Made\s*\n(.+?)(?=\n##|\n$)",
                "files_modified": r"## Files Modified\s*\n(.+?)(?=\n##|\n$)",
                "current_status": r"## Current Status\s*\n(.+?)(?=\n##|\n$)",
                "next_steps": r"## Next Steps\s*\n(.+?)(?=\n##|\n$)",
                "context_notes": r"## Context Notes\s*\n(.+?)(?=\n##|\n$)",
            }

            for field, pattern in sections.items():
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    handoff_data[field] = match.group(1).strip()

            return handoff_data

        except Exception as e:
            print(f"❌ Error parsing {handoff_file}: {e}")
            return None

    def _extract_agent_id(self, filename: str) -> Optional[str]:
        """Extract agent ID from filename like 'agent1-memory.md' or 'agent-1-memory.md'."""
        # Handle both agent1-memory.md and agent-1-memory.md formats
        match = re.match(r'(agent-?\d+)-memory\.md', filename)
        if match:
            agent_id = match.group(1)
            # Normalize to agent-N format
            if not agent_id.startswith('agent-'):
                agent_id = agent_id.replace('agent', 'agent-')
            return agent_id
        return None

    def _map_section_to_memory_type(self, section_title: str) -> Optional[str]:
        """Map markdown section title to memory type."""
        title_lower = section_title.lower()

        if any(word in title_lower for word in ["decision", "choice", "chose"]):
            return "decision"
        elif any(word in title_lower for word in ["context", "background", "situation"]):
            return "context"
        elif any(word in title_lower for word in ["learning", "learned", "insight"]):
            return "learning"
        elif any(word in title_lower for word in ["handoff", "transition"]):
            return "handoff"
        elif any(word in title_lower for word in ["action", "did", "completed"]):
            return "action"
        else:
            return "context"  # Default type

    def _get_all_agent_ids(self) -> List[str]:
        """Get all unique agent IDs from SQLite database."""
        try:
            with self.sqlite_manager._get_connection() as conn:
                cursor = conn.execute("SELECT DISTINCT agent_id FROM agent_memories")
                return [row[0] for row in cursor.fetchall()]
        except Exception:
            return []

    def _get_all_coordination_logs(self) -> List[Dict]:
        """Get all coordination logs from SQLite database."""
        try:
            import sqlite3
            with self.sqlite_manager._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM coordination_logs ORDER BY created_at"
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []

    def _get_all_handoffs(self) -> List[Dict]:
        """Get all handoffs from SQLite database."""
        try:
            import sqlite3
            with self.sqlite_manager._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM handoffs ORDER BY created_at")
                return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []

    def _generate_agent_memory_markdown(self, agent_id: str, memories: List[Dict]) -> str:
        """Generate markdown content for agent memory file."""
        content = [f"# {agent_id.upper()} Memory File"]
        content.append(f"\nMigrated from SQLite database on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        # Group memories by type
        memory_groups = {}
        for memory in memories:
            mem_type = memory["memory_type"]
            if mem_type not in memory_groups:
                memory_groups[mem_type] = []
            memory_groups[mem_type].append(memory)

        # Generate sections for each memory type
        for mem_type, type_memories in memory_groups.items():
            content.append(f"## {mem_type.title()} Memories")
            content.append("")

            for memory in type_memories:
                content.append(f"### {memory['created_at']}")
                content.append(memory["content"])

                if memory["metadata"]:
                    try:
                        metadata = json.loads(memory["metadata"])
                        content.append(f"\nMetadata: {json.dumps(metadata, indent=2)}")
                    except json.JSONDecodeError:
                        content.append(f"\nMetadata: {memory['metadata']}")

                content.append("")

        return "\n".join(content)

    def _generate_agentconvo_markdown(self, coord_logs: List[Dict]) -> str:
        """Generate markdown content for agentconvo.md file."""
        content = ["# Agent Communication Log"]
        content.append("\nFormat: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]")
        content.append("")
        content.append("## Communication History")
        content.append("")

        for log in coord_logs:
            timestamp = log["created_at"]
            from_agent = log["from_agent"]
            message = log["content"]  # SQLite uses 'content' field
            content.append(f"[{from_agent}] [{timestamp}] - {message}")

        return "\n".join(content)

    def _generate_agentconvo_entries(self, coord_logs: List[Dict]) -> str:
        """Generate new entries for existing agentconvo.md file."""
        entries = []
        for log in coord_logs:
            timestamp = log["created_at"]
            from_agent = log["from_agent"]
            message = log["content"]  # SQLite uses 'content' field
            entries.append(f"[{from_agent}] [{timestamp}] - {message}")

        return "\n".join(entries)

    def _generate_project_memory_markdown(self, project_state: Dict) -> str:
        """Generate markdown content for memory.md file."""
        content = ["# Project Memory"]
        content.append(f"\nMigrated from SQLite database on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        # Map project state fields to markdown sections
        if "task" in project_state:
            content.append("## Task")
            content.append(str(project_state["task"]))
            content.append("")

        if "team_configuration" in project_state:
            content.append("## Team Configuration")
            team_config = project_state["team_configuration"]
            if isinstance(team_config, dict):
                content.append(json.dumps(team_config, indent=2))
            else:
                content.append(str(team_config))
            content.append("")

        if "key_decisions" in project_state:
            content.append("## Key Decisions")
            decisions = project_state["key_decisions"]
            if isinstance(decisions, list):
                for decision in decisions:
                    content.append(f"- {decision}")
            else:
                content.append(str(decisions))
            content.append("")

        if "current_state" in project_state:
            content.append("## Current State")
            content.append(str(project_state["current_state"]))
            content.append("")

        # Add any other fields as JSON
        other_fields = {k: v for k, v in project_state.items()
                       if k not in ["task", "team_configuration", "key_decisions", "current_state", "source", "migrated_at"]}
        if other_fields:
            content.append("## Additional Data")
            content.append("```json")
            content.append(json.dumps(other_fields, indent=2))
            content.append("```")
            content.append("")

        return "\n".join(content)

    def _generate_handoff_markdown(self, handoff: Dict) -> str:
        """Generate markdown content for handoff file."""
        content = [f"# 🤝 Agent Handoff Document"]
        content.append(f"\n**Handoff ID**: {handoff['handoff_id']}")
        content.append(f"**From**: {handoff['from_agent']}")
        if handoff['to_agent']:
            content.append(f"**To**: {handoff['to_agent']}")
        content.append(f"**Status**: {handoff['status']}")
        content.append(f"**Created**: {handoff['created_at']}")
        content.append("")

        sections = [
            ("Problem Description", handoff["problem_description"]),
            ("Work Completed", handoff["work_completed"]),
            ("Commits Made", handoff["commits_made"]),
            ("Files Modified", handoff["files_modified"]),
            ("Current Status", handoff["current_status"]),
            ("Next Steps", handoff["next_steps"]),
            ("Context Notes", handoff["context_notes"]),
        ]

        for section_title, section_content in sections:
            if section_content:
                content.append(f"## {section_title}")
                content.append(section_content)
                content.append("")

        # Add git information
        if handoff["git_branch"] or handoff["git_commit"]:
            content.append("## Git Information")
            if handoff["git_branch"]:
                content.append(f"**Branch**: {handoff['git_branch']}")
            if handoff["git_commit"]:
                content.append(f"**Commit**: {handoff['git_commit']}")
            content.append("")

        content.append(f"**AGOR Version**: {handoff['agor_version']}")

        return "\n".join(content)

    def _backup_markdown_files(self):
        """Create backup of markdown files before deletion."""
        backup_dir = self.agor_dir / "markdown_backup"
        backup_dir.mkdir(exist_ok=True)

        # Backup files
        for pattern in ["*.md", "handoffs/*.md"]:
            for file_path in self.agor_dir.glob(pattern):
                if file_path.is_file():
                    backup_path = backup_dir / file_path.name
                    backup_path.write_text(file_path.read_text())
                    file_path.unlink()


# Convenience functions for migration operations
def migrate_to_sqlite(agor_dir: str = ".agor", preserve_markdown: bool = True) -> Dict[str, int]:
    """Migrate markdown memory files to SQLite database."""
    manager = MemoryMigrationManager(Path(agor_dir))
    return manager.migrate_markdown_to_sqlite(preserve_markdown)


def migrate_to_markdown(agor_dir: str = ".agor", overwrite_existing: bool = False) -> Dict[str, int]:
    """Migrate SQLite database to markdown memory files."""
    manager = MemoryMigrationManager(Path(agor_dir))
    return manager.migrate_sqlite_to_markdown(overwrite_existing)


def sync_memory_systems(agor_dir: str = ".agor", direction: str = "bidirectional") -> Dict[str, int]:
    """Synchronize between markdown and SQLite memory systems."""
    manager = MemoryMigrationManager(Path(agor_dir))
    return manager.sync_systems(direction)
