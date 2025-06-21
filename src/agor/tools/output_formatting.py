"""
AGOR Output Formatting Module

Handles all output formatting for AGOR tools, ensuring consistent formatting
across all AI deployment environments.
"""

from agor.tools.agent_prompts import detick_content


def apply_output_formatting(content: str, output_type: str) -> str:
    """
    Apply AGOR's standard output formatting to content.
    
    This function processes content to ensure it's properly formatted for
    copy-paste workflows across all AI deployment environments.
    
    Args:
        content: The raw content to format
        output_type: Type of output (e.g., "handoff_prompt", "pr_description", "meta_feedback")
    
    Returns:
        Formatted content ready for display
    """
    # Remove conflicting backticks to prevent codeblock issues
    processed_content = detick_content(content)
    
    # Add appropriate headers based on output type
    if output_type == "handoff_prompt":
        header = "# 🔄 Agent Handoff Prompt"
    elif output_type == "pr_description":
        header = "# 📝 PR Description"
    elif output_type == "meta_feedback":
        header = "# 🔍 AGOR Meta Feedback"
    elif output_type == "release_notes":
        header = "# 📋 Release Notes"
    else:
        header = f"# 📄 {output_type.replace('_', ' ').title()}"
    
    return f"{header}\n\n{processed_content}"


def generate_formatted_output(content: str, output_type: str) -> str:
    """
    Generate properly formatted output wrapped in codeblock for copy-paste.

    This is the main function agents should use for all formatted output.
    It ensures consistent formatting across all AI deployment environments.

    Args:
        content: Raw content to format
        output_type: Type of output for appropriate formatting

    Returns:
        Content wrapped in codeblock with proper formatting

    Raises:
        ValueError: If content is empty or None
    """
    # Validate input
    if not content or not content.strip():
        raise ValueError("content cannot be empty")

    formatted_content = apply_output_formatting(content, output_type)

    # Wrap in codeblock using double backticks (AGOR standard)
    return f"``\n{formatted_content}\n``"


def generate_pr_description_output(pr_content: str) -> str:
    """
    Generate properly formatted PR description for copy-paste.

    NOTE: Keep PR description content BRIEF to avoid processing errors.
    Long content can cause the formatting process to fail.

    Args:
        pr_content: Raw PR description content (keep brief)

    Returns:
        Formatted PR description wrapped in codeblock
    """
    return generate_formatted_output(pr_content, "pr_description")


def generate_release_notes_output(release_content: str) -> str:
    """
    Generate properly formatted release notes for copy-paste.

    Args:
        release_content: Raw release notes content

    Returns:
        Formatted release notes wrapped in codeblock
    """
    return generate_formatted_output(release_content, "release_notes")
