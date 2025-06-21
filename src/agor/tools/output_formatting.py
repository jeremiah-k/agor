"""
AGOR Output Formatting Module

Handles all output formatting for AGOR tools, ensuring consistent formatting
across all AI deployment environments.
"""

from agor.tools.agent_prompts import detick_content


def apply_output_formatting(content: str, output_type: str) -> str:
    """
    Format content with an AGOR-standard header based on the specified output type.
    
    Removes conflicting backticks from the content and prepends a context-specific header for consistent display across AI deployment environments.
    
    Parameters:
        content (str): The raw content to be formatted.
        output_type (str): The type of output, which determines the header (e.g., "handoff_prompt", "pr_description", "meta_feedback", "release_notes").
    
    Returns:
        str: The formatted content with the appropriate header.
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
    Format content with an appropriate header and wrap it in a double-backtick codeblock for AGOR tools.
    
    Raises:
        ValueError: If the content is empty or contains only whitespace.
    
    Returns:
        The formatted content, including a header based on output_type, wrapped in a double-backtick codeblock.
    """
    # Validate input
    if not content or not content.strip():
        raise ValueError("content cannot be empty")

    formatted_content = apply_output_formatting(content, output_type)

    # Wrap in codeblock using double backticks (AGOR standard)
    return f"``\n{formatted_content}\n``"


def generate_pr_description_output(pr_content: str) -> str:
    """
    Generate a formatted pull request description wrapped in a codeblock for copy-paste workflows.
    
    Parameters:
        pr_content (str): The raw content of the pull request description.
    
    Returns:
        str: The formatted PR description, including a header and codeblock wrapping.
    """
    return generate_formatted_output(pr_content, "pr_description")


def generate_release_notes_output(release_content: str) -> str:
    """
    Generate formatted release notes wrapped in a codeblock for copy-paste workflows.
    
    Parameters:
        release_content (str): The raw content of the release notes.
    
    Returns:
        str: The formatted release notes, including a header and codeblock wrapping.
    """
    return generate_formatted_output(release_content, "release_notes")
