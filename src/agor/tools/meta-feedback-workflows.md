# 🔄 AGOR Meta Feedback System Workflows

**Version**: 0.6.0
**Last Updated**: 2025-06-09
**Purpose**: Guide agents through effective meta feedback workflows for continuous AGOR improvement

## 🎯 Overview

The enhanced AGOR Meta Feedback System enables agents to provide structured, actionable feedback about AGOR functionality, workflows, and user experience. This system transforms feedback from ad-hoc comments into systematic improvement data.

## 📊 Feedback Categories

### 🐛 Bug Reports

**When to use**: System errors, unexpected behavior, functionality failures
**Severity levels**: Low → Medium → High → Critical
**Required info**: Reproduction steps, expected vs actual behavior

### ✨ Enhancement Requests

**When to use**: Feature suggestions, workflow improvements, capability additions
**Focus areas**: User experience, agent coordination, development efficiency

### ⚠️ Workflow Issues

**When to use**: Process friction, coordination problems, unclear procedures
**Impact**: Agent productivity, collaboration effectiveness

### 🎉 Success Stories

**When to use**: Workflows that work well, positive experiences, effective features
**Value**: Reinforces good design decisions, guides future development

### 📚 Documentation Feedback

**When to use**: Unclear instructions, missing information, outdated content
**Scope**: All AGOR documentation, guides, and help content

### ⚡ Performance Issues

**When to use**: Slow operations, resource consumption, efficiency concerns
**Metrics**: Response times, memory usage, processing delays

## 🛠️ Quick Start Workflows

### Scenario 1: Providing Feedback (Recommended Method)

Use the `provide_agor_feedback` function from `dev_tools`. This function handles both generation and formatting of the feedback report.

```python
from agor.tools.dev_tools import provide_agor_feedback # Recommended

# Example: Reporting a bug
bug_report_formatted = provide_agor_feedback(
    feedback_type="bug",
    feedback_content="Memory branch creation fails when repository has no initial commits.",
    suggestions=["Ensure git init is called and an initial commit exists before memory operations."],
    severity="high",
    component="memory_system"
    # For more detailed bug reports, you might prepare the content string for feedback_content
    # by including reproduction_steps, expected_behavior, actual_behavior details within it.
    # The underlying feedback_manager.generate_meta_feedback currently doesn't take these as separate params.
)
print(bug_report_formatted)

# Example: Suggesting an enhancement
enhancement_report_formatted = provide_agor_feedback(
    feedback_type="enhancement",
    feedback_content="Add auto-completion for development tool function names and parameters.",
    suggestions=[
        "Integrate with common shell completion frameworks.",
        "Provide a command to generate completion scripts."
    ],
    severity="medium",
    component="dev_tools"
)
print(enhancement_report_formatted)

# The provide_agor_feedback function (from dev_tools) uses feedback_manager internally and ensures:
# - Feedback is structured and collected.
# - Report is generated with GitHub issue link and suggested labels.
# - Output is deticked and wrapped in a code block for easy copy-pasting.
```

### Scenario 2: Direct Usage of Feedback Manager (Advanced)

If you need more direct control or are working outside the context where `dev_tools` is easily accessible, you can use `feedback_manager` directly. You would then be responsible for formatting the output for display.

```python
from agor.tools.feedback_manager import generate_meta_feedback
from agor.tools.dev_tools import generate_formatted_output # For formatting the output

# Example: Workflow Issue
detailed_feedback_raw = generate_meta_feedback(
    feedback_type="workflow_issue",
    feedback_content="Agent handoff process requires too many manual steps, especially concerning environment variable propagation and context capture. For instance, ensuring the PYTHONPATH is correctly set for subsequent agents or tools can be error-prone.",
    suggestions=[
        "Automate environment variable capture and restoration during handoff.",
        "Provide a dev tool to explicitly set/propagate critical env vars for AGOR.",
        "Enhance snapshot capabilities to include more environment details by default."
    ],
    severity="high",
    component="agent_handoffs"
    # Note: reproduction_steps, expected_behavior, actual_behavior are not direct params
    # of feedback_manager.generate_meta_feedback. They would need to be part of the
    # feedback_content string or collected differently if feedback_manager is used this way.
)

formatted_detailed_feedback = generate_formatted_output(detailed_feedback_raw, "meta_feedback")
print(formatted_detailed_feedback)
```

## 🏥 System Health Monitoring

### Regular Health Checks

```python
from agor.tools.dev_tools import system_health_check

# Comprehensive system status
health_report = system_health_check()

# Provides:
# - Git and workspace status
# - Environment validation
# - Dev tooling functionality
# - Memory system accessibility
# - Component-by-component analysis
# - Actionable recommendations
```

### Health Check Integration

Agents should run health checks:

- **At session start**: Verify system readiness
- **Before major operations**: Ensure stable environment
- **After errors**: Diagnose system state
- **During handoffs**: Validate environment for next agent

## 📈 Feedback Quality Guidelines

### Effective Bug Reports

✅ **Good Example**:

```
Component: memory_system
Severity: high
Description: Memory branch creation fails with "fatal: bad object" error when repository has no commits

Reproduction Steps:
1. Create new git repository with `git init`
2. Attempt to create memory branch using commit_to_memory_branch()
3. Observe failure with git error

Expected: Memory branch created successfully
Actual: Function fails with git tree error
```

❌ **Poor Example**:

```
Memory stuff doesn't work
```

### Effective Enhancement Requests

✅ **Good Example**:

```
Component: dev_tools
Severity: medium
Description: Add input validation and auto-completion for development tools

Benefits:
- Reduces agent errors from typos
- Improves development efficiency
- Provides better user experience
- Enables faster onboarding

Implementation Ideas:
- Add command validation before execution
- Provide suggestion lists for common commands
- Include help text for command parameters
```

## 🔗 Integration Workflows

### GitHub Issue Creation

The meta feedback system can generate GitHub-ready issue content. This is typically for more direct integration if an agent were to programmatically prepare content for a GitHub issue.

```python
from agor.tools.feedback_manager import create_github_issue_content, GitHubIssueConfig # Ensure GitHubIssueConfig is imported

# Create a configuration object for the feedback
issue_config = GitHubIssueConfig(
    feedback_type="enhancement",
    feedback_content="Improve agent coordination with real-time status updates.",
    suggestions=["Add WebSocket support for real-time updates.", "Create a shared status dashboard viewable by all agents."],
    severity="medium",
    component="coordination_module"
    # For bugs, you would also include:
    # reproduction_steps=["step 1", "step 2"],
    # expected_behavior="This should happen.",
    # actual_behavior="This actually happened."
)

# Generate the content for the GitHub issue body
github_issue_body_text = create_github_issue_content(config=issue_config)

print("### GitHub Issue Body Preview ###")
print(github_issue_body_text)

# The output of create_github_issue_content includes:
# - Proper GitHub formatting
# - Suggested labels
# - Component categorization
# - Severity indicators
```

### Memory Branch Integration

All feedback is automatically stored in memory branches for:

- **Persistence**: Feedback survives session changes
- **Coordination**: Multiple agents can access feedback history
- **Analysis**: Patterns and trends can be identified
- **Continuity**: Feedback context preserved across handoffs

## 🎯 Best Practices

### For Agents

1. **Be Specific**: Include exact error messages, steps, and context
2. **Use Categories**: Select appropriate feedback type and component
3. **Provide Context**: Include environment details and use cases
4. **Suggest Solutions**: When possible, include improvement ideas
5. **Follow Up**: Check if feedback was addressed in future sessions

### For Development Teams

1. **Regular Review**: Process feedback systematically
2. **Prioritization**: Use severity and component data for planning
3. **Response Loop**: Acknowledge and act on feedback
4. **Pattern Analysis**: Look for recurring issues and themes
5. **Documentation**: Update guides based on feedback insights

## 🔄 Continuous Improvement

The meta feedback system itself evolves based on usage:

- **Validation Rules**: Improved based on common input errors
- **Categories**: Refined based on actual feedback patterns
- **Templates**: Enhanced based on successful feedback examples
- **Integration**: Extended based on workflow needs

## 📞 Support and Resources

- **Documentation**: [AGOR Development Guide](agor-development-guide.md)
- **Templates**: [Agent Feedback Template](../.github/ISSUE_TEMPLATE/agent-feedback.md)
- **Coordination**: [Multi-Agent Protocols](multi-agent-protocols.md)
- **Development**: [Development Log](agor-development-log.md)

---

**The meta feedback system transforms AGOR from a static tool into a continuously evolving, self-improving platform that adapts to agent needs and workflows.**
