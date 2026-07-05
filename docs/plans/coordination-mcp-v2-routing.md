# Plan: coordination MCP v2 — CLI profile routing

**Status:** Phase A shipped (profiles + MCP tools)  
**Repos:** `ai-agent-teamwork-prompt` (canonical data), `agent-communication-mcp` (tools)

## Goal

Let LAN/Hermes agents **pick the right CLI worker** without tribal knowledge, while keeping user overrides sacred.

## Phase A (done)

- [x] YAML profiles + JSON schema in teamwork repo
- [x] Docs + `AGENTS.md` template + bootstrap hints
- [x] MCP: `list_cli_profiles`, `get_cli_profile`, `suggest_cli_for_task`
- [x] Env `AGENT_CLI_PROFILES_DIR` (default `~/projects/ai-agent-teamwork-prompt/profiles`)

## Phase B (next)

- [ ] Hermes skill patch: point `coding-cli-delegation` at MCP suggest tool
- [ ] Kanban worker prompt: call suggest before spawning codex/agy
- [ ] `submit_task` optional field `preferred_cli_profile` validated against profiles
- [ ] Launcher registry: expose profile dir path in project metadata for agents

## Phase C (later)

- [ ] Learned routing from task outcomes (do not auto-write without user OK)
- [ ] A2A agent cards link `cli_profile_id` for dev-agent/server-agent

## Non-goals

- Replacing Hermes `delegate_task` with external CLIs
- Auto-spawning CLIs without locks on shared repos