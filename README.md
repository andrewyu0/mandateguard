# MandateGuard

**A constraint-layer eval harness for delegated internet agents.**

MandateGuard verifies whether a specific proposed agent action preserves a specific user's delegated mandate before execution.

## Problem

The web is shifting from human-only interaction to agent traffic: AI agents will increasingly browse, compare, book, pay, submit, and modify state on behalf of users.

That changes the core product question:

> Not just: did the agent complete the task?  
> But: did the agent preserve the user's mandate while completing it?

## Thesis

MandateGuard is a runtime enforcement layer for delegated AI agents.

It sits between an agent's proposed action and execution, checks the action against the user's mandate and runtime context, then returns:

- `ALLOW`
- `BLOCK`
- `ESCALATE`

## Core Loop

```text
User Mandate
  -> Agent Proposed Action
  -> Runtime Context
  -> MandateGuard Validator
  -> Evidence
  -> Block / Allow / Escalate

What Is a Mandate?

A mandate is the user’s bounded delegation contract:

* goal
* budget
* allowed merchants/counterparties
* refundability/reversibility requirements
* forbidden actions
* scope limits

Why Now

As agents move from text generation to tool use and real-world execution, safety shifts from output filtering to runtime action validation.

MandateGuard focuses narrowly on delegated authority:

Is this exact action authorized by this exact user’s mandate?

Analogies

* Stripe Radar for agent actions
* OPA Gatekeeper for delegated authority
* Branch protection before real-world state mutation

MVP Architecture

mandateguard/
  schemas.py          # Mandate, Scenario, Violation, EvalResult
  policy_engine.py    # deterministic mandate checks
  scenarios.py        # scenario loading
  runner.py           # eval runner
  llm_judge.py        # optional semantic evaluator
  metrics.py          # false allow/block, violation recall
