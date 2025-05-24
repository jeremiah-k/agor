"""
AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

A comprehensive project planning and multi-agent coordination platform.
Plan complex development projects, design agent teams, and generate
specialized prompts for coordinated AI development workflows.
"""

import os
import pkg_resources

# First try to get version from environment variable (GitHub tag)
if "GITHUB_REF_NAME" in os.environ:
    __version__ = os.environ.get("GITHUB_REF_NAME")
else:
    # Fall back to setup.cfg metadata using pkg_resources (compatible with PyInstaller)
    try:
        __version__ = pkg_resources.get_distribution("agor").version
    except pkg_resources.DistributionNotFound:
        # If all else fails, use hardcoded version
        __version__ = "0.1.0"

__author__ = "Jeremiah K."
__email__ = "jeremiahk@gmx.com"
