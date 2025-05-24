"""
AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform

A comprehensive project planning and multi-agent coordination platform.
Plan complex development projects, design agent teams, and generate
specialized prompts for coordinated AI development workflows.
"""

import os

# First try to get version from environment variable (GitHub tag)
if "GITHUB_REF_NAME" in os.environ:
    __version__ = os.environ.get("GITHUB_REF_NAME")
else:
    # Fall back to package metadata
    try:
        # Try modern importlib.metadata first (Python 3.8+)
        from importlib.metadata import version
        __version__ = version("agor")
    except ImportError:
        # Fall back to pkg_resources for older Python versions
        try:
            import pkg_resources
            __version__ = pkg_resources.get_distribution("agor").version
        except (ImportError, pkg_resources.DistributionNotFound):
            # If all else fails, use hardcoded version
            __version__ = "0.1.0"
    except Exception:
        # If package not found or any other error, use hardcoded version
        __version__ = "0.1.0"

__author__ = "Jeremiah K."
__email__ = "jeremiahk@gmx.com"
