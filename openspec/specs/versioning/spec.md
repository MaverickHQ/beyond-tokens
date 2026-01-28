# Versioning Spec

## Staging Modes
- **v1 deterministic**: default mode, always enabled.
- **v1.1 Bedrock proposer**: optional, disabled by default.
- **v2 latent simulator**: optional, disabled by default.

## Selection
- The active mode is chosen by configuration and must be surfaced in `/health`.
- Any non-default mode must be explicitly enabled and logged.
