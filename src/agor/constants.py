"""
Constants for AGOR - immutable values only.

Mutable configuration values have been moved to settings.py.
"""

# File operations
DOWNLOAD_CHUNK_SIZE = 1024  # 1 Kibibyte chunks for downloads
PROGRESS_BAR_WIDTH = 80  # Consistent progress bar width

# Compression formats
SUPPORTED_COMPRESSION_FORMATS = ["zip", "gz", "bz2"]

# Platform detection
TERMUX_INDICATORS = [
    "com.termux",  # In HOME environment variable
    "/data/data/com.termux",  # In path
    "termux",  # In various environment variables
]

# Note: Git binary settings moved to settings.py
# Note: CLI defaults moved to settings.py

# File extensions
ARCHIVE_EXTENSIONS = {
    "zip": ".zip",
    "gz": ".tar.gz",
    "bz2": ".tar.bz2",
}

# Protocol version - increment when coordination protocols change
# This is separate from AGOR version and tracks protocol compatibility
# 0.x.x = Development/testing phase, 1.0.0+ = Production-ready
PROTOCOL_VERSION = "0.4.0"

# Version checking
VERSION_CHECK_URL = "https://api.github.com/repos/jeremiah-k/agor/releases/latest"
PROTOCOL_CHECK_URL = (
    "https://raw.githubusercontent.com/jeremiah-k/agor/main/src/agor/constants.py"
)

# Error messages
ERROR_MESSAGES = {
    "invalid_repo": "❌ Invalid repository. Please provide a valid git repository URL or local path.",
    "invalid_branch": "❌ Invalid branch name. Branch names cannot contain spaces or special characters like ..",
    "network_error": "❌ Network error. Please check your internet connection and try again.",
    "git_error": "❌ Git operation failed. Please ensure the repository exists and is accessible.",
    "file_error": "❌ File operation failed. Please check file permissions and available disk space.",
    "compression_error": "❌ Compression failed. Please check available disk space and try again.",
}

# Success messages
SUCCESS_MESSAGES = {
    "bundle_created": "🎼 AGOR Bundle created successfully!",
    "config_saved": "✅ Configuration saved successfully!",
    "config_reset": "🔄 Configuration reset to defaults!",
    "clipboard_copied": "📋 Copied to clipboard!",
}
