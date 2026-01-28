from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List, Optional
from uuid import uuid4

from services.core.actions import PlaceBuy, PlaceSell
from services.core.market import MarketPath
from services.core.state import State
from services.core.transitions import Action, TransitionResult, apply_action
from services.core.verifier import VerificationError, VerificationResult, verify_transition


@dataclass(frozen=True)
class StepResult:
    step_index: int
    action: Action
    accepted: bool
    errors: List[VerificationError]
    price_context: dict


@dataclass(frozen=True)
class SimulationResult:
    run_id: str
    trajectory: List[State]
    steps: List[StepResult]
    approved: bool
    rejected_step_index: Optional[int]


def _apply_market_price(action: Action, price_context: dict) -> Action:
    price = price_context[action.symbol]
    if isinstance(action, PlaceBuy):
        return replace(action, price=price)
    if isinstance(action, PlaceSell):
        return replace(action, price=price)
    return action


def simulate_plan(
    initial_state: State,
    plan: List[Action],
    market_path: MarketPath,
) -> SimulationResult:
    trajectory: List[State] = [initial_state]
    step_results: List[StepResult] = []
    rejected_index: Optional[int] = None

    for step_index, action in enumerate(plan):
        price_context = market_path.price_context(step_index)
        priced_action = _apply_market_price(action, price_context)
        verification: VerificationResult = verify_transition(trajectory[-1], priced_action)
        step_results.append(
            StepResult(
                step_index=step_index,
                action=priced_action,
                accepted=verification.accepted,
                errors=verification.errors,
                price_context=price_context,
            )
        )

        if not verification.accepted:
            rejected_index = step_index
            break

        transition: TransitionResult = apply_action(trajectory[-1], priced_action)
        trajectory.append(transition.next_state)

    approved = rejected_index is None

    return SimulationResult(
        run_id=str(uuid4()),
        trajectory=trajectory,
        steps=step_results,
        approved=approved,
        rejected_step_index=rejected_index,
    )
