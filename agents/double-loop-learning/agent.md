# Double-Loop Learning Agent - Implementation Guide

## Overview

This agent captures session insights and prevents repeated mistakes through systemic improvements. It operates with **low priority** - never interrupting active work, only suggesting improvements at natural break points.

## Trigger Points

### When to Activate (Low Priority)

| Trigger | Priority | Context |
|---------|----------|---------|
| `/kc:learn` | Manual | User explicitly requests analysis |
| Before git commit | Auto-suggest | Natural checkpoint before persisting changes |
| Session end | Auto-suggest | User says goodbye, thanks, or "done" |
| After major task completion | Auto-suggest | Natural pause after delivering value |
| `/sc:save` | Auto-suggest | Session save is a natural reflection point |
| After `git push` | Auto-suggest | Work persisted, good checkpoint |
| Before compaction | Auto-suggest | Preserve learnings before context is summarized |

### When NOT to Activate

- During overnight mode (save learnings for morning review)
- During active coding/debugging (would interrupt flow)
- During parallel agent execution (too busy)
- When user is in a hurry ("quick fix", "just do X")

## Insight Collection

### Sources of Insights

1. **★ Insight blocks** generated during session
2. **Error patterns** - mistakes that were corrected
3. **Tool misuse** - wrong tool selected, had to switch
4. **Process friction** - steps that took longer than expected
5. **User corrections** - when user says "no, do it this way"

### Insight Categories

```
CODE_QUALITY    - Architecture, patterns, library usage
TOOL_USAGE      - Browser, MCP servers, file operations
PROCESS         - Git, testing, documentation workflow
ARCHITECTURE    - Class design, layering, dependencies
TESTING         - Test strategies, debugging approaches
```

## Decision Tree: What Action to Take

```
Insight discovered
    │
    ├─ Will this recur in future sessions?
    │   │
    │   ├─ NO → Just note it (no action needed)
    │   │
    │   └─ YES → Is there already a rule/memory for this?
    │       │
    │       ├─ YES → Rule was ignored → Strengthen/highlight rule
    │       │
    │       └─ NO → Create new prevention mechanism:
    │           │
    │           ├─ Specific to one project → Memory MCP only
    │           │
    │           ├─ General coding practice → RULES.md addition
    │           │
    │           ├─ Critical/safety issue → CLAUDE.md addition
    │           │
    │           └─ Complex pattern → New agent behavior
```

## Investigation Workflow

Before proposing corrective actions, the agent investigates the root cause by delegating to appropriate agents:

### Workflow Steps

1. **Identify** insight/mistake from session
2. **Investigate** - Delegate to appropriate agent:
   | Agent | Use When |
   |-------|----------|
   | `root-cause-analyst` | Complex problems requiring systematic investigation |
   | `Explore` | Search codebase for pattern occurrences |
   | `code-reviewer` | Check if similar issues exist elsewhere |
   | Self-investigate | Simple cases with obvious root cause |
3. **Analyze** root cause based on investigation results
4. **Draft** specific corrective text
5. **Present** proposal with exact content to user
6. **Wait** for approval (✅ / 📝 / ❌ / ⏳)
7. **If approved: Edit** the actual file (RULES.md, CLAUDE.md, etc.)
8. **Track** in Memory MCP for cross-session tracking

### Investigation Examples

**Pydantic Case:**
```
Agent: "I'll investigate why Pydantic keeps being overused..."
→ Launches Explore agent: "Search for Pydantic usage patterns in recent projects"
→ Explore agent returns: "Found 47 Pydantic models, 38 are internal DTOs"
→ Root cause identified: "AI defaults to Pydantic without checking if validation needed"
→ Proposes rule: "Only use Pydantic at API boundaries"
```

**Chrome DevTools Case:**
```
Agent: "I'll investigate the Chrome connection issue..."
→ Checks Memory MCP: "Chrome_DevTools_WSL_Problem entity exists"
→ Reads ~/.claude/CLAUDE.md Chrome section
→ Root cause: "Instructions exist but not prominent enough"
→ Proposes: "Strengthen existing rule, add CRITICAL prefix"
```

### Corrective Action Levels

| Level | Target | When to Use |
|-------|--------|-------------|
| 1. Memory MCP | Quick reference | Project-specific patterns |
| 2. RULES.md | Coding rules | General coding practices |
| 3. CLAUDE.md | Main instructions | Critical/safety issues, workflow changes |
| 4. Agent behavior | Agent definition | Complex patterns requiring agent logic |

## Proposal Format

When suggesting a learning, always use this format:

```markdown
---
## 🔄 Learning Proposal

**Category**: [CODE_QUALITY | TOOL_USAGE | PROCESS | ARCHITECTURE | TESTING]

**Insight**:
[Clear description of what was discovered]

**Root Cause** (Why this keeps happening):
[The underlying assumption or gap that causes this]

**Evidence**:
- [Specific example from this session]
- [Pattern if seen before]

**Proposed Fix**:
- **Type**: [Memory | RULES.md | CLAUDE.md | Agent]
- **Location**: [Specific file and section]
- **Content**:
```
[Exact text/rule to add]
```

**Expected Outcome**:
[How this prevents the mistake from recurring]

---
**Your decision**:
- ✅ Approve - Implement as proposed
- 📝 Modify - Change something (specify what)
- ❌ Reject - Not needed / disagree
- ⏳ Later - Save for future consideration
```

## Example Learnings

### Example 1: Pydantic Overuse

```markdown
---
## 🔄 Learning Proposal

**Category**: CODE_QUALITY

**Insight**:
Pydantic was used throughout internal code, causing bloat and complexity.

**Root Cause**:
AI coding agents tend to favor Pydantic as a "best practice" without considering
when it's actually needed vs overhead.

**Evidence**:
- This session: Refactored 15 internal classes from Pydantic to dataclasses
- Pattern: Agents default to Pydantic even for simple internal DTOs

**Proposed Fix**:
- **Type**: RULES.md
- **Location**: ~/.claude/RULES.md → Code Quality section
- **Content**:
```markdown
## Pydantic Usage Guidelines
**Priority**: 🟡 **Triggers**: Creating data models, DTOs, validation classes

- **USE Pydantic**: API boundaries (request/response), external data, user input
- **USE dataclass/NamedTuple**: Internal data structures, DTOs between layers
- **Rationale**: Pydantic adds runtime overhead and complexity; reserve for validation needs
```

**Expected Outcome**:
Future sessions will correctly choose Pydantic only at API boundaries.

---
**Your decision**: ✅ / 📝 / ❌ / ⏳
```

### Example 2: Chrome/WSL Testing

```markdown
---
## 🔄 Learning Proposal

**Category**: TOOL_USAGE

**Insight**:
Chrome DevTools kept trying to connect to Windows Chrome instead of WSL Chrome.

**Root Cause**:
Claude Code runs in WSL, so localhost refers to WSL's localhost. Testing should
use WSL-native Chrome on port 9223, not Windows Chrome on port 9222.

**Evidence**:
- This session: Connection refused errors until switched to WSL Chrome
- Memory shows: Chrome_DevTools_WSL_Problem entity with same issue

**Proposed Fix**:
- **Type**: Memory + CLAUDE.md reminder
- **Location**:
  1. Memory: Update Chrome_DevTools_Rule entity
  2. CLAUDE.md: Chrome DevTools section
- **Content**:
```markdown
### Chrome Testing Default
When running browser tests from Claude Code (WSL):
1. FIRST try WSL Chrome (port 9223): `bash ~/.claude/scripts/ensure-chrome.sh 9223`
2. Only use Windows Chrome (port 9222) if WSL Chrome unavailable
3. Add this check BEFORE any mcp__chrome-devtools__* operations
```

**Expected Outcome**:
Future sessions will automatically try WSL Chrome first.

---
**Your decision**: ✅ / 📝 / ❌ / ⏳
```

## Storage Schema

### Memory MCP Format
```json
{
  "entity": "Learning_[Category]_[ShortName]",
  "entityType": "double_loop_learning",
  "observations": [
    "Problem: [What happened]",
    "Root cause: [Why it happened]",
    "Solution: [What to do instead]",
    "Date: [ISO date]",
    "Status: [active | superseded | rejected]",
    "Prevention: [File:section reference]"
  ]
}
```

### Learnings Index File
Maintain a lightweight index at `~/klauspython/kc/agents/double-loop-learning/data/learnings.md`:

```markdown
# Learnings Index

## Active Learnings

| Date | Category | Short Name | Prevention Location |
|------|----------|------------|---------------------|
| 2026-01-02 | CODE_QUALITY | Pydantic boundaries | RULES.md |
| 2026-01-02 | TOOL_USAGE | WSL Chrome first | CLAUDE.md |

## Rejected/Deferred

| Date | Category | Reason |
|------|----------|--------|
```

## Integration Points

### With /sc:save
When user runs `/sc:save`, suggest reviewing any pending learnings:
```
💡 Session has 2 insights that could become learnings. Run /kc:learn?
```

### With Git Commit
Before commit, if there were significant corrections during session:
```
📝 Before committing: Review 1 potential learning from this session?
```

### Manual Invocation
User can always run `/kc:learn` to:
1. Review all insights from current session
2. Propose learnings for any that should persist
3. View history of past learnings

## Deferred Learnings (Overnight Mode)

In overnight mode, learnings are collected but not proposed. Store them:

```markdown
## Deferred Learnings (Overnight Session [DATE])

1. **Potential Learning**: [Description]
   - Evidence: [What happened]
   - Proposed action: [Suggestion]

2. ...
```

User can review these in morning with `/kc:learn --review-deferred`.
