from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from services.core.simulator import SimulationResult


@dataclass
class ArtifactWriter:
    output_dir: Path

    def write(self, result: SimulationResult) -> Dict[str, Path]:
        run_dir = self.output_dir / result.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        trajectory_path = run_dir / "trajectory.json"
        decision_path = run_dir / "decision.json"
        deltas_path = run_dir / "deltas.json"

        trajectory_payload = {
            "run_id": result.run_id,
            "trajectory": [state.to_dict() for state in result.trajectory],
            "steps": [
                {
                    "step_index": step.step_index,
                    "action": {
                        "type": step.action.__class__.__name__,
                        "symbol": step.action.symbol,
                        "quantity": step.action.quantity,
                        "price": step.action.price,
                    },
                    "price_context": step.price_context,
                    "accepted": step.accepted,
                    "errors": [
                        {"code": error.code, "message": error.message}
                        for error in step.errors
                    ],
                    "explanation": step.explanation,
                    "state_delta": step.state_delta,
                }
                for step in result.steps
            ],
        }

        decision_payload = {
            "run_id": result.run_id,
            "approved": result.approved,
            "rejected_step_index": result.rejected_step_index,
            "errors": [
                {
                    "step_index": step.step_index,
                    "errors": [
                        {"code": error.code, "message": error.message}
                        for error in step.errors
                    ],
                }
                for step in result.steps
                if step.errors
            ],
            "planner": {
                "planner_name": result.planner_name,
                "planner_metadata": result.planner_metadata,
            },
            "policy": {
                "policy_id": result.policy_id,
                "policy_version": result.policy_version,
                "policy_hash": result.policy_hash,
            },
        }

        deltas_payload = {
            "run_id": result.run_id,
            "deltas": [step.state_delta for step in result.steps],
        }

        trajectory_path.write_text(json.dumps(trajectory_payload, indent=2))
        decision_path.write_text(json.dumps(decision_payload, indent=2))
        deltas_path.write_text(json.dumps(deltas_payload, indent=2))

        return {
            "trajectory": trajectory_path,
            "decision": decision_path,
            "deltas": deltas_path,
        }
