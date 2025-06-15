"""
Development Testing Module for AGOR Development Tools

This module contains all testing utilities and environment detection functionality
extracted from dev_tools.py for better organization and maintainability.

Functions:
- test_tooling: Comprehensive development tools tests
- detect_environment: Environment detection and configuration
- Environment validation and setup utilities
"""

import sys
from pathlib import Path
from typing import Any, Dict

from agor.tools.git_operations import (
    get_current_timestamp,
    get_file_timestamp,
    get_ntp_timestamp,
    get_precise_timestamp,
    run_git_command,
)


def detect_environment() -> Dict[str, Any]:
    """
    Detect the current development environment and return configuration details.

    Returns:
        Dictionary containing environment information:
        - mode: development, standalone, augmentcode_local, or bundle
        - platform: detected platform information
        - agor_version: AGOR version if available
        - python_version: Python version
        - has_git: Whether git is available
        - has_pyenv: Whether .pyenv directory exists
    """
    environment = {
        "mode": "unknown",
        "platform": "unknown",
        "agor_version": "0.4.4+",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "has_git": False,
        "has_pyenv": False,
    }

    # Detect git availability
    success, _ = run_git_command(["--version"])
    environment["has_git"] = success

    # Check for .pyenv directory
    environment["has_pyenv"] = Path(".pyenv").exists()

    # Detect mode based on environment
    if Path("src/agor").exists() and Path("pyproject.toml").exists():
        environment["mode"] = "development"
        environment["platform"] = "Development Environment"
    elif Path("src/agor/tools").exists():
        environment["mode"] = "standalone"
        environment["platform"] = "Standalone Mode"
    else:
        # Try to detect if we're in AugmentCode environment
        import importlib.util

        if importlib.util.find_spec("augment"):
            environment["mode"] = "augmentcode_local"
            environment["platform"] = "AugmentCode Local Agent"
        else:
            environment["mode"] = "bundle"
            environment["platform"] = "Bundle Mode"

    # Try to get AGOR version
    try:
        from agor import __version__

        environment["agor_version"] = __version__
    except ImportError:
        # Fallback version detection
        if environment["mode"] == "development":
            environment["agor_version"] = "0.4.3-dev"

    return environment


def test_tooling() -> bool:
    """
    Test all development tools functions to ensure they work correctly.

    This function validates:
    - Timestamp generation
    - Git operations
    - Environment detection
    - Import functionality

    Returns:
        True if all tests pass, False otherwise
    """
    print("🧪 Testing AGOR Development Tools...")

    try:
        print("Testing dev tools functions...")

        # Test timestamp functions
        current_ts = get_current_timestamp()
        file_ts = get_file_timestamp()
        precise_ts = get_precise_timestamp()
        ntp_ts = get_ntp_timestamp()

        print(f"📅 Current timestamp: {current_ts}")
        print(f"📁 File timestamp: {file_ts}")
        print(f"⏰ Precise timestamp: {precise_ts}")
        print(f"🌐 NTP timestamp: {ntp_ts}")

        # Test git operations (git binary detection handled in run_git_command)
        success, version_output = run_git_command(["--version"])
        if success:
            print(f"✅ Git working: {version_output.strip()}")
        else:
            print(f"❌ Git not available: {version_output}")
            return False

        # Test current branch detection
        success, branch = run_git_command(["branch", "--show-current"])
        if success:
            print(f"🌿 Current branch: {branch.strip()}")
        else:
            print(f"⚠️  Branch detection issue: {branch}")

        # Test working directory status
        success, status = run_git_command(["status", "--porcelain"])
        if success:
            if status.strip():
                lines = status.strip().split("\n")
                print(f"📝 Working directory has changes: {len(lines)} files")
            else:
                print("📝 Working directory clean")
        else:
            print(f"⚠️  Status check issue: {status}")

        print("🎉 Development tooling test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Development tooling test failed: {e}")
        return False


def get_agent_dependency_install_commands() -> str:
    """
    Returns shell commands for installing agent development tools dependencies,
    with automatic fallback to a `.pyenv` virtual environment if standard installation fails.

    Returns:
        Shell commands for dependency installation
    """
    return """# Install ONLY the dependencies needed for agent dev tools (NOT requirements.txt)
python3 -m pip install -r src/agor/tools/agent-requirements.txt || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    fi
}"""


def generate_dynamic_installation_prompt(environment: Dict[str, Any]) -> str:
    """
    Generate dynamic installation instructions based on detected environment.

    Args:
        environment: Environment configuration from detect_environment()

    Returns:
        Formatted installation instructions
    """
    base_instructions = """
## Detected Environment
"""

    # Add environment details
    base_instructions += f"""- **Mode**: {environment['mode']}
- **Platform**: {environment['platform']}
- **AGOR Version**: {environment['agor_version']}
- **Python Version**: {environment['python_version']}
- **Git Available**: {'✅' if environment['has_git'] else '❌'}
- **Virtual Environment**: {'✅ .pyenv found' if environment['has_pyenv'] else '❌ No .pyenv'}

## Installation Instructions

"""

    # Add mode-specific instructions
    if environment["mode"] == "development":
        dev_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### Development Mode Setup
```bash
# Install development dependencies
python3 -m pip install -r requirements.txt

{dev_install_commands}

# Test development tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_testing import test_tooling
test_tooling()
"
```
"""
    elif environment["mode"] == "augmentcode_local":
        local_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### AugmentCode Local Agent Setup
```bash
# Dependencies should be automatically available
# Verify memory manager dependencies
python3 -c "import pydantic, pydantic_settings; print('✅ Dependencies OK')"

# If missing, install with fallback
{local_install_commands}
```
"""
    elif environment["mode"] == "standalone":
        standalone_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### Standalone Mode Setup
```bash
# Install dependencies from requirements.txt
python3 -m pip install -r requirements.txt

{standalone_install_commands}

# Test AGOR tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_testing import test_tooling
test_tooling()
"
```
"""
    else:
        base_instructions += """### Standard Setup
```bash
# Install AGOR if not already installed
pipx install agor

# Verify installation
agor --version
```
"""

    # Add troubleshooting section
    base_instructions += """
## Troubleshooting

If you encounter issues:

1. **Missing Dependencies**: Install agent-requirements.txt
2. **Git Issues**: Ensure git is installed and configured
3. **Permission Issues**: Try using virtual environment (.pyenv)
4. **Import Errors**: Verify src/ directory is in Python path

"""

    return base_instructions
