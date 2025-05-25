# 🎯 Multi-Agent Strategies

AGOR's real power comes from coordinating multiple AI agents using proven strategies. Think of these as **playbooks** for different types of development challenges.

## 🧠 Strategy Overview

Each strategy is designed for specific scenarios and team dynamics. Choose based on your project needs, timeline, and coordination complexity.

| Strategy               | Best For                   | Team Size  | Coordination Level |
| ---------------------- | -------------------------- | ---------- | ------------------ |
| **Parallel Divergent** | Exploration, Research      | 2-4 agents | Medium             |
| **Pipeline**           | Sequential Tasks           | 3-6 agents | High               |
| **Swarm**              | Parallel Work              | 4-8 agents | Low                |
| **Red Team**           | Quality Assurance          | 2-4 agents | High               |
| **Mob Programming**    | Learning, Complex Problems | 3-5 agents | Very High          |

## 🔄 Parallel Divergent Strategy

**"Multiple minds, better solutions"**

### How It Works

1. **Divergent Phase**: Agents work independently on the same problem
2. **Convergent Phase**: Agents review each other's solutions
3. **Synthesis Phase**: Best ideas are combined into final solution

### Perfect For

- **Feature design** with multiple possible approaches
- **Architecture decisions** requiring different perspectives
- **Problem-solving** where creativity is key
- **Research phases** of development

### Example Workflow

```
PROJECT COORDINATOR:
1. sp → Create strategic plan
2. pd → Initialize Parallel Divergent strategy
3. ct → Create team with specialized roles

AGENT TEAM:
- Agent A: Frontend-focused approach
- Agent B: Backend-optimized approach
- Agent C: Performance-focused approach
- Agent D: Security-focused approach

COORDINATION:
1. Each agent develops independent solution
2. Peer review phase with structured feedback
3. Synthesis meeting to combine best elements
4. Final implementation with agreed approach
```

### Success Metrics

- **Solution quality** improved through diverse perspectives
- **Risk reduction** via multiple validation approaches
- **Team learning** through exposure to different methods

## ⚡ Pipeline Strategy

**"Assembly line for development"**

### How It Works

1. **Sequential handoffs** between specialized agents
2. **Clear interfaces** and deliverables at each stage
3. **Quality gates** before work moves to next agent
4. **Feedback loops** for continuous improvement

### Perfect For

- **Feature development** with clear stages
- **Bug fixes** requiring investigation → fix → testing
- **Refactoring** with analysis → planning → implementation
- **Integration projects** with multiple dependencies

### Example Workflow

```
PIPELINE STAGES:

1. FOUNDATION AGENT (Analysis)
   → Analyzes requirements and codebase
   → Deliverable: Technical specification

2. ARCHITECTURE AGENT (Design)
   → Designs solution architecture
   → Deliverable: Implementation plan

3. IMPLEMENTATION AGENT (Code)
   → Writes code following the plan
   → Deliverable: Working implementation

4. VALIDATION AGENT (Testing)
   → Tests and validates solution
   → Deliverable: Verified, tested code

5. INTEGRATION AGENT (Deployment)
   → Integrates with existing system
   → Deliverable: Production-ready feature
```

### Success Metrics

- **Predictable delivery** through structured process
- **Quality assurance** via stage gates
- **Specialization benefits** from focused expertise

## 🐝 Swarm Strategy

**"Distributed intelligence"**

### How It Works

1. **Shared task queue** with prioritized work items
2. **Dynamic assignment** based on agent availability
3. **Minimal coordination** overhead
4. **Emergent organization** through self-selection

### Perfect For

- **Large refactoring** with many independent tasks
- **Bug fixing** across multiple components
- **Documentation** updates and improvements
- **Testing** coverage expansion

### Example Workflow

```
TASK QUEUE SETUP:
- Refactor user authentication (Priority: High)
- Update API documentation (Priority: Medium)
- Add unit tests for utils (Priority: Medium)
- Fix CSS styling issues (Priority: Low)
- Optimize database queries (Priority: High)

SWARM BEHAVIOR:
Agent A: Claims "Refactor user authentication"
Agent B: Claims "Optimize database queries"
Agent C: Claims "Add unit tests for utils"
Agent D: Claims "Update API documentation"

DYNAMIC REBALANCING:
- Agent A finishes → Claims next high priority task
- Agent B needs help → Agent D assists after finishing docs
- New urgent task added → Highest priority, claimed immediately
```

### Success Metrics

- **Throughput maximization** through parallel execution
- **Flexibility** in handling changing priorities
- **Load balancing** across available agents

## ⚔️ Red Team Strategy

**"Build it, break it, fix it"**

### How It Works

1. **Blue Team** builds features and defenses
2. **Red Team** attacks and finds vulnerabilities
3. **Iterative cycles** of build → attack → improve
4. **Adversarial validation** ensures robustness

### Perfect For

- **Security-critical** applications
- **Performance optimization** under stress
- **API design** validation
- **Error handling** improvement

### Example Workflow

```
BLUE TEAM (Builders):
- Implements authentication system
- Adds input validation
- Creates error handling
- Documents security measures

RED TEAM (Breakers):
- Tests for SQL injection vulnerabilities
- Attempts authentication bypasses
- Stress tests with malformed inputs
- Analyzes error message leakage

ITERATION CYCLE:
1. Blue Team: "Authentication system complete"
2. Red Team: "Found session fixation vulnerability"
3. Blue Team: "Fixed session handling, added CSRF protection"
4. Red Team: "CSRF protection bypassed via XSS"
5. Blue Team: "Added XSS protection, content security policy"
6. Red Team: "No further vulnerabilities found"
```

### Success Metrics

- **Security posture** improvement through adversarial testing
- **Robustness** under attack conditions
- **Quality assurance** via systematic breaking attempts

## 👥 Mob Programming Strategy

**"All minds on one problem"**

### How It Works

1. **Collective problem-solving** with all agents engaged
2. **Rotating roles** (Driver, Navigator, Observers)
3. **Continuous discussion** and knowledge sharing
4. **Real-time collaboration** on complex challenges

### Perfect For

- **Complex algorithms** requiring deep thinking
- **Learning new technologies** as a team
- **Critical bug fixes** needing multiple perspectives
- **Knowledge transfer** sessions

### Example Workflow

```
ROLES ROTATION (15-minute intervals):

Round 1:
- Driver: Agent A (writes code)
- Navigator: Agent B (guides direction)
- Observers: Agents C, D (suggest improvements)

Round 2:
- Driver: Agent B (continues implementation)
- Navigator: Agent C (takes over guidance)
- Observers: Agents A, D (provide feedback)

CONTINUOUS ACTIVITIES:
- Real-time code review
- Knowledge sharing
- Problem decomposition
- Solution validation
```

### Success Metrics

- **Knowledge distribution** across all team members
- **Code quality** through continuous review
- **Problem-solving speed** via collective intelligence

## 🎛️ Strategy Selection Guide

### Quick Decision Matrix

**Need creative solutions?** → **Parallel Divergent**
**Have clear sequential steps?** → **Pipeline**  
**Many independent tasks?** → **Swarm**
**Security/quality critical?** → **Red Team**
**Complex problem requiring deep focus?** → **Mob Programming**

### Hybrid Approaches

You can combine strategies for complex projects:

```
PROJECT PHASES:
1. Parallel Divergent → Explore architecture options
2. Pipeline → Implement chosen architecture
3. Red Team → Validate security and robustness
4. Swarm → Handle remaining tasks and polish
```

## 🔧 Implementation Tips

### Starting a Strategy

```bash
# In AGOR, use strategy selection
ss

# Or directly initialize specific strategy
pd  # Parallel Divergent
pl  # Pipeline
sw  # Swarm
rt  # Red Team
mb  # Mob Programming
```

### Coordination Files

Each strategy creates specific coordination files:

- **`.agor/strategy-active.md`** - Current strategy details
- **`.agor/agentconvo.md`** - Cross-agent communication
- **`.agor/agent{N}-memory.md`** - Individual agent notes

### Handoff Procedures

Use AGOR's handoff prompts for smooth transitions:

```bash
hp  # Generate handoff prompts
da  # Detailed analysis for handoff
```

## 📊 Measuring Success

### Strategy Effectiveness Metrics

**Parallel Divergent**: Solution diversity, final quality, innovation level
**Pipeline**: Delivery predictability, stage completion time, defect rate
**Swarm**: Task completion rate, load distribution, adaptability
**Red Team**: Vulnerabilities found, fix rate, security improvement
**Mob Programming**: Knowledge transfer, code quality, problem resolution time

### Continuous Improvement

Use the `meta` hotkey to provide feedback on strategy effectiveness:

- What worked well?
- What coordination challenges emerged?
- How could the strategy be improved?
- What hybrid approaches might work better?

---

**Ready to coordinate your first multi-agent strategy?** Start with [Parallel Divergent](strategies.md#parallel-divergent-strategy) for exploration or [Pipeline](strategies.md#pipeline-strategy) for structured development! 🚀
