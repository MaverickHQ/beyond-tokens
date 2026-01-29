# Changelog

## v2.2.0 — AWS Planner Execution
- AWS simulate handler supports planner mode for mock/optional Bedrock.
- New AWS planner demo and smoke scripts + Makefile targets.
- Planner metadata persisted and validated in AWS integration tests.
- CDK wiring for gated Bedrock invoke permissions.

## v2.0.0 — Provider-neutral Planner
- Planner interface with deterministic mock planner
- Planner proposals always verified by the world model
- Planner metadata persisted alongside runs and artifacts

## v1.1.1 — Explainability, State Deltas, Policy Versioning
- Deterministic explanation strings for accepted and rejected steps
- Deltas artifact for step-by-step state changes
- Policy hash/version embedded in decisions and run metadata

## v1.1.0 — Executable World Model on AWS
- Deployed Minimum Viable World Model using AWS Lambda, DynamoDB, and S3
- Idempotent simulation and execution handlers
- Cloud artifacts for trajectories and decisions
- Smoke tests and end-to-end AWS demos

## v1.0.0 — Minimum Viable World Model (Local)
- Explicit state, actions, transitions, and verification
- Deterministic market paths and plan simulation
- Local persistence and artifact generation
- End-to-end demo with approval/rejection flows