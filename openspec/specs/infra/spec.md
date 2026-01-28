# Infra Spec

## Required Infrastructure
- AWS Step Functions for orchestration of simulate+verify.
- Persistent storage for artifacts and state (S3 or DynamoDB).
- API gateway or load balancer fronting the API service.

## Orchestration
- The **simulate** step must always precede **verify**.
- Failure in verify returns a failure response and still records artifacts.

## Staging
- **v1 deterministic** is the default and always enabled.
- **v1.1 Bedrock proposer** is optional and **disabled by default**.
- **v2 latent simulator** is optional and **disabled by default**.
