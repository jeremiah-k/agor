"""
Template Engine for AGOR 0.5.1

This module provides Jinja2-based template rendering for snapshots, handoff prompts,
and other generated content, replacing string concatenation with maintainable templates.

Key Features:
- Jinja2 template rendering
- Built-in template library
- Custom filters and functions
- Template validation and error handling
"""

import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("⚠️ Jinja2 not available. Install with: pip install jinja2")


class TemplateEngine:
    """
    Jinja2-based template engine for AGOR content generation.

    Provides template rendering with custom filters and functions
    for generating snapshots, handoff prompts, and other content.
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize the template engine.

        Args:
            template_dir: Directory containing template files. Defaults to built-in templates.
        """
        self.template_dir = template_dir or Path(__file__).parent / "templates"
        self.template_dir.mkdir(parents=True, exist_ok=True)

        if JINJA2_AVAILABLE:
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=select_autoescape(["html", "xml"]),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            self._register_custom_filters()
            self._register_custom_functions()
        else:
            self.env = None

        self._ensure_default_templates()

    def _register_custom_filters(self) -> None:
        """Register custom Jinja2 filters for AGOR templates."""
        if not self.env:
            return

        def format_timestamp(
            timestamp: datetime.datetime, format_str: str = "%Y-%m-%d %H:%M:%S"
        ) -> str:
            """Format datetime timestamp."""
            return timestamp.strftime(format_str)

        def truncate_commit(commit_hash: str, length: int = 8) -> str:
            """Truncate git commit hash."""
            return (
                commit_hash[:length] + "..."
                if len(commit_hash) > length
                else commit_hash
            )

        def format_list(
            items: List[str], prefix: str = "- ", join_str: str = "\n"
        ) -> str:
            """Format list items with prefix."""
            return join_str.join(f"{prefix}{item}" for item in items)

        def safe_filename(text: str, max_length: int = 30) -> str:
            """Create safe filename from text."""
            safe_text = "".join(c for c in text if c.isalnum() or c in "-_")
            return safe_text[:max_length]

        # Register filters using the filters dictionary
        self.env.filters.update(
            {
                "format_timestamp": format_timestamp,
                "truncate_commit": truncate_commit,
                "format_list": format_list,
                "safe_filename": safe_filename,
            }
        )

    def _register_custom_functions(self) -> None:
        """Register custom Jinja2 global functions."""
        if not self.env:
            return

        def current_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
            """Get current timestamp."""
            return datetime.datetime.now().strftime(format_str)

        def enumerate_items(items: List[str], start: int = 1) -> List[tuple]:
            """Enumerate items with custom start."""
            return list(enumerate(items, start))

        self.env.globals.update(
            {"current_timestamp": current_timestamp, "enumerate_items": enumerate_items}
        )

    def _ensure_default_templates(self) -> None:
        """Create default templates if they don't exist."""
        templates = {
            "snapshot.md.j2": self._get_snapshot_template(),
            "handoff_prompt.md.j2": self._get_handoff_template(),
            "completion_report.md.j2": self._get_completion_template(),
            "pr_description.md.j2": self._get_pr_description_template(),
        }

        for template_name, template_content in templates.items():
            template_path = self.template_dir / template_name
            if not template_path.exists():
                template_path.write_text(template_content)

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.

        Args:
            template_name: Name of the template file
            context: Template context variables

        Returns:
            Rendered template content
        """
        if not JINJA2_AVAILABLE:
            return self._fallback_render(template_name, context)

        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception:
            logging.exception(
                "Template rendering error while rendering %s", template_name
            )
            return self._fallback_render(template_name, context)

    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Render a template string with the given context.

        Args:
            template_string: Template content as string
            context: Template context variables

        Returns:
            Rendered template content
        """
        if not JINJA2_AVAILABLE:
            return template_string.format(**context)

        try:
            template = self.env.from_string(template_string)
            return template.render(**context)
        except Exception as e:
            print(f"⚠️ String template rendering error: {e}")
            return template_string.format(**context)

    def _fallback_render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Fallback rendering using string formatting when Jinja2 is not available.

        Note: This fallback only supports simple variable substitution and will not
        handle Jinja2 features like loops, conditionals, or filters.
        """
        template_path = self.template_dir / template_name
        if template_path.exists():
            template_content = template_path.read_text()
            try:
                # Warn about limitations
                if any(pattern in template_content for pattern in ["{%", "|", "{#"]):
                    print(
                        f"⚠️ Template '{template_name}' uses Jinja2 features not supported in fallback mode"
                    )
                return template_content.format(**context)
            except KeyError as e:
                print(f"⚠️ Template variable missing: {e}")
                return template_content
            except Exception as e:
                print(f"⚠️ Fallback rendering failed: {e}")
                return template_content
        else:
            return f"Template not found: {template_name}"

    def _get_snapshot_template(self) -> str:
        """Get the default snapshot template."""
        return """# 📸 Agent Snapshot Document

**Generated**: {{ current_timestamp() }}
**From Agent Role**: {{ agent_role }}
**Snapshot Reason**: {{ snapshot_reason }}
**AGOR Version**: {{ agor_version }}

## 📚 MANDATORY: Documentation Reading Requirement

**CRITICAL**: Before proceeding with any work, the receiving agent MUST read these core AGOR documentation files:

### Required Reading (In Order):
1. **`src/agor/tools/README_ai.md`** - Role selection and initialization protocol
2. **`src/agor/tools/AGOR_INSTRUCTIONS.md`** - Comprehensive operational instructions and hotkey menus
3. **`src/agor/tools/agent-start-here.md`** - Quick entry point for ongoing projects

### Verification Checklist:
- [ ] Read README_ai.md completely - understand role selection and initialization
- [ ] Read AGOR_INSTRUCTIONS.md completely - understand hotkeys, protocols, and workflows
- [ ] Read agent-start-here.md completely - understand project entry procedures
- [ ] Understand current AGOR version: {{ agor_version }}
- [ ] Understand snapshot system and coordination protocols
- [ ] Ready to follow AGOR protocols consistently

**No work should begin until all documentation is read and understood.**

## 🔧 Environment Context

**Git Branch**: `{{ git_context.branch }}`
**Current Commit**: `{{ git_context.current_commit | truncate_commit }}`
**Repository Status**: {{ 'Clean' if not git_context.status else 'Has uncommitted changes' }}

## 🎯 Problem Definition

{{ problem_description }}

## 📊 Current Status

**Overall Progress**: {{ current_status }}
**Estimated Completion**: {{ estimated_completion }}

## ✅ Work Completed

{{ work_completed | format_list }}

## 📝 Commits Made

{{ commits_made | format_list("- `", "`") }}

## 📁 Files Modified

{{ files_modified | format_list("- `", "`") }}

## 🔄 Next Steps

{% for step in next_steps -%}
{{ loop.index }}. {{ step }}
{% endfor %}

## 🧠 Context & Important Notes

{{ context_notes }}

## 🔧 Technical Context

### Git Repository State
**Branch**: `{{ git_context.branch }}`
**Current Commit**: `{{ git_context.current_commit }}`

### Repository Status
```
{{ git_context.status if git_context.status else 'Working directory clean' }}
```

### Uncommitted Changes
{% if git_context.uncommitted_changes -%}
{{ git_context.uncommitted_changes | format_list("- `", "`") }}
{% else -%}
- None
{% endif %}

### Staged Changes
{% if git_context.staged_changes -%}
{{ git_context.staged_changes | format_list("- `", "`") }}
{% else -%}
- None
{% endif %}

### Recent Commit History
```
{{ git_context.recent_commits }}
```

### Key Files to Review
{% for file in files_modified[:5] -%}
- `{{ file }}` - Review recent changes and understand current state
{% endfor %}

## 🎯 Snapshot Instructions for Receiving Agent (If Applicable)

### 1. Environment Verification
```bash
# Verify you're on the correct branch
git checkout {{ git_context.branch }}

# Verify you're at the correct commit
git log --oneline -1
# Should show: {{ git_context.current_commit | truncate_commit }}

# Check AGOR version compatibility
# This snapshot was created with AGOR {{ agor_version }}
```

### 2. Context Loading
```bash
# Review the current state
git status
git log --oneline -10

# Examine modified files
{% for file in files_modified[:3] -%}
# Review {{ file }}
{% endfor %}
```

### 3. Verify Understanding
- [ ] Read and understand the problem definition
- [ ] Review all completed work items
- [ ] Examine commits and understand changes made
- [ ] Verify current status matches expectations
- [ ] Understand the next steps planned
- [ ] Verify AGOR version compatibility
- [ ] Confirm you're on the correct git branch and commit

### 4. Continue Work
- [ ] Start with the first item in "Next Steps"
- [ ] Update this snapshot document with your progress
- [ ] Commit regularly with clear messages
- [ ] Update `.agor/agentconvo.md` with your status

### 5. Communication Protocol
- Update `.agor/agentconvo.md` with snapshot received confirmation (if applicable)
- Log major decisions and progress updates
- Create new snapshot document if passing to another agent or for archival

---

**Receiving Agent**: Please confirm snapshot receipt (if applicable) by updating `.agor/agentconvo.md` with:
```
[AGENT-ID] [{{ current_timestamp() }}] - SNAPSHOT RECEIVED: {{ problem_description[:50] }}...
```"""

    def _get_handoff_template(self) -> str:
        """Get the default handoff prompt template."""
        return """# 📋 MANDATORY SESSION END REPORT

**Generated**: {{ current_timestamp() }}
**Session Type**: {{ session_type | default('Work Session Complete') }}
**AGOR Version**: {{ agor_version }}

## ✅ WORK ACCOMPLISHED

{{ work_completed | format_list }}

## 📊 CURRENT PROJECT STATUS

**Status**: {{ current_status }}

## 📁 FILES MODIFIED THIS SESSION

{{ files_modified | format_list }}

## 🎯 NEXT AGENT INSTRUCTIONS

{{ next_agent_instructions | format_list }}

## 🧠 CRITICAL CONTEXT FOR CONTINUATION

{{ critical_context }}

## 🔄 HANDOFF REQUIREMENTS

The next agent should:

1. **Pull latest changes**: `git pull origin {{ git_context.branch }}`
2. **Install dependencies**: `python3 -m pip install -r src/agor/tools/agent-requirements.txt`
3. **Review this report**: Understand completed work and current status
4. **Continue from current state**: Don't restart or duplicate work
5. **Use dev tools**: All coordination must use AGOR dev tools functions
6. **Create session end report**: Before ending their session

## 🚀 IMMEDIATE NEXT STEPS

{% for step in immediate_next_steps | default(['Review and understand all completed work', 'Continue development from current status', 'Make substantial progress on remaining tasks', 'Generate proper session end report before stopping']) -%}
{{ loop.index }}. {{ step }}
{% endfor %}

---

**This report ensures seamless agent-to-agent coordination and prevents work duplication.**"""

    def _get_completion_template(self) -> str:
        """Get the default completion report template."""
        return """# 📦 AGOR Snapshot: Task Completion Report

## Snapshot ID
{{ current_timestamp('%Y%m%dT%H%M%S') }}-task-completion

## Author
{{ agent_role }}

## Strategy
{{ strategy | default('[Strategy from coordination system]') }}

## Assigned To
{{ coordinator_id }}

## Memory Branch
agor/mem/{{ current_timestamp('%Y%m%dT%H%M')[:13] }}

## Context
Task completion report for: {{ original_task }}

## Task Status
{{ final_status }}

📘 **If you're unfamiliar with task completion reports, read the following before proceeding:**
- `src/agor/tools/SNAPSHOT_SYSTEM_GUIDE.md`
- `src/agor/tools/AGOR_INSTRUCTIONS.md`
- `src/agor/tools/README_ai.md`
- `src/agor/tools/agent-start-here.md`

## Original Task
{{ original_task }}

## Work Completed
{{ work_completed | format_list }}

## Files Modified
{{ files_modified | format_list("- `", "` - [Description of changes]") }}

## Commits Made
{{ commits_made | format_list("- `", "`") }}

## Results Summary
{{ results_summary }}

## Issues Encountered
{{ issues_encountered | default('None') }}

## Recommendations
{{ recommendations | default('None') }}

## Technical Context
**Git Branch**: `{{ git_context.branch }}`
**Current Commit**: `{{ git_context.current_commit }}`"""

    def _get_pr_description_template(self) -> str:
        """Get the default PR description template."""
        return """## 🎯 Summary

{{ summary }}

## ✅ Changes Made

{{ changes_made | format_list }}

## 🧪 Testing

{{ testing_notes | default('- Manual testing completed') | format_list }}

## 📋 Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Tests added/updated for new functionality
- [ ] Documentation updated if needed
- [ ] No breaking changes introduced

## 🔗 Related Issues

{{ related_issues | default('None') }}

## 📝 Additional Notes

{{ additional_notes | default('None') }}"""


# Convenience functions for backward compatibility
def render_snapshot_template(context: Dict[str, Any]) -> str:
    """Render snapshot template with given context."""
    engine = TemplateEngine()
    return engine.render_template("snapshot.md.j2", context)


def render_handoff_template(context: Dict[str, Any]) -> str:
    """Render handoff prompt template with given context."""
    engine = TemplateEngine()
    return engine.render_template("handoff_prompt.md.j2", context)


def render_completion_template(context: Dict[str, Any]) -> str:
    """Render completion report template with given context."""
    engine = TemplateEngine()
    return engine.render_template("completion_report.md.j2", context)
