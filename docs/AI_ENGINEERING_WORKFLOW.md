# AI Engineering Workflow

## Roles

ChatGPT is the control plane. It keeps the broader project context, helps shape tasks, and decides what should be handed to Codex.

Codex CLI is the execution assistant. It performs one bounded repo task at a time, edits files, and reports exactly what changed.

The human is the reviewer and committer. The human approves direction, reviews changes, runs final judgment, and decides what enters history.

## Durable Memory

Repo docs are the durable memory for the project. Decisions, specs, workflows, and task state should be captured in versioned files so future runs do not rely on chat history alone.

Project Sources are the searchable mirror. They provide fast recall and cross-document lookup, but the repo remains the source of truth.

## Operating Rules

Use one bounded task per Codex run. Each run should have a clear file scope, expected output, and stopping point.

Batch safe read-only commands when useful. Reads can be grouped to gather context quickly, but command output should stay focused and relevant.

Keep manual mutation gates. File edits, dependency changes, migrations, commits, pushes, and destructive operations should happen only when explicitly requested.

Do not run blind destructive commands. Avoid commands that delete, reset, overwrite, or rewrite state unless the human has clearly asked for that exact action.

Codex does not run git commands unless asked. Status, diff, add, commit, branch, reset, checkout, pull, push, and related commands require an explicit request.

Stop after the requested edit. After completing the bounded task, Codex summarizes changed files and waits for the next instruction.
