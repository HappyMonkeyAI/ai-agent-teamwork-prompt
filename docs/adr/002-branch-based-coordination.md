# ADR-002: Branch-based coordination extension

## Status

Accepted

## Context

Manifest mode is fast but produces messy commit history when multiple agents contribute to the same repo. For higher-quality deliverables, we want clean merges and reviewable commits.

## Decision

Support a branch-based workflow where each agent works in its own branch or isolated workspace. An orchestrator is responsible for merging branches and resolving conflicts. Manifest mode remains the default for rapid prototyping, and branch mode is selected when the user requests clean history.

## Consequences

- Requires explicit merge/rebase steps.
- Adds complexity but preserves commit hygiene.
- Works well with the orchestrator pattern already used in this repo.
