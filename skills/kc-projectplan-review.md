---
name: projectplan-review
description: "Review and refine a project plan using iterative architect-reviewer workflow with DHH and ParkOptimizer reviewers"
category: workflow
complexity: complex
---

# Review and Refine Project Plan

Review an existing specification or project plan using iterative architect-reviewer workflow. Runs DHH and ParkOptimizer reviews, then refines the plan through multiple iterations until it meets quality standards.

## Arguments

`$ARGUMENTS` - Path to the plan/specification file to review, or inline requirements

**Flags:**
- `--review-only` - Skip iteration, just provide feedback
- `--iterations N` - Number of refinement iterations (default: 2)

## When to Use

- You have an existing spec that needs quality review and improvement
- You want to check lean architecture compliance
- You need brutal honest feedback AND automatic refinement
- Improving specs created outside the `/kc:architecture` workflow
- Validating plans before implementation

## Workflow Steps

### Step 1: Load and Analyze the Plan

Read the specification file and understand its scope:
- What feature/system does it describe?
- What tech stack is involved?
- What is the estimated complexity?
- Identify the original filename for versioning

**File versioning:**
- Original: `plan.md` → Copy to `plan-v1.md`
- After iteration 1: `plan-v2.md`
- After iteration 2: `plan-v3.md` (final)

### Step 2: DHH Code Review (First Pass)

Use the `kc-dhh-code-reviewer` agent to review the specification.

**Agent prompt template:**
```
Review this specification against DHH's standards for code quality:

[SPEC CONTENT]

Focus on:
- Unnecessary complexity and over-engineering
- Reinventing the wheel (use existing libraries!)
- Non-idiomatic patterns for the tech stack
- Missing or inadequate test coverage
- Workarounds instead of root cause fixes
- Architecture astronaut symptoms

Provide:
1. Overall assessment (1-10 score)
2. Critical issues that MUST be fixed
3. Improvements that SHOULD be made
4. Minor suggestions

Be brutally honest. Channel DHH's philosophy:
- DRY: Ruthlessly eliminate duplication
- Concise: Every line should earn its place
- Elegant: Solutions should feel natural
- Expressive: Code should read like prose
```

**Save feedback to:** `[basename]-v1-dhh-review.md`

### Step 3: ParkOptimizer Lean Review (First Pass)

Use the `kc-parkoptimizer-reviewer` agent to check lean architecture compliance.

**Agent prompt template:**
```
Review this specification for lean architecture compliance:

[SPEC CONTENT]

Check against ParkOptimizer standards:
- Class density (target: <5 classes/KLOC)
- Architecture nouns (REJECT: Manager, Service, Handler, Processor, Coordinator)
- Domain nouns (ACCEPT: Invoice, User, Product, Transaction)
- Layer depth (target: ≤3 layers)
- Minimum class size (100 LOC per class)
- Thin wrapper detection (merge or eliminate)

Metrics to calculate:
- Estimated classes vs KLOC ratio
- Import depth analysis
- Files per feature count

Provide:
1. Lean score (1-10)
2. Bloat indicators found
3. Consolidation opportunities
4. Domain noun suggestions for any architecture nouns
```

**Save feedback to:** `[basename]-v1-lean-review.md`

### Step 4: First Refinement Iteration

Use the `kc-application-architect` agent to refine the plan based on feedback.

**Agent prompt template:**
```
Refine this specification applying the reviewer feedback:

## Original Specification
[SPEC CONTENT FROM V1]

## DHH Review Feedback
[DHH FEEDBACK]

## Lean Architecture Feedback
[LEAN FEEDBACK]

Instructions:
1. Address ALL critical issues identified
2. Simplify over-engineered sections
3. Replace architecture nouns with domain nouns
4. Consolidate thin classes
5. Add missing test coverage details
6. Keep the same overall structure but make it leaner

Save the refined spec to: [basename]-v2.md
```

### Step 5: Second Review Pass

Run both reviewers again on the v2 spec:
- `kc-dhh-code-reviewer` → `[basename]-v2-dhh-review.md`
- `kc-parkoptimizer-reviewer` → `[basename]-v2-lean-review.md`

Check if scores improved. If both scores are ≥7, proceed to summary.
If scores are still <7, continue to Step 6.

### Step 6: Final Refinement (if needed)

Use `kc-application-architect` one more time:

**Agent prompt template:**
```
Create the FINAL refined specification. This is the last iteration.

## Previous Specification
[SPEC V2]

## Remaining Issues from DHH
[V2 DHH FEEDBACK - focus on unresolved items]

## Remaining Issues from Lean Review
[V2 LEAN FEEDBACK - focus on unresolved items]

Make it production-ready. No compromises on quality.

Save to: [basename]-v3-final.md
```

### Step 7: Summary Report

Create a combined summary:

```markdown
## Project Plan Review Summary

**Original file:** [path]
**Final file:** [basename]-v3-final.md
**Date:** [YYYY-MM-DD]
**Iterations:** [N]

### Score Progression
| Version | DHH Score | Lean Score | Overall |
|---------|-----------|------------|---------|
| v1 (original) | X/10 | Y/10 | Z/10 |
| v2 (refined) | X/10 | Y/10 | Z/10 |
| v3 (final) | X/10 | Y/10 | Z/10 |

### Key Improvements Made
1. [Major change 1]
2. [Major change 2]
3. [Major change 3]

### Remaining Considerations
- [Any trade-offs or notes for implementation]

### Generated Files
- `[basename]-v1.md` - Original (backup)
- `[basename]-v1-dhh-review.md`
- `[basename]-v1-lean-review.md`
- `[basename]-v2.md` - First refinement
- `[basename]-v2-dhh-review.md`
- `[basename]-v2-lean-review.md`
- `[basename]-v3-final.md` - **USE THIS**

### Verdict
[READY FOR IMPLEMENTATION / NEEDS MANUAL REVIEW]

### Next Steps
- [ ] Review final spec: `[basename]-v3-final.md`
- [ ] Implement with `/kc:parallel` or `/sc:implement`
- [ ] Run tests as specified in the plan
```

## Scoring Guide

### DHH Score
- **9-10**: Elegant, minimal, production-ready
- **7-8**: Good with minor improvements needed
- **5-6**: Acceptable but has unnecessary complexity
- **3-4**: Over-engineered, needs significant simplification
- **1-2**: Architecture astronaut territory, start over

### Lean Score
- **9-10**: ParkOptimizer-level density and clarity
- **7-8**: Good domain modeling, minor bloat
- **5-6**: Some architecture nouns, consolidation needed
- **3-4**: Too many thin classes, layer tax present
- **1-2**: Enterprise Java syndrome, major restructuring needed

### Iteration Exit Criteria
- **Both scores ≥8**: Stop, plan is excellent
- **Both scores ≥7**: Stop, plan is good enough
- **Any score <7 after 3 iterations**: Stop, flag for manual review

## Example Usage

```bash
# Full review + refinement (default)
/kc:projectplan-review docs/plans/260114-01-poweroffice-integration.md

# Review only, no refinement
/kc:projectplan-review docs/plans/my-spec.md --review-only

# More iterations for complex specs
/kc:projectplan-review docs/plans/big-refactor.md --iterations 3
```

## Anti-Pattern Detection

The reviewers will flag and the architect will fix:

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| Architecture nouns | `UserManager`, `DataService` | Use `User`, `DataStore` |
| Thin wrappers | 30-line classes | Merge into parent |
| Layer tax | Controller→Service→Repository→Model | Flatten to 2-3 layers |
| Speculative generality | Interfaces with 1 implementation | Remove interface |
| Premature abstraction | `BaseHandler` for one handler | Just use the handler |
| Test avoidance | "Tests will be added later" | Tests are required now |
| Workarounds | "Quick fix for now" | Root cause fix |

## Related Commands

- `/kc:architecture` - Full spec development from requirements (includes clarification)
- `/kc:parallel` - Parallel implementation after review passes
- `/sc:implement` - Single-threaded implementation
- `/sc:analyze` - Code analysis for existing implementations
