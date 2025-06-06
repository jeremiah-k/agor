#!/usr/bin/env python3
"""Fix remote agent work order using ONLY our dev tooling with proper backtick processing."""

import sys
sys.path.insert(0, 'src')

from agor.tools.dev_tooling import HandoffRequest, generate_handoff_prompt_only

def main():
    print('🔧 Fixing remote agent work order using ONLY our dev tooling...')
    
    # Create proper handoff request using our dev tooling
    outputs = generate_handoff_prompt_only(
        task_description='AGOR Hotkey System Improvement & Remote Agent Coordination Testing',
        work_completed=[
            'Enhanced AGOR Agent Handoff System - Production Ready (v0.4.2+)',
            'Fixed all critical branch safety issues with safe cross-branch commit',
            'Created flexible output generation system with convenience functions',
            'Added agent-requirements.txt with proper dependency management',
            'Updated usage guide with streamlined deployment instructions',
            'Established Project Coordinator mode for strategic oversight',
            'Created initial work order (needs fixing due to backtick processing failure)'
        ],
        next_steps=[
            'CRITICAL: Fix work order using proper dev tooling with backtick processing',
            'Improve AGOR hotkey system - replace placeholder hotkeys with useful dev tooling integration',
            'Hook up hotkeys to dev tooling functions (snapshot generation, handoff prompts, etc.)',
            'Add role/strategy display and change hotkeys',
            'Test remote agent coordination workflow with snapshot loading',
            'Validate back-and-forth communication via properly processed snapshots'
        ],
        brief_context='CRITICAL FIX: Remote agent work order failed to use backtick processing tooling. Must fix using ONLY our dev tooling to ensure proper single codeblock format for agent coordination.'
    )
    
    if outputs['success']:
        print('✅ SUCCESS: Proper work order generated using our dev tooling!')
        print()
        print('📋 CORRECTED REMOTE AGENT WORK ORDER (Ready for Single Codeblock):')
        print('=' * 80)
        print(outputs['handoff_prompt'])
        print()
        print('🎯 This output is properly processed and ready for copy-paste!')
        return 0
    else:
        print(f'❌ Error: {outputs["error"]}')
        return 1

if __name__ == "__main__":
    sys.exit(main())
