"""
AGOR Checklist and Workflow Validation Module

This module provides checklist generation, workflow validation, and progress tracking
utilities for AGOR development workflows.

All functions use absolute imports for better reliability.
"""

from typing import Dict, List

# Use absolute imports to prevent E0402 errors
from agor.tools.git_operations import get_current_timestamp, run_git_command


def generate_development_checklist(task_type: str = "general") -> str:
    """
    Generates a formatted development checklist tailored to the specified task type.
    
    The checklist includes sections for pre-development, development process, testing and validation, documentation, and completion. Additional task-specific checklist items are appended for 'feature', 'bugfix', or 'refactor' tasks. The checklist is timestamped and formatted as a markdown string.
    
    Args:
        task_type: The type of development task. Supported values are 'general', 'feature', 'bugfix', and 'refactor'.
    
    Returns:
        A markdown-formatted checklist string for the specified development task type.
    """
    timestamp = get_current_timestamp()

    base_checklist = f"""# 📋 Development Checklist - {task_type.title()}

**Generated**: {timestamp}
**Task Type**: {task_type}

## 🚀 Pre-Development
- [ ] Read AGOR documentation and select appropriate role
- [ ] Understand task requirements and scope
- [ ] Check current branch and git status
- [ ] Ensure workspace is clean and ready

## 🔧 Development Process
- [ ] Create feature branch if needed
- [ ] Implement changes following best practices
- [ ] Write or update tests as needed
- [ ] Document changes and decisions
- [ ] Commit frequently with descriptive messages

## 🧪 Testing & Validation
- [ ] Run existing tests to ensure no regressions
- [ ] Test new functionality thoroughly
- [ ] Validate changes meet requirements
- [ ] Check for edge cases and error handling

## 📝 Documentation
- [ ] Update relevant documentation
- [ ] Add code comments where needed
- [ ] Update README if applicable
- [ ] Document any breaking changes

## 🔄 Completion
- [ ] Final commit with comprehensive message
- [ ] Push changes to remote repository
- [ ] Create snapshot for handoff/continuation
- [ ] Update project status and coordination files
"""

    # Add task-specific items
    if task_type == "feature":
        base_checklist += """
## 🆕 Feature-Specific
- [ ] Feature meets acceptance criteria
- [ ] Integration with existing features tested
- [ ] Performance impact assessed
- [ ] User experience considerations addressed
"""
    elif task_type == "bugfix":
        base_checklist += """
## 🐛 Bugfix-Specific
- [ ] Root cause identified and documented
- [ ] Fix addresses the core issue
- [ ] Regression tests added
- [ ] Similar issues checked and addressed
"""
    elif task_type == "refactor":
        base_checklist += """
## 🔄 Refactor-Specific
- [ ] Functionality preserved (no behavior changes)
- [ ] Code quality and maintainability improved
- [ ] Performance impact assessed
- [ ] All tests still pass
"""

    return base_checklist


def generate_handoff_checklist() -> str:
    """
    Generates a formatted checklist for agent handoff procedures.
    
    The checklist covers snapshot creation, memory management, handoff preparation, technical and documentation handoff, and final verification, with a generation timestamp included.
    """
    timestamp = get_current_timestamp()

    return f"""# 🤖 Agent Handoff Checklist

**Generated**: {timestamp}

## 📸 Snapshot Creation
- [ ] Create comprehensive development snapshot
- [ ] Include all work completed and context
- [ ] Document current status and next steps
- [ ] List all modified files and changes

## 🔄 Memory Management
- [ ] Commit snapshot to memory branch
- [ ] Update coordination files
- [ ] Ensure memory branch is accessible
- [ ] Verify memory sync is working

## 📋 Handoff Preparation
- [ ] Generate handoff prompt with environment details
- [ ] Include setup instructions for next agent
- [ ] Provide clear task description
- [ ] Add brief context for quick orientation

## 🔧 Technical Handoff
- [ ] Ensure all changes are committed
- [ ] Push changes to remote repository
- [ ] Verify branch status and cleanliness
- [ ] Test that environment is reproducible

## 📝 Documentation Handoff
- [ ] Update project documentation
- [ ] Document any decisions made
- [ ] Note any blockers or issues
- [ ] Provide continuation guidance

## ✅ Final Verification
- [ ] Handoff prompt is complete and formatted
- [ ] All necessary context is included
- [ ] Next agent can pick up seamlessly
- [ ] Emergency contact information provided if needed
"""


def validate_workflow_completion(checklist_items: List[str]) -> Dict[str, any]:
    """
    Analyzes a checklist to determine workflow completion status.
    
    Counts completed items based on checklist markers, calculates completion percentage, identifies missing items, and assigns an overall status category. Returns a dictionary with timestamp, totals, completion metrics, missing items, and status.
    """
    validation = {
        "timestamp": get_current_timestamp(),
        "total_items": len(checklist_items),
        "completed_items": 0,
        "completion_percentage": 0,
        "missing_items": [],
        "status": "incomplete",
    }

    # Simple validation - in practice, this would check actual conditions
    # For now, we'll assume items marked with [x] are completed
    for item in checklist_items:
        if "[x]" in item.lower() or "[✓]" in item:
            validation["completed_items"] += 1
        else:
            validation["missing_items"].append(item.strip())

    if validation["total_items"] > 0:
        validation["completion_percentage"] = (
            validation["completed_items"] / validation["total_items"]
        ) * 100

    # Determine status
    if validation["completion_percentage"] == 100:
        validation["status"] = "complete"
    elif validation["completion_percentage"] >= 80:
        validation["status"] = "mostly_complete"
    elif validation["completion_percentage"] >= 50:
        validation["status"] = "in_progress"
    else:
        validation["status"] = "incomplete"

    return validation


def generate_progress_report(validation_results: Dict[str, any]) -> str:
    """
    Generates a formatted markdown progress report based on workflow validation results.
    
    Args:
        validation_results: A dictionary containing workflow completion data, typically produced by `validate_workflow_completion`.
    
    Returns:
        A markdown-formatted string summarizing workflow status, completion metrics, remaining checklist items, and a concluding message.
    """
    results = validation_results
    status_emoji = {
        "complete": "✅",
        "mostly_complete": "🟡",
        "in_progress": "🔄",
        "incomplete": "❌",
    }

    report = f"""# 📊 Workflow Progress Report

**Generated**: {results['timestamp']}
**Status**: {status_emoji.get(results['status'], '❓')} {results['status'].replace('_', ' ').title()}

## 📈 Completion Summary
- **Total Items**: {results['total_items']}
- **Completed**: {results['completed_items']}
- **Completion Rate**: {results['completion_percentage']:.1f}%

"""

    if results["missing_items"]:
        report += "## 📋 Remaining Items\n"
        for item in results["missing_items"]:
            report += f"- {item}\n"

    if results["status"] == "complete":
        report += (
            "\n## 🎉 Workflow Complete!\nAll checklist items have been completed.\n"
        )
    elif results["status"] == "mostly_complete":
        report += (
            "\n## 🎯 Nearly Complete\nMost items completed, review remaining items.\n"
        )
    else:
        report += "\n## 🔄 Continue Working\nSignificant work remains to complete the workflow.\n"

    return report


def check_git_workflow_status() -> Dict[str, any]:
    """
    Checks the current git workflow status and identifies potential issues.
    
    Returns:
        A dictionary containing the timestamp, branch safety, commit and push status, current branch name, number of commits ahead of remote, detected issues, and recommendations for maintaining a clean git workflow.
    """
    status = {
        "timestamp": get_current_timestamp(),
        "branch_safe": False,
        "changes_committed": False,
        "pushed_to_remote": False,
        "issues": [],
        "recommendations": [],
    }

    # Check current branch
    success_branch, current_branch_val = run_git_command(["branch", "--show-current"])
    if success_branch:
        current_branch = current_branch_val.strip()
        # Consider main/master as potentially unsafe for direct work
        unsafe_branches = ["main", "master", "production", "prod"]
        status["branch_safe"] = current_branch not in unsafe_branches
        status["current_branch"] = current_branch

        if not status["branch_safe"]:
            status["issues"].append(
                f"Working on potentially unsafe branch: {current_branch}"
            )
            status["recommendations"].append("Consider creating a feature branch")
    else:
        status["issues"].append("Could not determine current branch")

    # Check for uncommitted changes
    success_status, git_status_val = run_git_command(["status", "--porcelain"])
    if success_status:
        has_changes = bool(git_status_val.strip())
        status["changes_committed"] = not has_changes

        if has_changes:
            status["issues"].append("Uncommitted changes detected")
            status["recommendations"].append("Commit changes before proceeding")
    else:
        status["issues"].append("Could not check git status")

    # Check if local branch is ahead of remote
    if success_branch:
        success_ahead, ahead_output = run_git_command(
            ["rev-list", "--count", f"origin/{current_branch}..HEAD"]
        )
        if success_ahead:
            ahead_count = (
                int(ahead_output.strip()) if ahead_output.strip().isdigit() else 0
            )
            status["commits_ahead"] = ahead_count
            status["pushed_to_remote"] = ahead_count == 0

            if ahead_count > 0:
                status["issues"].append(f"{ahead_count} commits ahead of remote")
                status["recommendations"].append("Push commits to remote repository")
        else:
            # Might be a new branch without remote tracking
            status["recommendations"].append("Verify remote tracking is set up")

    return status


def generate_git_workflow_report() -> str:
    """
    Generates a formatted markdown report summarizing the current git workflow status.
    
    The report includes branch safety, commit and push status, number of commits ahead, detected issues, and recommendations. If no issues are found, it indicates a clean git workflow.
    """
    status = check_git_workflow_status()

    report = f"""# 🔄 Git Workflow Status

**Generated**: {status['timestamp']}
**Current Branch**: {status.get('current_branch', 'unknown')}

## ✅ Status Checks
- **Branch Safety**: {'✅ Safe' if status['branch_safe'] else '⚠️ Potentially unsafe'}
- **Changes Committed**: {'✅ Clean' if status['changes_committed'] else '❌ Uncommitted changes'}
- **Pushed to Remote**: {'✅ Synced' if status['pushed_to_remote'] else '⚠️ Local commits ahead'}

"""

    if status.get("commits_ahead", 0) > 0:
        report += f"**Commits Ahead**: {status['commits_ahead']}\n\n"

    if status["issues"]:
        report += "## 🚨 Issues\n"
        for issue in status["issues"]:
            report += f"- {issue}\n"
        report += "\n"

    if status["recommendations"]:
        report += "## 💡 Recommendations\n"
        for rec in status["recommendations"]:
            report += f"- {rec}\n"
        report += "\n"

    if not status["issues"]:
        report += "## 🎉 Git Workflow Clean\nNo issues detected with git workflow.\n"

    return report
