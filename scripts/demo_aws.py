from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import boto3

from services.aws.utils.output_loader import load_outputs

BASE_DIR = ROOT
OUTPUTS_PATH = Path(os.environ.get("AWS_OUTPUTS_PATH", BASE_DIR / "infra" / "cdk" / "cdk-outputs.json"))
SCENARIO_DIR = BASE_DIR / "examples" / "scenarios"


def invoke_lambda(function_name: str, payload: dict) -> dict:
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(payload).encode("utf-8"),
    )
    return json.loads(response["Payload"].read().decode("utf-8"))


def main() -> None:
    outputs = load_outputs(OUTPUTS_PATH)

    simulate_fn = outputs["SimulateFunctionName"]
    execute_fn = outputs["ExecuteFunctionName"]

    print("Scenario A (expected rejection)")
    reject_response = invoke_lambda(
        simulate_fn,
        {
            "scenario": "scenario_reject.json",
            "state_id": "demo_scenario_a",
            "policy_id": "demo_policy_a",
        },
    )
    if "run_id" not in reject_response:
        print("Simulate response did not include run_id. Raw response:")
        print(json.dumps(reject_response, indent=2))
        return
    print(
        json.dumps(
            {
                "run_id": reject_response["run_id"],
                "approved": reject_response["approved"],
                "rejected_step_index": reject_response["rejected_step_index"],
                "errors_summary": reject_response.get("errors_summary", []),
                "artifact_s3_prefix": reject_response.get("artifact_s3_prefix"),
            },
            indent=2,
        )
    )

    print("\nScenario B (expected approval)")
    approve_response = invoke_lambda(
        simulate_fn,
        {
            "scenario": "scenario_approve.json",
            "state_id": "demo_scenario_b",
            "policy_id": "demo_policy_b",
        },
    )
    if "run_id" not in approve_response:
        print("Simulate response did not include run_id. Raw response:")
        print(json.dumps(approve_response, indent=2))
        return
    print(
        json.dumps(
            {
                "run_id": approve_response["run_id"],
                "approved": approve_response["approved"],
                "rejected_step_index": approve_response["rejected_step_index"],
                "artifact_s3_prefix": approve_response.get("artifact_s3_prefix"),
            },
            indent=2,
        )
    )

    execution = invoke_lambda(execute_fn, {"run_id": approve_response["run_id"]})
    print("\nExecution summary")
    print(
        json.dumps(
            {
                "run_id": execution["run_id"],
                "executed": execution["executed"],
                "state_summary": execution.get("state_summary"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
