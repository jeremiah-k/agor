"""
Feedback Management System for AGOR 0.5.1

This module provides modularized feedback logic extracted from agent_handoffs.py,
offering better organization and maintainability for meta feedback collection.

Key Features:
- Structured feedback collection
- GitHub issue generation
- Feedback statistics and analysis
- Template-based feedback formatting
- Feedback validation and processing
"""

import datetime
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from agor.tools.template_engine import TemplateEngine

# Define allowed severity levels
ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}


@dataclass
class FeedbackEntry:
    """Structured feedback entry."""
    feedback_type: str
    feedback_content: str
    suggestions: List[str] = field(default_factory=list)
    severity: str = "medium"
    component: str = "general"
    reproduction_steps: List[str] = field(default_factory=list)
    expected_behavior: Optional[str] = None
    actual_behavior: Optional[str] = None
    timestamp: Optional[str] = None
    agent_id: Optional[str] = None


@dataclass
class GitHubIssueConfig:
    """Configuration for GitHub issue creation."""
    feedback_type: str
    feedback_content: str
    suggestions: List[str] = field(default_factory=list)
    severity: str = "medium"
    component: str = "general"
    reproduction_steps: List[str] = field(default_factory=list)
    expected_behavior: Optional[str] = None
    actual_behavior: Optional[str] = None


class FeedbackManager:
    """
    Manages feedback collection, processing, and analysis for AGOR.
    
    Provides structured feedback management with template-based formatting,
    GitHub issue generation, and feedback analytics.
    """
    
    def __init__(self, feedback_dir: Optional[Path] = None):
        """
        Initializes the FeedbackManager with a feedback storage directory, template engine, and loads existing feedback history.
        
        If no directory is specified, defaults to '.agor/feedback' in the current working directory.
        """
        self.feedback_dir = feedback_dir or Path(".agor/feedback")
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        
        self.template_engine = TemplateEngine()
        self.feedback_history: List[FeedbackEntry] = []
        self._load_feedback_history()
    
    def _load_feedback_history(self) -> None:
        """
        Loads feedback history from the feedback directory, deserializing entries from JSON.
        
        If the history file is corrupted or contains invalid data, creates a timestamped backup and prints a warning.
        """
        history_file = self.feedback_dir / "feedback_history.json"
        if history_file.exists():
            try:
                with open(history_file) as f:
                    history_data = json.load(f)
                
                for entry_data in history_data.get("feedback", []):
                    entry = FeedbackEntry(**entry_data)
                    self.feedback_history.append(entry)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"⚠️ Error loading feedback history: {e}")
                # Create backup of corrupted file
                self._backup_corrupted_file(history_file, e)
    
    def _save_feedback_history(self) -> None:
        """
        Persists the current feedback history to a JSON file in the feedback directory.
        """
        history_file = self.feedback_dir / "feedback_history.json"
        
        history_data = {
            "feedback": [
                {
                    "feedback_type": entry.feedback_type,
                    "feedback_content": entry.feedback_content,
                    "suggestions": entry.suggestions,
                    "severity": entry.severity,
                    "component": entry.component,
                    "reproduction_steps": entry.reproduction_steps,
                    "expected_behavior": entry.expected_behavior,
                    "actual_behavior": entry.actual_behavior,
                    "timestamp": entry.timestamp,
                    "agent_id": entry.agent_id
                }
                for entry in self.feedback_history
            ]
        }
        
        with open(history_file, 'w') as f:
            json.dump(history_data, f, indent=2)

    def _backup_corrupted_file(self, corrupted_file: Path, error: Exception) -> None:
        """
        Creates a timestamped backup of a corrupted feedback file for manual inspection.
        
        If an error occurs during backup, prints a warning message with details.
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"feedback_history_corrupted_{timestamp}.json"
            backup_path = corrupted_file.parent / backup_name

            # Copy corrupted file to backup location
            shutil.copy2(corrupted_file, backup_path)

            print(f"📁 Corrupted feedback file backed up to: {backup_path}")
            print(f"🔍 Error details: {error}")
            print("💡 You can inspect the backup file to recover data manually")

        except Exception as backup_error:
            print(f"⚠️ Failed to backup corrupted file: {backup_error}")
    
    def collect_feedback(
        self,
        feedback_type: str,
        feedback_content: str,
        suggestions: Optional[List[str]] = None,
        severity: str = "medium",
        component: str = "general",
        reproduction_steps: Optional[List[str]] = None,
        expected_behavior: Optional[str] = None,
        actual_behavior: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> FeedbackEntry:
        """
        Creates and stores a structured feedback entry with validation.
        
        Validates the severity level, constructs a FeedbackEntry with the provided details and current timestamp, appends it to the feedback history, persists the updated history, and returns the created entry.
        
        Args:
            feedback_type: The category of feedback, such as 'bug', 'enhancement', or 'workflow_issue'.
            feedback_content: The main content or description of the feedback.
            suggestions: Optional list of suggestions for improvement.
            severity: The severity level of the feedback; must be one of 'low', 'medium', 'high', or 'critical'.
            component: The affected component or area.
            reproduction_steps: Optional steps to reproduce the issue, relevant for bug reports.
            expected_behavior: Optional description of the expected behavior, relevant for bug reports.
            actual_behavior: Optional description of the actual behavior, relevant for bug reports.
            agent_id: Optional identifier for the agent submitting the feedback.
        
        Returns:
            The created FeedbackEntry instance.
        
        Raises:
            ValueError: If the provided severity is not one of the allowed levels.
        """
        # Validate severity
        if severity not in ALLOWED_SEVERITIES:
            raise ValueError(f"Invalid severity '{severity}'. Must be one of: {', '.join(sorted(ALLOWED_SEVERITIES))}")

        entry = FeedbackEntry(
            feedback_type=feedback_type,
            feedback_content=feedback_content,
            suggestions=suggestions or [],
            severity=severity,
            component=component,
            reproduction_steps=reproduction_steps or [],
            expected_behavior=expected_behavior,
            actual_behavior=actual_behavior,
            timestamp=datetime.datetime.now().isoformat(),
            agent_id=agent_id
        )
        
        self.feedback_history.append(entry)
        self._save_feedback_history()
        
        return entry
    
    def generate_meta_feedback(
        self,
        feedback_type: str,
        feedback_content: str,
        suggestions: Optional[List[str]] = None,
        severity: str = "medium",
        component: str = "general"
    ) -> str:
        """
        Generates formatted meta feedback content for AGOR platform improvement.
        
        Collects and stores structured feedback, then produces a markdown-formatted summary including feedback type, content, suggestions, severity, component, and action items.
        Returns the formatted meta feedback as a string.
        """
        # Collect the feedback
        entry = self.collect_feedback(
            feedback_type=feedback_type,
            feedback_content=feedback_content,
            suggestions=suggestions,
            severity=severity,
            component=component
        )
        
        # Generate formatted feedback using template
        context = {
            'feedback_type': feedback_type,
            'feedback_content': feedback_content,
            'suggestions': suggestions or [],
            'severity': severity,
            'component': component,
            'timestamp': entry.timestamp
        }
        
        template = """# 🔄 AGOR Meta Feedback

**Type**: {{ feedback_type.replace('_', ' ').title() }}
**Component**: {{ component }}
**Severity**: {{ severity }}
**Generated**: {{ timestamp }}

## 📝 Feedback Content

{{ feedback_content }}

{% if suggestions -%}
## 💡 Suggested Improvements

{{ suggestions | format_list }}
{% endif %}

## 🎯 Action Items

- [ ] Review feedback content and assess impact
- [ ] Prioritize based on severity: {{ severity }}
- [ ] Consider implementation of suggested improvements
- [ ] Update documentation if needed
- [ ] Test proposed solutions

## 📊 Feedback Context

This feedback was generated during AGOR usage to help improve the platform.
Component: {{ component }}
Priority: {{ severity }}

---

*This feedback helps make AGOR better for all users. Thank you for contributing to the improvement process!*"""
        
        return self.template_engine.render_string(template, context)
    
    def create_github_issue_content(self, config: GitHubIssueConfig) -> str:
        """
        Generates formatted GitHub issue content from a feedback configuration.
        
        The output includes a structured issue body with title, component, severity, description, reproduction steps, expected and actual behavior (for bugs), suggested solutions, and appropriate GitHub labels based on feedback type and severity.
        
        Args:
            config: Structured configuration containing feedback details for the issue.
        
        Returns:
            A string containing the formatted GitHub issue content.
        """
        # Map feedback types to GitHub labels
        type_labels = {
            "bug": "bug",
            "enhancement": "enhancement",
            "workflow_issue": "workflow",
            "success_story": "feedback",
            "documentation": "documentation",
            "performance": "performance",
            "usability": "UX"
        }
        
        severity_labels = {
            "low": "priority: low",
            "medium": "priority: medium",
            "high": "priority: high",
            "critical": "priority: critical"
        }
        
        context = {
            'title': config.feedback_type.replace('_', ' ').title(),
            'component': config.component,
            'severity': config.severity,
            'feedback_content': config.feedback_content,
            'feedback_type': config.feedback_type,
            'reproduction_steps': config.reproduction_steps,
            'expected_behavior': config.expected_behavior,
            'actual_behavior': config.actual_behavior,
            'suggestions': config.suggestions,
            'type_label': type_labels.get(config.feedback_type, "feedback"),
            'severity_label': severity_labels.get(config.severity, "priority: medium")
        }
        
        template = """## {{ title }}

**Component**: {{ component }}
**Severity**: {{ severity }}

### Description

{{ feedback_content }}

{% if feedback_type == "bug" -%}
{% if reproduction_steps -%}

### Reproduction Steps

{{ reproduction_steps | format_list }}
{% endif %}

{% if expected_behavior -%}

### Expected Behavior

{{ expected_behavior }}
{% endif %}

{% if actual_behavior -%}

### Actual Behavior

{{ actual_behavior }}
{% endif %}
{% endif %}

{% if suggestions -%}

### Suggested Solutions

{{ suggestions | format_list }}
{% endif %}

### Labels

{{ type_label }}, {{ severity_label }}{% if component != "general" %}, component: {{ component }}{% endif %}

---

*This issue was generated from AGOR meta feedback system*"""
        
        return self.template_engine.render_string(template, context)
    
    def get_feedback_statistics(self) -> Dict[str, Any]:
        """
        Returns aggregated statistics about all collected feedback.
        
        The statistics include the total number of feedback entries, counts grouped by type, severity, and component, as well as summaries of the five most recent feedback entries.
         
        Returns:
            A dictionary containing feedback statistics with keys: 'total_feedback', 'by_type', 'by_severity', 'by_component', and 'recent_feedback'.
        """
        if not self.feedback_history:
            return {
                "total_feedback": 0,
                "by_type": {},
                "by_severity": {},
                "by_component": {},
                "recent_feedback": []
            }
        
        # Count by type
        by_type = {}
        for entry in self.feedback_history:
            by_type[entry.feedback_type] = by_type.get(entry.feedback_type, 0) + 1
        
        # Count by severity
        by_severity = {}
        for entry in self.feedback_history:
            by_severity[entry.severity] = by_severity.get(entry.severity, 0) + 1
        
        # Count by component
        by_component = {}
        for entry in self.feedback_history:
            by_component[entry.component] = by_component.get(entry.component, 0) + 1
        
        # Get recent feedback (last 5)
        recent_feedback = [
            {
                "type": entry.feedback_type,
                "content": entry.feedback_content[:100] + "..." if len(entry.feedback_content) > 100 else entry.feedback_content,
                "severity": entry.severity,
                "timestamp": entry.timestamp
            }
            for entry in self.feedback_history[-5:]
        ]
        
        return {
            "total_feedback": len(self.feedback_history),
            "by_type": by_type,
            "by_severity": by_severity,
            "by_component": by_component,
            "recent_feedback": recent_feedback
        }
    
    def export_feedback(self, format_type: str = "json") -> str:
        """
        Exports all collected feedback entries in the specified format.
        
        Args:
            format_type: The export format, either "json" or "markdown".
        
        Returns:
            A string containing the exported feedback data in the chosen format.
        
        Raises:
            ValueError: If an unsupported export format is specified.
        """
        if format_type == "json":
            return json.dumps({
                "feedback": [
                    {
                        "feedback_type": entry.feedback_type,
                        "feedback_content": entry.feedback_content,
                        "suggestions": entry.suggestions,
                        "severity": entry.severity,
                        "component": entry.component,
                        "timestamp": entry.timestamp
                    }
                    for entry in self.feedback_history
                ]
            }, indent=2)

        if format_type == "markdown":
            lines = ["# AGOR Feedback Export\n"]
            for entry in self.feedback_history:
                lines.append(f"## {entry.feedback_type.replace('_', ' ').title()}")
                lines.append(f"**Severity**: {entry.severity}")
                lines.append(f"**Component**: {entry.component}")
                lines.append(f"**Timestamp**: {entry.timestamp}")
                lines.append(f"\n{entry.feedback_content}\n")
                if entry.suggestions:
                    lines.append("**Suggestions**:")
                    for suggestion in entry.suggestions:
                        lines.append(f"- {suggestion}")
                lines.append("\n---\n")
            return "\n".join(lines)

        raise ValueError(f"Unsupported export format: {format_type}")


# Global feedback manager instance
_feedback_manager = FeedbackManager()


# Convenience functions for backward compatibility
def generate_meta_feedback(feedback_type: str, feedback_content: str, **kwargs) -> str:
    """
    Generates formatted meta feedback content using the global feedback manager.
    
    Args:
        feedback_type: The category of feedback (e.g., bug, suggestion, question).
        feedback_content: The main feedback text.
    
    Returns:
        A formatted string containing the meta feedback, including details such as type, component, severity, timestamp, suggestions, and context.
    """
    return _feedback_manager.generate_meta_feedback(feedback_type, feedback_content, **kwargs)


def create_github_issue_content(config: GitHubIssueConfig) -> str:
    """
    Generates formatted GitHub issue content from a feedback configuration.
    
    Args:
        config: Structured feedback data for issue creation.
    
    Returns:
        A string containing the GitHub issue body with mapped labels and formatted sections.
    """
    return _feedback_manager.create_github_issue_content(config)


def get_feedback_statistics() -> Dict[str, Any]:
    """
    Returns aggregated statistics about collected feedback entries.
    
    The statistics include total feedback count, counts by type, severity, and component, as well as summaries of the most recent feedback entries.
    """
    return _feedback_manager.get_feedback_statistics()


def collect_feedback(feedback_type: str, feedback_content: str, **kwargs) -> FeedbackEntry:
    """
    Collects structured feedback and returns a FeedbackEntry.
    
    Delegates to the global feedback manager to validate, store, and persist the feedback entry with the provided type, content, and optional metadata.
    """
    return _feedback_manager.collect_feedback(feedback_type, feedback_content, **kwargs)
