# AIIP ChatGPT Session Start Protocol

Use this prompt at the beginning of every new AIIP development chat.

## Standard Start Prompt

```text
You are continuing development of AIIP Technologies.

Project:
AI Investment Intelligence Platform for Digital Assets (AIIP)

Repository:
ai-investment-intelligence-platform

Local repository:
C:\Development\AI-Investment-Intelligence-Platform

Development philosophy:
One production-ready version/module at a time.
Every completed change must remain deployable and tested.

Before making ANY code change:

1. Read:
   docs/development/CHATGPT_DEVELOPMENT_HANDOFF.md

2. Read:
   docs/development/CURRENT_STATE.md

3. Inspect the actual repository and Git state.

4. Verify:
   - current branch
   - working-tree status
   - latest commits
   - current version/workstream
   - active task
   - relevant specification
   - relevant ADRs
   - relevant source files
   - relevant tests
   - known blockers

5. Treat the repository as the source of truth.
   Do not assume that the previous chat's state is current.

6. Do not implement anything outside the authorized scope.

7. Before coding, give me a concise:
   - current-state assessment
   - task interpretation
   - files likely to change
   - validation plan

8. After implementation:
   - run relevant tests
   - run formatter/linter/type checker as applicable
   - run git diff --check
   - inspect the final diff
   - update docs/development/CURRENT_STATE.md
   - report exactly what changed and what remains

If the repository state conflicts with CURRENT_STATE.md,
trust the repository/Git evidence, correct CURRENT_STATE.md,
and explain the discrepancy before proceeding.
```

## Fast Start

For routine continuation, this shorter prompt may be used:

```text
Continue AIIP development from the repository's current state.

First read:
docs/development/CHATGPT_DEVELOPMENT_HANDOFF.md
docs/development/CURRENT_STATE.md

Then verify Git state and inspect the active specification before changing code.

Do not guess. Do not make unrelated changes. Work only on the authorized next task.
Test everything you change and update CURRENT_STATE.md before handoff.
```
