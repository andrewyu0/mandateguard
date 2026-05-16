# mandateguard/envs/mandate_env.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MandateEnvResult:
    observation: dict[str, Any]
    reward: int
    terminated: bool
    truncated: bool
    info: dict[str, Any]


class MandateEnv:
    """
    Minimal Gymnasium-style one-shot env wrapper.

    No RL training.
    No simulator loop.
    No evaluator refactor.

    reset() returns the scenario/mandate observation.
    step(trace) evaluates exactly one trace and terminates.

    OPTIONAL README NOTE:

    ## Gymnasium-style environment wrapper

    MandateGuard can be used as a lightweight
    one-shot simulation environment:

    - observation = scenario + mandate
    - action = candidate agent trace
    - reward = +1 for mandate pass, -1 for violation
    - terminated = true after one trace evaluation
    - info["verdict"] contains the evaluator result

    This is eval/simulation infrastructure,
    not RL training.
    
    """

    metadata = {"render_modes": []}

    def __init__(self, scenario: dict[str, Any], evaluator: Any):
        self.scenario = scenario
        self.evaluator = evaluator
        self._terminated = False

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        self._terminated = False
        observation = {
            "scenario": self.scenario,
            "mandate": self.scenario.get("mandate", {}),
        }
        return observation, {}

    def step(
        self,
        trace: dict[str, Any],
    ) -> tuple[dict[str, Any], int, bool, bool, dict[str, Any]]:
        if self._terminated:
            raise RuntimeError("MandateEnv is terminal. Call reset().")

        verdict = self.evaluator.evaluate(self.scenario, trace)

        passed = _is_pass(verdict)
        reward = 1 if passed else -1

        self._terminated = True

        observation = {
            "scenario": self.scenario,
            "trace": trace,
            "verdict": verdict,
        }

        info = {
            "verdict": verdict,
            "passed": passed,
        }

        return observation, reward, True, False, info


def _is_pass(verdict: Any) -> bool:
    if isinstance(verdict, dict):
        return verdict.get("verdict") == "pass" or verdict.get("passed") is True

    return (
        getattr(verdict, "verdict", None) == "pass"
        or getattr(verdict, "passed", False) is True
    )