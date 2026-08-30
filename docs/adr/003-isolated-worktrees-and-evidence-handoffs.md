# ADR-003: Isolated worktrees and evidence-bearing handoffs

## Status

Accepted

## Context

Parallel agents can silently overwrite dirty changes, work from the wrong branch, or report a focused check as if it were full acceptance. Branch mode alone does not prevent workspace collisions, and a task-board status is not proof that the integrated result works.

## Decision

In branch mode, implementation agents use one isolated Git worktree under `.worktrees/<task-id>` and one `agent/<task-id>` branch per task. Delegators provide a self-contained context pack with repository path, baseline, dependencies, owned files, constraints, and verification commands.

Every worker handoff must include the absolute worktree and branch, exact changed paths, commands and real results, known failures/skips, and commit/push status. The parent/orchestrator independently reviews the final tree and owns final acceptance. Focused checks remain labeled as focused checks.

Pre-existing dirty changes and generated artifacts are preserved and excluded from commits unless explicitly in scope.

## Consequences

- Parallel implementation is safer and branch history remains reviewable.
- Worktree setup and handoff reporting add a small amount of process overhead.
- A task cannot be considered accepted solely because a worker reports success or the task board is complete.