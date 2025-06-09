"""
AGOR Development Tooling - Main Interface Module

This module provides the main interface for AGOR development utilities.
It imports functionality from specialized modules for better organization:

- snapshots: Snapshot creation and agent handoff functionality
- hotkeys: Hotkey helpers and workflow convenience functions
- checklist: Checklist generation and workflow validation
- git_operations: Safe git operations and timestamp utilities
- memory_manager: Cross-branch memory commits and branch management
- agent_handoffs: Agent coordination and handoff utilities
- dev_testing: Testing utilities and environment detection

Provides a clean API interface while keeping individual modules under 500 LOC.
"""

from pathlib import Path
from typing import Dict, List, Optional

from agor.tools.agent_handoffs import detick_content, retick_content
from agor.tools.checklist import (
    check_git_workflow_status,
    generate_development_checklist,
    generate_git_workflow_report,
    generate_handoff_checklist,
    generate_progress_report,
    validate_workflow_completion,
)
from agor.tools.dev_testing import detect_environment, test_tooling

# Use absolute imports to prevent E0402 errors
from agor.tools.git_operations import (
    get_current_timestamp,
    quick_commit_push,
    run_git_command,
)
from agor.tools.hotkeys import (
    display_project_status,
    display_workspace_health,
    emergency_commit,
    get_project_status,
    quick_status_check,
    workspace_health_check,
)
from agor.tools.memory_manager import auto_commit_memory

# Import from new modular components
from agor.tools.snapshots import (
    create_seamless_handoff,
    create_snapshot,
    generate_agent_handoff_prompt,
    generate_mandatory_session_end_prompt,
)

# Handle imports for both installed and development environments
try:
    from agor.git_binary import git_manager
except ImportError:
    # Development environment - fallback to basic git
    print("⚠️  Using fallback git binary (development mode)")

    class FallbackGitManager:
        def get_git_binary(self):
            import shutil

            git_path = shutil.which("git")
            if not git_path:
                raise RuntimeError("Git not found in PATH")
            return git_path

    git_manager = FallbackGitManager()


# Main API Functions - Core Interface
# ===================================


def create_development_snapshot(title: str, context: str) -> bool:
    """Create development snapshot - main API function."""
    return create_snapshot(title, context)


def generate_seamless_agent_handoff(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    files_modified: list = None,
    context_notes: str = None,
    brief_context: str = None,
) -> tuple[str, str]:
    """Generate seamless agent handoff - main API function."""
    return create_seamless_handoff(
        task_description=task_description,
        work_completed=work_completed,
        next_steps=next_steps,
        files_modified=files_modified,
        context_notes=context_notes,
        brief_context=brief_context,
    )


def generate_session_end_prompt(
    task_description: str = "Session completion",
    brief_context: str = "Work session completed",
) -> str:
    """Generate mandatory session end prompt - main API function."""
    return generate_mandatory_session_end_prompt(task_description, brief_context)


def generate_project_handoff_prompt(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """Generate project handoff prompt - main API function."""
    return generate_agent_handoff_prompt(
        task_description=task_description,
        snapshot_content=snapshot_content,
        memory_branch=memory_branch,
        environment=environment,
        brief_context=brief_context,
    )


# Convenience Functions - Wrapper API
# ===================================


def quick_commit_and_push(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push wrapper."""
    return quick_commit_push(message, emoji)


def commit_memory_to_branch(
    content: str, memory_type: str, agent_id: str = "dev"
) -> bool:
    """Auto-commit memory wrapper."""
    return auto_commit_memory(content, memory_type, agent_id)


def test_development_tooling() -> bool:
    """Test development tooling wrapper."""
    return test_tooling()


def get_current_timestamp_formatted() -> str:
    """Get formatted timestamp wrapper."""
    return get_current_timestamp()


def process_content_for_codeblock(content: str) -> str:
    """Process content for safe codeblock embedding."""
    return detick_content(content)


def restore_content_from_codeblock(content: str) -> str:
    """Restore content from codeblock processing."""
    return retick_content(content)


# Status and Health Check Functions
# =================================


def get_workspace_status() -> dict:
    """Get comprehensive workspace status."""
    return get_project_status()


def display_workspace_status() -> str:
    """Display formatted workspace status."""
    return display_project_status()


def get_quick_status() -> str:
    """Get quick status summary."""
    return quick_status_check()


def perform_workspace_health_check() -> dict:
    """Perform comprehensive workspace health check."""
    return workspace_health_check()


def display_health_check_results() -> str:
    """Display formatted health check results."""
    return display_workspace_health()


def emergency_save(message: str = "Emergency commit - work in progress") -> bool:
    """Emergency commit for quick saves."""
    return emergency_commit(message)


# Checklist and Workflow Functions
# ================================


def create_development_checklist(task_type: str = "general") -> str:
    """Create development checklist for task type."""
    return generate_development_checklist(task_type)


def create_handoff_checklist() -> str:
    """Create agent handoff checklist."""
    return generate_handoff_checklist()


def validate_workflow(checklist_items: List[str]) -> Dict[str, any]:
    """Validate workflow completion against checklist."""
    return validate_workflow_completion(checklist_items)


def create_progress_report(validation_results: Dict[str, any]) -> str:
    """Create formatted progress report."""
    return generate_progress_report(validation_results)


def check_git_workflow() -> Dict[str, any]:
    """Check git workflow status."""
    return check_git_workflow_status()


def display_git_workflow_status() -> str:
    """Display git workflow status report."""
    return generate_git_workflow_report()


# Memory Management Functions
# ===========================


# Import memory branch utilities from memory_manager to avoid code duplication
# Note: read_from_memory_branch and list_memory_branches available if needed


def generate_agent_memory_branch() -> str:
    """
    Generates a unique agent memory branch name using a timestamp-based hash.
    
    Returns:
        A string in the format 'agor/mem/agent_{hash}' for uniquely identifying an agent's memory branch.
    """
    import hashlib
    import time

    agent_id = hashlib.md5(f"agent_{time.time()}".encode()).hexdigest()[:8]
    memory_branch = f"agor/mem/agent_{agent_id}"

    return memory_branch


def create_agent_memory_branch(memory_branch: str = None) -> tuple[bool, str]:
    """
    Creates an agent-specific memory branch with an initial commit containing metadata and usage guidelines.
    
    If no branch name is provided, a unique one is generated. Returns a tuple indicating success and the branch name.
    """
    if memory_branch is None:
        memory_branch = generate_agent_memory_branch()

    try:
        from agor.tools.memory_manager import commit_to_memory_branch

        # Create initial commit to establish the memory branch
        initial_content = f"""# Agent Memory Branch: {memory_branch}

**Created**: {get_current_timestamp()}
**Purpose**: Dedicated memory space for agent coordination and snapshots

## Branch Usage

This memory branch stores:
- Development snapshots
- Agent coordination data
- Session context and handoff information
- Workflow state and progress tracking

## Agent Guidelines

- Use this branch for all snapshot commits
- Reference this branch in handoff prompts
- Maintain context continuity across sessions
- Clean up when agent work is complete
"""

        success = commit_to_memory_branch(
            content=initial_content,
            memory_type="agent_initialization",
            agent_id=memory_branch.split('_')[-1],  # Extract agent ID from branch name
            memory_branch=memory_branch
        )

        if success:
            print(f"✅ Created agent memory branch: {memory_branch}")
        else:
            print(f"❌ Failed to create agent memory branch: {memory_branch}")

        return success, memory_branch

    except Exception as e:
        print(f"❌ Error creating agent memory branch: {e}")
        return False, memory_branch


def validate_output_formatting(content: str) -> dict:
    """
    Validates whether the provided content complies with AGOR output formatting standards.
    
    Checks for the presence of codeblocks, triple backticks, and proper codeblock wrapping. Identifies issues such as the need for deticking or incorrect formatting of handoff prompts, and provides suggestions for compliance.
    
    Args:
        content: The content string to validate.
    
    Returns:
        A dictionary containing compliance status, detected issues, suggestions for correction, and flags indicating codeblock and deticking requirements.
    """
    validation = {
        "is_compliant": True,
        "issues": [],
        "suggestions": [],
        "has_codeblocks": False,
        "has_triple_backticks": False,
        "detick_needed": False
    }

    # Check for codeblock presence
    if "```" in content:
        validation["has_codeblocks"] = True
        validation["has_triple_backticks"] = True

        # Check if content has triple backticks that need deticking
        if content.count("```") > 0:
            validation["detick_needed"] = True
            validation["issues"].append("Content contains triple backticks that may break codeblock rendering")
            validation["suggestions"].append("Process through detick_content() before wrapping in codeblocks")

    # Check for proper codeblock wrapping indicators
    if (not content.startswith("``") or not content.endswith("``")) and validation["has_codeblocks"]:
        validation["is_compliant"] = False
        validation["issues"].append("Content with codeblocks should be wrapped in double backticks")
        validation["suggestions"].append("Wrap entire content in double backticks for copy-paste safety")

    # Check for handoff prompt indicators
    if ("handoff" in content.lower() or "session end" in content.lower()) and (not validation["has_codeblocks"] or validation["has_triple_backticks"]):
        validation["is_compliant"] = False
        validation["issues"].append("Handoff prompts must be deticked and wrapped in single codeblocks")
        validation["suggestions"].append("Use detick_content() and wrap in double backticks")

    return validation


def apply_output_formatting(content: str, content_type: str = "general") -> str:
    """
    Formats content according to AGOR output standards for safe embedding and compliance.
    
    Deticks the input content to remove triple backticks and, for specific content types such as handoff prompts, snapshots, or meta feedback, wraps the result in double backtick codeblocks. Returns the formatted content ready for output.
    """
    # Process through detick to handle any triple backticks
    processed_content = detick_content(content)

    # For handoff prompts and critical outputs, wrap in codeblock
    if content_type in ["handoff_prompt", "snapshot", "meta_feedback"]:
        formatted_content = f"``\n{processed_content}\n``"
    else:
        formatted_content = processed_content

    return formatted_content


# Utility Functions
# =================


def detect_current_environment() -> dict:
    """Detect current development environment."""
    return detect_environment()


def test_all_tooling() -> bool:
    """
    Runs comprehensive tests on all development tooling components.
    
    Returns:
        True if all tests pass successfully, otherwise False.
    """
    return test_tooling()


# Workflow Optimization Functions
# ===============================


def generate_workflow_prompt_template(
    task_description: str,
    memory_branch: str = None,
    include_bookend: bool = True,
    include_explicit_requirements: bool = True
) -> str:
    """
    Generates an optimized workflow prompt template for AGOR agent tasks.
    
    Creates a detailed prompt incorporating the task description, memory branch reference, session start requirements, development guidelines, mandatory session end requirements (with example code), and success criteria. Supports options to include the bookend approach and explicit handoff requirements for seamless agent coordination.
    
    Args:
        task_description: Description of the agent's task.
        memory_branch: Optional memory branch name for context continuity; generated if not provided.
        include_bookend: Whether to include session start and end requirements.
        include_explicit_requirements: Whether to include explicit handoff and formatting requirements.
    
    Returns:
        A formatted prompt template string ready for agent use.
    """
    if memory_branch is None:
        memory_branch = generate_agent_memory_branch()

    prompt_template = f"""# 🎯 AGOR Agent Task: {task_description}

**Memory Branch**: {memory_branch}
**Generated**: {get_current_timestamp()}

## 📋 Task Description

{task_description}

"""

    if include_bookend:
        prompt_template += """## 🚀 Session Start Requirements

Before starting work:
1. Read AGOR documentation and understand the task
2. Create a development plan and approach
3. Set up your memory branch for snapshots

"""

    prompt_template += """## 🔧 Development Guidelines

- Use quick_commit_and_push() frequently during work
- Create progress snapshots for major milestones
- Test your changes thoroughly
- Document your implementation process

"""

    if include_explicit_requirements:
        prompt_template += f"""## ⚠️ MANDATORY SESSION END REQUIREMENTS

Your response MUST end with:

1. **Development Snapshot**: Use create_development_snapshot()
2. **Handoff Prompt**: Use generate_session_end_prompt()
3. **Proper Formatting**: Process through detick_content() and wrap in codeblocks

**Memory Branch Reference**: {memory_branch}

```python
# Required session end code:
from agor.tools.dev_tooling import create_development_snapshot
from agor.tools.agent_handoffs import generate_session_end_prompt, detick_content

# Create snapshot
create_development_snapshot(
    title="Your work title",
    context="Detailed description of what you accomplished"
)

# Generate handoff prompt
handoff_prompt = generate_session_end_prompt(
    work_completed=["List your accomplishments"],
    current_status="Current project status",
    next_agent_instructions=["Instructions for next agent"],
    critical_context="Important context to preserve",
    files_modified=["Files you modified"]
)

# Format and output
processed_prompt = detick_content(handoff_prompt)
print("``")
print(processed_prompt)
print("``")
```

"""

    prompt_template += """## 🎯 Success Criteria

You will have succeeded when:
- All task objectives are completed
- Changes are tested and working
- Comprehensive snapshot is created
- Handoff prompt is generated and properly formatted
- Next agent has clear instructions to continue

---

**Remember**: AGOR's goal is seamless agent coordination. Your handoff prompt should enable the next agent to continue work without manual re-entry of context."""

    return prompt_template


def validate_agor_workflow_completion(
    work_completed: list,
    files_modified: list,
    has_snapshot: bool = False,
    has_handoff_prompt: bool = False
) -> dict:
    """
    Validates workflow completion against AGOR standards and provides feedback.
    
    Checks for documentation of completed work, file modifications, development snapshot creation, and handoff prompt generation. Returns a dictionary with completeness status, score, identified issues, recommendations, and any missing requirements.
    """
    validation = {
        "is_complete": True,
        "score": 0,
        "max_score": 10,
        "issues": [],
        "recommendations": [],
        "missing_requirements": []
    }

    # Check work completion documentation
    if work_completed and len(work_completed) > 0:
        validation["score"] += 2
    else:
        validation["is_complete"] = False
        validation["issues"].append("No work completion documented")
        validation["missing_requirements"].append("Document completed work items")

    # Check file modification tracking
    if files_modified and len(files_modified) > 0:
        validation["score"] += 2
    else:
        validation["issues"].append("No file modifications documented")
        validation["recommendations"].append("Track and document all file changes")

    # Check snapshot creation
    if has_snapshot:
        validation["score"] += 3
    else:
        validation["is_complete"] = False
        validation["issues"].append("Development snapshot not created")
        validation["missing_requirements"].append("Create development snapshot with create_development_snapshot()")

    # Check handoff prompt generation
    if has_handoff_prompt:
        validation["score"] += 3
    else:
        validation["is_complete"] = False
        validation["issues"].append("Handoff prompt not generated")
        validation["missing_requirements"].append("Generate handoff prompt with generate_session_end_prompt()")

    # Add recommendations based on score
    if validation["score"] < 5:
        validation["recommendations"].append("Review AGOR workflow optimization guide")
        validation["recommendations"].append("Use workflow prompt templates for better compliance")
    elif validation["score"] < 8:
        validation["recommendations"].append("Improve documentation completeness")
        validation["recommendations"].append("Ensure all requirements are met")
    else:
        validation["recommendations"].append("Excellent workflow compliance!")

    return validation


def get_workflow_optimization_tips() -> str:
    """
    Returns formatted AGOR workflow optimization tips, including best practices, common issues with solutions, helper function usage examples, and success metrics to improve agent workflow compliance and coordination.
    """
    tips = f"""# 🎯 AGOR Workflow Optimization Tips

**Generated**: {get_current_timestamp()}

## 🔄 Proven Strategies

### 1. The "Bookend" Approach
- Start sessions with clear requirements
- End sessions with mandatory deliverables
- Include explicit handoff instructions

### 2. Memory Branch Strategy
- Generate unique agent memory branch: `{generate_agent_memory_branch()}`
- Use for all snapshots and coordination
- Reference in handoff prompts for continuity

### 3. Output Formatting Compliance
- ALL handoff prompts must be deticked and wrapped in codeblocks
- Use `detick_content()` before wrapping in double backticks
- Test formatting with `validate_output_formatting()`

## 🚨 Common Issues to Avoid

❌ **Agent doesn't create handoff prompt**
✅ **Solution**: Include explicit requirements in prompt template

❌ **Context lost between agents**
✅ **Solution**: Always reference memory branches and previous work

❌ **Formatting breaks codeblocks**
✅ **Solution**: Use detick_content() and proper wrapping

## 🛠️ Helper Functions

```python
# Generate optimized prompt
prompt = generate_workflow_prompt_template(
    task_description="Your task",
    memory_branch="agor/mem/agent_12345678"
)

# Validate completion
validation = validate_agor_workflow_completion(
    work_completed=["item1", "item2"],
    files_modified=["file1.py", "file2.md"],
    has_snapshot=True,
    has_handoff_prompt=True
)

# Check output formatting
formatting = validate_output_formatting(content)
```

## 🎯 Success Metrics

**Green flags** (workflow working well):
- Agents automatically create handoff prompts
- Context flows seamlessly between agents
- Minimal user intervention required
- Work continues without manual re-entry

**Red flags** (optimization needed):
- Repeatedly reminding agents about handoffs
- Context getting lost between sessions
- Manual re-entry of requirements
- Agents not following AGOR protocols

---

**Use these tips to maintain seamless AGOR coordination workflows.**
"""

    return tips
