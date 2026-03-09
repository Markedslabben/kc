---
name: parallel-debugger
description: "Complete debugging pipeline from bug report to verified fix using parallel hypothesis testing (CONSOLIDATED AGENT)"
category: debugging
complexity: advanced
---

# /kc:parallel-debugger - Complete Debugging Pipeline (Unified Agent)

> **KC Framework Consolidated Agent**: Full debugging pipeline with built-in parallel testing engine.

**🎯 THIS IS THE ONLY PARALLEL DEBUGGING AGENT YOU NEED**

Consolidates former `parallel-test`, `parallel-tester`, and `parallel-debugger` into ONE comprehensive agent.

---

## What It Does

**Complete 6-phase debugging workflow:**

```
Bug Report
    ↓
Phase 1: Generate Hypotheses (or accept user's)
    ↓
Phase 2: Test Hypotheses in Parallel (BUILT-IN falsification testing)
    ↓
Phase 3: Confirm Root Cause
    ↓
Phase 4: Design Solution
    ↓
Phase 5: Implement Fix
    ↓
Phase 6: Validate & Add Tests
    ↓
Verified Fix + Regression Tests
```

---

## Three Modes

### 1. **Full Pipeline** (Default)
```
/kc:parallel-debugger "Login fails intermittently"

# Complete workflow: Bug → Verified Fix
# All 6 phases executed
```

### 2. **Test-Only Mode**
```
/kc:parallel-debugger --test-only "API timeout" \
  --hypotheses "H1: pool, H2: cache, H3: network"

# Just test hypotheses (no fix)
# Stops after Phase 2
# Output: Which hypotheses survived/falsified
```

### 3. **Analyze Mode**
```
/kc:parallel-debugger --analyze "Memory leak in worker"

# Test + identify root cause (no fix)
# Stops after Phase 3
# Output: Root cause identified
```

---

## Built-In Parallel Testing

**No need for separate parallel-tester agent!**

Uses **Karl Popper's falsification method**:
- Design tests that would DISPROVE each hypothesis
- Execute tests in parallel using git worktrees
- Classify: FALSIFIED (eliminated) or SURVIVED (likely correct)

**Overhead-optimized:**
```
Parallelizes only when:
  parallel_time < sequential_time

Example (5 hypotheses @ 60s each):
  Sequential: 300s
  Parallel: 68s (overhead accounted for)
  Speedup: 4.4x faster
```

---

## Usage Examples

### Example 1: Full Debugging
```bash
/kc:parallel-debugger "Auth service rejects valid sessions randomly"

# Agent will:
# 1. Generate 5 hypotheses about the cause
# 2. Test all 5 in parallel using git worktrees
# 3. Identify root cause from survivors
# 4. Design optimal fix strategy
# 5. Implement the fix
# 6. Validate with regression tests

# Output: Verified fix with tests
```

### Example 2: Just Test Hypotheses
```bash
/kc:parallel-debugger --test-only "API timeouts under load" \
  --hypotheses "H1: DB connection pool exhaustion, H2: cache miss storm, H3: network latency"

# Agent will:
# 1. Test 3 hypotheses in parallel
# 2. Report which survived/falsified

# Output:
#   H1: SURVIVED (likely root cause)
#   H2: FALSIFIED (not the problem)
#   H3: FALSIFIED (not the problem)
```

### Example 3: Find Root Cause (No Fix)
```bash
/kc:parallel-debugger --analyze "Memory leak in background worker"

# Agent will:
# 1. Generate hypotheses
# 2. Test in parallel
# 3. Confirm root cause

# Output: Root cause identified (no implementation)
```

### Example 4: Resume Interrupted Session
```bash
/kc:parallel-debugger --resume SESSION_ID

# Continues from last saved phase
```

---

## Key Features

✅ **Unified Agent** - No confusion about which agent to use
✅ **Built-In Parallel Testing** - No separate parallel-tester needed
✅ **Three Modes** - test-only, analyze, or full pipeline
✅ **Falsification Method** - Scientific hypothesis elimination
✅ **Overhead-Optimized** - Only parallelizes when beneficial
✅ **Session Persistence** - Resume interrupted sessions
✅ **Specialist Orchestration** - Routes to domain experts (python-expert, backend-architect, etc.)
✅ **Regression Tests** - Always adds tests for fixed bugs

---

## Configuration

```yaml
parallel_debugger:
  default_mode: full              # full | analyze | test-only
  max_hypotheses: 5
  test_timeout: 300               # Seconds per test
  min_test_time_for_parallel: 60
  require_regression_test: true
```

---

## Migration from Old Agents

**DEPRECATED** (now aliases to this agent):
- ❌ `parallel-test` → Use `/kc:parallel-debugger --analyze`
- ❌ `parallel-tester` → Use `/kc:parallel-debugger --test-only`

**NEW CONSOLIDATED AGENT:**
- ✅ `/kc:parallel-debugger` - Does everything

---

## Behind the Scenes

This command executes:
```
Use the Task tool with subagent_type='parallel-debugger' for complete debugging pipeline
```

The agent internally handles:
- Hypothesis generation (Phase 1)
- Parallel testing with git worktrees (Phase 2)
- Root cause analysis (Phase 3)
- Solution design (Phase 4)
- Implementation (Phase 5)
- Validation (Phase 6)

No need for separate agents or manual orchestration.

---

## See Also

- `/kc:root-cause-analyst` - If you only need hypothesis generation
- `/kc:quality-engineer` - If you only need testing strategies
- `/kc:python-expert` - If you have the fix and just need implementation

---

**Version**: 2.0 (Consolidated Agent)
**Replaces**: parallel-test, parallel-tester, parallel-debugger (old architecture)
