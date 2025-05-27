# 📦 AGOR Bundle Mode Initialization Guide

**For AI agents working in bundle mode (uploaded archives)**

**How to know you're in Bundle Mode**: Look for `/tmp/agor_tools/` directory with bundled tools.

This is a streamlined initialization guide specifically for bundle mode. Follow these steps exactly.

## 🎯 Step 1: Role Confirmation

You should have already selected your role from README_ai.md:
- **Role A**: SOLO DEVELOPER
- **Role B**: PROJECT COORDINATOR
- **Role C**: AGENT WORKER

## 🔧 Step 2: Bundle Mode Setup

### Essential Setup (All Roles)

1. **Locate the project directory**:
   ```bash
   # Find the git repository
   find /tmp -name ".git" -type d 2>/dev/null
   cd /tmp/project  # or wherever the .git directory was found
   ```

2. **Set up git configuration**:
   ```bash
   # Make git binary executable
   chmod 755 /tmp/agor_tools/git

   # Configure git identity
   /tmp/agor_tools/git config user.name "AgentOrchestrator"
   /tmp/agor_tools/git config user.email "agor@example.local"

   # Verify setup
   /tmp/agor_tools/git status
   ```

3. **Load code exploration tools**:
   ```python
   # Load the bundled tools
   exec(open('/tmp/agor_tools/code_exploration.py').read())
   ```

## 📊 Step 3: Role-Specific Initialization

### For SOLO DEVELOPER (Role A)

1. **Perform codebase analysis** using the loaded tools
2. **Present analysis results** to the user
3. **Display the SOLO DEVELOPER menu** (and ONLY this menu):

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

1. **Initialize coordination system** (create .agor/ directory)
2. **Perform project overview**
3. **Display the PROJECT COORDINATOR menu**

### For AGENT WORKER (Role C)

1. **Minimal setup** (git config, check coordination files)
2. **Announce readiness**
3. **Display the AGENT WORKER menu**

## ⚠️ Critical Rules for Bundle Mode

1. **NEVER show technical function names** like `tree('.')` or `analyze_file_structure(path)`
2. **ONLY show clean menus** as defined above
3. **Use the bundled git binary** at `/tmp/agor_tools/git` for all git operations
4. **Load tools internally** but don't expose the loading process to users
5. **Keep the user interface clean** and professional

## 🚫 What NOT to Show Users

❌ `tree('.') – show project structure`
❌ `grep('.', 'def ') – search for function definitions`
❌ `analyze_file_structure(path) – analyze any file`
❌ Any Python function calls or technical documentation

✅ Clean menu options like `tree) directory structure`
✅ Professional descriptions of capabilities
✅ Clear action-oriented choices

---

**Remember**: Bundle mode users should see a polished, professional interface. Keep all technical implementation details hidden.
