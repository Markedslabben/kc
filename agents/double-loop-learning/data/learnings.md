# Learnings Index

This file tracks all learnings captured by the double-loop-learning agent.

## Active Learnings

| Date | Category | Short Name | Prevention Location | Status |
|------|----------|------------|---------------------|--------|
| 2026-01-02 | CODE_QUALITY | Pydantic boundaries | RULES.md | Proposed |
| 2026-01-02 | TOOL_USAGE | WSL Chrome first | CLAUDE.md | Proposed |

## Pending Approval

*Learnings awaiting user decision*

| Date | Category | Short Name | Proposed Action |
|------|----------|------------|-----------------|
| 2026-01-02 | CODE_QUALITY | Pydantic boundaries | Add RULES.md section |
| 2026-01-02 | TOOL_USAGE | WSL Chrome first | Strengthen CLAUDE.md rule |

## Implemented

*Learnings that have been implemented*

| Date | Category | Short Name | File Modified | Commit |
|------|----------|------------|---------------|--------|
| - | - | - | - | - |

## Rejected/Deferred

| Date | Category | Short Name | Reason | Decision |
|------|----------|------------|--------|----------|
| - | - | - | - | - |

## Deferred Learnings (Overnight Sessions)

*Learnings collected during overnight mode, pending morning review*

| Session Date | Count | Status |
|--------------|-------|--------|
| - | - | - |

---

## Learning Details

### Learning_CODE_QUALITY_PydanticBoundaries

**Problem**: Pydantic overused in internal code causing bloat and complexity
**Root Cause**: AI coding agents default to Pydantic as "best practice" without considering validation needs
**Solution**: Use Pydantic only at API boundaries; use dataclass/NamedTuple for internal structures
**Date**: 2026-01-02
**Status**: Proposed
**Prevention**: RULES.md - Code Quality section

### Learning_TOOL_USAGE_WSLChromeFirst

**Problem**: Chrome DevTools repeatedly connecting to Windows Chrome instead of WSL Chrome
**Root Cause**: Claude Code runs in WSL; localhost refers to WSL localhost, not Windows
**Solution**: Always try WSL Chrome (port 9223) first; use ensure-chrome.sh 9223
**Date**: 2026-01-02
**Status**: Proposed
**Prevention**: CLAUDE.md - Chrome DevTools section
