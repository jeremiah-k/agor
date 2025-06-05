#!/usr/bin/env python3
"""Test script for prompt preparation functionality."""

import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import prepare_prompt_content

def test_prompt_preparation():
    """Test the prompt preparation function directly."""
    print('Testing prompt preparation function...')

    # Test with a simple code example
    test_content = '''Here is some code:

```python
import sys
print('hello')
```

And more text.'''

    print('Original content:')
    print(repr(test_content))
    print()

    prepared = prepare_prompt_content(test_content)

    print('Prepared content:')
    print(repr(prepared))
    print()

    print('Rendered prepared content:')
    print(prepared)
    print()

    print('Verification:')
    print(f'Original contains triple backticks: {"```" in test_content}')
    print(f'Prepared contains triple backticks: {"```" in prepared}')
    print(f'Prepared contains double backticks: {"``" in prepared}')

    if "```" not in prepared and "``" in prepared:
        print('✅ Prompt preparation working correctly!')
        return True
    else:
        print('❌ Prompt preparation not working as expected')
        return False

if __name__ == "__main__":
    test_prompt_preparation()
