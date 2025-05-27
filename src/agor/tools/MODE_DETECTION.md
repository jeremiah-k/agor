# 🔍 AGOR Mode Detection Guide

**Quick reference for determining your operational mode**

## 🤖 How to Detect Your Mode

### Bundle Mode Indicators:

- ✅ `/tmp/agor_tools/` directory exists
- ✅ `/tmp/agor_tools/git` binary is present
- ✅ `/tmp/agor_tools/code_exploration.py` exists
- ✅ You're working with uploaded/extracted files
- ✅ Project is typically in `/tmp/project/` or similar

### Standalone Mode Indicators:

- ✅ You cloned AGOR repository yourself
- ✅ You have direct git access to repositories
- ✅ You're working in a persistent environment
- ✅ System git is available (`which git` works)
- ✅ You can push/pull directly to remote repositories

## 🚀 Quick Detection Commands

```bash
# Check for bundle mode
ls /tmp/agor_tools/ 2>/dev/null && echo "Bundle Mode" || echo "Not Bundle Mode"

# Check for system git (standalone mode)
which git && echo "System Git Available" || echo "No System Git"

# Check current directory structure
pwd && ls -la
```

## 📋 Mode-Specific Initialization

Once you've determined your mode:

### Bundle Mode → Use `BUNDLE_INITIALIZATION.md`

- Streamlined setup
- Professional user interface
- Bundled tools and git binary

### Standalone Mode → Use `STANDALONE_INITIALIZATION.md`

- Comprehensive setup
- Direct repository access
- System integration

## ⚠️ Important Notes

- **Bundle Mode**: Focus on user experience, hide technical details
- **Standalone Mode**: More technical capabilities, direct git operations
- **Both Modes**: Converge to same role-specific menus after initialization
- **Never Mix**: Don't use bundle mode instructions in standalone mode or vice versa

---

**When in doubt**: Check for `/tmp/agor_tools/` - if it exists, you're in Bundle Mode.
