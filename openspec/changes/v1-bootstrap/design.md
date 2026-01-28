# v1 Bootstrap Design

## Architecture
- Core domain implements deterministic simulator and verifier.
- API exposes `/simulate`, `/verify`, and `/simulate-verify` with strict error format.
- Infra orchestrates simulate+verify via Step Functions.
