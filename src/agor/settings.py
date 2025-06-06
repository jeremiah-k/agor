"""
Pydantic settings for AGOR configuration.

Replaces the old config.py globals with a proper settings object
that can read from environment variables and config files.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgorSettings(BaseSettings):
    """AGOR configuration settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="AGOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Git operations
    default_shallow_depth: int = Field(
        default=100, description="Default depth for shallow git clones"
    )
    git_binary_url: str = Field(
        default="https://github.com/nikvdp/1bin/releases/download/v0.0.40/git",
        description="URL to download portable git binary",
    )
    git_binary_sha256: str = Field(
        default="af17911884c5afcf5be1c2438483e8d65a82c6a80ed8a354b8d4f6e0b964978f",
        description="SHA256 hash for git binary verification",
    )

    # Bundle creation
    compression_format: str = Field(
        default="zip", description="Default compression format for bundles"
    )
    preserve_history: bool = Field(
        default=True, description="Whether to preserve full git history in bundles"
    )
    main_only: bool = Field(
        default=False,
        description="Whether to bundle only main/master branch by default",
    )

    # Memory management
    memory_file: str = Field(
        default=".agor/memory.md",
        description="Path to memory file relative to project root",
    )

    # User interface
    interactive: bool = Field(
        default=True, description="Whether to show interactive prompts"
    )
    assume_yes: bool = Field(
        default=False, description="Whether to assume yes for all prompts"
    )
    clipboard_copy_default: bool = Field(
        default=True, description="Whether to copy prompts to clipboard by default"
    )

    # Logging
    log_level: str = Field(
        default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    # Paths
    config_dir: Optional[Path] = Field(
        default=None, description="Custom configuration directory"
    )
    cache_dir: Optional[Path] = Field(
        default=None, description="Custom cache directory"
    )


# Global settings instance
settings = AgorSettings()
