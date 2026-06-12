# CONTEXT — ai-agent-teamwork

## Stack and runtime assumptions

- Linux host with Python 3.9+
- Repo is managed with git
- Agents may be Hermes, Codex, Gemini CLI, or similar terminal-based tools
- Project uses plain files and shell tooling by default

## Non-negotiable rules

- Do not edit files another agent is working on without explicit coordination.
- Use the manifest for rapid prototyping and swarm builds.
- Use git branches when clean merge history matters.
- Update docs in the same change as related code or workflow changes.

## Workflow protocols

### Manifest mode (rapid swarm)

- Run `init.py` once per repo.
- Acquire locks before editing files.
- Heartbeat long tasks.
- Clean up stale locks before committing.

### Branch mode (clean history)

- Each agent works in its own branch or cloned workspace.
- Merge only after an agent reports task complete.
- Rebase onto main before merge to keep history linear.

## Resolved architecture decisions

- Coordination metadata uses JSON rather than shell scripts.
- Agents are identified via `AGENT_ID` env var or `.agent-session.json`.
- Manifest files are tracked in `.gitignore` for local-only coordination.

## What not to do

- Do not use manifest mode when mergeable branch history is required.
- Do not share `AGENT_ID` between agents.
- Do not force-unlock a lock younger than 10 minutes without confirmation.
