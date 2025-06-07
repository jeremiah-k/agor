#!/usr/bin/env python3
"""Simple test for AGOR memory system."""

import sys
sys.path.insert(0, 'src')

def main():
    print("🧪 Simple Memory System Test")
    print("=" * 40)
    
    try:
        # Test basic memory commit
        print("1️⃣ Testing memory commit...")
        from agor.tools.dev_tooling import auto_commit_memory
        
        test_content = """
# Simple Memory Test

This is a test of the AGOR memory system.
The content should be committed to a memory branch, not the working branch.
"""
        
        result = auto_commit_memory(
            content=test_content,
            memory_type="simple_test",
            agent_id="test"
        )
        
        if result:
            print("✅ Memory commit successful")
        else:
            print("❌ Memory commit failed")
            return False
        
        # Test session end prompt
        print("\n2️⃣ Testing session end prompt...")
        from agor.tools.dev_tooling import generate_mandatory_session_end_prompt
        
        session_result = generate_mandatory_session_end_prompt(
            work_completed=["Tested memory system"],
            current_status="Test complete",
            next_agent_instructions=["Review test results"],
            critical_context="Simple test completed successfully",
            files_modified=["simple_memory_test.py"]
        )
        
        if session_result and session_result.get('success'):
            print("✅ Session end prompt generated")
            prompt = session_result.get('session_end_prompt', '')
            print(f"📄 Prompt length: {len(prompt)} characters")
        else:
            print("❌ Session end prompt failed")
            if session_result and 'error' in session_result:
                print(f"Error: {session_result['error']}")
            return False
        
        # Check git status
        print("\n3️⃣ Checking git status...")
        from agor.tools.git_operations import run_git_command
        
        success, status = run_git_command(["status", "--porcelain"])
        if success:
            print(f"📋 Git status: {status.strip() if status.strip() else 'Clean'}")
        else:
            print(f"❌ Git status check failed: {status}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
