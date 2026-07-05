# AGENTS.md — multi-agent swarm (template)

Copy into your project root when using **ai-agent-teamwork-prompt** coordination. Customize project name only; keep coordination + routing sections.

## Role

You are a swarm worker on this repo. Coordinate via **tasks.py / lock.py**, not ad-hoc edits.

## Before editing files

1. `python3 scripts/tasks.py list` — pick an unclaimed task.
2. `python3 scripts/tasks.py claim <task-id>`
3. `python3 scripts/lock.py <files...> "<reason>"`
4. Read `CONTEXT.md` and this file.

## CLI agent routing (Stephen stack)

Profiles live in the parent teamwork repo:

`~/projects/ai-agent-teamwork-prompt/profiles/`

| If you are… | Set `AGENT_ID` | Profile id |
|-------------|----------------|------------|
| OpenAI Codex CLI | `codex-lane` | codex |
| Antigravity (agy) | `agy-lane` | agy |
| OpenCode | `opencode-lane` | opencode |
| Kiro IDE agent | `kiro-lane` | kiro |
| Hermes / Grok operator | `hermes-primary` | grok / hermes |

**Rules:**

- If the **user named a CLI**, use that CLI — do not reroute.
- For **parallel lanes** on one repo: non-overlapping `files` in `.agent-tasks.json`; hub files (e.g. `server.py`) serialize or leave wiring to Hermes.
- After any CLI run: **verify** with git status, tests, and task `verify-complete` — not exit code alone.

**MCP:** `agent-communication-mcp` → `suggest_cli_for_task(description=...)` for automated hints.

## Completing work

- Run build/tests from the task definition.
- `python3 scripts/tasks.py verify-complete <task-id>`
- `python3 scripts/unlock.py <files...>`

## Do not

- Edit `.agent-tasks.json` by hand.
- Force-unlock locks younger than 10 minutes without confirmation.
- Refactor outside the claimed task scope.