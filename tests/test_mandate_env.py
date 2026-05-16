# tests/test_mandate_env.py

from mandateguard.envs.mandate_env import MandateEnv


class DummyEvaluator:
    def evaluate(self, scenario, trace):
        return {"verdict": trace["expected_verdict"]}


def test_mandate_env_pass_reward():
    env = MandateEnv(
        scenario={"mandate": {"max_total_usd": 500}},
        evaluator=DummyEvaluator(),
    )

    obs, info = env.reset()
    assert obs["mandate"]["max_total_usd"] == 500

    obs, reward, terminated, truncated, info = env.step({"expected_verdict": "pass"})

    assert reward == 1
    assert terminated is True
    assert truncated is False
    assert info["verdict"]["verdict"] == "pass"


def test_mandate_env_fail_reward():
    env = MandateEnv(
        scenario={"mandate": {"max_total_usd": 500}},
        evaluator=DummyEvaluator(),
    )

    env.reset()
    _, reward, terminated, _, info = env.step({"expected_verdict": "fail"})

    assert reward == -1
    assert terminated is True
    assert info["passed"] is False
