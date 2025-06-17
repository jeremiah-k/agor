# AGOR External Project Integration Guide

**For AI agents working on projects where AGOR is installed separately**

This guide addresses the critical integration issues identified in meta feedback and provides standardized workflows for using AGOR tools with external projects.

## 🎯 Problem Statement

When AGOR is installed separately from the project being worked on (e.g., Augment local agent working on an external project with AGOR installed elsewhere), agents encounter:

1. **Tool Location Issues**: Cannot find AGOR tools in separate directory
2. **Module Import Failures**: Internal dependencies fail even when path is found
3. **Missing Integration Pattern**: No standardized workflow for external usage
4. **Documentation Gap**: Unclear how to integrate AGOR with external projects

## ✅ Solution: External Integration System

### Quick Start

```python
# Step 1: Import the external integration system
from agor.tools.external_integration import get_agor_tools

# Step 2: Initialize with automatic detection
tools = get_agor_tools()

# Step 3: Use AGOR functions with automatic fallback
tools.generate_pr_description_output("Your PR content here")
tools.create_development_snapshot("Feature Implementation", "Added new functionality")
tools.quick_commit_and_push("Implement feature X")
```

### Detailed Integration Steps

#### 1. Environment Setup

**Option A: Automatic Detection (Recommended)**

```python
from agor.tools.external_integration import AgorExternalTools

# Automatic detection tries multiple methods:
# - Direct import (if AGOR in same environment)
# - Common installation paths (~/agor, ~/dev/agor, etc.)
# - Python site-packages
tools = AgorExternalTools()
tools.print_status()  # Check what was detected
```

**Option B: Explicit Path**

```python
# If you know where AGOR is installed
tools = AgorExternalTools(agor_path="/path/to/agor")
```

**Option C: Environment Variable**

```bash
export AGOR_PATH="/path/to/agor"
```

```python
import os
tools = AgorExternalTools(agor_path=os.getenv('AGOR_PATH'))
```

#### 2. Dependency Installation

The external integration system requires minimal dependencies:

```bash
# Install required packages for external integration
pip install pathlib importlib-util

# Optional: Install full AGOR requirements if available
pip install -r /path/to/agor/src/agor/tools/agent-requirements.txt
```

#### 3. Function Usage with Fallbacks

All AGOR functions work with automatic fallback when tools are unavailable:

```python
# These functions work whether AGOR is available or not
tools = get_agor_tools()

# Generate formatted outputs (with fallback formatting)
pr_description = tools.generate_pr_description_output("""
# Feature Implementation

- Added new authentication system
- Updated user interface
- Fixed critical security bug
""")

# Create development snapshots (with fallback logging)
success = tools.create_development_snapshot(
    title="Authentication System Implementation",
    context="Completed OAuth integration and user management"
)

# Quick git operations (with fallback git commands)
tools.quick_commit_and_push("Implement OAuth authentication", "✨")

# Get workspace status (with fallback information)
status = tools.get_workspace_status()
print(f"Project status: {status}")
```

## 🛠️ Available Functions

### Core Development Functions

| Function                           | Purpose                | Fallback Behavior                     |
| ---------------------------------- | ---------------------- | ------------------------------------- |
| `generate_pr_description_output()` | Format PR descriptions | Manual deticking + codeblock wrapping |
| `generate_handoff_prompt_output()` | Format agent handoffs  | Manual deticking + codeblock wrapping |
| `generate_release_notes_output()`  | Format release notes   | Manual deticking + codeblock wrapping |
| `create_development_snapshot()`    | Create work snapshots  | Logging with context summary          |
| `quick_commit_and_push()`          | Git commit and push    | Direct git commands                   |
| `get_workspace_status()`           | Project status info    | Basic fallback status                 |
| `test_all_tools()`                 | Test functionality     | Integration status check              |

### Status and Debugging

```python
# Check integration status
tools.print_status()

# Get detailed status information
status = tools.get_status()
print(f"AGOR Available: {status['agor_available']}")
print(f"Fallback Mode: {status['fallback_mode']}")
print(f"Functions Available: {len(status['functions_available'])}")
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "ModuleNotFoundError: No module named 'agor'"

**Solution**: Use external integration system instead of direct imports

```python
# ❌ Don't do this in external projects
from agor.tools.dev_tools import generate_pr_description_output

# ✅ Do this instead
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()
tools.generate_pr_description_output("content")
```

#### Issue 2: "AGOR tools not found"

**Solutions**:

1. **Specify explicit path**:

   ```python
   tools = AgorExternalTools(agor_path="/explicit/path/to/agor")
   ```

2. **Check common locations**:

   ```bash
   # Look for AGOR in these locations:
   ls ~/agor/src/agor/tools/
   ls ~/dev/agor/src/agor/tools/
   ls /opt/agor/src/agor/tools/
   ```

3. **Use environment variable**:
   ```bash
   export AGOR_PATH="/path/to/agor"
   ```

#### Issue 3: "Import errors even with correct path"

**Solution**: The external integration system handles internal dependencies automatically. If you still get errors:

```python
# Check what's actually available
tools = get_agor_tools()
tools.print_status()

# Use fallback mode explicitly
if not tools.agor_available:
    print("Using fallback mode - limited functionality")
    # Functions still work, just with basic implementations
```

### Debugging Steps

1. **Test the integration**:

   ```python
   from agor.tools.external_integration import get_agor_tools
   tools = get_agor_tools()
   tools.test_all_tools()
   ```

2. **Check search paths**:

   ```python
   import sys
   print("Python path:", sys.path)

   from pathlib import Path
   common_paths = [Path.home() / "agor", Path.home() / "dev" / "agor"]
   for path in common_paths:
       print(f"Checking {path}: {path.exists()}")
   ```

3. **Verify AGOR installation**:
   ```bash
   # If AGOR is properly installed, these should exist:
   find ~ -name "dev_tools.py" -path "*/agor/tools/*" 2>/dev/null
   ```

## 📋 Integration Checklist

When setting up AGOR external integration:

- [ ] Import external integration system (not direct AGOR imports)
- [ ] Initialize with automatic detection or explicit path
- [ ] Test integration status with `tools.print_status()`
- [ ] Verify functions work with `tools.test_all_tools()`
- [ ] Use fallback-aware function calls
- [ ] Handle both success and fallback scenarios in your workflow

## 🚀 Best Practices

### 1. Always Use External Integration System

```python
# ✅ Correct approach for external projects
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()

# ❌ Avoid direct imports in external projects
# from agor.tools.dev_tools import create_development_snapshot
```

### 2. Check Status Before Critical Operations

```python
tools = get_agor_tools()
if tools.agor_available:
    # Full AGOR functionality available
    tools.create_development_snapshot("Title", "Full context")
else:
    # Fallback mode - still functional but limited
    print("⚠️  Using fallback mode")
    tools.create_development_snapshot("Title", "Basic logging")
```

### 3. Handle Both Success and Fallback Scenarios

```python
# Generate outputs that work in both modes
pr_output = tools.generate_pr_description_output(content)
# This works whether AGOR is available or in fallback mode

# Always check the result
if tools.agor_available:
    print("✅ Generated with full AGOR formatting")
else:
    print("🔄 Generated with fallback formatting")
```

### 4. Use Environment Variables for Team Consistency

```bash
# In your project's setup documentation
export AGOR_PATH="/team/standard/agor/location"
```

## 📚 Related Documentation

- **[AGOR_INSTRUCTIONS.md](AGOR_INSTRUCTIONS.md)**: Complete AGOR operational guide
- **[README_ai.md](README_ai.md)**: Role selection and initialization
- **[agent-start-here.md](agent-start-here.md)**: Quick startup guide
- **[index.md](index.md)**: Documentation index

## 🔄 Migration from Direct Imports

If you have existing code using direct AGOR imports:

```python
# Old approach (fails in external projects)
from agor.tools.dev_tools import (
    generate_pr_description_output,
    create_development_snapshot,
    quick_commit_and_push
)

# New approach (works everywhere)
from agor.tools.external_integration import get_agor_tools
tools = get_agor_tools()

# Same function calls, but through the tools object
tools.generate_pr_description_output(content)
tools.create_development_snapshot(title, context)
tools.quick_commit_and_push(message)
```

---

**This integration system solves the critical meta feedback issues and enables seamless AGOR usage across all project types.**
