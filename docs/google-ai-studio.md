# 🆓 Google AI Studio Guide

Google AI Studio provides a **free way** to use AGOR with Pro models - no subscription required! This guide will get you set up and running smoothly.

## 🎯 Why Google AI Studio?

- **✅ Free access** to powerful Pro models
- **✅ Function Calling support** (essential for AGOR)
- **✅ File upload capability** for bundles
- **✅ No subscription fees** or usage limits for basic use

## 🚀 Quick Setup

### Step 1: Prepare Your Bundle

```bash
# Install AGOR locally
pipx install agor

# Bundle your project (use .zip format for Google AI Studio)
agor bundle /path/to/your/project -f zip

# This creates: your-project-agor-bundle.zip
```

### Step 2: Google AI Studio Setup

1. **Visit [Google AI Studio](https://aistudio.google.com/)**
2. **Sign in** with your Google account
3. **Create a new chat**
4. **⚠️ CRITICAL: Enable Function Calling**
   - Look for "Function Calling" toggle in the model settings
   - **This must be enabled** for AGOR to work properly
   - Without this, the AI will simulate commands instead of executing them

### Step 3: Upload and Initialize

1. **Upload your .zip bundle** using the file attachment button
2. **Copy and paste the generated prompt** (AGOR creates this automatically)
3. **Select your role** when prompted:
   - **PROJECT COORDINATOR** - Strategic planning and team coordination
   - **ANALYST/SOLO DEV** - Deep codebase analysis and implementation
   - **AGENT WORKER** - Task execution and coordination handoffs

## 🔧 Critical Configuration

### Function Calling Must Be Enabled

Google AI Studio has a **Function Calling** toggle that **must be enabled** for AGOR to work. Here's why:

- **With Function Calling**: AI executes real git commands using the portable binary
- **Without Function Calling**: AI simulates commands and can't access your actual code

**If you see simulation behavior:**

```
# Simulating: git ls-files
# Simulating: git status
```

**Remind the AI:**

> "You have a real, functional git binary at `/tmp/agor_tools/git`. Please make it executable with `chmod 755 /tmp/agor_tools/git` and use it directly. Do not simulate commands - execute them for real."

## 🎼 Role Selection Guide

When AGOR initializes, it will ask you to choose a role. Here's how to decide:

### 📋 PROJECT COORDINATOR

**Choose this when:**

- Planning a new feature or project
- Coordinating multiple development tasks
- Designing team workflows
- Breaking down complex requirements

**You'll get:**

- Strategic planning tools
- Team coordination hotkeys
- Multi-agent strategy selection
- Workflow design capabilities

### 🔍 ANALYST/SOLO DEV

**Choose this when:**

- Analyzing existing code
- Implementing specific features
- Debugging issues
- Working solo on technical tasks

**You'll get:**

- Comprehensive codebase analysis
- Code exploration tools
- Implementation-focused hotkeys
- Technical deep-dive capabilities

### 🤖 AGENT WORKER

**Choose this when:**

- Following instructions from a coordinator
- Executing specific assigned tasks
- Working as part of a larger team
- Implementing predefined requirements

**You'll get:**

- Task execution tools
- Coordination communication
- Handoff procedures
- Status reporting capabilities

## 💡 Pro Tips for Google AI Studio

### Optimize Your Workflow

1. **Start with PROJECT COORDINATOR** for planning phases
2. **Switch to ANALYST/SOLO DEV** for implementation
3. **Use the `meta` hotkey** to provide feedback on AGOR itself

### Handle Common Issues

**If the AI simulates instead of executing:**

```
Please execute real commands. You have a functional git binary at /tmp/agor_tools/git.
Make it executable: chmod 755 /tmp/agor_tools/git
Then use it directly: /tmp/agor_tools/git status
```

**If git commands fail:**

```
First make the git binary executable:
chmod 755 /tmp/agor_tools/git

Then verify it works:
/tmp/agor_tools/git --version
```

**If you need to restart:**

- Upload a fresh bundle
- Re-paste the initialization prompt
- Select your role again

## 🎯 Best Practices

### Project Planning Workflow

1. **Upload bundle** with PROJECT COORDINATOR role
2. **Use `sp` (strategic plan)** to break down the project
3. **Use `ss` (strategy selection)** to choose coordination approach
4. **Use `ct` (create team)** to design agent roles

### Implementation Workflow

1. **Upload bundle** with ANALYST/SOLO DEV role
2. **Use `a` (analyze)** to understand the codebase
3. **Use code exploration tools** to investigate specific areas
4. **Use `f` (full files)** to examine implementation details

### Feedback Workflow

1. **Use `meta` hotkey** when you encounter issues or have suggestions
2. **Choose appropriate feedback path** based on your situation
3. **Provide specific, technical details** to help improve AGOR

## 🔄 Multi-Agent Coordination

Google AI Studio works great for **single-agent workflows**, but you can also coordinate **multiple AI instances**:

1. **Coordinator Instance**: Use PROJECT COORDINATOR role for planning
2. **Worker Instances**: Use AGENT WORKER role for implementation
3. **Share coordination files** (`.agor/agentconvo.md`) between instances
4. **Use handoff prompts** generated by the coordinator

## 🆘 Troubleshooting

### Common Issues

**"Function not found" errors**

- ✅ Ensure Function Calling is enabled in model settings

**Git commands being simulated**

- ✅ Remind AI about real git binary at `/tmp/agor_tools/git`
- ✅ Tell it to make binary executable first

**Bundle extraction fails**

- ✅ Use `.zip` format (not `.tar.gz`) for Google AI Studio
- ✅ Re-upload if extraction seems incomplete

**Role selection not working**

- ✅ Re-paste the initialization prompt
- ✅ Ensure the bundle was properly extracted

### Getting Help

- **Check [Troubleshooting Guide](troubleshooting.md)** for detailed solutions
- **Use the `meta` hotkey** to report issues directly
- **Visit [GitHub Issues](https://github.com/jeremiah-k/agor/issues)** for community support

---

**Ready to start coordinating with Google AI Studio?** Upload your first bundle and experience the power of free multi-agent development! 🚀
