"""
Comprehensive unit tests for documentation validation functionality.

Tests cover document structure validation, link checking, configuration validation,
file format support, error handling, and performance considerations.
"""

import pytest

# Use pytest.importorskip to conditionally import the real module
docs_validation = pytest.importorskip("agor.docs_validation")

# Import the functions and classes directly from the module
from agor.docs_validation import (
    validate_documentation,
    validate_documentation_batch,
    validate_documentation_structure,
    validate_config,
    validate_links,
    DocumentValidationResult,
    ConfigValidationResult,
    LinkValidationResult
)