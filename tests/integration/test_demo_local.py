from pathlib import Path

from services.core.actions import PlaceBuy
from services.core.artifacts import ArtifactWriter
from services.core.execution import execute_run
from services.core.market import MarketPath
from services.core.persistence import PolicyStore, RunStore, StateStore
from services.core.simulator import simulate_plan
from services.core.state import RiskLimits, State


def test_reject_scenario_writes_artifacts(tmp_path: Path):
    state_store = StateStore(tmp_path / "state.json")
    run_store = RunStore(tmp_path / "runs.json")
    policy_store = PolicyStore(tmp_path / "policies.json")
    artifact_writer = ArtifactWriter(tmp_path / "artifacts")

    policy_store.save_policy({"policy_id": "default"})
    initial_state = State(
        cash_balance=1_000.0,
        positions={},
        exposure=0.0,
        risk_limits=RiskLimits(2.0, 0.8, 5_000.0),
    )
    state_store.init_state(initial_state)

    market_path = MarketPath.from_fixture(Path("examples/fixtures/trading_path.json"))
    actions = [
        PlaceBuy("AAPL", 1, 0.0),
        PlaceBuy("AAPL", 20, 0.0),
    ]

    result = simulate_plan(initial_state, actions, market_path)
    run_store.save_run(result)
    artifacts = artifact_writer.write(result)

    assert not result.approved
    assert result.rejected_step_index == 1
    assert artifacts["trajectory"].exists()
    assert artifacts["decision"].exists()


def test_approve_scenario_execution_idempotent(tmp_path: Path):
    state_store = StateStore(tmp_path / "state.json")
    run_store = RunStore(tmp_path / "runs.json")
    policy_store = PolicyStore(tmp_path / "policies.json")
    artifact_writer = ArtifactWriter(tmp_path / "artifacts")

    policy_store.save_policy({"policy_id": "default"})
    initial_state = State(
        cash_balance=1_000.0,
        positions={},
        exposure=0.0,
        risk_limits=RiskLimits(2.0, 0.8, 5_000.0),
    )
    state_store.init_state(initial_state)

    market_path = MarketPath.from_fixture(Path("examples/fixtures/trading_path.json"))
    actions = [
        PlaceBuy("AAPL", 1, 0.0),
        PlaceBuy("MSFT", 1, 0.0),
    ]

    result = simulate_plan(initial_state, actions, market_path)
    run_store.save_run(result)
    artifact_writer.write(result)

    execution = execute_run(run_store, state_store, result.run_id)
    second_execution = execute_run(run_store, state_store, result.run_id)

    assert execution.approved
    assert second_execution.message == "Run already executed."
    assert execution.state.to_dict() == second_execution.state.to_dict()
