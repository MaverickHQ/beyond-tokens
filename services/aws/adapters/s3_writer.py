from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict

import boto3

from services.core.simulator import SimulationResult


@dataclass
class S3ArtifactWriter:
    bucket_name: str

    def __post_init__(self) -> None:
        self._client = boto3.client("s3")

    def write(self, result: SimulationResult) -> Dict[str, str]:
        prefix = f"artifacts/{result.run_id}"
        trajectory_key = f"{prefix}/trajectory.json"
        decision_key = f"{prefix}/decision.json"
        deltas_key = f"{prefix}/deltas.json"

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

        self._client.put_object(
            Bucket=self.bucket_name,
            Key=trajectory_key,
            Body=json.dumps(trajectory_payload, indent=2).encode("utf-8"),
        )
        self._client.put_object(
            Bucket=self.bucket_name,
            Key=decision_key,
            Body=json.dumps(decision_payload, indent=2).encode("utf-8"),
        )
        self._client.put_object(
            Bucket=self.bucket_name,
            Key=deltas_key,
            Body=json.dumps(deltas_payload, indent=2).encode("utf-8"),
        )

        return {
            "artifact_prefix": prefix,
            "trajectory_key": trajectory_key,
            "decision_key": decision_key,
            "deltas_key": deltas_key,
        }
