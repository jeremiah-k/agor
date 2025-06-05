# AugmentCode Local Agent Detection and Integration

## Environment Detection

When running in the AugmentCode Local Agent environment (VS Code extension), agents have access to special capabilities:

### Available Features

- **Augment Memories**: Persistent memory system across sessions
- **User Guidelines**: User-defined guidelines for consistent behavior
- **Workspace Context**: Direct access to project files and AGOR documentation
- **Local File System**: Full file system access without upload limitations

### Detection Methods

#### Method 1: Environment Variables

```python
import os

def is_augmentcode_local():
    """Detect if running in AugmentCode Local Agent environment"""
    # Check for AugmentCode-specific environment variables
    augment_indicators = [
        'AUGMENT_WORKSPACE',
        'AUGMENT_LOCAL_MODE',
        'VSCODE_AUGMENT_EXTENSION'
    ]

    return any(os.getenv(var) for var in augment_indicators)
```

#### Method 2: Workspace Context

```python
def has_augment_workspace_context():
    """Check if AGOR is available in workspace context"""
    import os

    # Check if AGOR tools are directly accessible by looking for README_ai.md
    try:
        # Check for README_ai.md in the expected directory
        readme_path = os.path.join('src', 'agor', 'tools', 'README_ai.md')
        return os.path.exists(readme_path)
    except Exception:
        return False
```

#### Method 3: User Guidelines Access

```python
def has_user_guidelines_access():
    """Check if User Guidelines are accessible"""
    # This would be implementation-specific to AugmentCode
    # Placeholder for actual detection logic
    return False  # To be implemented based on AugmentCode API
```

## Integration Instructions

### For AugmentCode Local Agent Users

When setting up AGOR with AugmentCode Local Agent:

1. **Add AGOR to Workspace Sources**

   - Clone AGOR repository locally
   - Add AGOR directory to AugmentCode workspace sources
   - Ensure `src/agor/tools/` is accessible

2. **Configure User Guidelines**

   **Recommended**: Use the comprehensive AGOR User Guidelines from the repository root:
   **[docs/augment_user_guidelines.md](../../../docs/augment_user_guidelines.md)**

   This provides complete AGOR integration with proper protocols, snapshot requirements, and coordination workflows.

   **Quick Setup**: Copy the entire content of augment_user_guidelines.md into your AugmentCode User Guidelines for full AGOR functionality.

3. **Optional Workspace Guidelines**
   Create `.augment-guidelines` in project root:
   ```
   - Use AGOR framework for development coordination when available in workspace sources
   - Follow AGOR role-based workflows for structured development
   - Utilize AGOR hotkeys and snapshot system for context management
   - Reference AGOR documentation for best practices and coordination protocols
   ```

### For AI Agents

When an agent detects AugmentCode Local Agent environment:

1. **Enhanced Initialization**

   - Access User Guidelines for project-specific preferences
   - Leverage Augment Memories for session continuity
   - Use workspace context for immediate AGOR access

2. **Modified Workflow**

   - No need to clone AGOR repository (already in workspace)
   - Direct access to all AGOR documentation
   - Enhanced memory persistence through Augment system

3. **Integration Benefits**
   - Seamless AGOR integration with existing VS Code workflow
   - Persistent guidelines ensure consistent AGOR usage
   - No file upload limits or token efficiency concerns

## Implementation Notes

### Environment-Specific Behavior

```python
def initialize_agor_environment():
    """Initialize AGOR based on detected environment"""

    if is_augmentcode_local():
        # AugmentCode Local Agent environment
        return {
            'mode': 'local_integration',
            'memory_system': 'augment_memories',
            'guidelines_access': has_user_guidelines_access(),
            'workspace_context': has_augment_workspace_context(),
            'setup_required': False
        }
    else:
        # Standard environment (Bundle/Standalone)
        return {
            'mode': 'standard',
            'memory_system': 'agor_memory_sync',
            'guidelines_access': has_user_guidelines_access(),
            'workspace_context': has_augment_workspace_context(),
            'setup_required': True
        }
```

### Adaptive Instructions

Based on environment detection, provide different initialization instructions:

- **AugmentCode Local**: Reference workspace sources, use User Guidelines
- **Standard Mode**: Follow normal AGOR initialization (README_ai.md)

## Future Enhancements

### Planned Features

- Automatic AGOR activation when AugmentCode Local Agent is detected
- Integration with AugmentCode memory system
- Seamless handoff between AugmentCode and AGOR coordination
- Enhanced workspace-aware file operations

### API Integration

- Direct integration with AugmentCode User Guidelines API
- Augment Memories synchronization with AGOR memory system
- Workspace context optimization for AGOR tools

---

**Note**: This detection system ensures AGOR works optimally in the AugmentCode Local Agent environment while maintaining compatibility with all other deployment modes.
