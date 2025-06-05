"""
Enhanced Hotkey System for AGOR - Automatic Checklist Integration

This system enhances the existing AGOR hotkey system by automatically integrating
with the agent checklist system. When agents use hotkeys, the system automatically
tracks progress and enforces mandatory procedures.

Key Features:
- Automatic checklist integration with all hotkeys
- Session end detection and snapshot enforcement
- Progress tracking and recommendations
- Seamless integration with existing AGOR workflows
"""

import re
from typing import Dict, List, Optional, Callable
from pathlib import Path

# Import checklist system
try:
    from agor.tools.agent_checklist_system import checklist_manager, create_checklist, mark_complete, get_status, create_snapshot
    from agor.tools.dev_tooling import dev_tools, get_timestamp
except ImportError:
    # Fallback for development environment
    print("⚠️  Enhanced hotkeys running in development mode")
    
    class MockChecklistManager:
        def get_checklist_status(self):
            return {"status": "no_checklist"}
    
    checklist_manager = MockChecklistManager()
    
    def create_checklist(*args, **kwargs):
        return None
    
    def mark_complete(*args, **kwargs):
        return True
    
    def get_status():
        return {"status": "no_checklist"}
    
    def create_snapshot(*args, **kwargs):
        return True


class EnhancedHotkeySystem:
    """Enhanced hotkey system with automatic checklist integration."""
    
    def __init__(self):
        self.session_active = False
        self.completion_indicators = [
            "thanks", "goodbye", "done", "finished", "complete", "end session",
            "that's all", "wrap up", "closing", "final", "submit"
        ]
        self.hotkey_checklist_mapping = {
            # Analysis hotkeys
            "a": "codebase_analysis",
            "f": "codebase_analysis", 
            "da": "codebase_analysis",
            
            # Git operations
            "commit": "frequent_commits",
            "diff": "frequent_commits",
            "m": "frequent_commits",
            
            # Documentation
            "doc": "test_changes",
            "comment": "test_changes",
            "explain": "codebase_analysis",
            
            # Coordination
            "status": "update_coordination",
            "sync": "update_coordination",
            "log": "update_coordination",
            "msg": "update_coordination",
            
            # Snapshots
            "snapshot": "create_snapshot",
            "load_snapshot": "create_snapshot",
            "complete": "create_snapshot",
            
            # Strategy (for coordinators)
            "sp": "strategy_selection",
            "bp": "strategy_selection",
            "ss": "strategy_selection",
            "pd": "strategy_selection",
            "pl": "strategy_selection",
            "sw": "strategy_selection",
            "rt": "strategy_selection",
            "mb": "strategy_selection"
        }
    
    def detect_session_start(self, user_input: str, agent_role: str = "solo_developer") -> bool:
        """Detect if this is the start of a new session and create checklist."""
        start_indicators = [
            "start", "begin", "initialize", "new session", "hello", "hi",
            "let's work", "ready to", "working on", "need to", "help me"
        ]
        
        if any(indicator in user_input.lower() for indicator in start_indicators):
            if not self.session_active:
                self.session_active = True
                
                # Extract task description from user input
                task_description = self._extract_task_description(user_input)
                
                # Prompt agent to create their own checklist
                self._prompt_checklist_creation(task_description, agent_role)
                return True
        
        return False
    
    def _extract_task_description(self, user_input: str) -> str:
        """Extract task description from user input."""
        # Simple extraction - look for common patterns
        patterns = [
            r"working on (.+)",
            r"need to (.+)",
            r"help me (.+)",
            r"implement (.+)",
            r"fix (.+)",
            r"create (.+)",
            r"build (.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).strip()
        
        # Fallback to first sentence
        sentences = user_input.split('.')
        if sentences:
            return sentences[0].strip()
        
        return "Development task"
    
    def _prompt_checklist_creation(self, task_description: str, agent_role: str):
        """Internal agent checklist creation - no user interaction."""
        print(f"\n🎯 **Internal Session Checklist Created**")
        print(f"Task: {task_description}")
        print(f"Role: {agent_role}")
        print("\nCreating internal checklist with mandatory AGOR items...")

        # Agent automatically determines custom items based on task
        custom_items = self._auto_generate_custom_items(task_description, agent_role)

        # Create checklist automatically
        checklist = self.create_agent_checklist(task_description, custom_items, "internal_agent", agent_role)

        if checklist:
            print(f"✅ Internal checklist created with {len(checklist.items)} items")

        return checklist

    def _auto_generate_custom_items(self, task_description: str, agent_role: str) -> List[str]:
        """Automatically generate custom checklist items based on task and role."""
        custom_items = []

        # Analyze task description for common patterns
        task_lower = task_description.lower()

        if any(word in task_lower for word in ["test", "testing", "spec"]):
            custom_items.append("Review and update test coverage")

        if any(word in task_lower for word in ["doc", "documentation", "readme"]):
            custom_items.append("Update relevant documentation")

        if any(word in task_lower for word in ["api", "endpoint", "service"]):
            custom_items.append("Verify API contracts and interfaces")

        if any(word in task_lower for word in ["bug", "fix", "error", "issue"]):
            custom_items.append("Reproduce issue and verify fix")

        if any(word in task_lower for word in ["feature", "implement", "add"]):
            custom_items.append("Consider backward compatibility")

        if any(word in task_lower for word in ["security", "auth", "permission"]):
            custom_items.append("Review security implications")

        if any(word in task_lower for word in ["performance", "optimize", "speed"]):
            custom_items.append("Measure performance impact")

        # Role-specific items
        if agent_role == "project_coordinator":
            custom_items.extend([
                "Review team capacity and assignments",
                "Identify potential blockers"
            ])
        elif agent_role == "agent_worker":
            custom_items.extend([
                "Clarify requirements with coordinator",
                "Estimate completion time"
            ])

        return custom_items
    
    def create_agent_checklist(self, task_description: str, custom_items: List[str], agent_id: str = "agent", role: str = "solo_developer"):
        """Create internal agent checklist automatically."""
        # Create checklist
        checklist = create_checklist(task_description, custom_items, agent_id, role)

        if checklist:
            print(f"\n✅ **Internal Checklist Created for Session {checklist.session_id}**")
            print(f"📊 Total items: {len(checklist.items)}")
            print(f"🔴 Mandatory: {sum(1 for item in checklist.items if item.mandatory)}")
            print(f"🔵 Custom: {sum(1 for item in checklist.items if not item.mandatory)}")

            self._display_checklist_summary(checklist)

            # Mark documentation reading as complete if this is initialization
            mark_complete("read_documentation", "Documentation read during initialization")

            return checklist
        else:
            print("❌ Failed to create internal checklist")
            return None
    
    def _display_checklist_summary(self, checklist):
        """Display a summary of the created internal checklist."""
        print("\n📋 **Internal Agent Checklist:**")

        mandatory_items = [item for item in checklist.items if item.mandatory]
        custom_items = [item for item in checklist.items if not item.mandatory]

        print("\n🔴 **Mandatory Items:**")
        for item in mandatory_items:
            status = "✅" if item.completed else "⏳"
            print(f"  {status} {item.description}")

        if custom_items:
            print("\n🔵 **Auto-Generated Items:**")
            for item in custom_items:
                status = "✅" if item.completed else "⏳"
                print(f"  {status} {item.description}")

        print(f"\n💡 Items will be automatically marked complete as work progresses")
        print(f"💡 Use checklist_status() to see progress anytime")
    
    def process_hotkey(self, hotkey: str, context: str = "") -> Dict:
        """Process hotkey and update checklist automatically."""
        result = {
            "hotkey": hotkey,
            "checklist_updated": False,
            "recommendations": [],
            "warnings": []
        }
        
        # Map hotkey to checklist item
        if hotkey in self.hotkey_checklist_mapping:
            item_id = self.hotkey_checklist_mapping[hotkey]
            
            # Mark item as complete
            if mark_complete(item_id, f"Completed via {hotkey} hotkey"):
                result["checklist_updated"] = True
                print(f"✅ Checklist updated: {item_id} marked complete")
        
        # Get current status and recommendations
        status = get_status()
        if status["status"] == "active":
            result["recommendations"] = status.get("recommendations", [])
            
            # Check for warnings
            if status.get("mandatory_incomplete", 0) > 0:
                result["warnings"].append(f"{status['mandatory_incomplete']} mandatory items remaining")
            
            # Progress update
            completion = status.get("completion_percentage", 0)
            print(f"📊 Session progress: {completion:.1f}% complete")
            
            if completion > 80 and not status.get("snapshot_created", False):
                result["warnings"].append("Consider creating a snapshot soon")
        
        return result
    
    def detect_session_end(self, user_input: str) -> bool:
        """Detect if user is indicating session end."""
        return any(indicator in user_input.lower() for indicator in self.completion_indicators)
    
    def enforce_session_end_procedures(self) -> bool:
        """Enforce mandatory procedures before session end."""
        status = get_status()
        
        if status["status"] != "active":
            print("ℹ️  No active checklist to check")
            return True
        
        # Check mandatory items
        mandatory_incomplete = status.get("mandatory_incomplete", 0)
        snapshot_created = status.get("snapshot_created", False)
        
        if mandatory_incomplete > 0:
            print(f"🚨 **CANNOT END SESSION**")
            print(f"❌ {mandatory_incomplete} mandatory items incomplete")
            
            if status.get("next_mandatory"):
                print(f"📋 Next mandatory item: {status['next_mandatory']}")
            
            return False
        
        if not snapshot_created:
            print("🚨 **MANDATORY: Create session snapshot before ending**")
            print("Use: create_snapshot() or snapshot hotkey")
            
            # Offer to create snapshot automatically
            print("\n💡 Would you like me to create the snapshot now? (y/n)")
            return False
        
        print("✅ All mandatory procedures complete - session can end safely")
        self.session_active = False
        return True
    
    def get_checklist_status_display(self) -> str:
        """Get formatted checklist status for display."""
        status = get_status()
        
        if status["status"] != "active":
            return "📋 No active checklist"
        
        completion = status.get("completion_percentage", 0)
        mandatory_incomplete = status.get("mandatory_incomplete", 0)
        optional_incomplete = status.get("optional_incomplete", 0)
        
        display = f"""
📊 **Checklist Status**
Progress: {completion:.1f}% complete
Mandatory remaining: {mandatory_incomplete}
Optional remaining: {optional_incomplete}
Snapshot created: {'✅' if status.get('snapshot_created', False) else '❌'}
"""
        
        recommendations = status.get("recommendations", [])
        if recommendations:
            display += "\n💡 **Recommendations:**\n"
            for rec in recommendations:
                display += f"  • {rec}\n"
        
        return display.strip()


# Global enhanced hotkey system instance
enhanced_hotkeys = EnhancedHotkeySystem()


# Convenience functions
def start_session(user_input: str, agent_role: str = "solo_developer") -> bool:
    """Detect and start new session with checklist."""
    return enhanced_hotkeys.detect_session_start(user_input, agent_role)


def process_hotkey(hotkey: str, context: str = "") -> Dict:
    """Process hotkey with automatic checklist integration."""
    return enhanced_hotkeys.process_hotkey(hotkey, context)


def end_session(user_input: str) -> bool:
    """Detect session end and enforce procedures."""
    if enhanced_hotkeys.detect_session_end(user_input):
        return enhanced_hotkeys.enforce_session_end_procedures()
    return True


def checklist_status() -> str:
    """Get formatted checklist status."""
    return enhanced_hotkeys.get_checklist_status_display()


def create_agent_checklist(task_description: str, custom_items: str, agent_id: str = "agent", role: str = "solo_developer"):
    """Create agent checklist with custom items."""
    return enhanced_hotkeys.create_agent_checklist(task_description, custom_items, agent_id, role)
