"""
Handoff templates and procedures for seamless agent transitions.

Enables agents to hand off work to other agents with complete context,
including problem definition, progress made, commits, and next steps.
"""

import datetime
from pathlib import Path
from typing import Dict, List, Optional


def generate_handoff_document(
    problem_description: str,
    work_completed: List[str],
    commits_made: List[str],
    current_status: str,
    next_steps: List[str],
    files_modified: List[str],
    context_notes: str,
    agent_role: str,
    handoff_reason: str,
    estimated_completion: str = "Unknown"
) -> str:
    """Generate a comprehensive handoff document for agent transitions."""
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""# 🤝 Agent Handoff Document

**Generated**: {timestamp}
**From Agent Role**: {agent_role}
**Handoff Reason**: {handoff_reason}

## 🎯 Problem Definition

{problem_description}

## 📊 Current Status

**Overall Progress**: {current_status}
**Estimated Completion**: {estimated_completion}

## ✅ Work Completed

{chr(10).join(f"- {item}" for item in work_completed)}

## 📝 Commits Made

{chr(10).join(f"- `{commit}`" for commit in commits_made)}

## 📁 Files Modified

{chr(10).join(f"- `{file}`" for file in files_modified)}

## 🔄 Next Steps

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(next_steps))}

## 🧠 Context & Important Notes

{context_notes}

## 🔧 Technical Context

### Current Branch
```bash
git branch --show-current
git status --porcelain
```

### Recent Changes
```bash
git log --oneline -5
git diff --name-only HEAD~1
```

### Key Files to Review
{chr(10).join(f"- `{file}` - Review recent changes and understand current state" for file in files_modified[:5])}

## 🎯 Handoff Instructions for Receiving Agent

### 1. Context Loading
```bash
# Review the current state
git status
git log --oneline -10

# Examine modified files
{chr(10).join(f"# Review {file}" for file in files_modified[:3])}
```

### 2. Verify Understanding
- [ ] Read and understand the problem definition
- [ ] Review all completed work items
- [ ] Examine commits and understand changes made
- [ ] Verify current status matches expectations
- [ ] Understand the next steps planned

### 3. Continue Work
- [ ] Start with the first item in "Next Steps"
- [ ] Update this handoff document with your progress
- [ ] Commit regularly with clear messages
- [ ] Update `.agor/agentconvo.md` with your status

### 4. Communication Protocol
- Update `.agor/agentconvo.md` with handoff received confirmation
- Log major decisions and progress updates
- Create new handoff document if passing to another agent

---

**Receiving Agent**: Please confirm handoff receipt by updating `.agor/agentconvo.md` with:
```
[AGENT-ID] [{timestamp}] - HANDOFF RECEIVED: {problem_description[:50]}...
```
"""


def generate_handoff_prompt(handoff_file_path: str) -> str:
    """Generate a prompt for handing off work to another agent."""
    
    return f"""# 🤝 Work Handoff to Another Agent

I'm handing off this work to another agent. Here's the complete context:

## Handoff Document
Please read the complete handoff document at: `{handoff_file_path}`

## Instructions for Receiving Agent

### 1. Load Context
```bash
# Read the handoff document
cat {handoff_file_path}

# Review current repository state
git status
git log --oneline -10
```

### 2. Confirm Understanding
After reading the handoff document, please confirm you understand:
- The problem being solved
- Work completed so far
- Current status and next steps
- Files that have been modified
- Technical context and important notes

### 3. Continue the Work
- Start with the first item in the "Next Steps" section
- Update the handoff document with your progress
- Follow the communication protocol outlined in the document

### 4. Update Communication Log
Add to `.agor/agentconvo.md`:
```
[YOUR-AGENT-ID] [{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - HANDOFF RECEIVED: [Brief description of task]
```

## Ready to Begin?
Type `receive-handoff` to confirm you've read the handoff document and are ready to continue the work.
"""


def generate_receive_handoff_prompt() -> str:
    """Generate a prompt for receiving a handoff from another agent."""
    
    return """# 🤝 Receiving Work Handoff

I'm ready to receive a handoff from another agent. Please provide:

## Required Information

### 1. Handoff Document Location
- Path to the handoff document (usually in `.agor/handoffs/`)
- Or paste the complete handoff document content

### 2. Current Repository State
```bash
# Let me check the current state
git status
git log --oneline -5
```

### 3. Verification Steps
I will:
- [ ] Read and understand the complete handoff document
- [ ] Review the problem definition and context
- [ ] Examine all completed work and commits
- [ ] Understand the current status and next steps
- [ ] Verify the technical context

### 4. Confirmation Process
Once I understand the handoff, I will:
- [ ] Confirm receipt in `.agor/agentconvo.md`
- [ ] Begin work on the next steps
- [ ] Update progress regularly
- [ ] Maintain communication protocols

## Ready to Receive
Please provide the handoff document or its location, and I'll take over the work seamlessly.
"""


def create_handoff_directory() -> Path:
    """Create handoff directory structure in .agor/"""
    
    handoff_dir = Path(".agor/handoffs")
    handoff_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index file if it doesn't exist
    index_file = handoff_dir / "index.md"
    if not index_file.exists():
        index_content = """# 🤝 Handoff Index

This directory contains handoff documents for agent transitions.

## Active Handoffs
- None currently

## Completed Handoffs
- None yet

## Handoff Naming Convention
- `YYYY-MM-DD_HHMMSS_problem-summary.md`
- Example: `2024-01-15_143022_fix-authentication-bug.md`

## Usage
- Use `handoff` hotkey to create new handoff
- Use `receive-handoff` hotkey to accept handoff
- Update this index when handoffs are created or completed
"""
        index_file.write_text(index_content)
    
    return handoff_dir


def save_handoff_document(
    handoff_content: str,
    problem_summary: str
) -> Path:
    """Save handoff document to .agor/handoffs/ directory."""
    
    handoff_dir = create_handoff_directory()
    
    # Generate filename with timestamp and problem summary
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_summary = "".join(c for c in problem_summary if c.isalnum() or c in "-_")[:30]
    filename = f"{timestamp}_{safe_summary}.md"
    
    handoff_file = handoff_dir / filename
    handoff_file.write_text(handoff_content)
    
    # Update index
    update_handoff_index(filename, problem_summary, "active")
    
    return handoff_file


def update_handoff_index(filename: str, problem_summary: str, status: str):
    """Update the handoff index with new or completed handoffs."""
    
    index_file = Path(".agor/handoffs/index.md")
    if not index_file.exists():
        create_handoff_directory()
    
    content = index_file.read_text()
    
    if status == "active":
        # Add to active handoffs
        content = content.replace(
            "## Active Handoffs\n- None currently",
            f"## Active Handoffs\n- `{filename}` - {problem_summary}"
        )
        if "- None currently" not in content and f"`{filename}`" not in content:
            content = content.replace(
                "## Active Handoffs\n",
                f"## Active Handoffs\n- `{filename}` - {problem_summary}\n"
            )
    elif status == "completed":
        # Move from active to completed
        content = content.replace(
            f"- `{filename}` - {problem_summary}",
            ""
        )
        content = content.replace(
            "## Completed Handoffs\n- None yet",
            f"## Completed Handoffs\n- `{filename}` - {problem_summary}"
        )
        if "- None yet" not in content and f"`{filename}`" not in content:
            content = content.replace(
                "## Completed Handoffs\n",
                f"## Completed Handoffs\n- `{filename}` - {problem_summary}\n"
            )
    
    index_file.write_text(content)


# Hotkey integration templates
HANDOFF_HOTKEY_HELP = """
🤝 **Handoff Commands:**
handoff) create handoff document for another agent
receive) receive handoff from another agent
handoffs) list all handoff documents
"""
