# MandateGuard / AgentEvalSim — SPEC

Date: 2026-05-15
Workstream: ARCH_agent_eval_harness
Project: hack0516

## 1. Product

| Field | Spec |
|---|---|
| Product | MandateGuard / AgentEvalSim |
| Category | Eval harness for delegated internet agents |
| Core problem | Agents can complete delegated tasks while violating explicit user boundaries: budget, privacy, forbidden actions, account constraints, escalation rules |
| Core thesis | Task success is insufficient. Delegated agents need mandate-fidelity evaluation. |
| Primary users | AI agent builders, eval engineers, safety/product teams, developers integrating tool-using agents |
| MVP artifact | Local runnable eval harness: JSON fixtures -> trace input -> evaluator -> verdict report |
| Non-goals v0 | Full browser automation, production policy engine, multi-agent runtime, hosted dashboard |
| Success criterion | Given a mandate + scenario + action trace, produce a clear pass/fail verdict with evidence spans and violation class |

## 2. Architecture Spine

```text
mandate + scenario + trace -> evaluator -> evidence-backed verdict
```

MandateGuard does not need to build or run an agent in v0. It evaluates whether an agent respected the delegated authority boundary encoded by the user's mandate.

## 3. System Architecture

```text
fixtures/
  mandates/*.json
  scenarios/*.json
  traces/*.json

src/
  models.py          # typed contracts
  evaluator.py       # deterministic rule checks
  taxonomy.py        # violation classes / severity
  report.py          # JSON + Markdown output
  cli.py             # run eval from terminal

outputs/
  reports/*.md
  verdicts/*.json
```

| Component | Responsibility | Input | Output |
|---|---|---|---|
| Scenario | Defines delegated task and trap conditions | JSON fixture | Task context |
| UserMandate | Encodes allowed/forbidden behavior | JSON fixture | Constraint set |
| ActionTrace | Records agent behavior | JSON trace | Event stream |
| Evaluator | Checks trace against mandate | mandate + scenario + trace | verdict |
| Taxonomy | Normalizes violation types | detected violations | class/severity |
| Reporter | Makes result reviewable | verdict object | Markdown/JSON |
| CLI | Runs local eval loop | file paths | terminal + files |

## 4. Eval Loop

```text
1. Load scenario
2. Load user mandate
3. Load agent trace
4. Validate schema
5. Normalize trace events
6. Run deterministic checks
7. Map failures to violation taxonomy
8. Assign severity
9. Emit JSON verdict
10. Emit Markdown report
```

| Stage | Function | Example check |
|---|---|---|
| Schema validation | Ensure inputs are well-formed | trace.scenario_id == scenario.id |
| Permission check | Detect forbidden tool/action usage | purchase_flight without confirmation |
| Constraint check | Compare event fields to mandate limits | price_usd > max_budget_usd |
| Privacy check | Detect restricted data exposure | calendar details sent externally |
| Escalation check | Verify agent asked user when required | no ask_user before purchase |
| Evidence extraction | Point to exact trace event | event_idx = 2 |
| Verdict generation | Aggregate pass/fail | critical violation -> fail |

## 5. MVP Scope

### Must Build

| Priority | Item | Reason |
|---:|---|---|
| P0 | JSON schemas for mandate/scenario/trace/verdict | Core contract |
| P0 | 3 fixture scenarios | Demo breadth |
| P0 | Deterministic evaluator | Trustworthy v0 |
| P0 | CLI runner | Fast demo path |
| P0 | Markdown report | Judge/user-readable |
| P1 | Severity mapping | Product polish |
| P1 | Unit tests | Engineering credibility |
| P1 | README with demo command | Runnable artifact |

### Explicit Non-Goals v0

| Avoid | Why |
|---|---|
| Browser automation | Too much surface area for v0 |
| Real payment/email integrations | Risk + time sink |
| Database | JSON fixtures are enough |
| Web dashboard | CLI + Markdown sufficient for v0 |
| LLM judge first | Makes product feel vague/unverifiable |
| Multi-agent orchestration | Not necessary for mandate-fidelity thesis |

## 6. MVP Demo Scenarios

| Scenario | Mandate trap | Expected eval signal |
|---|---|---|
| Travel booking | Budget + purchase confirmation | Detect overspend / unauthorized purchase |
| Email assistant | Privacy + deletion boundary | Detect sending/deleting forbidden content |
| Shopping agent | Brand/budget/substitution constraint | Detect unauthorized substitution or upsell |

Recommended first fixture:

```text
travel_booking_budget_violation
```

Reason: easiest to understand quickly. Money + permission boundary is obvious.

## 7. Architecture Decisions

| ID | Decision | Rationale |
|---|---|---|
| ADR-001 | File fixtures first | Git-reviewable, fast, transparent |
| ADR-002 | Deterministic evaluator first | Avoids vague LLM-judge product smell |
| ADR-003 | Trace as source of truth | Makes verdict explainable |
| ADR-004 | Evidence spans required | Prevents hand-wavy eval output |
| ADR-005 | Severity taxonomy explicit | Makes product feel safety/eval-grade |
| ADR-006 | CLI before UI | Fastest path to runnable credibility |

## 8. Suggested Repository Contract

```text
mandateguard/
  README.md
  SPEC.md
  docs/
    SPEC.md
    EVAL_SCHEMA.md
  fixtures/
    mandates/
      travel_budget.json
      email_privacy.json
      shopping_budget.json
    scenarios/
      travel_booking.json
      email_cleanup.json
      shopping_agent.json
    traces/
      travel_good.json
      travel_bad.json
      email_bad.json
  src/
    mandateguard/
      __init__.py
      models.py
      evaluator.py
      taxonomy.py
      report.py
      cli.py
  tests/
    test_evaluator.py
  outputs/
    .gitkeep
```

## 9. CLI Contract

```bash
python -m mandateguard.cli \
  --scenario fixtures/scenarios/travel_booking.json \
  --mandate fixtures/mandates/travel_budget.json \
  --trace fixtures/traces/travel_bad.json \
  --out outputs/travel_bad_report.md
```

Expected terminal output:

```text
MandateGuard verdict: FAIL

Violations:
- critical unauthorized_transaction at event[2]
- high budget_violation at event[2]

Report written: outputs/travel_bad_report.md
```

## 10. Open Questions

| Question | Working decision |
|---|---|
| Real traces or synthetic traces first? | Start synthetic; keep trace format compatible with real agent logs later |
| Does v0 require an LLM judge? | No. Add optional semantic evaluator after deterministic path works |
| Should mandate be policy-like or natural-language-first? | Structured JSON v0; natural-language ingestion later |
| What is the scoring model? | Binary pass/fail + severity first; numeric score later |
| Is product MandateGuard or AgentEvalSim? | MandateGuard = product; AgentEvalSim = internal harness descriptor |
| Minimal wow demo? | Same task, two traces: compliant vs violating; report catches violation with evidence |

## 11. HANDOFF

```text
HANDOFF_ARCH_20260515

Workstream:
ARCH_agent_eval_harness

Product:
MandateGuard = eval harness for delegated internet agents.

Core architecture:
JSON fixtures -> mandate/scenario/trace schemas -> deterministic evaluator -> violation taxonomy -> evidence-backed verdict -> Markdown/JSON report.

Key decision:
Build deterministic local eval harness first. Do not start with browser automation, UI, DB, or LLM judge.

Core data model:
Scenario, UserMandate, AgentActionTrace, EvaluatorVerdict, Violation, EvidenceSpan, RemediationNote.

MVP:
- 3 scenarios: travel booking, email assistant, shopping agent
- good/bad traces
- deterministic evaluator
- CLI runner
- Markdown report
- README demo command
- unit tests

Highest-leverage next action:
BUILD should implement repo skeleton and first runnable travel-budget eval.

Risk:
Overengineering into agent runtime/browser automation before proving eval substrate.

Recommended next workstream:
BUILD_repo_execution
```
