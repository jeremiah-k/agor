"""
Configuration management for AGOR.

Supports JSON config files with environment variable overrides.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import platformdirs


class AgorConfig:
    """Configuration manager for AGOR with JSON files and environment variable support."""

    # Default configuration values
    DEFAULT_CONFIG = {
        "compression_format": "zip",
        "quiet": False,
        "preserve_history": False,
        "main_only": False,
        "interactive": True,
        "assume_yes": False,
        "shallow_depth": 5,
        "download_chunk_size": 1024,
        "progress_bar_width": 80,
        "git_binary_url": "https://github.com/nikvdp/1bin/releases/download/v0.0.40/git",
        "git_binary_sha256": "af17911884c5afcf5be1c2438483e8d65a82c6a80ed8a354b8d4f6e0b964978f",
        "clipboard_copy_default": True,
    }

    # Environment variable prefix
    ENV_PREFIX = "AGOR_"

    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path(platformdirs.user_config_dir("agor"))
        self.config_file = self.config_dir / "config.json"
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file and environment variables."""
        # Start with defaults
        config = self.DEFAULT_CONFIG.copy()

        # Load from JSON file if it exists
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  Warning: Could not load config file {self.config_file}: {e}")

        # Override with environment variables
        for key in config:
            env_key = f"{self.ENV_PREFIX}{key.upper()}"
            env_value = os.environ.get(env_key)
            if env_value is not None:
                # Convert string values to appropriate types
                if isinstance(config[key], bool):
                    config[key] = env_value.lower() in ("true", "1", "yes", "on")
                elif isinstance(config[key], int):
                    try:
                        config[key] = int(env_value)
                    except ValueError:
                        print(
                            f"⚠️  Warning: Invalid integer value for {env_key}: {env_value}"
                        )
                else:
                    config[key] = env_value

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save to file."""
        self._config[key] = value
        self.save()

    def save(self) -> None:
        """Save current configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)
        except OSError as e:
            print(f"❌ Error: Could not save config file {self.config_file}: {e}")

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        if self.config_file.exists():
            try:
                self.config_file.unlink()
            except OSError as e:
                print(
                    f"⚠️  Warning: Could not remove config file {self.config_file}: {e}"
                )

    def show(self) -> Dict[str, Any]:
        """Return current configuration for display."""
        return self._config.copy()

    def get_env_vars(self) -> Dict[str, str]:
        """Get all AGOR environment variables currently set."""
        env_vars = {}
        for key in self.DEFAULT_CONFIG:
            env_key = f"{self.ENV_PREFIX}{key.upper()}"
            env_value = os.environ.get(env_key)
            if env_value is not None:
                env_vars[env_key] = env_value
        return env_vars


# Global configuration instance
config = AgorConfig()
