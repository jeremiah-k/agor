#!/usr/bin/env python3
"""
Test script to verify that AGOR strategy modules can be loaded in bundle mode.
This simulates the exec() loading that happens in bundle environments.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_bundle_mode_loading():
    """Test loading strategy modules in bundle mode using exec()."""

    print("🧪 Testing AGOR Strategy Bundle Mode Loading")
    print("=" * 50)

    # Get the current directory
    current_dir = Path(__file__).parent
    agor_tools_dir = current_dir / "src" / "agor" / "tools"

    if not agor_tools_dir.exists():
        print(f"❌ AGOR tools directory not found: {agor_tools_dir}")
        return False

    # Create a temporary directory to simulate bundle extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        bundle_agor_tools = temp_path / "agor_tools"

        print(f"📁 Creating simulated bundle at: {bundle_agor_tools}")

        # Copy agor_tools to simulate bundle extraction
        shutil.copytree(agor_tools_dir, bundle_agor_tools)

        # Change to the bundle directory
        original_cwd = os.getcwd()
        os.chdir(temp_path)

        try:
            # Test loading each strategy module using exec()
            strategy_files = [
                "agor_tools/strategies/multi_agent_strategies.py",
                "agor_tools/strategies/parallel_divergent.py",
                "agor_tools/strategies/mob_programming.py",
                "agor_tools/strategies/red_team.py",
                "agor_tools/strategies/quality_gates.py",
                "agor_tools/strategies/team_management.py",
                "agor_tools/strategies/workflow_design.py"
            ]

            results = {}

            for strategy_file in strategy_files:
                print(f"\n🔍 Testing: {strategy_file}")

                try:
                    # This simulates how bundles load strategy files
                    with open(strategy_file, 'r') as f:
                        strategy_code = f.read()

                    # Create a new namespace for execution
                    exec_globals = {
                        '__name__': '__main__',
                        '__file__': strategy_file,
                        '__builtins__': __builtins__
                    }
                    exec(strategy_code, exec_globals)

                    print(f"✅ Successfully loaded {strategy_file}")
                    results[strategy_file] = "SUCCESS"

                    # Test specific functions if they exist
                    if 'select_strategy' in exec_globals:
                        try:
                            result = exec_globals['select_strategy']("test project", 3, "medium")
                            print(f"✅ select_strategy() function works")
                        except Exception as e:
                            print(f"⚠️  select_strategy() function exists but failed: {e}")

                except Exception as e:
                    print(f"❌ Failed to load {strategy_file}: {e}")
                    results[strategy_file] = f"FAILED: {e}"

            # Summary
            print("\n" + "=" * 50)
            print("📊 BUNDLE MODE LOADING TEST RESULTS")
            print("=" * 50)

            success_count = 0
            for file, result in results.items():
                status = "✅" if result == "SUCCESS" else "❌"
                print(f"{status} {file}: {result}")
                if result == "SUCCESS":
                    success_count += 1

            print(f"\n📈 Success Rate: {success_count}/{len(strategy_files)} ({success_count/len(strategy_files)*100:.1f}%)")

            if success_count == len(strategy_files):
                print("🎉 ALL STRATEGY MODULES LOAD SUCCESSFULLY IN BUNDLE MODE!")
                return True
            else:
                print("⚠️  Some strategy modules failed to load in bundle mode")
                return False

        finally:
            # Restore original working directory
            os.chdir(original_cwd)

if __name__ == "__main__":
    success = test_bundle_mode_loading()
    sys.exit(0 if success else 1)
