# 🤖 Google AI Studio Guide

Google AI Studio provides access to AGOR with Pro models. This guide will get you set up and running smoothly.

## 🎯 Why Google AI Studio?

- **✅ Access to powerful models** like Gemini 2.5 Pro
- **✅ Function Calling support** (essential for AGOR)
- **✅ File upload capability** for bundles
- **✅ Comprehensive model features** for development workflows

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
   - **Worker Agent** - Deep codebase analysis and implementation
   - **Project Coordinator** - Strategic planning and team coordination

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
- Team coordination tools
- Multi-agent strategy selection
- Workflow design capabilities

### 🔍 Worker Agent

**Choose this when:**

- Analyzing existing code
- Implementing specific features
- Debugging issues
- Working solo on technical tasks

**You'll get:**

- Comprehensive codebase analysis and exploration
- Code exploration tools
- Implementation-focused development tools
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
- Snapshot procedures
- Status reporting capabilities

## 💡 Workflow Tips & Troubleshooting Reminders

Remember that the AI may need explicit instructions, especially regarding the execution of tools like Git. Refer to the main "Troubleshooting" section for detailed solutions. AGOR's development tools are always available for providing feedback and coordination.

## 🔄 Multi-Agent Coordination

Google AI Studio works great for **single-agent workflows**, but you can also coordinate **multiple AI instances**:

1. **Coordinator Instance**: Use PROJECT COORDINATOR role for planning
2. **Worker Instances**: Use AGENT WORKER role for implementation
3. **Share coordination files** (`.agor/agentconvo.md`) between instances
4. **Use snapshot prompts** generated by the coordinator using AGOR's development tools.

## 🆘 Troubleshooting

### Common Issues

**AI simulates commands or reports functions unavailable**

- ✅ **Ensure Function Calling is enabled in model settings.** This is the most common cause. Look for a "Function Calling" or "Tools" toggle in the Google AI Studio model settings. Without this, the AI cannot execute actual commands or use provided tools.

**Git commands being simulated**

- ✅ Remind AI about the real git binary: "You have a real, functional git binary at `/tmp/agor_tools/git`. Please make it executable with `chmod 755 /tmp/agor_tools/git` and use it directly for all Git operations (e.g., `/tmp/agor_tools/git status`). Do not simulate commands."

**Git commands fail (e.g., permission denied or command not found initially)**

- ✅ Remind the AI to make the bundled Git binary executable: `chmod 755 /tmp/agor_tools/git`. It should then use the full path: `/tmp/agor_tools/git <command>`.
- ✅ If the AI reports `git: command not found`, explicitly tell it: "The git binary is located at `/tmp/agor_tools/git`. You must use this full path to execute git commands, for example: `/tmp/agor_tools/git --version`."

**AI cannot find the Git repository**

- ✅ Instruct the AI to search its environment recursively for the `.git` directory (e.g., `find /tmp -name .git -type d`) and then navigate to the project's root directory (the parent directory of the `.git` folder).

**Bundle extraction fails**

- ✅ Use `.zip` format (not `.tar.gz`) for Google AI Studio.
- ✅ Re-upload if extraction seems incomplete or if the AI cannot find expected files in `/tmp/PROJECT_NAME_agor_bundle/`.

**Role selection not working**

- ✅ Re-paste the initialization prompt that AGOR provided when you created the bundle.
- ✅ Ensure the bundle was properly extracted and the AI can see the `README_ai.md` file within the bundle.

### Getting Help

- **Use AGOR's feedback tools** to report issues directly
- **Visit [GitHub Issues](https://github.com/jeremiah-k/agor/issues)** for community support
- **Check [Complete AI Protocol](../src/agor/tools/README_ai.md)** for detailed instructions

---

**Ready to start coordinating with Google AI Studio?** Upload your first bundle and experience the power of multi-agent development! 🚀
