from pathlib import Path
import json
import os

import boto3
import pytest

from services.aws.utils.output_loader import load_outputs


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_AWS_TESTS") != "1",
    reason="AWS tests are disabled by default.",
)


def _invoke_lambda(function_name: str, payload: dict) -> dict:
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(payload).encode("utf-8"),
    )
    return json.loads(response["Payload"].read().decode("utf-8"))


def test_aws_demo_scenarios():
    outputs_path = Path(os.getenv("AWS_OUTPUTS_PATH", "infra/cdk/cdk-outputs.json"))
    outputs = load_outputs(outputs_path)

    simulate_fn = outputs["SimulateFunctionName"]
    execute_fn = outputs["ExecuteFunctionName"]

    reject_payload = {
        "scenario": "scenario_reject.json",
        "state_id": "test_scenario_a",
        "policy_id": "test_policy_a",
    }
    approve_payload = {
        "scenario": "scenario_approve.json",
        "state_id": "test_scenario_b",
        "policy_id": "test_policy_b",
    }

    reject_response = _invoke_lambda(simulate_fn, reject_payload)
    assert reject_response["approved"] is False
    assert reject_response["rejected_step_index"] is not None

    approve_response = _invoke_lambda(simulate_fn, approve_payload)
    assert approve_response["approved"] is True
    assert approve_response["rejected_step_index"] is None

    execution = _invoke_lambda(execute_fn, {"run_id": approve_response["run_id"]})
    assert execution["executed"] is True
