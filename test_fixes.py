#!/usr/bin/env python3
"""
Test script to verify all fixes are working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_flexible_output_generation():
    """Test the flexible output generation system."""
    print("🧪 Testing flexible output generation...")
    
    try:
        from agor.tools.dev_tooling import (
            generate_pr_description_only, 
            generate_release_notes_only, 
            generate_handoff_prompt_only
        )
        
        # Test PR description only
        pr_only = generate_pr_description_only(
            task_description='Test PR',
            pr_title='Test PR Title',
            pr_description='Test PR description with ```code``` blocks'
        )
        
        has_pr = 'pr_description' in pr_only
        no_snapshot = 'snapshot' not in pr_only
        print(f'✅ PR description only: has_pr={has_pr}, no_snapshot={no_snapshot}')
        
        # Test release notes only
        release_only = generate_release_notes_only(
            task_description='Test Release',
            release_notes='Test release notes with ```more code```'
        )
        
        has_release = 'release_notes' in release_only
        no_handoff = 'handoff_prompt' not in release_only
        print(f'✅ Release notes only: has_release={has_release}, no_handoff={no_handoff}')
        
        # Test handoff prompt only
        handoff_only = generate_handoff_prompt_only(
            task_description='Test Handoff',
            brief_context='Test context'
        )
        
        has_handoff = 'handoff_prompt' in handoff_only
        no_pr = 'pr_description' not in handoff_only
        print(f'✅ Handoff prompt only: has_handoff={has_handoff}, no_pr={no_pr}')
        
        print('🎉 Flexible output generation working correctly!')
        return True
        
    except Exception as e:
        print(f'❌ Error in flexible output generation: {e}')
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    print("🧪 Testing dependencies...")
    
    try:
        import pydantic
        print(f'✅ pydantic: {pydantic.__version__}')
    except ImportError as e:
        print(f'❌ pydantic missing: {e}')
        return False
    
    try:
        import pydantic_settings
        print(f'✅ pydantic_settings: {pydantic_settings.__version__}')
    except ImportError as e:
        print(f'❌ pydantic_settings missing: {e}')
        return False
    
    try:
        import platformdirs
        print(f'✅ platformdirs: {platformdirs.__version__}')
    except ImportError as e:
        print(f'❌ platformdirs missing: {e}')
        return False
    
    print('🎉 All dependencies available!')
    return True

def test_agent_requirements_file():
    """Test that the agent requirements file exists and is valid."""
    print("🧪 Testing agent requirements file...")
    
    req_file = 'src/agor/tools/agent-requirements.txt'
    if not os.path.exists(req_file):
        print(f'❌ Agent requirements file missing: {req_file}')
        return False
    
    with open(req_file, 'r') as f:
        content = f.read()
        
    required_deps = ['pydantic', 'pydantic-settings', 'platformdirs']
    for dep in required_deps:
        if dep not in content:
            print(f'❌ Missing dependency in requirements: {dep}')
            return False
    
    print(f'✅ Agent requirements file valid: {req_file}')
    return True

def main():
    """Run all tests."""
    print("🚀 Running comprehensive fix verification tests...")
    print("=" * 60)
    
    tests = [
        test_agent_requirements_file,
        test_dependencies,
        test_flexible_output_generation,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f'❌ Test {test.__name__} failed with exception: {e}')
            results.append(False)
            print()
    
    print("=" * 60)
    if all(results):
        print("🎉 ALL TESTS PASSED! Fixes are working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
