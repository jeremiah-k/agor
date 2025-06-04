# AGOR State Management System

## Overview

AGOR's state management system provides structured coordination for multi-agent development strategies. The `.agor/state/` directory contains JSON, YAML, and Markdown files that track strategy progress, agent assignments, and coordination status.

**Note for AGOR Core Developers:** The `.agor/` directory and its state files described herein are intended for _target projects_ being managed by AGOR. When developing AGOR itself, these files should generally not be committed to the AGOR repository. Refer to the "[Testing Coordination Strategies & State Management](agor-development-guide.md#testing-coordination-strategies--state-management)" section in the AGOR Development Guide for best practices.

## Directory Structure

```
.agor/
├── state/                          # Strategy state management
│   ├── strategy.json               # Current strategy configuration
│   ├── agent_branches.json         # Agent-to-branch mapping
│   ├── active_tasks.json           # Agent status tracking
│   ├── pd_evaluation.md            # Parallel Divergent evaluation
│   ├── sync_flags.yaml             # Coordination flags
│   └── state.log                   # Event log
├── agent-instructions/             # Individual agent instructions
│   ├── agent1-instructions.md
│   ├── agent2-instructions.md
│   └── agent3-instructions.md

├── agentconvo.md                   # Agent communication log
└── memory.md                       # Project memory
```

## State Files

### strategy.json

Contains the current strategy configuration:

```json
{
  "mode": "pd",
  "task": "implement e2e encryption for login system",
  "agents": ["agent1", "agent2", "agent3"],
  "created": "2025-05-26T01:18:36.806222",
  "status": "initialized"
}
```

### agent_branches.json

Maps agents to their assigned git branches:

```json
{
  "agent1": "agent1/implement-e2e-encryp",
  "agent2": "agent2/implement-e2e-encryp",
  "agent3": "agent3/implement-e2e-encryp"
}
```

### active_tasks.json

Tracks the current status of each agent:

```json
{
  "agent1": "completed",
  "agent2": "completed",
  "agent3": "completed"
}
```

**Valid statuses:**

- `pending`: Agent hasn't started work
- `in-progress`: Agent is actively working
- `completed`: Agent has finished their solution

### sync_flags.yaml

Contains coordination flags and metadata:

```yaml
agents_ready: 3
last_sync: "2025-05-26T01:18:36.806632"
last_update: "2025-05-26T01:20:19.865927"
pd_merge_pending: true
total_agents: 3
```

### state.log

Event log with timestamps:

```
[2025-05-26 01:18:36] Initialized Parallel Divergent strategy for task: implement e2e encryption for login system
[2025-05-26 01:20:06] Agent agent1 status: pending → in-progress
[2025-05-26 01:20:11] Agent agent2 status: pending → completed
[2025-05-26 01:20:16] Agent agent3 status: pending → completed
[2025-05-26 01:20:19] Agent agent1 status: in-progress → completed
[2025-05-26 01:20:19] All agents completed - merge phase ready
```

## CLI Commands

### Initialize Strategy

```bash
# Initialize basic coordination
agor init "task description" --agents 3

# Initialize Parallel Divergent strategy
agor pd "implement e2e encryption" --agents 3
```

### Monitor Progress

```bash
# Check overall status
agor status

# Update agent status
agor agent-status agent1 in-progress
agor agent-status agent1 completed

# Sync with remote
agor sync
```

### Strategy Selection

```bash
# Get strategy recommendations
agor ss --complexity complex --team-size 4
```

## Parallel Divergent Workflow

### Phase 1: Divergent Execution

1. **Setup**: `agor pd "task description" --agents 3`
2. **Agent Assignment**: Each agent gets their own branch and instructions
3. **Independent Work**: Agents work without coordination
4. **Status Updates**: `agor agent-status agent1 in-progress`

### Phase 2: Convergent Review

1. **Completion**: All agents mark status as `completed`
2. **Review**: Agents review each other's solutions
3. **Evaluation**: Update `pd_evaluation.md` with findings
4. **Comparison**: Identify best practices and innovations

### Phase 3: Synthesis

1. **Merge Planning**: Decide which approaches to combine
2. **Implementation**: Create unified solution
3. **Documentation**: Update project documentation
4. **Finalization**: Merge to main branch

## Integration with Existing Tools

### Memory Synchronization System

The state management integrates with AGOR's memory synchronization system:

- State changes are logged to memory files
- Agent memories are stored in markdown files
- Coordination events are tracked in git branches

### Git Integration

- Automatic branch creation for each agent
- Branch naming follows pattern: `{agent_id}/{task_slug}`
- Status tracking includes git synchronization

### Agent Instructions

- Individual instruction files generated for each agent
- Clear phase-based workflow guidance
- Communication protocols defined

## Best Practices

### File Management

- Keep state files under 500 lines
- Use structured JSON/YAML for machine readability
- Maintain human-readable Markdown for documentation

### Status Updates

- Update agent status regularly during development
- Use descriptive commit messages on agent branches
- Log significant decisions in `pd_evaluation.md`

### Coordination

- Check `agor status` before major decisions
- Sync regularly with `agor sync`
- Use agent communication log for cross-agent messages

## Error Handling

### Missing Files

- State files are auto-generated if missing
- Graceful degradation when files are corrupted
- Clear error messages for invalid operations

### Invalid States

- Status validation prevents invalid transitions
- Agent ID validation ensures correct assignments
- Strategy mode validation prevents conflicts

## Future Extensions

### Additional Strategies

- Pipeline strategy state management
- Swarm strategy task queues
- Red Team adversarial tracking

### Enhanced Coordination

- Real-time status updates
- Automated merge conflict detection
- Performance metrics tracking

## Troubleshooting

### Common Issues

**No state directory found:**

```bash
# Solution: Initialize strategy first
agor pd "your task" --agents 3
```

**Agent not found:**

```bash
# Check available agents
agor status
# Use correct agent ID (agent1, agent2, etc.)
```

**Invalid status:**

```bash
# Use valid statuses: pending, in-progress, completed
agor agent-status agent1 completed
```

### Recovery

**Corrupted state files:**

1. Backup existing `.agor/` directory
2. Re-initialize strategy: `agor pd "task" --agents N`
3. Manually update status if needed

**Missing branches:**

- Branches are auto-created during strategy initialization
- Manual creation: `git checkout -b agent1/task-name`

## Implementation Details

### File Formats

- **JSON**: Machine-readable configuration and status
- **YAML**: Human-readable flags and metadata
- **Markdown**: Documentation and evaluation notes
- **Log**: Timestamped event tracking

### Atomic Operations

- File updates are atomic to prevent corruption
- Status changes are logged before file updates
- Rollback capability for failed operations

### Performance

- Minimal file I/O for status checks
- Efficient JSON parsing for large agent counts
- Lazy loading of non-critical files

This state management system provides the foundation for robust multi-agent coordination while maintaining simplicity and extensibility.
