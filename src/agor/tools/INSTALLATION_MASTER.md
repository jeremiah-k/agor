# 🛠️ AGOR Installation Master Reference

**Single source of truth for all AGOR installation instructions**

This file contains the canonical installation instructions that are referenced by all other documentation to eliminate duplication and ensure consistency.

## 📦 Core AGOR Installation

### Method 1: pipx (Recommended)
```bash
# Install AGOR using pipx (isolated environment)
pipx install agor

# Verify installation
agor --version
# Should output: agor, version 0.4.1
```

### Method 2: pip (Alternative)
```bash
# Install AGOR using pip
pip install agor

# Verify installation
agor --version
```

### Prerequisites
- **Python 3.10+** installed
- **Git** installed and configured
- **pipx** recommended (install with `pip install pipx`)

## 🔧 Git Configuration (Optional but Recommended)

```bash
# Import from environment variables
agor git-config --import-env

# Or set manually
agor git-config --name "Your Name" --email "your@email.com"

# Verify configuration
git config --list | grep -E "(user\.|author\.|committer\.)"
```

## 🚀 Development Dependencies (For AGOR Development)

### Standard Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt
```

### Memory Manager Dependencies (Critical for Agent Coordination)
```bash
# Install additional dependencies for memory manager types
pip install pydantic pydantic-settings || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        pip install pydantic pydantic-settings
    fi
}
```

### Development Tooling Test
```bash
# Test the AGOR development tooling to ensure everything works
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling, get_timestamp

# Verify tooling works
test_tooling()
print(f'Session started at: {get_timestamp()}')
"
```

## 🎯 Platform-Specific Setup

### Bundle Mode Platforms
- **Google AI Studio**: Use `.zip` format (`agor bundle . -f zip`)
- **ChatGPT**: Use `.tar.gz` format (`agor bundle .`)
- **Other upload platforms**: Choose appropriate format

### Standalone Mode Platforms
- **AugmentCode Remote Agents**: Direct git access, full coordination
- **Jules by Google**: URL-based file access, limited git capabilities
- **Local AI assistants**: File system access with AGOR integration

### Local Integration Platforms
- **AugmentCode Local Agent**: Workspace integration with persistent guidelines
- **VS Code extensions**: Direct file access and context preservation
- **Development environments**: AI integration with AGOR protocols

## 🔍 Verification Steps

### Basic Installation Check
```bash
# Verify AGOR is installed and working
agor --version
agor --help
```

### Bundle Creation Test
```bash
# Test bundle creation (in any git repository)
agor bundle . --dry-run
```

### Development Environment Check
```bash
# Verify development dependencies (if doing AGOR development)
python3 -c "import pydantic, pydantic_settings; print('✅ Memory manager dependencies OK')"
```

## 🆘 Troubleshooting

### Common Issues

**"agor command not found"**
- Ensure pipx/pip installation completed successfully
- Check PATH includes pipx bin directory
- Try `python -m agor` as alternative

**"Git not configured"**
- Run `agor git-config` setup commands above
- Verify with `git config --list`

**"Memory manager type errors"**
- Install pydantic dependencies using commands above
- Verify with dependency check commands

**"Bundle creation fails"**
- Ensure you're in a git repository
- Check git status and commit any pending changes
- Verify git binary is accessible

### Platform-Specific Issues

**Google AI Studio**
- Enable Function Calling in model settings
- Use `.zip` format for bundles
- Ensure file upload limits are respected

**ChatGPT**
- Requires subscription for file uploads
- Use `.tar.gz` format for bundles
- Check file size limits

**Standalone Mode**
- Verify agent has git and shell access
- Ensure network access for repository cloning
- Check permissions for file operations

---

**Note**: This is the master reference for installation instructions. All other documentation should reference this file rather than duplicating these instructions.
