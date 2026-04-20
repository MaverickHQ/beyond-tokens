from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.core.artifacts import ArtifactWriter
from services.core.market import MarketPath
from services.core.persistence import PolicyStore, RunStore, StateStore
from services.core.planner import BedrockPlanner, run_planned_simulation
from services.core.policy.versioning import ensure_policy_metadata
from services.core.state import RiskLimits, State

BASE_DIR = ROOT
DATA_DIR = BASE_DIR / "tmp" / "demo_local_bedrock"
FIXTURE_PATH = BASE_DIR / "examples" / "fixtures" / "trading_path.json"
ARTIFACT_DIR = DATA_DIR / "artifacts"
RUNS_PATH = DATA_DIR / "runs.json"
POLICIES_PATH = DATA_DIR / "policies.json"


def _ensure_enabled() -> bool:
    if os.getenv("ENABLE_BEDROCK_PLANNER") != "1":
        print("Bedrock planner disabled; set ENABLE_BEDROCK_PLANNER=1 to enable.")
        return False
    missing = [
        name
        for name in ("AWS_REGION", "BEDROCK_MODEL_ID")
        if not os.getenv(name)
    ]
    if missing:
        print(
            "Missing required env vars for Bedrock planner: "
            + ", ".join(missing)
            + "."
        )
        return False
    return True


def _format_action(index: int, action: object, market_path: MarketPath) -> str:
    symbol = getattr(action, "symbol", None)
    side = "BUY" if action.__class__.__name__ == "PlaceBuy" else "SELL"
    qty = getattr(action, "quantity", "?")
    price_context = market_path.price_context(index)
    price = price_context.get(symbol) if price_context else None
    if price is None:
        price = getattr(action, "price", 0.0)
    return f"{index + 1}) {side} {qty} {symbol} @ {price}"


def _explain(simulation) -> str:
    if not simulation.steps:
        return ""
    if simulation.approved:
        return simulation.steps[-1].explanation
    rejected_index = simulation.rejected_step_index
    if rejected_index is not None and rejected_index < len(simulation.steps):
        return simulation.steps[rejected_index].explanation
    return simulation.steps[-1].explanation


def main() -> None:
    if not _ensure_enabled():
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    run_store = RunStore(RUNS_PATH)
    policy_store = PolicyStore(POLICIES_PATH)
    artifact_writer = ArtifactWriter(ARTIFACT_DIR)

    policy = ensure_policy_metadata(
        {
            "policy_id": "default",
            "risk_limits": {
                "max_leverage": 2.0,
                "max_position_pct": 0.8,
                "max_position_value": 5_000.0,
            },
        }
    )
    policy_store.save_policy(policy)

    market_path = MarketPath.from_fixture(FIXTURE_PATH)
    planner = BedrockPlanner(
        model_id=os.environ["BEDROCK_MODEL_ID"],
        region_name=os.environ["AWS_REGION"],
    )

    print("Bedrock planner demo: initialized policy and state")

    # Scenario A — constrained state: $50 cash, any buy fails
    state_a = State(
        cash_balance=50.0,
        positions={},
        exposure=0.0,
        risk_limits=RiskLimits(2.0, 0.8, 5_000.0),
    )
    state_summary_a = {
        **state_a.to_dict(),
        "current_prices": market_path.price_context(0),
    }
    planner_result_a, simulation_a = run_planned_simulation(
        planner=planner,
        initial_state=state_a,
        market_path=market_path,
        policy=policy,
        goal=None,
        state_summary=state_summary_a,
    )

    # Scenario B — available capital: $1,000 cash, plan should pass
    state_b = State(
        cash_balance=1_000.0,
        positions={},
        exposure=0.0,
        risk_limits=RiskLimits(2.0, 0.8, 5_000.0),
    )
    state_summary_b = {
        **state_b.to_dict(),
        "current_prices": market_path.price_context(0),
    }
    planner_result_b, simulation_b = run_planned_simulation(
        planner=planner,
        initial_state=state_b,
        market_path=market_path,
        policy=policy,
        goal=None,
        state_summary=state_summary_b,
    )

    print("\nScenario A — constrained state ($50 cash)")
    print(f"Planner: {planner_result_a.planner_name}")
    reasoning_a = (planner_result_a.metadata or {}).get(
        "planner_metadata", {}
    ).get("reasoning", "no reasoning returned")
    print(f"Claude's reasoning: {reasoning_a}")
    print("Plan proposed:")
    for index, action in enumerate(planner_result_a.plan):
        print(f"  {_format_action(index, action, market_path)}")
    decision_a = "approved" if simulation_a.approved else "rejected"
    print(f"Verifier decision: {decision_a}")
    print(f"Explanation: {_explain(simulation_a)}")
    run_store.save_run(simulation_a)
    artifacts_a = artifact_writer.write(simulation_a)
    print(f"Artifacts: trajectory={artifacts_a['trajectory']} "
          f"decision={artifacts_a['decision']}")

    print("\nScenario B — available capital ($1,000 cash)")
    print(f"Planner: {planner_result_b.planner_name}")
    reasoning_b = (planner_result_b.metadata or {}).get(
        "planner_metadata", {}
    ).get("reasoning", "no reasoning returned")
    print(f"Claude's reasoning: {reasoning_b}")
    print("Plan proposed:")
    for index, action in enumerate(planner_result_b.plan):
        print(f"  {_format_action(index, action, market_path)}")
    decision_b = "approved" if simulation_b.approved else "rejected"
    print(f"Verifier decision: {decision_b}")
    print(f"Explanation: {_explain(simulation_b)}")
    run_store.save_run(simulation_b)
    artifacts_b = artifact_writer.write(simulation_b)
    print(f"Artifacts: trajectory={artifacts_b['trajectory']} "
          f"decision={artifacts_b['decision']}")


if __name__ == "__main__":
    main()
