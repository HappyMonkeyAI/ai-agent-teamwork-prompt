# ADR-001: Local file-locking coordination protocol

## Status

Accepted

## Context

Multiple AI agents need to work on one local checkout without overwriting each other. We want a lightweight, portable mechanism without introducing a central server or heavy tooling.

## Decision

Use a repo-root manifest (`.agent-manifest.json`) with Python locking scripts as the primary coordination mode for rapid swarm work. Agents acquire locks before editing files, send heartbeats for long tasks, and release locks when done.

## Consequences

- Fast to adopt; minimal dependencies.
- Works well for rapid prototyping and dense parallel work.
- Does not produce clean git history by itself.
- Requires follow-up commit organization for branch-based workflows.
