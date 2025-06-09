# 🔄 AGOR Refresh Protocols

**Elegant ways to reset, refresh, and reorient during AGOR sessions**

## 🎯 The Refresh Challenge

During longer AGOR sessions, both users and agents can:

- Lose track of current context
- Forget available options
- Get confused about their role or mode
- Need to restart after errors
- Want to change direction

**Goal**: Provide smooth, non-disruptive ways to refresh and reorient.

## 🔄 Refresh Mechanisms

### 1. **Soft Refresh** - Context Reminder

**Hotkey**: `?` or `help`
**Purpose**: Quick reminder without full reset

```
🎼 AGOR Quick Reference

**Your Current Context:**
• Role: Worker Agent
• Mode: Bundle Mode
• Project: [project-name]
• Last Action: [last-action]

**Most Common Actions:**
a) analyze codebase    f) full files    edit) modify files
sp) strategic plan     tree) structure  commit) save changes

**Need More Options?** Type `menu` for full menu
**Lost?** Type `reset` to restart cleanly
**Help?** Type `guide` for role-specific guidance

What would you like to do?
```

### 2. **Menu Refresh** - Full Options Display

**Hotkey**: `menu` or `m`
**Purpose**: Redisplay full role-specific menu

```
🔄 Refreshing your options...

[DISPLAYS FULL ROLE-SPECIFIC MENU]

Select an option:
```

### 3. **Clean Reset** - Fresh Start

**Hotkey**: `reset` or `restart`
**Purpose**: Clean slate without losing context

```
🔄 AGOR Clean Reset

Refreshing your session while preserving your work...

**Your Context:**
• Role: [ROLE]
• Mode: [MODE]
• Project: [PROJECT]

**Ready for Action:**
[DISPLAYS FRESH ROLE-SPECIFIC MENU]

Select an option:
```

### 4. **Role Reminder** - Identity Refresh

**Hotkey**: `role` or `who`
**Purpose**: Remind about current role and capabilities

```
🎭 Role Reminder

**You are: [ROLE NAME]**
**Your Focus**: [role description]
**Your Strengths**: [key capabilities]
**Your Tools**: [main hotkeys]

**Ready to continue?**
[DISPLAYS ROLE-SPECIFIC MENU]
```

### 5. **Guide Refresh** - Protocol Reminder

**Hotkey**: `guide` or `protocol`
**Purpose**: Quick protocol reminder without full restart

```
📋 AGOR Protocol Reminder

**Your Mode**: [Bundle/Standalone]
**Key Principles**:
• Always confirm actions before executing
• Show results clearly
• Return to menu after each action
• Keep interface professional

**Current Menu:**
[DISPLAYS CURRENT ROLE MENU]
```

## 🎨 Design Principles

### **Elegant Integration**

- Refresh options feel natural, not like error recovery
- Consistent with overall AGOR aesthetic
- Quick and non-disruptive
- Preserve user context and progress

### **Progressive Disclosure**

- `?` - Minimal context reminder
- `menu` - Full options without explanation
- `reset` - Fresh start with context preservation
- `guide` - Protocol and role reminder

### **Context Preservation**

- Never lose user's work or progress
- Remember last actions and current state
- Maintain role and mode information
- Keep project context intact

## 📋 Implementation in Menus

### Add to All Role Menus:

```
**🔄 Session Management:**
?) quick help    menu) full options    reset) clean restart
role) role reminder    guide) protocol refresh
```

### Or More Subtle Integration:

```
**🔄 Navigation:**
?) help    menu) options    reset) restart    guide) protocol
```

## 🎯 Contextual Refresh Triggers

### **When to Suggest Refresh**:

1. **After Errors**: "Something went wrong? Try `reset` for a clean start"
2. **Long Sessions**: "Been working a while? Type `?` for a quick refresher"
3. **User Confusion**: "Not sure what to do? Try `menu` to see all options"
4. **Mode Switches**: "Switched contexts? Type `role` to confirm your current role"

### **Proactive Refresh Suggestions**:

```
💡 **Session Tip**: Type `?` anytime for quick help, or `menu` to see all options

💡 **Lost?** Try `reset` for a clean restart while keeping your progress

💡 **Quick Refresh**: Use `role` to remind yourself of your current capabilities
```

## 🔄 Smart Refresh Logic

### **Context-Aware Suggestions**:

- After 10+ actions: Suggest `?` for quick refresh
- After errors: Suggest `reset` for clean start
- When user seems confused: Suggest `menu` for full options
- When switching between different types of actions: Suggest `role` reminder

### **Adaptive Messaging**:

```python
# Pseudo-logic for smart refresh suggestions
if action_count > 10:
    suggest("💡 Type `?` for a quick refresher of your options")
elif last_action_failed:
    suggest("💡 Try `reset` for a clean restart")
elif user_input_unclear:
    suggest("💡 Type `menu` to see all available options")
```

## 🎨 Visual Design

### **Consistent Formatting**:

- Use 🔄 emoji for all refresh-related actions
- Maintain AGOR's professional aesthetic
- Keep refresh messages brief and helpful
- Use consistent language patterns

### **Non-Intrusive Placement**:

- Include refresh options in menus naturally
- Don't make them prominent unless needed
- Provide as helpful suggestions, not requirements
- Keep the main workflow clean and focused

## 🚫 What to Avoid

❌ **Don't be pushy**: "You seem confused, try reset!"
❌ **Don't interrupt flow**: Constant refresh suggestions
❌ **Don't lose context**: Refresh should preserve work
❌ **Don't be technical**: "Reinitialize protocol stack"

✅ **Do be helpful**: "Type `?` for quick help"
✅ **Do be subtle**: Include options naturally in menus
✅ **Do preserve context**: Keep user's progress and state
✅ **Do be professional**: Maintain AGOR's polished feel

## 🎯 Implementation Strategy

### **Phase 1**: Add basic refresh hotkeys to all menus

- `?` for quick help
- `menu` for full options
- `reset` for clean restart

### **Phase 2**: Add contextual suggestions

- Smart triggers based on session state
- Helpful tips without being intrusive

### **Phase 3**: Advanced context preservation

- Remember user preferences
- Adaptive refresh suggestions
- Session state management

## 🛠️ Implementation Guide for Agents

### **Handling Refresh Hotkeys**:

**When user types `?` or `help`**:

```
🎼 AGOR Quick Reference

**Your Current Context:**
• Role: [CURRENT_ROLE]
• Mode: [Bundle/Standalone]
• Project: [project-name if available]
• Last Action: [last-action if available]

**Most Common Actions:**
a) analyze codebase    f) full files    edit) modify files
sp) strategic plan     tree) structure  commit) save changes

**Need More Options?** Type `menu` for full menu
**Lost?** Type `reset` to restart cleanly
**Help?** Type `guide` for role-specific guidance

What would you like to do?
```

**When user types `menu`**:

- Simply redisplay the full role-specific menu
- No extra explanation needed
- Clean, fresh presentation

**When user types `reset`**:

```
🔄 AGOR Clean Reset

Refreshing your session while preserving your work...

**Your Context:**
• Role: [ROLE]
• Mode: [MODE]
• Project: [PROJECT]

**Ready for Action:**
[DISPLAY FULL ROLE-SPECIFIC MENU]

Select an option:
```

**When user types `role`**:

```
🎭 Role Reminder

**You are: [ROLE NAME]**
**Your Focus**: [role description]
**Your Strengths**: [key capabilities]
**Your Tools**: [main hotkeys]

**Ready to continue?**
[DISPLAY ROLE-SPECIFIC MENU]
```

**When user types `guide`**:

```
📋 AGOR Protocol Reminder

**Your Mode**: [Bundle/Standalone]
**Key Principles**:
• Always confirm actions before executing
• Show results clearly
• Return to menu after each action
• Keep interface professional

**Current Menu:**
[DISPLAY CURRENT ROLE MENU]
```

### **Smart Suggestions**:

After certain conditions, include helpful tips:

- After 10+ actions: "💡 Type `?` for a quick refresher"
- After errors: "💡 Try `reset` for a clean start"
- When user seems confused: "💡 Type `menu` to see all options"

---

**Remember**: Refresh mechanisms should feel like helpful navigation tools, not error recovery. The goal is to keep users confident and oriented throughout their AGOR session.
