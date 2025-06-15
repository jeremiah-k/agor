# 🤖 Agent Prompt Examples

This guide shows you exactly how to ask agents to use AGOR tools. **Emphasis is critical** - agents need clear direction to use AGOR tools instead of trying their own approaches.

## 🎯 Key Principles

1. **Be explicit about using AGOR tools**
2. **Use action words**: "Use", "Create", "Generate", "Run"
3. **Specify the exact tool function when possible**
4. **Don't assume agents will automatically use AGOR tools**

## 📸 Snapshots & Memory Management

### ✅ Good Examples

**End of work session:**
> "**Use AGOR's snapshot tools** to create a development snapshot of our progress, then **generate a handoff prompt** so another agent can continue this work."

**Before major changes:**
> "Before we refactor this code, **use `create_development_snapshot()`** to save our current state with the title 'Pre-refactor baseline'."

**Regular progress saving:**
> "**Create an AGOR snapshot** of our current progress and **commit it to your memory branch** so we don't lose this work."

### ❌ Avoid These

> "Save our progress" *(too vague - agent might use its own methods)*
> "Create a backup" *(agent won't use AGOR tools)*
> "Document what we've done" *(agent will write text, not use snapshots)*

## 🚀 Git Operations & Release Management

### ✅ Good Examples

**Committing work:**
> "**Use AGOR's `quick_commit_and_push()`** to commit our changes with a proper message about the authentication feature we just built."

**Creating release notes:**
> "**Use the AGOR dev tools to generate release notes** for this update. Include the bug fixes and new features we implemented."

**PR descriptions:**
> "**Use `generate_pr_description_output()`** to create a properly formatted PR description for this branch."

### ❌ Avoid These

> "Commit our changes" *(agent might use basic git)*
> "Write release notes" *(agent will write manually)*
> "Create a PR description" *(agent won't use AGOR formatting)*

## 🔄 Agent Coordination & Handoffs

### ✅ Good Examples

**Creating handoffs:**
> "**Use AGOR's handoff tools** to create a comprehensive snapshot and **generate a session end prompt** for the next agent."

**Loading previous work:**
> "**Use AGOR's snapshot loading tools** to understand what the previous agent accomplished and what needs to be done next."

**Multi-agent coordination:**
> "**Update the agentconvo.md file using AGOR protocols** to let other agents know we're working on the backend API."

### ❌ Avoid These

> "Hand this off to another agent" *(too vague)*
> "Check what was done before" *(agent won't use AGOR tools)*
> "Coordinate with other agents" *(agent will improvise)*

## 🛠️ Development Workflow

### ✅ Good Examples

**Starting work:**
> "**Use AGOR tools to initialize** this project workspace and **create your agent memory branch** before we begin coding."

**Testing and validation:**
> "After running the tests, **use AGOR's commit tools** to save our changes and **create a snapshot** titled 'Tests passing - ready for review'."

**Code review preparation:**
> "**Use AGOR's PR generation tools** to create a comprehensive PR description that explains our implementation approach and testing strategy."

### ❌ Avoid These

> "Set up the workspace" *(agent won't use AGOR initialization)*
> "Save our work" *(too vague)*
> "Prepare for code review" *(agent will improvise)*

## 🎯 Specific Tool Usage

### Memory & Snapshots
- `create_development_snapshot(title, context)`
- `generate_session_end_prompt()`
- `create_agent_memory_branch()`

### Git & Release Management
- `quick_commit_and_push(message)`
- `generate_pr_description_output()`
- `generate_release_notes_output()`

### Agent Coordination
- Update `.agor/agentconvo.md` with agent ID
- Use agent-specific memory branches
- Reference snapshots in handoffs

## 💡 Pro Tips

1. **Always specify "AGOR tools"** in your requests
2. **Use function names** when you know them
3. **Be explicit about outputs** you want (snapshots, PR descriptions, etc.)
4. **Emphasize using existing tools** rather than creating new approaches
5. **Reference the agent's memory branch** for continuity

## 🚫 Common Mistakes

- Asking agents to "figure out the best way" *(they'll avoid AGOR tools)*
- Using vague language like "save" or "document" *(not specific enough)*
- Assuming agents know to use AGOR tools *(they need explicit direction)*
- Not specifying output format *(agents will use their own formatting)*

Remember: **Agents need clear, explicit instructions to use AGOR tools effectively!**
