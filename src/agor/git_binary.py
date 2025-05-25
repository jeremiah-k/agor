"""
Git binary management with integrity checking and fallback strategies.
"""

import shutil
import subprocess
from pathlib import Path
from typing import Optional

import platformdirs

from .config import config
from .exceptions import GitBinaryError
from .settings import settings
from .utils import download_file


class GitBinaryManager:
    """Manages git binary with 4-tier fallback strategy."""

    def __init__(self):
        """Initialize git binary manager."""
        self.cache_dir = Path(platformdirs.user_cache_dir("agor")) / "git_binary"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cached_binary = self.cache_dir / "git"

    def get_git_binary(self) -> str:
        """
        Get git binary path using 4-tier fallback strategy.

        Returns:
            Path to working git binary

        Raises:
            GitBinaryError: If no working git binary can be found
        """
        strategies = [
            self._try_system_git,
            self._try_cached_binary,
            self._try_download_binary,
            self._try_fallback_paths,
        ]

        for strategy in strategies:
            try:
                git_path = strategy()
                if git_path and self._test_git_binary(git_path):
                    return git_path
            except Exception:
                continue  # Try next strategy

        raise GitBinaryError(
            "❌ No working git binary found. Please install git or check your PATH."
        )

    def _try_system_git(self) -> Optional[str]:
        """Try to find git in system PATH."""
        git_path = shutil.which("git")
        if git_path:
            return git_path
        return None

    def _try_cached_binary(self) -> Optional[str]:
        """Try to use cached git binary."""
        if self.cached_binary.exists():
            # Verify integrity if we have the expected hash
            if self._verify_binary_integrity(self.cached_binary):
                self.cached_binary.chmod(0o755)
                return str(self.cached_binary)
            else:
                # Remove corrupted binary
                self.cached_binary.unlink(missing_ok=True)
        return None

    def _try_download_binary(self) -> Optional[str]:
        """Try to download git binary."""
        try:
            git_url = config.get("git_binary_url", settings.git_binary_url)
            expected_hash = config.get("git_binary_sha256", settings.git_binary_sha256)

            # Only verify hash if it's not the placeholder
            verify_hash = (
                expected_hash if expected_hash != settings.git_binary_sha256 else None
            )

            download_file(git_url, self.cached_binary, verify_hash)
            self.cached_binary.chmod(0o755)
            return str(self.cached_binary)
        except Exception:
            return None

    def _try_fallback_paths(self) -> Optional[str]:
        """Try common git installation paths."""
        fallback_paths = [
            "/usr/bin/git",
            "/usr/local/bin/git",
            "/opt/homebrew/bin/git",  # macOS Homebrew
            "/usr/local/git/bin/git",  # macOS git installer
            "C:\\Program Files\\Git\\bin\\git.exe",  # Windows
            "C:\\Program Files (x86)\\Git\\bin\\git.exe",  # Windows 32-bit
        ]

        for path in fallback_paths:
            if Path(path).exists():
                return path
        return None

    def _test_git_binary(self, git_path: str) -> bool:
        """Test if git binary works."""
        try:
            result = subprocess.run(
                [git_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0 and "git version" in result.stdout.lower()
        except Exception:
            return False

    def _verify_binary_integrity(self, binary_path: Path) -> bool:
        """Verify binary integrity using SHA256."""
        expected_hash = config.get("git_binary_sha256", settings.git_binary_sha256)

        # Skip verification if using placeholder hash
        if expected_hash == settings.git_binary_sha256:
            return True

        try:
            import hashlib

            sha256_hash = hashlib.sha256()
            with open(binary_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)

            actual_hash = sha256_hash.hexdigest()
            return actual_hash == expected_hash
        except Exception:
            return False

    def clear_cache(self) -> None:
        """Clear cached git binary."""
        if self.cached_binary.exists():
            self.cached_binary.unlink()

    def get_cache_info(self) -> dict:
        """Get information about cached git binary."""
        info = {
            "cache_dir": str(self.cache_dir),
            "cached_binary_exists": self.cached_binary.exists(),
            "cached_binary_path": (
                str(self.cached_binary) if self.cached_binary.exists() else None
            ),
        }

        if self.cached_binary.exists():
            info["cached_binary_size"] = self.cached_binary.stat().st_size
            info["integrity_verified"] = self._verify_binary_integrity(
                self.cached_binary
            )

        return info


# Global git binary manager instance
git_manager = GitBinaryManager()
