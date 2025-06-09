# 🎯 AGOR Menu Flow Guide

**Guidelines for smooth user experience through AGOR menus**

## 🔄 Menu Flow Principles

### 1. **Clear Feedback Loop**

When a user selects a hotkey, always provide:

- ✅ Confirmation of what action is being taken
- ✅ Clear indication of what's happening
- ✅ Results or next steps
- ✅ Return to menu or next action options

### 2. **Progressive Disclosure**

- **Level 1**: Main role menu (clean, simple)
- **Level 2**: Action confirmation and parameters
- **Level 3**: Execution and results
- **Level 4**: Next actions or return to menu

### 3. **Consistent Patterns**

All hotkey interactions should follow this pattern:

```
User Input: a
↓
Agent Response: "🔍 Analyzing codebase..."
↓
Agent Action: [Performs analysis]
↓
Agent Output: [Results]
↓
Agent Menu: [Clean menu with next options]
```

## 📋 Hotkey Response Templates

### Analysis Actions (a, f, co, tree, grep)

```
🔍 [ACTION NAME]
[Brief description of what's happening]

[RESULTS]

✅ Analysis complete. What would you like to do next?

[RETURN TO CLEAN MENU]
```

### Planning Actions (sp, bp, ar)

```
🎯 [PLANNING ACTION]
[Brief description]

[PLANNING RESULTS]

✅ Planning complete. Next steps:

[RETURN TO CLEAN MENU]
```

### Editing Actions (edit, commit, diff)

```
✏️ [EDITING ACTION]
[Brief description]

[EDITING RESULTS]

✅ Changes applied. What's next?

[RETURN TO CLEAN MENU]
```

## 🚫 What NOT to Do

❌ **Don't expose technical details**:

```
# BAD
tree('.') – show project structure
analyze_file_structure(path) – analyze any file
```

✅ **Do provide clean options**:

```
# GOOD
tree) directory structure
a) analyze codebase
```

❌ **Don't leave users hanging**:

```
# BAD
[Performs action]
[Shows results]
[No next steps]
```

✅ **Do provide clear next steps**:

```
# GOOD
[Performs action]
[Shows results]
✅ Action complete. What would you like to do next?
[Clean menu]
```

## 🎼 Menu Templates by Role

### Worker Agent Menu Template

```
🎼 Worker Agent - Ready for Action

**📊 Analysis & Display:**
a ) analyze codebase    f ) full files         co) changes only
da) detailed snapshot   m ) show diff

**🔍 Code Exploration:**
bfs) breadth-first search    grep) search patterns    tree) directory structure

**✏️ Editing & Changes:**
edit) modify files      commit) save changes    diff) show changes

**📋 Documentation:**
doc) generate docs      comment) add comments   explain) code explanation

**🎯 Planning Support:**
sp) strategic plan      bp) break down project

**🤝 Snapshot Procedures:**
snapshot) create snapshot document for another agent
load_snapshot) receive snapshot from another agent
list_snapshots) list all snapshot documents

**🔄 Meta-Development:**
meta) provide feedback on AGOR itself

**🔄 Session Navigation:**
?) quick help    menu) refresh options    reset) clean restart

Select an option:
```

### PROJECT COORDINATOR Menu Template

```
🎼 PROJECT COORDINATOR - Strategy & Coordination

**🎯 Strategic Planning:**
sp) strategic plan      bp) break down project     ar) architecture review
dp) dependency planning rp) risk planning

**⚡ Strategy Selection:**
ss) strategy selection  pd) parallel divergent     pl) pipeline
sw) swarm              rt) red team               mb) mob programming

**👥 Team Design:**
ct) create team        tm) team manifest          hp) snapshot prompts

**🔄 Coordination:**
wf) workflow design    qg) quality gates          init) initialize coordination

**📊 Basic Analysis:**
a ) analyze codebase   da) detailed snapshot

**🤝 Snapshot Procedures:**
snapshot) create snapshot document for another agent
load_snapshot) receive snapshot from another agent
list_snapshots) list all snapshot documents

**🔄 Meta-Development:**
meta) provide feedback on AGOR itself

**🔄 Session Navigation:**
?) quick help    menu) refresh options    reset) clean restart

Select an option:
```

### AGENT WORKER Menu Template

```
🎼 AGENT WORKER - Task Execution

**🤝 Coordination:**
status) check coordination    sync) update from main    ch) checkpoint planning

**📨 Communication:**
log) update agent log        msg) post to agentconvo   report) status report

**📋 Task Management:**
task) receive task          complete) mark complete    snapshot) prepare snapshot

**📊 Basic Analysis:**
a ) analyze codebase        f ) full files            co) changes only

**🤝 Snapshot Procedures:**
snapshot) create snapshot document for another agent
load_snapshot) receive snapshot from another agent
list_snapshots) list all snapshot documents

**🔄 Meta-Development:**
meta) provide feedback on AGOR itself

**🔄 Session Navigation:**
?) quick help    menu) refresh options    reset) clean restart

Select an option:
```

## 🔄 After Action Flow

After any hotkey action, always:

1. **Confirm completion**: "✅ [Action] complete"
2. **Show results**: Present the output clearly
3. **Provide next steps**: Suggest logical follow-up actions
4. **Return to menu**: Show the clean role-specific menu
5. **Wait for input**: "Select an option:"

## 💡 Best Practices

### For Bundle Mode:

- Keep interface polished and professional
- Hide all technical implementation details
- Focus on user experience
- Provide clear guidance at each step

### For Standalone Mode:

- Can be slightly more technical
- Still maintain clean menus
- Provide git operation feedback
- Show coordination status

### For All Modes:

- Always return to clean menus after actions
- Never leave users without next steps
- Maintain consistent formatting
- Use emojis and clear section headers

---

**Remember**: The goal is a smooth, professional experience where users always know what's happening and what they can do next.
