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

## ✅ Step 2: Development Environment

```bash
# Test AGOR development tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling
test_tooling()
"
```

## ✅ Step 3: Workflow Strategy

**Throughout your session:**

- **Commit frequently** - after each logical unit of work
- **Push regularly** - every 2-3 commits minimum  
- **Use clear commit messages** with emoji prefixes
- **Never wait until end of session** to push

```bash
# Example commit pattern
git add .
git commit -m "📋 Add feature documentation"
git push origin main
```

## 🎯 Why This Matters

- **Prevents push failures** due to email privacy settings
- **Avoids losing work** if session ends unexpectedly
- **Maintains clean git history** with proper attribution
- **Enables collaboration** with real-time updates

---

**Copy this checklist to your session notes and check off each step before starting work.**
