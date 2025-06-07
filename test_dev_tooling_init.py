# Test and initialize dev tooling
import sys
sys.path.insert(0, 'src')

print("🧪 Testing AGOR Development Tooling...")

try:
    from agor.tools.dev_tooling import test_tooling, get_timestamp, DevTooling
    
    # Initialize dev tooling
    dev_tools = DevTooling()
    
    # Test tooling functionality
    print("Testing dev tooling functions...")
    test_result = test_tooling()
    
    # Get current timestamp
    timestamp = get_timestamp()
    print(f"Session started at: {timestamp}")
    
    # Test git operations
    success, output = dev_tools._run_git_command(["status"])
    if success:
        print("✅ Git operations working")
        print(f"Git status: {output[:100]}...")
    else:
        print(f"❌ Git issue: {output}")
    
    print("✅ Dev tooling initialization complete")

    # Create initial memory entry
    from agor.tools.dev_tooling import auto_commit_memory

    memory_content = """
# AGOR Refactoring Project - Session Start

## Project Overview
Working on comprehensive AGOR improvements based on review findings:

### High Priority Issues:
1. **Git Safety**: Implement safe_git_push function (no force push without safeguards)
2. **Dev Tooling Modularization**: Break down 2446-line dev_tooling.py into focused modules
3. **Memory Branch Architecture**: Change from orphan branches to 1-commit-behind-HEAD
4. **Role System**: Update Project Coordinator role, simplify to 2 roles (Worker Agent + PC)

### Current Status:
- ✅ Dev tooling initialized and tested
- ✅ Review work file deleted as requested
- 🔄 Starting Phase 1: Git safety implementation

### Next Steps:
1. Implement safe_git_push function with upstream checking
2. Update quick_commit_push to use safe push
3. Fix memory branch creation logic
4. Update role documentation

## Technical Notes:
- Using existing dev tooling throughout
- Will create snapshots and memories frequently
- All prompt outputs must use detick method for proper codeblock rendering
- Working as Agent Worker role until instructed otherwise
"""

    auto_commit_memory(memory_content, "project_start", "refactor_agent")
    print("💾 Created initial memory entry")

    # Commit the cleanup
    from agor.tools.dev_tooling import quick_commit_push
    quick_commit_push("🧹 Delete review work file and initialize refactoring session", "🧹")
    print("✅ Committed cleanup and initialization")

except Exception as e:
    print(f"❌ Dev tooling initialization failed: {e}")
    import traceback
    traceback.print_exc()
