# AGOR Meta-Development Feedback

## Purpose

This file captures feedback, suggestions, and improvements for AGOR itself from AI agents using the platform. Since you're development agents, your insights help AGOR evolve and improve for future users.

## How to Use This File

- **Add your feedback** when you encounter rough spots, have suggestions, or discover exceptional workflows
- **Be specific and technical** - you're development agents, so detailed feedback is valuable
- **Include context** about your role, project type, and what you were trying to accomplish
- **Suggest concrete improvements** with implementation ideas when possible

---

## Feedback Template

```markdown
### [Date] - [Agent Role] - [Project Type]

**Issue/Suggestion**: Brief description

**Context**: What were you trying to do? What role were you in?

**Details**: Specific technical details, error messages, workflow issues

**Suggested Improvement**: Concrete suggestions for fixing or enhancing

**Impact**: How would this improvement help future agents?

---
```

## Current Feedback Log

### Example Entry - 2025-05-25 - ANALYST/SOLO DEV - Python Web App

**Issue/Suggestion**: Git binary path instructions could be clearer

**Context**: Working in Bundle Mode, trying to analyze a Flask application codebase

**Details**: Initially tried to use `git` instead of `/tmp/agor_tools/git` despite instructions. The warnings helped but could be more prominent.

**Suggested Improvement**: Add a shell alias setup in initialization: `alias git='/tmp/agor_tools/git'`

**Impact**: Would prevent path confusion and make git commands more natural for agents

---

## Categories for Feedback

### 🐛 **Bug Reports**

- Import errors, path issues, broken functionality
- Specific error messages and reproduction steps

### 💡 **Feature Suggestions**

- New hotkeys, workflow improvements, tool enhancements
- Integration ideas, coordination improvements

### 📚 **Documentation Issues**

- Unclear instructions, missing examples, confusing workflows
- Role-specific documentation gaps

### ⚡ **Performance & Efficiency**

- Slow operations, redundant steps, workflow bottlenecks
- Optimization opportunities

### 🎯 **Workflow Improvements**

- Better coordination patterns, handoff procedures
- Multi-agent collaboration enhancements

### 🏆 **Success Stories**

- Workflows that worked exceptionally well
- Patterns that should be promoted or standardized

---

## Meta-Development Guidelines

### For AI Agents Providing Feedback

1. **Be Constructive**: Focus on specific, actionable improvements
2. **Include Context**: Role, project type, what you were trying to achieve
3. **Think Systematically**: How would this help the broader AGOR ecosystem?
4. **Consider Implementation**: Suggest concrete technical approaches when possible
5. **Document Workarounds**: If you found a way around an issue, share it

### For AGOR Maintainers

1. **Review Regularly**: Agent feedback is valuable for prioritizing improvements
2. **Implement High-Impact Changes**: Focus on issues that affect multiple agents/workflows
3. **Update Documentation**: Address common confusion points
4. **Evolve Hotkeys**: Add frequently requested shortcuts
5. **Enhance Role Support**: Improve role-specific workflows based on feedback

---

## Quick Feedback Hotkey: `meta`

Use the `meta` hotkey to provide feedback through multiple pathways based on your situation:

### **Option 1: Working on Different Project (GitHub Issue)**

If you're using AGOR for another project and encounter issues:

- Creates structured GitHub issue with technical details
- Uses issue template for consistent reporting
- Allows maintainers to prioritize and implement

### **Option 2: Working on AGOR Itself (Direct Implementation)**

If you're using AGOR to improve AGOR:

- Edit files directly and commit improvements
- Create PR with your enhancements
- Full development workflow within AGOR

### **Option 3: Quick Contribution (Copy-Paste Code)**

If you have specific improvements but limited time:

- Generate exact code changes in copy-paste format
- Provide file paths and complete replacement content
- Enable manual implementation by maintainers

### **Option 4: Local Feedback Log (This File)**

For ongoing documentation and pattern recognition:

- Add entries to this file for future reference
- Build knowledge base of common issues and solutions
- Track successful patterns and workflows

The system will detect your context and guide you to the most appropriate feedback method!
