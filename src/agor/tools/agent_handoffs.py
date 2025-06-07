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
from typing import List

from agor.tools.git_operations import get_current_timestamp, run_git_command


def get_current_branch() -> str:
    """
    Retrieves the current Git branch name.
    
    Returns:
        The name of the current Git branch, or "main" if the branch cannot be determined.
    """
    success, branch = run_git_command(["branch", "--show-current"])
    if success:
        return branch.strip()
    return "main"  # fallback


def get_agor_version() -> str:
    """
    Retrieves the current AGOR version string.
    
    Returns:
        The AGOR version as specified in the `agor` package, or a default version string if the package is not available.
    """
    try:
        import agor
        return getattr(agor, '__version__', '0.4.3+')
    except ImportError:
        return '0.4.3+'


def detick_content(content: str) -> str:
    """
    Converts triple backticks in the input content to double backticks for consistent codeblock rendering in markdown prompts.
    
    This helps prevent codeblock formatting issues during agent-to-agent communication by ensuring that triple backticks do not interfere with prompt rendering.
    """
    # Use regex to avoid runaway replacements
    # Only replace ``` that are not preceded or followed by another backtick
    pattern = r'(?<!`)```(?!`)'
    return re.sub(pattern, '``', content)


def retick_content(content: str) -> str:
    """
    Restores triple backticks in content by converting double backticks to triple backticks.
    
    Reverses the detick_content transformation to enable standard markdown codeblock formatting.
    """
    # Use regex to avoid runaway replacements
    # Only replace `` that are not preceded or followed by another backtick
    pattern = r'(?<!`)``(?!`)'
    return re.sub(pattern, '```', content)


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
    files_modified: List[str] = None
) -> str:
    """
    Generates a structured handoff prompt for agent-to-agent coordination.
    
    Creates a formatted markdown prompt summarizing completed work, current project status, instructions for the next agent, critical context, and files modified. The prompt includes environment setup steps, critical requirements, immediate next steps, and coordination protocol, with all content processed to ensure clean codeblock rendering for seamless agent communication.
    
    Args:
        work_completed: List of items completed during the session.
        current_status: Description of the current project state.
        next_agent_instructions: Actionable instructions for the next agent or session.
        critical_context: Essential context that must be preserved for continuity.
        files_modified: List of files changed during the session.
    
    Returns:
        A deticked markdown-formatted handoff prompt for agent coordination.
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
    files_modified: List[str] = None
) -> str:
    """
    Generates a mandatory session end report prompt for agent coordination.
    
    Creates a formatted markdown report summarizing completed work, current project status, files modified, instructions for the next agent, and critical context. The prompt includes handoff requirements and immediate next steps, with all content processed to ensure clean codeblock rendering for agent communication.
    
    Args:
        work_completed: List of completed work items for the session.
        current_status: Description of the current project status.
        next_agent_instructions: Instructions for the next agent to follow.
        critical_context: Essential context to preserve for project continuity.
        files_modified: List of files modified during the session.
    
    Returns:
        A deticked markdown string containing the session end report prompt.
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
    feedback_type: str,
    feedback_content: str,
    suggestions: List[str] = None
) -> str:
    """
    Generates a formatted meta feedback report for AGOR, including feedback type, content, suggestions, and recommended actions.
    
    Args:
        feedback_type: The category of feedback (e.g., bug, enhancement, workflow).
        feedback_content: The main feedback message.
        suggestions: Optional list of improvement suggestions.
    
    Returns:
        A markdown-formatted meta feedback report with deticked content for clean codeblock rendering.
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
