#!/usr/bin/env python3
"""
Programmatic refactor script to change "dev tools" -> "dev tools" terminology
across the AGOR codebase.
"""

import os
import re
from pathlib import Path

def refactor_terminology(directory='.'):
    """Programmatically refactor dev_tools -> dev_tools terminology"""
    
    # Define replacement patterns
    replacements = [
        # Function names and symbols
        (r'test_development_tools', 'test_development_tools'),
        (r'test_all_tools', 'test_all_tools'),
        (r'dev_tools', 'dev_tools'),
        (r'DevTools', 'DevTools'),
        
        # User-facing strings (case-sensitive)
        (r'development tools', 'development tools'),
        (r'Development Tools', 'Development Tools'),
        (r'dev tools', 'dev tools'),
        (r'Dev Tools', 'Dev Tools'),
        (r'AGOR Development Tools Functions Reference', 'AGOR Development Tools Functions Reference'),
        (r'All available AGOR development tools functions', 'All available AGOR development tools functions'),
        (r'development tools components', 'development tools components'),
        (r'Test development tools', 'Test development tools'),
        (r'Test all development tools', 'Test all development tools'),
        (r'Testing AGOR Development Tools', 'Testing AGOR Development Tools'),
        (r'AGOR Development Tools', 'AGOR Development Tools'),
        (r'development tools functions', 'development tools functions'),
        (r'all development tools', 'all development tools'),
    ]
    
    # File extensions to process
    extensions = {'.py', '.md', '.txt', '.rst'}
    
    # Track changes
    files_changed = []
    total_replacements = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'__pycache__', 'node_modules'}]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_replacements = 0
                    
                    # Apply all replacements
                    for pattern, replacement in replacements:
                        matches = len(re.findall(pattern, content))
                        content = re.sub(pattern, replacement, content)
                        file_replacements += matches
                    
                    # Write back if changed
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_changed.append(str(file_path))
                        total_replacements += file_replacements
                        print(f'✅ Updated {file_path} ({file_replacements} replacements)')
                
                except Exception as e:
                    print(f'❌ Error processing {file_path}: {e}')
    
    print(f'\n📊 Refactor Summary:')
    print(f'Files changed: {len(files_changed)}')
    print(f'Total replacements: {total_replacements}')
    
    return files_changed, total_replacements

if __name__ == '__main__':
    print('🔄 Starting programmatic terminology refactor...')
    files_changed, total_replacements = refactor_terminology()
    
    if total_replacements > 0:
        print(f'\n🎯 Refactor completed successfully!')
        print(f'Next steps:')
        print(f'1. Review changes: git diff')
        print(f'2. Test functionality: python -m pytest')
        print(f'3. Commit changes: git commit -am "refactor: rename all dev_tools → dev_tools symbols and references"')
    else:
        print('\n✅ No changes needed - terminology already consistent!')
