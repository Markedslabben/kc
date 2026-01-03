---
name: learn
description: Review session insights and propose systemic improvements to prevent recurring mistakes. Triggers the double-loop-learning agent to analyze ★ Insight blocks, investigate root causes, and propose corrective actions to RULES.md, CLAUDE.md, or Memory MCP. Use when saying "/kc:learn", "capture learnings", "what did we learn", or at session end.
---

# Double-Loop Learning Session Review

Analyze the current session for insights and learnings that should persist to prevent future mistakes.

## Task

You are invoking the **double-loop-learning** agent to review this session's insights and propose systemic improvements.

### Instructions

#### 1. Identify Mode

**Arguments:**
| Flag | Mode | Description |
|------|------|-------------|
| (none) | Standard | Review current session insights |
| `--review-deferred` | Deferred | Review learnings from overnight sessions |
| `--history` | History | Show past learnings and their status |
| `--category <cat>` | Filtered | Focus on specific category |

**Categories:** CODE_QUALITY, TOOL_USAGE, PROCESS, ARCHITECTURE, TESTING

#### 2. Collect Insights

Scan the session for:
- **★ Insight blocks** generated during session
- **Error patterns** - mistakes that were corrected
- **Tool misuse** - wrong tool selected, had to switch
- **User corrections** - when user said "no, do it this way"
- **Process friction** - steps that took longer than expected

#### 3. For Each Potential Learning

Follow the 8-step workflow:

1. **Identify** - What was the insight/mistake?
2. **Investigate** - Delegate to appropriate agent:
   - `root-cause-analyst` for complex problems
   - `Explore` to search for pattern occurrences
   - `code-reviewer` to check for similar issues
   - Self-investigate for simple cases
3. **Analyze** - What is the root cause?
4. **Draft** - Write specific corrective text
5. **Present** - Show proposal to user
6. **Wait** - Get user approval (✅ / 📝 / ❌ / ⏳)
7. **Edit** - If approved, modify the target file
8. **Track** - Store in Memory MCP

#### 4. Proposal Format

Present each learning as:

```markdown
---
## 🔄 Learning Proposal

**Category**: [CODE_QUALITY | TOOL_USAGE | PROCESS | ARCHITECTURE | TESTING]

**Insight**:
[Clear description of what was discovered]

**Investigation**:
[What was investigated and by which agent]

**Root Cause**:
[Why this keeps happening - the underlying assumption/gap]

**Proposed Fix**:
- **Type**: [Memory | RULES.md | CLAUDE.md | Agent]
- **Location**: [Specific file and section]
- **Content**:
```
[Exact text/rule to add or modify]
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

#### 5. After User Decision

- **✅ Approved**: Edit the target file (RULES.md, CLAUDE.md, etc.)
- **📝 Modify**: Adjust proposal and re-present
- **❌ Reject**: Note reason in learnings index
- **⏳ Later**: Store in deferred learnings

#### 6. Update Tracking

After each learning:
1. Create/update Memory MCP entity: `Learning_[Category]_[ShortName]`
2. Update learnings index: `~/klauspython/kc/agents/double-loop-learning/data/learnings.md`

## Examples

**Standard review:**
```
User: /kc:learn
Agent: "I found 3 potential learnings from this session. Let me investigate each one..."
→ Presents proposals one by one
→ Waits for approval on each
→ Implements approved changes
```

**Specific category:**
```
User: /kc:learn --category TOOL_USAGE
Agent: "Filtering for TOOL_USAGE insights..."
→ Only shows tool-related learnings
```

**After overnight session:**
```
User: /kc:learn --review-deferred
Agent: "Found 5 deferred learnings from overnight session 2026-01-02..."
→ Presents deferred learnings for review
```

## Integration

This skill works with:
- `/sc:save` - Suggests running /kc:learn before saving session
- `git push` - Suggests reviewing learnings after pushing
- Session end - Offers to capture learnings before goodbye
