# /parallel - Parallel Orchestrator with Overhead Optimization

Orchestrate parallel Claude Code sessions using git worktrees with intelligent overhead-aware task splitting.

## Key Features

- **Dynamic splitting**: 1-10 subtasks based on overhead analysis (no hardcoded limits)
- **Break-even calculation**: Only parallelizes when efficiency gain exceeds overhead
- **Complexity scoring**: Analyzes repo structure to determine max possible splits
- **Resource validation**: Checks available worktrees and concurrent session limits

## Invocation

```bash
/parallel <task-description>                    # Analyze with overhead optimization
/parallel --task-scope large <task>             # Specify task size for time estimation
/parallel --max-splits 6 <task>                 # Override maximum splits
/parallel --tasks "branch1,branch2,branch3"     # Quick setup for known branches
/parallel --check branch1 branch2               # Check conflicts between branches
/parallel --analyze-repo                        # Analyze repo for parallelization
```

## Task Scope Options

| Scope | Base Time | Use Case |
|-------|-----------|----------|
| `small` | 5-15 min | Quick fixes, single component |
| `medium` | 20-60 min | Feature additions, moderate changes |
| `large` | 1-3 hours | Refactoring, multi-component work |
| `xlarge` | 3+ hours | Migrations, major rewrites |

---

## Workflow

### Step 1: Determine Mode
Parse arguments:
- Has `--tasks`? → Quick Setup mode
- Has `--check`? → Conflict Check mode
- Has `--analyze-repo`? → Repository Analysis mode
- Otherwise → Overhead-Optimized Analysis mode

### Step 2: Execute Based on Mode

**Overhead-Optimized Analysis Mode (default):**
```bash
python3 ~/klauspython/parallel-orchestrator/scripts/task-splitter.py \
  --task-scope medium \
  "Task description"
```

Output includes:
```
============================================================
OVERHEAD ANALYSIS
============================================================
Estimated sequential time: 45 min
Recommended splits: 4
Break-even at: 2 splits
Estimated parallel time: 16.4 min
Overhead: 2.9 min
Efficiency gain: 64%
Recommendation: Optimal: 4 parallel tasks saves 64% time
```

**Quick Setup Mode:**
```bash
setup-worktree.sh <branches>
run-parallel.sh --tasks "<branches>"
```

**Conflict Check Mode:**
```bash
merge-results.sh --branches "<branches>" --dry-run
```

**Repository Analysis Mode:**
```bash
python3 ~/klauspython/parallel-orchestrator/scripts/task-splitter.py --analyze-repo
```

---

## Overhead Model

```
Per-session overhead:
├── Worktree creation:    8 sec
├── Session startup:      5 sec
├── Context building:    20 sec
└── Merge per branch:    10 sec

Total: ~43 seconds per parallel session
```

### Break-Even Calculation

```
For a 30 min task:

Splits | Execution | Overhead | Total   | Savings
-------|-----------|----------|---------|--------
  1    |  30.0 min |  0.0 min | 30.0    |   0%
  2    |  18.0 min |  1.4 min | 19.4    |  35%
  3    |  12.0 min |  2.2 min | 14.2    |  53%
  4    |   9.0 min |  2.9 min | 11.9    |  60% ← Optimal
  5    |   7.2 min |  3.6 min | 10.8    |  64%
  6    |   6.0 min |  4.3 min | 10.3    |  66% (diminishing returns)
```

---

## Decision Rules

### Parallelize When:
- Estimated efficiency gain > 15%
- Task has independent components
- No file overlaps between subtasks
- Resource constraints not exceeded

### Do NOT Parallelize When:
- Task < 5 minutes (overhead exceeds benefit)
- Single file modifications
- Tightly coupled components
- Sequential dependencies exist
- conflict_risk == HIGH

---

## Example Outputs

### Task Analysis (with overhead)
```
/parallel "Add user profile feature with avatar upload"

============================================================
OVERHEAD ANALYSIS
============================================================
Estimated sequential time: 45 min
Recommended splits: 4
Break-even at: 2 splits
Estimated parallel time: 16.2 min
Overhead: 2.9 min
Efficiency gain: 64%

============================================================
SUBTASKS
============================================================
1. profile-backend
   Files to modify: src/api/profile.py, src/models/profile.py
   Complexity: medium
   Estimated time: 15 min

2. profile-frontend
   Files to modify: src/components/Profile/
   Complexity: medium
   Estimated time: 12 min

3. avatar-upload
   Files to create: src/services/upload.py
   Complexity: low
   Estimated time: 10 min

4. profile-tests
   Files to create: tests/test_profile.py
   Complexity: low
   Estimated time: 8 min

Merge order: profile-backend → avatar-upload → profile-frontend → profile-tests

============================================================
COMMANDS TO EXECUTE
============================================================
# Create worktrees:
setup-worktree.sh profile-backend profile-frontend avatar-upload profile-tests

# Run in parallel:
run-parallel.sh --tasks "profile-backend,profile-frontend,avatar-upload,profile-tests"

# Expected efficiency:
#   Sequential: ~45 min
#   Parallel:   ~16 min
#   Savings:    ~64%
```

### Small Task (not worth parallelizing)
```
/parallel --task-scope small "Fix typo in README"

============================================================
OVERHEAD ANALYSIS
============================================================
Estimated sequential time: 5 min
Recommended splits: 1
Recommendation: Task too small (5 min < 5.0 min threshold)

Sequential execution recommended - overhead would exceed benefit.
```

### Repository Analysis
```
/parallel --analyze-repo

============================================================
REPOSITORY ANALYSIS
============================================================
Total files: 127
Estimated LOC: 19,050
Modules: 8
Complexity score: 0.67
Max recommended parallel: 6

Modules:
  src: 45 files [✓]
  tests: 32 files [✓]
  components: 28 files [⚠ 2 recent]
  api: 12 files [✓]
  utils: 10 files [✓]

Parallelization opportunities:
  src: 45 files [SAFE]
  tests: 32 files [SAFE]
  api: 12 files [SAFE]

Resource limits:
  Existing worktrees: 2
  Max concurrent: 8
```

---

## Scripts Location

All scripts in: `~/klauspython/parallel-orchestrator/scripts/`

```bash
# Ensure PATH includes scripts
export PATH="$PATH:$HOME/klauspython/parallel-orchestrator/scripts"
```

---

## Configuration

The overhead model can be customized in `task-splitter.py`:

```python
@dataclass
class ParallelConfig:
    # Overhead times (seconds)
    worktree_creation_time: float = 8.0
    session_startup_time: float = 5.0
    context_building_time: float = 20.0
    merge_time_per_branch: float = 10.0

    # Resource limits
    max_concurrent_sessions: int = 8
    max_worktrees: int = 15
    min_files_per_subtask: int = 2

    # Break-even thresholds (minutes)
    min_task_time_for_2_splits: float = 5.0
```

---

## See Also

- Agent documentation: `~/.claude/AGENTS.md` (parallel-orchestrator-agent)
- Scripts: `~/klauspython/parallel-orchestrator/scripts/`
- README: `~/klauspython/parallel-orchestrator/README.md`
