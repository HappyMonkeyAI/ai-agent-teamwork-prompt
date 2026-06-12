# ai-agent-teamwork

A lightweight, decentralized coordination layer for multiple AI agents working on the same codebase without a central orchestrator.

## What this repo contains

- `docs/` — usage, protocol notes, and future guidance
- `.agent-manifest.json` — machine-readable lock/state tracking (source of truth for active coordination)
- `.agent-status.md` — human-readable coordination dashboard
- `research/` — references, comparisons, and notes about related projects and approaches

## Getting started

Use the `multi-agent-coordination` skill from Hermes, or call the Python scripts in `scripts/` directly:

```bash
python3 /home/stephen/.hermes/skills/devops/multi-agent-coordination/scripts/init.py
python3 /home/stephen/.hermes/skills/devops/multi-agent-coordination/scripts/lock.py src/auth.py "Adding OAuth2 support"
python3 /home/stephen/.hermes/skills/devops/multi-agent-coordination/scripts/status.py
```

Set `AGENT_ID` per agent so locks are unambiguous.

## Goals

1. Let multiple AI agents share one local checkout safely.
2. Keep history and commits clean when needed.
3. Stay minimal, portable, and easy to drop into an existing project.
