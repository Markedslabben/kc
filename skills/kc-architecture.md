---
name: kc-architecture
description: Develop a refined specification for a new feature using iterative architect-reviewer workflow. Creates tight, lean specs by running 3 iterations of architect → reviewer refinement. (user)
---

# Develop a Lean Architecture Spec

You will receive a requirements document and use the Application Architect, DHH Code Reviewer, and ParkOptimizer Reviewer agents to develop a great, lean specification.

## Arguments

`$ARGUMENTS` - Path to requirements document or inline requirements

## Workflow Steps

### Step 1: Clarify Requirements

First, evaluate whether the requirements need clarification.

**Always ask at least 3 clarifying questions** to reduce ambiguity:
- What is the core problem being solved?
- What are the constraints (performance, scale, budget)?
- What existing patterns should this follow?
- What is explicitly out of scope?

Use `AskUserQuestion` tool to gather answers. Append clarifications to the requirements.

### Step 2: Fetch Documentation (if needed)

Check if external documentation is needed:
- New libraries or frameworks
- API integrations
- Cloud service documentation

If needed, use `WebFetch` to retrieve and summarize relevant docs.

### Step 3: First Iteration - Architect

Use the `kc-application-architect` agent to create the first spec iteration.

**Agent prompt template:**
```
Create a detailed implementation specification for the following requirements:

[REQUIREMENTS]

Consider:
- Data model and schema
- API design (if applicable)
- Key classes and modules
- Integration points
- Testing strategy

Save the spec to: docs/plans/YYMMDD-01a-[feature-name].md
```

**Expected output**: Comprehensive (likely bloated) first draft.

### Step 4: DHH Review - First Pass

Use the `kc-dhh-code-reviewer` agent to review the first iteration.

**Agent prompt template:**
```
Review this specification against DHH's standards for code quality:

[SPEC FROM STEP 3]

Focus on:
- Unnecessary complexity
- Over-engineering
- Reinventing the wheel
- Non-idiomatic patterns
- Test coverage requirements

Save feedback to: docs/plans/YYMMDD-01a-[feature-name]-dhh-feedback.md
```

**Expected output**: Brutal, honest feedback with specific improvements.

### Step 5: Second Iteration - Apply Feedback

Use `kc-application-architect` again with the original requirements AND DHH feedback.

**Agent prompt template:**
```
Create a refined specification applying this feedback:

[ORIGINAL REQUIREMENTS]
[DHH FEEDBACK FROM STEP 4]

Remove unnecessary complexity. Keep it lean.

Save to: docs/plans/YYMMDD-01b-[feature-name].md
```

### Step 6: ParkOptimizer Review

Use the `kc-parkoptimizer-reviewer` agent to check lean architecture compliance.

**Agent prompt template:**
```
Review this specification for lean architecture compliance:

[SPEC FROM STEP 5]

Check:
- Class density (target: <5 classes/KLOC)
- Architecture nouns (reject: Manager, Service, Handler)
- Layer depth (target: ≤3 layers)
- Thin wrappers (minimum 100 LOC per class)

Save feedback to: docs/plans/YYMMDD-01b-[feature-name]-lean-feedback.md
```

### Step 7: Third Iteration - Final Refinement

Use `kc-application-architect` one more time with all feedback.

**Agent prompt template:**
```
Create the final specification applying all feedback:

[ORIGINAL REQUIREMENTS]
[DHH FEEDBACK]
[PARKOPTIMIZER FEEDBACK]

This is the final iteration. Make it production-ready and lean.

Save to: docs/plans/YYMMDD-01c-[feature-name].md
```

### Step 8: Summary and User Approval

Notify the user that the spec is ready for review.

**Summary format:**
```
## Specification Complete

**Feature**: [name]
**Final Spec**: docs/plans/YYMMDD-01c-[feature-name].md

### Summary
[1-2 paragraphs describing the final architecture]

### Key Changes from Reviews
- DHH: [main improvements from DHH review]
- Lean: [main improvements from ParkOptimizer review]

### Metrics
- Classes: X (target: domain nouns only)
- Estimated LOC: Y
- Layer depth: Z

Ready to proceed with implementation?
```

### Step 9: Implementation (After Approval)

Once user approves, use appropriate developer agents:
- `kc-python-developer` for backend
- `kc-frontend-developer` for frontend

Instruct them to:
1. Follow the approved spec exactly
2. Write tests alongside implementation
3. Use browser testing (Playwright) for UI verification

## File Naming Convention

```
docs/
├── requirements/
│   └── YYMMDD-NN-feature-name.md    # Original requirements
└── plans/
    ├── YYMMDD-NNa-feature-name.md   # First iteration
    ├── YYMMDD-NNa-...-dhh-feedback.md
    ├── YYMMDD-NNb-feature-name.md   # Second iteration
    ├── YYMMDD-NNb-...-lean-feedback.md
    └── YYMMDD-NNc-feature-name.md   # Final iteration
```

## Anti-Pattern Guards

Throughout the workflow, enforce:

1. **No workarounds** - Fix root causes
2. **No test removal** - All features need tests
3. **No "pre-existing issues"** - Don't claim bugs existed before
4. **No over-engineering** - Keep it lean
5. **No architecture nouns** - Use domain nouns
6. **Follow CLAUDE.md** - Respect project rules

## Example Usage

```
/kc-architecture docs/requirements/260103-01-user-auth.md
```

Or inline:
```
/kc-architecture "Add user authentication with OAuth2 and JWT tokens"
```
