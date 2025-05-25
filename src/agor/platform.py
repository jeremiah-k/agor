"""
Platform detection and platform-specific utilities for AGOR.
"""

import os
import platform
import shutil
import subprocess
from pathlib import Path

import platformdirs

from .constants import TERMUX_INDICATORS


def is_termux() -> bool:
    """
    Check if running in Termux environment using multiple indicators.

    Returns:
        True if running in Termux, False otherwise
    """
    # Check HOME environment variable
    home = os.environ.get("HOME", "")
    if any(indicator in home for indicator in TERMUX_INDICATORS):
        return True

    # Check PATH environment variable
    path = os.environ.get("PATH", "")
    if any(indicator in path for indicator in TERMUX_INDICATORS):
        return True

    # Check PREFIX environment variable (Termux-specific)
    prefix = os.environ.get("PREFIX", "")
    if "termux" in prefix.lower():
        return True

    # Check if termux-specific commands exist
    if shutil.which("termux-info") or shutil.which("pkg"):
        return True

    return False


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Check if running on Linux (excluding Termux)."""
    return platform.system() == "Linux" and not is_termux()


def get_downloads_dir() -> str:
    """
    Get the Downloads directory path based on the platform.

    Returns:
        Path to the Downloads directory
    """
    if is_termux():
        # For Termux, use ~/storage/downloads
        storage_downloads = os.path.expanduser("~/storage/downloads")
        if os.path.exists(storage_downloads):
            return storage_downloads

    # For other environments, use platformdirs to get the standard downloads directory
    try:
        downloads_dir = platformdirs.user_downloads_dir()
        if os.path.exists(downloads_dir):
            return downloads_dir
    except Exception:
        pass

    # Fallback to standard Downloads directories
    home_dir = os.path.expanduser("~")

    # Try common Downloads directory names
    for downloads_name in ["Downloads", "Download"]:
        downloads_dir = os.path.join(home_dir, downloads_name)
        if os.path.exists(downloads_dir):
            return downloads_dir

    # Fallback to current directory
    return os.getcwd()


def copy_to_clipboard(text: str) -> tuple[bool, str]:
    """
    Copy text to clipboard with platform-specific handling.

    Args:
        text: Text to copy to clipboard

    Returns:
        Tuple of (success: bool, message: str)
    """
    # First try pyperclip as it works on many platforms
    try:
        import pyperclip

        pyperclip.copy(text)
        return True, "📋 Copied to clipboard!"
    except Exception:
        pass

    # Platform-specific fallbacks
    try:
        if is_termux():
            return _copy_termux(text)
        elif is_windows():
            return _copy_windows(text)
        elif is_macos():
            return _copy_macos(text)
        elif is_linux():
            return _copy_linux(text)
        else:
            return False, f"❌ Clipboard not supported on {platform.system()}"
    except Exception as e:
        return False, f"❌ Failed to copy to clipboard: {e}"


def _copy_termux(text: str) -> tuple[bool, str]:
    """Copy to clipboard in Termux environment."""
    try:
        subprocess.run(
            ["termux-clipboard-set"],
            input=text.encode("utf-8"),
            check=True,
        )
        return True, "📋 Copied to clipboard using termux-api!"
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"❌ Failed to copy with termux-api: {e}. Install with 'pkg install termux-api'",
        )
    except FileNotFoundError:
        return (
            False,
            "❌ termux-clipboard-set not found. Install with 'pkg install termux-api'",
        )


def _copy_windows(text: str) -> tuple[bool, str]:
    """Copy to clipboard on Windows."""
    # Try PowerShell first
    try:
        subprocess.run(
            ["powershell", "-command", f"Set-Clipboard -Value '{text}'"],
            check=True,
            capture_output=True,
        )
        return True, "📋 Copied to clipboard using PowerShell!"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Try clip.exe
    try:
        subprocess.run(
            ["clip"],
            input=text.encode("utf-8"),
            check=True,
        )
        return True, "📋 Copied to clipboard using clip.exe!"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "❌ No clipboard command found on Windows"


def _copy_macos(text: str) -> tuple[bool, str]:
    """Copy to clipboard on macOS."""
    try:
        subprocess.run("pbcopy", text=True, input=text, check=True)
        return True, "📋 Copied to clipboard using pbcopy!"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "❌ pbcopy not found on macOS"


def _copy_linux(text: str) -> tuple[bool, str]:
    """Copy to clipboard on Linux."""
    # Try xclip first
    if shutil.which("xclip"):
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True, "📋 Copied to clipboard using xclip!"
        except subprocess.CalledProcessError:
            pass

    # Try xsel
    if shutil.which("xsel"):
        try:
            subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True, "📋 Copied to clipboard using xsel!"
        except subprocess.CalledProcessError:
            pass

    # Try wl-copy (Wayland)
    if shutil.which("wl-copy"):
        try:
            subprocess.run(
                ["wl-copy"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True, "📋 Copied to clipboard using wl-copy!"
        except subprocess.CalledProcessError:
            pass

    return False, "❌ No clipboard command found. Install xclip, xsel, or wl-clipboard"


def reveal_file_in_explorer(file_path: Path) -> bool:
    """
    Reveal file in system file explorer.

    Args:
        file_path: Path to the file to reveal

    Returns:
        True if successful, False otherwise
    """
    try:
        if is_macos():
            subprocess.run(["open", "-R", str(file_path)], check=True)
            return True
        elif is_windows():
            subprocess.run(["explorer", "/select,", str(file_path)], check=True)
            return True
        elif is_linux() and not is_termux():
            # Try to open the parent directory
            subprocess.run(["xdg-open", str(file_path.parent)], check=True)
            return True
        else:
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_platform_info() -> dict:
    """Get comprehensive platform information."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "is_termux": is_termux(),
        "is_windows": is_windows(),
        "is_macos": is_macos(),
        "is_linux": is_linux(),
        "downloads_dir": get_downloads_dir(),
        "python_version": platform.python_version(),
    }
