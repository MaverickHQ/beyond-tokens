from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Optional

from services.core.actions import PlaceBuy, PlaceSell
from services.core.planner.base import Planner
from services.core.planner.types import PlannerError, PlannerResult
from services.core.transitions import Action


@dataclass(frozen=True)
class BedrockPlanResponse:
    plan: List[Dict[str, object]]
    rationale: Optional[str] = None


def parse_bedrock_plan(payload: Dict[str, object]) -> BedrockPlanResponse:
    if "plan" not in payload:
        raise ValueError("Missing 'plan' in Bedrock response.")
    plan = payload["plan"]
    if not isinstance(plan, list):
        raise ValueError("'plan' must be a list.")
    for item in plan:
        if not isinstance(item, dict):
            raise ValueError("Each plan item must be an object.")
        _action_from_payload(item)

    rationale = payload.get("rationale")
    if rationale is not None and not isinstance(rationale, str):
        raise ValueError("'rationale' must be a string if provided.")
    return BedrockPlanResponse(plan=plan, rationale=rationale)


def _action_from_payload(item: Dict[str, object]) -> Action:
    action_type = item.get("type")
    if action_type not in {"PlaceBuy", "PlaceSell"}:
        raise ValueError(f"Unknown action type: {action_type}")
    symbol = item.get("symbol")
    quantity = item.get("quantity")
    if not isinstance(symbol, str) or not symbol:
        raise ValueError("Action 'symbol' must be a non-empty string.")
    if not isinstance(quantity, (int, float)):
        raise ValueError("Action 'quantity' must be a number.")
    price = item.get("price", 0.0) or 0.0
    if not isinstance(price, (int, float)):
        raise ValueError("Action 'price' must be a number.")
    if action_type == "PlaceBuy":
        return PlaceBuy(symbol=symbol, quantity=float(quantity), price=float(price))
    return PlaceSell(symbol=symbol, quantity=float(quantity), price=float(price))


class BedrockPlanner(Planner):
    name = "bedrock"

    def __init__(self, model_id: str, region_name: str) -> None:
        self._model_id = model_id
        self._region_name = region_name

    def propose(self, state_summary: Dict[str, object], policy: Dict[str, object], goal: str) -> PlannerResult:
        prompt = {
            "goal": goal,
            "state": state_summary,
            "policy": policy,
            "instructions": (
                "Return JSON with 'plan' as a list of actions. Each action:"
                " {'type': 'PlaceBuy'|'PlaceSell', 'symbol': str, 'quantity': number, 'price': number (optional)}."
                " Optionally include 'rationale'."
            ),
        }

        try:
            import boto3

            client = boto3.client("bedrock-runtime", region_name=self._region_name)
            response = client.invoke_model(
                modelId=self._model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps({"prompt": json.dumps(prompt)}),
            )
            raw_body = response.get("body")
            body_bytes = raw_body.read() if hasattr(raw_body, "read") else raw_body
            payload = json.loads(body_bytes.decode("utf-8"))
            parsed = parse_bedrock_plan(payload)
            actions = [_action_from_payload(item) for item in parsed.plan]
        except Exception as exc:
            return PlannerResult(
                plan=[],
                planner_name=self.name,
                metadata={"model_id": self._model_id, "error": str(exc)},
                error=PlannerError(code="bedrock_error", message=str(exc)),
            )

        metadata = {
            "model_id": self._model_id,
            "region": self._region_name,
        }
        request_id = response.get("ResponseMetadata", {}).get("RequestId")
        if request_id:
            metadata["request_id"] = request_id
        if parsed.rationale:
            metadata["rationale"] = parsed.rationale

        return PlannerResult(plan=actions, planner_name=self.name, metadata=metadata)