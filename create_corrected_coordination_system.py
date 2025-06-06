#!/usr/bin/env python3
"""Create corrected coordination system with mandatory session end prompts."""

import sys
sys.path.insert(0, 'src')

from agor.tools.dev_tooling import generate_handoff_prompt_only

def main():
    print('🔧 Creating corrected coordination system...')
    
    # Generate corrected work order with DIRECT instructions
    outputs = generate_handoff_prompt_only(
        task_description='CORRECTED: Agent Coordination System with Mandatory Session End Prompts',
        work_completed=[
            'IDENTIFIED CRITICAL COORDINATION FAILURES:',
            '❌ Remote agent completed work but provided no return prompt',
            '❌ Work order gave confusing "tell your remote agent" instructions',
            '❌ No automatic coordination at session end',
            '❌ Agents celebrating instead of generating coordination output',
            '',
            'IMPLEMENTED FIXES:',
            '✅ Added generate_mandatory_session_end_prompt() function',
            '✅ Added session-end hotkey to AGOR instructions',
            '✅ Created mandatory coordination protocol',
            '✅ Fixed work order language to be direct instructions'
        ],
        next_steps=[
            'CRITICAL: Test new mandatory session end prompt system',
            'VALIDATE: Ensure agents automatically generate return prompts',
            'IMPLEMENT: Make session end prompts truly mandatory',
            'TEST: End-to-end coordination workflow',
            'CONTINUE: Productive development work with proper coordination'
        ],
        brief_context='Fixed critical coordination failures. Agents must now generate mandatory session end prompts using our dev tooling. Work orders must be direct instructions, not meta-instructions about telling other agents.'
    )
    
    if outputs['success']:
        print('✅ SUCCESS: Corrected coordination system generated!')
        print()
        print('📋 CORRECTED AGENT WORK ORDER (Direct Instructions):')
        print('=' * 80)
        print(outputs['handoff_prompt'])
        print()
        print('🎯 This gives DIRECT instructions to the agent!')
        return 0
    else:
        print(f'❌ Error: {outputs["error"]}')
        return 1

if __name__ == "__main__":
    sys.exit(main())
