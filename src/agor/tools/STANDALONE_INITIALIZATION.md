# 🚀 AGOR Standalone Mode Initialization Guide

**For AI agents with direct git access and system capabilities**

**How to know you're in Standalone Mode**: You cloned AGOR yourself and have direct git access to repositories.

This guide is for agents that have cloned AGOR themselves and have direct access to repositories.

## 🎯 Step 1: Role Confirmation

You should have already selected your role from README_ai.md:

- **Role A**: SOLO DEVELOPER
- **Role B**: PROJECT COORDINATOR
- **Role C**: AGENT WORKER

## 🔧 Step 2: Standalone Mode Setup

These steps assume you are already operating *within* the target project's repository. The main task is to access AGOR's instructional files and utility scripts.

### Essential Setup (All Roles)

1.  **Locate/Access AGOR Instructional Files and Utilities:**
    Determine how AGOR's instructional files (`README_ai.md`, `AGOR_INSTRUCTIONS.md`) and Python utilities are accessible. Consider these scenarios to identify the path to these tools:
    *   **Scenario A (Working on AGOR itself):** Tools are in `src/agor/tools/`.
    *   **Scenario B (Embedded in user project):** Tools might be in `.agor_tools/`.
    *   **Scenario C (AGOR cloned separately for protocols):** Tools might be in `/tmp/agor_protocols/src/agor/tools/`.

    You will use this path to `cat` `README_ai.md` and `AGOR_INSTRUCTIONS.md`, and to execute Python utilities.

2.  **Git Setup and Verification (in the current target project repository):**

    ```bash
    # Configure git identity (use system git)
    # Ensure these are appropriate for the user's project context and your operational guidelines
    git config user.name "AGOR AI Agent (Standalone)"
    git config user.email "ai-agent.standalone@example.com"

    # Test git functionality with a temporary test commit
    CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
    TEST_BRANCH="agor-git-test-$(date +%s)"
    git checkout -b "$TEST_BRANCH"
    echo "# AGOR Git Test $(date)" > .agor-standalone-test.md
    git add .agor-standalone-test.md
    if git commit -m "Test: Verify git configuration in Standalone Mode"; then
      echo "Git commit successful."
      git checkout "$CURRENT_BRANCH"
      git branch -D "$TEST_BRANCH"
      rm -f .agor-standalone-test.md
    else
      echo "ERROR: Git commit failed. Please check your Git configuration and repository permissions."
      # Attempt to cleanup
      git reset HEAD .agor-standalone-test.md
      git checkout "$CURRENT_BRANCH"
      git branch -D "$TEST_BRANCH" 2>/dev/null || true
      rm -f .agor-standalone-test.md
      echo "Please resolve Git issues before proceeding."
      # Agent should halt or seek guidance if this fails.
    fi
    ```
    This verification step ensures you can make commits in the current project repository. If it fails, you must resolve git configuration or permission issues.

3.  **Using AGOR Python Utilities** (if required by `AGOR_INSTRUCTIONS.md` for your role/task):
    When `AGOR_INSTRUCTIONS.md` refers to executing a Python script (e.g., for code exploration, strategy management):
    *   Invoke it using `python path/to/agor/tools/script_name.py [arguments]`. The `path/to/agor/tools/` is determined in Step 2.1.
    *   Example (if AGOR tools were accessed from `/tmp/agor_protocols/`):
        ```bash
        python /tmp/agor_protocols/src/agor/tools/code_exploration.py --pattern "my_function" .
        ```

## 📊 Step 3: Role-Specific Initialization

### For SOLO DEVELOPER (Role A)

1. **Perform codebase analysis** using available tools
2. **Present analysis results** to the user
3. **Display the SOLO DEVELOPER menu**:

```
🎼 SOLO DEVELOPER - Ready for Action

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

Select an option:
```

### For PROJECT COORDINATOR (Role B)

1. **Initialize coordination system** (create .agor/ directory in target project)
2. **Perform project overview**
3. **Display the PROJECT COORDINATOR menu**

### For AGENT WORKER (Role C)

1. **Check for existing coordination** (look for .agor/ directory)
2. **Announce readiness**
3. **Display the AGENT WORKER menu**

## 🔄 Key Differences from Bundle Mode

### Advantages:

- **Direct git access**: Can push/pull directly to repositories
- **System integration**: Access to full system capabilities
- **Real-time collaboration**: Multiple agents can work on live repositories
- **No file size limits**: Complete repository access

### Considerations:

- **Security**: Direct commit access requires careful permission management
- **Environment setup**: Must have git and other tools installed
- **Coordination**: .agor/ files must be committed/pushed for multi-agent coordination

## ⚠️ Critical Rules for Standalone Mode

1. **Use system git**: No need for bundled git binary
2. **Commit coordination files**: .agor/ directory should be version controlled
3. **Real git operations**: Push/pull for multi-agent coordination
4. **Clean user interface**: Still show professional menus, not technical details

## 🔄 Git Operations

```bash
# Standard git operations (use system git)
git status
git add .
git commit -m "Your commit message"
git push origin branch-name

# For coordination
git add .agor/
git commit -m "Update coordination files"
git push
```

## 🤝 Multi-Agent Coordination

In standalone mode, coordination happens through:

- **Shared .agor/ directory**: Version controlled coordination files
- **Real-time git operations**: Push/pull coordination state
- **Direct repository access**: All agents work on the same live repository

---

**Remember**: Standalone mode provides more power but requires more responsibility. Use git operations carefully and coordinate with other agents through version control.
