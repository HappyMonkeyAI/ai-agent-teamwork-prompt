# ai-agent-teamwork

A lightweight, terminal-friendly coordination system for multiple AI agents building the same project together.
No central orchestrator required. No special runtime. Just files, locks, and a shared task board.

## What this gives you

- A project bootstrap prompt any agent can run
- An agent bootstrap prompt that teaches any subagent how to join safely
- File locks and a manifest so parallel edits don’t clobber each other
- A self-service task board (`tasks.py`) so agents pick their own work
- Optional ADR scaffolding and research folders for project context

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

## Current CLI guidance

- `opencode` is the proven non-interactive dispatch path
- Other CLIs may work but can have sandbox or approval friction around file writes

## Goals

1. Let multiple AI agents share one local checkout safely.
2. Keep history and commits clean when needed.
3. Stay minimal, portable, and easy to drop into an existing project.
