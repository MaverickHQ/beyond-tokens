import pytest

from services.core.planner.bedrock import _action_from_payload, parse_bedrock_plan


def test_parse_bedrock_plan_accepts_valid_payload():
    payload = {
        "plan": [
            {"type": "PlaceBuy", "symbol": "AAPL", "quantity": 1},
            {"type": "PlaceSell", "symbol": "MSFT", "quantity": 2, "price": 200.0},
        ],
        "rationale": "diversify",
    }

    parsed = parse_bedrock_plan(payload)

    assert len(parsed.plan) == 2
    assert parsed.rationale == "diversify"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"plan": "not-a-list"},
        {"plan": [{"type": "Unknown", "symbol": "AAPL", "quantity": 1}]},
        {"plan": [{"type": "PlaceBuy", "symbol": "", "quantity": 1}]},
        {"plan": [{"type": "PlaceBuy", "symbol": "AAPL", "quantity": "x"}]},
        {"plan": [{"type": "PlaceBuy", "symbol": "AAPL", "quantity": 1, "price": "x"}]},
        {"plan": [], "rationale": 123},
    ],
)
def test_parse_bedrock_plan_rejects_invalid_payload(payload):
    with pytest.raises(Exception):
        parse_bedrock_plan(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "Unknown", "symbol": "AAPL", "quantity": 1},
        {"type": "PlaceBuy", "symbol": "", "quantity": 1},
        {"type": "PlaceBuy", "symbol": "AAPL", "quantity": "x"},
        {"type": "PlaceBuy", "symbol": "AAPL", "quantity": 1, "price": "x"},
    ],
)
def test_action_from_payload_rejects_invalid(payload):
    with pytest.raises(ValueError):
        _action_from_payload(payload)