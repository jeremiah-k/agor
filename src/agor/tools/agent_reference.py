"""
AGOR Agent Education System

Programmatic documentation and guidance functions for AI agents.
Agents take programmatic output more seriously than markdown documentation,
reducing skimming and ensuring comprehensive understanding.

This module provides structured, callable documentation that agents can
access to get complete setup instructions, requirements, and guidance.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


def detect_platform() -> str:
    """
    Detect the current AI platform environment.
    
    Returns:
        Platform identifier: 'augment_local', 'augment_remote', 'chatgpt', 'claude', etc.
    """
    # Check for AugmentCode environment indicators
    if os.environ.get('AUGMENT_LOCAL'):
        return 'augment_local'
    if os.environ.get('AUGMENT_REMOTE'):
        return 'augment_remote'
    
    # Check for other platform indicators
    # This can be expanded as we identify platform-specific markers
    
    # Default fallback
    return 'unknown'


def detect_project_type() -> str:
    """
    Detect if working on AGOR itself or external project.
    
    Returns:
        'agor_development' or 'external_project'
    """
    current_dir = Path.cwd()
    
    # Check if we're in AGOR directory structure
    agor_indicators = [
        'src/agor/tools',
        'docs/agor-development-guide.md',
    ]
    
    # Check pyproject.toml for AGOR-specific content
    pyproject_file = current_dir / 'pyproject.toml'
    if pyproject_file.exists():
        try:
            with open(pyproject_file, 'r', encoding='utf-8') as f:
                pyproject_content = f.read()
                if 'name = "agor"' in pyproject_content:
                    agor_indicators.append('pyproject.toml')
        except (IOError, UnicodeDecodeError):
            pass
    
    for indicator in agor_indicators:
        if (current_dir / indicator).exists():
            return 'agor_development'
    
    return 'external_project'


def resolve_agor_paths(project_type: str, custom_path: Optional[str] = None) -> Dict[str, str]:
    """
    Resolve AGOR file paths based on project type and environment.

    Args:
        project_type: 'agor_development' or 'external_project'
        custom_path: Optional custom AGOR installation path (supports ~ and relative paths)

    Returns:
        Dictionary with resolved paths for documentation files
    """
    if custom_path:
        # Expand user home directory and resolve to absolute path
        resolved_path = Path(custom_path).expanduser().resolve()
        base_path = resolved_path.as_posix()
    elif project_type == 'agor_development':
        base_path = 'src/agor'
    else:
        # External project - try common locations
        common_locations = [
            '~/agor/src/agor',
            '~/dev/agor/src/agor',
            '/opt/agor/src/agor'
        ]

        for location in common_locations:
            expanded_path = Path(location).expanduser()
            if expanded_path.exists():
                base_path = expanded_path.as_posix()
                break
        else:
            # Fallback to relative path assumption
            base_path = 'src/agor'

    base = Path(base_path)
    return {
        'tools_path': (base / 'tools').as_posix(),
        'readme_ai': (base / 'tools' / 'README_ai.md').as_posix(),
        'instructions': (base / 'tools' / 'AGOR_INSTRUCTIONS.md').as_posix(),
        'start_here': (base / 'tools' / 'agent-start-here.md').as_posix(),
        'index': (base / 'tools' / 'index.md').as_posix(),
        'external_guide': (base / 'tools' / 'EXTERNAL_INTEGRATION_GUIDE.md').as_posix()
    }


def get_platform_specific_instructions(platform: str, project_type: str) -> str:
    """
    Get platform-specific setup instructions and quirks.
    
    Args:
        platform: Platform identifier
        project_type: Project type identifier
        
    Returns:
        Platform-specific instruction text
    """
    instructions = {
        'augment_local': {
            'external_project': '''
### AugmentCode Local Agent - External Project Setup

**CRITICAL**: Use external integration system for projects outside AGOR:

```python
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()
tools.print_status()  # Verify integration works
```

**Environment**: Direct workspace access, persistent guidelines, full file system access.
**Memory**: Enhanced through Augment system with persistent User Guidelines.
**Dependencies**: May need venv setup for AGOR tools if using development functions.
            ''',
            'agor_development': '''
### AugmentCode Local Agent - AGOR Development

**Direct Access**: Working on AGOR itself, use direct imports:

```python
from agor.tools.dev_tools import create_development_snapshot, test_all_tools
```

**Environment**: Full AGOR development environment with all tools available.
**Memory**: Persistent User Guidelines and direct access to all AGOR documentation.
            '''
        },
        'augment_remote': {
            'external_project': '''
### AugmentCode Remote Agent - External Project Setup

**CRITICAL**: Use external integration system for projects outside AGOR:

```python
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()
tools.print_status()  # Verify integration works
```

**Environment**: Remote execution environment with workspace access.
**Memory**: Session-based memory, use snapshots for continuity.
**Dependencies**: AGOR tools should be pre-installed in remote environment.
            ''',
            'agor_development': '''
### AugmentCode Remote Agent - AGOR Development

**Direct Access**: Working on AGOR itself, use direct imports:

```python
from agor.tools.dev_tools import create_development_snapshot, test_all_tools
```

**Environment**: Remote AGOR development environment with all tools available.
**Memory**: Session-based memory, create comprehensive snapshots for handoffs.
            '''
        },
        'chatgpt': {
            'external_project': '''
### ChatGPT - External Project Setup

**File Upload**: Upload AGOR documentation files to conversation.
**Memory**: Limited to conversation context, use snapshots for continuity.
**Integration**: Use external integration system if AGOR installed separately.
            ''',
            'agor_development': '''
### ChatGPT - AGOR Development

**File Upload**: Upload AGOR source files and documentation.
**Memory**: Use conversation memory and file uploads for context.
**Development**: Limited code execution, focus on analysis and planning.
            '''
        },
        'unknown': {
            'external_project': '''
### Unknown Platform - External Project

**Integration**: Try external integration system first:
```python
from agor.tools.external_integration import get_agor_tools
```

**Fallback**: If integration fails, request AGOR documentation upload or access.
            ''',
            'agor_development': '''
### Unknown Platform - AGOR Development

**Access**: Ensure access to AGOR source code and documentation.
**Integration**: Use direct imports if working within AGOR environment.
            '''
        }
    }
    
    return instructions.get(platform, instructions['unknown']).get(project_type, 
                                                                   instructions['unknown']['external_project'])


def generate_deployment_prompt(platform: Optional[str] = None, 
                             project_type: Optional[str] = None,
                             custom_paths: Optional[Dict[str, str]] = None) -> str:
    """
    Generate complete deployment prompt for AI agents.
    
    Args:
        platform: Platform identifier (auto-detected if None)
        project_type: Project type (auto-detected if None)  
        custom_paths: Custom path overrides
        
    Returns:
        Complete deployment prompt ready for copy-paste
    """
    # Auto-detect if not provided
    if platform is None:
        platform = detect_platform()
    if project_type is None:
        project_type = detect_project_type()
    
    # Resolve paths with fallback to defaults
    default_paths = resolve_agor_paths(project_type)
    paths = {**default_paths, **custom_paths} if custom_paths else default_paths
    
    # Get platform-specific instructions
    platform_instructions = get_platform_specific_instructions(platform, project_type)
    
    # Generate complete prompt
    prompt = f"""I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files from workspace sources to understand the system:
- {paths['readme_ai']} (role selection and initialization)
- {paths['instructions']} (comprehensive operational guide)
- {paths['start_here']} (quick startup guide)
- {paths['index']} (documentation index for efficient lookup)

Read as much AGOR documentation as you need to maintain a good workflow. Analyze the snapshot system and its templates. Understand memory branches and how they operate.

{platform_instructions}

# <--- Add your detailed step-by-step instructions below --->

**As we approach the end of our work in this branch, be prepared to use the dev tools as we finish. If asked, be prepared to create a PR summary and release notes using the dev tools, wrapping the output of each in a single codeblock (for easy copying & pasting). You might also be expected to create a handoff prompt for another agent, containing full initialization instructions and how to use the dev tools to read the snapshot with the rest of the context, if applicable. Be prepared to give me these deliverables (each with its output/content wrapped in its own single codeblock) at the end of each series of changes, so I do not need to ask for everything individually.**

---
Platform: {platform} | Project: {project_type} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    return prompt


def get_memory_branch_guide() -> str:
    """
    Comprehensive guide to AGOR memory branch system.

    Returns:
        Formatted guide explaining memory branches and cross-branch operations
    """
    guide = """
🧠 AGOR MEMORY BRANCH SYSTEM - CRITICAL UNDERSTANDING

═══════════════════════════════════════════════════════════════════

🚨 FUNDAMENTAL RULE: .agor/ directories exist ONLY on memory branches

📋 MEMORY BRANCH ARCHITECTURE:
• Memory branches: agor/mem/main, agor/mem/feature-name, etc.
• Working branches: main, feature-branches, development branches
• .agor/ directory structure exists exclusively on memory branches
• Cross-branch commits: Memory operations commit to memory branch while staying on working branch

📋 MEMORY BRANCH OPERATIONS:
• Dev tools automatically handle memory branch creation and switching
• Snapshots saved to .agor/snapshots/ on memory branches
• Agent coordination files in .agor/agents/ on memory branches
• Never manually create .agor/ directories on working branches

📋 CROSS-BRANCH COMMIT DESIGN:
• You work on feature-branch-A
• Dev tools commit snapshot to agor/mem/main
• You remain on feature-branch-A throughout
• Memory and working branches stay synchronized but separate

📋 WHY THIS ARCHITECTURE:
• Keeps working branches clean of coordination files
• Enables seamless agent handoffs without polluting project history
• Allows multiple agents to coordinate without merge conflicts
• Maintains clear separation between project code and agent coordination

📋 COMMON MISTAKES TO AVOID:
• Never create .agor/ directories manually on working branches
• Don't try to access memory files directly - use dev tools
• Don't commit .agor/ files to working branches
• Don't switch to memory branches manually for file access

═══════════════════════════════════════════════════════════════════
✅ Use dev tools for all memory operations - they handle the complexity
"""
    return guide


def get_coordination_guide() -> str:
    """
    Multi-agent coordination patterns and requirements.

    Returns:
        Formatted guide for agent coordination and communication
    """
    guide = """
🤝 AGOR MULTI-AGENT COORDINATION GUIDE

═══════════════════════════════════════════════════════════════════

📋 COORDINATION PRINCIPLES:
• Each agent creates their own snapshots with complete context
• Use agentconvo.md for cross-agent communication
• Handoff prompts contain full initialization instructions
• Memory branches enable seamless context preservation

📋 AGENT COMMUNICATION PATTERNS:
• Update .agor/shared/agentconvo.md with status and findings
• Include current work, decisions made, and blockers encountered
• Reference specific snapshots and commits for context
• Provide clear handoff instructions for continuing agents

📋 SNAPSHOT HANDOFF REQUIREMENTS:
• Every snapshot must include meaningful next_steps
• Provide specific, actionable continuation instructions
• Include context about decisions made and rationale
• Reference relevant files, functions, and documentation

📋 COORDINATION STRATEGIES:
• Parallel Divergent: Independent exploration → synthesis
• Pipeline: Sequential snapshots with specialization
• Swarm: Dynamic task assignment from shared queue
• Red Team: Adversarial build/break cycles
• Mob Programming: Collaborative real-time coding

📋 HANDOFF BEST PRACTICES:
• Generate handoff prompts with full initialization context
• Include platform-specific setup instructions
• Provide clear success criteria and validation steps
• Reference all relevant snapshots and coordination files

═══════════════════════════════════════════════════════════════════
✅ Effective coordination enables seamless multi-agent development
"""
    return guide


def get_role_selection_guide() -> str:
    """
    Decision tree and guidance for selecting appropriate AGOR role.

    Returns:
        Formatted guide for Worker Agent vs Project Coordinator selection
    """
    guide = """
🎯 AGOR ROLE SELECTION GUIDE - CHOOSE THE RIGHT ROLE

═══════════════════════════════════════════════════════════════════

📋 ROLE DECISION TREE:

🔍 WORKER AGENT - Choose when you need to:
• Analyze existing codebase and understand current implementation
• Implement specific features, bug fixes, or enhancements
• Debug issues and troubleshoot technical problems
• Write, modify, or refactor code directly
• Create technical documentation and code explanations
• Execute specific development tasks with clear requirements
• Work within established architecture and patterns

📋 PROJECT COORDINATOR - Choose when you need to:
• Plan project architecture and high-level design decisions
• Break down large projects into manageable tasks
• Coordinate multiple agents or development streams
• Make strategic technology and approach decisions
• Manage project timelines and resource allocation
• Design multi-agent workflows and coordination strategies
• Oversee project direction and ensure alignment with goals

📋 DECISION FACTORS:

🔍 Choose WORKER AGENT if:
• Task is implementation-focused
• Requirements are clearly defined
• Working within existing codebase
• Need hands-on coding and technical work
• Debugging or troubleshooting specific issues
• Creating documentation for existing features

📋 Choose PROJECT COORDINATOR if:
• Task involves planning and strategy
• Need to break down complex requirements
• Managing multiple workstreams or agents
• Making architectural decisions
• Coordinating team efforts
• Setting project direction and priorities

📋 ROLE SWITCHING:
• You can switch roles during a project as needs change
• Use snapshots to transition between roles effectively
• Project Coordinator can hand off to Worker Agent for implementation
• Worker Agent can escalate to Project Coordinator for strategic decisions

═══════════════════════════════════════════════════════════════════
✅ Choose the role that best matches your current task requirements
"""
    return guide


def get_external_integration_guide() -> str:
    """
    Comprehensive guide for external project integration.

    Returns:
        Formatted guide for setting up AGOR with external projects
    """
    guide = """
🔗 AGOR EXTERNAL PROJECT INTEGRATION GUIDE

═══════════════════════════════════════════════════════════════════

🚨 CRITICAL: Use external integration when AGOR is installed separately from your project

📋 SETUP PROCESS:

Step 1: Import External Integration System
```python
from agor.tools.external_integration import get_agor_tools
```

Step 2: Initialize AGOR Tools
```python
tools = get_agor_tools()
tools.print_status()  # Verify integration works
```

Step 3: Use AGOR Functions Through Tools Object
```python
# Create snapshots
tools.create_development_snapshot("title", "context", ["next", "steps"])

# Generate formatted outputs
tools.generate_pr_description_output("content")
tools.generate_handoff_prompt_output("content")
tools.generate_release_notes_output("content")

# Workspace operations
tools.quick_commit_and_push("message", "emoji")
tools.get_workspace_status()
tools.test_all_tools()
```

📋 WHY EXTERNAL INTEGRATION IS NEEDED:
• Direct imports fail when AGOR installed separately from project
• Path resolution issues with different installation locations
• Module not found errors when using from agor.tools.dev_tools import
• External integration provides automatic detection and fallback mechanisms

📋 TROUBLESHOOTING:

Problem: ModuleNotFoundError: No module named 'agor'
Solution: Use external integration system instead of direct imports

Problem: AGOR tools not found
Solution: Check AGOR installation path and use custom_path parameter

Problem: Functions not working
Solution: Verify tools.print_status() shows successful integration

📋 INSTALLATION LOCATIONS:
• ~/agor/src/agor (common user installation)
• ~/dev/agor/src/agor (development setup)
• /opt/agor/src/agor (system installation)
• Custom locations supported with custom_path parameter

═══════════════════════════════════════════════════════════════════
✅ Always use external integration for projects outside AGOR repository
"""
    return guide


def get_dev_tools_reference() -> str:
    """
    Complete AGOR dev tools function reference with examples.

    Returns:
        Formatted reference guide for all dev tools functions
    """
    guide = """
🛠️ AGOR DEV TOOLS COMPLETE REFERENCE

═══════════════════════════════════════════════════════════════════

📋 SNAPSHOT FUNCTIONS:
• create_development_snapshot(title, context, next_steps)
  - Creates comprehensive development snapshot
  - Requires meaningful next_steps list
  - Saves to memory branch automatically

• generate_handoff_prompt_output(content)
  - Formats handoff prompts for agent transitions
  - Includes full initialization instructions
  - Output wrapped in single codeblock for copy-paste

📋 OUTPUT FORMATTING FUNCTIONS:
• generate_pr_description_output(content) - Brief content only
• generate_release_notes_output(content) - Brief content only
• generate_handoff_prompt_output(content) - Can be full length
• All functions handle deticking and codeblock wrapping automatically

📋 WORKSPACE FUNCTIONS:
• get_workspace_status() - Git status, branch info, recent commits
• quick_commit_and_push(message, emoji) - Commit and push with formatting
• test_all_tools() - Verify all dev tools work correctly

📋 MEMORY MANAGEMENT:
• cleanup_memory_branches() - Remove old memory branches
• initialize_agent_workspace() - Set up agent directories
• check_pending_handoffs() - Find pending agent transitions

📋 EDUCATION FUNCTIONS:
• get_agor_initialization_guide() - Complete setup instructions
• get_snapshot_requirements() - Critical snapshot information
• get_memory_branch_guide() - Memory system understanding
• get_coordination_guide() - Multi-agent coordination patterns

📋 USAGE EXAMPLES:
```python
# Create snapshot with proper next steps
create_development_snapshot(
    title="Implement user authentication",
    context="Added JWT auth with bcrypt hashing...",
    next_steps=[
        "Test authentication with edge cases",
        "Add rate limiting to login endpoint",
        "Update API documentation"
    ]
)

# Generate formatted PR description
pr_content = "Brief description of changes..."
formatted_pr = generate_pr_description_output(pr_content)
print(formatted_pr)  # Ready for copy-paste
```

═══════════════════════════════════════════════════════════════════
✅ Use these functions for all AGOR operations - never manual processes
"""
    return guide


def get_output_formatting_requirements() -> str:
    """
    Critical output formatting requirements for AGOR deliverables.

    Returns:
        Formatted guide for proper output formatting and copy-paste workflow
    """
    guide = """
📋 AGOR OUTPUT FORMATTING REQUIREMENTS - CRITICAL

═══════════════════════════════════════════════════════════════════

🚨 MANDATORY: ALL generated outputs MUST use proper formatting functions

📋 FORMATTING WORKFLOW:

Step 1: Agent Creates Content Normally
• Write PR descriptions, handoff prompts, release notes with regular codeblocks
• Use normal ``` codeblocks within content as needed
• Don't worry about formatting conflicts during content creation

Step 2: Use AGOR Formatting Functions
```python
# For PR descriptions (brief content only)
formatted_pr = generate_pr_description_output(pr_content)

# For release notes (brief content only)
formatted_release = generate_release_notes_output(release_content)

# For handoff prompts (can be full length)
formatted_handoff = generate_handoff_prompt_output(handoff_content)
```

Step 3: Copy-Paste Workflow
• Functions automatically detick content (``` becomes ``)
• Functions wrap in single outer codeblock for copy-paste
• User copies the formatted output
• User runs `agor retick` to restore backticks

📋 WHY THIS PROCESS IS CRITICAL:
• Prevents nested codeblock conflicts
• Ensures consistent formatting across all outputs
• Enables seamless copy-paste workflow
• Maintains proper markdown structure

📋 CONTENT LENGTH REQUIREMENTS:
• PR descriptions: BRIEF content only (avoid processing errors)
• Release notes: BRIEF content only (avoid processing errors)
• Handoff prompts: Can be full length with comprehensive details
• Snapshots: Complete context and comprehensive information

📋 COMMON MISTAKES TO AVOID:
• Never manually wrap content in codeblocks
• Don't try to handle deticking manually
• Always use the formatting functions
• Don't skip the formatting step for deliverables

📋 CLI COMMANDS FOR USERS:
• `agor detick` - Remove backticks from content
• `agor retick` - Restore backticks to content
• Used in copy-paste workflow for processing AGOR outputs

═══════════════════════════════════════════════════════════════════
✅ Always use formatting functions - never manual codeblock wrapping
"""
    return guide


# Export main functions for easy access
__all__ = [
    'generate_deployment_prompt',
    'detect_platform',
    'detect_project_type',
    'resolve_agor_paths',
    'get_platform_specific_instructions',
    'get_memory_branch_guide',
    'get_coordination_guide',
    'get_dev_tools_reference',
    'get_role_selection_guide',
    'get_external_integration_guide',
    'get_output_formatting_requirements'
]
