# 🛠️ AGOR Development Guide

**For AI agents and developers working on AGOR itself**

This guide ensures consistency, quality, and proper protocol management when developing AGOR. Use this checklist for all changes to maintain the integrity of the multi-agent coordination platform.

## 🔍 Pre-Development Checklist

### Understanding the Change

- [ ] **Identify impact scope**: Core protocol, documentation, tooling, or platform support?
- [ ] **Check existing issues**: Review GitHub issues for related work or conflicts
- [ ] **Understand user impact**: How will this affect existing AGOR users?
- [ ] **Review related documentation**: Ensure you understand current behavior

### Environment Setup

- [ ] **Configure git identity**: Use `agor git-config --import-env` or set manually
- [ ] **Verify attribution**: Ensure commits will be attributed correctly
- [ ] **Check environment variables**: Set GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL if using --import-env

### Branch Management

- [ ] **Create feature branch**: Use pattern `work-X.Y.Z-N` (e.g., `work-0.2.1-5`)
- [ ] **Base on latest main**: Always start from up-to-date main branch
- [ ] **Single responsibility**: One logical change per branch/PR

## 📋 Development Checklist

### Version Management

- [ ] **Update version numbers** if making protocol changes:
  - `src/agor/__init__.py` - Fallback version
  - `pyproject.toml` - Package version
  - Documentation references to version numbers
- [ ] **Protocol changes require version bump**: Any changes to hotkeys, coordination protocols, or agent behavior
- [ ] **Backward compatibility**: Consider impact on existing bundles and workflows

### Code Quality

- [ ] **Follow existing patterns**: Match coding style and architecture
- [ ] **Add type hints**: Use Python type annotations consistently
- [ ] **Update docstrings**: Document new functions and classes
- [ ] **Error handling**: Add appropriate error messages to `constants.py`
- [ ] **Logging**: Use structured logging with `structlog` for new features

### Documentation Updates

- [ ] **Update README.md** if adding new features or changing core functionality
- [ ] **Update relevant guides**:
  - `docs/bundle-mode.md` for platform changes
  - `docs/quick-start.md` for workflow changes
  - `src/agor/tools/README_ai.md` for protocol changes
- [ ] **Update documentation index** (`docs/index.md`) with new files or major changes
- [ ] **Check for broken links** after moving or renaming files
- [ ] **Update line counts** in documentation index if files change significantly

### Protocol and Hotkey Changes

- [ ] **Update hotkey documentation** in `README_ai.md` if adding/changing hotkeys
- [ ] **Update role-specific menus** for each role (PROJECT COORDINATOR, ANALYST/SOLO DEV, AGENT WORKER)
- [ ] **Test hotkey conflicts**: Ensure new hotkeys don't conflict with existing ones
- [ ] **Update agent prompt templates** if changing coordination protocols
- [ ] **Consider multi-agent impact**: How do changes affect agent-to-agent communication?

### File and Tool Management

- [ ] **Update MANIFEST.in** if adding new files to be included in packages
- [ ] **Update .trunk/trunk.yaml** if adding files that need linter exceptions
- [ ] **Check tool dependencies**: Ensure new tools are properly bundled
- [ ] **Test bundle creation**: Verify bundles include all necessary files
- [ ] **Validate git binary inclusion**: Ensure portable git binary is properly included

### Platform Compatibility

- [ ] **Test on target platforms**:
  - Google AI Studio (Gemini 2.5 Pro, Function Calling)
  - ChatGPT (GPT-4o, file upload)
  - Agent Mode (git-capable agents)
- [ ] **Verify bundle formats**: Test .zip and .tar.gz creation
- [ ] **Check platform-specific instructions** in bundle-mode.md
- [ ] **Test SQLite memory features** if applicable

## 🧪 Testing Checklist

### Functional Testing

- [ ] **Bundle creation**: Test `agor bundle` with various options
- [ ] **Bundle extraction**: Verify bundles extract properly on target platforms
- [ ] **Git binary functionality**: Ensure portable git works in bundle environment
- [ ] **Hotkey functionality**: Test new or modified hotkeys
- [ ] **Role initialization**: Test all three roles work properly
- [ ] **Memory systems**: Test both markdown and SQLite memory (if applicable)

### Integration Testing

- [ ] **Multi-agent workflows**: Test coordination between agents
- [ ] **Handoff procedures**: Verify handoff generation and reception
- [ ] **Communication protocols**: Test .agor/ directory structure and files
- [ ] **Cross-platform compatibility**: Test on different operating systems

### Edge Case Testing

- [ ] **Large repositories**: Test with substantial codebases
- [ ] **Special characters**: Test with non-ASCII filenames and content
- [ ] **Network issues**: Test bundle creation with poor connectivity
- [ ] **Permission issues**: Test in restricted environments

## 📝 Documentation Standards

### Writing Guidelines

- [ ] **Use consistent emoji**: Follow existing patterns (🎼 for AGOR, 📦 for bundles, etc.)
- [ ] **Token efficiency**: Write for AI consumption - clear, concise, scannable
- [ ] **Code examples**: Use proper markdown formatting with language tags
- [ ] **Platform specificity**: Clearly mark platform-specific instructions
- [ ] **Version references**: Use current version numbers consistently

### Content Requirements

- [ ] **Purpose statement**: Every doc should clearly state its purpose
- [ ] **Prerequisites**: List what users need before following instructions
- [ ] **Step-by-step procedures**: Break complex tasks into numbered steps
- [ ] **Troubleshooting sections**: Include common issues and solutions
- [ ] **Cross-references**: Link to related documentation appropriately

## 🔄 Pre-Commit Checklist

### Code Review

- [ ] **Self-review**: Read through all changes as if reviewing someone else's code
- [ ] **Check imports**: Ensure all imports are necessary and properly organized
- [ ] **Remove debug code**: Clean up any temporary debugging statements
- [ ] **Verify constants**: Use constants from `constants.py` instead of magic strings

### Attribution and Licensing

- [ ] **Maintain AgentGrunt attribution**: Keep proper attribution in appropriate files
- [ ] **License compatibility**: Ensure new dependencies are MIT-compatible
- [ ] **Copyright notices**: Add appropriate copyright for substantial new files

### Final Validation

- [ ] **Run linters**: Ensure trunk checks pass
- [ ] **Test installation**: Verify `pip install -e .` works
- [ ] **Test CLI**: Verify `agor --version` and basic commands work
- [ ] **Check bundle creation**: Create a test bundle to verify functionality

## 📤 Commit and PR Guidelines

### Commit Messages

- [ ] **Use conventional format**: `🔧 Fix bundle creation for Windows paths`
- [ ] **Include scope**: Specify what area is affected
- [ ] **Explain why**: Include reasoning for non-obvious changes
- [ ] **Reference issues**: Link to GitHub issues when applicable

### Pull Request Requirements

- [ ] **Descriptive title**: Clearly summarize the change
- [ ] **Comprehensive description**: Use the PR template format
- [ ] **Breaking changes**: Clearly mark any breaking changes
- [ ] **Testing notes**: Explain how the change was tested
- [ ] **Documentation updates**: List all documentation changes made

## 🚨 Critical Checkpoints

### Protocol Changes (Require Version Bump)

- [ ] **Hotkey additions/changes**: Any modification to the hotkey system
- [ ] **Role behavior changes**: Modifications to role-specific functionality
- [ ] **Communication format changes**: Changes to .agor/ file formats
- [ ] **Bundle structure changes**: Modifications to bundle contents or layout
- [ ] **Memory system changes**: Changes to memory management or storage

### Backward Compatibility Breaks

- [ ] **Document breaking changes**: Clearly explain what breaks and why
- [ ] **Provide migration path**: Explain how users can adapt
- [ ] **Update version appropriately**: Major version for breaking changes
- [ ] **Update compatibility notes**: Modify handoff compatibility guidelines

## 🎯 Quality Gates

### Before Merging

- [ ] **All tests pass**: Functional and integration tests complete
- [ ] **Documentation complete**: All relevant docs updated
- [ ] **Version consistency**: All version references match
- [ ] **No broken links**: All documentation links work
- [ ] **Bundle testing**: Created and tested bundle on target platform

### Post-Merge Validation

- [ ] **PyPI compatibility**: Ensure package can be built and installed
- [ ] **User workflow testing**: Test complete user journey
- [ ] **Agent feedback**: Monitor for issues from AI agents using AGOR
- [ ] **Performance impact**: Verify no significant performance regressions

---

## 🤖 For AI Agents

When working on AGOR, you're improving the platform you're using. This creates a unique feedback loop where your development experience directly informs the quality of the tool.

**Remember**:

- Use the `meta` hotkey to provide feedback about the development process itself
- Document any pain points or inefficiencies you encounter
- Suggest improvements to this development guide based on your experience
- Test changes from the perspective of other AI agents who will use AGOR

**Your development work on AGOR helps all AI agents coordinate better!** 🎼

---

_This guide evolves with AGOR. Suggest improvements through the `meta` hotkey or GitHub issues._
