"""
AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

A comprehensive project planning and multi-agent coordination platform.
Plan complex development projects, design agent teams, and generate
specialized prompts for coordinated AI development workflows.
"""

import os

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # Fallback for Python < 3.8
    from importlib_metadata import PackageNotFoundError, version

# First try to get version from environment variable (GitHub tag)
if "GITHUB_REF_NAME" in os.environ:
    __version__ = os.environ.get("GITHUB_REF_NAME")
else:
    # Fall back to package metadata using importlib.metadata (modern replacement for pkg_resources)
    try:
        __version__ = version("agor")
    except PackageNotFoundError:
        # If all else fails, use hardcoded version
        __version__ = "0.6.1"

__author__ = "Jeremiah K."
__email__ = "jeremiahk@gmx.com"
