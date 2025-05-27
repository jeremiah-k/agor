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

### Essential Setup (All Roles)

1. **Verify AGOR tools access**:
   ```bash
   # You should be in the AGOR repository directory
   ls src/agor/tools/  # Verify tools are available
   ```

2. **Navigate to target project**:
   ```bash
   # Go to the project you're working on
   cd /path/to/target/project
   # or clone it if needed:
   # git clone https://github.com/user/project.git && cd project
   ```

3. **Set up git configuration**:
   ```bash
   # Configure git identity (use system git)
   git config user.name "AGOR AI Agent"
   git config user.email "ai-agent@example.com"

   # Verify setup
   git status
   ```

4. **Load AGOR tools** (if needed):
   ```python
   # Import AGOR tools from the cloned repository
   import sys
   sys.path.append('/path/to/agor/src')
   from agor.tools import code_exploration
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
