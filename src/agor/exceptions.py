"""
Custom exceptions for AGOR to replace generic Exception handling.
"""


class AgorError(Exception):
    """Base exception for all AGOR-specific errors."""

    pass


class ConfigurationError(AgorError):
    """Raised when there's an issue with configuration."""

    pass


class RepositoryError(AgorError):
    """Raised when there's an issue with git repository operations."""

    pass


class NetworkError(AgorError):
    """Raised when there's a network-related error."""

    pass


class CompressionError(AgorError):
    """Raised when there's an issue with file compression."""

    pass


class ValidationError(AgorError):
    """Raised when input validation fails."""

    pass


class GitBinaryError(AgorError):
    """Raised when there's an issue with the git binary."""

    pass


class PlatformError(AgorError):
    """Raised when there's a platform-specific error."""

    pass


class ClipboardError(AgorError):
    """Raised when clipboard operations fail."""

    pass
