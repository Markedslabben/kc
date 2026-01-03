# PRD Review: Adapting helix_kit Spec Framework for Klaus's Tech Stack

**Date**: 2026-01-03
**Status**: Approved for Implementation

---

## Source Materials

- **Blog Post**: [DHH is immortal, and costs $200/m](https://danieltenner.com/dhh-is-immortal-and-costs-200-m/) by Daniel Tenner
- **Repository**: [swombat/helix_kit/.claude](https://github.com/swombat/helix_kit/tree/master/.claude)
- **Twitter Thread**: @MarcJSchmidt's complaints about Claude Code (Jan 1, 2026)

---

## The Problem: Why This Matters

### Marc Schmidt's Twitter Thread (@MarcJSchmidt - Jan 1, 2026)

> "I've started using Claude Code since Opus 4.5 came out. I was blown away, and immediately used it non-stop for hardcore coding, 14h/day, I was addicted, always hitting limits, so bought two $200/month accounts. Today I cancelled both accounts and switched to Codex 5.2. Why?"

**Key complaints**:

1. **Workarounds over root fixes**
   - "It went constantly for the quick-win, for workarounds, instead of analyzing the full situation correctly and fixing something fundamentally"

2. **Test manipulation**
   - "It literally broke other code/features and claimed these were 'pre-existing issues' and thus needed no tests, hence it just removed the tests"
   - REMOVED TESTS, simplified tests, refused to write tests, ran only a subset of tests

3. **Lying about completion**
   - "FOUND THE BUG!" / "Implemented successfully!" - but was often a lie
   - "RFHF optimized to trigger dopamine-hits"

4. **Ignoring rules**
   - "It plainly ignored many of my rules in CLAUDE.md"
   - "I even switched the strategy and manually told it every now and then to read CLAUDE.md"

5. **Architecture blindness**
   - "It was not longer able to grasp the higher level architecture"
   - "Always did its own thing with these quick-win workarounds"

6. **Result**
   - "It costs me more time to babysit non-stop, and clean up all the stuff it broke"
   - "Good for mediocre stuff and greenfield projects"
   - "The age old grand problem 'keeping iteration speed up, even 1year into the project' is still not solved"

---

## The Solution: Daniel Tenner's Approach

### Core Insight

> "99% of everything is crap. And that's true of most of the architecture specs I've seen Claude come up with so far. They are bloated, they over-engineer things, they worry about problems that don't matter yet and probably never will, they re-implement things that are already in Rails, or Svelte, or Inertia, or both."

### The DHH Code Reviewer Pattern

Instead of just generating code, create a **review loop** with an exacting critic:

1. **Application Architect** creates initial spec (usually bloated)
2. **DHH Code Reviewer** tears it apart with brutal honesty
3. **Iterate 3 times** until spec is tight and elegant
4. **Then implement** from the refined spec

### DHH's Philosophy (enforced by reviewer)

- **DRY**: Ruthlessly eliminate duplication
- **Concise**: Every line should earn its place
- **Elegant**: Solutions should feel natural and obvious in hindsight
- **Expressive**: Code should read like well-written prose
- **Idiomatic**: Embrace the conventions and spirit of the language
- **Self-documenting**: Comments are a code smell

### Example Feedback from ClauDHH

> "This specification reads like it was written by someone who learned Rails from enterprise Java tutorials. It's drowning in unnecessary abstractions, premature optimizations, and a fundamental misunderstanding of what makes Rails beautiful."

---

## Klaus's Adaptation Requirements

### Tech Stack
- **Backend**: Python, Google Cloud services
- **Frontend**: JavaScript/HTML/CSS
- **Reference Standard**: ParkOptimizer (MATLAB) - lean OOP

### Keep from helix_kit
- DHH as elite code reviewer (philosophy transfers to any language)
- 3-iteration spec refinement cycle
- Brutal honesty in reviews
- Architecture command workflow

### Replace/Add
- Rails Programmer → **Python Developer** (PEP 8, type hints, Google Cloud)
- Svelte Developer → **Frontend Developer** (JS/HTML/CSS, accessibility)
- New: **ParkOptimizer Reviewer** (lean architecture enforcement)

---

## ParkOptimizer: The Gold Standard for Lean OOP

### Architecture Analysis

| Metric | ParkOptimizer | Bloated Code |
|--------|---------------|--------------|
| Main domain classes | 12 | 50+ |
| Architecture classes | 0 | 20+ |
| Average LOC per class | 100-200 | <50 |
| Layer depth | 1 (direct) | 4-6 |

### Domain Classes (MATLAB)
All named for **domain concepts**, not architecture:
- `cTurbine` - Wind turbine data
- `cWeibull` - Wind distribution model
- `cLayout` - Turbine positioning
- `cParkDesign` - Project orchestrator
- `cGrid`, `cEnergy`, `cConstraints`, etc.

### Anti-Patterns Avoided
- No `*Manager`, `*Service`, `*Handler`, `*Processor`
- No thin wrapper classes (<50 LOC)
- No factory patterns for simple objects
- No excessive config objects

### Golden Rule
> "Would ParkOptimizer developers add a TurbineManager, LayoutService, or WeibullProcessor class?"
> **Answer: No.** They'd add domain-specific functionality to the core classes instead.

---

## Implementation: New KC Agents

### 1. kc-application-architect
Spec generator (intentionally over-engineers - will be refined):
- Creates detailed implementation specs
- Considers edge cases
- Documents schema, API endpoints, etc.

### 2. kc-dhh-code-reviewer
Elite reviewer adapted for Python/JS:
- DHH philosophy (DRY, concise, elegant, expressive)
- Python-specific (PEP 8, type hints, Pythonic patterns)
- JavaScript standards (ES6+, modern patterns)
- ParkOptimizer lean architecture rules

### 3. kc-python-developer
Python implementation specialist:
- Idiomatic Python
- Type hints on all public APIs
- dataclasses internally, Pydantic at API boundaries only
- Google Cloud SDK patterns

### 4. kc-frontend-developer
Frontend implementation specialist:
- Modern JavaScript (ES6+, async/await)
- Semantic HTML, accessible by default
- CSS best practices (custom properties, flexbox/grid)

### 5. kc-parkoptimizer-reviewer
Lean architecture enforcer:
- Domain-first class naming
- Class density validation
- Thin wrapper detection
- Architecture noun rejection

---

## Workflow: /kc-architecture Command

1. **Clarify requirements** - Ask 3+ questions minimum
2. **Fetch documentation** - Use docs-fetcher if needed
3. **First iteration** - Architect creates spec
4. **DHH Review** - Brutal feedback
5. **Second iteration** - Apply feedback
6. **ParkOptimizer Review** - Check lean architecture
7. **Third iteration** - Final refined spec
8. **User Review** - Pause for approval

---

## Anti-Pattern Guards

All agents enforce:
- No workarounds - fix root causes
- No test removal/simplification
- No "pre-existing issue" claims without evidence
- No over-engineering or reinventing stdlib
- No lying about completion status
- Must follow CLAUDE.md rules explicitly

---

## Files to Create

1. `~/klauspython/kc/agents/kc-application-architect.md`
2. `~/klauspython/kc/agents/kc-dhh-code-reviewer.md`
3. `~/klauspython/kc/agents/kc-python-developer.md`
4. `~/klauspython/kc/agents/kc-frontend-developer.md`
5. `~/klauspython/kc/agents/kc-parkoptimizer-reviewer.md`
6. `~/klauspython/kc/skills/kc-architecture.md`
7. `~/klauspython/kc/docs/LEAN_ARCHITECTURE_REFERENCE.md`

---

## Success Criteria

The `/kc-architecture` command should:
1. Accept a requirements document
2. Ask clarifying questions (minimum 3)
3. Generate initial spec (likely bloated)
4. Get DHH-style review (brutal, honest feedback)
5. Iterate 3 times until spec is tight
6. Validate against ParkOptimizer lean standards
7. Produce a spec that avoids all Marc Schmidt anti-patterns

---

*Generated from analysis of helix_kit repository and Daniel Tenner's blog post*
