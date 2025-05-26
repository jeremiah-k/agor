#!/usr/bin/env python3
"""
Git Configuration Setup for AGOR Bundle Environment

This script applies git configuration that was captured during bundle creation,
ensuring agents use the same git identity as the bundle creator.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=capture_output, text=True
        )
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        if capture_output:
            return None
        raise e


def get_current_git_config():
    """Get current git configuration."""
    name = run_command("git config user.name", check=False)
    email = run_command("git config user.email", check=False)
    return name, email


def get_environment_config():
    """Get git configuration from environment variables."""
    # Check multiple possible environment variable names
    env_name = (
        os.getenv("GIT_AUTHOR_NAME")
        or os.getenv("GIT_USER_NAME")
        or os.getenv("GIT_COMMITTER_NAME")
    )
    env_email = (
        os.getenv("GIT_AUTHOR_EMAIL")
        or os.getenv("GIT_USER_EMAIL")
        or os.getenv("GIT_COMMITTER_EMAIL")
    )
    return env_name, env_email


def load_captured_config():
    """Load git configuration that was captured during bundle creation."""
    # Look for git_config.json in the same directory as this script
    script_dir = Path(__file__).parent
    config_file = script_dir / "git_config.json"

    if not config_file.exists():
        return None

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except Exception:
        return None


def apply_captured_config():
    """Apply git configuration that was captured during bundle creation."""
    config = load_captured_config()

    if not config:
        print("⚠️  No captured git configuration found.")
        return False

    name = config.get("user_name")
    email = config.get("user_email")

    if not name or not email:
        print("⚠️  Incomplete git configuration in bundle.")
        return False

    print("📦 Applying git configuration from bundle...")
    print(f"   Name: {name}")
    print(f"   Email: {email}")

    set_git_config(name, email)

    # Show when this config was captured
    captured_at = config.get("captured_at")
    if captured_at:
        print(f"   Captured: {captured_at}")

    return True


def set_git_config(name=None, email=None, global_scope=False):
    """Set git configuration."""
    scope = "--global" if global_scope else ""

    if name:
        cmd = f"git config {scope} user.name '{name}'"
        run_command(cmd, capture_output=False)
        print(f"✅ Set user.name: {name}")

    if email:
        cmd = f"git config {scope} user.email '{email}'"
        run_command(cmd, capture_output=False)
        print(f"✅ Set user.email: {email}")


def get_repo_info():
    """Get current repository information."""
    try:
        repo_root = run_command("git rev-parse --show-toplevel", check=False)
        if repo_root:
            repo_name = os.path.basename(repo_root)
            current_branch = run_command("git branch --show-current", check=False)
            return repo_name, current_branch
    except Exception:
        pass
    return None, None


def show_config():
    """Show current git configuration and environment."""
    print("🔍 Current Git Configuration:")

    current_name, current_email = get_current_git_config()
    if current_name or current_email:
        print(f"   Name: {current_name or 'Not set'}")
        print(f"   Email: {current_email or 'Not set'}")
    else:
        print("   No git configuration found")

    # Show captured configuration from bundle
    captured_config = load_captured_config()
    if captured_config:
        print("\n📦 Captured Configuration (from bundle):")
        if captured_config.get("user_name"):
            print(f"   Name: {captured_config['user_name']}")
        if captured_config.get("user_email"):
            print(f"   Email: {captured_config['user_email']}")
        if captured_config.get("captured_at"):
            print(f"   Captured: {captured_config['captured_at']}")

    # Show environment variables
    env_name, env_email = get_environment_config()
    if env_name or env_email:
        print("\n🌍 Environment Variables:")
        if env_name:
            print(f"   Name: {env_name}")
        if env_email:
            print(f"   Email: {env_email}")

    # Show repository info
    repo_name, current_branch = get_repo_info()
    if repo_name:
        print(f"\n📁 Repository: {repo_name}")
        print(f"🌿 Current branch: {current_branch}")
        if current_branch == "main":
            print("💡 Ready to create feature branch when needed")


def setup_git_from_env():
    """Set up git configuration from environment variables."""
    env_name, env_email = get_environment_config()

    if not env_name and not env_email:
        print("⚠️  No git environment variables found.")
        print("   Set one of: GIT_AUTHOR_NAME, GIT_USER_NAME, GIT_COMMITTER_NAME")
        print("   Set one of: GIT_AUTHOR_EMAIL, GIT_USER_EMAIL, GIT_COMMITTER_EMAIL")
        return False

    print("🔧 Setting up git configuration from environment...")
    set_git_config(env_name, env_email)

    repo_name, current_branch = get_repo_info()
    if repo_name:
        print(f"\n📁 Repository: {repo_name}")
        print(f"🌿 Current branch: {current_branch}")
        if current_branch == "main":
            print("💡 Ready to create feature branch when needed")

    print("\n🚀 Git configuration complete!")
    return True


def setup_git_manual(name, email, global_scope=False):
    """Set up git configuration manually."""
    print("🔧 Setting up git configuration...")
    set_git_config(name, email, global_scope)

    repo_name, current_branch = get_repo_info()
    if repo_name:
        print(f"\n📁 Repository: {repo_name}")
        print(f"🌿 Current branch: {current_branch}")
        if current_branch == "main":
            print("💡 Ready to create feature branch when needed")

    print("\n🚀 Git configuration complete!")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) == 1:
        print("🛠️  AGOR Git Configuration Setup")
        print("=" * 40)
        print()
        show_config()
        print()
        print("Usage:")
        print("  python git_setup.py --show                    # Show current config")
        print(
            "  python git_setup.py --apply-bundle           # Apply config from bundle"
        )
        print(
            "  python git_setup.py --import-env              # Import from environment"
        )
        print("  python git_setup.py --set 'Name' 'email@example.com'  # Set manually")
        print(
            "  python git_setup.py --set 'Name' 'email@example.com' --global  # Set globally"
        )
        return

    if "--show" in sys.argv:
        show_config()
    elif "--apply-bundle" in sys.argv:
        if apply_captured_config():
            repo_name, current_branch = get_repo_info()
            if repo_name:
                print(f"\n📁 Repository: {repo_name}")
                print(f"🌿 Current branch: {current_branch}")
                if current_branch == "main":
                    print("💡 Ready to create feature branch when needed")
            print("\n🚀 Git configuration complete!")
    elif "--import-env" in sys.argv:
        setup_git_from_env()
    elif "--set" in sys.argv:
        try:
            set_index = sys.argv.index("--set")
            name = sys.argv[set_index + 1]
            email = sys.argv[set_index + 2]
            global_scope = "--global" in sys.argv
            setup_git_manual(name, email, global_scope)
        except (IndexError, ValueError):
            print("❌ Invalid --set usage. Provide name and email:")
            print("   python git_setup.py --set 'Your Name' 'your@email.com'")
    else:
        print("❌ Unknown option. Use --show, --apply-bundle, --import-env, or --set")


# Functions for programmatic use by other tools
def configure_git_for_agent():
    """
    Configure git for an AI agent automatically.

    This function tries captured config first, then environment variables,
    then prompts for manual setup. Returns True if configuration was successful.
    """
    print("🤖 Configuring git for AI agent...")

    # First try captured configuration from bundle
    if apply_captured_config():
        return True

    # Then try environment variables
    if setup_git_from_env():
        return True

    # If no configuration available, show current config and guidance
    print("\n" + "=" * 50)
    print("🔧 Git Configuration Required")
    print("=" * 50)
    show_config()
    print()
    print("To configure git, you can:")
    print("1. Apply bundle config: python git_setup.py --apply-bundle")
    print("2. Set environment variables and run: python git_setup.py --import-env")
    print("3. Set manually: python git_setup.py --set 'Your Name' 'your@email.com'")
    print()
    print("Environment variables to set:")
    print("  export GIT_AUTHOR_NAME='Your Name'")
    print("  export GIT_AUTHOR_EMAIL='your@email.com'")

    return False


if __name__ == "__main__":
    main()
