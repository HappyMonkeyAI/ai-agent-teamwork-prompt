# ai-agent-teamwork

A lightweight, terminal-friendly coordination system for multiple AI agents building the same project together at pace.
No central orchestrator required. No special runtime. Just files, locks, and a shared task board.

**Note:** This is an early, beta-stage effort at creating a simple coordination system.

## Version
Current version: `v0.1.0-beta` (See `VERSION` file)

## How to Use This System

To coordinate multiple subagents for building a project, follow these steps:

1.  **Clone this repository**:
    ```bash
    git clone https://github.com/google/ai-agent-teamwork.git
    cd ai-agent-teamwork
    ```

2.  **Create your project directory**:
    Create a new directory for your project under the `projects/` folder:
    ```bash
    mkdir -p projects/my-new-project
    ```

3.  **Bootstrap your project**:
    Point your primary or "best" agent at the following files from the parent directory to initialize the project:
    - `setup-prompt.txt`
    - `bootstrap-project-prompt.md`

    The agent will use these to spin up the project structure, task list, manifest files, and an `AGENTS.md` file. The `AGENTS.md` file contains instructions for any subagents working on the project to work together as a "swarm."

4.  **Add subagents to the swarm**:
    You can explicitly request any CLI-capable agent (such as Claude, Codex, Gemini, Antigravity, Opencode, etc.) to join the project. Instruct them to reference the agent bootstrap prompt in the parent directory:
    - `bootstrap-agent-prompt.md`

    This ensures they will work as part of the swarm, coordinating through the manifest and task list without stepping on each other's toes.

5.  **Run the final review when the task board is done**:
    Once all tasks are complete, fire the final review prompt at the strongest available agent:
    - `final-review-prompt.md`

    This gives you one last integration pass for cross-task issues, cleanup, and validation before shipping.

## What this gives you

- A project bootstrap prompt any agent can run
- An agent bootstrap prompt that teaches any subagent how to join safely
- File locks and a manifest so parallel edits don’t clobber each other
- A self-service task board (`tasks.py`) so agents pick their own work
- Optional ADR scaffolding and research folders for project context
- **CLI agent profiles** (`profiles/`) and `templates/AGENTS.md` for codex, agy, opencode, kiro, grok routing

## CLI profiles

See `docs/agent-cli-profiles.md`. Wired into **agent-communication-mcp** (`suggest_cli_for_task`).

## How it works

1. You give one agent the **project bootstrap prompt**
   - It creates the project structure, task list, coordination scripts, and README/CONTEXT
2. You give every other agent the **agent bootstrap prompt**
   - It reads the task board, claims one task, locks the files it will edit, builds, then unlocks
3. Locks and task status live in plain files in the project root
   - Any agent can see what’s locked, in progress, done, or blocked

## Quick start

```bash
# From the project directory
python3 scripts/init.py
python3 scripts/tasks.py list
python3 scripts/tasks.py claim <task-id>
python3 scripts/tasks.py verify-complete <task-id>
python3 scripts/tasks.py unlock <file>
```

Set `AGENT_ID` per agent so locks are unambiguous.

## Changed-aware validation

Run only the validation lanes affected by changed or untracked files:

```bash
python3 scripts/check_changed.py
python3 scripts/check_changed.py --base origin/main
python3 scripts/check_changed.py --config path/to/checks.json --base <git-ref>
```

The default base is `HEAD`, which checks working-tree and untracked files. An explicit
base also includes tracked changes from that ref through the current working tree.
Matching lanes from `templates/checks.json` execute concurrently. The terminal gets a
compact pass/fail summary; complete stdout/stderr is retained under
`.tmp/check-runs/<timestamp>/`. Any failed selected lane makes the runner exit nonzero.

The configuration boundary is intentionally small: the top-level object has `version`
and `lanes`; every lane has exactly `name`, `paths`, and `command`. Commands are JSON
argument arrays and execute directly without a shell, so pipes, redirects, substitutions,
and shell metacharacters are not interpreted. The runner validates this structure and
safe lane names before execution. **Configuration is still trusted repository-local
code**: a command can invoke any executable with the current user's permissions. Review
config changes like script changes; never run a config from an untrusted branch.

Example lane:

```json
{
  "name": "python-tests",
  "paths": ["src/**/*.py", "tests/**/*.py"],
  "command": ["python3", "-m", "pytest", "tests"]
}
```

## Current CLI guidance

- `opencode` is the proven non-interactive dispatch path
- Other CLIs may work but can have sandbox or approval friction around file writes

## Goals

1. Let multiple AI agents share one local checkout safely.
2. Keep history and commits clean when needed.
3. Stay minimal, portable, and easy to drop into an existing project.
