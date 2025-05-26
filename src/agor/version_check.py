"""
Version checking utilities for AGOR and protocol versions.
"""

import re
from typing import Optional, Tuple

import httpx
import structlog

from . import __version__
from .constants import PROTOCOL_CHECK_URL, PROTOCOL_VERSION, VERSION_CHECK_URL

log = structlog.get_logger()


def get_current_versions() -> Tuple[str, str]:
    """Get current AGOR and protocol versions."""
    return __version__, PROTOCOL_VERSION


def check_agor_version() -> Optional[dict]:
    """
    Check for AGOR updates from GitHub releases.

    Returns:
        dict with version info if update available, None otherwise
    """
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(VERSION_CHECK_URL)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data["tag_name"].lstrip("v")
            current_version = __version__

            # Simple version comparison (assumes semantic versioning)
            if _is_newer_version(latest_version, current_version):
                return {
                    "current": current_version,
                    "latest": latest_version,
                    "url": release_data["html_url"],
                    "published_at": release_data["published_at"],
                    "name": release_data.get("name", f"AGOR {latest_version}"),
                }

    except Exception as e:
        log.debug("Failed to check AGOR version", error=str(e))

    return None


def check_protocol_version() -> Optional[dict]:
    """
    Check for protocol version updates from main branch.

    Returns:
        dict with protocol info if update available, None otherwise
    """
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(PROTOCOL_CHECK_URL)
            response.raise_for_status()

            content = response.text

            # Extract protocol version from constants.py
            match = re.search(r'PROTOCOL_VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if not match:
                return None

            latest_protocol = match.group(1)
            current_protocol = PROTOCOL_VERSION

            if _is_newer_version(latest_protocol, current_protocol):
                return {
                    "current": current_protocol,
                    "latest": latest_protocol,
                    "url": "https://github.com/jeremiah-k/agor/blob/main/src/agor/constants.py",
                }

    except Exception as e:
        log.debug("Failed to check protocol version", error=str(e))

    return None


def _is_newer_version(latest: str, current: str) -> bool:
    """
    Compare version strings to determine if latest is newer than current.

    Handles semantic versioning (X.Y.Z) and development versions.
    """
    # Handle development/unknown versions
    if current in ["development", "unknown"]:
        return True

    try:
        # Parse semantic versions
        latest_parts = [int(x) for x in latest.split(".")]
        current_parts = [int(x) for x in current.split(".")]

        # Pad shorter version with zeros
        max_len = max(len(latest_parts), len(current_parts))
        latest_parts.extend([0] * (max_len - len(latest_parts)))
        current_parts.extend([0] * (max_len - len(current_parts)))

        return latest_parts > current_parts

    except (ValueError, AttributeError):
        # Fallback to string comparison if parsing fails
        return latest != current


def display_version_info(check_updates: bool = True) -> None:
    """Display current version information and optionally check for updates."""
    current_agor, current_protocol = get_current_versions()

    print(f"🎼 AGOR Version: {current_agor}")
    print(f"📋 Protocol Version: {current_protocol}")

    if not check_updates:
        return

    print("\n🔍 Checking for updates...")

    # Check AGOR version
    agor_update = check_agor_version()
    if agor_update:
        print(
            f"✨ AGOR update available: {agor_update['current']} → {agor_update['latest']}"
        )
        print(f"   Release: {agor_update['name']}")
        print(f"   URL: {agor_update['url']}")
        print("   Update: pipx upgrade agor")
    else:
        print("✅ AGOR is up to date")

    # Check protocol version
    protocol_update = check_protocol_version()
    if protocol_update:
        print(
            f"📋 Protocol update available: {protocol_update['current']} → {protocol_update['latest']}"
        )
        print(
            "   This may include new hotkeys, coordination features, or agent capabilities"
        )
        print("   Update AGOR to get the latest protocol version")
    else:
        print("✅ Protocol is up to date")


def should_check_version() -> bool:
    """
    Determine if we should check for version updates.

    Checks for updates once per day to avoid being annoying.
    """
    try:
        import time
        from pathlib import Path

        # Use platformdirs for cache directory
        import platformdirs

        cache_dir = Path(platformdirs.user_cache_dir("agor"))
        cache_dir.mkdir(parents=True, exist_ok=True)

        version_check_file = cache_dir / "last_version_check"

        if not version_check_file.exists():
            return True

        # Check if it's been more than 24 hours
        last_check = version_check_file.stat().st_mtime
        return (time.time() - last_check) > 86400  # 24 hours

    except Exception:
        return False


def mark_version_checked() -> None:
    """Mark that we've checked for version updates."""
    try:
        from pathlib import Path

        import platformdirs

        cache_dir = Path(platformdirs.user_cache_dir("agor"))
        cache_dir.mkdir(parents=True, exist_ok=True)

        version_check_file = cache_dir / "last_version_check"
        version_check_file.touch()

    except Exception:
        pass


def check_versions_if_needed() -> None:
    """Check for version updates if it's been a while since last check."""
    if should_check_version():
        print("🔍 Checking for AGOR updates...")

        # Check AGOR version
        agor_update = check_agor_version()
        if agor_update:
            print(
                f"✨ AGOR update available: {agor_update['current']} → {agor_update['latest']}"
            )
            print("   Update with: pipx upgrade agor")
            print(f"   Release: {agor_update['url']}")

        # Check protocol version
        protocol_update = check_protocol_version()
        if protocol_update:
            print(
                f"📋 Protocol update available: {protocol_update['current']} → {protocol_update['latest']}"
            )
            print("   Update AGOR to get the latest coordination protocols")

        if not agor_update and not protocol_update:
            print("✅ AGOR and protocol are up to date")

        mark_version_checked()
        print()  # Add spacing after version check
