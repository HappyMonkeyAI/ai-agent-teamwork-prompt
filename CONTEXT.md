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

- Each implementation agent works in its own Git worktree under `.worktrees/<task-id>` and on an `agent/<task-id>` branch. A separate clone is acceptable when worktrees are unavailable.
- Before editing, confirm the worktree, branch, baseline commit, task ownership, and declared file scope.
- Preserve pre-existing dirty changes; never reset, clean, stash, or overwrite another agent's work without explicit coordination.
- Merge only after an agent reports task complete.
- Rebase onto main before merge to keep history linear.
- The parent/orchestrator performs final integration verification; a worker report is not acceptance evidence by itself.

### Subagent context and handoff

- Every delegated task receives a self-contained context pack: repository/worktree path, task goal, dependencies, owned files, relevant symbols, baseline verification, constraints, and exact expected commands.
- Workers return an evidence-bearing handoff with the worktree/branch, exact changed paths, tests/build/typecheck output, known failures, and commit/push status.
- Focused tests, partial runs, and successful compilation must be labeled as such; they must not be reported as full acceptance.
- Generated reports, screenshots, logs, and test artifacts stay out of commits unless explicitly required.

## Resolved architecture decisions

- Coordination metadata uses JSON rather than shell scripts.
- Agents are identified via `AGENT_ID` env var or `.agent-session.json`.
- Manifest files are tracked in `.gitignore` for local-only coordination.

## What not to do

- Do not use manifest mode when mergeable branch history is required.
- Do not share `AGENT_ID` between agents.
- Do not force-unlock a lock younger than 10 minutes without confirmation.
