#!/usr/bin/env python3
"""
Test specific strategy functions mentioned in the snapshot to ensure they work in bundle mode.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_strategy_functions():
    """Test key strategy functions in bundle mode."""
    
    print("🧪 Testing AGOR Strategy Functions in Bundle Mode")
    print("=" * 60)
    
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
            # Test the main functions mentioned in the snapshot
            test_cases = [
                {
                    'file': 'agor_tools/strategies/multi_agent_strategies.py',
                    'functions': ['select_strategy', 'initialize_parallel_divergent', 'initialize_mob_programming', 'initialize_red_team']
                },
                {
                    'file': 'agor_tools/strategies/parallel_divergent.py', 
                    'functions': ['ParallelDivergentProtocol']
                },
                {
                    'file': 'agor_tools/strategies/quality_gates.py',
                    'functions': ['setup_quality_gates']
                }
            ]
            
            for test_case in test_cases:
                print(f"\n🔍 Testing functions in: {test_case['file']}")
                
                try:
                    # Load the strategy file
                    with open(test_case['file'], 'r') as f:
                        strategy_code = f.read()
                    
                    exec_globals = {
                        '__name__': '__main__',
                        '__file__': test_case['file'],
                        '__builtins__': __builtins__
                    }
                    exec(strategy_code, exec_globals)
                    
                    # Test each function
                    for func_name in test_case['functions']:
                        if func_name in exec_globals:
                            print(f"  ✅ {func_name} - function exists")
                            
                            # Test specific functions with sample calls
                            try:
                                if func_name == 'select_strategy':
                                    result = exec_globals[func_name]("test project", 3, "medium")
                                    print(f"  ✅ {func_name} - function executes successfully")
                                elif func_name == 'setup_quality_gates':
                                    result = exec_globals[func_name]("Test Project", "comprehensive", "high")
                                    print(f"  ✅ {func_name} - function executes successfully")
                                elif func_name.startswith('initialize_'):
                                    result = exec_globals[func_name]("test task", 3)
                                    print(f"  ✅ {func_name} - function executes successfully")
                                elif func_name.endswith('Protocol'):
                                    # Test class instantiation
                                    instance = exec_globals[func_name]()
                                    print(f"  ✅ {func_name} - class instantiates successfully")
                                else:
                                    print(f"  ✅ {func_name} - function exists (not tested)")
                            except Exception as e:
                                print(f"  ⚠️  {func_name} - exists but execution failed: {e}")
                        else:
                            print(f"  ❌ {func_name} - function not found")
                
                except Exception as e:
                    print(f"❌ Failed to load {test_case['file']}: {e}")
            
            print(f"\n🎯 Testing exec() loading as mentioned in snapshot...")
            
            # Test the exact exec() pattern mentioned in the snapshot
            try:
                exec_code = 'exec(open("agor_tools/strategies/multi_agent_strategies.py").read())'
                exec_globals = {'__builtins__': __builtins__}
                exec(exec_code, exec_globals)
                print("✅ Direct exec(open(...).read()) pattern works!")
                
                # Check if select_strategy is available
                if 'select_strategy' in exec_globals:
                    print("✅ select_strategy() available after direct exec")
                else:
                    print("⚠️  select_strategy() not found in global scope after exec")
                    
            except Exception as e:
                print(f"❌ Direct exec(open(...).read()) pattern failed: {e}")
                
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

if __name__ == "__main__":
    test_strategy_functions()
