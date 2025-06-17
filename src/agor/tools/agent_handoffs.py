"""
Agent Handoffs Module for AGOR Development Tools

This module contains all agent coordination and handoff functionality
extracted from dev_tools.py for better organization and maintainability.

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

# Import feedback manager for modularized feedback handling
try:
    from .feedback_manager import FeedbackManager

    FEEDBACK_MANAGER_AVAILABLE = True
except ImportError:
    FEEDBACK_MANAGER_AVAILABLE = False


def get_current_branch() -> str:
    """Get current git branch name."""
    success, branch = run_git_command(["branch", "--show-current"])
    if success:
        return branch.strip()
    return "main"  # fallback


def get_agor_version() -> str:
    """Get current AGOR version."""
    try:
        import agor

        return getattr(agor, "__version__", "0.4.3+")
    except ImportError:
        return "0.4.3+"


def detick_content(content: str) -> str:
    """
    Convert triple backticks (```) to double backticks (``) for clean codeblock rendering.

    This prevents codeblocks from jumping in and out when content is used in prompts.
    Essential for agent-to-agent communication via snapshots and handoffs.

    Args:
        content: Content with potential triple backticks

    Returns:
        Content with triple backticks converted to double backticks
    """
    # Use regex to avoid runaway replacements
    # Only replace ``` that are not preceded or followed by another backtick
    pattern = r"(?<!`)```(?!`)"
    return re.sub(pattern, "``", content)


def retick_content(content: str) -> str:
    """
    Convert double backticks (``) back to triple backticks (```) for normal rendering.

    Reverses the detick_content operation when content needs to be restored
    to normal markdown format.

    Args:
        content: Content with double backticks

    Returns:
        Content with double backticks converted to triple backticks
    """
    # Use regex to avoid runaway replacements
    # Only replace `` that are not preceded or followed by another backtick
    pattern = r"(?<!`)``(?!`)"
    return re.sub(pattern, "```", content)


def _format_feedback_list(items: List[str], empty_message: str) -> str:
    """
    Formats a list of feedback items as a markdown bullet list.

    If the list is empty, returns a single bullet with the provided empty message.
    """
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def validate_feedback_input(
    feedback_type: str,
    feedback_content: str,
    severity: str = "medium",
    component: str = "general",
) -> dict:
    """
    Validates meta feedback input for type, severity, content quality, and component.

    Checks if the feedback type and severity are among allowed values, ensures the content is sufficiently descriptive, and suggests improvements based on feedback type. Returns a dictionary indicating validity, detected issues, suggestions for improvement, and normalized values for type, severity, and component.
    """
    validation = {
        "is_valid": True,
        "issues": [],
        "suggestions": [],
        "normalized_type": feedback_type,
        "normalized_severity": severity,
        "normalized_component": component,
    }

    # Validate feedback type
    valid_types = [
        "bug",
        "enhancement",
        "workflow_issue",
        "success_story",
        "documentation",
        "performance",
        "usability",
    ]
    if feedback_type not in valid_types:
        validation["issues"].append(f"Invalid feedback type: {feedback_type}")
        validation["suggestions"].append(f"Use one of: {', '.join(valid_types)}")
        validation["normalized_type"] = "general"
        validation["is_valid"] = False

    # Validate severity
    valid_severities = ["low", "medium", "high", "critical"]
    if severity not in valid_severities:
        validation["issues"].append(f"Invalid severity: {severity}")
        validation["suggestions"].append(f"Use one of: {', '.join(valid_severities)}")
        validation["normalized_severity"] = "medium"
        validation["is_valid"] = False

    # Validate content length and quality
    if not feedback_content or len(feedback_content.strip()) < 10:
        validation["issues"].append("Feedback content is too short or empty")
        validation["suggestions"].append(
            "Provide at least 10 characters of meaningful feedback"
        )
        validation["is_valid"] = False

    if len(feedback_content) > 5000:
        validation["issues"].append("Feedback content is very long")
        validation["suggestions"].append(
            "Consider breaking into multiple feedback items"
        )

    # Validate component
    common_components = [
        "dev_tools",
        "memory_system",
        "hotkeys",
        "coordination",
        "documentation",
        "git_operations",
        "agent_handoffs",
        "snapshots",
        "environment_detection",
        "workflow",
        "user_interface",
        "performance",
        "general",
    ]

    if component not in common_components:
        validation["suggestions"].append(
            f"Consider using a standard component: {', '.join(common_components[:5])}..."
        )

    # Content quality suggestions
    if feedback_type == "bug" and "reproduce" not in feedback_content.lower():
        validation["suggestions"].append("For bugs, include reproduction steps")

    if feedback_type == "enhancement" and "benefit" not in feedback_content.lower():
        validation["suggestions"].append(
            "For enhancements, explain the expected benefits"
        )

    return validation


@dataclass
class GitHubIssueConfig:
    """Configuration for GitHub issue creation."""

    feedback_type: str
    feedback_content: str
    suggestions: List[str] = None
    severity: str = "medium"
    component: str = "general"
    reproduction_steps: List[str] = None
    expected_behavior: str = None
    actual_behavior: str = None


def create_github_issue_content(config: GitHubIssueConfig) -> str:
    """
    Generates formatted GitHub issue content from a GitHubIssueConfig instance.

    Creates a structured issue template including feedback type, component, severity, description, reproduction steps, expected and actual behavior (for bugs), suggested solutions, and appropriate labels. Designed for use with AGOR meta feedback submissions.
    """
    if config.suggestions is None:
        config.suggestions = []
    if config.reproduction_steps is None:
        config.reproduction_steps = []

    # Map feedback types to GitHub labels
    type_labels = {
        "bug": "bug",
        "enhancement": "enhancement",
        "workflow_issue": "workflow",
        "success_story": "feedback",
        "documentation": "documentation",
        "performance": "performance",
        "usability": "UX",
    }

    severity_labels = {
        "low": "priority: low",
        "medium": "priority: medium",
        "high": "priority: high",
        "critical": "priority: critical",
    }

    issue_content = f"""## {config.feedback_type.replace('_', ' ').title()}

**Component**: {config.component}
**Severity**: {config.severity}

### Description

{config.feedback_content}"""

    if config.feedback_type == "bug":
        if config.reproduction_steps:
            issue_content += f"""

### Reproduction Steps

{_format_feedback_list(config.reproduction_steps, 'No reproduction steps provided')}"""

        if config.expected_behavior:
            issue_content += f"""

### Expected Behavior

{config.expected_behavior}"""

        if config.actual_behavior:
            issue_content += f"""

### Actual Behavior

{config.actual_behavior}"""

    if config.suggestions:
        issue_content += f"""

### Suggested Solutions

{_format_feedback_list(config.suggestions, 'No suggestions provided')}"""

    # Add labels section
    labels = [
        type_labels.get(config.feedback_type, "feedback"),
        severity_labels.get(config.severity, "priority: medium"),
    ]
    if config.component != "general":
        labels.append(f"component: {config.component}")

    issue_content += f"""

### Labels

{', '.join(labels)}

---

*This issue was generated from AGOR meta feedback system*
"""

    return issue_content


def get_feedback_statistics() -> dict:
    """
    Retrieves feedback usage statistics and system status.

    Returns:
        A dictionary containing feedback statistics, including total items, breakdowns by type, severity, and component, recent feedback, timestamp, available memory branches, and system status. If an error occurs, returns error details and status.
    """
    try:
        from agor.tools.memory_manager import list_memory_branches

        stats = {
            "total_feedback_items": 0,
            "feedback_by_type": {},
            "feedback_by_severity": {},
            "feedback_by_component": {},
            "recent_feedback": [],
            "timestamp": get_current_timestamp(),
        }

        # This is a placeholder implementation
        # In a real system, this would analyze stored feedback data
        memory_branches = list_memory_branches()

        stats["memory_branches_available"] = len(memory_branches)
        stats["feedback_system_status"] = "operational"

        return stats

    except Exception as e:
        return {
            "error": str(e),
            "feedback_system_status": "error",
            "timestamp": get_current_timestamp(),
        }


def generate_handoff_prompt_only(
    work_completed: List[str],
    current_status: str,
    next_agent_instructions: List[str],
    critical_context: str,
    files_modified: List[str] = None,
) -> str:
    """
    Generates a formatted handoff prompt for agent coordination in AGOR development sessions.

    Creates a structured prompt summarizing completed work, current status, instructions for the next agent, critical context, and files modified. Includes environment setup commands, coordination protocol instructions, and immediate next steps. Applies detick processing to ensure clean codeblock rendering for agent-to-agent communication.

    Args:
        work_completed: List of completed work items for the session.
        current_status: Description of the current project status.
        next_agent_instructions: Instructions or tasks for the next agent or session.
        critical_context: Essential context that must be preserved for continuity.
        files_modified: List of files modified during the session.

    Returns:
        A markdown-formatted handoff prompt with deticked content for seamless agent coordination.
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
3. **Use our dev tools** - All coordination must use our backtick processing
4. **Create return prompts** - Every session must end with coordination output
5. **Focus on productivity** - Substantial progress, not just note-passing

## 🚀 IMMEDIATE NEXT STEPS

1. Review completed work and current status
2. Continue development from where this session left off
3. Make substantial progress on remaining tasks
4. Generate return prompt using our dev tools before ending

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
    Generate mandatory session end prompt for agent coordination.

    This function creates the required session end documentation with
    deticked content for proper codeblock rendering in agent handoffs.

    Args:
        work_completed: List of completed work items
        current_status: Current project status
        next_agent_instructions: Instructions for next agent
        critical_context: Critical context to preserve
        files_modified: List of modified files

    Returns:
        Formatted session end prompt with deticked content
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
5. **Use dev tools**: All coordination must use AGOR dev tools functions
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
    suggestions: List[str] = None,
    severity: str = "medium",
    component: str = "general",
    reproduction_steps: List[str] = None,
    expected_behavior: str = None,
    actual_behavior: str = None,
    environment_info: dict = None,
) -> str:
    """
    Generates structured meta feedback for AGOR, including validation, environment details, and actionable recommendations.

    Creates a formatted feedback report with severity and type indicators, affected component, AGOR version, and environment context. For bug reports, includes sections for reproduction steps, expected and actual behavior. Lists improvement suggestions, tailored recommended actions based on feedback type, and metadata for tracking. Ensures clean markdown formatting for agent communication.
    """
    # Validate and set defaults
    if suggestions is None:
        suggestions = []
    if reproduction_steps is None:
        reproduction_steps = []

    # Validate feedback type
    valid_types = [
        "bug",
        "enhancement",
        "workflow_issue",
        "success_story",
        "documentation",
        "performance",
        "usability",
    ]
    if feedback_type not in valid_types:
        feedback_type = "general"

    # Validate severity
    valid_severities = ["low", "medium", "high", "critical"]
    if severity not in valid_severities:
        severity = "medium"

    # Auto-detect environment if not provided
    if environment_info is None:
        try:
            from agor.tools.dev_testing import detect_environment

            environment_info = detect_environment()
        except Exception:
            environment_info = {"mode": "unknown", "platform": "unknown"}

    timestamp = get_current_timestamp()
    agor_version = get_agor_version()

    # Get severity emoji
    severity_emojis = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}

    # Get type emoji
    type_emojis = {
        "bug": "🐛",
        "enhancement": "✨",
        "workflow_issue": "⚠️",
        "success_story": "🎉",
        "documentation": "📚",
        "performance": "⚡",
        "usability": "🎯",
        "general": "💭",
    }

    meta_content = f"""# {type_emojis.get(feedback_type, '💭')} AGOR Meta Feedback

**Generated**: {timestamp}
**Type**: {feedback_type.replace('_', ' ').title()}
**Severity**: {severity_emojis.get(severity, '🟡')} {severity.title()}
**Component**: {component}
**AGOR Version**: {agor_version}
**Environment**: {environment_info.get('mode', 'unknown')} ({environment_info.get('platform', 'unknown')})

## 📝 FEEDBACK CONTENT

{feedback_content}"""

    # Add bug-specific sections
    if feedback_type == "bug" and (
        reproduction_steps or expected_behavior or actual_behavior
    ):
        meta_content += """

## 🔍 BUG DETAILS"""

        if reproduction_steps:
            meta_content += f"""

### Reproduction Steps
{_format_feedback_list(reproduction_steps, 'No reproduction steps provided')}"""

        if expected_behavior:
            meta_content += f"""

### Expected Behavior
{expected_behavior}"""

        if actual_behavior:
            meta_content += f"""

### Actual Behavior
{actual_behavior}"""

    meta_content += f"""

## 💡 IMPROVEMENT SUGGESTIONS

{_format_feedback_list(suggestions, 'No specific suggestions provided')}

## 🎯 RECOMMENDED ACTIONS

Based on this {feedback_type.replace('_', ' ')} feedback, consider:"""

    # Customize recommendations based on feedback type
    if feedback_type == "bug":
        meta_content += """

1. **Bug Investigation**: Reproduce and analyze the issue
2. **Root Cause Analysis**: Identify underlying causes
3. **Fix Implementation**: Develop and test solution
4. **Regression Testing**: Ensure fix doesn't break other functionality
5. **Documentation Update**: Update relevant documentation"""

    elif feedback_type == "enhancement":
        meta_content += """

1. **Feature Analysis**: Evaluate feasibility and impact
2. **Design Planning**: Create implementation strategy
3. **User Experience**: Consider impact on agent workflows
4. **Implementation**: Develop feature with proper testing
5. **Documentation**: Add usage examples and guides"""

    elif feedback_type == "workflow_issue":
        meta_content += """

1. **Workflow Analysis**: Map current process and pain points
2. **Process Optimization**: Streamline common operations
3. **Tool Enhancement**: Add missing workflow functionality
4. **User Training**: Update documentation and examples
5. **Feedback Loop**: Monitor improvements and iterate"""

    elif feedback_type == "documentation":
        meta_content += """

1. **Content Review**: Assess current documentation quality
2. **Gap Analysis**: Identify missing or unclear sections
3. **Content Update**: Improve clarity and completeness
4. **Example Addition**: Add practical usage examples
5. **User Testing**: Validate documentation with real users"""

    else:
        meta_content += """

1. **Impact Assessment**: Evaluate significance and scope
2. **Priority Analysis**: Determine urgency and importance
3. **Resource Planning**: Allocate appropriate development effort
4. **Implementation Strategy**: Plan development approach
5. **Success Metrics**: Define how to measure improvement"""

    meta_content += f"""

## 📊 FEEDBACK METADATA

- **Feedback ID**: {timestamp.replace(':', '').replace('-', '').replace(' ', '_')}
- **Component**: {component}
- **Severity**: {severity}
- **Environment**: {environment_info.get('mode', 'unknown')}
- **Platform**: {environment_info.get('platform', 'unknown')}
- **AGOR Version**: {agor_version}

## 📞 FEEDBACK SUBMISSION INSTRUCTIONS

**IMPORTANT**: Copy the content above and manually create a GitHub issue:

1. **Go to**: https://github.com/jeremiah-k/agor/issues/new
2. **Title**: Use the feedback type and brief description (e.g., "Enhancement: Improve Git error messages")
3. **Body**: Paste the entire feedback content from above
4. **Labels**: Add `meta-feedback` and appropriate component labels
5. **Submit**: Click "Submit new issue"

**Why Manual Submission?**
- Gives you control over the submission process
- Allows you to add additional context if needed
- Prevents automatic spam and ensures thoughtful feedback

## 🏷️ SUGGESTED LABELS

When creating the GitHub issue, add these labels:
- `meta-feedback` (always include this)
- `bug` / `enhancement` / `workflow` (based on feedback type)
- `component: {component}` (e.g., `component: external-integration`)
- `priority: {severity}` (e.g., `priority: medium`)

## 🔗 RELATED RESOURCES

- [AGOR Development Guide](docs/agor-development-guide.md)
- [GitHub Issues](https://github.com/jeremiah-k/agor/issues)
- [Multi-Agent Protocols](docs/multi-agent-protocols.md)

---

**Meta feedback helps evolve AGOR into a more effective coordination platform. Thank you for contributing!**
"""

    # Use new feedback manager if available
    if FEEDBACK_MANAGER_AVAILABLE:
        try:
            feedback_manager = FeedbackManager()
            return feedback_manager.generate_meta_feedback(
                feedback_type=feedback_type,
                feedback_content=feedback_content,
                suggestions=suggestions,
                severity=severity,
                component=component,
            )
        except Exception as e:
            print(f"⚠️ Feedback manager error, using fallback: {e}")

    # Apply detick processing for clean codeblock rendering (fallback)
    return detick_content(meta_content)


# HandoffRequest available from snapshots if needed


def generate_agent_handoff_prompt_extended(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """
    Generates a comprehensive agent handoff prompt with environment, task, and context details.

    The prompt includes environment information, setup instructions, memory branch access commands, task overview, optional brief context, and previous work context if provided. It is formatted for seamless agent transitions and applies backtick processing to ensure safe embedding within single codeblocks.

    Args:
        task_description: Description of the task for the next agent.
        snapshot_content: Optional summary of previous agent work.
        memory_branch: Optional name of the memory branch for coordination.
        environment: Optional environment details; auto-detected if not provided.
        brief_context: Optional brief background for quick orientation.

    Returns:
        A formatted prompt string ready for use in a single codeblock.
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

Remember: Always create a snapshot before ending your session using the dev tools.

---
*This handoff prompt was generated automatically with environment detection and backtick processing*
"""

    # Apply backtick processing to prevent formatting issues
    processed_prompt = detick_content(prompt)

    return processed_prompt
