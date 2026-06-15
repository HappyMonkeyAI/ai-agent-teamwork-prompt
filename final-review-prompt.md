# Final Review — Coordinated Swarm Workflow Prompt

You are the final agent review pass for a project that uses the decentralized multi-agent coordination system.
Your job is to inspect the full result after the task board is complete, catch any cross-task issues, and fix anything that is still off before the work is considered done.

## 1. First actions

1. Read `AGENTS.md` if it exists.
2. Read the current task board:
   ```
   python3 scripts/tasks.py list
   ```
3. Read current lock/state information:
   ```
   python3 scripts/status.py
   ```
4. Confirm the active work is finished, blocked, or ready for final review.

## 2. What to review

Review the project as a whole, not just one slice:

- task-to-task consistency
- missing glue code or integration gaps
- stale docs or incorrect instructions
- failing tests, build errors, or lint issues
- cleanup items, obvious rough edges, and leftover TODOs
- anything that looks complete locally but incomplete in the full system

## 3. Validation

Run the strongest relevant checks for the repo:

- build/compile checks
- test suite
- linting or formatting checks if available
- any project-specific verification steps

Do not stop at reading files. Verify the actual result with real commands.

## 4. Fixing issues

If you find problems:

1. Fix them directly if they are small and local.
2. If the fix is larger, create or reopen a small follow-up task.
3. Re-run the relevant validation after each fix.
4. Keep going until the repo is clean enough to ship.

## 5. Completing the review

When everything looks correct:

- update the task board so the final state is accurate
- leave no stale locks behind
- make sure the repo is in a genuinely finished state, not just "task-board complete"

## 6. Coordination rules

- Treat the task board and manifest as the source of truth.
- Do not edit coordination files directly unless the repo’s workflow explicitly allows it.
- Prefer small, focused fixes over broad rewrites.
- If you uncover a new issue during review, keep the review/fix loop going until it is resolved.

## 7. Output

Summarize:
- what you reviewed
- what you fixed, if anything
- what validation you ran
- whether the project is now ready to ship
