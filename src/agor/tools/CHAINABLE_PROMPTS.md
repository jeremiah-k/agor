# AGOR Chainable Initialization Prompts

**Token-efficient prompts for various AGOR scenarios**

These prompts are designed to maximize token efficiency by combining AGOR initialization with specific task instructions. Each prompt ends with the chainable comment, allowing you to add your detailed instructions without requiring a separate initialization step.

## 🚨 CRITICAL: Snapshot System Requirement

**ALL agents using these prompts MUST provide a comprehensive snapshot in a single codeblock before ending their session.** This is mandatory for context preservation and coordination. Read `SNAPSHOT_SYSTEM_GUIDE.md` for complete instructions.

## 🎯 General Purpose Prompts

### Universal AGOR Initialization

```
I'm working with the AGOR (AgentOrchestrator) framework for multi-agent development coordination.

Please read these key files to understand the system:
- README_ai.md (role selection)
- AGOR_INSTRUCTIONS.md (comprehensive guide)

After reading these files, help me initialize AGOR for this project and select the appropriate role based on my needs.

# <--- Add your detailed step-by-step instructions below --->
```

### Quick Solo Development Start

```
I need help with solo development work using AGOR's structured approach.

Please read README_ai.md and select Role A: Worker Agent, then read the Worker Agent sections of AGOR_INSTRUCTIONS.md and SNAPSHOT_SYSTEM_GUIDE.md.

Initialize as Worker Agent and help me with codebase analysis and development tasks.

IMPORTANT: You MUST provide a comprehensive snapshot in a single codeblock before ending this session.

# <--- Add your detailed step-by-step instructions below --->
```

### Multi-Agent Project Planning

```
I'm planning a multi-agent development project using AGOR coordination.

Please read README_ai.md and select Role B: Project Coordinator, then read the Project Coordinator sections of AGOR_INSTRUCTIONS.md and SNAPSHOT_SYSTEM_GUIDE.md.

Initialize as Project Coordinator and help me design the development strategy.

IMPORTANT: You MUST provide a comprehensive snapshot in a single codeblock before ending this session.

# <--- Add your detailed step-by-step instructions below --->
```

## 🔧 Development-Specific Prompts

### Code Review and Analysis

```
I need comprehensive code review and analysis using AGOR's structured approach.

Please read README_ai.md (select Worker Agent) and AGOR_INSTRUCTIONS.md (focus on development tools functions).

Initialize as Worker Agent and help me analyze the codebase for quality, structure, and improvement opportunities.

# <--- Add your detailed step-by-step instructions below --->
```

### Feature Development Planning

```
I'm planning to develop a new feature and need AGOR's strategic planning capabilities.

Please read README_ai.md (select appropriate role based on team size) and AGOR_INSTRUCTIONS.md (focus on strategic planning hotkeys: `sp`, `bp`, `ar`).

Initialize AGOR and help me plan the feature development with clear milestones and coordination.

# <--- Add your detailed step-by-step instructions below --->
```

### Refactoring Coordination

```
I need to coordinate a large-scale refactoring project using AGOR's multi-agent strategies.

Please read README_ai.md (select Project Coordinator), AGOR_INSTRUCTIONS.md (focus on strategy selection and team coordination).

Initialize as Project Coordinator and help me design a refactoring strategy with agent coordination.

# <--- Add your detailed step-by-step instructions below --->
```

## 🤝 Collaboration Prompts

### Snapshot Transition Preparation

```
I need to prepare a work snapshot for another agent using AGOR's snapshot system.

Please read README_ai.md, AGOR_INSTRUCTIONS.md (focus on snapshot procedures), and understand the snapshot_templates.py system.

Help me create a comprehensive snapshot document for seamless agent transition.

# <--- Add your detailed step-by-step instructions below --->
```

### Receiving Work Snapshot

```
I'm receiving a work snapshot from another agent and need to continue their work.

Please read README_ai.md (select appropriate role), AGOR_INSTRUCTIONS.md (focus on snapshot reception), and understand the coordination protocols.

Help me load the snapshot context and continue the work seamlessly.

# <--- Add your detailed step-by-step instructions below --->
```

### Team Coordination Setup

```
I need to set up team coordination for a multi-agent development project.

Please read README_ai.md (select Project Coordinator), AGOR_INSTRUCTIONS.md (focus on team management and coordination).

Initialize team coordination and help me establish the development workflow.

# <--- Add your detailed step-by-step instructions below --->
```

## 🎨 Specialized Prompts

### Documentation Generation

```
I need to generate comprehensive documentation using AGOR's structured approach.

Please read README_ai.md (select Worker Agent) and AGOR_INSTRUCTIONS.md (focus on development tools functions).

Initialize as Worker Agent and help me create thorough documentation for the codebase.

# <--- Add your detailed step-by-step instructions below --->
```

### Quality Assurance Planning

```
I need to establish quality assurance processes using AGOR's quality gates system.

Please read README_ai.md (select Project Coordinator), AGOR_INSTRUCTIONS.md (focus on quality gates: `qg`).

Initialize quality assurance planning and help me establish validation procedures.

# <--- Add your detailed step-by-step instructions below --->
```

### Architecture Review

```
I need a comprehensive architecture review using AGOR's analysis capabilities.

Please read README_ai.md (select appropriate role), AGOR_INSTRUCTIONS.md (focus on architecture review: `ar`, `dp`), and understand the analysis tools.

Initialize architecture review and help me assess the current system design.

# <--- Add your detailed step-by-step instructions below --->
```

## 💡 Usage Guidelines

### Token Efficiency Tips

1. **Choose the most specific prompt** for your use case
2. **Combine initialization with task details** after the chainable comment
3. **Reference specific AGOR files** only when needed for your task
4. **Use role-specific prompts** when you know your role in advance

### Customization Examples

**Example 1: Feature Development**

```
[Use Feature Development Planning prompt above]

# <--- Add your detailed step-by-step instructions below --->

1. Analyze the current authentication system
2. Plan integration of OAuth 2.0 support
3. Design database schema changes
4. Create implementation timeline with milestones
5. Set up testing strategy for the new feature
```

**Example 2: Code Review**

```
[Use Code Review and Analysis prompt above]

# <--- Add your detailed step-by-step instructions below --->

1. Review the recent changes in the user management module
2. Check for security vulnerabilities in authentication code
3. Assess code quality and adherence to project standards
4. Identify opportunities for performance optimization
5. Suggest refactoring improvements
```

### Best Practices

- **Be specific** in your additional instructions
- **Reference file paths** when asking for specific file analysis
- **Include context** about your project's current state
- **Mention constraints** like deadlines or technical requirements
- **Specify deliverables** you expect from the session

---

_These prompts are designed to work with any AGOR deployment method (Bundle, Standalone, or Local Integration) and can be adapted for your specific development environment._
