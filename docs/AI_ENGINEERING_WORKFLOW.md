# AI Engineering Workflow

Operational notes from building MandateGuard / AgentEvalSim using ChatGPT, Codex CLI, Git, and repo-backed documentation during a hackathon.
The goal is not maximal automation.
The goal is:

- fast execution
- bounded delegation
- human review gates
- durable operational memory
- low workflow drift

---

# Core Model


| Role            | Responsibility                          |
| --------------- | --------------------------------------- |
| ChatGPT         | strategic planning / task decomposition |
| Codex CLI       | bounded implementation executor         |
| Human           | review, testing, staging, commit, push  |
| Git             | durable operational memory              |
| Repo docs       | externalized cognition                  |
| Project Sources | searchable context mirror               |


---

# Core Principles

## 1. Bounded delegation

AI agents should receive:

- one scoped task
- clear file boundaries
- explicit stop conditions
Bad:
  > "Refactor the project."
  > Good:
  > "Update README top section only. Do not edit any other files."

---

## 2. Human mutation gates

AI may edit files.
Human reviews before:

- `git add`
- `git commit`
- `git push`
- destructive shell commands
The human remains responsible for repository state.

---

## 3. Repo docs are durable memory

Important operational knowledge should live in:

- `README.md`
- `docs/TASKS.md`
- `docs/COMMANDS.md`
- `docs/DECISIONS.md`
- `docs/AI_ENGINEERING_WORKFLOW.md`
Chat memory is useful but non-authoritative.
Git-tracked docs are the canonical source of truth.

---

## 4. Read-only commands can be safely batched

Typical review loop:

```
pwd
git status --short
git diff
python -m pytest
```

Mutation commands are executed only after review.

---

## **5. Separate execution from verification**

Preferred workflow:

- Codex edits
- human inspects
- human stages
- human commits
- human pushes

This preserves:

- auditability
- intent verification
- operational awareness

---

# **CLI-First Workflow**

Terminal-first workflows reduce:

- context switching
- UI dependency
- delegation friction

CLI tools compose naturally with:

- AI agents
- Git
- automation
- remote execution
- logs
- structured text workflows

However:  
the goal is not terminal maximalism.

Use the lowest-friction interface for the task.

---

# **Goblin Mode Mobile (GMM)**

GMM = mobile-first supervision of desktop/CLI execution.

Pattern:

```text
ChatGPT
  ->
Codex CLI
  ->
Git / Repo Docs
  ->
Mobile supervision
```

Observed benefits:

- async execution
- low-friction iteration
- remote review
- persistent operational continuity

---

# **Workflow Evolution**

Initial workflow optimization targeted:

- screenshot UX
- mobile readability
- temporary capture

Later evolution shifted toward:

- durable repo docs
- searchable artifacts
- Git-backed operational memory
- Project Sources integration

This became the more scalable system:

```text
chat
  ->
repo docs
  ->
git
  ->
project sources
  ->
searchable operational memory
```

Instead of:

```text
chat
  ->
screenshots
  ->
manual re-upload
```

---

# **Practical Rules**

## **Safe**

- `git status`
- `git diff`
- `pytest`
- bounded Codex edits

## **Human review required**

- `git add`
- `git commit`
- `git push`

## **Never blind-paste**

- `rm`
- `git reset --hard`
- `git clean`
- force push
- destructive shell commands

---

# **Example Codex Prompt**

```text
Update README top section only.

Add:
- one-sentence thesis
- one-command demo
- short sample output

Do not edit any other files.
Do not run git commands.
Stop after editing.
```

---

# **Main Insight**

The important shift was realizing that:  
AI-assisted engineering works best when:

- delegation boundaries are explicit
- operational memory is durable
- review gates remain human-controlled
- workflows are repo-centric instead of chat-centric

---

# **Misc**

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

---

# Heredoc / Terminal-Native Artifact Flow

A major workflow realization was distinguishing between:

- interactive editors
- shell-driven file generation

Example:

```bash
cat > pitch_cheatcard.html <<'EOF'
...content...
EOF
open pitch_cheatcard.html
```

This is not an editor.

No IDE/nano/vim process is launched.

Instead:

1. shell enters heredoc input mode
2. terminal captures multiline stdin
3. `cat` streams text directly into a file
4. `EOF` terminates the stream
5. shell returns to command mode
6. browser/editor renders the artifact

Conceptually:

```text
stdin -> file
```

not:

```text
editor -> save file
```

Key realization:
AI-generated content pairs extremely well with heredoc workflows because the content already exists as a complete blob.

This enables an extremely low-friction loop:

```text
LLM output
  ->
terminal
  ->
artifact
  ->
browser/render
```

Benefits:
- zero IDE/context switching
- terminal-native
- composable
- automation-friendly
- fast artifact generation
- works naturally with AI tooling

Important distinction:
heredocs do not replace editors.

Use:
- heredoc for generated/pasted blobs
- nano/vim for manual editing
- IDEs for larger iterative coding tasks

This reflects a broader Unix mental model:
- shells orchestrate processes
- programs consume streams
- files are text sinks/sources
- process boundaries are explicit

This became an important part of the terminal-native / AI-native engineering workflow.