"""
Constants for AGOR to replace magic numbers and hard-coded values.
"""

# Git operations
DEFAULT_SHALLOW_DEPTH = 5  # Shallow clone gets last 5 commits instead of full history
GIT_BINARY_URL = "https://github.com/nikvdp/1bin/releases/download/v0.0.26/git"

# File operations
DOWNLOAD_CHUNK_SIZE = 1024  # 1 Kibibyte chunks for downloads
PROGRESS_BAR_WIDTH = 80  # Consistent progress bar width

# Compression formats
SUPPORTED_COMPRESSION_FORMATS = ["zip", "gz", "bz2"]
DEFAULT_COMPRESSION_FORMAT = "zip"

# Platform detection
TERMUX_INDICATORS = [
    "com.termux",  # In HOME environment variable
    "/data/data/com.termux",  # In path
    "termux",  # In various environment variables
]

# Git binary integrity - placeholder hash (verification disabled for compatibility)
GIT_BINARY_SHA256 = "placeholder_hash_for_v0.0.26_git_binary_disable_verification"

# CLI defaults
DEFAULT_CLIPBOARD_COPY = True
DEFAULT_INTERACTIVE = True
DEFAULT_ASSUME_YES = False
DEFAULT_PRESERVE_HISTORY = False
DEFAULT_MAIN_ONLY = False

# File extensions
ARCHIVE_EXTENSIONS = {
    "zip": ".zip",
    "gz": ".tar.gz",
    "bz2": ".tar.bz2",
}

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
