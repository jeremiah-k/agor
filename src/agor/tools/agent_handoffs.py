"""
Agent Handoffs Module for AGOR Development Tooling

This module contains all agent coordination and handoff functionality
extracted from dev_tooling.py for better organization and maintainability.

Functions:
- generate_handoff_prompt_only: Generate handoff prompts for agent coordination
- generate_mandatory_session_end_prompt: Session end coordination
- detick_content/retick_content: Backtick processing for clean codeblocks
- Snapshot generation and agent coordination utilities
"""

import re
from dataclasses import dataclass
from typing import List

from agor.tools.git_operations import get_current_timestamp, run_git_command


def get_current_branch() -> str:
    """Get current git branch name."""
    success, branch = run_git_command(["branch", "--show-current"])
    if success:
        return branch.strip()
    return "main"  # fallback


def get_agor_version() -> str:
    """
    Retrieves the current AGOR version string.
    
    Returns:
        The AGOR package version if available; otherwise, a default version string.
    """
    try:
        import agor

        return getattr(agor, "__version__", "0.4.3+")
    except ImportError:
        return "0.4.3+"


def detick_content(content: str) -> str:
    """
    Converts triple backticks (```) in the input content to double backticks (``) to prevent codeblock rendering issues during agent communication.
    
    Args:
        content: The input string potentially containing triple backticks.
    
    Returns:
        The content with all standalone triple backticks replaced by double backticks.
    """
    # Use regex to avoid runaway replacements
    # Only replace ``` that are not preceded or followed by another backtick
    pattern = r"(?<!`)```(?!`)"
    return re.sub(pattern, "``", content)


def retick_content(content: str) -> str:
    """
    Converts double backticks (``) in the input content back to triple backticks (```) to restore standard markdown codeblock formatting.
    
    Args:
        content: The string containing double backticks to be converted.
    
    Returns:
        The content with all double backticks replaced by triple backticks.
    """
    # Use regex to avoid runaway replacements
    # Only replace `` that are not preceded or followed by another backtick
    pattern = r"(?<!`)``(?!`)"
    return re.sub(pattern, "```", content)


def _format_feedback_list(items: List[str], empty_message: str) -> str:
    """
    Formats a list of strings as a markdown bullet list for feedback display.
    
    If the list is empty, returns a single bullet with the provided empty message.
    """
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def generate_handoff_prompt_only(
    work_completed: List[str],
    current_status: str,
    next_agent_instructions: List[str],
    critical_context: str,
    files_modified: List[str] = None,
) -> str:
    """
    Generates a formatted agent handoff prompt summarizing completed work, current status, instructions for the next agent, critical context, and files modified.
    
    The prompt includes environment setup steps, coordination protocol, and critical requirements for seamless multi-agent workflows. All content is processed to replace triple backticks with double backticks for safe embedding in codeblocks.
    
    Args:
        work_completed: List of completed work items for the session.
        current_status: Description of the current project status.
        next_agent_instructions: Actionable instructions for the next agent or session.
        critical_context: Essential context that must be preserved for continuity.
        files_modified: List of files modified during the session.
    
    Returns:
        A deticked, markdown-formatted handoff prompt string for agent coordination.
    """
    # Validate required inputs
    if not isinstance(work_completed, list):
        work_completed = []
    if not isinstance(next_agent_instructions, list):
        next_agent_instructions = []
    if not current_status:
        current_status = "Status not provided"
    if not critical_context:
        critical_context = "No critical context provided"
    if files_modified is None:
        files_modified = []

    timestamp = get_current_timestamp()
    current_branch = get_current_branch()
    agor_version = get_agor_version()

    prompt_content = f"""# 🚀 AGOR Agent Handoff Prompt

**Generated**: {timestamp}
**Session Type**: Agent Handoff Required
**AGOR Version**: {agor_version}

## 📋 WORK COMPLETED THIS SESSION

{_format_feedback_list(work_completed, 'No work completed')}

## 📊 CURRENT PROJECT STATUS

**Status**: {current_status or 'Status not provided'}

## 📁 FILES MODIFIED

{_format_feedback_list(files_modified, 'No files modified')}

## 🎯 INSTRUCTIONS FOR NEXT AGENT/SESSION

{_format_feedback_list(next_agent_instructions, 'No specific instructions provided')}

## 🧠 CRITICAL CONTEXT TO PRESERVE

{critical_context or 'No critical context provided'}

## 🔧 ENVIRONMENT SETUP FOR CONTINUATION

# Pull latest changes
git pull origin {current_branch}

# Install dependencies
python3 -m pip install -r src/agor/tools/agent-requirements.txt

# Read updated documentation
- src/agor/tools/README_ai.md (2-role system)
- src/agor/tools/AGOR_INSTRUCTIONS.md (comprehensive guide)

## ⚠️ CRITICAL REQUIREMENTS FOR NEXT SESSION

1. **Review this session's work** - Understand what was completed
2. **Continue from current status** - Don't restart or duplicate work
3. **Use our dev tooling** - All coordination must use our backtick processing
4. **Create return prompts** - Every session must end with coordination output
5. **Focus on productivity** - Substantial progress, not just note-passing

## 🚀 IMMEDIATE NEXT STEPS

1. Review completed work and current status
2. Continue development from where this session left off
3. Make substantial progress on remaining tasks
4. Generate return prompt using our dev tooling before ending

## 📞 COORDINATION PROTOCOL

**When you complete your work, you MUST run:**

``python
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.agent_handoffs import generate_mandatory_session_end_prompt

outputs = generate_mandatory_session_end_prompt(
    work_completed=['List what you completed'],
    current_status='Current project status',
    next_agent_instructions=['Instructions for next agent'],
    critical_context='Important context to preserve',
    files_modified=['Files you modified']
)

print(outputs)
"
``

This ensures seamless coordination between agents and preserves all critical context.
"""

    # Apply detick processing for clean codeblock rendering
    return detick_content(prompt_content)


def generate_mandatory_session_end_prompt(
    work_completed: List[str],
    current_status: str,
    next_agent_instructions: List[str],
    critical_context: str,
    files_modified: List[str] = None,
) -> str:
    """
    Generates a mandatory session end report summarizing completed work, project status, files modified, next agent instructions, and critical context for agent coordination.
    
    The report includes handoff requirements and immediate next steps, formatted for seamless agent-to-agent workflow. Content is processed to prevent codeblock rendering issues during handoff.
    
    Args:
        work_completed: List of completed work items for the session.
        current_status: Description of the current project status.
        next_agent_instructions: Instructions for the next agent to follow.
        critical_context: Essential context that must be preserved for continuation.
        files_modified: List of files modified during the session.
    
    Returns:
        A formatted session end prompt string with deticked content for safe embedding in agent handoff workflows.
    """
    if files_modified is None:
        files_modified = []

    timestamp = get_current_timestamp()
    current_branch = get_current_branch()
    agor_version = get_agor_version()

    session_end_content = f"""# 📋 MANDATORY SESSION END REPORT

**Generated**: {timestamp}
**Session Type**: Work Session Complete
**AGOR Version**: {agor_version}

## ✅ WORK ACCOMPLISHED

{_format_feedback_list(work_completed, 'No work completed this session')}

## 📊 CURRENT PROJECT STATUS

**Status**: {current_status or 'Status not provided'}

## 📁 FILES MODIFIED THIS SESSION

{_format_feedback_list(files_modified, 'No files modified')}

## 🎯 NEXT AGENT INSTRUCTIONS

{_format_feedback_list(next_agent_instructions, 'No specific instructions for next agent')}

## 🧠 CRITICAL CONTEXT FOR CONTINUATION

{critical_context or 'No critical context provided'}

## 🔄 HANDOFF REQUIREMENTS

The next agent should:

1. **Pull latest changes**: `git pull origin {current_branch}`
2. **Install dependencies**: `python3 -m pip install -r src/agor/tools/agent-requirements.txt`
3. **Review this report**: Understand completed work and current status
4. **Continue from current state**: Don't restart or duplicate work
5. **Use dev tooling**: All coordination must use AGOR dev tooling functions
6. **Create session end report**: Before ending their session

## 🚀 IMMEDIATE NEXT STEPS

1. Review and understand all completed work
2. Continue development from current status
3. Make substantial progress on remaining tasks
4. Generate proper session end report before stopping

---

**This report ensures seamless agent-to-agent coordination and prevents work duplication.**
"""

    # Apply detick processing for clean codeblock rendering
    return detick_content(session_end_content)


def generate_meta_feedback(
    feedback_type: str, feedback_content: str, suggestions: List[str] = None
) -> str:
    """
    Generates a formatted meta feedback report for AGOR, including feedback type, content, improvement suggestions, recommended actions, and submission instructions.
    
    Args:
        feedback_type: The category of feedback (e.g., bug, enhancement, workflow).
        feedback_content: The main feedback message.
        suggestions: Optional list of improvement suggestions.
    
    Returns:
        A deticked markdown-formatted string containing the meta feedback report.
    """
    if suggestions is None:
        suggestions = []

    timestamp = get_current_timestamp()
    agor_version = get_agor_version()

    meta_content = f"""# 🔄 AGOR Meta Feedback

**Generated**: {timestamp}
**Feedback Type**: {feedback_type}
**AGOR Version**: {agor_version}

## 📝 FEEDBACK CONTENT

{feedback_content}

## 💡 IMPROVEMENT SUGGESTIONS

{_format_feedback_list(suggestions, 'No specific suggestions provided')}

## 🎯 RECOMMENDED ACTIONS

Based on this feedback, consider:

1. **Documentation Updates**: Improve clarity and completeness
2. **Workflow Optimization**: Streamline common operations
3. **Tool Enhancement**: Add missing functionality
4. **Error Prevention**: Improve safety and validation
5. **User Experience**: Make operations more intuitive

## 📞 FEEDBACK SUBMISSION

This feedback should be:
- Reviewed by the development team
- Considered for future AGOR improvements
- Used to enhance agent coordination workflows
- Integrated into continuous improvement processes

---

**Meta feedback helps evolve AGOR into a more effective coordination platform.**
"""

    # Apply detick processing for clean codeblock rendering
    return detick_content(meta_content)


@dataclass
class HandoffRequest:
    """Configuration object for handoff operations to reduce parameter count."""

    task_description: str
    work_completed: list = None
    next_steps: list = None
    files_modified: list = None
    context_notes: str = None
    brief_context: str = None
    pr_title: str = None
    pr_description: str = None
    release_notes: str = None
    # Output selection flags for flexible generation
    generate_snapshot: bool = True
    generate_handoff_prompt: bool = True
    generate_pr_description: bool = True
    generate_release_notes: bool = True

    def __post_init__(self):
        """
        Initializes optional fields to empty lists or strings if they are None after dataclass creation.
        
        Prevents mutable default argument issues by ensuring all list and string fields have safe default values.
        """
        if self.work_completed is None:
            self.work_completed = []
        if self.next_steps is None:
            self.next_steps = []
        if self.files_modified is None:
            self.files_modified = []
        if self.context_notes is None:
            self.context_notes = ""
        if self.brief_context is None:
            self.brief_context = ""


def generate_agent_handoff_prompt_extended(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """
    Generates a comprehensive agent handoff prompt with environment details, setup instructions, memory branch access, task overview, and optional context.
    
    The prompt includes metadata such as generation timestamp, detected environment, AGOR version, and memory branch if provided. It outlines environment setup steps, AGOR initialization guidance, and instructions for accessing previous work context. Optional brief context and snapshot content are included when supplied. The output is processed to replace triple backticks with double backticks for safe embedding in single codeblocks.
    
    Args:
        task_description: Description of the task for the next agent.
        snapshot_content: Optional summary of previous agent work.
        memory_branch: Optional name of the memory branch for coordination.
        environment: Optional environment information; auto-detected if not provided.
        brief_context: Optional brief background for quick orientation.
    
    Returns:
        A formatted and deticked prompt string ready for use in a single codeblock.
    """
    if environment is None:
        from agor.tools.dev_testing import detect_environment

        environment = detect_environment()

    from agor.tools.git_operations import get_current_timestamp

    timestamp = get_current_timestamp()

    # Start building the prompt
    prompt = f"""# 🤖 AGOR Agent Handoff

**Generated**: {timestamp}
**Environment**: {environment.get('mode', 'unknown')} ({environment.get('platform', 'unknown')})
**AGOR Version**: {environment.get('agor_version', 'unknown')}
"""

    # Add memory branch information if available
    if memory_branch:
        prompt += f"""**Memory Branch**: {memory_branch}
"""

    prompt += f"""
## Task Overview
{task_description}
"""

    # Add brief context if provided
    if brief_context:
        prompt += f"""
## Quick Context
{brief_context}
"""

    # Add environment-specific setup
    from agor.tools.dev_testing import get_agent_dependency_install_commands

    prompt += f"""
## Environment Setup
{get_agent_dependency_install_commands()}

## AGOR Initialization
Read these files to understand the system:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (operational guide)
- src/agor/tools/index.md (documentation index)

Select appropriate role:
- Worker Agent: Code analysis, implementation, technical work
- Project Coordinator: Planning and multi-agent coordination
"""

    # Add memory branch access if applicable
    if memory_branch:
        prompt += f"""
## Memory Branch Access
Your coordination files are stored on memory branch: {memory_branch}

Access previous work context:
```bash
# View memory branch contents
git show {memory_branch}:.agor/
git show {memory_branch}:.agor/snapshots/
```
"""

    # Add snapshot content if provided
    if snapshot_content:
        prompt += f"""
## Previous Work Context
{snapshot_content}
"""

    prompt += """
## Getting Started
1. Initialize your environment using the setup commands above
2. Read the AGOR documentation files
3. Select your role based on the task requirements
4. Review any previous work context provided
5. Begin work following AGOR protocols

Remember: Always create a snapshot before ending your session using the dev tooling.

---
*This handoff prompt was generated automatically with environment detection and backtick processing*
"""

    # Apply backtick processing to prevent formatting issues
    processed_prompt = detick_content(prompt)

    return processed_prompt
