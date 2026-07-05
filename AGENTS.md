# AGENTS.md — ai-agent-teamwork-prompt

This repo is the **canonical home** for swarm templates and **CLI agent profiles** (`profiles/*.yaml`).

Subprojects copy `templates/AGENTS.md` into their root during bootstrap.

## Profile routing

See `docs/agent-cli-profiles.md`. Orchestrators should call **agent-communication-mcp** `suggest_cli_for_task` when choosing codex vs agy vs opencode.

## Workers

This repo rarely uses the task board; doc changes are single-agent unless user requests swarm mode.