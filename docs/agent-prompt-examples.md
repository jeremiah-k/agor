# 🤖 Agent Prompt Examples

This guide shows you exactly how to ask agents to use AGOR tools. **Emphasis is critical** - agents need clear direction to use AGOR tools instead of trying their own approaches.

## 🎯 Key Principles

1. **Be explicit about using AGOR tools**
2. **Use action words**: "Use", "Create", "Generate", "Run"
3. **Specify the exact tool function when possible**
4. **Always request single codeblock output** for easy copy-paste
5. **Don't assume agents will automatically use AGOR tools**
6. **For multi-agent work**: Tell the next agent what AGOR actions to take

## 📸 Snapshots & Memory Management

### ✅ Good Examples

**End of work session:**
```
Use AGOR's snapshot tools to create a development snapshot of our progress, then generate a handoff prompt so another agent can continue this work. Wrap the output in a single codeblock so I can copy and paste easily for a clean transition. Be verbose in your explanation of your work.
```

**Before major changes:**
```
Before we refactor this code, use `create_development_snapshot()` to save our current state with the title 'Pre-refactor baseline'. Use AGOR dev tools to format the output and wrap it in a single codeblock for easy copy-paste.
```

**Regular progress saving:**
```
Create an AGOR snapshot of our current progress and commit it to your memory branch so we don't lose this work. Use dev tools to format the snapshot output and wrap it in a single codeblock.
```

### ❌ Avoid These

> "Save our progress" *(too vague - agent might use its own methods)*
> "Create a backup" *(agent won't use AGOR tools)*
> "Document what we've done" *(agent will write text, not use snapshots)*
> "Generate a handoff prompt" *(missing codeblock request - output won't be copy-pasteable)*

## 🚀 Git Operations & Release Management

### ✅ Good Examples

**Committing work:**
```
Use AGOR's `quick_commit_and_push()` to commit our changes with a proper message about the authentication feature we just built. Wrap the output in a single codeblock so I can copy and paste easily.
```

**Creating release notes:**
```
Use the AGOR dev tools to generate release notes for this update. Include the bug fixes and new features we implemented. Run it through our dev tools formatting and wrap the output in a single codeblock for easy copy-paste.
```

**PR descriptions:**
```
Use `generate_pr_description_output()` to create a properly formatted PR description for this branch. Wrap the final output in a single codeblock so I can copy and paste it directly.
```

### ❌ Avoid These

> "Commit our changes" *(agent might use basic git)*
> "Write release notes" *(agent will write manually, won't format properly)*
> "Create a PR description" *(agent won't use AGOR formatting or codeblock)*

## 🔄 Agent Coordination & Handoffs

### ✅ Good Examples

**Creating handoffs:**
```
Use AGOR's handoff tools to create a comprehensive snapshot and generate a session end prompt for the next agent. In the handoff prompt, instruct the next agent to generate their own snapshot when they complete their work and create a return handoff prompt using AGOR dev tools. Wrap the output in a single codeblock so I can copy and paste easily for a clean transition.
```

**Loading previous work:**
```
Use AGOR's snapshot loading tools to understand what the previous agent accomplished and what needs to be done next. When you complete your analysis, create your own snapshot using AGOR tools and wrap the output in a single codeblock.
```

**Multi-agent coordination:**
```
Update the agentconvo.md file using AGOR protocols to let other agents know we're working on the backend API. Include instructions for the next agent to update the conversation log when they start their work. Format the output in a single codeblock for easy copy-paste.
```

### ❌ Avoid These

> "Hand this off to another agent" *(too vague, no codeblock request)*
> "Check what was done before" *(agent won't use AGOR tools)*
> "Coordinate with other agents" *(agent will improvise, no AGOR guidance)*

## 🔗 Stacking Multiple Requests

**Complex workflow example:**
```
First refactor the authentication module and then update our unit tests. Create a PR description, run it through our dev tools so it's formatted properly, then wrap the output in a single codeblock.

Then similarly create release notes for OurProject v1.2.3, run the output through our dev tools again and wrap it in its own codeblock as well.

Then generate a snapshot and a handoff prompt to another agent. Explain in detail what you have accomplished here and ask for a review and a return handoff prompt. Use AGOR dev tools and wrap it in a single codeblock. In your handoff instructions, tell the next agent to generate their own snapshot after the review and create a return handoff using AGOR tools.
```

**Multi-step coordination:**
```
Use AGOR tools to commit our current progress, then create a development snapshot titled 'Feature X Implementation Complete'. Generate a handoff prompt for the QA agent, instructing them to run tests, document any issues in agentconvo.md, and create their own handoff back to development if fixes are needed. Wrap each output (commit confirmation, snapshot, and handoff prompt) in separate codeblocks for easy copy-paste.
```

## 🛠️ Development Workflow

### ✅ Good Examples

**Starting work:**
```
Use AGOR tools to initialize this project workspace and create your agent memory branch before we begin coding. Wrap any initialization output in a single codeblock for easy reference.
```

**Testing and validation:**
```
After running the tests, use AGOR's commit tools to save our changes and create a snapshot titled 'Tests passing - ready for review'. Use dev tools to format the snapshot and wrap it in a single codeblock.
```

**Code review preparation:**
```
Use AGOR's PR generation tools to create a comprehensive PR description that explains our implementation approach and testing strategy. Run it through generate_pr_description_output() and wrap the final result in a single codeblock so I can copy and paste it directly.
```

### ❌ Avoid These

> "Set up the workspace" *(agent won't use AGOR initialization)*
> "Save our work" *(too vague, no codeblock request)*
> "Prepare for code review" *(agent will improvise, no formatting specified)*

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
4. **Always request single codeblock output** for easy copy-paste
5. **Emphasize using existing tools** rather than creating new approaches
6. **Reference the agent's memory branch** for continuity
7. **For multi-agent work**: Tell the next agent what AGOR actions to take
8. **Stack multiple requests** efficiently in one prompt

## 🚫 Common Mistakes

- Asking agents to "figure out the best way" *(they'll avoid AGOR tools)*
- Using vague language like "save" or "document" *(not specific enough)*
- Assuming agents know to use AGOR tools *(they need explicit direction)*
- **Not requesting single codeblock output** *(output won't be copy-pasteable)*
- Not telling the next agent what AGOR actions to take *(breaks agent-to-agent flow)*
- Forgetting to specify dev tools formatting *(output won't be properly formatted)*

Remember: **Agents need clear, explicit instructions to use AGOR tools effectively AND format output properly!**
