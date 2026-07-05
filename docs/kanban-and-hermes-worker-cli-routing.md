# Kanban + Hermes worker — CLI routing (Phase B)

When a **coding** card lands on a worker that can use `terminal` (or reads tasks from **agent-communication-mcp**):

## 1. Pin or suggest

- Task has **`preferred_cli_profile`** (from `submit_task`) → use that profile; call `get_cli_profile(id)` for `invoke` templates.
- User named a CLI in the card → **override** everything.
- Else → **`suggest_cli_for_task(description=card body or instructions)`** on agent-communication-mcp.

## 2. Parallel lanes (one repo)

- Set swarm **`AGENT_ID`** to profile **`parallel_lane_id`** (`codex-lane`, `agy-lane`).
- Non-overlapping `files` in `.agent-tasks.json`; serialize hub files.

## 3. Spawn

Use `invoke.one_shot` from the profile YAML (`{workdir}`, `{prompt}`). Hermes: `terminal(..., pty=needs_pty)` per `coding-cli-delegation`.

## 4. Verify

`git status`, plan tests; agy exit 0 + clean tree = no-op.

## Bootstrap

`get_coordination_bootstrap` on agent-communication-mcp returns paths from **launcher-project-registry** `agent_coordination` block.