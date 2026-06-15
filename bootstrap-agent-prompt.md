# Bootstrap Agent — Coordinated Swarm Workflow Prompt

You are joining an existing project that uses the decentralized multi-agent coordination system.
Your job is to pick up work from the shared task board, coordinate via the manifest, and complete tasks safely without overlapping other agents.

## 1. First actions on entering the project

1. Read `AGENTS.md` if it exists.
2. Read `.agent-tasks.json` with:
   ```
   python3 scripts/tasks.py list
   ```
3. Read current lock state with:
   ```
   python3 scripts/status.py
   ```
4. Identify one task you can claim. Do not pick a task marked `blocked` unless you can unblock it.

## 2. Claiming a task

```
python3 scripts/tasks.py claim <task-id>
```

- The task board will mark it `in_progress` and record your agent ID.
- Check `depends_on` before claiming. Do not claim tasks that depend on incomplete work.

## 3. Acquiring file locks

Before editing any file listed in the task’s `files` array:

```
python3 scripts/lock.py <file1> <file2> ... "<short reason>"
```

Rules:
- Lock every file you plan to modify.
- Do not edit files you have not locked.
- If a lock fails because another agent holds it, stop. Choose a different task.

## 4. Performing the work

- Make the changes described in the task.
- Keep changes minimal and focused.
- Do not refactor unrelated files.
- Do not delete or rewrite large blocks without clear justification.

## 5. Verifying your work

Before marking a task complete, you MUST verify both the filesystem and the compile/test state:

- **Filesystem**: Every declared task file must exist and be non-empty.
- **Build/Compile**: Ensure the project builds successfully (e.g. `npm run build`, `docker compose build`, or `npx tsc --noEmit`).
- **Tests**: Run the test suites (e.g. `pytest`, `npm test`, `playwright test`) and ensure all tests pass. 
- **CRITICAL**: The `verify-complete` CLI script only checks file existence and size. It does NOT replace running compiler, build, and test tools. You must run these verification tools manually before marking the task complete.

## 6. Completing and unlocking

```
python3 scripts/tasks.py verify-complete <task-id>
python3 scripts/unlock.py <file1> <file2> ...
```

- `verify-complete` will fail if any declared file is missing or empty.
- Only unlock the files you locked.
- Do not unlock files held by other agents.

## 7. Handling blockers

If you cannot complete a task:

1. Update the task board:
   ```
   python3 scripts/tasks.py update <task-id> --status blocked --note "<reason>"
   ```
2. Unlock any files you locked.
3. Stop. Do not silently abandon work.

## 8. Heartbeat for long tasks

If you expect to hold a lock for more than a few minutes:

```
python3 scripts/heartbeat.py <file1> <file2> ...
```

This extends the lock so it is not treated as stale.

## 9. Coordination rules

- One agent per task at a time.
- No shared editor state; treat the manifest as the source of truth.
- Do not edit `.agent-manifest.json`, `.agent-status.md`, or `.agent-tasks.json` directly — use the provided scripts.
- If you see a stale lock older than 10 minutes, use:
  ```
  python3 scripts/force-unlock.py <file>
  ```

## 10. End of session

When you are done for this session:
1. Finish or block any claimed tasks.
2. Unlock all files you locked.
3. Leave the task board in an accurate state.
