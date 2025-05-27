# 🚀 Standalone Mode Guide

**Standalone Mode** is AGOR's workflow for environments where AI agents have direct access to your Git repository and can execute shell commands, including real Git operations. This mode is ideal for more integrated development setups and real-time collaboration.

## 🎯 When to Use Standalone Mode

Choose Standalone Mode if:

*   **You're using AI platforms with direct environment access**: Such as Jules by Google, Augment Code Remote Agents, or other systems where the AI can clone repositories and run shell commands.
*   **You want the AI to make direct Git commits**: If your setup allows and you trust the AI with commit access, this mode enables true end-to-end automation.
*   **Real-time collaboration is needed**: Multiple agents (AI or human) can work on the same live repository, pulling changes and coordinating in real time.
*   **Your project is very large or complex**: Avoiding the bundling step can be quicker for very large repositories, and there are no file size limitations imposed by uploads.
*   **You need full Git operational flexibility**: Agents can create branches, merge, rebase, and perform any Git operation directly.

## 🛠️ How It Works

1.  **Initial Setup (Agent Task)**:
    *   The AI agent first clones the AGOR repository (usually to a temporary directory) to load and understand the AGOR protocol (`AGOR_INSTRUCTIONS.md` and `README_ai.md`).
    *   It then clones your target project repository directly into its environment.
2.  **Environment Configuration**:
    *   The agent configures its Git identity (`user.name`, `user.email`). This can be done by importing environment variables or setting them manually via AGOR's `git-config` utility (if AGOR CLI is available to the agent) or direct `git config` commands.
3.  **Direct Code Interaction**:
    *   The AI analyzes and modifies code directly in the cloned project repository.
    *   It uses its internal tools (like `code_exploration.py` for analysis, if AGOR tools are made available) and direct file manipulation.
4.  **Git Operations**:
    *   The AI performs all Git operations (status, diff, add, commit, branch, push, pull) using a standard Git binary available in its environment. AGOR protocols emphasize using real git commands.
5.  **Output & Collaboration**:
    *   If making direct commits, the AI pushes changes to the remote repository (if configured and authorized).
    *   If direct commit access isn't available or desired, the AI produces code changes as diffs or complete files in codeblocks (similar to Bundle Mode output), which the user then applies manually.
    *   Coordination with other agents (if any) happens via the `.agor/` directory within the project, which should be committed and pushed/pulled.

**Example Initial Agent Workflow (Conceptual):**

```bash
# Commands an AI agent might execute in its environment:

# 1. Learn AGOR protocol
cd /tmp
git clone https://github.com/jeremiah-k/agor.git
cd agor
# Agent reads src/agor/tools/AGOR_INSTRUCTIONS.md and src/agor/tools/README_ai.md

# 2. Clone the target project
cd /workspace # Or any other designated project directory
git clone https://github.com/your-username/your-project.git
cd your-project

# 3. Configure Git
git config user.name "AGOR AI Agent"
git config user.email "ai-agent@example.com"

# 4. Start AGOR workflow (role selection, analysis, etc.)
# (Agent would now typically ask for role selection as per AGOR_INSTRUCTIONS.md)
```

## ✨ Advantages of Standalone Mode

*   **Full Git Power**: Unrestricted access to all Git commands allows for sophisticated version control strategies, branching, merging, and history analysis directly by the AI.
*   **Real-Time Collaboration**: Changes made by one agent can be pulled by others, enabling seamless teamwork between multiple AIs or AIs and human developers.
*   **No Upload/Download Bottlenecks**: Works directly with the live repository, eliminating the need to bundle and upload files, which can be beneficial for very large projects or frequent iterations.
*   **Immediate Change Application**: If direct commit/push is enabled, changes are reflected in the remote repository instantly.
*   **Environment Consistency**: The AI works in an environment that can more closely mirror a human developer's setup.

## ⚙️ Key Considerations

*   **Security and Permissions**: Granting AI agents direct commit access to repositories requires careful consideration of security implications and appropriate permission scoping.
*   **Environment Setup**: The AI's environment must have Git installed and network access to clone repositories.
*   **AGOR Protocol Files**: For multi-agent coordination, the `.agor/` directory and its contents must be version-controlled (committed and pushed/pulled) to be shared among agents.
*   **Fallback to Copy-Paste**: Even in Standalone Mode, if direct commit access is not provided, the workflow for applying changes will revert to the user copying and pasting code provided by the AI, similar to Bundle Mode.

## 🆚 Standalone vs. Bundled Mode

| Feature                 | Standalone Mode                                  | Bundled Mode                                         |
| ----------------------- | ------------------------------------------------ | ---------------------------------------------------- |
| **Repo Access**         | Direct clone, live repository                    | Packaged snapshot at time of bundle                  |
| **Git Operations**      | Full, direct (commits, branches, push/pull)      | Limited to analysis (using bundled Git)              |
| **Change Application**  | Direct commits (if allowed) or copy-paste        | Copy-paste by user                                   |
| **Collaboration**       | Real-time via Git                                | Asynchronous, via re-bundling or manual integration  |
| **Setup**               | AI needs Git & network access                    | User bundles locally, AI uploads                     |
| **File Size Limits**    | None by AGOR (environment limits may apply)      | Platform-dependent upload limits                     |
| **Context Richness**    | Live, full history, all branches accessible      | Rich snapshot (full history, all branches by default)|

Both modes leverage AGOR's powerful coordination protocols and agent instructions. Choose the mode that best fits your AI platform's capabilities, your project's needs, and your preferred development workflow.

---

This guide provides an overview of AGOR's Standalone Mode. For role-specific instructions and detailed AGOR protocols, always refer to the `AGOR_INSTRUCTIONS.md` file.
