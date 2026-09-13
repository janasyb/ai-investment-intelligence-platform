# AIIP ChatGPT Development Handoff System

**Status:** Active
**Owner:** AIIP Technologies
**Repository:** `ai-investment-intelligence-platform`
**Product:** AI Investment Intelligence Platform for Digital Assets

## Purpose

This document defines how AIIP development is handed from one ChatGPT session to another.

The repository, Git history, specifications, tests, and this handoff system are the source of truth.
ChatGPT conversation history is supporting context only.

## Source-of-Truth Hierarchy

When information conflicts, use this order:

1. Current source code in the repository
2. Passing automated tests and CI results
3. Git history and current branch state
4. Current approved specifications in `specs/` and `docs/`
5. `docs/development/CURRENT_STATE.md`
6. Other project documentation
7. Previous ChatGPT conversation context
8. ChatGPT assumptions

Never override repository evidence with conversational assumptions.

## Mandatory Start-of-Session Procedure

Before changing code, the AI assistant must establish:

- repository root
- current branch
- Git working-tree status
- latest commits
- current AIIP version/release
- active module/workstream
- current objective
- relevant specification
- relevant architecture decision records
- current tests/build status
- known blockers
- explicit next task

If any of these are unknown, inspect the repository before implementing.

## Mandatory Development Rules

1. Do not make speculative architectural changes.
2. Do not rewrite unrelated code.
3. Work on one coherent module/task at a time.
4. Read the relevant specification before implementation.
5. Preserve backward compatibility unless the specification explicitly changes it.
6. Add or update tests with implementation changes.
7. Run the relevant formatter, linter, type checker, and tests.
8. Do not claim a task is complete when validation has not passed.
9. Update `CURRENT_STATE.md` before handing work to another session.
10. Keep the working tree clean at a completed handoff unless an explicit WIP state is recorded.
11. Never expose secrets, API keys, private keys, seed phrases, credentials, or personal financial-account information.
12. Never silently change product requirements because a task is difficult.
13. If a requirement is ambiguous and could materially affect architecture, stop and document the ambiguity before implementation.
14. Prefer a small, reversible change over a broad refactor.

## Change Authorization

ChatGPT may:

- inspect the repository
- analyze existing implementation
- implement an explicitly approved task
- add/update tests
- update technical documentation required by the task
- update the handoff state
- propose architectural changes

ChatGPT must not silently:

- change the company/product strategy
- change security boundaries
- change public API contracts
- change database schemas with destructive consequences
- remove working functionality
- introduce a new infrastructure dependency
- change production deployment configuration
- mark a release production-ready

Such changes require explicit approval or an already-approved specification/ADR.

## Definition of Done

A task is complete only when:

- implementation matches the approved requirement
- relevant tests exist
- relevant tests pass
- formatting passes
- linting passes
- type checking passes where applicable
- `git diff --check` passes
- documentation is updated when required
- `CURRENT_STATE.md` is updated
- Git status is understood
- next handoff is unambiguous

## Handoff Rule

At the end of every meaningful development session, update:

`docs/development/CURRENT_STATE.md`

The next session must begin from that file plus repository/Git verification.

## Recovery Rule

If `CURRENT_STATE.md` conflicts with the actual repository:

- trust the repository and Git evidence
- correct `CURRENT_STATE.md`
- record the correction in the handoff notes
- do not continue based on stale state

## Session Command Baseline

From the repository root:

```powershell
git status --short
git branch --show-current
git log --oneline -10
git diff --check
```

Then run the project's relevant validation commands before declaring completion.
