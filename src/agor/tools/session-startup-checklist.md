# 🚀 Session Startup Checklist

**For every agent session - follow this sequence before starting work.**

## ✅ Step 1: Git Configuration

```bash
# Set up git config (prevents push failures)
git config user.email "jeremiah-k@users.noreply.github.com"
git config user.name "Jeremiah K"

# Verify it worked
git config --list | grep user
```

## ✅ Step 2: Create Feature Branch

```bash
# AI agents NEVER work directly on main
# Create feature branch from current head
git checkout -b feature/descriptive-name

# Verify you're on the feature branch
git branch
```

**Branch Naming Convention:**

- `feature/add-documentation`
- `feature/fix-memory-system`
- `feature/update-protocols`

## ✅ Step 3: Development Environment

```bash
# Test AGOR development tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tools import test_tooling
test_tooling()
"
```

## ✅ Step 4: Workflow Strategy

**Throughout your session:**

- **Commit frequently** - after each logical unit of work
- **Push regularly** - every 2-3 commits minimum
- **Use clear commit messages** with emoji prefixes
- **Never wait until end of session** to push

```bash
# Example commit pattern
git add .
git commit -m "📋 Add feature documentation"
git push origin feature/your-branch-name
```

## 🔄 Step 5: Create Pull Request

**When your work is complete:**

1. **Push your feature branch** to origin
2. **Create a Pull Request** to merge into main
3. **Never merge directly to main** - always use PR review process
4. **Include clear PR description** with changes and testing completed

## 🎯 Why This Matters

- **Prevents push failures** due to email privacy settings
- **Protects main branch** from direct AI commits (main is protected)
- **Enables code review** through PR process before merging
- **Avoids losing work** if session ends unexpectedly
- **Maintains clean git history** with proper attribution
- **Enables collaboration** with real-time updates on feature branches

---

**Copy this checklist to your session notes and check off each step before starting work.**
