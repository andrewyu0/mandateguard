# Commands

Project operating commands for MandateGuard / AgentEvalSim.

These are workflow commands used with ChatGPT, Codex CLI, Git, and repo docs.

## go / cockpit

Rehydrate project state.

Use when restarting work.

Output should include:

- current repo state
- active branch
- current phase
- last wins
- next exact action
- risks / blockers
- commands to run

## stop

Create a session-close checkpoint.

Use when ending a work block.

Output should include:

- current state
- completed work
- commits / pushed changes
- next restart action
- risks to remember
- proof-of-work wins

## pace

Check execution tempo.

Use when deciding whether to speed up, pause, narrow scope, or change task.

Output should include:

- time pressure
- current velocity
- risk of drift
- recommended adjustment
- next highest-leverage action

## SAVE

Create a durable engineering log entry.

Use only for decisions worth preserving.

Entry should include:

- timestamp
- type
- title
- decision / change
- rationale
- impact
- artifacts
- owner
- next action

## BACKLOG

Defer an item without losing it.

Use when a thought is useful but not part of the active workstream.

## SSSS

Legacy compact plaintext format.

Use only when screenshot/mobile capture matters.

Default now:

- concise normal prose
- durable repo docs
- searchable Project Sources
- Git-tracked artifacts

## Current operating model

ChatGPT:

- strategic planning
- task routing
- scope control

Codex CLI:

- bounded edits
- implementation assistance

Human:

- review
- test
- stage
- commit
- push

Git:

- durable operational memory

Repo docs:

- canonical source of truth