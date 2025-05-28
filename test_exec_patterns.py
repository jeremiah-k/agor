#!/usr/bin/env python3
"""
Test different exec() patterns for loading AGOR strategies in bundle mode.
This demonstrates the proper way to use exec() as mentioned in the snapshot.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_exec_patterns():
    """Test various exec() patterns for bundle mode loading."""
    
    print("🧪 Testing AGOR Strategy exec() Patterns")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    agor_tools_dir = current_dir / "src" / "agor" / "tools"
    
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
            print("\n🎯 Pattern 1: Basic exec(open(...).read()) - WILL FAIL")
            try:
                exec(open("agor_tools/strategies/multi_agent_strategies.py").read())
                print("✅ Basic exec pattern works")
            except Exception as e:
                print(f"❌ Basic exec pattern failed: {e}")
                print("   This is expected - needs proper globals")
            
            print("\n🎯 Pattern 2: exec() with proper globals - RECOMMENDED")
            try:
                # Create proper execution environment
                exec_globals = {
                    '__name__': '__main__',
                    '__file__': 'agor_tools/strategies/multi_agent_strategies.py',
                    '__builtins__': __builtins__
                }
                
                exec(open("agor_tools/strategies/multi_agent_strategies.py").read(), exec_globals)
                
                # Test that functions are available
                if 'select_strategy' in exec_globals:
                    result = exec_globals['select_strategy']("test project", 3, "medium")
                    print("✅ exec() with proper globals works!")
                    print("✅ select_strategy() function accessible and working")
                else:
                    print("⚠️  Functions not found in exec_globals")
                    
            except Exception as e:
                print(f"❌ exec() with proper globals failed: {e}")
            
            print("\n🎯 Pattern 3: exec() into current globals - SIMPLE")
            try:
                # This pattern makes functions available in current namespace
                exec(open("agor_tools/strategies/multi_agent_strategies.py").read(), globals())
                
                # Test that functions are now available globally
                if 'select_strategy' in globals():
                    result = select_strategy("test project", 3, "medium")
                    print("✅ exec() into globals() works!")
                    print("✅ select_strategy() function accessible globally")
                else:
                    print("⚠️  Functions not found in global namespace")
                    
            except Exception as e:
                print(f"❌ exec() into globals() failed: {e}")
            
            print("\n🎯 Pattern 4: Testing all initialize_*() functions")
            try:
                # Load the file with proper globals
                exec_globals = {
                    '__name__': '__main__',
                    '__file__': 'agor_tools/strategies/multi_agent_strategies.py',
                    '__builtins__': __builtins__
                }
                exec(open("agor_tools/strategies/multi_agent_strategies.py").read(), exec_globals)
                
                # Test all initialize functions mentioned in the snapshot
                initialize_functions = [
                    'initialize_parallel_divergent',
                    'initialize_mob_programming', 
                    'initialize_red_team'
                ]
                
                for func_name in initialize_functions:
                    if func_name in exec_globals:
                        try:
                            result = exec_globals[func_name]("test task", 3)
                            print(f"✅ {func_name}() works in bundle mode")
                        except Exception as e:
                            print(f"⚠️  {func_name}() exists but failed: {e}")
                    else:
                        print(f"❌ {func_name}() not found")
                        
            except Exception as e:
                print(f"❌ Testing initialize functions failed: {e}")
            
            print("\n📋 BUNDLE MODE USAGE RECOMMENDATIONS")
            print("=" * 50)
            print("For agents working in bundle mode, use this pattern:")
            print()
            print("```python")
            print("# Recommended pattern for bundle mode")
            print("exec_globals = {")
            print("    '__name__': '__main__',")
            print("    '__file__': 'agor_tools/strategies/multi_agent_strategies.py',")
            print("    '__builtins__': __builtins__")
            print("}")
            print("exec(open('agor_tools/strategies/multi_agent_strategies.py').read(), exec_globals)")
            print()
            print("# Access functions from exec_globals")
            print("select_strategy = exec_globals['select_strategy']")
            print("result = select_strategy('project description', 3, 'medium')")
            print("```")
            print()
            print("Or for simpler usage:")
            print("```python")
            print("# Simple pattern - functions become globally available")
            print("exec(open('agor_tools/strategies/multi_agent_strategies.py').read(), globals())")
            print("result = select_strategy('project description', 3, 'medium')")
            print("```")
                
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

if __name__ == "__main__":
    test_exec_patterns()
