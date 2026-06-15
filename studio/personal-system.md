# Personal System — Local Agent Tooling and Endpoints

This slot documents the user’s local machine setup that swarm workers should assume exists.

## Model endpoint

- LM Studio: `http://192.168.5.157:1234`
- OpenAI-compatible: `http://192.168.5.157:1234/v1`
- Prefer local model `google/gemma-4-12b-qat` unless another is specified

## Available CLIs

All in PATH or under local bin directories:

- `opencode` — `/home/stephen/.opencode/bin/opencode`
- `gemini` — `/home/stephen/.nvm/versions/node/v22.22.2/bin/gemini`
- `agy` — `/home/stephen/.local/bin/agy`
- `codex` — `/home/stephen/.nvm/versions/node/v22.22.2/bin/codex`

## Dispatch guidance

- Use `gemini` headless (`gemini -p`) for free text/code tasks
- Use `agy --print` as secondary free worker
- Use `opencode run` for non-interactive one-shot tasks
- Use `codex` interactively when richer terminal tool use is needed

## Home directories

- Projects target: `/home/stephen/projects/`
- Web project reference area: `/home/stephen/Documents/www/`

## Notes

- Node via nvm
- Python3 available
- Git available
