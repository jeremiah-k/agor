# 📦 Bundle Mode Guide

**Bundle Mode** is AGOR's upload-based workflow for AI platforms that work with file uploads. This guide covers setup, platform-specific optimizations, and troubleshooting for all supported platforms.

## 🎯 Quick Start

```bash
# Install AGOR
pipx install agor

# Bundle for your platform
agor bundle /path/to/your/project -f zip    # Google AI Studio
agor bundle /path/to/your/project           # ChatGPT (.tar.gz)
```

## 🤖 Platform-Specific Setup

### Google AI Studio

**Best Model**: **Gemini 2.5 Pro** - Latest flagship model with advanced reasoning

**Setup Steps**:

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create new chat with **Gemini 2.5 Pro**
3. **⚠️ CRITICAL: Enable Function Calling** in model settings
4. **Enable Code Execution** (if available in interface)
5. Upload your `.zip` bundle
6. Paste the generated initialization prompt

**Bundle Format**: `.zip` (optimized for Google AI Studio)

```bash
agor bundle /path/to/your/project -f zip
```

**Key Features**:

- ✅ **Function Calling** - Essential for real git command execution
- ✅ **Code Execution** - Python code generation and execution
- ✅ **Pro model access** - Access to advanced Gemini models
- ✅ **Large file uploads** - Handles substantial project bundles

**Common Issues & Solutions**:

**Git commands being simulated instead of executed**:

```
Remind the AI: "You have a real, functional git binary at /tmp/agor_tools/git.
Please make it executable with 'chmod 755 /tmp/agor_tools/git' and use it
directly. Do not simulate commands - execute them for real."
```

**Function Calling not working**:

- Ensure the toggle is enabled in model settings
- Look for "Function Calling" or "Tools" in the interface
- Without this, AGOR cannot execute real commands

### ChatGPT (Subscription Required)

**Best Model**: **GPT-4o** - Latest flagship model with multimodal capabilities

**Setup Steps**:

1. Open [ChatGPT](https://chat.openai.com/) (requires Plus/Pro subscription)
2. Start new chat with **GPT-4o**
3. Upload your `.tar.gz` bundle
4. Paste the generated initialization prompt

**Bundle Format**: `.tar.gz` (standard compression)

```bash
agor bundle /path/to/your/project
```

**Key Features**:

- ✅ **Advanced reasoning** - Excellent for complex coordination tasks
- ✅ **File upload support** - Handles .tar.gz bundles well
- ✅ **Consistent performance** - Reliable execution of AGOR protocols
- ⚠️ **Subscription required** - ChatGPT Plus or Pro needed

**Subscription Requirements**:

- **ChatGPT Plus** ($20/month) - Access to GPT-4o
- **ChatGPT Pro** ($200/month) - Higher usage limits, priority access

### Other Platforms

**Claude (Anthropic)**:

- Use `.tar.gz` format
- Good reasoning capabilities but limited file upload
- May require manual extraction steps

**Local AI Models**:

- Use `.tar.gz` format
- Ensure model supports function calling
- Performance varies by model size and capabilities

## ⚙️ Git Configuration

AGOR includes built-in git configuration management to streamline development workflows:

### Environment Variable Import

```bash
# Set environment variables (recommended)
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"
# or
export GIT_USER_NAME="Your Name"
export GIT_USER_EMAIL="your@email.com"

# Import from environment
agor git-config --import-env
```

### Manual Configuration

```bash
# Set git configuration manually
agor git-config --name "Your Name" --email "your@email.com"

# Set globally (affects all repositories)
agor git-config --name "Your Name" --email "your@email.com" --global
```

### View Configuration

```bash
# Show current git configuration and environment variables
agor git-config --show
```

### Benefits

- ✅ **Consistent attribution** across all development work
- ✅ **Environment integration** with your existing development setup
- ✅ **Repository awareness** shows current branch and repository info
- ✅ **Flexible scope** configure per-repository or globally

## 🔧 Bundle Options

### Standard Bundle

```bash
agor bundle /path/to/your/project
```

- Includes git history and portable git binary
- Standard compression (.tar.gz)
- Compatible with most platforms

### Google AI Studio Optimized

```bash
agor bundle /path/to/your/project -f zip
```

- ZIP format for better Google AI Studio compatibility
- Optimized file structure
- Recommended for Google AI Studio

### Branch-Specific Bundling

```bash
# Main branch only
agor bundle /path/to/your/project -m

# Specific branches
agor bundle /path/to/your/project -b feature1,feature2

# All branches (default)
agor bundle /path/to/your/project
```

## 🧠 The Advantage of Full Codebase Context

When you create a bundle with AGOR, you're providing the AI with a remarkably comprehensive understanding of your project. This isn't just about the current state of your files; by default, AGOR includes:

- **The Entire Repository**: Every file and directory tracked by Git is included.
- **Full Git History**: The AI has access to the complete history of changes, including all branches, commits, and tags.
- **Portable Git Tools**: The bundle contains a functional Git binary, allowing the AI to run actual Git commands for deep analysis (e.g., `git log`, `git diff <commit>`, `git blame`).

**Why is this a significant advantage?**

Many AI coding tools or integrations operate with a limited view of your codebase—perhaps only open files, a specific directory, or no history at all. AGOR's approach offers superior context:

- **Holistic Understanding**: The AI can understand how different parts of your project connect, how features have evolved, and why certain design decisions were made by examining the commit history.
- **Better Analysis & Debugging**: When analyzing code or debugging issues, the AI can trace changes across branches, identify when a bug might have been introduced, or understand the context of a particular line of code by looking at its history (`git blame`).
- **More Accurate Answers**: When you ask questions about the codebase, the AI can provide much more insightful and accurate answers because it's not guessing based on a partial view.
- **Effective Large-Scale Changes**: For refactoring or implementing features that span multiple files or modules, the AI can operate with a much clearer picture of potential impacts.

This comprehensive context empowers the AI to act more like an experienced developer with deep project knowledge, leading to higher quality assistance, more accurate code generation, and more insightful analysis. While bundling all branches is the default and provides maximum context, AGOR also offers [Branch-Specific Bundling](#branch-specific-bundling) options if you need to create smaller, more focused bundles.

## 🎭 Role Selection

After uploading and initializing, AGOR will prompt for role selection:

### 📋 PROJECT COORDINATOR

**Best for**: Planning, strategy, team coordination

- Strategic planning and project breakdown
- Multi-agent strategy selection (`ss`, `pd`, `pl`, `sw`)
- Team design and workflow orchestration (`ct`, `tm`)

### 🔍 Worker Agent

**Best for**: Code analysis, implementation, solo work

- Comprehensive codebase analysis and exploration
- Code exploration and investigation
- Implementation and development work

### 👥 AGENT WORKER

**Best for**: Receiving snapshots, collaborative work

- Task execution from snapshots (`task`, `complete`)
- Team coordination (`status`, `sync`)
- Communication with other agents (`log`, `msg`)

## 🔥 Essential Hotkeys

**Universal**:

- `init` - Initialize/re-initialize role
- `status` - Check current state
- `meta` - Provide feedback on AGOR

**Analysis**:

- `a` - Analyze codebase
- `f` - Show full files
- `co` - Changes only

**Strategy & Planning**:

- `ss` - Strategy selection
- `ct` - Create team
- `bp` - Break down project

**Memory**:

- `mem-add` - Add memory entry
- `mem-search` - Search memories

## 🆘 Troubleshooting

### Bundle Upload Issues

**Google AI Studio**:

- Use `.zip` format only
- Ensure Function Calling is enabled
- Re-upload if extraction seems incomplete

**ChatGPT**:

- Use `.tar.gz` format
- Ensure you have active subscription
- Try smaller bundles if upload fails

### Git Binary Issues

**Commands being simulated**:

```
Tell the AI: "Make the git binary executable and use it directly:
chmod 755 /tmp/agor_tools/git
/tmp/agor_tools/git status"
```

**Binary not found**:

- Verify bundle was properly extracted
- Check `/tmp/agor_tools/` directory exists
- Re-upload bundle if necessary

### Performance Issues

**Slow responses**:

- Use smaller bundles with `-m` flag (main branch only)
- Consider excluding large files or directories
- Try different model if available

**Memory issues**:

- Use memory synchronization system for persistent memory
- Clear conversation and re-initialize if needed
- Break large tasks into smaller chunks

## 💡 Pro Tips

### Optimize Bundle Size

```bash
# Exclude unnecessary files
echo "node_modules/\n*.log\n.env" > .agorignore
agor bundle /path/to/your/project
```

### Platform Switching

- Keep bundles for different platforms ready
- Use consistent project structure across platforms
- Document platform-specific quirks in project notes

### Multi-Platform Workflows

1. **Plan** on Google AI Studio (free, good for strategy)
2. **Implement** on ChatGPT (subscription, excellent execution)
3. **Review** on either platform based on preference

## 🔄 What's Next?

After successful bundle setup:

1. **Explore [Multi-Agent Strategies](strategies.md)** - Learn coordination patterns
2. **Master [Agent Snapshots](snapshots.md)** - Seamless agent transitions
3. **Read [Complete AI Protocol](../src/agor/tools/README_ai.md)** - Full capabilities

---

**Ready to bundle?** Choose your platform, create your bundle, and experience the power of coordinated AI development! 🚀
