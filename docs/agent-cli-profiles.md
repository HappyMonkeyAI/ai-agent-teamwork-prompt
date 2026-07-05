# CLI agent profiles (Stephen stack)

Canonical machine-readable profiles for **grok, codex, agy, kiro, opencode**, plus **hermes** as orchestrator.

## Location

- Schema: `profiles/agent-cli-profile.schema.json`
- Profiles: `profiles/*.yaml` (one file per agent id)

## How orchestrators use this

1. **Hermes** — load `coding-cli-delegation` skill; when user does not name a CLI, call **agent-communication-mcp** `suggest_cli_for_task` or read `profiles/codex.yaml` etc.
2. **Swarm / task board** — set `AGENT_ID` to `parallel_lane_id` (e.g. `codex-lane`, `agy-lane`) when claiming tasks matched to profile.
3. **User override** — if user says "use codex", skip routing; honor explicitly.

## Routing heuristics (v0)

| Task signal | Prefer |
|-------------|--------|
| Written plan in `docs/plans/`, multi-file impl | codex or agy (parallel lanes) |
| User frustrated with subagent quality | opencode |
| MCP + tools + research + ship | grok / hermes |
| IDE session in Kiro | kiro |
| 3+ mechanical tool steps | hermes `execute_code` |
| Reasoning-heavy isolated subtask | hermes `delegate_task` |

## Updating profiles

Edit YAML here; restart not required for MCP (reads on each call). Keep in sync with Hermes skill `coding-cli-delegation`.

## See also

- `docs/plans/coordination-mcp-v2-routing.md`
- `templates/AGENTS.md` (snippet for per-repo AGENTS.md)
- `agent-communication-mcp` tools: `list_cli_profiles`, `get_cli_profile`, `suggest_cli_for_task`