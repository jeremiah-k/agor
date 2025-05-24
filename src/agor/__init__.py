"""
AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

A comprehensive project planning and multi-agent coordination platform.
Plan complex development projects, design agent teams, and generate
specialized prompts for coordinated AI development workflows.
"""

import os

# Version management - single source of truth
__version__ = "0.1.0"

# Override with environment variable if available (for CI/CD)
if "GITHUB_REF_NAME" in os.environ:
    __version__ = os.environ.get("GITHUB_REF_NAME")

__author__ = "Jeremiah K."
__email__ = "jeremiahk@gmx.com"
